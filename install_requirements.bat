@echo off
title WhisperScribe ������װ����
color 0A

echo ======================================
echo   WhisperScribe ������װ����
echo ======================================
echo.

echo [1/2] ���ڰ�װ Python ������...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo [2/2] ��鰲װ���...
python -c "import torch; import gradio; import transformers; print('��������װ�ɹ���')"

if errorlevel 1 (
    echo.
    echo [����] ��������װ���ܲ��������������ϴ�����Ϣ��
    echo ����������������
    echo 1. ȷ���Ѱ�װ Python 3.8 ����߰汾
    echo 2. �����������
    echo 3. �����ֶ���װʧ�ܵİ�
) else (
    echo.
    echo [�ɹ�] �����������Ѱ�װ��ɣ�
    echo ��һ���������� install_ffmpeg.bat ��װ��Ƶ���������
)

echo.
echo ��������˳�...
pause >nul
