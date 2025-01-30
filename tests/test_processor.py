import unittest
from pathlib import Path
from main import ExcelProcessor
import json
import os

class TestExcelProcessor(unittest.TestCase):
    def setUp(self):
        """เตรียมข้อมูลสำหรับการทดสอบ"""
        self.test_file = "demo/invoice_template.xlsx"
        self.processor = ExcelProcessor(self.test_file)

    def test_extract_customer_info(self):
        """ทดสอบการแยกข้อมูลลูกค้า"""
        # ทดสอบกรณีข้อมูลถูกต้อง
        test_data = "นางสาว ราตรี สกุลวงษ์"
        result = self.processor.extract_customer_info(test_data)
        self.assertEqual(result["title"], "นางสาว")
        self.assertEqual(result["first_name"], "ราตรี")
        self.assertEqual(result["last_name"], "สกุลวงษ์")

        # ทดสอบกรณีข้อมูลไม่ถูกต้อง
        test_data = "ไม่มีคำนำหน้า"
        result = self.processor.extract_customer_info(test_data)
        self.assertIsNone(result)

    def test_process_file(self):
        """ทดสอบการประมวลผลไฟล์"""
        if Path(self.test_file).exists():
            result = self.processor.process_file()
            self.assertIsInstance(result, dict)
            self.assertTrue(len(result) > 0)

    def test_save_template(self):
        """ทดสอบการบันทึกเทมเพลต"""
        test_data = {
            "Sheet1": {
                "content": [
                    {"name": "Test User", "value": 100}
                ],
                "structure": [
                    {"row": 1, "type": "header"}
                ]
            }
        }
        self.processor.save_as_template("test_template", test_data)
        
        # ตรวจสอบว่ามีการบันทึกลงฐานข้อมูล
        with self.processor.engine.connect() as conn:
            result = conn.execute(
                self.processor.template_table.select().where(
                    self.processor.template_table.c.name == "test_template"
                )
            ).first()
            self.assertIsNotNone(result)

    def tearDown(self):
        """ทำความสะอาดหลังการทดสอบ"""
        if os.path.exists("excel_data.db"):
            os.remove("excel_data.db")

if __name__ == '__main__':
    unittest.main() 