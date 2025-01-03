import os
import sys
import importlib.util
import gradio as gr
import logging

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# 动态导入模块
module_path = os.path.join(current_dir, "whisper_transcriber.py")
spec = importlib.util.spec_from_file_location("whisper_module", module_path)
whisper_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(whisper_module)

# 从模块中获取所需函数
setup_whisper = whisper_module.setup_whisper
transcribe_audio = whisper_module.transcribe_audio
setup_directories_and_logging = whisper_module.setup_directories_and_logging

# 初始化Whisper模型
pipe = None  # 全局变量声明

def process_audio(audio_path, progress=gr.Progress()):
    """处理音频文件并返回转录结果"""
    try:
        if pipe is None:
            return "错误：模型未能正确加载，请检查网络连接。", "❌ 转录失败"
        
        # 设置日志和结果保存路径
        progress(0, desc="准备转录环境...")
        log_file_path, result_file_path = setup_directories_and_logging()
        
        # 用于收集状态更新
        status_text = []
        
        def status_callback(message):
            status_text.append(message)
            # 更新进度条和状态
            if "音频格式转换完成" in message:
                progress(0.3, desc=message)
            elif "正在加载音频文件" in message:
                progress(0.4, desc=message)
            elif "正在进行语音识别" in message:
                progress(0.6, desc=message)
            elif "正在保存转录结果" in message:
                progress(0.9, desc=message)
            return message
        
        # 转录音频
        progress(0.2, desc="开始处理音频...")
        result = transcribe_audio(pipe, audio_path, result_file_path, status_callback)
        
        # 准备最终结果
        progress(1.0, desc="转录完成！")
        final_result = (f"✨ 转录完成！\n\n"
                       f"📝 结果已保存至: {result_file_path}\n\n"
                       f"📌 转录内容:\n{result}")
        
        return final_result, "\n".join(status_text)
    except Exception as e:
        error_msg = f"❌ 处理失败: {str(e)}"
        logging.error(error_msg)
        return error_msg, error_msg

