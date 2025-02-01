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
    
    def clean_data(self) -> None:
        """
        ทำความสะอาดข้อมูล
        
        Tips สำหรับนักศึกษา:
        - จัดการค่า null
        - ลบข้อมูลซ้ำ
        - แปลงรูปแบบข้อมูล
        """
        if self.df is None:
            self.load_file()
        
        # ลบคอลัมน์ที่ไม่มีชื่อ
        unnamed_cols = [col for col in self.df.columns if 'Unnamed:' in str(col)]
        self.df = self.df.drop(columns=unnamed_cols)
        
        # จัดการค่า null
        self.df = self.df.fillna({
            'ชื่อ-นามสกุล': 'ไม่ระบุ',
            'ที่อยู่': 'ไม่ระบุ',
            'เลขประจำตัวผู้เสียภาษี': '0000000000'
        })
        
        # ลบข้อมูลซ้ำ
        self.df = self.df.drop_duplicates()
        
        # แปลงรูปแบบวันที่
        date_columns = self.df.select_dtypes(include=['datetime64']).columns
        for col in date_columns:
            self.df[col] = pd.to_datetime(self.df[col]).dt.strftime('%Y-%m-%d')
        
        logger.info(f"ทำความสะอาดข้อมูลสำเร็จ: {len(self.df)} แถว")
    
    def analyze_data(self) -> Dict[str, Any]:
        """
        วิเคราะห์ข้อมูลเชิงลึก
        
        Returns:
            Dict[str, Any]: ผลการวิเคราะห์
        
        Tips สำหรับนักศึกษา:
        - คำนวณสถิติพื้นฐาน
        - วิเคราะห์แนวโน้ม
        - สร้างการจัดกลุ่ม
        """
        if self.df is None:
            self.load_file()
        
        # สถิติพื้นฐาน
        numeric_stats = {}
        for col in self.df.select_dtypes(include=['int64', 'float64']).columns:
            data = self.df[col].dropna()  # ลบค่า NaN ก่อนคำนวณ
            if len(data) > 0:  # ตรวจสอบว่ามีข้อมูลก่อนคำนวณ
                numeric_stats[col] = {
                    "count": len(data),
                    "mean": float(data.mean()),
                    "std": float(data.std()) if len(data) > 1 else 0,
                    "min": float(data.min()),
                    "max": float(data.max())
                }
            else:
                numeric_stats[col] = {
                    "count": 0,
                    "mean": 0,
                    "std": 0,
                    "min": 0,
                    "max": 0
                }
        
        # การจัดกลุ่ม
        groupby_results = {}
        for col in self.df.select_dtypes(include=['object']).columns:
            groupby_results[col] = self.df[col].value_counts().to_dict()
        
        # แนวโน้มตามเวลา
        time_series = {}
        date_columns = self.df.select_dtypes(include=['datetime64']).columns
        for col in date_columns:
            time_series[col] = self.df.groupby(col).size().to_dict()
        
        analysis_results = {
            "numeric_stats": numeric_stats,
            "groupby_results": groupby_results,
            "time_series": time_series
        }
        
        logger.info("วิเคราะห์ข้อมูลสำเร็จ")
        return analysis_results

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
        
        # ตรวจสอบค่า null
        null_check = {
            "missing_values": self.df.isnull().sum().to_dict(),
            "missing_percentage": (self.df.isnull().sum() / len(self.df) * 100).to_dict()
        }
        
        # ตรวจสอบค่าซ้ำ
        duplicate_check = {
            "duplicates": len(self.df[self.df.duplicated()]),
            "duplicate_percentage": len(self.df[self.df.duplicated()]) / len(self.df) * 100
        }
        
        # ตรวจสอบรูปแบบข้อมูล
        data_types = {
            col: str(dtype) for col, dtype in self.df.dtypes.items()
        }
        
        # ตรวจสอบค่าที่ผิดปกติ (สำหรับคอลัมน์ตัวเลข)
        outliers = {}
        for col in self.df.select_dtypes(include=['int64', 'float64']).columns:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers[col] = {
                "outliers_count": len(self.df[(self.df[col] < (Q1 - 1.5 * IQR)) | (self.df[col] > (Q3 + 1.5 * IQR))]),
                "min": float(self.df[col].min()),
                "max": float(self.df[col].max()),
                "mean": float(self.df[col].mean()),
                "median": float(self.df[col].median())
            }
        
        validation_results = {
            "null_check": null_check,
            "duplicate_check": duplicate_check,
            "data_types": data_types,
            "outliers": outliers,
            "total_rows": len(self.df),
            "total_columns": len(self.df.columns)
        }
        
        # บันทึก log
        logger.info(f"ตรวจสอบข้อมูลสำเร็จ: {len(self.df)} แถว")
        if null_check["missing_values"]:
            logger.warning(f"พบค่า null: {null_check['missing_values']}")
        if duplicate_check["duplicates"]:
            logger.warning(f"พบข้อมูลซ้ำ: {duplicate_check['duplicates']} แถว")
        
        return validation_results 