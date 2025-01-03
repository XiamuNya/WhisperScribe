@echo off
REM 设置代码页为UTF-8
chcp 65001 >nul

echo ======================================
echo   WhisperScribe 启动程序
echo ======================================
echo.
echo 正在初始化环境...
set PYTHONPATH=%PYTHONPATH%;%~dp0

echo 正在启动程序...
python webui.py

if errorlevel 1 (
    echo.
    echo 程序异常退出，请检查错误信息。
    echo 按任意键退出...
    pause >nul
) 