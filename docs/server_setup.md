# 🖥️ คู่มือการตั้งค่าและเชื่อมต่อกับ Data Server

## 📋 สารบัญ
1. [ความต้องการของระบบ](#ความต้องการของระบบ)
2. [การติดตั้ง Database Server](#การติดตั้ง-database-server)
3. [การตั้งค่าการเชื่อมต่อ](#การตั้งค่าการเชื่อมต่อ)
4. [การสำรองข้อมูล](#การสำรองข้อมูล)
5. [คำถามที่พบบ่อย](#คำถามที่พบบ่อย)

## 💻 ความต้องการของระบบ

### Server Requirements
- CPU: 2 cores หรือมากกว่า
- RAM: 4GB หรือมากกว่า
- Storage: 50GB หรือมากกว่า
- OS: Ubuntu 20.04 LTS หรือสูงกว่า

### Software Requirements
- PostgreSQL 12 หรือสูงกว่า
- Python 3.8 หรือสูงกว่า
- nginx (สำหรับ Production)

## 🛠️ การติดตั้ง Database Server

### 1. ติดตั้ง PostgreSQL
```bash
# อัพเดทระบบ
sudo apt update
sudo apt upgrade -y

# ติดตั้ง PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# ตรวจสอบสถานะ
sudo systemctl status postgresql
```

### 2. ตั้งค่าฐานข้อมูล
```bash
# เข้าสู่ PostgreSQL
sudo -u postgres psql

# สร้างฐานข้อมูล
CREATE DATABASE excel_processor;

# สร้างผู้ใช้
CREATE USER myuser WITH PASSWORD 'mypassword';

# ให้สิทธิ์
GRANT ALL PRIVILEGES ON DATABASE excel_processor TO myuser;

# ออกจาก PostgreSQL
\q
```

### 3. เปิด Remote Access (ถ้าต้องการ)
```bash
# แก้ไขไฟล์ postgresql.conf
sudo nano /etc/postgresql/12/main/postgresql.conf
# แก้ไขบรรทัด:
# listen_addresses = '*'

# แก้ไขไฟล์ pg_hba.conf
sudo nano /etc/postgresql/12/main/pg_hba.conf
# เพิ่มบรรทัด:
# host    all             all             0.0.0.0/0               md5

# รีสตาร์ท PostgreSQL
sudo systemctl restart postgresql
```

## ⚙️ การตั้งค่าการเชื่อมต่อ

### 1. ตั้งค่าในไฟล์ .env
```bash
# สร้างไฟล์ .env
cp .env.example .env

# แก้ไขการตั้งค่า
DB_HOST=localhost
DB_PORT=5432
DB_NAME=excel_processor
DB_USER=myuser
DB_PASSWORD=mypassword
```

### 2. รูปแบบ Connection String
```python
# PostgreSQL
postgresql://myuser:mypassword@localhost:5432/excel_processor

# MySQL
mysql://myuser:mypassword@localhost:3306/excel_processor

# SQLite
sqlite:///path/to/database.db
```

### 3. ตัวอย่างการเชื่อมต่อ
```python
from excel_processor.form_manager import FormManager

# สร้าง FormManager
manager = FormManager(
    storage_path='templates',
    db_url='postgresql://myuser:mypassword@localhost:5432/excel_processor'
)

# เรียนรู้รูปแบบจาก Excel
template = manager.learn_from_excel(
    'sample.xlsx',
    'sales_report',
    'แบบฟอร์มรายงานยอดขาย'
)

# บันทึกข้อมูลลงฐานข้อมูล
df = pd.read_excel('data.xlsx')
manager.save_to_db('sales_report', df)

# ดึงข้อมูลจากฐานข้อมูล
data = manager.get_from_db('sales_report')
```

## 💾 การสำรองข้อมูล

### 1. Backup Database
```bash
# Backup
pg_dump -U myuser -d excel_processor > backup.sql

# Restore
psql -U myuser -d excel_processor < backup.sql
```

### 2. Backup Templates
```bash
# Backup
tar -czf templates_backup.tar.gz templates/

# Restore
tar -xzf templates_backup.tar.gz
```

## ❓ คำถามที่พบบ่อย

### Q: ควรเลือกใช้ Database ชนิดใด?
A: แนะนำให้ใช้:
- **PostgreSQL**: สำหรับระบบขนาดใหญ่ ต้องการความเสถียรและฟีเจอร์ขั้นสูง
- **MySQL**: สำหรับระบบขนาดกลาง ใช้งานง่าย
- **SQLite**: สำหรับระบบขนาดเล็ก ไม่ต้องติดตั้ง Server เพิ่ม

### Q: จะป้องกันการเข้าถึงฐานข้อมูลอย่างไร?
A: 
1. ใช้ไฟร์วอลล์จำกัดการเข้าถึง
2. ตั้งรหัสผ่านที่ซับซ้อน
3. อัพเดท PostgreSQL เป็นเวอร์ชันล่าสุด
4. เปิดใช้ SSL สำหรับการเชื่อมต่อ

### Q: ระบบรองรับการทำงานพร้อมกันหลายคนหรือไม่?
A: รองรับ โดย:
1. PostgreSQL จัดการ Concurrent Access ได้
2. มีระบบ Lock Table ป้องกันการแก้ไขพร้อมกัน
3. สามารถกำหนดสิทธิ์ผู้ใช้แยกกันได้

### Q: หากต้องการย้าย Server ต้องทำอย่างไร?
A:
1. Backup ข้อมูลทั้งหมด
2. ติดตั้ง PostgreSQL บน Server ใหม่
3. Restore ข้อมูล
4. อัพเดทการตั้งค่าการเชื่อมต่อ 