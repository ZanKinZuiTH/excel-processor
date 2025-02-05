import pytest
import pandas as pd
from excel_processor import ExcelProcessor
from pathlib import Path

def test_process_excel_file(processor, test_data_dir):
    """ทดสอบการประมวลผลไฟล์ Excel พื้นฐาน"""
    result = processor.process_file()
    assert result['status'] == 'success'
    assert 'data' in result
    assert len(result['data']) == 3  # จำนวนแถวตามข้อมูลตัวอย่าง

def test_excel_validation(processor):
    """ทดสอบการตรวจสอบความถูกต้องของข้อมูล"""
    validation_result = processor.validate_data()
    assert validation_result['is_valid'] == True
    assert 'errors' in validation_result
    assert len(validation_result['errors']) == 0

def test_data_transformation(processor):
    """ทดสอบการแปลงข้อมูล"""
    transformed_data = processor.transform_data()
    assert isinstance(transformed_data, pd.DataFrame)
    assert 'รหัส' in transformed_data.columns
    assert 'ชื่อ' in transformed_data.columns
    assert 'อายุ' in transformed_data.columns
    assert 'แผนก' in transformed_data.columns

def test_export_results(processor, test_data_dir):
    """ทดสอบการส่งออกผลลัพธ์"""
    output_path = Path(test_data_dir) / 'output' / 'result.xlsx'
    result = processor.export_results(output_path)
    assert result['status'] == 'success'
    assert output_path.exists()

def test_batch_processing(processor, test_data_dir):
    """ทดสอบการประมวลผลแบบ batch"""
    files = [Path(test_data_dir) / 'test.xlsx'] * 3  # จำลองการมีไฟล์หลายไฟล์
    results = processor.process_batch(files)
    assert len(results) == 3
    assert all(r['status'] == 'success' for r in results)

@pytest.mark.asyncio
async def test_async_processing(processor):
    """ทดสอบการประมวลผลแบบ async"""
    result = await processor.process_async()
    assert result['status'] == 'success'
    assert 'data' in result

def test_error_handling(processor):
    """ทดสอบการจัดการข้อผิดพลาด"""
    # ทดสอบกรณีไฟล์เสียหาย
    with pytest.raises(Exception) as exc_info:
        processor.file_path = "not_exists.xlsx"
        processor.process_file()
    assert "File not found" in str(exc_info.value)

def test_performance(processor, benchmark):
    """ทดสอบประสิทธิภาพการทำงาน"""
    # ใช้ pytest-benchmark วัดประสิทธิภาพ
    result = benchmark(processor.process_file)
    assert result['status'] == 'success'
    # ตั้งค่าเกณฑ์ความเร็วขั้นต่ำ
    assert benchmark.stats.stats.mean < 1.0  # ต้องทำงานเสร็จภายใน 1 วินาที 