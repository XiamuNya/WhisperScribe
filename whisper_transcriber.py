import os
import tempfile
from pydub import AudioSegment
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import librosa
import logging
from datetime import datetime
import pathlib
import re

def check_ffmpeg():
    """
    检查 ffmpeg 是否可用，如果不可用则尝试使用本地 ffmpeg
    """
    import shutil

    def is_ffmpeg_available():
        return shutil.which('ffmpeg') is not None

    if not is_ffmpeg_available():
        # 检查当前目录是否有 ffmpeg
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ffmpeg_path = os.path.join(current_dir, 'ffmpeg.exe')
        ffprobe_path = os.path.join(current_dir, 'ffprobe.exe')
        
        if os.path.exists(ffmpeg_path) and os.path.exists(ffprobe_path):
            # 设置 pydub 使用本地 ffmpeg
            AudioSegment.converter = ffmpeg_path
            AudioSegment.ffmpeg = ffmpeg_path
            AudioSegment.ffprobe = ffprobe_path
        else:
            print("警告: 未找到 ffmpeg，请运行 install_ffmpeg.bat 安装必要组件")
            print("或访问 https://ffmpeg.org/download.html 下载安装 ffmpeg")
            return False
    return True

def convert_audio_to_wav(audio_path):
    """
    将音频文件转换为WAV格式
    """
    try:
        # 首先检查 ffmpeg
        if not check_ffmpeg():
            raise Exception("ffmpeg 未正确安装，无法处理非 WAV 格式的音频")

        # 获取文件扩展名
        ext = os.path.splitext(audio_path)[1].lower()
        
        # 如果已经是wav格式，直接返回
        if ext == '.wav':
            return audio_path
            
        # 创建临时文件
        temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        temp_wav_path = temp_wav.name
        temp_wav.close()
        
        try:
            # 使用 pydub 转换音频
            audio = AudioSegment.from_file(audio_path)
            audio.export(temp_wav_path, format="wav")
            return temp_wav_path
        except Exception as e:
            print(f"音频转换失败: {str(e)}")
            if os.path.exists(temp_wav_path):
                os.remove(temp_wav_path)
            raise
            
    except Exception as e:
        print(f"音频转换失败: {str(e)}")
        print("请确保:")
        print("1. 已运行 install_ffmpeg.bat 安装必要组件")
        print("2. 音频文件格式正确且未损坏")
        print("3. 有足够的磁盘空间")
        raise 

def setup_whisper():
    """
    初始化并配置 Whisper 语音识别模型
    """
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    model_id = "openai/whisper-small"

    try:
        print("\n" + "="*50)
        print("欢迎使用语音转文字工具，by-程 v1.0")
        print("初次启动可能需要多等待一会，请耐心等待...")
        print("建议使用Chrome浏览器以获得最佳体验~")
        print("="*50 + "\n")
        
        print("正在从国内镜像下载模型，请稍候...")
        
        # 设置 HuggingFace 镜像
        os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
        os.environ['HF_MIRROR'] = 'https://hf-mirror.com'
        
        try:
            model = AutoModelForSpeechSeq2Seq.from_pretrained(
                "openai/whisper-small",
                torch_dtype=torch_dtype,
                low_cpu_mem_usage=True,
                use_safetensors=True,
                local_files_only=False,
                mirror='https://hf-mirror.com',
                trust_remote_code=True
            )
            print("模型下载完成！")
        except Exception as e:
            print("\n模型下载失败，请检查网络连接")
            print("详细错误信息：", str(e))
            raise e

        model.to(device)

        try:
            print("正在下载处理器...")
            processor = AutoProcessor.from_pretrained(
                "openai/whisper-small",
                local_files_only=False,
                mirror='https://hf-mirror.com',
                trust_remote_code=True
            )
            print("处理器下载完成！")
        except Exception as e:
            print("\n处理器下载失败，请检查网络连接")
            print("详细错误信息：", str(e))
            raise e

        pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            max_new_tokens=256,
            chunk_length_s=15,
            batch_size=16,
            torch_dtype=torch_dtype,
            device=device,
        )
        print("初始化完成！")
        return pipe
    except Exception as e:
        print("\n程序初始化失败，请检查网络连接后重试")
        raise e

