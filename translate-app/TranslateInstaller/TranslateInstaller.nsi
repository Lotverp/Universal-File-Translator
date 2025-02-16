; IMPOSTAZIONI BASE
OutFile "TranslateFile_Setup.exe" ; Nome dell'installer
InstallDir "$PROGRAMFILES\TranslateFile" ; Cartella di installazione predefinita
Icon "logo.ico" ; Icona dell'installer
RequestExecutionLevel admin ; Richiede i permessi di amministratore

; SEZIONE DI INSTALLAZIONE
Section
  ; Copia i file nella cartella di destinazione
  SetOutPath $INSTDIR
  File "translate.exe"
  File "logo.ico"

  ; Crea un collegamento nel menu Start
  CreateDirectory "$SMPROGRAMS\TranslateFile"
  CreateShortcut "$SMPROGRAMS\TranslateFile\TranslateFile.lnk" "$INSTDIR\translate.exe" "" "$INSTDIR\logo.ico"

  ; Crea un collegamento sul desktop (opzionale)
  ; CreateShortcut "$DESKTOP\TranslateFile.lnk" "$INSTDIR\translate.exe" "" "$INSTDIR\logo.ico"

  ; Scrivi l'uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

; SEZIONE DI DISINSTALLAZIONE
Section "Uninstall"
  ; Elimina i file
  Delete "$INSTDIR\translate.exe"
  Delete "$INSTDIR\logo.ico"
  Delete "$INSTDIR\Uninstall.exe"

  ; Elimina i collegamenti
  Delete "$SMPROGRAMS\TranslateFile\TranslateFile.lnk"
  ; Delete "$DESKTOP\TranslateFile.lnk" ; Se abilitato
  RMDir "$SMPROGRAMS\TranslateFile"
  RMDir "$INSTDIR"
SectionEnd