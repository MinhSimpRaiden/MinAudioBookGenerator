import time
from vieneu import Vieneu

# Tạo text mẫu dài (lặp lại 1 câu dài để đo lường)
sample_sentence = "Trong một thế giới đầy màu sắc của sách nói, việc mô phỏng tốc độ đọc thực sự rất quan trọng để ước lượng thời gian. " * 3
# Tạo ra một batch 20 câu (khoảng 600 từ)
texts = [sample_sentence] * 20 

print("Đang khởi tạo VieNeu TTS (để lấy thông số GPU)...")
try:
    tts = Vieneu()
    print("Bắt đầu mô phỏng quá trình tạo audio (Batch size = 32)...")
    
    # Warm up (chạy thử 1 câu trước để GPU nạp graph, tránh tính thời gian khởi động ban đầu)
    tts.infer(sample_sentence, voice="Phạm Tuyên")
    
    start_time = time.time()
    audios = tts.infer_batch(texts, voice="Phạm Tuyên", batch_size=32)
    end_time = time.time()

    elapsed_time = end_time - start_time
    # Tính tổng thời lượng audio tạo ra
    sample_rate = 48000
    total_audio_samples = sum(len(a) for a in audios)
    audio_duration = total_audio_samples / sample_rate
