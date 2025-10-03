import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any
from dotenv import load_dotenv

from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner

load_dotenv()

SUBJECTS_TEACHERS = {
    "Toán": ["Thầy A", "Thầy B"], "Văn": ["Cô C", "Cô D"], "Anh": ["Cô E", "Thầy F"],
    "Lý": ["Thầy G", "Thầy H"], "Hóa": ["Cô I", "Cô J"], "Sinh": ["Thầy K", "Cô L"]
}

CLASSES = ["10A1", "10A2", "10A3"]
TIME_SLOTS = ["07:30-08:15", "08:20-09:05", "09:10-09:55", "10:00-10:45", "13:30-14:15", "14:20-15:05"]


def read_schedule(date: str = None) -> Dict[str, Any]:
    """Đọc lịch trình từ file JSON."""
    try:
        with open('data/schedule.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        if date:
            return {"success": True, "schedule": data.get(date, [])}
        return {"success": True, "schedule": data}
    except FileNotFoundError:
        return {"success": False, "error": "File lịch trình không tồn tại"}

def auto_generate_schedule(week_offset: int = 0) -> Dict[str, Any]:
    """Tự động tạo lịch học cho các lớp."""
    try:
        start_of_week = datetime.now() - timedelta(days=datetime.now().weekday()) + timedelta(weeks=week_offset)
        schedule_data = {}
        
        for class_name in CLASSES:
            for day in range(5):  # Chỉ từ thứ 2 đến thứ 6
                date_str = (start_of_week + timedelta(days=day)).strftime('%Y-%m-%d')
                if date_str not in schedule_data:
                    schedule_data[date_str] = []
                
                # Thêm 4 môn học mỗi ngày
                for i, subject in enumerate(list(SUBJECTS_TEACHERS.keys())[:4]):
                    teacher = SUBJECTS_TEACHERS[subject][i % 2]
                    task = {
                        "title": f"{subject} - {class_name}",
                        "date": date_str,
                        "time": TIME_SLOTS[i],
                        "teacher": teacher,
                        "class": class_name,
                        "subject": subject
                    }
                    schedule_data[date_str].append(task)
        
        os.makedirs('data', exist_ok=True)
        with open('data/schedule.json', 'w', encoding='utf-8') as f:
            json.dump(schedule_data, f, ensure_ascii=False, indent=2)
        
        total_classes = sum(len(tasks) for tasks in schedule_data.values())
        return {"success": True, "total_classes": total_classes, "message": f"Đã tạo {total_classes} lớp học"}
        
    except Exception as e:
        return {"success": False, "error": f"Lỗi: {str(e)}"}

def analyze_schedule() -> Dict[str, Any]:
    """Phân tích lịch trình đơn giản."""
    try:
        result = read_schedule()
        if not result["success"]:
            return result
        
        schedule_data = result["schedule"]
        total_classes = sum(len(tasks) for tasks in schedule_data.values())
        
        teacher_stats = {}
        for tasks in schedule_data.values():
            for task in tasks:
                teacher = task.get("teacher", "Không xác định")
                teacher_stats[teacher] = teacher_stats.get(teacher, 0) + 1
        
        return {
            "success": True,
            "total_classes": total_classes,
            "teacher_stats": teacher_stats,
            "days_scheduled": len(schedule_data)
        }
        
    except Exception as e:
        return {"success": False, "error": f"Lỗi phân tích: {str(e)}"}

def get_week_schedule(week_offset: int = 0) -> Dict[str, Any]:
    """Lấy lịch trình tuần hiện tại."""
    try:
        start_of_week = datetime.now() - timedelta(days=datetime.now().weekday()) + timedelta(weeks=week_offset)
        week_schedule = {}
        
        for i in range(5):
            date_str = (start_of_week + timedelta(days=i)).strftime('%Y-%m-%d')
            daily_result = read_schedule(date_str)
            week_schedule[date_str] = daily_result.get("schedule", []) if daily_result["success"] else []
        
        total_classes = sum(len(tasks) for tasks in week_schedule.values())
        return {
            "success": True,
            "week_start": start_of_week.strftime('%Y-%m-%d'),
            "total_classes": total_classes,
            "schedule": week_schedule
        }
        
    except Exception as e:
        return {"success": False, "error": f"Lỗi: {str(e)}"}


root_agent = LlmAgent(
    name="ScheduleManagerAgent",
    model="gemini-2.5-flash",
    description="Quản lý lịch học đơn giản",
    instruction="""
Bạn là trợ lý quản lý lịch học. Giúp:
1. Tạo lịch tự động: auto_generate_schedule()
2. Phân tích: analyze_schedule() 
3. Xem lịch tuần: get_week_schedule()
""",
    tools=[auto_generate_schedule, analyze_schedule, get_week_schedule],
    output_key="result",
)


async def main():
    # Sử dụng agent trực tiếp thay vì thông qua runner phức tạp
    print("=== HỆ THỐNG LỊCH HỌC ĐƠN GIẢN ===\n")
    
    # Tạo lịch
    print("1. Đang tạo lịch...")
    result = await root_agent.run("Tạo lịch học mới")
    print(result)
    
    # Phân tích
    print("\n2. Đang phân tích...")
    result = await root_agent.run("Phân tích lịch trình")
    print(result)
    
    # Xem lịch
    print("\n3. Đang xem lịch tuần...")
    result = await root_agent.run("Cho xem lịch tuần này")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())