# UpDesk — Suporte Remoto UP Tech

Versão customizada do RustDesk para clientes UP Tech.

## Características

- **Servidor:** `updesk.uptech.eti.br` (Oracle Cloud São Paulo — gratuito sempre)
- **Modo:** Receiver-only (clientes só recebem acesso, não conseguem acessar outras máquinas)
- **Ícone:** UP Tech (Monitor + Cursor)
- **Base:** RustDesk 1.3.8

## Como gerar o executável

1. Vá em **Actions** → **Build UpDesk for Windows**
2. Clique em **Run workflow** → **Run workflow**
3. Aguarde ~90 minutos (build completo)
4. Baixe o artifact `updesk-windows-x64-1.3.8`
5. Dentro do ZIP: o arquivo principal é `updesk.exe` + DLLs

## Distribuição para clientes avulsos

Compacte o conteúdo do artifact em ZIP e envie ao cliente. Ele clica duas vezes em `updesk.exe`.

## Modificações no RustDesk original

| Arquivo | Mudança |
|---------|---------|
| `libs/hbb_common/src/config.rs` | `RENDEZVOUS_SERVERS` → `updesk.uptech.eti.br` |
| `src/common.rs` | `load_custom_client()` injeta server + key + `conn-type=incoming` |
| `flutter/windows/CMakeLists.txt` | `BINARY_NAME = "updesk"` |
| `flutter/windows/runner/Runner.rc` | Metadados do .exe (empresa: UP Tech, produto: UpDesk) |
| `flutter/windows/runner/resources/app_icon.ico` | Ícone UP Tech (Monitor+Cursor, 512px) |

## Estrutura

```
updesk/
├── .github/workflows/build-updesk.yml   ← workflow de build
├── assets/app_icon.ico                   ← ícone UP Tech
└── README.md
```

## Notas

- O build usa o servidor público do GitHub Actions (runner Windows 2022 gratuito).
- As dependências (vcpkg, Flutter, Rust) são cacheadas — segunda build ~40min.
- Não assina o .exe digitalmente (sem certificado). Windows pode mostrar aviso.
