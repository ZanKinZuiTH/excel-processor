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

# ตั้งค่า URL Rewrite
Install-Module -Name IISAdministration
Import-Module IISAdministration

# ตั้งค่า Application Pool
New-IISAppPool -Name "ExcelProcessor"
Set-IISAppPool -Name "ExcelProcessor" -ManagedRuntimeVersion "v4.0"

# ตั้งค่า Website
New-IISWebsite -Name "ExcelProcessor" -PhysicalPath "C:\Apps\excel-processor" -BindingInformation "*:80:"
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
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /opt/excel-processor/static/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
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
  -v /templates:/app/templates \
  --restart unless-stopped \
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
      - ./templates:/app/templates
    environment:
      - DATABASE_URL=sqlite:///data/excel_data.db
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=false
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
    restart: unless-stopped
```

### 3. Deploy ด้วย Docker Swarm
```bash
# Initialize Swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml excel-processor

# Scale services
docker service scale excel-processor_app=3
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
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        volumeMounts:
        - name: data
          mountPath: /app/data
        - name: templates
          mountPath: /app/templates
        env:
        - name: DATABASE_URL
          valueFrom:
            configMapKeyRef:
              name: excel-processor-config
              key: database_url
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: excel-processor-secrets
              key: secret_key
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: excel-processor-data-pvc
      - name: templates
        persistentVolumeClaim:
          claimName: excel-processor-templates-pvc

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

---
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: excel-processor
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - excel-processor.example.com
    secretName: excel-processor-tls
  rules:
  - host: excel-processor.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: excel-processor
            port:
              number: 80
```

## 🔒 การตั้งค่าความปลอดภัย

### 1. การตั้งค่า Firewall
```bash
# Windows (PowerShell)
New-NetFirewallRule -DisplayName "Excel Processor" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 80,443

# Linux (UFW)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

### 2. การตั้งค่า SSL/TLS
```bash
# ตั้งค่า SSL ใน Nginx
server {
    listen 443 ssl http2;
    server_name your_domain.com;

    ssl_certificate /etc/nginx/ssl/certificate.crt;
    ssl_certificate_key /etc/nginx/ssl/private.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
}
```

### 3. การตั้งค่า Security Headers
```nginx
# เพิ่ม Security Headers ใน Nginx
add_header X-Frame-Options "SAMEORIGIN";
add_header X-XSS-Protection "1; mode=block";
add_header X-Content-Type-Options "nosniff";
add_header Strict-Transport-Security "max-age=31536000";
add_header Content-Security-Policy "default-src 'self'";
```

## 📊 การ Monitor ระบบ

### 1. การตั้งค่า Prometheus
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'excel-processor'
    static_configs:
      - targets: ['localhost:8000']
```

### 2. การตั้งค่า Grafana Dashboard
```bash
# ติดตั้ง Grafana
docker run -d \
  --name=grafana \
  -p 3000:3000 \
  grafana/grafana
```

### 3. การตั้งค่า Alert Manager
```yaml
# alertmanager.yml
route:
  group_by: ['alertname']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 1h
  receiver: 'email-notifications'

receivers:
- name: 'email-notifications'
  email_configs:
  - to: 'admin@example.com'
```

## 🔧 การแก้ไขปัญหา

### 1. ตรวจสอบ Logs
```bash
# Windows
Get-EventLog -LogName Application -Source "Excel Processor"

# Linux
journalctl -u excel-processor.service
```

### 2. ตรวจสอบ Performance
```bash
# ตรวจสอบการใช้งาน CPU และ Memory
top -p $(pgrep -f "excel-processor")

# ตรวจสอบ Disk Usage
df -h /opt/excel-processor
```

### 3. การ Backup และ Restore
```bash
# Backup
tar -czf backup.tar.gz /opt/excel-processor/data

# Restore
tar -xzf backup.tar.gz -C /opt/excel-processor/
```

## 📞 การติดต่อสนับสนุน

หากพบปัญหาในการติดตั้งหรือใช้งาน สามารถติดต่อได้ที่:
- 📧 Email: support@brxg.co.th
- 💬 Line: @brxgdev
- �� โทร: 02-XXX-XXXX 