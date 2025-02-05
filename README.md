# 🚀 Excel Processor

ระบบประมวลผล Excel อัจฉริยะ พร้อมระบบ AI วิเคราะห์และจัดการเทมเพลตอัตโนมัติ

## ✨ คุณสมบัติเด่น

### 🤖 ระบบ AI อัจฉริยะ
- วิเคราะห์โครงสร้างเอกสารอัตโนมัติ
- แนะนำเทมเพลตที่เหมาะสม
- เรียนรู้และปรับปรุงจากการใช้งาน

### 📑 จัดการเทมเพลตอัตโนมัติ
- คลังเทมเพลตสำเร็จรูป
- สร้างและปรับแต่งเทมเพลตใหม่
- แชร์และจัดการเวอร์ชัน

### 🔄 ประมวลผลอัตโนมัติ
- รองรับไฟล์ Excel ทุกรูปแบบ
- ประมวลผลแบบ Batch
- ตรวจสอบและแก้ไขข้อมูลอัตโนมัติ

### 👥 ทำงานร่วมกัน
- แชร์เทมเพลตระหว่างผู้ใช้
- จัดการสิทธิ์การเข้าถึง
- ติดตามการเปลี่ยนแปลง

## 🛠️ การติดตั้ง

### ความต้องการของระบบ
- Python 3.8+
- PostgreSQL 12+
- Redis 6+
- 8GB RAM ขึ้นไป

### วิธีติดตั้ง
```bash
# Clone repository
git clone https://github.com/yourusername/excel-processor.git
cd excel-processor

# สร้าง virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# หรือ
.\venv\Scripts\activate  # Windows

# ติดตั้ง dependencies
pip install -r requirements.txt

# ตั้งค่าฐานข้อมูล
python setup.py init-db

# รันระบบ
python cli.py start
```

## 📖 การใช้งาน

### Web Interface
1. เปิดเบราว์เซอร์ไปที่ `http://localhost:8501`
2. เข้าสู่ระบบด้วยบัญชีผู้ใช้
3. อัพโหลดไฟล์ Excel ที่ต้องการประมวลผล
4. เลือกเทมเพลตหรือใช้ระบบ AI แนะนำ
5. ดูผลลัพธ์และดาวน์โหลดไฟล์

### Command Line
```bash
# ประมวลผลไฟล์เดียว
python cli.py process single input.xlsx

# ประมวลผลหลายไฟล์
python cli.py process batch input_folder/

# สร้างเทมเพลตใหม่
python cli.py template create my_template
```

## 🔧 การตั้งค่า

### การตั้งค่าฐานข้อมูล
```bash
# สร้างไฟล์ .env
cp .env.example .env

# แก้ไขการตั้งค่าใน .env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=exceldb
DB_USER=exceluser
DB_PASSWORD=your_password
```

### การตั้งค่า AI
```bash
# ตั้งค่าใน config/ai_config.json
{
    "model_path": "models/",
    "use_gpu": true,
    "batch_size": 32
}
```

## 📚 เอกสาร

### คู่มือการใช้งาน
- [คู่มือผู้ใช้](docs/user_guide.md)
- [คู่มือการนำเสนอ](docs/presentation_guide.md)
- [คู่มือการติดตั้งเซิร์ฟเวอร์](docs/server_setup.md)

### API Reference
- [API Documentation](https://api.example.com)
- [OpenAPI Specification](docs/openapi.json)

## 🤝 การสนับสนุน

### ช่องทางติดต่อ
- Email: support@example.com
- โทร: 02-xxx-xxxx
- Line: @excelprocessor
- Discord: discord.gg/excelprocessor

### การรายงานปัญหา
- สร้าง Issue ใน GitHub
- แจ้งผ่านระบบ Support Ticket
- ติดต่อทีมสนับสนุนโดยตรง

## 📝 License

โครงการนี้อยู่ภายใต้ MIT License - ดูรายละเอียดใน [LICENSE](LICENSE) 