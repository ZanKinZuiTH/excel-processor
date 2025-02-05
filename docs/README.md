# 📊 Excel Processor

ระบบประมวลผลไฟล์ Excel อัตโนมัติ พร้อมฟีเจอร์การวิเคราะห์ข้อมูลด้วย AI และการแสดงผลที่หลากหลาย

## 📋 สารบัญ
1. [คุณสมบัติหลัก](#คุณสมบัติหลัก)
2. [การติดตั้ง](#การติดตั้ง)
3. [การใช้งาน](#การใช้งาน)
4. [ระบบ AI](#ระบบ-ai)
5. [โครงสร้างโปรเจค](#โครงสร้างโปรเจค)
6. [API Reference](#api-reference)
7. [การแก้ไขปัญหา](#การแก้ไขปัญหา)
8. [การพัฒนาเพิ่มเติม](#การพัฒนาเพิ่มเติม)

## 🌟 คุณสมบัติหลัก
- ประมวลผลไฟล์ Excel แบบ Batch Processing
- วิเคราะห์เอกสารอัตโนมัติด้วย AI
- สร้าง Template อัตโนมัติด้วย Deep Learning
- รองรับการวิเคราะห์ข้อมูลเชิงลึก
- มีส่วนติดต่อผู้ใช้แบบ Web UI และ CLI
- ระบบ Template สำหรับการประมวลผล
- การแสดงผลด้วยกราฟและตาราง
- ระบบความปลอดภัยและการจัดการผู้ใช้
- รองรับการทำงานบน Docker

## 🔧 การติดตั้ง

### วิธีที่ 1: ติดตั้งโดยตรง
```bash
# 1. Clone โปรเจค
git clone https://github.com/yourusername/excel-processor.git
cd excel-processor

# 2. สร้าง Virtual Environment
python -m venv venv
source venv/bin/activate  # สำหรับ Linux/Mac
venv\Scripts\activate     # สำหรับ Windows

# 3. ติดตั้ง Dependencies
pip install -r requirements.txt

# 4. ติดตั้ง AI Dependencies (optional)
pip install tensorflow opencv-python scikit-learn

# 5. ตั้งค่าไฟล์ .env
cp .env.example .env
# แก้ไขค่าใน .env ตามต้องการ
```

### วิธีที่ 2: ใช้ Docker
```bash
# 1. Build Image
docker-compose build

# 2. รัน Container
docker-compose up -d
```

## 🎯 การใช้งาน

### 1. Web UI
1. รันเซิร์ฟเวอร์:
```bash
python app.py
```
2. เปิดเบราว์เซอร์ไปที่ `http://localhost:8000`
3. เข้าสู่ระบบด้วยบัญชีผู้ใช้
4. อัพโหลดไฟล์ Excel ที่ต้องการประมวลผล
5. เลือก Template และตั้งค่าการประมวลผล
6. กดประมวลผลและรอผลลัพธ์

### 2. Command Line Interface
```bash
# ประมวลผลไฟล์เดียว
python cli.py process single input.xlsx

# ประมวลผลหลายไฟล์
python cli.py process batch folder_path/

# สร้าง Template ใหม่
python cli.py template create template_name

# ดูรายการ Template
python cli.py template list
```

## 🤖 ระบบ AI

### ความสามารถของระบบ AI
1. **การวิเคราะห์เอกสาร**
   - วิเคราะห์โครงสร้างเอกสารด้วย CNN
   - แยกประเภทเอกสารอัตโนมัติ
   - วิเคราะห์ฟิลด์ข้อมูลด้วย CNN+LSTM

2. **การสร้าง Template อัตโนมัติ**
   - เรียนรู้รูปแบบจากตัวอย่าง
   - แนะนำการตั้งค่าที่เหมาะสม
   - ปรับปรุง Template อัตโนมัติ

3. **การวิเคราะห์ข้อมูล**
   - ตรวจจับรูปแบบข้อมูล
   - วิเคราะห์ความสัมพันธ์
   - ทำนายประเภทข้อมูล

### การใช้งานระบบ AI
```python
from excel_processor import AIFormLearner

# สร้าง AI Learner
learner = AIFormLearner()

# เทรนโมเดล
learner.train(
    excel_files=['sample1.xlsx', 'sample2.xlsx'],
    labels=['invoice', 'report'],
    epochs=10
)

# วิเคราะห์เอกสารใหม่
result = learner.predict('new_doc.xlsx')
print(f"Document Type: {result['document_type']}")
print(f"Confidence: {result['confidence']}")

# บันทึกโมเดล
learner.save_model('models/my_model')
```

### การปรับแต่งระบบ AI
- ปรับแต่งพารามิเตอร์ใน `config/ai_config.json`
- เพิ่มประเภทเอกสารใหม่
- ปรับปรุงโมเดลด้วยข้อมูลใหม่
- ใช้ GPU เพื่อเพิ่มประสิทธิภาพ

## 📁 โครงสร้างโปรเจค
```
excel-processor/
├── app.py              # Web Application หลัก
├── cli.py              # Command Line Interface
├── config.py           # การตั้งค่าระบบ
├── api.py              # REST API Endpoints
├── security.py         # ระบบความปลอดภัย
├── excel_processor/    # โมดูลหลัก
│   ├── processor.py    # ตัวประมวลผล Excel
│   ├── form_manager.py # ระบบจัดการฟอร์ม
│   ├── ai_learner.py   # ระบบ AI
│   └── utils.py        # Utility Functions
├── models/            # โมเดล AI
├── templates/         # Template Files
├── static/           # Static Files
├── tests/            # Unit Tests
└── docs/             # เอกสารประกอบ
```

## 📚 API Reference

### REST API
- `POST /api/process`
  - ประมวลผลไฟล์ Excel
  - Parameters:
    - `file`: ไฟล์ Excel (multipart/form-data)
    - `template_id`: ID ของ Template
    - `options`: ตัวเลือกการประมวลผล (JSON)

- `GET /api/templates`
  - ดึงรายการ Template ทั้งหมด

- `POST /api/templates`
  - สร้าง Template ใหม่
  - Body: Template Configuration (JSON)

### AI API
```python
# วิเคราะห์เอกสาร
POST /api/ai/analyze
Parameters:
  - file: ไฟล์ Excel (multipart/form-data)
Response:
  - document_type: ประเภทเอกสาร
  - confidence: ความเชื่อมั่น
  - field_analysis: ผลวิเคราะห์ฟิลด์

# เทรนโมเดล
POST /api/ai/train
Parameters:
  - files: ไฟล์ตัวอย่าง (multipart/form-data)
  - labels: ประเภทเอกสาร (JSON)
  - epochs: จำนวนรอบเทรน

# ดูสถานะการเทรน
GET /api/ai/status
```

## 🔍 การแก้ไขปัญหา

### ปัญหาที่พบบ่อย
1. **ไฟล์ไม่สามารถอ่านได้**
   - ตรวจสอบรูปแบบไฟล์ (.xlsx, .xls)
   - ตรวจสอบการเข้ารหัสไฟล์
   - ลองเปิดไฟล์ด้วย Excel ก่อน

2. **Template ไม่ตรงกับข้อมูล**
   - ตรวจสอบชื่อคอลัมน์ใน Template
   - ตรวจสอบประเภทข้อมูลที่กำหนด
   - อัพเดท Template ให้ตรงกับข้อมูล

3. **ระบบทำงานช้า**
   - ลดขนาดไฟล์ข้อมูล
   - เพิ่ม RAM ให้ระบบ
   - ใช้ Batch Processing

### ปัญหาเกี่ยวกับ AI
1. **โมเดลทำนายผิดพลาด**
   - เพิ่มข้อมูลเทรน
   - ปรับแต่งพารามิเตอร์
   - ตรวจสอบคุณภาพข้อมูล

2. **การเทรนใช้เวลานาน**
   - ใช้ GPU
   - ลดขนาด Batch
   - ลดจำนวน Epochs

3. **หน่วยความจำไม่พอ**
   - เพิ่ม RAM
   - ลดขนาด Batch
   - ใช้ Data Generator

## 🚀 การพัฒนาเพิ่มเติม

### การเพิ่ม Template ใหม่
1. สร้างไฟล์ Template ใน `templates/`
2. กำหนดโครงสร้างข้อมูล
3. ทดสอบ Template
4. อัพเดทเอกสาร

### การเพิ่มฟีเจอร์ใหม่
1. สร้าง Branch ใหม่
2. พัฒนาฟีเจอร์
3. เขียน Unit Tests
4. ทำ Pull Request

## 📝 License
MIT License - ดูรายละเอียดใน [LICENSE](LICENSE) 