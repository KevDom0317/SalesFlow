@echo off
echo ========================================
echo   SalesFlow - Iniciando Aplicacion
echo ========================================
echo.

REM Verificar si Python esta instalado (probar diferentes comandos)
python --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=python
    set PIP_CMD=pip
    goto :found_python
)

py --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=py
    set PIP_CMD=py -m pip
    goto :found_python
)

python3 --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=python3
    set PIP_CMD=pip3
    goto :found_python
)

REM Si no se encuentra Python
echo.
echo ========================================
echo   ERROR: Python no encontrado
echo ========================================
echo.
echo Python no esta instalado o no esta en el PATH del sistema.
echo.
echo SOLUCIONES:
echo.
echo 1. Instalar Python:
echo    - Descarga desde: https://www.python.org/downloads/
echo    - IMPORTANTE: Marca la opcion "Add Python to PATH" durante la instalacion
echo.
echo 2. Si Python ya esta instalado:
echo    - Agrega Python al PATH del sistema manualmente
echo    - O ejecuta manualmente: python app.py
echo.
echo 3. Verificar instalacion:
echo    - Abre PowerShell y ejecuta: python --version
echo.
echo ========================================
pause
exit /b 1

:found_python
echo Python encontrado: 
%PYTHON_CMD% --version
echo.

echo [1/2] Instalando dependencias...
%PIP_CMD% install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo ERROR al instalar dependencias
    echo Intenta ejecutar manualmente: %PIP_CMD% install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo [2/2] Iniciando servidor Flask...
echo.
echo ========================================
echo   Servidor iniciado!
echo   Abre tu navegador en: http://localhost:5000
echo ========================================
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

%PYTHON_CMD% app.py

pause

