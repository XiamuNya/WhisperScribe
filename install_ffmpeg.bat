@echo off
title FFmpeg ��װ���� - WhisperScribe
color 0A

echo ======================================
echo   FFmpeg ��װ���� - WhisperScribe
echo ======================================
echo.

REM ��װ Python ��
echo [1/2] ���ڰ�װ��Ҫ�� Python ��...
pip install ffmpeg-python -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install pydub -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo ======================================
echo   FFmpeg ����˵��
echo ======================================
echo 1. ��������°ٶ������������� FFmpeg:
echo    ����: https://pan.baidu.com/s/1WV94oj6oKvh_DVleOUDLIA
echo    ��ȡ��: wnqd
echo.
echo 2. ������ɺ��뽫�����ļ����Ƶ�����Ŀ¼:
echo    - ffmpeg.exe
echo    - ffprobe.exe
echo    (���Ƶ��뱾bat�ļ���ͬ��Ŀ¼)
echo ======================================
echo.
echo ��ܰ��ʾ��
echo - ���ص��ļ���Ϊ��FFmpeg(��Ƶת¼�ı�һЩ��Ҫ�ļ�)
echo - ����ٶ���������ʧЧ������ϵ���߻�ȡ������
echo - ����� https://ffmpeg.org/download.html ��������
echo.
echo ����ļ����ƺ󣬰������������鰲װ...
pause >nul

REM ����ļ��Ƿ����
if not exist ffmpeg.exe (
    echo [����] δ�ҵ� ffmpeg.exe
    echo ��ȷ���ѽ� ffmpeg.exe ���Ƶ���ǰĿ¼��
    echo %~dp0
    goto end
)

if not exist ffprobe.exe (
    echo [����] δ�ҵ� ffprobe.exe
    echo ��ȷ���ѽ� ffprobe.exe ���Ƶ���ǰĿ¼��
    echo %~dp0
    goto end
)

echo.
echo [�ɹ�] FFmpeg �ļ��Ѿ�����
echo ��װ��ɣ����ڿ������� run_webui.bat ���������ˡ�

:end
echo.
echo ��������˳�...
pause >nul
