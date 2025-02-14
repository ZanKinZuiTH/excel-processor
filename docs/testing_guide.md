# 🧪 คู่มือการทดสอบระบบ Excel Processor

## 📑 สารบัญ
- [🚀 การเตรียมสภาพแวดล้อม](#-การเตรียมสภาพแวดล้อม)
- [📊 การทดสอบระบบ Template](#-การทดสอบระบบ-template)
- [🔍 การทดสอบการประมวลผลข้อมูล](#-การทดสอบการประมวลผลข้อมูล)
- [🤖 การทดสอบระบบ AI](#-การทดสอบระบบ-ai)
- [🖨️ การทดสอบระบบพิมพ์](#️-การทดสอบระบบพิมพ์)
- [🔒 การทดสอบระบบความปลอดภัย](#-การทดสอบระบบความปลอดภัย)
- [📈 การทดสอบระบบติดตาม](#-การทดสอบระบบติดตาม)

## 🚀 การเตรียมสภาพแวดล้อม

### การติดตั้ง Testing Framework
```bash
pip install pytest pytest-cov pytest-mock pytest-asyncio
```

### การเตรียมข้อมูลทดสอบ
1. สร้างโฟลเดอร์ `tests/data/`
2. เตรียมไฟล์ทดสอบ:
   - `sample_data.xlsx`
   - `invalid_data.xlsx`
   - `large_data.xlsx`

### การรันเทสทั้งหมด
```bash
pytest tests/ -v --cov=./ --cov-report=html
```

## 📊 การทดสอบระบบ Template

### Unit Tests สำหรับ Template Manager
```python
def test_create_template():
    template = TemplateManager()
    result = template.create_template(name="Test", columns=["A", "B"])
    assert result.name == "Test"
    assert len(result.columns) == 2

def test_validate_template():
    template = TemplateManager()
    is_valid = template.validate_template(data=sample_data)
    assert is_valid == True
```

### Integration Tests
```python
def test_template_workflow():
    # 1. สร้าง Template
    template = create_test_template()
    
    # 2. ใช้งานกับข้อมูล
    processor = DataProcessor(template)
    result = processor.process_data(test_data)
    
    # 3. ตรวจสอบผล
    assert result.success == True
```

## 🔍 การทดสอบการประมวลผลข้อมูล

### การทดสอบการนำเข้าข้อมูล
```python
def test_data_import():
    processor = DataProcessor()
    
    # ทดสอบไฟล์ปกติ
    result = processor.import_file("valid.xlsx")
    assert result.success == True
    
    # ทดสอบไฟล์ไม่ถูกต้อง
    with pytest.raises(InvalidFileError):
        processor.import_file("invalid.xlsx")
```

### การทดสอบการตรวจสอบข้อมูล
```python
def test_data_validation():
    validator = DataValidator()
    
    # ทดสอบค่าว่าง
    nulls = validator.check_nulls(data)
    assert len(nulls) == 0
    
    # ทดสอบข้อมูลซ้ำ
    duplicates = validator.check_duplicates(data)
    assert len(duplicates) == 0
```

## 🤖 การทดสอบระบบ AI

### การทดสอบ Prophet
```python
def test_prophet_analysis():
    analyzer = TrendAnalyzer()
    
    # ทดสอบการวิเคราะห์
    forecast = analyzer.analyze_trend(data, period=30)
    assert len(forecast) == 30
    assert "yhat" in forecast.columns
```

### การทดสอบ LSTM
```python
def test_lstm_prediction():
    predictor = LSTMPredictor()
    
    # ทดสอบการเทรน
    model = predictor.train(train_data, epochs=10)
    assert model.trained == True
    
    # ทดสอบการพยากรณ์
    prediction = predictor.predict(test_data)
    assert len(prediction) > 0
```

## 🖨️ การทดสอบระบบพิมพ์

### การทดสอบการตั้งค่าเครื่องพิมพ์
```python
def test_printer_setup():
    printer = PrinterManager()
    
    # ทดสอบการตั้งค่า
    config = printer.setup(name="Test", paper_size="A4")
    assert config.name == "Test"
    assert config.paper_size == "A4"
```

### การทดสอบการพิมพ์
```python
def test_print_document():
    printer = PrinterManager()
    
    # ทดสอบการพิมพ์
    job = printer.print_document(doc="test.pdf", copies=2)
    assert job.status == "completed"
    assert job.copies == 2
```

## 🔒 การทดสอบระบบความปลอดภัย

### การทดสอบการยืนยันตัวตน
```python
def test_authentication():
    auth = AuthManager()
    
    # ทดสอบการล็อกอิน
    token = auth.login(username="test", password="pass")
    assert token is not None
    
    # ทดสอบการตรวจสอบโทเคน
    is_valid = auth.verify_token(token)
    assert is_valid == True
```

### การทดสอบการเข้ารหัส
```python
def test_encryption():
    crypto = CryptoManager()
    
    # ทดสอบการเข้ารหัส
    encrypted = crypto.encrypt(data="test")
    assert encrypted != "test"
    
    # ทดสอบการถอดรหัส
    decrypted = crypto.decrypt(encrypted)
    assert decrypted == "test"
```

## 📈 การทดสอบระบบติดตาม

### การทดสอบการติดตามทรัพยากร
```python
def test_resource_monitoring():
    monitor = ResourceMonitor()
    
    # ทดสอบการติดตาม CPU
    cpu_usage = monitor.get_cpu_usage()
    assert 0 <= cpu_usage <= 100
    
    # ทดสอบการติดตาม RAM
    ram_usage = monitor.get_ram_usage()
    assert ram_usage > 0
```

### การทดสอบการแจ้งเตือน
```python
def test_alerts():
    alerter = AlertManager()
    
    # ทดสอบการสร้างการแจ้งเตือน
    alert = alerter.create_alert(
        type="cpu_high",
        threshold=90
    )
    assert alert.active == True
    
    # ทดสอบการส่งการแจ้งเตือน
    notification = alerter.send_alert(alert)
    assert notification.sent == True
```

## 📊 การวัดความครอบคลุมของการทดสอบ

### การรันเทสพร้อมรายงาน
```bash
pytest --cov=./ --cov-report=html
```

### เป้าหมายความครอบคลุม
- Unit Tests: > 90%
- Integration Tests: > 80%
- End-to-End Tests: > 70%

### การตรวจสอบคุณภาพโค้ด
```bash
# ตรวจสอบ Code Style
flake8 ./

# ตรวจสอบ Type Hints
mypy ./

# ตรวจสอบความซับซ้อน
radon cc ./
```

## 🔄 การทดสอบอัตโนมัติ

### การตั้งค่า CI/CD
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest
```

### การรันเทสอัตโนมัติ
```bash
# ทดสอบก่อน Commit
pre-commit run --all-files

# ทดสอบก่อน Push
git push origin main
```

---

## 📝 การรายงานข้อผิดพลาด

หากพบข้อผิดพลาดในการทดสอบ กรุณาแจ้งผ่าน:
1. สร้าง Issue ใน GitHub
2. แจ้งทีมพัฒนาที่ support@brxg.co.th
3. แจ้งผ่าน Line: @brxgdev 