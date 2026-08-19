#!/usr/bin/env python3
"""
UpDesk Patch Script
Applies all customizations to the RustDesk 1.3.8 source for UP Tech's branded build.

Environment variables (set by GitHub Actions):
  UPDESK_SERVER  - e.g. updesk.uptech.eti.br
  UPDESK_KEY     - e.g. qiTu+VUce5K1VE3JZJeHS3+8MY96ihiiG40pA9RAMCc=
"""

import os
import shutil
import sys

# Windows cp1252 nao suporta emoji — forca UTF-8 no stdout
sys.stdout.reconfigure(encoding="utf-8")

BASE = "rustdesk-src"
SERVER = os.environ.get("UPDESK_SERVER", "updesk.uptech.eti.br")
KEY = os.environ.get("UPDESK_KEY", "qiTu+VUce5K1VE3JZJeHS3+8MY96ihiiG40pA9RAMCc=")

errors = 0

def patch(path, old, new, label):
    global errors
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌  [{label}] File not found: {path}")
        errors += 1
        return False
    if old not in content:
        print(f"⚠️  [{label}] Target string not found in {path}")
        print(f"    Looking for: {old[:80]!r}")
        errors += 1
        return False
    content = content.replace(old, new, 1)
    with open(path, "w", encoding="utf-8", errors="replace") as f:
        f.write(content)
    print(f"✅  [{label}]")
    return True


# ─── Patch 1: hbb_common — change default fallback rendezvous server ──────────
patch(
    os.path.join(BASE, "libs/hbb_common/src/config.rs"),
    '&["rs-ny.rustdesk.com"]',
    f'&["{SERVER}"]',
    "hbb_common: default rendezvous server"
)


# ─── Patch 2: src/common.rs — inject server + key + conn-type at startup ──────
# We inject a block at the top of load_custom_client()
INJECT_RUST = (
    "    // UpDesk: receiver-only mode + hardcoded UP Tech server\n"
    "    {\n"
    "        config::HARD_SETTINGS\n"
    "            .write().unwrap()\n"
    '            .insert("conn-type".to_string(), "incoming".to_string());\n'
    "        let mut ow = config::OVERWRITE_SETTINGS.write().unwrap();\n"
    f'        ow.insert("custom-rendezvous-server".to_string(), "{SERVER}".to_string());\n'
    f'        ow.insert("key".to_string(), "{KEY}".to_string());\n'
    f'        ow.insert("relay-server".to_string(), "{SERVER}".to_string());\n'
    "    }\n"
    '    *hbb_common::config::APP_NAME.write().unwrap() = "UpDesk".to_string();\n'
)

OLD_LOAD = "pub fn load_custom_client() {\n    #[cfg(debug_assertions)]"
NEW_LOAD  = "pub fn load_custom_client() {\n" + INJECT_RUST + "    #[cfg(debug_assertions)]"

patch(
    os.path.join(BASE, "src/common.rs"),
    OLD_LOAD,
    NEW_LOAD,
    "common.rs: load_custom_client injection"
)


# ─── Patch 3: flutter/windows/CMakeLists.txt — rename binary ──────────────────
patch(
    os.path.join(BASE, "flutter/windows/CMakeLists.txt"),
    'set(BINARY_NAME "rustdesk")',
    'set(BINARY_NAME "updesk")',
    "CMakeLists: binary name → updesk"
)


# ─── Patch 4: Runner.rc — Windows executable metadata ─────────────────────────
rc_path = os.path.join(BASE, "flutter/windows/runner/Runner.rc")
try:
    with open(rc_path, "r", encoding="utf-8", errors="replace") as f:
        rc = f.read()

    rc = rc.replace('"Purslane Ltd"',             '"UP Tech"')
    rc = rc.replace('"RustDesk Remote Desktop"',  '"UpDesk - Suporte Remoto UP Tech"')
    rc = rc.replace('"rustdesk"',                 '"updesk"')
    rc = rc.replace('"rustdesk.exe"',             '"updesk.exe"')
    rc = rc.replace('"RustDesk"',                 '"UpDesk"')

    with open(rc_path, "w", encoding="utf-8", errors="replace") as f:
        f.write(rc)
    print("✅  [Runner.rc: app metadata]")
except FileNotFoundError:
    print(f"❌  [Runner.rc] File not found")
    errors += 1


# ─── Patch 5: Replace app icon ────────────────────────────────────────────────
icon_src = "assets/app_icon.ico"
icon_dst = os.path.join(BASE, "flutter/windows/runner/resources/app_icon.ico")
if os.path.exists(icon_src):
    shutil.copy2(icon_src, icon_dst)
    print("✅  [Icon: replaced with UP Tech icon]")
else:
    print(f"⚠️  [Icon] {icon_src} not found — keeping default RustDesk icon")



# ─── Patch 6: Hide Network settings tab ───────────────────────────────────────
# The network tab exposes server + key to the end user.
# RustDesk already guards this tab with kOptionHideNetworkSetting — we simply
# remove the entry from tabKeys so it never appears in the UI.
patch(
    os.path.join(BASE, "flutter/lib/desktop/pages/desktop_setting_page.dart"),
    "    if (!bind.isDisableSettings() &&\n"
    "        bind.mainGetBuildinOption(key: kOptionHideNetworkSetting) != 'Y')\n"
    "      SettingsTabKey.network,",
    "",
    "desktop_setting_page: hide network tab"
)

# ─── Summary ───────────────────────────────────────────────────────────────────
print()
if errors > 0:
    print(f"❌  {errors} patch(es) failed. See above for details.")
    sys.exit(1)
else:
    print("✅  All UpDesk patches applied successfully.")
    print(f"    Server: {SERVER}")
    print(f"    Mode:   receiver-only (conn-type=incoming)")
    print(f"    Name:   UpDesk")
