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
- [การใช้งานขั้นสูง](#-การใช้งานขั้นสูง)
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

### 1. การประมวลผลข้อมูลพื้นฐาน
```python
from excel_processor import ExcelProcessor

# สร้าง instance
processor = ExcelProcessor("data.xlsx")

# ประมวลผลข้อมูล
result = processor.process_file()

# ดูข้อมูลลูกค้า
print(result["customer_info"])

# ดูสรุปข้อมูล
print(f"จำนวนแถว: {result['summary']['total_rows']}")
print(f"คอลัมน์: {result['summary']['columns']}")
```

### 2. การตรวจสอบและทำความสะอาดข้อมูล
```python
# ตรวจสอบข้อมูล
validation = processor.validate_data()

# ดูผลการตรวจสอบ
print("ค่า null:")
for col, count in validation["null_check"]["missing_values"].items():
    if count > 0:
        print(f"- {col}: {count} แถว ({validation['null_check']['missing_percentage'][col]:.2f}%)")

print("\nข้อมูลซ้ำ:")
print(f"- จำนวน: {validation['duplicate_check']['duplicates']} แถว")
print(f"- เปอร์เซ็นต์: {validation['duplicate_check']['duplicate_percentage']:.2f}%")

# ทำความสะอาดข้อมูล
processor.clean_data()
```

### 3. การวิเคราะห์ข้อมูลเชิงลึก
```python
# วิเคราะห์ข้อมูล
analysis = processor.analyze_data()

# ดูสถิติพื้นฐาน
for col, stats in analysis["numeric_stats"].items():
    print(f"\nสถิติของคอลัมน์ {col}:")
    print(f"- ค่าเฉลี่ย: {stats['mean']:.2f}")
    print(f"- ส่วนเบี่ยงเบน: {stats['std']:.2f}")
    print(f"- ค่าต่ำสุด: {stats['min']:.2f}")
    print(f"- ค่าสูงสุด: {stats['max']:.2f}")

# ดูการจัดกลุ่ม
for col, groups in analysis["groupby_results"].items():
    print(f"\nการจัดกลุ่มของ {col}:")
    for value, count in groups.items():
        print(f"- {value}: {count} รายการ")
```

## 🔧 การใช้งานขั้นสูง

### 1. การจัดการข้อมูลขนาดใหญ่
```python
# ตั้งค่าการประมวลผล
processor.config.set({
    "chunk_size": 10000,
    "use_multiprocessing": True,
    "n_jobs": -1  # ใช้ CPU ทั้งหมด
})

# ประมวลผลไฟล์ขนาดใหญ่
result = processor.process_file()
```

### 2. การปรับแต่งการทำความสะอาดข้อมูล
```python
# กำหนดค่าเริ่มต้นสำหรับค่า null
default_values = {
    'ชื่อ-นามสกุล': 'ไม่ระบุ',
    'ที่อยู่': 'ไม่ระบุ',
    'เลขประจำตัวผู้เสียภาษี': '0000000000',
    'ยอดขาย': 0,
    'วันที่': pd.Timestamp.now()
}

# ทำความสะอาดข้อมูลแบบกำหนดเอง
processor.df = processor.df.fillna(default_values)
processor.df = processor.df.drop_duplicates(subset=['เลขประจำตัวผู้เสียภาษี'])
```

### 3. การส่งออกผลลัพธ์
```python
# บันทึกเป็น Excel
processor.save_template("clean_data.xlsx")

# ส่งออกเป็น CSV
processor.df.to_csv("data.csv", index=False, encoding="utf-8-sig")

# สร้างรายงาน PDF
processor.export_pdf("report.pdf", include_charts=True)
```

## ❓ คำถามที่พบบ่อย

### Q: รองรับไฟล์ Excel รูปแบบใดบ้าง?
A: รองรับไฟล์ .xlsx, .xls และ .csv

### Q: มีข้อจำกัดขนาดไฟล์หรือไม่?
A: รองรับไฟล์ขนาดไม่เกิน 100MB สำหรับการประมวลผลปกติ และ 1GB สำหรับการประมวลผลแบบ chunk

### Q: รองรับภาษาไทยหรือไม่?
A: รองรับทั้งภาษาไทยและภาษาอังกฤษ พร้อมระบบตรวจจับและแก้ไขปัญหาการแสดงผลภาษาไทยอัตโนมัติ

### Q: แก้ปัญหาภาษาไทยแสดงผลไม่ถูกต้องอย่างไร?
```python
# ตั้งค่า encoding
processor.config.set({
    "encoding": "utf-8-sig",
    "font_family": "THSarabunNew"
})
```

## 🛠️ การแก้ไขปัญหาทั่วไป

### 1. ปัญหาการโหลดไฟล์
```python
try:
    processor = ExcelProcessor("data.xlsx")
except FileNotFoundError:
    print("ไม่พบไฟล์ที่ระบุ")
except Exception as e:
    print(f"เกิดข้อผิดพลาด: {str(e)}")
```

### 2. ปัญหาหน่วยความจำ
```python
# ใช้การโหลดแบบ chunk
processor.config.set({
    "chunk_size": 5000,
    "low_memory": True
})
```

### 3. ปัญหาประสิทธิภาพ
```python
# เพิ่มประสิทธิภาพการประมวลผล
processor.config.set({
    "use_multiprocessing": True,
    "n_jobs": 4,
    "optimize_memory": True
})
```

### การติดต่อสนับสนุน
- Email: support@brxg.co.th
- Line: @brxgdev
- GitHub Issues: [รายงานปัญหา](https://github.com/BRXG/excel-processor/issues)

---
⚡️ พัฒนาโดย [BRXG Co.](https://brxg.co.th) - Making Excellence Simple 