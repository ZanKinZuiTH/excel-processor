# 🚀 Excel Processor

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)]()
[![Discord](https://img.shields.io/badge/discord-join%20chat-7289da)]()

> ระบบประมวลผล Excel อัจฉริยะ พร้อมระบบ AI วิเคราะห์และจัดการเทมเพลตอัตโนมัติ

[🇹🇭 ภาษาไทย](README.md) | [🇺🇸 English](README_EN.md) | [🎮 Demo](README_DEMO.md)

<div align="center">
  <img src="docs/images/demo.gif" alt="Excel Processor Demo" width="600">
</div>

## 🔍 Quick Links
| 📚 [เอกสาร](#-เอกสาร) | 🛠️ [การติดตั้ง](#️-การติดตั้ง) | 📖 [การใช้งาน](#-การใช้งาน) | 🧪 [การทดสอบ](docs/testing_guide.md) | 🤝 [การสนับสนุน](#-การสนับสนุน) |
|---|---|---|---|---|

## ✨ คุณสมบัติเด่น

<table>
<tr>
<td width="50%">

### 🎯 การจัดการเทมเพลต
- ✅ สร้างและแก้ไขเทมเพลตอัตโนมัติ
- ✅ แชร์เทมเพลตระหว่างผู้ใช้
- ✅ ควบคุมเวอร์ชันของเทมเพลต
- ✅ แนะนำเทมเพลตที่เหมาะสมด้วย AI

### 📊 การประมวลผลข้อมูล
- ✅ วิเคราะห์โครงสร้างข้อมูลอัตโนมัติ
- ✅ ตรวจจับและแก้ไขข้อผิดพลาด
- ✅ แปลงรูปแบบข้อมูลอัตโนมัติ
- ✅ รองรับการประมวลผลแบบกลุ่ม

</td>
<td width="50%">

### 🤖 ระบบ AI อัจฉริยะ
- ✅ วิเคราะห์แนวโน้มด้วย Prophet
- ✅ คาดการณ์ข้อมูลด้วย LSTM
- ✅ คำนวณความสำคัญของ Features
- ✅ เรียนรู้และปรับปรุงอัตโนมัติ

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

### �� ระบบความปลอดภัย
- ✅ รองรับ JWT Authentication
- ✅ ควบคุมสิทธิ์การเข้าถึง
- ✅ เข้ารหัสข้อมูลอัตโนมัติ
- ✅ ป้องกันการโจมตี

### 📈 ระบบติดตาม
- ติดตามการใช้งานทรัพยากร
- วิเคราะห์ประสิทธิภาพ
- แจ้งเตือนเมื่อเกินเกณฑ์
- สร้างรายงานอัตโนมัติ

</td>
</tr>
</table>

## 🛠️ การติดตั้ง

<details>
<summary>1. Clone โปรเจค</summary>

```bash
git clone https://github.com/yourusername/excel-processor.git
cd excel-processor
```
</details>

<details>
<summary>2. สร้าง Virtual Environment</summary>

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
</details>

<details>
<summary>3. ติดตั้ง Dependencies</summary>

```bash
pip install -r requirements.txt
```
</details>

<details>
<summary>4. ตั้งค่าระบบ</summary>

```bash
python cli.py setup
```
</details>

## 📖 การใช้งาน

<details>
<summary>🖥️ Web Interface</summary>

1. เริ่มต้นระบบ:
```bash
python cli.py start
```
2. เปิดเบราว์เซอร์ไปที่ `http://localhost:8501`
</details>

<details>
<summary>💻 Command Line</summary>

```bash
# ประมวลผลไฟล์
python cli.py process input.xlsx

# สร้างเทมเพลต
python cli.py template create

# วิเคราะห์ด้วย AI
python cli.py analyze data.xlsx
```
</details>

## 🔧 การตั้งค่า

<details>
<summary>⚙️ การตั้งค่าพื้นฐาน</summary>

```env
APP_NAME=ระบบจัดการเทมเพลต Excel
APP_VERSION=1.0.0
DEBUG=False
```
</details>

<details>
<summary>🔐 การตั้งค่าความปลอดภัย</summary>

```env
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
</details>

<details>
<summary>🗄️ การตั้งค่าฐานข้อมูล</summary>

```env
DATABASE_URL=sqlite:///./excel_data.db
```
</details>

## 📚 เอกสาร

| เอกสาร | คำอธิบาย |
|---|---|
| [📘 คู่มือการใช้งาน](docs/user_guide.md) | แนะนำการใช้งานระบบทั้งหมด |
| [🔧 คู่มือการติดตั้ง](docs/server_setup.md) | ขั้นตอนการติดตั้งและตั้งค่าระบบ |
| [📊 คู่มือการนำเสนอ](docs/presentation_guide.md) | แนวทางการนำเสนอระบบ |
| [🧪 คู่มือการทดสอบ](docs/testing_guide.md) | การทดสอบระบบและ API |

## 👥 ผู้พัฒนา

<table>
<tr>
<td align="center">
<a href="https://github.com/ZanKinZuiTH">
<img src="https://avatars.githubusercontent.com/u/YOUR_ID?v=4" width="100px;" alt=""/>
<br />
<sub><b>ZanKinZuiTH</b></sub>
</a>
</td>
</tr>
</table>

## 📄 License

โปรเจคนี้อยู่ภายใต้ MIT License - ดูรายละเอียดใน [LICENSE](LICENSE)

## 📫 การสนับสนุน

<table>
<tr>
<td>

### 🐛 รายงานปัญหา
- [GitHub Issues](https://github.com/ZanKinZuiTH/excel-processor/issues)

### 📧 ติดต่อ
- Email: support@brxg.co.th
- Line Official: @brxgdev

### 💬 ชุมชน
- [Discord Server](https://discord.gg/your-server)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/excel-processor)

</td>
</tr>
</table>

---
⌨️ ด้วย ❤️ โดย [ZanKinZuiTH](https://github.com/ZanKinZuiTH) 