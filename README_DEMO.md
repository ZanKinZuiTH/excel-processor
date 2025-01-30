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

# 📚 Excel Processor - คู่มือการใช้งานและตัวอย่าง

## 📋 สารบัญ
- [การติดตั้ง](#-การติดตั้ง)
- [การใช้งานพื้นฐาน](#-การใช้งานพื้นฐาน)
- [ตัวอย่างการใช้งาน](#-ตัวอย่างการใช้งาน)
- [คำถามที่พบบ่อย](#-คำถามที่พบบ่อย)

## 📥 การติดตั้ง

### วิธีที่ 1: ติดตั้งผ่าน CLI
```bash
# ติดตั้งระบบ
python cli.py setup

# ตรวจสอบการติดตั้ง
python cli.py version
```

### วิธีที่ 2: ติดตั้งด้วยตนเอง
1. ติดตั้ง Python 3.8+
2. ติดตั้ง dependencies: `pip install -r requirements.txt`
3. ตั้งค่าระบบ: `python cli.py setup`

## 🚀 การใช้งานพื้นฐาน

### 1. เริ่มใช้งาน GUI
```bash
python cli.py start
```
เปิดเบราว์เซอร์ไปที่ http://localhost:8501

### 2. อัพโหลดไฟล์
1. คลิกปุ่ม "อัพโหลดไฟล์"
2. เลือกไฟล์ Excel ของคุณ
3. รอระบบประมวลผล

## 📊 ตัวอย่างการใช้งาน

### 1. วิเคราะห์ข้อมูล
```python
from excel_processor import ExcelProcessor

# สร้าง instance
processor = ExcelProcessor("data.xlsx")

# วิเคราะห์ข้อมูล
results = processor.analyze_data()
print(f"จำนวนแถว: {results['total_rows']}")
print(f"คอลัมน์: {results['columns']}")
```

### 2. สร้างรายงาน PDF
```python
# ประมวลผลและสร้าง PDF
processor.process_file()
processor.export_pdf("report.pdf")
```

### 3. การตั้งค่าขั้นสูง
```python
# กำหนดค่าการประมวลผล
processor.config.set({
    "language": "th",
    "theme": "dark",
    "export_path": "./exports"
})
```

## ❓ คำถามที่พบบ่อย

### Q: รองรับไฟล์ Excel รูปแบบใดบ้าง?
A: รองรับไฟล์ .xlsx, .xls และ .csv

### Q: มีข้อจำกัดขนาดไฟล์หรือไม่?
A: รองรับไฟล์ขนาดไม่เกิน 100MB

### Q: รองรับภาษาไทยหรือไม่?
A: รองรับทั้งภาษาไทยและภาษาอังกฤษ

### Q: แก้ปัญหาภาษาไทยแสดงผลไม่ถูกต้องอย่างไร?
```python
# ตั้งค่า encoding
processor.config.set({
    "encoding": "utf-8-sig"
})
```

## 🔧 การใช้งานเพิ่มเติม

### CLI Commands
```bash
# ประมวลผลไฟล์
python cli.py process input.xlsx

# สร้างเทมเพลต
python cli.py template create

# ตรวจสอบสถานะ
python cli.py status
```

### API Usage
```python
# ใช้งานผ่าน API
from excel_processor import api

# ประมวลผลไฟล์
response = api.process_file("data.xlsx")

# ดึงข้อมูล
data = api.get_data(response["id"])
```

## 🛠️ การแก้ไขปัญหา

### ปัญหาที่พบบ่อย
1. ไฟล์เสียหาย: ใช้คำสั่ง `python cli.py repair`
2. ข้อมูลไม่สมบูรณ์: ตรวจสอบ log ที่ `logs/error.log`
3. ระบบทำงานช้า: ลองลด batch size ในการประมวลผล

### การติดต่อสนับสนุน
- Email: support@brxg.co.th
- Line: @brxgdev
- GitHub Issues: [รายงานปัญหา](https://github.com/BRXG/excel-processor/issues)

---
⚡️ พัฒนาโดย [BRXG Co.](https://brxg.co.th) - Making Excellence Simple 