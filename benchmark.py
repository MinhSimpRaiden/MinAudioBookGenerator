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
