import pandas as pd

# สร้างข้อมูลทดสอบ
test_data = {
    'ชื่อ-นามสกุล': ['บริษัท ทดสอบ จำกัด'],
    'ที่อยู่': ['123 ถ.ทดสอบ ต.ทดสอบ อ.ทดสอบ จ.ทดสอบ 12345'],
    'เลขประจำตัวผู้เสียภาษี': ['1234567890123']
}

# สร้าง DataFrame
df = pd.DataFrame(test_data)

# บันทึกเป็นไฟล์ Excel
df.to_excel('tests/data/test_invoice.xlsx', index=False) 