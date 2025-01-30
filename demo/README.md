# 🎮 ตัวอย่างการใช้งานระบบ

## 📁 โครงสร้างโฟลเดอร์

```
demo/
├── demo.py              # ไฟล์สาธิตการใช้งาน
├── invoice_template.xlsx # เทมเพลตใบแจ้งหนี้
├── customer_data.xlsx   # ข้อมูลลูกค้าตัวอย่าง
└── README.md           # เอกสารอธิบาย
```

## 🚀 การรันตัวอย่าง

1. เตรียมไฟล์ `.env`:
```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///./demo.db
```

2. รันตัวอย่าง:
```bash
python demo/demo.py
```

## 📝 ตัวอย่างที่มีให้

### 1. การจัดการเทมเพลต
```python
from template_manager import TemplateManager

# สร้าง instance
manager = TemplateManager()

# อัพโหลดเทมเพลต
template_id = manager.upload_template(
    file_path="invoice_template.xlsx",
    name="ใบแจ้งหนี้",
    description="เทมเพลตสำหรับออกใบแจ้งหนี้"
)

# ใช้งานเทมเพลต
result = manager.use_template(template_id, {
    "customer_name": "บริษัท ตัวอย่าง จำกัด",
    "amount": 1000.00,
    "date": "2024-01-30"
})
```

### 2. การประมวลผลไฟล์
```python
from processor import ExcelProcessor

# สร้าง instance
processor = ExcelProcessor("customer_data.xlsx")

# ประมวลผลไฟล์
result = processor.process_file()

# บันทึกผลลัพธ์
processor.save_result("output.xlsx")
```

### 3. การพิมพ์เอกสาร
```python
from printer import PrintManager

# สร้าง instance
printer = PrintManager()

# พิมพ์เอกสาร
printer.print_file(
    file_path="output.xlsx",
    printer_name="HP LaserJet"
)
```

## 🔒 ตัวอย่างการใช้ระบบความปลอดภัย

```python
from security import SecurityManager

# สร้าง instance
security = SecurityManager()

# สร้าง token
token = security.create_access_token({
    "username": "demo_user",
    "role": "demo"
})

# ตรวจสอบไฟล์
security.validate_file("customer_data.xlsx")
```

## ⚙️ ตัวอย่างการใช้การตั้งค่า

```python
from config import get_settings

# ดึงการตั้งค่า
settings = get_settings()

# ใช้งานการตั้งค่า
print(f"แอปพลิเคชัน: {settings.APP_NAME}")
print(f"โหมดดีบัก: {settings.DEBUG}")
```

## 🧪 ตัวอย่างการทดสอบ

```python
import pytest
from processor import ExcelProcessor

def test_process_file():
    processor = ExcelProcessor("customer_data.xlsx")
    result = processor.process_file()
    assert result["status"] == "success"
```

## 📊 ตัวอย่างผลลัพธ์

1. ไฟล์ที่ประมวลผลแล้ว:
   - `output/processed_invoice.xlsx`
   - `output/customer_summary.xlsx`

2. รายงานสรุป:
   - `reports/processing_report.pdf`
   - `reports/error_log.txt`

## ⚠️ ข้อควรระวัง

1. **การใช้ไฟล์ตัวอย่าง**
   - ใช้เฉพาะเพื่อการทดสอบ
   - ห้ามใช้ข้อมูลจริง
   - สำรองข้อมูลก่อนทดสอบ

2. **การรันตัวอย่าง**
   - ตรวจสอบ dependencies
   - ตั้งค่า .env ให้ถูกต้อง
   - ตรวจสอบสิทธิ์การเข้าถึง

## 🔍 การแก้ไขปัญหา

1. **ไฟล์ไม่ถูกต้อง**
   ```python
   # ตรวจสอบไฟล์
   security.validate_file("file.xlsx")
   ```

2. **Token หมดอายุ**
   ```python
   # สร้าง token ใหม่
   new_token = security.create_access_token(data)
   ```

3. **การเชื่อมต่อล้มเหลว**
   ```python
   # ตรวจสอบการตั้งค่า
   print(settings.DATABASE_URL)
   ``` 