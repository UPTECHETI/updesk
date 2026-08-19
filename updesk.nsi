!define APP_NAME "UpDesk"
!define APP_EXE "updesk.exe"
!define APP_VERSION "1.3.8"

Name "${APP_NAME} - Suporte Remoto UP Tech"
OutFile "UpDesk-Setup.exe"
InstallDir "$LOCALAPPDATA\UpDesk"
RequestExecutionLevel user
ShowInstDetails hide
SetCompressor /SOLID lzma

!include "MUI2.nsh"
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "PortugueseBR"

Section "Install"
  SetOutPath "$INSTDIR"
  File /r "updesk-release\*"

  CreateShortcut "$DESKTOP\UpDesk.lnk" "$INSTDIR\${APP_EXE}" "" "$INSTDIR\${APP_EXE}" 0
  CreateDirectory "$SMPROGRAMS\UpDesk"
  CreateShortcut "$SMPROGRAMS\UpDesk\UpDesk.lnk" "$INSTDIR\${APP_EXE}"

  WriteUninstaller "$INSTDIR\Uninstall.exe"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\UpDesk" "DisplayName" "UpDesk - Suporte Remoto UP Tech"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\UpDesk" "UninstallString" '"$INSTDIR\Uninstall.exe"'
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\UpDesk" "DisplayVersion" "${APP_VERSION}"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\UpDesk" "Publisher" "UP Tech"
SectionEnd

Section "Uninstall"
  Delete "$DESKTOP\UpDesk.lnk"
  RMDir /r "$SMPROGRAMS\UpDesk"
  RMDir /r "$INSTDIR"
  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\UpDesk"
SectionEnd
