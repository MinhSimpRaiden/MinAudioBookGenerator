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
