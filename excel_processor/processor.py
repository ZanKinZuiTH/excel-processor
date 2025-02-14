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
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
import numpy as np
import traceback
from datetime import datetime

# ตั้งค่า logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExcelProcessorError(Exception):
    """Base class สำหรับ error ทั้งหมดใน ExcelProcessor"""
    pass

class FileNotSupportedError(ExcelProcessorError):
    """Error สำหรับไฟล์ที่ไม่รองรับ"""
    pass

class DataValidationError(ExcelProcessorError):
    """Error สำหรับข้อมูลที่ไม่ถูกต้อง"""
    pass

class ProcessingError(ExcelProcessorError):
    """Error สำหรับการประมวลผลล้มเหลว"""
    pass

class ExcelProcessor:
    """
    ประมวลผลไฟล์ Excel
    
    สำหรับนักศึกษา:
    1. ศึกษาการทำงานของแต่ละเมธอด
    2. ทดลองเพิ่มฟีเจอร์ใหม่
    3. ปรับปรุงประสิทธิภาพ
    """
    
    def __init__(self, file_path: Union[str, Path]) -> None:
        """
        กำหนดค่าเริ่มต้น
        
        Args:
            file_path: พาธของไฟล์ Excel
            
        Raises:
            FileNotFoundError: ถ้าไม่พบไฟล์
            FileNotSupportedError: ถ้าไฟล์ไม่ใช่ไฟล์ Excel
        """
        self.file_path = Path(file_path)
        self.df: Optional[pd.DataFrame] = None
        self.logger = logging.getLogger(__name__)
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"ไม่พบไฟล์: {self.file_path}")
            
        if self.file_path.suffix not in ['.xlsx', '.xls']:
            raise FileNotSupportedError(f"ไม่รองรับไฟล์นามสกุล: {self.file_path.suffix}")
            
        self.processed_data = {}  # ข้อมูลที่ประมวลผลแล้ว
        
        logger.info(f"เริ่มต้นประมวลผลไฟล์: {file_path}")
    
    def load_file(self) -> None:
        """
        โหลดไฟล์ Excel
        
        Raises:
            ProcessingError: ถ้าโหลดไฟล์ไม่สำเร็จ
        """
        try:
            self.df = pd.read_excel(self.file_path)
            logger.info(f"โหลดไฟล์สำเร็จ: {self.file_path}")
        except Exception as e:
            error_msg = f"เกิดข้อผิดพลาดในการโหลดไฟล์: {str(e)}"
            self.logger.error(error_msg)
            self.logger.debug(traceback.format_exc())
            raise ProcessingError(error_msg)
    
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
        ประมวลผลไฟล์ Excel
        
        Returns:
            Dict[str, Any]: ผลการประมวลผล
            
        Raises:
            ProcessingError: ถ้าประมวลผลไม่สำเร็จ
        """
        try:
            # โหลดและตรวจสอบข้อมูล
            validation_results = self.validate_data()
            
            # ประมวลผลข้อมูล
            results = {
                "status": "success",
                "validation": validation_results,
                "statistics": self._calculate_statistics(),
                "processed_at": datetime.now().isoformat()
            }
            
            self.logger.info(f"ประมวลผลไฟล์สำเร็จ: {self.file_path}")
            return results
            
        except Exception as e:
            error_msg = f"เกิดข้อผิดพลาดในการประมวลผล: {str(e)}"
            self.logger.error(error_msg)
            self.logger.debug(traceback.format_exc())
            raise ProcessingError(error_msg)
    
    def validate_data(self) -> Dict[str, Any]:
        """
        ตรวจสอบความถูกต้องของข้อมูล
        
        Returns:
            Dict[str, Any]: ผลการตรวจสอบ
            
        Raises:
            DataValidationError: ถ้าข้อมูลไม่ถูกต้อง
        """
        if self.df is None:
            self.load_file()
            
        validation_results = {
            "is_valid": True,
            "errors": [],
            "warnings": []
        }
        
        try:
            # ตรวจสอบค่าว่าง
            null_counts = self.df.isnull().sum()
            if null_counts.any():
                validation_results["warnings"].append({
                    "type": "null_values",
                    "columns": null_counts[null_counts > 0].to_dict()
                })
                
            # ตรวจสอบค่าซ้ำ
            duplicates = self.df.duplicated()
            if duplicates.any():
                validation_results["warnings"].append({
                    "type": "duplicates",
                    "count": duplicates.sum()
                })
                
            # ตรวจสอบประเภทข้อมูล
            for column in self.df.columns:
                try:
                    if self.df[column].dtype == 'object':
                        pd.to_numeric(self.df[column], errors='raise')
                except:
                    validation_results["warnings"].append({
                        "type": "invalid_numeric",
                        "column": column
                    })
                    
            if len(validation_results["errors"]) > 0:
                validation_results["is_valid"] = False
                
            return validation_results
            
        except Exception as e:
            error_msg = f"เกิดข้อผิดพลาดในการตรวจสอบข้อมูล: {str(e)}"
            self.logger.error(error_msg)
            self.logger.debug(traceback.format_exc())
            raise DataValidationError(error_msg)
    
    def _calculate_statistics(self) -> Dict[str, Any]:
        """
        คำนวณสถิติของข้อมูล
        
        Returns:
            Dict[str, Any]: ข้อมูลสถิติ
            
        Raises:
            ProcessingError: ถ้าคำนวณไม่สำเร็จ
        """
        try:
            stats = {
                "row_count": len(self.df),
                "column_count": len(self.df.columns),
                "numeric_columns": {}
            }
            
            for column in self.df.select_dtypes(include=[np.number]).columns:
                stats["numeric_columns"][column] = {
                    "mean": self.df[column].mean(),
                    "std": self.df[column].std(),
                    "min": self.df[column].min(),
                    "max": self.df[column].max()
                }
                
            return stats
            
        except Exception as e:
            error_msg = f"เกิดข้อผิดพลาดในการคำนวณสถิติ: {str(e)}"
            self.logger.error(error_msg)
            self.logger.debug(traceback.format_exc())
            raise ProcessingError(error_msg)
    
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