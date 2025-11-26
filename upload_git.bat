@echo off
setlocal

REM Commit-Nachricht abfragen
set /p commitmsg=Commit-Nachricht: 

REM GitLab Repo-URL (fix, dein Repo)
set "repo=https://github.com/yungggun/Edu-Lock.git"

REM In den Ordner wechseln, in dem die .bat liegt
cd /d "%~dp0"

REM Git initialisieren, falls noch nicht geschehen
if not exist ".git" (
    git init
    git branch -M main
    git remote add origin %repo%
)

REM Alle Dateien im aktuellen Ordner hinzufügen
git add .

REM Commit mit eingegebener Nachricht
git commit -m "%commitmsg%"

REM Push auf GitLab
git push -u origin main

echo.
echo ✅ Alle Dateien im aktuellen Ordner wurden mit der Commit-Nachricht "%commitmsg%" auf GitLab hochgeladen!
pause
