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

    rtf = elapsed_time / audio_duration
    
    print(f"\n[KẾT QUẢ BENCHMARK TRÊN MÁY BẠN]")
    print(f"- Thời gian thực thi: {elapsed_time:.2f} giây")
    print(f"- Thời lượng audio sinh ra: {audio_duration:.2f} giây")
    print(f"- Hệ số RTF (Real-Time Factor): {rtf:.4f}")
    print(f"- Tốc độ render: Nhanh gấp {1/rtf:.1f} lần tốc độ đọc của người thật")

    # Ước tính cho tập 5 tiếng (18000 giây)
    estimated_time_5h = 18000 * rtf
    print(f"\n=> ƯỚC TÍNH: 1 Tập (5 tiếng) sẽ tốn khoảng {estimated_time_5h / 60:.1f} phút để convert xong hoàn toàn.")
    
except Exception as e:
    print(f"Lỗi khi chạy benchmark: {e}")
