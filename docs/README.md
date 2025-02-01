# 📊 Excel Processor

ระบบประมวลผลไฟล์ Excel อัตโนมัติ พร้อมฟีเจอร์การวิเคราะห์ข้อมูลและการแสดงผลที่หลากหลาย

## 📋 สารบัญ
1. [คุณสมบัติหลัก](#คุณสมบัติหลัก)
2. [การติดตั้ง](#การติดตั้ง)
3. [การใช้งาน](#การใช้งาน)
4. [โครงสร้างโปรเจค](#โครงสร้างโปรเจค)
5. [API Reference](#api-reference)
6. [การแก้ไขปัญหา](#การแก้ไขปัญหา)
7. [การพัฒนาเพิ่มเติม](#การพัฒนาเพิ่มเติม)

## 🌟 คุณสมบัติหลัก
- ประมวลผลไฟล์ Excel แบบ Batch Processing
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

# 4. ตั้งค่าไฟล์ .env
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
│   └── utils.py        # Utility Functions
├── templates/          # Template Files
├── static/            # Static Files
├── tests/             # Unit Tests
└── docs/              # เอกสารประกอบ
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

### Python API
```python
from excel_processor import ExcelProcessor

# สร้าง Instance
processor = ExcelProcessor()

# โหลดไฟล์
processor.load_file("input.xlsx")

# ประมวลผล
results = processor.process()

# วิเคราะห์ข้อมูล
analysis = processor.analyze_data()

# ส่งออกผลลัพธ์
processor.export_results("output.xlsx")
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