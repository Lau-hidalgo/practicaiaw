@echo off
REM Script rápido para sincronizar con GitHub

echo Sincronizando cambios con GitHub...

git add .
git commit -m "Auto-update: %date% %time%"
git push

echo Listo!
pause
