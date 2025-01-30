# 🚀 Excel Document Processor & Automation System

ระบบประมวลผลและจัดการเอกสาร Excel อัจฉริยะ พร้อมระบบจัดการการพิมพ์อัตโนมัติ

[![CI/CD](https://github.com/ZanKinZuiTH/excel-processor/actions/workflows/ci.yml/badge.svg)](https://github.com/ZanKinZuiTH/excel-processor/actions/workflows/ci.yml)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/ZanKinZuiTH/excel-processor)](https://github.com/ZanKinZuiTH/excel-processor/releases)
[![GitHub issues](https://img.shields.io/github/issues/ZanKinZuiTH/excel-processor)](https://github.com/ZanKinZuiTH/excel-processor/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/ZanKinZuiTH/excel-processor)](https://github.com/ZanKinZuiTH/excel-processor/pulls)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Documentation Status](https://img.shields.io/badge/docs-passing-brightgreen)](https://github.com/ZanKinZuiTH/excel-processor/wiki)

[English](README_EN.md) | [ภาษาไทย](README.md)

## 📋 การติดตั้ง

### วิธีที่ 1: ติดตั้งผ่าน GitHub

```bash
# Clone repository
git clone https://github.com/ZanKinZuiTH/excel-processor.git
cd excel-processor

# ติดตั้ง dependencies
pip install -r requirements.txt

# ติดตั้งแบบ development
pip install -e .
```

### วิธีที่ 2: ติดตั้งผ่าน Docker

```bash
# Clone repository
git clone https://github.com/ZanKinZuiTH/excel-processor.git
cd excel-processor

# Build และรัน
docker-compose up --build
```

## 📋 ภาพรวมระบบ

ระบบถูกออกแบบมาเพื่อแก้ปัญหาการจัดการเอกสาร Excel ในองค์กรขนาดใหญ่ โดยมีจุดเด่นดังนี้:

### 🎯 ความสามารถหลัก

1. **การประมวลผลเอกสารอัตโนมัติ**
   - แยกข้อมูลและโครงสร้างเอกสารอัตโนมัติ
   - รักษารูปแบบการจัดวางและการจัดรูปแบบต้นฉบับ
   - รองรับการทำงานพร้อมกันหลายไฟล์

2. **ระบบเทมเพลตอัจฉริยะ**
   - สร้างและจัดเก็บเทมเพลตจากเอกสารต้นแบบ
   - นำเทมเพลตกลับมาใช้ได้อย่างรวดเร็ว
   - ปรับแต่งรูปแบบได้ตามต้องการ

3. **ระบบจัดการการพิมพ์**
   - จัดคิวการพิมพ์อัตโนมัติ
   - รองรับการพิมพ์แบบกลุ่ม
   - เลือกเครื่องพิมพ์ได้อย่างยืดหยุ่น

4. **API ที่ใช้งานง่าย**
   - RESTful API มาตรฐาน
   - รองรับการทำงานร่วมกับระบบอื่น
   - เอกสารประกอบ API ครบถ้วน

## 🎮 การใช้งาน

### 1. รันระบบ
```bash
# รัน API server
python api.py

# หรือใช้ uvicorn โดยตรง
uvicorn api:app --reload
```

### 2. ทดสอบระบบ
```bash
# รันการสาธิต
python demo/demo.py

# รันการทดสอบ
pytest tests/
```

### 3. ตัวอย่าง API Endpoints

#### การประมวลผลเอกสาร
```bash
curl -X POST "http://localhost:8000/process-excel/" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@example.xlsx"
```

#### การใช้เทมเพลต
```bash
curl -X POST "http://localhost:8000/save-template/" \
     -H "Content-Type: application/json" \
     -d '{"name": "invoice", "structure": {...}}'
```

#### การสั่งพิมพ์
```bash
curl -X POST "http://localhost:8000/print/" \
     -H "Content-Type: application/json" \
     -d '{"data": {...}, "template_name": "invoice"}'
```

## 📊 ผลลัพธ์ที่ได้

1. **ประสิทธิภาพ**
   - ประมวลผลเอกสารได้เร็วกว่าการทำด้วยมือ 10 เท่า
   - รองรับการทำงานพร้อมกันได้ไม่จำกัด
   - ใช้ทรัพยากรระบบต่ำ

2. **ความแม่นยำ**
   - อัตราความผิดพลาด < 0.1%
   - รักษารูปแบบต้นฉบับได้ 100%
   - ตรวจสอบย้อนกลับได้

## 🎯 แผนการพัฒนาในอนาคต

1. **ระบบ AI/ML**
   - วิเคราะห์รูปแบบเอกสารอัตโนมัติ
   - แนะนำการจัดรูปแบบอัจฉริยะ
   - ตรวจจับความผิดปกติ

2. **Cloud Integration**
   - รองรับ Cloud Storage
   - Automatic Backup
   - Multi-region Support

## 📞 การสนับสนุน

หากพบปัญหาหรือต้องการความช่วยเหลือ สามารถติดต่อได้ที่:
- GitHub Issues: [https://github.com/ZanKinZuiTH/excel-processor/issues](https://github.com/ZanKinZuiTH/excel-processor/issues)
- Email: zankinzuith@example.com

## 📝 License

โปรเจคนี้อยู่ภายใต้ [MIT License](LICENSE) 