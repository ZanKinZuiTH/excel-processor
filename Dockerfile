FROM python:3.9-slim

WORKDIR /app

# ติดตั้ง dependencies สำหรับ pywin32
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# คัดลอกไฟล์ที่จำเป็น
COPY requirements.txt .
COPY setup.py .
COPY README.md .
COPY main.py .
COPY api.py .
COPY printer.py .
COPY demo/ demo/

# ติดตั้ง dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e .

# สร้างโฟลเดอร์สำหรับข้อมูล
RUN mkdir -p data templates

# เปิดพอร์ต
EXPOSE 8000

# รัน API server
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"] 