import gradio as gr
import os
import re
import numpy as np
from vieneu import Vieneu
from pydub import AudioSegment
import tempfile

# Khởi tạo TTS engine với backend mặc định (GPU - PyTorch nếu có CUDA, nếu không sẽ chạy ONNX/CPU)
print("Khởi tạo VieNeu TTS...")
try:
    tts = Vieneu()
    voices = tts.list_preset_voices()
    # Truyền cả cặp (label, voice_id) để Gradio hiển thị label nhưng trả về voice_id
    VOICE_CHOICES = voices
    if not VOICE_CHOICES:
        VOICE_CHOICES = [("Phạm Tuyên", "Phạm Tuyên"), ("Hải Đăng", "Hải Đăng"), ("Mai Anh", "Mai Anh")]
    print(f"Đã tải thành công {len(VOICE_CHOICES)} giọng đọc.")
except Exception as e:
    print("Lỗi khi khởi tạo Vieneu:", e)
    VOICE_CHOICES = [("Phạm Tuyên", "Phạm Tuyên"), ("Hải Đăng", "Hải Đăng"), ("Mai Anh", "Mai Anh")]
    tts = None

def split_text_into_episodes(text, words_per_episode):
    """
    Chia văn bản thành các tập dựa trên số từ ước tính.
    Văn bản được tách theo đoạn (paragraph) để không bị đứt ngang câu.
    """
    # Tách văn bản thành các đoạn nhỏ
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    
    episodes = []
    current_episode_paragraphs = []
    current_word_count = 0
    
    for p in paragraphs:
        word_count = len(p.split())
        # Nếu cộng thêm đoạn này mà vượt quá giới hạn và đã có nội dung trong tập hiện tại
        if current_word_count + word_count > words_per_episode and current_episode_paragraphs:
            episodes.append(current_episode_paragraphs)
            current_episode_paragraphs = [p]
            current_word_count = word_count
        else:
            current_episode_paragraphs.append(p)
            current_word_count += word_count
            
    if current_episode_paragraphs:
        episodes.append(current_episode_paragraphs)
        
    return episodes

def process_audiobook(file_obj, text_input, voice_name, words_per_ep, progress=gr.Progress()):
    if not tts:
        return "Lỗi: Chưa khởi tạo được VieNeu TTS. Hãy kiểm tra lại môi trường (GPU, Torch)."
        
    text = ""
    if file_obj is not None:
        try:
            with open(file_obj.name, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            return f"Lỗi đọc file text: {e}"
    elif text_input and text_input.strip():
        text = text_input.strip()
    else:
        return "Vui lòng tải lên file truyện hoặc nhập văn bản."

    if not text:
        return "Văn bản rỗng."

    words_per_ep = int(words_per_ep)
    progress(0, desc="Đang phân tích và chia tập...")
    
    episodes = split_text_into_episodes(text, words_per_ep)
    total_episodes = len(episodes)
    
    output_dir = "output_audiobooks"
    os.makedirs(output_dir, exist_ok=True)
    output_files = []
    
    for i, ep_paragraphs in enumerate(episodes):
        ep_num = i + 1
        progress((i) / total_episodes, desc=f"Đang tạo audio Tập {ep_num}/{total_episodes}...")
        
        # Batching: Vieneu hỗ trợ batch size, ta cắt các đoạn văn ra để đưa vào infer_batch
        # Tuy nhiên nếu đoạn văn quá dài, infer_batch có thể out of memory. 
        # Tạm thời gọi infer_batch cho toàn bộ tập (nếu RAM/VRAM đủ) hoặc chia thành các batch nhỏ.
        ep_audios = []
        batch_size = 32
        
        # Chia nhỏ số paragraph ra thành nhiều đợt để tránh OOM trên VRAM
        for j in range(0, len(ep_paragraphs), batch_size):
            batch = ep_paragraphs[j:j+batch_size]
            try:
                # Trả về list of np.ndarray
                audios = tts.infer_batch(batch, voice=voice_name, batch_size=batch_size)
                ep_audios.extend(audios)
            except Exception as e:
                return f"Lỗi khi tạo audio (Tập {ep_num}): {e}"
        
        # Ghép nối các numpy array audio lại
        if ep_audios and isinstance(ep_audios[0], np.ndarray):
            final_audio = np.concatenate(ep_audios, axis=0)
            
            # Xuất ra file WAV
            out_path_wav = os.path.join(output_dir, f"Tap_{ep_num:02d}.wav")
            tts.save(final_audio, out_path_wav)
            output_files.append(out_path_wav)
            
            # Thử convert sang MP3 nếu hệ thống có FFmpeg (thông qua pydub)
            try:
                audio_seg = AudioSegment.from_wav(out_path_wav)
                out_path_mp3 = os.path.join(output_dir, f"Tap_{ep_num:02d}.mp3")
                audio_seg.export(out_path_mp3, format="mp3", bitrate="128k")
                # Nếu convert thành công, dùng file mp3 thay vì wav
                output_files[-1] = out_path_mp3
                # Tuỳ chọn xoá file wav để tiết kiệm dung lượng
                os.remove(out_path_wav)
            except Exception as e:
                print(f"Không thể convert sang MP3 (có thể thiếu FFmpeg): {e}")
