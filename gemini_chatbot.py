import os
import time
import warnings
import logging
from typing import List, Tuple
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

# Cấu hình logging và warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')
logging.getLogger().setLevel(logging.ERROR)

env_path = Path('key.env')
if not env_path.is_file():
    print("Lỗi: Không tìm thấy file key.env")
    print("Vui lòng tạo file key.env với nội dung: API_KEY=your_api_key_here")
    exit(1)

load_dotenv(env_path)

# Lấy API key từ biến môi trường
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    print("Lỗi: Không tìm thấy API_KEY trong file key.env")
    print("Vui lòng kiểm tra định dạng file key.env: API_KEY=your_actual_api_key")
    exit(1)

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('models/gemini-2.0-flash')
except Exception as e:
    print(f"Lỗi khi cấu hình Gemini: {str(e)}")
    exit(1)

# Khởi tạo lịch sử chat
chat_history: List[Tuple[str, str]] = []

def chat_with_gemini(message: str, max_retries: int = 3) -> str:
    retry_count = 0
    last_delay = 5  # Bắt đầu với 5 giây delay
    
    while retry_count < max_retries:
        try:
            # Tạo prompt từ lịch sử chat
            prompt_parts = []
            for role, text in chat_history:
                prompt_parts.append(f"{role} {text}")
            
            prompt_parts.append(f"User: {message}")
            full_prompt = "\n".join(prompt_parts)
            
            # Gửi request đến Gemini
            response = model.generate_content(full_prompt)
            
            # Lưu tin nhắn và phản hồi vào lịch sử
            chat_history.append(("User", message))
            chat_history.append(("", response.text))
            
            return response.text
            
        except Exception as e:
            error_msg = str(e)
            
            # Kiểm tra lỗi quota (429)
            if "429" in error_msg or "quota" in error_msg.lower():
                retry_count += 1
                
                # Trích xuất thời gian chờ đề xuất từ thông báo lỗi
                delay = last_delay
                if "retry in" in error_msg:
                    try:
                        # Tìm số giây trong thông báo lỗi
                        import re
                        match = re.search(r"retry in (\d+\.?\d*)s", error_msg)
                        if match:
                            delay = float(match.group(1))
                            last_delay = delay
                    except:
                        pass
                
                print(f"Tạm thời hết lượt truy cập. Thử lại sau {delay} giây... (Lần thử {retry_count}/{max_retries})")
                time.sleep(delay)
                
            else:
                # Các lỗi khác
                return f"Đã xảy ra lỗi: {error_msg}"
    
    return "Xin lỗi, tôi tạm thời không thể phản hồi do vượt quá giới hạn sử dụng. Vui lòng thử lại sau vài phút."

# Giao diện console
if __name__ == "__main__":
    print("Chat với Gemini AI (Gõ 'quit' để thoát)")
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == 'quit':
                print("Kết thúc trò chuyện. Tạm biệt!")
                break
            
            response = chat_with_gemini(user_input)
            print(f"AI: {response}")
        
        except KeyboardInterrupt:
            print("\nKết thúc trò chuyện. Tạm biệt!")
            break
        except Exception as e:
            print(f"Lỗi không xác định: {str(e)}")