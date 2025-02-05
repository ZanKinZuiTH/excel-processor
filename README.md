# 🚀 Excel Processor

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)]()
[![Discord](https://img.shields.io/badge/discord-join%20chat-7289da)]()

> ระบบประมวลผล Excel อัจฉริยะ พร้อมระบบ AI วิเคราะห์และจัดการเทมเพลตอัตโนมัติ

[🇹🇭 ภาษาไทย](README.md) | [🇺🇸 English](README_EN.md) | [🎮 Demo](README_DEMO.md)

<p align="center">
  <img src="docs/images/demo.gif" alt="Excel Processor Demo" width="600">
</p>

## 📑 สารบัญ
- [✨ คุณสมบัติเด่น](#-คุณสมบัติเด่น)
- [🛠️ การติดตั้ง](#️-การติดตั้ง)
- [📖 การใช้งาน](#-การใช้งาน)
- [🔧 การตั้งค่า](#-การตั้งค่า)
- [📚 เอกสาร](#-เอกสาร)
- [👨‍💻 สำหรับนักพัฒนา](#-สำหรับนักพัฒนา)
- [🤝 การสนับสนุน](#-การสนับสนุน)
- [📝 License](#-license)

## ✨ คุณสมบัติเด่น

<table>
<tr>
<td width="50%">

### 🤖 ระบบ AI อัจฉริยะ
- วิเคราะห์โครงสร้างเอกสารอัตโนมัติ
- แนะนำเทมเพลตที่เหมาะสม
- เรียนรู้และปรับปรุงจากการใช้งาน

### 📑 จัดการเทมเพลตอัตโนมัติ
- คลังเทมเพลตสำเร็จรูป
- สร้างและปรับแต่งเทมเพลตใหม่
- แชร์และจัดการเวอร์ชัน

</td>
<td width="50%">

### 🔄 ประมวลผลอัตโนมัติ
- รองรับไฟล์ Excel ทุกรูปแบบ
- ประมวลผลแบบ Batch
- ตรวจสอบและแก้ไขข้อมูลอัตโนมัติ

### 👥 ทำงานร่วมกัน
- แชร์เทมเพลตระหว่างผู้ใช้
- จัดการสิทธิ์การเข้าถึง
- ติดตามการเปลี่ยนแปลง

</td>
</tr>
</table>

## 🚀 เริ่มต้นใช้งานใน 5 นาที

1️⃣ **ติดตั้งระบบ**
```bash
# Clone repository
git clone https://github.com/ZanKinZuiTH/excel-processor.git
cd excel-processor

# สร้าง virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# ติดตั้ง dependencies
pip install -r requirements.txt
```

2️⃣ **ตั้งค่าระบบ**
```bash
# ตั้งค่าเริ่มต้น
python setup.py init

# ตั้งค่าฐานข้อมูล
python setup.py init-db
```

3️⃣ **เริ่มใช้งาน**
```bash
# รันระบบ
python cli.py start
```

🌐 เปิดเบราว์เซอร์ไปที่ http://localhost:8501

## 📖 การใช้งานเบื้องต้น

<table>
<tr>
<td width="33%">
<h3>🖥️ Web Interface</h3>
<img src="docs/images/web-ui.png" alt="Web UI">

1. เข้าสู่ระบบ
2. อัพโหลดไฟล์ Excel
3. เลือกเทมเพลต/AI
4. ดูผลลัพธ์

</td>
<td width="33%">
<h3>📱 Mobile Interface</h3>
<img src="docs/images/mobile-ui.png" alt="Mobile UI">

- รองรับทุกอุปกรณ์
- UI ปรับตามหน้าจอ
- ใช้งานง่าย

</td>
<td width="33%">
<h3>💻 Command Line</h3>
<img src="docs/images/cli-ui.png" alt="CLI">

```bash
# ประมวลผลไฟล์
python cli.py process input.xlsx

# สร้างเทมเพลต
python cli.py template create
```

</td>
</tr>
</table>

## 👨‍💻 สำหรับนักพัฒนา

### 🔧 โครงสร้างโปรเจค
```
excel_processor/
├── processor.py     # ระบบประมวลผลหลัก
├── ai_model/        # โมเดล AI
├── templates/       # ระบบจัดการเทมเพลต
└── tests/          # ชุดทดสอบ
```

### 🧪 การทดสอบ
```bash
# รันทดสอบทั้งหมด
pytest

# ทดสอบเฉพาะส่วน
pytest tests/test_processor.py
```

### 📚 API Documentation
- [REST API](docs/api.md)
- [Python SDK](docs/sdk.md)
- [OpenAPI Spec](docs/openapi.json)

## 🎓 สำหรับนักศึกษา

### 📖 แหล่งเรียนรู้
- [คู่มือเริ่มต้น](docs/getting_started.md)
- [บทเรียน & ตัวอย่าง](docs/tutorials/)
- [คำถามที่พบบ่อย](docs/faq.md)

### 🛠️ การพัฒนาต่อยอด
1. Fork โปรเจค
2. สร้าง Feature Branch
3. พัฒนาฟีเจอร์ใหม่
4. ส่ง Pull Request

## 🤝 การสนับสนุน

### 📞 ติดต่อเรา
- [Discord Community](https://discord.gg/excelprocessor)
- [GitHub Discussions](https://github.com/ZanKinZuiTH/excel-processor/discussions)
- Email: support@example.com
- Line: @excelprocessor

### 🐛 รายงานปัญหา
- [GitHub Issues](https://github.com/ZanKinZuiTH/excel-processor/issues)
- [Bug Report Template](docs/bug_report_template.md)

## 📝 License

โครงการนี้อยู่ภายใต้ MIT License - ดูรายละเอียดใน [LICENSE](LICENSE)

---

<p align="center">
⭐ หากโครงการนี้เป็นประโยชน์ สามารถให้ดาวโปรเจคได้ ⭐
</p>

<p align="center">
พัฒนาด้วย ❤️ โดย <a href="https://github.com/ZanKinZuiTH">ZanKinZuiTH</a>
</p> 