# 🎓 คู่มือสำหรับนักศึกษา

## 📝 โครงสร้างโปรเจค

### 1. ไฟล์หลัก
- `api.py`: API endpoints
- `main.py`: เริ่มต้นการทำงาน
- `processor.py`: ประมวลผลไฟล์ Excel
- `template_manager.py`: จัดการเทมเพลต
- `printer.py`: ระบบพิมพ์

### 2. ระบบใหม่
- `security.py`: ระบบความปลอดภัย
- `config.py`: จัดการการตั้งค่า
- `tests/`: ระบบทดสอบ

## 🚀 เริ่มต้นใช้งาน

1. ติดตั้ง dependencies:
```bash
pip install -r requirements.txt
```

2. ตั้งค่าไฟล์ `.env`:
```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///./app.db
```

3. รันระบบ:
```bash
uvicorn main:app --reload
```

## 📚 ตัวอย่างการใช้งาน

### 1. การใช้งานระบบความปลอดภัย
```python
from security import SecurityManager

# สร้าง instance
security = SecurityManager()

# สร้าง token
token = security.create_access_token({"username": "student"})

# ตรวจสอบ token
user = security.verify_token(token)

# เพิกถอน token
security.revoke_token(token)
```

### 2. การใช้งานระบบตั้งค่า
```python
from config import get_settings

# ดึงการตั้งค่า
settings = get_settings()

# ใช้งานการตั้งค่า
print(settings.APP_NAME)
print(settings.DATABASE_URL)
```

### 3. การเขียนการทดสอบ
```python
import pytest
from processor import ExcelProcessor

def test_process_file():
    # Arrange
    processor = ExcelProcessor("test.xlsx")
    
    # Act
    result = processor.process_file()
    
    # Assert
    assert result["status"] == "success"
```

## 🔍 แนวทางการศึกษา

### 1. เริ่มต้นศึกษา
1. อ่านเอกสารประกอบในโฟลเดอร์ `docs/`
2. ศึกษาตัวอย่างในโฟลเดอร์ `demo/`
3. ทดลองรันการทดสอบใน `tests/`

### 2. การพัฒนาต่อยอด
1. เพิ่มการตรวจสอบข้อมูล
2. ปรับแต่งการแสดงผล
3. เพิ่มฟีเจอร์ใหม่

### 3. การทดสอบ
1. เขียนการทดสอบเพิ่มเติม
2. ทดสอบ edge cases
3. ทดสอบประสิทธิภาพ

## ⚠️ ข้อควรระวัง

1. **การจัดการไฟล์**
   - ตรวจสอบ path ให้ถูกต้อง
   - ปิดไฟล์หลังใช้งาน
   - ระวังการใช้ memory

2. **ความปลอดภัย**
   - ไม่เปิดเผย SECRET_KEY
   - ตรวจสอบ input
   - จำกัดขนาดไฟล์

3. **การทำงานพร้อมกัน**
   - ระวัง race conditions
   - ใช้ locks เมื่อจำเป็น
   - จัดการ resources

## 📚 แหล่งเรียนรู้เพิ่มเติม

1. **เอกสารอ้างอิง**
   - [FastAPI Documentation](https://fastapi.tiangolo.com/)
   - [Pandas Documentation](https://pandas.pydata.org/docs/)
   - [Pytest Documentation](https://docs.pytest.org/)

2. **บทความแนะนำ**
   - [Python Best Practices](https://realpython.com/tutorials/best-practices/)
   - [Security Best Practices](https://owasp.org/www-project-top-ten/)
   - [Testing Best Practices](https://docs.pytest.org/en/latest/goodpractices.html)

3. **วิดีโอสอน**
   - [FastAPI Tutorial](https://www.youtube.com/watch?v=7t2alSnE2-I)
   - [Pandas Tutorial](https://www.youtube.com/watch?v=vmEHCJofslg)
   - [Pytest Tutorial](https://www.youtube.com/watch?v=DhUpxWjOhME)

## 🤝 การขอความช่วยเหลือ

1. **ช่องทางติดต่อ**
   - GitHub Issues
   - Email Support
   - Discussion Forum

2. **การรายงานปัญหา**
   - อธิบายปัญหาชัดเจน
   - แนบ error message
   - ระบุขั้นตอนที่ทำ

3. **การขอฟีเจอร์ใหม่**
   - อธิบายความต้องการ
   - ให้เหตุผลประกอบ
   - เสนอแนวทางแก้ไข 