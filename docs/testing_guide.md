# 🧪 คู่มือการทดสอบระบบ Excel Processor

## 📋 สารบัญ
1. [การเตรียมสภาพแวดล้อม](#การเตรียมสภาพแวดล้อม)
2. [โครงสร้างการทดสอบ](#โครงสร้างการทดสอบ)
3. [การรันทดสอบ](#การรันทดสอบ)
4. [การเขียนการทดสอบ](#การเขียนการทดสอบ)
5. [แนวทางการทดสอบที่ดี](#แนวทางการทดสอบที่ดี)

## 🔧 การเตรียมสภาพแวดล้อม

### 1. ติดตั้ง Dependencies
```bash
# ติดตั้ง dependencies สำหรับการทดสอบ
pip install -r requirements-dev.txt
```

### 2. ตรวจสอบการติดตั้ง
```bash
# ตรวจสอบเวอร์ชัน pytest
pytest --version

# ตรวจสอบ plugins ที่ติดตั้ง
pytest --trace-config
```

## 📁 โครงสร้างการทดสอบ

```
tests/
├── conftest.py          # Shared fixtures
├── test_processor.py    # Excel Processor tests
├── test_template.py     # Template Manager tests
└── data/               # Test data files
```

### Fixtures ที่มีให้ใช้
1. `test_data_dir`: โฟลเดอร์ชั่วคราวสำหรับเก็บข้อมูลทดสอบ
2. `sample_excel`: ไฟล์ Excel ตัวอย่างสำหรับทดสอบ
3. `processor`: ExcelProcessor instance
4. `template_manager`: TemplateManager instance
5. `print_manager`: PrintManager instance

## 🚀 การรันทดสอบ

### 1. รันทดสอบทั้งหมด
```bash
pytest
```

### 2. รันเฉพาะบางประเภท
```bash
# Unit tests
pytest -m unit

# Integration tests
pytest -m integration

# Performance tests
pytest -m performance

# Async tests
pytest -m async
```

### 3. รันแบบ Parallel
```bash
# ใช้ CPU ทุก core
pytest -n auto

# กำหนดจำนวน processes
pytest -n 4
```

### 4. รันพร้อมดูความครอบคลุม
```bash
# ดูรายงานใน terminal
pytest --cov

# สร้างรายงาน HTML
pytest --cov --cov-report=html
```

### 5. รันเฉพาะ Performance Tests
```bash
# รัน benchmark tests
pytest --benchmark-only

# บันทึกผล benchmark
pytest --benchmark-autosave
```

## ✍️ การเขียนการทดสอบ

### 1. การเขียน Unit Test พื้นฐาน
```python
def test_process_excel_file(processor):
    """ทดสอบการประมวลผลไฟล์ Excel พื้นฐาน"""
    result = processor.process_file()
    assert result['status'] == 'success'
    assert 'data' in result
```

### 2. การทดสอบ Async Functions
```python
@pytest.mark.asyncio
async def test_async_processing(processor):
    """ทดสอบการประมวลผลแบบ async"""
    result = await processor.process_async()
    assert result['status'] == 'success'
```

### 3. การทดสอบ Performance
```python
def test_performance(processor, benchmark):
    """ทดสอบประสิทธิภาพการทำงาน"""
    result = benchmark(processor.process_file)
    assert result['status'] == 'success'
    assert benchmark.stats.stats.mean < 1.0
```

### 4. การจัดการ Test Data
```python
def test_with_custom_data(processor, test_data_dir):
    """ทดสอบด้วยข้อมูลที่กำหนดเอง"""
    # สร้างข้อมูลทดสอบ
    data = {
        'รหัส': ['001', '002'],
        'ชื่อ': ['ทดสอบ1', 'ทดสอบ2']
    }
    df = pd.DataFrame(data)
    
    # บันทึกไฟล์
    test_file = Path(test_data_dir) / 'custom.xlsx'
    df.to_excel(test_file, index=False)
    
    # ทดสอบ
    processor.file_path = test_file
    result = processor.process_file()
    assert result['status'] == 'success'
```

## 💡 แนวทางการทดสอบที่ดี

### 1. การตั้งชื่อ Test Function
- ใช้ชื่อที่อธิบายสิ่งที่ทดสอบ
- เริ่มด้วย `test_`
- ใช้ snake_case
```python
def test_process_large_excel_file():
def test_invalid_template_format():
def test_concurrent_processing():
```

### 2. การใช้ Fixtures
- ใช้ fixtures เพื่อลดการเขียนโค้ดซ้ำ
- สร้าง fixtures ที่ใช้ร่วมกันใน conftest.py
- กำหนด scope ให้เหมาะสม
```python
@pytest.fixture(scope="session")
def large_excel_file(test_data_dir):
    """สร้างไฟล์ Excel ขนาดใหญ่สำหรับทดสอบ"""
    # สร้างข้อมูล
    return file_path
```

### 3. การจัดการ Test Data
- แยกข้อมูลทดสอบออกจากโค้ด
- ใช้ temporary files/directories
- ทำความสะอาดหลังทดสอบเสร็จ

### 4. การทดสอบ Error Cases
- ทดสอบกรณีผิดพลาดต่างๆ
- ใช้ pytest.raises ตรวจสอบ exceptions
```python
def test_error_handling():
    with pytest.raises(ValueError) as exc_info:
        # ทำให้เกิด error
    assert "error message" in str(exc_info.value)
```

### 5. การใช้ Markers
- ใช้ markers แยกประเภทการทดสอบ
- กำหนด markers ใน pytest.ini
```python
@pytest.mark.slow
@pytest.mark.integration
def test_large_file_processing():
```

## 🔍 การแก้ไขปัญหาที่พบบ่อย

### 1. การทดสอบไม่ผ่าน
- ตรวจสอบ test data
- ดู log ในโหมด verbose: `pytest -v`
- ใช้ pytest-sugar ดูผลแบบสวยงาม

### 2. การทดสอบช้า
- ใช้ parallel testing
- แยก slow tests ด้วย markers
- ใช้ pytest-xdist

### 3. Memory Issues
- ใช้ fixtures แบบ function scope
- ทำความสะอาดข้อมูลหลังทดสอบ
- ระวังการสร้างข้อมูลขนาดใหญ่

## 📊 การวิเคราะห์ผลการทดสอบ

### 1. Coverage Report
```bash
# สร้างรายงาน HTML
pytest --cov --cov-report=html

# ดูส่วนที่ยังไม่ได้ทดสอบ
pytest --cov-report=term-missing
```

### 2. Performance Report
```bash
# ดูผล benchmark
pytest --benchmark-only --benchmark-sort=mean

# เปรียบเทียบกับครั้งก่อน
pytest --benchmark-compare
```

## 🤝 การสนับสนุน

### การรายงานปัญหา
- สร้าง issue ใน GitHub
- แนบ log การทดสอบ
- อธิบายขั้นตอนที่ทำให้เกิดปัญหา

### การขอความช่วยเหลือ
- Discord: [ลิงก์]
- GitHub Discussions
- Email: support@example.com 