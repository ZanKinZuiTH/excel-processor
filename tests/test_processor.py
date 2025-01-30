"""
ไฟล์ทดสอบสำหรับ Excel Processor

สำหรับนักศึกษา:
1. การเขียนเทสต์:
   - ใช้ pytest framework
   - แยกเทสต์เป็นส่วนๆ ตามฟังก์ชัน
   - ใช้ fixtures เพื่อจัดการข้อมูลทดสอบ

2. การทดสอบการทำงาน:
   - ทดสอบการอ่านไฟล์ Excel
   - ทดสอบการแปลงข้อมูล
   - ทดสอบการจัดการข้อผิดพลาด

3. การพัฒนาต่อยอด:
   - เพิ่มการทดสอบ edge cases
   - เพิ่มการทดสอบประสิทธิภาพ
   - เพิ่มการทดสอบความปลอดภัย
"""

import pytest
import os
from pathlib import Path
from excel_processor.processor import ExcelProcessor

@pytest.fixture
def test_file_path():
    """
    Fixture สำหรับไฟล์ทดสอบ
    
    Tips สำหรับนักศึกษา:
    - สร้างไฟล์ทดสอบที่มีโครงสร้างหลากหลาย
    - ใช้ tmp_path สำหรับไฟล์ชั่วคราว
    - เพิ่มข้อมูลทดสอบที่ครอบคลุม
    """
    return Path("tests/data/test_invoice.xlsx")

@pytest.fixture
def processor(test_file_path):
    """
    Fixture สำหรับ ExcelProcessor
    
    Tips สำหรับนักศึกษา:
    - ตั้งค่าเริ่มต้นที่เหมาะสม
    - จัดการทรัพยากรอย่างถูกต้อง
    - เพิ่มการตรวจสอบความพร้อม
    """
    return ExcelProcessor(test_file_path)

def test_extract_customer_info(processor):
    """
    ทดสอบการดึงข้อมูลลูกค้า
    
    Tips สำหรับนักศึกษา:
    - ทดสอบรูปแบบข้อมูลที่หลากหลาย
    - ตรวจสอบการจัดการข้อมูลที่ไม่สมบูรณ์
    - เพิ่มการทดสอบข้อผิดพลาด
    """
    info = processor.extract_customer_info()
    assert isinstance(info, dict)
    assert "name" in info
    assert "address" in info
    assert "tax_id" in info

def test_process_file(processor):
    """
    ทดสอบการประมวลผลไฟล์
    
    Tips สำหรับนักศึกษา:
    - ทดสอบการแปลงข้อมูลที่ซับซ้อน
    - ตรวจสอบผลลัพธ์ที่ได้
    - เพิ่มการทดสอบประสิทธิภาพ
    """
    result = processor.process_file()
    assert result is not None
    assert "processed_data" in result
    assert "summary" in result

def test_save_template(processor, tmp_path):
    """
    ทดสอบการบันทึกเทมเพลต
    
    Tips สำหรับนักศึกษา:
    - ทดสอบการบันทึกในรูปแบบต่างๆ
    - ตรวจสอบความถูกต้องของไฟล์
    - เพิ่มการทดสอบความปลอดภัย
    """
    output_path = tmp_path / "output.xlsx"
    processor.save_template(output_path)
    assert output_path.exists()
    assert output_path.stat().st_size > 0

def test_invalid_file():
    """
    ทดสอบการจัดการไฟล์ที่ไม่ถูกต้อง
    
    Tips สำหรับนักศึกษา:
    - ทดสอบไฟล์ที่ไม่มีอยู่
    - ทดสอบไฟล์ที่เสียหาย
    - เพิ่มการทดสอบความปลอดภัย
    """
    with pytest.raises(FileNotFoundError):
        ExcelProcessor("nonexistent.xlsx")

def test_large_file(tmp_path):
    """
    ทดสอบการจัดการไฟล์ขนาดใหญ่
    
    Tips สำหรับนักศึกษา:
    - ทดสอบประสิทธิภาพ
    - ตรวจสอบการใช้หน่วยความจำ
    - เพิ่มการทดสอบการทำงานแบบ async
    """
    # สร้างไฟล์ขนาดใหญ่
    import pandas as pd
    import numpy as np
    
    # สร้างข้อมูลทดสอบ
    rows = 100000
    df = pd.DataFrame({
        'ชื่อ-นามสกุล': ['ทดสอบ'] * rows,
        'ที่อยู่': ['กรุงเทพฯ'] * rows,
        'เลขประจำตัวผู้เสียภาษี': ['1234567890'] * rows,
        'ข้อมูล': np.random.rand(rows)
    })
    
    # บันทึกไฟล์
    test_file = tmp_path / "large_test.xlsx"
    df.to_excel(test_file, index=False)
    
    # ทดสอบประมวลผล
    import time
    start_time = time.time()
    
    processor = ExcelProcessor(test_file)
    result = processor.process_file()
    
    process_time = time.time() - start_time
    
    # ตรวจสอบผลลัพธ์
    assert result is not None
    assert result['summary']['total_rows'] == rows
    assert process_time < 60  # ต้องเสร็จภายใน 60 วินาที

