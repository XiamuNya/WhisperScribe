@echo off
REM 设置代码页为UTF-8
chcp 65001 >nul

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