# 🧪 คู่มือการทดสอบสำหรับนักศึกษา

## 📝 บทนำ

การทดสอบเป็นส่วนสำคัญในการพัฒนาซอฟต์แวร์ คู่มือนี้จะแนะนำวิธีการทดสอบระบบอย่างมีประสิทธิภาพ

## 🎯 เป้าหมายการเรียนรู้
1. เข้าใจความสำคัญของการทดสอบ
2. รู้จักประเภทของการทดสอบ
3. สามารถเขียนและรันการทดสอบได้
4. วิเคราะห์ผลการทดสอบได้

## 🔧 การติดตั้งเครื่องมือ

```bash
# ติดตั้ง dependencies สำหรับการทดสอบ
pip install -r requirements-dev.txt

# ตรวจสอบการติดตั้ง
pytest --version
```

## 📚 ประเภทของการทดสอบ

### 1. Unit Testing
```python
# ตัวอย่าง Unit Test
def test_extract_customer_info(processor):
    result = processor.extract_customer_info()
    assert "customer_name" in result
    assert "customer_id" in result
    assert result["status"] == "success"
```

### 2. Integration Testing
```python
# ตัวอย่าง Integration Test
def test_process_and_save(processor, db):
    # ทดสอบการทำงานร่วมกันของหลายๆ ส่วน
    data = processor.process_file()
    result = db.save_data(data)
    assert result["saved"] == True
```

### 3. Performance Testing
```python
# ตัวอย่าง Performance Test
@pytest.mark.benchmark
def test_large_file_processing(benchmark):
    def process():
        processor = ExcelProcessor("large_file.xlsx")
        return processor.process_file()
    
    result = benchmark(process)
    assert result["processing_time"] < 5.0  # ต้องเร็วกว่า 5 วินาที
```

## 🏃 การรันการทดสอบ

### รันทดสอบทั้งหมด
```bash
pytest
```

### รันเฉพาะบางการทดสอบ
```bash
# รันเฉพาะ unit tests
pytest tests/test_processor.py

# รันเฉพาะ performance tests
pytest -m benchmark

# รันพร้อมดู coverage
pytest --cov=excel_processor
```

## ✍️ การเขียนการทดสอบ

### 1. โครงสร้างพื้นฐาน
```python
import pytest
from excel_processor import ExcelProcessor

def test_basic_functionality():
    # Arrange
    processor = ExcelProcessor("test.xlsx")
    
    # Act
    result = processor.process_file()
    
    # Assert
    assert result["status"] == "success"
```

### 2. การใช้ Fixtures
```python
@pytest.fixture
def sample_data():
    return {
        "name": "ทดสอบ",
        "age": 20,
        "score": 85
    }

def test_with_fixture(sample_data):
    assert sample_data["score"] >= 0
```

### 3. การจัดการ Exceptions
```python
def test_invalid_file():
    with pytest.raises(FileNotFoundError):
        processor = ExcelProcessor("not_exists.xlsx")
        processor.process_file()
```

## 🔍 การวิเคราะห์ผลการทดสอบ

### 1. การอ่าน Test Report
```bash
pytest --html=report.html
```

### 2. การวิเคราะห์ Coverage
```bash
pytest --cov=excel_processor --cov-report=html
```

### 3. การแก้ไขการทดสอบที่ล้มเหลว
1. อ่านข้อความ error ให้เข้าใจ
2. ตรวจสอบ input และ expected output
3. ใช้ debugger ช่วยหาปัญหา

## 📝 แบบฝึกหัด

### แบบฝึกหัดที่ 1: Unit Testing
1. เขียน test case สำหรับ TemplateManager
2. ทดสอบการสร้าง/แก้ไข/ลบเทมเพลต
3. ทดสอบการจัดการข้อผิดพลาด

### แบบฝึกหัดที่ 2: Integration Testing
1. ทดสอบการทำงานร่วมกับฐานข้อมูล
2. ทดสอบการเชื่อมต่อกับ API
3. ทดสอบการทำงานของระบบทั้งหมด

### แบบฝึกหัดที่ 3: Performance Testing
1. ทดสอบประสิทธิภาพกับไฟล์ขนาดใหญ่
2. วัดการใช้ memory
3. ทดสอบการทำงานพร้อมกันหลายๆ user

## 💡 เคล็ดลับการทดสอบ

### 1. การเขียน Test Cases ที่ดี
- ทดสอบทั้งกรณีปกติและผิดพลาด
- แยก test cases ให้ชัดเจน
- ตั้งชื่อ test function ให้สื่อความหมาย

### 2. การจัดการ Test Data
- ใช้ fixtures สำหรับข้อมูลที่ใช้บ่อย
- แยกไฟล์ test data
- ทำความสะอาดข้อมูลหลังการทดสอบ

### 3. การ Debug
- ใช้ pytest -v สำหรับรายละเอียดเพิ่มเติม
- ใช้ pdb สำหรับ debugging
- เช็ค log files

## 🏆 เกณฑ์การประเมิน

### 1. ความครอบคลุมของการทดสอบ (40%)
- Unit tests ครบทุก function
- Integration tests ครบทุกระบบ
- Edge cases และ error handling

### 2. คุณภาพของ Test Cases (30%)
- ความชัดเจนของการทดสอบ
- การจัดการ test data
- การใช้ fixtures และ helpers

### 3. Performance Testing (30%)
- การทดสอบประสิทธิภาพ
- การวัดและวิเคราะห์ผล
- การปรับปรุงประสิทธิภาพ

## 📞 การขอความช่วยเหลือ

### ช่องทางติดต่อ
- Email: support@brxg.co.th
- Line: @brxgdev
- เวลาทำการ: จันทร์-ศุกร์ 9:00-16:00

### ขั้นตอนการขอความช่วยเหลือ
1. ตรวจสอบ documentation
2. ค้นหาใน test examples
3. ติดต่ออาจารย์ผู้สอน 