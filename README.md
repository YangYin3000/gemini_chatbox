# Báo cáo: Chatbot Gemini  

## 1. Giới thiệu  
Đây là chương trình **chatbot sử dụng Google Generative AI (Gemini)** để trò chuyện với người dùng. Chương trình được xây dựng bằng Python, chạy trên giao diện dòng lệnh (CLI), có khả năng lưu lịch sử hội thoại và xử lý khi kết nối API gặp lỗi.  

## 2. Chức năng chính  
- Kết nối với **Gemini API** thông qua API Key.  
- Cho phép người dùng trò chuyện trực tiếp trên cửa sổ dòng lệnh.  
- Lưu lại **lịch sử hội thoại** để đảm bảo ngữ cảnh.  
- Có cơ chế **tự động thử lại (retry)** khi gặp lỗi từ API.  

## 3. Công cụ và môi trường  
- **Ngôn ngữ lập trình:** Python 3.8 trở lên.  
- **Thư viện sử dụng:**  
  ```bash
  pip install google-generativeai
  ```  

## 4. Hướng dẫn cài đặt và chạy  
### Bước 1: Cấu hình API Key  
Mở file `gemini_chatbot.py` và thay dòng sau bằng API Key thật của bạn:  
```python
API_KEY = "YOUR_API_KEY"
```  

### Bước 2: Chạy chương trình  
Trong terminal hoặc command prompt:  
```bash
python gemini_chatbot.py
```  

### Bước 3: Tương tác với chatbot  
- Gõ nội dung cần hỏi và nhấn **Enter** để gửi.  
- Gõ `exit` để thoát chương trình.  

## 5. Ví dụ chạy chương trình  
```text
User: Xin chào
Gemini: Chào bạn! Mình có thể giúp gì?
User: Hãy giải thích định luật Newton
Gemini: Định luật Newton gồm 3 định luật cơ bản...
```

## 6. Kết luận  
Chương trình đã thực hiện được:  
- Kết nối và giao tiếp với mô hình Gemini của Google.  
- Lưu giữ lịch sử hội thoại để tăng tính tự nhiên khi đối thoại.  
- Xử lý lỗi API bằng cơ chế thử lại nhiều lần.  

Hạn chế:  
- Chưa có giao diện đồ họa.  
- Cần API Key hợp lệ từ Google AI Studio.  

Định hướng phát triển:  
- Xây dựng giao diện web/app cho người dùng.  
- Bổ sung chức năng quản lý hội thoại, lưu lịch sử ra file.  