# 创建Web界面
def create_ui():
    with gr.Blocks(
        title="语音转文字工具 v1.0 by 程",
        theme=gr.themes.Soft(
            primary_hue=gr.themes.Color(
                c50="#fff1f2",
                c100="#ffe4e6",
                c200="#fecdd3",
                c300="#fda4af",
                c400="#fb7185",
                c500="#f43f5e",
                c600="#e11d48",
                c700="#be123c",
                c800="#9f1239",
                c900="#881337",
                c950="#4c0519",
            ),
            secondary_hue="pink",
            neutral_hue="rose",
            radius_size=gr.themes.sizes.radius_sm,
            font=[gr.themes.GoogleFont("Source Sans Pro"), "system-ui", "sans-serif"],
        ),
    ) as demo:
        gr.Markdown("""
        <div style="text-align: center; max-width: 800px; margin: 0 auto; padding: 20px;">
            <h1 style="color: #2196F3; margin-bottom: 10px; font-size: 2.5em;">
                🎙️ 语音转文字工具 v1.0
            </h1>
            <p style="font-size: 1.2em; color: #666; margin-bottom: 20px;">
                此项目使用 Whisper 模型将语音转换为文字，支持高达96种语言。
            </p>
            <div style="height: 2px; background: linear-gradient(90deg, #2196F3, #1976D2); margin: 20px auto;"></div>
        </div>
        """)
        
        with gr.Row(equal_height=True):
            with gr.Column(scale=1, min_width=300):
                gr.Markdown("""
                <div class="info-card author">
                    <h3>👨‍💻 作者信息</h3>
                    <ul>
                        <li>作者：程老师</li>
                        <li>版本：v1.0</li>
                        <li>更新：2024.01</li>
                    </ul>
                </div>
                """)
            
            with gr.Column(scale=2, min_width=400):
                gr.Markdown("""
                <div class="info-card features">
                    <h3>📝 功能特点</h3>
                    <ul>
                        <li>🔄 支持多种音频格式（自动转换）</li>
                        <li>💾 自动保存转录结果</li>
                        <li>📌 智能添加标点符号</li>
                        <li>🌏 支持中英文等多语言</li>
                    </ul>
                </div>
                """)
        
        with gr.Row(equal_height=True):
            with gr.Column():
                audio_input = gr.Audio(
                    label="上传音频文件",
                    type="filepath",
                    elem_classes="audio-input"
                )
                
                with gr.Row():
                    process_btn = gr.Button(
                        "🎯 开始转录",
                        variant="primary",
                        scale=3
                    )
                    status = gr.Textbox(
                        label="处理状态",
                        value="⌛ 等待开始转录...",
                        interactive=False,
                        scale=2,
                        lines=4,
                        elem_classes="status-box"
                    )
            
            with gr.Column():
                output_text = gr.Textbox(
                    label="转录结果",
                    placeholder="转录结果将在这里显示...",
                    lines=12,
                    elem_classes="output-text"
                )
        
        process_btn.click(
            fn=process_audio,
            inputs=[audio_input],
            outputs=[output_text, status],
            show_progress=True,  # 显示进度条
        )
        
        gr.Markdown("""
        <div class="info-section">
            <h3>💡 使用说明</h3>
            <ol>
                <li>上传音频文件（支持格式：wav, mp3, ogg, flac, m4a等大部分音频格式）
                    <br><small>非wav格式的音频文件将会被转换成wav格式</small>
                    <br><small class="warning">注意: 如未下载 ffmpeg.exe 和 ffprobe.exe，则只能使用 WAV 格式进行转录</small>
                </li>
                <li>点击"开始转录"按钮</li>
                <li>等待处理完成，查看转录结果</li>
            </ol>
        </div>
        """)

        gr.Markdown("""
        <div class="info-section">
            <h3>📋 注意事项</h3>
            <ul>
                <li>⚠️ 首次运行需要下载模型，请确保网络正常</li>
                <li>📁 转录结果自动保存在 result 目录</li>
                <li>📝 详细日志保存在 log 目录</li>
            </ul>
        </div>
        """)

        # 添加自定义CSS
        gr.Markdown("""
        <style>
        .info-card {
            background: linear-gradient(to bottom right, #fff1f2, #fff);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(244,63,94,0.1);
            margin: 10px;
            transition: transform 0.2s;
        }
        
        .info-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(244,63,94,0.15);
        }
        
        .info-card h3 {
            color: #e11d48;
            margin-bottom: 15px;
            border-bottom: 2px solid #fecdd3;
            padding-bottom: 8px;
        }
        
        .info-card ul {
            list-style-type: none;
            padding-left: 0;
        }
        
        .info-card li {
            margin: 10px 0;
            padding-left: 25px;
            position: relative;
        }
        
        .info-card li:before {
            content: "•";
            color: #2196F3;
            font-weight: bold;
            position: absolute;
            left: 10px;
        }
        
        .audio-input {
            border-radius: 10px;
            border: 2px solid #e0e0e0;
            padding: 15px;
            background: white;
            transition: all 0.3s ease;
        }
        
        .audio-input:hover {
            border-color: #2196F3;
            box-shadow: 0 2px 10px rgba(33,150,243,0.1);
        }
        
        .output-text {
            border-radius: 10px;
            border: 2px solid #e0e0e0;
            background-color: white;
            font-family: 'Source Sans Pro', sans-serif;
            padding: 15px;
            transition: all 0.3s ease;
        }
        
        .output-text:hover {
            border-color: #2196F3;
            box-shadow: 0 2px 10px rgba(33,150,243,0.1);
        }
        
        .status-box {
            border-radius: 10px;
            border: 2px solid #e0e0e0;
            background-color: white;
            font-family: monospace;
            font-size: 0.9em;
            line-height: 1.4;
            padding: 12px;
            transition: all 0.3s ease;
        }
        
        .status-box:hover {
            border-color: #2196F3;
            box-shadow: 0 2px 10px rgba(33,150,243,0.1);
        }
        
        .gradio-button.primary {
            background: linear-gradient(135deg, #f43f5e, #e11d48);
            border: none;
            color: white;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 8px;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .gradio-button.primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(244,63,94,0.3);
            background: linear-gradient(135deg, #fb7185, #be123c);
        }
        
        .info-section {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .info-section h3 {
            color: #2196F3;
            margin: 20px 0 15px 0;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 8px;
        }
        
        .info-section ul, .info-section ol {
            padding-left: 20px;
        }
        
        .info-section li {
            margin: 10px 0;
            line-height: 1.6;
        }
        
        small {
            color: #666;
            display: block;
            margin-top: 5px;
        }
        
        .warning {
            color: #e11d48;
            font-weight: bold;
        }
        </style>
        """)
    
    return demo

if __name__ == "__main__":
    demo = create_ui()
    
    # 初始化Whisper模型（只初始化一次）
    try:
        pipe = setup_whisper()
    except Exception as e:
        print(f"模型加载失败: {str(e)}")
        pipe = None

    # 启动服务器
    try:
        demo.launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=False,
            inbrowser=True,
            quiet=True
        )
    except Exception as e:
        print(f"启动失败: {str(e)}")
        print("\n可能的解决方案:")
        print("1. 检查端口7860是否被占用")
        print("2. 检查网络连接")
        print("3. 尝试重启程序")
        input("\n按回车键退出...") 