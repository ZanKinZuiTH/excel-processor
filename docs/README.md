# 📊 Excel Processor - ระบบประมวลผล Excel อัจฉริยะ

## 📑 สารบัญ
1. [ภาพรวมระบบ](#ภาพรวมระบบ)
2. [คุณสมบัติเด่น](#คุณสมบัติเด่น)
3. [การติดตั้ง](#การติดตั้ง)
4. [การใช้งาน](#การใช้งาน)
5. [ระบบ AI](#ระบบ-ai)
6. [เอกสารอ้างอิง](#เอกสารอ้างอิง)
7. [การพัฒนาต่อยอด](#การพัฒนาต่อยอด)

## 🌟 ภาพรวมระบบ
ระบบประมวลผลไฟล์ Excel อัจฉริยะที่ช่วยให้การจัดการข้อมูลเป็นเรื่องง่าย ด้วยความสามารถ:
- 🤖 วิเคราะห์ข้อมูลอัตโนมัติด้วย AI
- 📝 จัดการเทมเพลตอย่างชาญฉลาด
- 🔍 ตรวจสอบและแก้ไขข้อผิดพลาด
- 📊 สร้างรายงานและกราฟที่สวยงาม

## ⭐ คุณสมบัติเด่น

### การจัดการเทมเพลต
- สร้างและแก้ไขเทมเพลตอัตโนมัติ
- แชร์เทมเพลตระหว่างผู้ใช้
- ควบคุมเวอร์ชันของเทมเพลต
- แนะนำเทมเพลตที่เหมาะสม

### การประมวลผลข้อมูล
- รองรับการประมวลผลแบบกลุ่ม
- วิเคราะห์โครงสร้างข้อมูลอัตโนมัติ
- ตรวจจับและแก้ไขข้อผิดพลาด
- แปลงรูปแบบข้อมูลอัตโนมัติ

### ระบบ AI
- วิเคราะห์รูปแบบเอกสาร
- แนะนำการตั้งค่าที่เหมาะสม
- เรียนรู้จากตัวอย่างอัตโนมัติ
- ปรับปรุงประสิทธิภาพต่อเนื่อง

## 🔧 การติดตั้ง

### ความต้องการระบบ
- Python 3.8 หรือสูงกว่า
- RAM 4GB ขึ้นไป
- พื้นที่ว่าง 500MB

### ขั้นตอนการติดตั้ง
```bash
# 1. Clone โปรเจค
git clone https://github.com/yourusername/excel-processor.git
cd excel-processor

# 2. สร้าง Virtual Environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. ติดตั้ง Dependencies
pip install -r requirements.txt

# 4. ตั้งค่าระบบ
python cli.py setup
```

## 🎯 การใช้งาน

### Web Interface
1. เริ่มต้นระบบ:
```bash
python cli.py start
```
2. เปิดเบราว์เซอร์ไปที่ `http://localhost:8501`

### Command Line
```bash
# ประมวลผลไฟล์
python cli.py process input.xlsx

# สร้างเทมเพลต
python cli.py template create

# วิเคราะห์ด้วย AI
python cli.py analyze data.xlsx
```

## 🤖 ระบบ AI

### ความสามารถ
- วิเคราะห์โครงสร้างเอกสาร
- แนะนำเทมเพลตที่เหมาะสม
- เรียนรู้จากตัวอย่าง
- ปรับปรุงประสิทธิภาพอัตโนมัติ

### การใช้งาน AI
```python
from excel_processor import AIProcessor

# สร้าง AI Processor
processor = AIProcessor()

# วิเคราะห์เอกสาร
result = processor.analyze("data.xlsx")

# แนะนำเทมเพลต
suggestions = processor.suggest_template("data.xlsx")
```

## 📚 เอกสารอ้างอิง

### คู่มือการใช้งาน
- [คู่มือผู้ใช้](docs/user_guide.md)
- [คู่มือการติดตั้ง](docs/server_setup.md)
- [คู่มือการนำเสนอ](docs/presentation_guide.md)

### API Reference
- [REST API Documentation](docs/api_reference.md)
- [Python SDK Documentation](docs/sdk_reference.md)

## 🚀 การพัฒนาต่อยอด

### แผนการพัฒนา
1. เพิ่มการวิเคราะห์ข้อมูลเชิงลึก
2. พัฒนาระบบ AI ให้ฉลาดขึ้น
3. เพิ่มรูปแบบรายงานใหม่
4. ปรับปรุงประสิทธิภาพการประมวลผล

### การมีส่วนร่วม
- Fork โปรเจค
- สร้าง Feature Branch
- ส่ง Pull Request
- รายงานปัญหาที่พบ

## 📞 การสนับสนุน
- Email: support@example.com
- เว็บไซต์: https://example.com
- GitHub Issues

## 📄 License
MIT License - ดูรายละเอียดใน [LICENSE](LICENSE) 