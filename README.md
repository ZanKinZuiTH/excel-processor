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

### 🎯 การจัดการเทมเพลต
- สร้างและแก้ไขเทมเพลตอัตโนมัติ
- แชร์เทมเพลตระหว่างผู้ใช้
- ควบคุมเวอร์ชันของเทมเพลต
- แนะนำเทมเพลตที่เหมาะสมด้วย AI

### 📊 การประมวลผลข้อมูล
- วิเคราะห์โครงสร้างข้อมูลอัตโนมัติ
- ตรวจจับและแก้ไขข้อผิดพลาด
- แปลงรูปแบบข้อมูลอัตโนมัติ
- รองรับการประมวลผลแบบกลุ่ม

### 🤖 ระบบ AI อัจฉริยะ
- วิเคราะห์แนวโน้มด้วย Prophet
- คาดการณ์ข้อมูลด้วย LSTM
- คำนวณความสำคัญของ Features
- เรียนรู้และปรับปรุงอัตโนมัติ

### 🖨️ ระบบพิมพ์เอกสาร
- จัดการคิวการพิมพ์อัตโนมัติ
- รองรับการพิมพ์แบบกลุ่ม
- เลือกเครื่องพิมพ์ได้อย่างยืดหยุ่น
- จัดรูปแบบเอกสารอัตโนมัติ

### 🌐 Web API & UI
- REST API ครบวงจร
- UI สวยงามด้วย Streamlit
- รองรับการทำงานแบบ Async
- ระบบแจ้งเตือนแบบ Real-time

### 🔒 ระบบความปลอดภัย
- รองรับ JWT Authentication
- ควบคุมสิทธิ์การเข้าถึง
- เข้ารหัสข้อมูลอัตโนมัติ
- ป้องกันการโจมตี

### 📈 ระบบติดตาม
- ติดตามการใช้งานทรัพยากร
- วิเคราะห์ประสิทธิภาพ
- แจ้งเตือนเมื่อเกินเกณฑ์
- สร้างรายงานอัตโนมัติ

## 🛠️ การติดตั้ง

1. Clone โปรเจค:
```bash
git clone https://github.com/yourusername/excel-processor.git
cd excel-processor
```

2. สร้าง Virtual Environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. ติดตั้ง Dependencies:
```bash
pip install -r requirements.txt
```

4. ตั้งค่าระบบ:
```bash
python cli.py setup
```

## 📖 การใช้งาน

### 🖥️ Web Interface
1. เริ่มต้นระบบ:
```bash
python cli.py start
```
2. เปิดเบราว์เซอร์ไปที่ `http://localhost:8501`

### 💻 Command Line
```bash
# ประมวลผลไฟล์
python cli.py process input.xlsx

# สร้างเทมเพลต
python cli.py template create

# วิเคราะห์ด้วย AI
python cli.py analyze data.xlsx
```

## 🔧 การตั้งค่า

### ⚙️ การตั้งค่าพื้นฐาน
```env
APP_NAME=ระบบจัดการเทมเพลต Excel
APP_VERSION=1.0.0
DEBUG=False
```

### 🔐 การตั้งค่าความปลอดภัย
```env
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 🗄️ การตั้งค่าฐานข้อมูล
```env
DATABASE_URL=sqlite:///./excel_data.db
```

## 📚 เอกสาร

- [📘 คู่มือการใช้งาน](docs/user_guide.md)
- [🔧 คู่มือการติดตั้ง](docs/server_setup.md)
- [📊 คู่มือการนำเสนอ](docs/presentation_guide.md)
- [🧪 คู่มือการทดสอบ](docs/testing_guide.md)

## 👥 ผู้พัฒนา

- **ZanKinZuiTH** - [GitHub](https://github.com/ZanKinZuiTH)

## 📄 License

โปรเจคนี้อยู่ภายใต้ MIT License - ดูรายละเอียดใน [LICENSE](LICENSE)

## 📫 การสนับสนุน

หากพบปัญหาหรือต้องการความช่วยเหลือ:
- 🐛 [GitHub Issues](https://github.com/ZanKinZuiTH/excel-processor/issues)
- 📧 Email: support@brxg.co.th
- 💬 Line Official: @brxgdev

---
⌨️ ด้วย ❤️ โดย [ZanKinZuiTH](https://github.com/ZanKinZuiTH) 