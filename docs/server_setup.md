# 🖥️ คู่มือการติดตั้งเซิร์ฟเวอร์

## 📋 สารบัญ
1. [ความต้องการของระบบ](#ความต้องการของระบบ)
2. [การติดตั้งระบบ](#การติดตั้งระบบ)
3. [การตั้งค่าระบบ](#การตั้งค่าระบบ)
4. [การทดสอบระบบ](#การทดสอบระบบ)
5. [การบำรุงรักษา](#การบำรุงรักษา)

## 💻 ความต้องการของระบบ

### ฮาร์ดแวร์ขั้นต่ำ
- CPU: 4 cores
- RAM: 8GB
- Storage: 100GB SSD
- Network: 100Mbps

### ซอฟต์แวร์ที่จำเป็น
- OS: Ubuntu 20.04 LTS หรือสูงกว่า
- Python 3.8 หรือสูงกว่า
- PostgreSQL 12 หรือสูงกว่า
- Redis 6 หรือสูงกว่า
- NGINX

## 🚀 การติดตั้งระบบ

### 1. ติดตั้ง Dependencies
```bash
# อัพเดทระบบ
sudo apt update
sudo apt upgrade -y

# ติดตั้ง Python และเครื่องมือที่จำเป็น
sudo apt install python3.8 python3.8-venv python3-pip

# ติดตั้ง PostgreSQL
sudo apt install postgresql postgresql-contrib

# ติดตั้ง Redis
sudo apt install redis-server

# ติดตั้ง NGINX
sudo apt install nginx
```

### 2. ตั้งค่าฐานข้อมูล
```bash
# สร้างฐานข้อมูลและผู้ใช้
sudo -u postgres psql
CREATE DATABASE exceldb;
CREATE USER exceluser WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE exceldb TO exceluser;
\q
```

### 3. ติดตั้งแอปพลิเคชัน
```bash
# Clone repository
git clone https://github.com/yourusername/excel-processor.git
cd excel-processor

# สร้าง virtual environment
python3 -m venv venv
source venv/bin/activate

# ติดตั้ง dependencies
pip install -r requirements.txt
```

## ⚙️ การตั้งค่าระบบ

### 1. ตั้งค่าสภาพแวดล้อม
```bash
# สร้างไฟล์ .env
cat > .env << EOL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=exceldb
DB_USER=exceluser
DB_PASSWORD=your_password
REDIS_HOST=localhost
REDIS_PORT=6379
SECRET_KEY=your_secret_key
EOL
```

### 2. ตั้งค่า NGINX
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /path/to/your/static/;
    }
}
```

### 3. ตั้งค่า Systemd Service
```bash
# สร้าง service file
sudo nano /etc/systemd/system/excel-processor.service

[Unit]
Description=Excel Processor Service
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/path/to/excel-processor
Environment="PATH=/path/to/excel-processor/venv/bin"
ExecStart=/path/to/excel-processor/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

## 🧪 การทดสอบระบบ

### 1. ทดสอบการเชื่อมต่อ
```bash
# ทดสอบ PostgreSQL
psql -h localhost -U exceluser -d exceldb

# ทดสอบ Redis
redis-cli ping

# ทดสอบ API
curl http://localhost:8000/health
```

### 2. ทดสอบการทำงาน
```bash
# รัน unit tests
python -m pytest tests/

# ทดสอบ load testing
locust -f tests/locustfile.py
```

## 🔧 การบำรุงรักษา

### การสำรองข้อมูล
```bash
# สำรองฐานข้อมูล
pg_dump -U exceluser exceldb > backup.sql

# สำรอง Redis
redis-cli save
```

### การอัพเดทระบบ
```bash
# อัพเดทโค้ด
git pull origin main

# อัพเดท dependencies
pip install -r requirements.txt --upgrade

# รีสตาร์ทบริการ
sudo systemctl restart excel-processor
```

### การตรวจสอบ Log
```bash
# ดู application logs
tail -f logs/app.log

# ดู NGINX logs
tail -f /var/log/nginx/access.log
```

## 🚨 การแก้ไขปัญหา

### ปัญหาทั่วไป
1. **ไม่สามารถเชื่อมต่อฐานข้อมูล**
   - ตรวจสอบ PostgreSQL service
   - ตรวจสอบ credentials
   - ตรวจสอบ firewall

2. **ระบบทำงานช้า**
   - ตรวจสอบการใช้ RAM
   - ตรวจสอบ CPU usage
   - ตรวจสอบ disk I/O

3. **Error 500**
   - ตรวจสอบ application logs
   - ตรวจสอบ memory usage
   - รีสตาร์ทบริการ

### คำสั่งที่ใช้บ่อย
```bash
# ตรวจสอบสถานะบริการ
sudo systemctl status excel-processor

# ดูการใช้ทรัพยากร
htop

# ตรวจสอบพื้นที่ดิสก์
df -h

# ล้าง cache
redis-cli flushall
```

## 📞 การติดต่อสนับสนุน

### ช่องทางติดต่อ
- Email: support@example.com
- โทร: 02-xxx-xxxx
- Line: @excelprocessor
- Discord: discord.gg/excelprocessor

### เอกสารอ้างอิง
- [Official Documentation](https://docs.example.com)
- [API Reference](https://api.example.com)
- [GitHub Repository](https://github.com/yourusername/excel-processor)