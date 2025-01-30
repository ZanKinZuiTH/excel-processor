"""
ระบบประมวลผลไฟล์ Excel

สำหรับนักศึกษา:
1. การใช้งาน pandas:
   - อ่านและเขียนไฟล์ Excel
   - จัดการข้อมูลใน DataFrame
   - แปลงรูปแบบข้อมูล

2. การจัดการข้อผิดพลาด:
   - ตรวจสอบไฟล์
   - จัดการข้อมูลที่ไม่สมบูรณ์
   - บันทึก log

3. การพัฒนาต่อยอด:
   - เพิ่มการวิเคราะห์ข้อมูล
   - เพิ่มการตรวจสอบคุณภาพ
   - เพิ่มการแปลงรูปแบบ
"""

import os
import pandas as pd
import logging
from typing import Dict, Any, Optional
from pathlib import Path

# ตั้งค่า logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExcelProcessor:
    """
    ประมวลผลไฟล์ Excel
    
    สำหรับนักศึกษา:
    1. ศึกษาการทำงานของแต่ละเมธอด
    2. ทดลองเพิ่มฟีเจอร์ใหม่
    3. ปรับปรุงประสิทธิภาพ
    """
    
    def __init__(self, file_path: str):
        """
        กำหนดค่าเริ่มต้น
        
        Args:
            file_path: พาธของไฟล์ Excel
        """
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"ไม่พบไฟล์: {file_path}")
        
        self.df = None  # DataFrame สำหรับเก็บข้อมูล
        self.processed_data = {}  # ข้อมูลที่ประมวลผลแล้ว
        
        logger.info(f"เริ่มต้นประมวลผลไฟล์: {file_path}")
    
    def load_file(self) -> None:
        """
        โหลดไฟล์ Excel เข้า DataFrame
        
        Tips สำหรับนักศึกษา:
        - ใช้ pd.read_excel() สำหรับอ่านไฟล์
        - ตรวจสอบ sheet_name ที่ต้องการ
        - จัดการ NaN values
        """
        try:
            self.df = pd.read_excel(self.file_path)
            logger.info(f"โหลดไฟล์สำเร็จ: {len(self.df)} แถว")
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการโหลดไฟล์: {str(e)}")
            raise
    
    def extract_customer_info(self) -> Dict[str, Any]:
        """
        ดึงข้อมูลลูกค้าจาก DataFrame
        
        Returns:
            Dict[str, Any]: ข้อมูลลูกค้า
        
        Tips สำหรับนักศึกษา:
        - ใช้ df.loc[] สำหรับดึงข้อมูลแบบมีเงื่อนไข
        - ทำความสะอาดข้อมูลก่อนส่งคืน
        - จัดการข้อมูลที่หายไป
        """
        if self.df is None:
            self.load_file()
        
        try:
            # ดึงข้อมูลลูกค้า
            customer_info = {
                "name": self.df.iloc[0].get("ชื่อ-นามสกุล", ""),
                "address": self.df.iloc[0].get("ที่อยู่", ""),
                "tax_id": self.df.iloc[0].get("เลขประจำตัวผู้เสียภาษี", "")
            }
            
            logger.info(f"ดึงข้อมูลลูกค้าสำเร็จ: {customer_info['name']}")
            return customer_info
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการดึงข้อมูลลูกค้า: {str(e)}")
            raise
    
    def process_file(self) -> Dict[str, Any]:
        """
        ประมวลผลไฟล์ทั้งหมด
        
        Returns:
            Dict[str, Any]: ผลลัพธ์การประมวลผล
        
        Tips สำหรับนักศึกษา:
        - แบ่งการประมวลผลเป็นส่วนๆ
        - เพิ่มการตรวจสอบข้อมูล
        - สร้างรายงานสรุป
        """
        try:
            if self.df is None:
                self.load_file()
            
            # ประมวลผลข้อมูล
            customer_info = self.extract_customer_info()
            
            # สรุปผล
            self.processed_data = {
                "customer_info": customer_info,
                "processed_data": self.df.to_dict(),
                "summary": {
                    "total_rows": len(self.df),
                    "columns": list(self.df.columns)
                }
            }
            
            logger.info("ประมวลผลไฟล์สำเร็จ")
            return self.processed_data
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการประมวลผล: {str(e)}")
            raise
    
    def save_template(self, output_path: str) -> None:
        """
        บันทึกเทมเพลต
        
        Args:
            output_path: พาธสำหรับบันทึกไฟล์
        
        Tips สำหรับนักศึกษา:
        - ใช้ df.to_excel() สำหรับบันทึกไฟล์
        - ตั้งค่า format ต่างๆ
        - เพิ่ม metadata
        """
        try:
            if self.df is None:
                self.load_file()
            
            # บันทึกไฟล์
            self.df.to_excel(output_path, index=False)
            logger.info(f"บันทึกเทมเพลตสำเร็จ: {output_path}")
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการบันทึกเทมเพลต: {str(e)}")
            raise
    
    def validate_data(self) -> Dict[str, Any]:
        """
        ตรวจสอบความถูกต้องของข้อมูล
        
        Returns:
            Dict[str, Any]: ผลการตรวจสอบ
        
        Tips สำหรับนักศึกษา:
        - ตรวจสอบค่า null
        - ตรวจสอบรูปแบบข้อมูล
        - ตรวจสอบค่าที่ผิดปกติ
        """
        if self.df is None:
            self.load_file()
        
        validation_results = {
            "missing_values": self.df.isnull().sum().to_dict(),
            "duplicates": len(self.df[self.df.duplicated()]),
            "total_rows": len(self.df)
        }
        
        logger.info(f"ตรวจสอบข้อมูลสำเร็จ: {validation_results}")
        return validation_results 