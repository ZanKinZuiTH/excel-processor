# 📘 คู่มือการใช้งานสำหรับนักศึกษา

## 🚀 การเริ่มต้นใช้งาน

### 1. การเข้าสู่ระบบ
1. เปิดโปรแกรมผ่าน URL: `http://localhost:8501`
2. กรอกข้อมูลเข้าสู่ระบบ:
   - รหัสนักศึกษา
   - รหัสผ่าน
3. เลือกบทบาท (Role):
   - นักศึกษา
   - ผู้ช่วยสอน
   - อาจารย์

### 2. หน้าจอหลัก
![หน้าจอหลัก](images/main_screen.png)

#### เมนูด้านซ้าย
- 📊 แดชบอร์ด
- 📁 จัดการเทมเพลต
- 🔍 ประมวลผลข้อมูล
- 📋 รายงาน
- ⚙️ ตั้งค่า

## 📝 การใช้งานพื้นฐาน

### 1. การจัดการเทมเพลต
```python
# ตัวอย่างการสร้างเทมเพลตใหม่
from template_manager import TemplateManager

# สร้าง instance
manager = TemplateManager()

# สร้างเทมเพลตใหม่
template = manager.create_template(
    name="ใบแจ้งหนี้",
    fields=["รหัส", "รายการ", "จำนวน", "ราคา"]
)
```

### 2. การประมวลผลข้อมูล
```python
# ตัวอย่างการประมวลผลไฟล์ Excel
from excel_processor import ExcelProcessor

# สร้าง instance
processor = ExcelProcessor("data.xlsx")

# ประมวลผล
result = processor.process_file()
print(f"ผลลัพธ์: {result}")
```

### 3. การสร้างรายงาน
```python
# ตัวอย่างการสร้างรายงาน
import pandas as pd
import matplotlib.pyplot as plt

# สร้างกราฟ
data = pd.read_excel("data.xlsx")
plt.figure(figsize=(10, 6))
data.plot(kind='bar')
plt.title("รายงานยอดขาย")
plt.show()
```

## 🔍 การใช้งานขั้นสูง

### 1. การใช้งาน AI
```python
# ตัวอย่างการวิเคราะห์ด้วย AI
from ai_module import AIAnalyzer

analyzer = AIAnalyzer()
insights = analyzer.analyze("data.xlsx")
print("ผลการวิเคราะห์:", insights)
```

### 2. การจัดการ DICOM
```python
# ตัวอย่างการใช้งาน DICOM
from dicom_module import DicomViewer

viewer = DicomViewer()
viewer.view_image("image.dcm")
```

### 3. การติดตามประสิทธิภาพ
```python
# ตัวอย่างการติดตามประสิทธิภาพ
from monitoring import SystemMonitor

monitor = SystemMonitor()
stats = monitor.get_system_metrics()
print("สถานะระบบ:", stats)
```

## 💡 เคล็ดลับการใช้งาน

### 1. การจัดการข้อมูล
- ตรวจสอบข้อมูลก่อนประมวลผล
- สำรองข้อมูลเสมอ
- ใช้เทมเพลตที่เหมาะสม

### 2. การแก้ไขปัญหา
- ตรวจสอบ error log
- ใช้ระบบติดตาม
- ปรึกษาอาจารย์เมื่อติดปัญหา

### 3. การพัฒนาต่อยอด
- ศึกษาโค้ดตัวอย่าง
- ทดลองปรับแต่งพารามิเตอร์
- สร้างฟีเจอร์ใหม่

## 🎯 แบบฝึกหัดท้ายบท

### แบบฝึกหัดที่ 1: การจัดการเทมเพลต
1. สร้างเทมเพลตใบสั่งซื้อ
2. เพิ่มการคำนวณอัตโนมัติ
3. ทดสอบการใช้งาน

### แบบฝึกหัดที่ 2: การวิเคราะห์ข้อมูล
1. นำเข้าข้อมูลตัวอย่าง
2. วิเคราะห์ด้วย AI
3. สร้างรายงานสรุป

### แบบฝึกหัดที่ 3: การพัฒนาฟีเจอร์
1. เพิ่มฟีเจอร์ใหม่
2. เขียนเอกสาร
3. นำเสนอผลงาน

## 📞 การขอความช่วยเหลือ

### ช่องทางติดต่อ
- 📧 Email: support@brxg.co.th
- 💬 Line: @brxgdev
- 📱 โทร: 02-XXX-XXXX

### เวลาให้คำปรึกษา
- จันทร์-ศุกร์: 9:00-16:00
- เสาร์: 9:00-12:00

### ขั้นตอนการขอความช่วยเหลือ
1. ตรวจสอบเอกสาร
2. ค้นหาใน FAQ
3. ติดต่อผู้สอน 