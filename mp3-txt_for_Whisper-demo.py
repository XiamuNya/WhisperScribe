"""
Whisper 语音识别模型脚本

这个脚本展示了如何使用 OpenAI 的 Whisper 模型进行语音识别。
Whisper 是一个支持多语种语音识别和翻译的开源模型。


输出日志文件保存路径(此路径为当前脚本所在目录下的log文件夹,命名方式为:年月日时分秒毫秒_文件名.log):
E:\Desktop\claude_test\mp3_txt\log

输出结果文件保存路径(此路径为当前脚本所在目录下的result文件夹,命名方式为:年月日时分秒_文件名.txt):
E:\Desktop\claude_test\mp3_txt\result

依赖安装:
pip install transformers torch datasets accelerate soundfile -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install librosa  # 添加 librosa 用于音频处理
"""

import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset
import os
import librosa  # 添加 librosa 导入
import warnings
import logging
from datetime import datetime
import pathlib
import re
import jieba
import jieba.posseg as pseg
from pydub import AudioSegment
import tempfile

warnings.filterwarnings("ignore", message="Error parsing dependencies")

def setup_directories_and_logging():
    """
    创建必要的目录并设置日志记录
    
    返回值:
        tuple: (log_file_path, result_file_path)
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
    
    参数:
        text: 原始转录文本
    返回值:
        str: 处理后的文本
    """
    # 移除多余的空格和标点
    text = re.sub(r'\s+', ' ', text.strip())
    text = re.sub(r'[,.。，、？！?!]+', '', text)
    
    # 使用结巴分词进行分词和词性标注
    words = pseg.cut(text)
    
    # 根据词性添加标点
    processed_text = []
    sentence_length = 0
    for word, flag in words:
        processed_text.append(word)
        sentence_length += len(word)
        
        # 在句子结尾词后添加句号
        if flag in ['v', 'vn'] and sentence_length > 15:
            processed_text.append('。')
            sentence_length = 0
        # 在较长的名词短语后添加逗号
        elif flag.startswith('n') and sentence_length > 10:
            processed_text.append('，')
            sentence_length = 0
        # 在语气词后添加逗号
        elif flag in ['y', 'uj', 'ul']:
            processed_text.append('，')
            sentence_length = 0
    
    # 合并文本并确保最后以句号结尾
    result = ''.join(processed_text)
    if not result.endswith('。'):
        result += '。'
    
    # 清理可能出现的连续标点
    result = re.sub(r'[,，]{2,}', '，', result)
    result = re.sub(r'[.。]{2,}', '。', result)
    result = re.sub(r'，。', '。', result)
    
    return result

def setup_whisper():
    """
    初始化并配置 Whisper 语音识别模型
    """
    def try_load_model(use_proxy=False):
        if use_proxy:
            # 设置代理
            os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
            os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
            proxies = {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}
        else:
            # 清除代理
            os.environ.pop('HTTP_PROXY', None)
            os.environ.pop('HTTPS_PROXY', None)
            proxies = None

        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        model_id = "openai/whisper-small"

        try:
            model = AutoModelForSpeechSeq2Seq.from_pretrained(
                model_id, 
                torch_dtype=torch_dtype,
                low_cpu_mem_usage=True,
                use_safetensors=True,
                trust_remote_code=True,
                local_files_only=False,
                proxies=proxies
            )
            model.to(device)

            processor = AutoProcessor.from_pretrained(
                model_id,
                trust_remote_code=True,
                local_files_only=False,
                proxies=proxies
            )

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
            return pipe
        except Exception as e:
            if use_proxy:
                raise e
            return None

    # 首先尝试不使用代理
    print("超时设置——>10s 但实际上可能需要多等待一会会 ^ ^...")
    print("如直接连接失败，将启动代理，请耐心等待....")
    print("尝试直接连接...")
    pipe = try_load_model(use_proxy=False)
    if pipe is not None:
        print("模型加载成功！(直接连接)")
        return pipe

    # 如果失败，尝试使用代理
    print("直接连接失败，尝试使用代理...")
    try:
        pipe = try_load_model(use_proxy=True)
        print("模型加载成功！(使用代理)")
        return pipe
    except Exception as e:
        print(f"模型加载失败: {str(e)}")
        print("\n请尝试以下解决方案:")
        print("1. 检查网络连接")
        print("2. 确保代理服务器(127.0.0.1:7890)正在运行")
        print("3. 尝试重启代理")
        print("4. 如果还是不行，可以尝试直接从浏览器下载模型文件")
        raise e

