import pytest
import os
import tempfile
import shutil
from pathlib import Path
from excel_processor import ExcelProcessor
from template_manager import TemplateManager
from printer import PrintManager

@pytest.fixture(scope="session")
def test_data_dir():
    """สร้างโฟลเดอร์ชั่วคราวสำหรับเก็บข้อมูลทดสอบ"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture(scope="session")
def sample_excel(test_data_dir):
    """สร้างไฟล์ Excel ตัวอย่างสำหรับทดสอบ"""
    import pandas as pd
    
    # สร้างข้อมูลตัวอย่าง
    data = {
        'รหัส': ['001', '002', '003'],
        'ชื่อ': ['สมชาย', 'สมหญิง', 'สมศรี'],
        'อายุ': [25, 30, 35],
        'แผนก': ['IT', 'HR', 'Sales']
    }
    df = pd.DataFrame(data)
    
    # บันทึกไฟล์
    file_path = os.path.join(test_data_dir, 'test.xlsx')
    df.to_excel(file_path, index=False)
    return file_path

@pytest.fixture
def processor(sample_excel):
    """สร้าง ExcelProcessor instance สำหรับทดสอบ"""
    return ExcelProcessor(sample_excel)

@pytest.fixture
def template_manager():
    """สร้าง TemplateManager instance สำหรับทดสอบ"""
    return TemplateManager()

@pytest.fixture
def print_manager():
    """สร้าง PrintManager instance สำหรับทดสอบ"""
    return PrintManager()

@pytest.fixture(autouse=True)
def setup_test_env(test_data_dir):
    """ตั้งค่าสภาพแวดล้อมสำหรับการทดสอบ"""
    # ตั้งค่าตัวแปรสภาพแวดล้อม
    os.environ['TEST_MODE'] = 'true'
    os.environ['TEST_DATA_DIR'] = test_data_dir
    
    # สร้างโฟลเดอร์ที่จำเป็น
    Path(test_data_dir, 'templates').mkdir(exist_ok=True)
    Path(test_data_dir, 'output').mkdir(exist_ok=True)
    Path(test_data_dir, 'previews').mkdir(exist_ok=True)
    
    yield
    
    # เก็บกวาดหลังทดสอบ
    os.environ.pop('TEST_MODE', None)
    os.environ.pop('TEST_DATA_DIR', None) 