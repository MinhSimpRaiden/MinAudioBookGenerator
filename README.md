# MinAudioBookGenerator

MinAudioBookGenerator là ứng dụng mã nguồn mở chuyển đổi truyện chữ (text) thành sách nói (audiobook) chất lượng cao sử dụng trí tuệ nhân tạo.
Dự án được xây dựng với Python, Gradio và bộ lõi **VieNeu-TTS** (hỗ trợ đọc tiếng Việt cực kỳ tự nhiên và mượt mà).

## Tính năng chính
- Dán văn bản hoặc tải lên file `.txt` truyện.
- Tự động nhận diện và chia nhỏ truyện thành nhiều tập (mỗi tập khoảng 2 tiếng đọc ~ 19.200 từ).
- Chạy hoàn toàn dưới máy cá nhân (Local) để bảo vệ quyền riêng tư và không mất phí API.
- Hỗ trợ GPU NVIDIA để render audio siêu tốc.