def convert_audio_to_wav(audio_path):
    """
    将音频文件转换为WAV格式
    
    参数:
        audio_path: 原始音频文件路径
    返回:
        str: 临时WAV文件的路径
    """
    try:
        # 获取文件扩展名
        ext = os.path.splitext(audio_path)[1].lower()
        
        # 如果已经是wav格式，直接返回
        if ext == '.wav':
            return audio_path
            
        # 创建临时文件
        temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        temp_wav_path = temp_wav.name
        temp_wav.close()
        
        # 根据不同格式进行转换
        if ext == '.mp3':
            audio = AudioSegment.from_mp3(audio_path)
        elif ext == '.ogg':
            audio = AudioSegment.from_ogg(audio_path)
        elif ext == '.flac':
            audio = AudioSegment.from_file(audio_path, format="flac")
        elif ext == '.m4a':
            audio = AudioSegment.from_file(audio_path, format="m4a")
        else:
            # 尝试自动识别格式
            audio = AudioSegment.from_file(audio_path)
        
        # 导出为WAV格式
        audio.export(temp_wav_path, format="wav")
        return temp_wav_path
        
    except Exception as e:
        print(f"音频转换失败: {str(e)}")
        return audio_path

def transcribe_audio(pipe, audio_path, result_file_path):
    """
    将音频文件转录为文本并保存结果
    """
    from opencc import OpenCC
    cc = OpenCC('t2s')

    try:
        logging.info(f"开始处理音频文件: {audio_path}")
        
        # 转换音频格式
        wav_path = convert_audio_to_wav(audio_path)
        logging.info(f"音频格式转换完成: {wav_path}")
        
        # 加载音频
        audio, sr = librosa.load(wav_path, sr=16000)
        
        # 如果是临时文件，处理完后删除
        if wav_path != audio_path:
            try:
                os.remove(wav_path)
            except:
                pass
        
        result = pipe(audio)
        
        if "language" in result and "zh" in result["language"]:
            logging.info(f"检测到语言: {result['language']}")
            text = cc.convert(result["text"])
            result["language"] = "zh-cn"
            
            # 对文本进行智能标点处理
            processed_text = process_text_with_punctuation(text)
            result["text"] = processed_text
        
        # 保存转录结果
        with open(result_file_path, 'w', encoding='utf-8') as f:
            f.write(f"音频文件: {audio_path}\n")
            f.write(f"转录时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"识别语言: {result.get('language', 'unknown')}\n")
            f.write("\n转录内容:\n")
            f.write(result["text"])
        
        logging.info(f"转录结果已保存到: {result_file_path}")
        return result["text"]
    except Exception as e:
        logging.error(f"音频处理失败: {str(e)}")
        raise e

def demo():
    """
     Whisper 模型的使用方法
    """
    # 设置目录和日志
    log_file_path, result_file_path = setup_directories_and_logging()
    logging.info("初始化转录环境")
    
    # 初始化语音识别模型
    try:
        pipe = setup_whisper()
        logging.info("Whisper模型加载成功")
        
        audio_file_path = ""
        logging.info(f"准备处理音频文件: {audio_file_path}")
        
        result = transcribe_audio(pipe, audio_file_path, result_file_path)
        logging.info("转录完成")
        print("转录结果:", result)
        
    except FileNotFoundError:
        logging.error(f"找不到音频文件: {audio_file_path}")
        print(f"错误：找不到音频文件 '{audio_file_path}'")
    except Exception as e:
        logging.error(f"处理过程中出错: {str(e)}")
        print(f"处理音频时出错：{str(e)}")

if __name__ == "__main__":
    demo()

'''


1. 安装必要的依赖
2. 加载 Whisper 模型
3. 配置语音识别管道
4. 处理音频文件并获得文本转录结果

Whisper 的主要特点：
- 支持多语言：可以识别和翻译 96 种语言
- 强大的性能：即使在嘈杂环境下也有不错的识别效果
- 灵活性：有多个型号可选择，从 tiny 到 large
- 开源免费：可以本地运行，保护隐私

它能用来干什么？：
- 转录语音或视频内容
- 生成字幕
- 翻译语音内容
- 创建语音助手

需要注意的是，你需要根据实际需求选择合适的模型大小。larger 模型效果更好但需要更多计算资源，smaller 模型则更轻量但准确度可能略低。

'''