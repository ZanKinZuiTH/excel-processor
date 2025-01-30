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
from processor import ExcelProcessor

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
    # TODO: เพิ่มการทดสอบไฟล์ขนาดใหญ่
    pass

def test_concurrent_processing():
    """
    ทดสอบการประมวลผลพร้อมกัน
    
    Tips สำหรับนักศึกษา:
    - ทดสอบการทำงานแบบ concurrent
    - ตรวจสอบการแย่งใช้ทรัพยากร
    - เพิ่มการทดสอบ race conditions
    """
    # TODO: เพิ่มการทดสอบการประมวลผลพร้อมกัน
    pass

if __name__ == "__main__":
    pytest.main(["-v"]) 