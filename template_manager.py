"""
ระบบจัดการเทมเพลต Excel
สำหรับนักศึกษา: ไฟล์นี้เป็นคลาสหลักในการจัดการเทมเพลต Excel
"""

import os
import pandas as pd
from datetime import datetime
import json
import logging
from typing import Dict, List, Any, Optional, Union

class TemplateManager:
    """คลาสสำหรับจัดการเทมเพลต Excel
    
    สำหรับนักศึกษา:
    1. ศึกษาการออกแบบคลาสและเมธอด
    2. สังเกตการใช้ Type Hints
    3. การจัดการไฟล์และข้อมูล
    """
    
    def __init__(self):
        """กำหนดค่าเริ่มต้นสำหรับระบบ"""
        self.templates_dir = "templates"
        self.data_dir = "data"
        self.preview_dir = "previews"
        
        # สร้างโฟลเดอร์ที่จำเป็น
        for directory in [self.templates_dir, self.data_dir, self.preview_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
        
        # ตั้งค่า logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def upload_template(
        self,
        file_path: str,
        name: str,
        description: str,
        sheet_data: Optional[Dict] = None
    ) -> str:
        """อัพโหลดเทมเพลตใหม่
        
        Args:
            file_path: พาธของไฟล์ Excel
            name: ชื่อเทมเพลต
            description: คำอธิบายเทมเพลต
            sheet_data: ข้อมูลจาก sheet ต่างๆ (ถ้ามี)
        
        Returns:
            str: ID ของเทมเพลตที่สร้าง
        """
        try:
            # สร้าง ID สำหรับเทมเพลต
            template_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # บันทึกไฟล์เทมเพลต
            template_path = os.path.join(self.templates_dir, f"{template_id}.xlsx")
            if os.path.exists(file_path):
                df = pd.read_excel(file_path)
                df.to_excel(template_path, index=False)
            
            # บันทึกข้อมูลเทมเพลต
            metadata = {
                "id": template_id,
                "name": name,
                "description": description,
                "created_at": datetime.now().isoformat(),
                "sheet_data": sheet_data or {}
            }
            
            metadata_path = os.path.join(self.templates_dir, f"{template_id}.json")
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"อัพโหลดเทมเพลต {name} สำเร็จ (ID: {template_id})")
            return template_id
            
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการอัพโหลดเทมเพลต: {str(e)}")
            raise
    
    def save_data_entry(
        self,
        template_id: str,
        data: Dict[str, Any]
    ) -> str:
        """บันทึกข้อมูลสำหรับเทมเพลต
        
        Args:
            template_id: ID ของเทมเพลต
            data: ข้อมูลที่ต้องการบันทึก
        
        Returns:
            str: ID ของข้อมูลที่บันทึก
        """
        try:
            # สร้าง ID สำหรับข้อมูล
            entry_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # บันทึกข้อมูล
            data_path = os.path.join(self.data_dir, f"{entry_id}.json")
            entry_data = {
                "id": entry_id,
                "template_id": template_id,
                "created_at": datetime.now().isoformat(),
                "data": data
            }
            
            with open(data_path, 'w', encoding='utf-8') as f:
                json.dump(entry_data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"บันทึกข้อมูลสำเร็จ (ID: {entry_id})")
            return entry_id
            
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการบันทึกข้อมูล: {str(e)}")
            raise
    
    def create_preview(
        self,
        template_id: str,
        entry_id: str,
        sheet_name: Optional[str] = None
    ) -> Dict[str, str]:
        """สร้างตัวอย่างเอกสาร
        
        Args:
            template_id: ID ของเทมเพลต
            entry_id: ID ของข้อมูล
            sheet_name: ชื่อ sheet ที่ต้องการดูตัวอย่าง (ถ้ามี)
        
        Returns:
            Dict[str, str]: ข้อมูลตัวอย่างเอกสาร
        """
        try:
            # โหลดเทมเพลตและข้อมูล
            template_path = os.path.join(self.templates_dir, f"{template_id}.xlsx")
            data_path = os.path.join(self.data_dir, f"{entry_id}.json")
            
            if not os.path.exists(template_path) or not os.path.exists(data_path):
                raise FileNotFoundError("ไม่พบไฟล์เทมเพลตหรือข้อมูล")
            
            # สร้างตัวอย่างเอกสาร
            preview_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            preview_path = os.path.join(self.preview_dir, f"{preview_id}.xlsx")
            
            # อ่านข้อมูล
            with open(data_path, 'r', encoding='utf-8') as f:
                entry_data = json.load(f)
            
            # สร้างไฟล์ตัวอย่าง
            df = pd.read_excel(template_path)
            
            # แปลงข้อมูลเป็น DataFrame
            if sheet_name:
                data = entry_data['data'].get(sheet_name, {})
                if isinstance(data, dict):
                    # กรณีข้อมูลเป็น dict ให้แปลงเป็น DataFrame แถวเดียว
                    df_data = pd.DataFrame([data])
                elif isinstance(data, list):
                    # กรณีข้อมูลเป็น list ให้แปลงเป็น DataFrame หลายแถว
                    df_data = pd.DataFrame(data)
                else:
                    df_data = pd.DataFrame()
                
                # บันทึกไฟล์
                df_data.to_excel(preview_path, sheet_name=sheet_name, index=False)
            else:
                # กรณีไม่ระบุ sheet_name ให้สร้างทุก sheet
                with pd.ExcelWriter(preview_path) as writer:
                    for sheet, data in entry_data['data'].items():
                        if isinstance(data, dict):
                            df_data = pd.DataFrame([data])
                        elif isinstance(data, list):
                            df_data = pd.DataFrame(data)
                        else:
                            df_data = pd.DataFrame()
                        df_data.to_excel(writer, sheet_name=sheet, index=False)
            
            preview_url = f"file://{os.path.abspath(preview_path)}"
            self.logger.info(f"สร้างตัวอย่างเอกสารสำเร็จ (ID: {preview_id})")
            
            return {
                "id": preview_id,
                "url": preview_url
            }
            
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการสร้างตัวอย่างเอกสาร: {str(e)}")
            raise
    
    def print_document(
        self,
        template_id: str,
        entry_id: str,
        printer: str,
        sheets: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """พิมพ์เอกสาร
        
        Args:
            template_id: ID ของเทมเพลต
            entry_id: ID ของข้อมูล
            printer: ชื่อเครื่องพิมพ์
            sheets: รายชื่อ sheet ที่ต้องการพิมพ์ (ถ้ามี)
        
        Returns:
            Dict[str, Any]: ผลการพิมพ์
        """
        try:
            # สร้างตัวอย่างเอกสารก่อนพิมพ์
            preview = self.create_preview(template_id, entry_id)
            
            # จำลองการพิมพ์ (ในที่นี้เป็นแค่การ log)
            self.logger.info(f"กำลังพิมพ์เอกสารไปยังเครื่องพิมพ์ {printer}")
            
            return {
                "status": "success",
                "message": f"ส่งไปยังเครื่องพิมพ์ {printer} สำเร็จ",
                "preview_id": preview["id"]
            }
            
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการพิมพ์เอกสาร: {str(e)}")
            raise 