# 📊 Excel Processor - ระบบประมวลผล Excel อัจฉริยะ

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)]()
[![License](https://img.shields.io/badge/license-BRXG%20Co.-green)]()
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)]()

## 📌 สารบัญ
- [คุณสมบัติเด่น](#-คุณสมบัติเด่น)
- [การติดตั้ง](#-การติดตั้ง)
- [การใช้งาน](#-การใช้งาน)
- [ฟีเจอร์หลัก](#-ฟีเจอร์หลัก)
- [โครงสร้างโปรเจค](#-โครงสร้างโปรเจค)
- [การทดสอบ](#-การทดสอบ)
- [การพัฒนาต่อยอด](#-การพัฒนาต่อยอด)
- [ผู้พัฒนา](#-ผู้พัฒนา)

## ⭐ คุณสมบัติเด่น
- 🚀 **ใช้งานง่าย**: ติดตั้งและเริ่มใช้งานได้ภายใน 5 นาที
- 🔄 **ประมวลผลอัตโนมัติ**: วิเคราะห์ข้อมูล Excel โดยอัตโนมัติ
- 🔍 **ตรวจสอบข้อมูล**: ค้นหาค่า null, ข้อมูลซ้ำ และค่าผิดปกติ
- 📊 **วิเคราะห์เชิงลึก**: สถิติพื้นฐาน, การจัดกลุ่ม และแนวโน้ม
- 🧹 **ทำความสะอาดข้อมูล**: จัดการค่า null และข้อมูลซ้ำอัตโนมัติ
- 🌐 **รองรับ 2 ภาษา**: ไทย/อังกฤษ
- ⚙️ **ปรับแต่งได้**: กำหนดค่าต่างๆ ได้ตามต้องการ
- 📱 **Responsive**: ใช้งานได้ทั้งบน Desktop และ Mobile

## 📥 การติดตั้ง
1. ติดตั้ง Python 3.8 ขึ้นไป
```bash
# ดาวน์โหลดโปรเจค
git clone https://github.com/BRXG/excel-processor.git
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

## 🛠️ ฟีเจอร์หลัก

### 1. การประมวลผลข้อมูล
```python
from excel_processor import ExcelProcessor

# สร้าง instance
processor = ExcelProcessor("data.xlsx")

# ประมวลผลข้อมูล
result = processor.process_file()
```

### 2. การตรวจสอบข้อมูล
```python
# ตรวจสอบความถูกต้อง
validation = processor.validate_data()

# ดูผลการตรวจสอบ
print(f"ค่า null: {validation['null_check']}")
print(f"ข้อมูลซ้ำ: {validation['duplicate_check']}")
print(f"ค่าผิดปกติ: {validation['outliers']}")
```

### 3. การวิเคราะห์ข้อมูล
```python
# วิเคราะห์ข้อมูล
analysis = processor.analyze_data()

# ดูผลการวิเคราะห์
print(f"สถิติ: {analysis['numeric_stats']}")
print(f"การจัดกลุ่ม: {analysis['groupby_results']}")
```

### 4. การทำความสะอาดข้อมูล
```python
# ทำความสะอาดข้อมูล
processor.clean_data()
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
5. เพิ่มการตรวจจับรูปแบบข้อมูลอัตโนมัติ
6. พัฒนาระบบแนะนำการแก้ไขข้อมูล

## 👨‍💻 ผู้พัฒนา
- BRXG Co. Development Team
- Email: contact@brxg.co.th
- Website: https://brxg.co.th

## 📝 License
Copyright © 2024 BRXG Co. All rights reserved.

This software is proprietary and confidential. 
Unauthorized copying of this file, via any medium is strictly prohibited.
Written by BRXG Development Team <dev@brxg.co.th>, 2024 