def test_concurrent_processing(tmp_path):
    """
    ทดสอบการประมวลผลพร้อมกัน
    
    Tips สำหรับนักศึกษา:
    - ทดสอบการทำงานแบบ concurrent
    - ตรวจสอบการแย่งใช้ทรัพยากร
    - เพิ่มการทดสอบ race conditions
    """
    import concurrent.futures
    import pandas as pd
    
    # สร้างไฟล์ทดสอบหลายไฟล์
    files = []
    for i in range(5):
        df = pd.DataFrame({
            'ชื่อ-นามสกุล': [f'ทดสอบ {i}'],
            'ที่อยู่': ['กรุงเทพฯ'],
            'เลขประจำตัวผู้เสียภาษี': ['1234567890']
        })
        test_file = tmp_path / f"test_{i}.xlsx"
        df.to_excel(test_file, index=False)
        files.append(test_file)
    
    # ทดสอบประมวลผลพร้อมกัน
    def process_file(file_path):
        processor = ExcelProcessor(file_path)
        return processor.process_file()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(process_file, f) for f in files]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    
    # ตรวจสอบผลลัพธ์
    assert len(results) == len(files)
    for result in results:
        assert result is not None
        assert "processed_data" in result
        assert "summary" in result

def test_clean_data(processor):
    """
    ทดสอบการทำความสะอาดข้อมูล
    
    Tips สำหรับนักศึกษา:
    - ทดสอบการจัดการค่า null
    - ทดสอบการลบข้อมูลซ้ำ
    - ทดสอบการแปลงรูปแบบข้อมูล
    """
    # โหลดไฟล์ก่อนทดสอบ
    processor.load_file()
    
    # ทดสอบก่อนทำความสะอาด
    initial_rows = len(processor.df)
    
    # ทำความสะอาดข้อมูล
    processor.clean_data()
    
    # ตรวจสอบผลลัพธ์
    assert len(processor.df) <= initial_rows  # จำนวนแถวต้องไม่เพิ่มขึ้น
    
    # ตรวจสอบว่าไม่มีคอลัมน์ที่ไม่มีชื่อ
    unnamed_cols = [col for col in processor.df.columns if 'Unnamed:' in str(col)]
    assert len(unnamed_cols) == 0
    
    # ตรวจสอบค่า null ในคอลัมน์หลัก
    main_columns = ['ชื่อ-นามสกุล', 'ที่อยู่', 'เลขประจำตัวผู้เสียภาษี']
    for col in main_columns:
        if col in processor.df.columns:
            assert processor.df[col].isnull().sum() == 0

def test_analyze_data(processor):
    """
    ทดสอบการวิเคราะห์ข้อมูล
    
    Tips สำหรับนักศึกษา:
    - ทดสอบการคำนวณสถิติ
    - ทดสอบการจัดกลุ่ม
    - ทดสอบการวิเคราะห์แนวโน้ม
    """
    # วิเคราะห์ข้อมูล
    analysis = processor.analyze_data()
    
    # ตรวจสอบผลลัพธ์
    assert "numeric_stats" in analysis
    assert "groupby_results" in analysis
    assert "time_series" in analysis
    
    # ตรวจสอบสถิติพื้นฐาน
    for col in processor.df.select_dtypes(include=['int64', 'float64']).columns:
        assert col in analysis["numeric_stats"]
        stats = analysis["numeric_stats"][col]
        assert "count" in stats
        assert "mean" in stats
        assert "std" in stats
    
    # ตรวจสอบการจัดกลุ่ม
    for col in processor.df.select_dtypes(include=['object']).columns:
        assert col in analysis["groupby_results"]
        assert isinstance(analysis["groupby_results"][col], dict)

def test_data_validation(processor):
    """
    ทดสอบการตรวจสอบข้อมูล
    
    Tips สำหรับนักศึกษา:
    - ทดสอบการตรวจจับค่า null
    - ทดสอบการตรวจจับค่าผิดปกติ
    - ทดสอบการตรวจสอบรูปแบบข้อมูล
    """
    validation = processor.validate_data()
    
    # ตรวจสอบโครงสร้างผลลัพธ์
    assert "null_check" in validation
    assert "duplicate_check" in validation
    assert "data_types" in validation
    assert "outliers" in validation
    
    # ตรวจสอบค่า null
    assert "missing_values" in validation["null_check"]
    assert "missing_percentage" in validation["null_check"]
    
    # ตรวจสอบค่าซ้ำ
    assert "duplicates" in validation["duplicate_check"]
    assert "duplicate_percentage" in validation["duplicate_check"]
    
    # ตรวจสอบค่าผิดปกติ
    for col in processor.df.select_dtypes(include=['int64', 'float64']).columns:
        if col in validation["outliers"]:
            assert "outliers_count" in validation["outliers"][col]
            assert "min" in validation["outliers"][col]
            assert "max" in validation["outliers"][col]

if __name__ == "__main__":
    pytest.main(["-v"]) 