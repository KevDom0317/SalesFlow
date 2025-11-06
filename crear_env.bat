@echo off
echo ========================================
echo   Creando archivo de configuracion .env
echo ========================================
echo.

REM Verificar si el archivo ya existe
if exist .env (
    echo El archivo .env ya existe.
    echo.
    choice /C SN /M "¿Deseas sobrescribirlo"
    if errorlevel 2 goto :end
    if errorlevel 1 goto :crear
) else (
    goto :crear
)

:crear
echo Creando archivo .env...
(
echo # Configuracion de Base de Datos
echo # La aplicacion se conecta directamente a MySQL/MariaDB
echo # phpMyAdmin es solo una herramienta web para gestionar la BD
echo.
echo DB_HOST=127.0.0.1
echo DB_PORT=3306
echo DB_NAME=salesflow
echo DB_USER=root
echo DB_PASSWORD=
) > .env

echo.
echo ========================================
echo   Archivo .env creado exitosamente!
echo ========================================
echo.
echo IMPORTANTE: Si MySQL tiene contraseña, edita el archivo .env
echo y agrega tu contraseña en la linea DB_PASSWORD=
echo.
echo Ejemplo:
echo DB_PASSWORD=mi_contraseña
echo.

:end
pause

