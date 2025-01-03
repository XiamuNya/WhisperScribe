def create_bat_files():
    # install_ffmpeg.bat
    with open('install_ffmpeg.bat', 'w', encoding='gbk') as f:
        f.write('''@echo off
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
''')

    # install_requirements.bat
    with open('install_requirements.bat', 'w', encoding='gbk') as f:
        f.write('''@echo off
title WhisperScribe 依赖安装程序
color 0A

echo ======================================
echo   WhisperScribe 依赖安装程序
echo ======================================
echo.

echo [1/2] 正在安装 Python 依赖包...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo [2/2] 检查安装结果...
python -c "import torch; import gradio; import transformers; print('依赖包安装成功！')"

if errorlevel 1 (
    echo.
    echo [错误] 依赖包安装可能不完整，请检查以上错误信息。
    echo 常见问题解决方案：
    echo 1. 确保已安装 Python 3.8 或更高版本
    echo 2. 检查网络连接
    echo 3. 尝试手动安装失败的包
) else (
    echo.
    echo [成功] 所有依赖包已安装完成！
    echo 下一步：请运行 install_ffmpeg.bat 安装音频处理组件。
)

echo.
echo 按任意键退出...
pause >nul
''')

    # run_webui.bat
    with open('run_webui.bat', 'w', encoding='gbk') as f:
        f.write('''@echo off
title WhisperScribe 启动程序
color 0A

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
''')

    print("批处理文件已创建完成！")

if __name__ == "__main__":
    create_bat_files() 