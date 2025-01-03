@echo off
chcp 65001
echo 初始化并启动WebUI......
set PYTHONPATH=%PYTHONPATH%;%~dp0
python webui.py
pause 