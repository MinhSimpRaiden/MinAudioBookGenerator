# MinAudioBookGenerator

MinAudioBookGenerator là ứng dụng mã nguồn mở chuyển đổi truyện chữ (text) thành sách nói (audiobook) chất lượng cao sử dụng trí tuệ nhân tạo.
Dự án được xây dựng với Python, Gradio và bộ lõi **VieNeu-TTS** (hỗ trợ đọc tiếng Việt cực kỳ tự nhiên và mượt mà).

## Tính năng chính
- Dán văn bản hoặc tải lên file `.txt` truyện.
- Tự động nhận diện và chia nhỏ truyện thành nhiều tập (mỗi tập khoảng 2 tiếng đọc ~ 19.200 từ).
- Chạy hoàn toàn dưới máy cá nhân (Local) để bảo vệ quyền riêng tư và không mất phí API.
- Hỗ trợ GPU NVIDIA để render audio siêu tốc.

## Yêu cầu hệ thống
- Hệ điều hành: Windows / macOS / Linux.
- Có cài đặt **Python 3.9+**.
- *(Khuyến nghị)* Card đồ hoạ (VGA) NVIDIA để sử dụng được PyTorch CUDA (giúp render nhanh gấp 10-20 lần so với CPU).
- *(Tùy chọn)* **FFmpeg** để xuất file dưới định dạng `.mp3`. (Nếu không có FFmpeg, app sẽ tự động lưu dưới dạng `.wav`).

## Cách cài đặt

Ứng dụng đang trong quá trình cài đặt tự động (file `install.ps1`). Nếu bạn muốn cài thủ công, mở Terminal/PowerShell tại thư mục này và chạy:

```powershell
python -m venv venv
.\venv\Scripts\activate

# Cài đặt PyTorch với CUDA 12.8 (hoặc phiên bản phù hợp)
pip install torch==2.8.0 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cu128
pip install transformers==4.57.6
pip install vieneu gradio pydub
```
