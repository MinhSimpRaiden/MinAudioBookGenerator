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
