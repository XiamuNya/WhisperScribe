@echo off
title WhisperScribe ��������
color 0A

echo ======================================
echo   WhisperScribe ��������
echo ======================================
echo.
echo ���ڳ�ʼ������...
set PYTHONPATH=%PYTHONPATH%;%~dp0

echo ������������...
python webui.py

if errorlevel 1 (
    echo.
    echo �����쳣�˳������������Ϣ��
    echo ��������˳�...
    pause >nul
)
