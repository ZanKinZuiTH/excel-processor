# 🌐 คู่มือการติดตั้งและเชื่อมต่อกับเซิร์ฟเวอร์

## 📑 สารบัญ
1. [การเตรียมความพร้อม](#การเตรียมความพร้อม)
2. [การติดตั้งบน Windows Server](#การติดตั้งบน-windows-server)
3. [การติดตั้งบน Linux Server](#การติดตั้งบน-linux-server)
4. [การติดตั้งผ่าน Docker](#การติดตั้งผ่าน-docker)
5. [การติดตั้งบน Kubernetes](#การติดตั้งบน-kubernetes)
6. [การตั้งค่าความปลอดภัย](#การตั้งค่าความปลอดภัย)
7. [การ Monitor ระบบ](#การ-monitor-ระบบ)
8. [การแก้ไขปัญหา](#การแก้ไขปัญหา)

## 🚀 การเตรียมความพร้อม

### ความต้องการของระบบ
- CPU: 2 cores ขึ้นไป
- RAM: 4GB ขึ้นไป
- Disk: 20GB ขึ้นไป
- OS: Windows Server 2019+, Ubuntu 20.04+, CentOS 8+
- Network: Static IP, Port 80/443 เปิด

### Software ที่จำเป็น
```bash
# Python 3.8+
python --version

# Git
git --version

# Docker (ถ้าใช้)
docker --version

# Kubernetes (ถ้าใช้)
kubectl version
```

### การเตรียม SSL Certificate
1. สร้าง Self-signed Certificate (สำหรับทดสอบ)
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout private.key -out certificate.crt
```

2. ใช้ Let's Encrypt (แนะนำสำหรับ Production)
```bash
# ติดตั้ง Certbot
sudo apt-get install certbot

# ขอ Certificate
sudo certbot certonly --standalone -d yourdomain.com
```

## 💻 การติดตั้งบน Windows Server

### 1. ติดตั้ง Python และ Dependencies
```powershell
# ดาวน์โหลด Python
Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe" -OutFile "python-3.9.0.exe"

# ติดตั้ง Python (Silent Install)
./python-3.9.0.exe /quiet InstallAllUsers=1 PrependPath=1

# ติดตั้ง Dependencies
pip install -r requirements.txt
```

### 2. ตั้งค่า Windows Service
```powershell
# สร้าง Service
New-Service -Name "ExcelProcessor" -BinaryPathName "C:\Python39\python.exe C:\Apps\excel-processor\app.py"

# เริ่มต้น Service
Start-Service -Name "ExcelProcessor"

# ตั้งค่าให้เริ่มต้นอัตโนมัติ
Set-Service -Name "ExcelProcessor" -StartupType Automatic
```

### 3. ตั้งค่า IIS
```powershell
# ติดตั้ง IIS
Install-WindowsFeature -Name Web-Server -IncludeManagementTools

# ตั้งค่า Reverse Proxy
# (ดูรายละเอียดในส่วน IIS Configuration)
```

## 🐧 การติดตั้งบน Linux Server

### 1. Update และติดตั้ง Dependencies
```bash
# Update ระบบ
sudo apt update && sudo apt upgrade -y

# ติดตั้ง Dependencies
sudo apt install -y python3-pip python3-venv nginx

# สร้าง Virtual Environment
python3 -m venv venv
source venv/bin/activate

# ติดตั้ง Python packages
pip install -r requirements.txt
```

### 2. ตั้งค่า Systemd Service
```bash
# สร้างไฟล์ Service
sudo nano /etc/systemd/system/excel-processor.service

[Unit]
Description=Excel Processor Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/excel-processor
Environment="PATH=/opt/excel-processor/venv/bin"
ExecStart=/opt/excel-processor/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target

# Reload และเริ่มต้น Service
sudo systemctl daemon-reload
sudo systemctl start excel-processor
sudo systemctl enable excel-processor
```

### 3. ตั้งค่า Nginx
```bash
# สร้าง Nginx config
sudo nano /etc/nginx/sites-available/excel-processor

server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/excel-processor /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 🐳 การติดตั้งผ่าน Docker

### 1. สร้าง Docker Image
```bash
# Build image
docker build -t excel-processor:latest .

# Run container
docker run -d \
  --name excel-processor \
  -p 8000:8000 \
  -v /data:/app/data \
  excel-processor:latest
```

### 2. ใช้ Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      - DATABASE_URL=sqlite:///data/excel_data.db
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - app
```

### 3. Deploy ด้วย Docker Swarm
```bash
# Initialize Swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml excel-processor
```

## ☸️ การติดตั้งบน Kubernetes

### 1. สร้าง Kubernetes Manifests
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: excel-processor
spec:
  replicas: 3
  selector:
    matchLabels:
      app: excel-processor
  template:
    metadata:
      labels:
        app: excel-processor
    spec:
      containers:
      - name: excel-processor
        image: excel-processor:latest
        ports:
        - containerPort: 8000
        volumeMounts:
        - name: data
          mountPath: /app/data
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: excel-processor-pvc

---
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: excel-processor
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8000
  selector:
    app: excel-processor
```

### 2. Deploy บน Kubernetes
```bash
# Apply manifests
kubectl apply -f k8s/

# ตรวจสอบสถานะ
kubectl get pods
kubectl get services
```

## 🔒 การตั้งค่าความปลอดภัย

### 1. Firewall Rules
```bash
# Windows (PowerShell)
New-NetFirewallRule -DisplayName "Excel Processor" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 80,443

# Linux (UFW)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

### 2. SSL/TLS Configuration
```nginx
# Nginx SSL config
server {
    listen 443 ssl;
    server_name your_domain.com;

    ssl_certificate /etc/letsencrypt/live/your_domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your_domain.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000" always;
}
```

## 📊 การ Monitor ระบบ

### 1. ตั้งค่า Prometheus
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'excel-processor'
    static_configs:
      - targets: ['localhost:8000']
```

### 2. ตั้งค่า Grafana Dashboard
```bash
# ติดตั้ง Grafana
docker run -d \
  --name=grafana \
  -p 3000:3000 \
  grafana/grafana
```

### 3. ตั้งค่า Alert Manager
```yaml
# alertmanager.yml
route:
  group_by: ['alertname']
  receiver: 'email-notifications'

receivers:
- name: 'email-notifications'
  email_configs:
  - to: 'admin@your_domain.com'
```

## ❗ การแก้ไขปัญหา

### 1. ตรวจสอบ Logs
```bash
# Windows
Get-EventLog -LogName Application -Source "Excel Processor"

# Linux
journalctl -u excel-processor

# Docker
docker logs excel-processor

# Kubernetes
kubectl logs deployment/excel-processor
```

### 2. ปัญหาที่พบบ่อย
1. **Connection Refused**
   - ตรวจสอบ Firewall
   - ตรวจสอบ Service Status
   - ตรวจสอบ Port Binding

2. **SSL Certificate Issues**
   - ตรวจสอบวันหมดอายุ
   - ตรวจสอบ Path ของ Certificate
   - ตรวจสอบ Permission

3. **Performance Issues**
   - ตรวจสอบ Resource Usage
   - ตรวจสอบ Database Connection
   - พิจารณาเพิ่ม Cache

### 3. Backup และ Recovery
```bash
# Backup Database
pg_dump -U username dbname > backup.sql

# Backup Configuration
tar -czf config_backup.tar.gz /etc/excel-processor/

# Recovery
pg_restore -U username -d dbname backup.sql
```

## 📚 แหล่งข้อมูลเพิ่มเติม

### Documentation
- [Python Documentation](https://docs.python.org/)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Nginx Documentation](https://nginx.org/en/docs/)

### Community
- [GitHub Issues](https://github.com/your-repo/issues)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/excel-processor)
- [Discord Community](https://discord.gg/excel-processor)

### Video Tutorials
1. [การติดตั้งบน Windows Server](https://youtube.com/...)
2. [การติดตั้งบน Linux](https://youtube.com/...)
3. [การใช้งาน Docker](https://youtube.com/...)
4. [การ Deploy บน Kubernetes](https://youtube.com/...)

## 🎓 สำหรับนักศึกษา

### การเรียนรู้เพิ่มเติม
1. ศึกษาการทำงานของ Web Server
2. เรียนรู้เรื่อง Container และ Orchestration
3. ทำความเข้าใจเรื่อง Security Best Practices
4. ฝึกการ Monitor และ Debug ระบบ

### แบบฝึกหัด
1. ติดตั้งระบบบน VM ในเครื่องตัวเอง
2. ทดลองใช้ Docker Compose
3. สร้าง Monitoring Dashboard
4. ทดสอบ Backup และ Recovery

### Tips สำหรับการสอบ
1. เข้าใจขั้นตอนการ Deploy ทั้งหมด
2. รู้วิธีแก้ปัญหาพื้นฐาน
3. สามารถอธิบายความแตกต่างของแต่ละวิธีการ Deploy
4. เข้าใจเรื่องความปลอดภัยและการ Monitor