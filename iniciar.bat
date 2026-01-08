@echo off
chcp 65001 >nul
title Plan de Desarrollo Profesional - Servidor

echo ========================================
echo   Plan de Desarrollo Profesional
echo ========================================
echo.

REM Verificar si el entorno virtual está activo
if not defined VIRTUAL_ENV (
    echo Activando entorno virtual...
    call Scripts\activate.bat
)

echo.
echo Iniciando servidor FastAPI...
echo.
echo El servidor estara disponible en:
echo   http://localhost:8000
echo.
echo Presiona Ctrl+C para detener el servidor
echo ========================================
echo.

python main.py

pause
