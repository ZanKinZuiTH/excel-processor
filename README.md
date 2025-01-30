# 📊 Excel Processor - ระบบประมวลผล Excel อัจฉริยะ

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)]()

## 📌 สารบัญ
- [คุณสมบัติเด่น](#-คุณสมบัติเด่น)
- [การติดตั้ง](#-การติดตั้ง)
- [การใช้งาน](#-การใช้งาน)
- [โครงสร้างโปรเจค](#-โครงสร้างโปรเจค)
- [การทดสอบ](#-การทดสอบ)
- [การพัฒนาต่อยอด](#-การพัฒนาต่อยอด)
- [ผู้พัฒนา](#-ผู้พัฒนา)

## ⭐ คุณสมบัติเด่น
- 🚀 **ใช้งานง่าย**: ติดตั้งและเริ่มใช้งานได้ภายใน 5 นาที
- 🔄 **ประมวลผลอัตโนมัติ**: วิเคราะห์ข้อมูล Excel โดยอัตโนมัติ
- 🔒 **ปลอดภัย**: ตรวจสอบและป้องกันข้อมูลสำคัญ
- 🌐 **รองรับ 2 ภาษา**: ไทย/อังกฤษ
- ⚙️ **ปรับแต่งได้**: กำหนดค่าต่างๆ ได้ตามต้องการ
- 📱 **Responsive**: ใช้งานได้ทั้งบน Desktop และ Mobile

## 📥 การติดตั้ง
1. ติดตั้ง Python 3.8 ขึ้นไป
```bash
# ดาวน์โหลดโปรเจค
git clone https://github.com/yourusername/excel-processor.git
cd excel-processor

# ติดตั้ง dependencies
pip install -r requirements.txt

# ติดตั้งระบบ
python cli.py setup
```

## 🚀 การใช้งาน
### GUI (Streamlit)
```bash
python cli.py start
```
เปิดเบราว์เซอร์ไปที่ http://localhost:8501

### CLI
```bash
# ประมวลผลไฟล์
python cli.py process input.xlsx

# ทดสอบระบบ
python cli.py test

# ดูเวอร์ชัน
python cli.py version
```

## 📁 โครงสร้างโปรเจค
```
excel_processor/
├── processor.py     # ระบบประมวลผลหลัก
├── config.py        # การตั้งค่าระบบ
├── security.py      # ระบบความปลอดภัย
├── ui.py            # ส่วนติดต่อผู้ใช้
└── tests/           # ชุดทดสอบ
```

## 🧪 การทดสอบ
```bash
# รันทดสอบทั้งหมด
pytest tests/

# ทดสอบพร้อมรายงานความครอบคลุม
pytest tests/ --cov=./ --cov-report=xml
```

## 🔄 การพัฒนาต่อยอด
1. เพิ่มการวิเคราะห์ข้อมูลเชิงลึก
2. เพิ่มการรายงานผลแบบ Real-time
3. พัฒนา API สำหรับบริการภายนอก
4. เพิ่มการสนับสนุนไฟล์รูปแบบอื่น

## 👨‍💻 ผู้พัฒนา
- นาย ก - Project Lead
- นาย ข - Backend Developer
- นาย ค - Frontend Developer

## 📝 License
MIT License 