@echo off
echo Installing required packages...
pip install gradio -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
echo Installation completed!
pause 