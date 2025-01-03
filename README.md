# 语音转文字工具 v1.0

一个基于 Whisper 模型的语音转文字工具，支持多种语言和音频格式。

## 功能特点

- 🔄 支持多种音频格式（wav, mp3, ogg, flac, m4a等）
- 💾 自动保存转录结果
- 📌 智能添加标点符号
- 🌏 支持中英文等96种语言
- 🎯 简单易用的Web界面

## 安装说明

1. 确保已安装 Python 3.8 或更高版本
2. 克隆或下载本项目
3. 安装依赖：
   ```bash
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```
4. 运行 `install_requirements.bat` 安装依赖项
5. 运行 `install_ffmpeg.bat` 安装 FFmpeg（用于音频格式转换）

## 使用方法

1. 运行 `run_webui.bat` 启动程序
2. 在浏览器中打开 http://127.0.0.1:7860
3. 上传音频文件并点击"开始转录"
4. 等待处理完成，查看转录结果

## 注意事项

- 首次运行需要下载模型，请确保网络正常
- 建议使用Chrome浏览器以获得最佳体验
- 转录结果自动保存在 result 目录
- 详细日志保存在 log 目录

## 系统要求

- Windows 10/11
- Python 3.8+
- 4GB+ RAM
- 建议有独立显卡（支持CUDA可加速处理）

## 作者

- 作者：程老师
- 版本：v1.0
- 更新：2024.01

# WhisperScribe
