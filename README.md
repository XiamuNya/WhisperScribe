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

## 模型说明

本项目使用 openai/whisper-small 模型。

### 自动下载（推荐）
首次运行时，模型会自动下载到用户目录的缓存文件夹中（约1GB）。如果下载失败，可以尝试以下解决方案：
1. 检查网络连接
2. 使用代理
3. 更换网络环境
4. 手动下载（见下文）

### 手动下载说明
如果自动下载一直失败，可以按以下步骤手动下载：

1. 访问模型下载页面：https://hf-mirror.com/openai/whisper-small

2. 下载以下必需文件：
   - config.json (约2KB)
   - generation_config.json (约4KB)
   - model.safetensors (约944MB)
   - tokenizer.json (约2.4MB)
   - vocab.json (约816KB)
   - preprocessor_config.json (约181KB)
   - tokenizer_config.json (约277KB)

3. 模型文件存放位置：
   ```
   C:\Users\[用户名]\.cache\huggingface\hub\
   └── models--openai--whisper-small\
       └── snapshots\
           └── [某个哈希值目录]\
               ├── config.json
               ├── generation_config.json
               ├── model.safetensors
               ├── tokenizer.json
               ├── vocab.json
               ├── preprocessor_config.json
               └── tokenizer_config.json
   ```

4. 说明：
   - `[用户名]` 替换为您的 Windows 用户名
   - `[某个哈希值目录]` 是一个长字符串目录名，如果目录不存在会自动创建
   - 也可以让程序自动创建目录，只需将文件放入 models--openai--whisper-small 目录即可

注意事项：
- 确保所有文件名完全匹配
- 特别注意 model.safetensors 文件要下载完整（约944MB）
- 如果手动下载后仍然无法加载，可以尝试删除缓存目录让程序重新下载

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
