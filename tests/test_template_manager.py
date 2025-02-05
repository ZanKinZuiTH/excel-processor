import pytest
from pathlib import Path
from template_manager import TemplateManager

def test_create_template(template_manager, test_data_dir):
    """ทดสอบการสร้างเทมเพลต"""
    template_data = {
        'name': 'test_template',
        'fields': ['รหัส', 'ชื่อ', 'อายุ', 'แผนก'],
        'format': 'A4',
        'orientation': 'portrait'
    }
    result = template_manager.create_template(template_data)
    assert result['status'] == 'success'
    assert result['template_id'] is not None

def test_load_template(template_manager):
    """ทดสอบการโหลดเทมเพลต"""
    template = template_manager.load_template('test_template')
    assert template is not None
    assert template['name'] == 'test_template'
    assert len(template['fields']) == 4

def test_update_template(template_manager):
    """ทดสอบการอัพเดทเทมเพลต"""
    updates = {
        'name': 'test_template',
        'fields': ['รหัส', 'ชื่อ', 'อายุ', 'แผนก', 'เงินเดือน'],
        'format': 'A4',
        'orientation': 'landscape'
    }
    result = template_manager.update_template('test_template', updates)
    assert result['status'] == 'success'
    
    # ตรวจสอบการอัพเดท
    updated = template_manager.load_template('test_template')
    assert len(updated['fields']) == 5
    assert updated['orientation'] == 'landscape'

def test_delete_template(template_manager):
    """ทดสอบการลบเทมเพลต"""
    result = template_manager.delete_template('test_template')
    assert result['status'] == 'success'
    
    # ตรวจสอบว่าไม่สามารถโหลดเทมเพลตที่ลบแล้วได้
    with pytest.raises(Exception):
        template_manager.load_template('test_template')

def test_list_templates(template_manager):
    """ทดสอบการแสดงรายการเทมเพลต"""
    # สร้างเทมเพลตหลายอัน
    templates = [
        {'name': f'template_{i}', 'fields': ['field1', 'field2']}
        for i in range(3)
    ]
    for t in templates:
        template_manager.create_template(t)
    
    # ตรวจสอบรายการ
    template_list = template_manager.list_templates()
    assert len(template_list) >= 3
    assert all(isinstance(t, dict) for t in template_list)

def test_template_validation(template_manager):
    """ทดสอบการตรวจสอบความถูกต้องของเทมเพลต"""
    # ทดสอบเทมเพลตที่ไม่ถูกต้อง
    invalid_template = {
        'name': 'invalid',
        'fields': []  # ไม่มี fields
    }
    with pytest.raises(ValueError):
        template_manager.create_template(invalid_template)

def test_template_preview(template_manager, test_data_dir):
    """ทดสอบการสร้างตัวอย่างเทมเพลต"""
    template_data = {
        'name': 'preview_test',
        'fields': ['รหัส', 'ชื่อ'],
        'format': 'A4'
    }
    template_manager.create_template(template_data)
    
    preview_path = Path(test_data_dir) / 'previews' / 'preview_test.pdf'
    result = template_manager.generate_preview('preview_test', preview_path)
    assert result['status'] == 'success'
    assert preview_path.exists()

@pytest.mark.asyncio
async def test_async_template_operations(template_manager):
    """ทดสอบการทำงานแบบ async ของ Template Manager"""
    template_data = {
        'name': 'async_test',
        'fields': ['field1', 'field2']
    }
    result = await template_manager.create_template_async(template_data)
    assert result['status'] == 'success'
    
    loaded = await template_manager.load_template_async('async_test')
    assert loaded['name'] == 'async_test' 