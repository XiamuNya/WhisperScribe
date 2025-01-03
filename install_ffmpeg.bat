@echo off
title FFmpeg 安装程序 - WhisperScribe
color 0A

echo ======================================
echo   FFmpeg 安装程序 - WhisperScribe
echo ======================================
echo.

REM 安装 Python 包
echo [1/2] 正在安装必要的 Python 包...
pip install ffmpeg-python -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install pydub -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo ======================================
echo   FFmpeg 下载说明
echo ======================================
echo 1. 请访问以下百度网盘链接下载 FFmpeg:
echo    链接: https://pan.baidu.com/s/1WV94oj6oKvh_DVleOUDLIA
echo    提取码: wnqd
echo.
echo 2. 下载完成后，请将以下文件复制到程序目录:
echo    - ffmpeg.exe
echo    - ffprobe.exe
echo    (复制到与本bat文件相同的目录)
echo ======================================
echo.
echo 温馨提示：
echo - 下载的文件名为：FFmpeg(音频转录文本一些重要文件)
echo - 如果百度网盘链接失效，请联系作者获取新链接
echo - 或访问 https://ffmpeg.org/download.html 自行下载
echo.
echo 完成文件复制后，按任意键继续检查安装...
pause >nul

REM 检查文件是否存在
if not exist ffmpeg.exe (
    echo [错误] 未找到 ffmpeg.exe
    echo 请确保已将 ffmpeg.exe 复制到当前目录：
    echo %~dp0
    goto end
)

if not exist ffprobe.exe (
    echo [错误] 未找到 ffprobe.exe
    echo 请确保已将 ffprobe.exe 复制到当前目录：
    echo %~dp0
    goto end
)

echo.
echo [成功] FFmpeg 文件已就绪！
echo 安装完成！现在可以运行 run_webui.bat 启动程序了。

:end
echo.
echo 按任意键退出...
pause >nul