def setup_directories_and_logging():
    """
    创建必要的目录并设置日志记录
    """
    # 获取当前脚本所在目录
    current_dir = pathlib.Path(__file__).parent
    
    # 创建所需的目录
    log_dir = current_dir / "log"
    result_dir = current_dir / "result"
    log_dir.mkdir(exist_ok=True)
    result_dir.mkdir(exist_ok=True)
    
    # 生成文件名
    current_time = datetime.now()
    log_filename = current_time.strftime("%Y%m%d_%H%M%S_%f") + ".log"
    result_filename = current_time.strftime("%Y%m%d_%H%M%S") + "-result.txt"
    
    log_file_path = log_dir / log_filename
    result_file_path = result_dir / result_filename
    
    # 配置日志记录
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_path, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    logging.info("开始新的转录会话")
    return log_file_path, result_file_path

def process_text_with_punctuation(text):
    """
    对转录文本进行智能标点处理
    """
    import jieba
    import jieba.posseg as pseg
    
    # 移除多余的空格和标点
    text = re.sub(r'\s+', ' ', text.strip())
    text = re.sub(r'[,.。，、？！?!]+', '', text)
    
    # 使用结巴分词进行分词和词性标注
    words = pseg.cut(text)
    
    # 根据词性添加标点
    processed_text = []
    sentence_length = 0
    prev_word_type = None
    
    for word, flag in words:
        processed_text.append(word)
        sentence_length += len(word)
        
        # 标点添加规则
        if flag.startswith('w'):  # 保留原有标点
            continue
            
        # 在句子结尾词后添加句号
        if sentence_length >= 15 and flag in ['v', 'vn', 'n', 'a']:
            if not any(p in ['。', '！', '？'] for p in processed_text[-1]):
                processed_text.append('。')
                sentence_length = 0
        
        # 在较长的名词短语后添加逗号
        elif sentence_length >= 8 and flag.startswith('n'):
            if prev_word_type != 'n':  # 避免在连续名词中间加逗号
                processed_text.append('，')
                sentence_length = 0
        
        # 在语气词后添加逗号或句号
        elif flag in ['y', 'uj', 'ul']:
            if sentence_length > 10:
                processed_text.append('。')
            else:
                processed_text.append('，')
            sentence_length = 0
        
        # 在连词后添加逗号
        elif flag in ['c', 'cc']:
            processed_text.append('，')
            sentence_length = 0
        
        # 在特定词后添加问号
        elif '吗' in word or '呢' in word or '？' in word:
            processed_text.append('？')
            sentence_length = 0
        
        # 在感叹词后添加感叹号
        elif flag == 'e' or any(w in word for w in ['啊', '哇', '哦']):
            processed_text.append('！')
            sentence_length = 0
            
        prev_word_type = flag
    
    # 合并文本并确保最后以标点结尾
    result = ''.join(processed_text)
    if not any(result.endswith(p) for p in ['。', '！', '？']):
        result += '。'
    
    # 清理可能出现的连续标点
    result = re.sub(r'[,，]{2,}', '，', result)
    result = re.sub(r'[.。]{2,}', '。', result)
    result = re.sub(r'，[。！？]', lambda m: m.group(0)[-1], result)
    
    return result

def transcribe_audio(pipe, audio_path, result_file_path, status_callback=None):
    """
    将音频文件转录为文本并保存结果
    """
    try:
        def update_status(message):
            logging.info(message)
            if status_callback:
                return status_callback(message)
        
        update_status("开始新的转录会话...")
        update_status(f"开始处理音频文件: {audio_path}")
        
        # 转换音频格式
        wav_path = convert_audio_to_wav(audio_path)
        update_status(f"音频格式转换完成: {wav_path}")
        
        # 加载音频
        update_status("正在加载音频文件...")
        audio, sr = librosa.load(wav_path, sr=16000)
        
        # 如果是临时文件，处理完后删除
        if wav_path != audio_path:
            try:
                os.remove(wav_path)
            except:
                pass
        
        update_status("正在进行语音识别...")
        result = pipe(audio)
        
        # 处理转录文本，添加标点符号
        text = result["text"]
        processed_text = process_text_with_punctuation(text)
        result["text"] = processed_text
        
        # 保存转录结果
        update_status("正在保存转录结果...")
        with open(result_file_path, 'w', encoding='utf-8') as f:
            f.write(f"音频文件: {audio_path}\n")
            f.write(f"转录时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"识别语言: {result.get('language', 'unknown')}\n")
            f.write("\n转录内容:\n")
            f.write(result["text"])
        
        update_status(f"✅ 转录完成！结果已保存到: {result_file_path}")
        return result["text"]
    except Exception as e:
        error_msg = f"❌ 音频处理失败: {str(e)}"
        logging.error(error_msg)
        if status_callback:
            status_callback(error_msg)
        raise e 