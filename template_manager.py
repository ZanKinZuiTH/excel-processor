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
from openpyxl import Workbook
from pathlib import Path
import shutil
from Levenshtein import distance
from fuzzywuzzy import fuzz

class TemplateLibrary:
    """คลาสสำหรับจัดการเทมเพลตสำเร็จรูป"""
    
    def __init__(self):
        self.templates_dir = "templates/builtin"
        os.makedirs(self.templates_dir, exist_ok=True)
        self.load_builtin_templates()
        
    def load_builtin_templates(self):
        """โหลดเทมเพลตสำเร็จรูปที่มีมาให้"""
        builtin_templates = {
            "invoice": {
                "name": "ใบแจ้งหนี้",
                "description": "เทมเพลตสำหรับออกใบแจ้งหนี้มาตรฐาน",
                "file": "invoice_template.xlsx"
            },
            "personal_info": {
                "name": "ข้อมูลส่วนบุคคล",
                "description": "เทมเพลตสำหรับกรอกข้อมูลส่วนบุคคล",
                "file": "personal_info_template.xlsx"
            },
            "employee": {
                "name": "ข้อมูลพนักงาน",
                "description": "เทมเพลตสำหรับบันทึกข้อมูลพนักงาน",
                "file": "employee_template.xlsx"
            }
        }
        
        for key, template in builtin_templates.items():
            template_path = os.path.join(self.templates_dir, template["file"])
            if not os.path.exists(template_path):
                # สร้างเทมเพลตเปล่าถ้ายังไม่มี
                wb = Workbook()
                wb.save(template_path)
                
    def get_builtin_template(self, template_key: str) -> Optional[str]:
        """ดึงพาธของเทมเพลตสำเร็จรูป"""
        template_path = os.path.join(self.templates_dir, f"{template_key}_template.xlsx")
        return template_path if os.path.exists(template_path) else None

class TemplateManager:
    """คลาสสำหรับจัดการเทมเพลต Excel
    
    สำหรับนักศึกษา:
    1. ศึกษาการออกแบบคลาสและเมธอด
    2. สังเกตการใช้ Type Hints
    3. การจัดการไฟล์และข้อมูล
    """
    
    def __init__(self):
        """กำหนดค่าเริ่มต้นสำหรับระบบ"""
        self.templates_dir = Path("templates")
        self.templates_dir.mkdir(exist_ok=True)
        self.data_dir = "data"
        self.preview_dir = "previews"
        self.template_library = TemplateLibrary()
        
        # สร้างโฟลเดอร์ที่จำเป็น
        for directory in [self.templates_dir, self.data_dir, self.preview_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
        
        # ตั้งค่า logging
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
    
    def setup_logging(self):
        """ตั้งค่า logging"""
        handler = logging.FileHandler("template_manager.log")
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def is_ready(self) -> bool:
        """ตรวจสอบว่าระบบพร้อมใช้งานหรือไม่"""
        try:
            return (
                self.templates_dir.exists() and
                self.templates_dir.is_dir() and
                os.access(self.templates_dir, os.R_OK | os.W_OK)
            )
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการตรวจสอบความพร้อม: {str(e)}")
            return False
    
    def check_database_connection(self) -> bool:
        """ตรวจสอบการเชื่อมต่อฐานข้อมูล"""
        try:
            # TODO: เพิ่มการตรวจสอบการเชื่อมต่อฐานข้อมูลจริง
            return True
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการเชื่อมต่อฐานข้อมูล: {str(e)}")
            return False
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """ดึงรายการเทมเพลตทั้งหมด"""
        try:
            templates = []
            for file in self.templates_dir.glob("*.json"):
                if not file.name.endswith("_versions.json"):
                    with open(file, "r", encoding="utf-8") as f:
                        template = json.load(f)
                        templates.append(template)
            return templates
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการดึงรายการเทมเพลต: {str(e)}")
            return []
    
    def process_with_template(self, template_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """ประมวลผลข้อมูลด้วยเทมเพลต"""
        try:
            template = self.get_template(template_id)
            if not template:
                raise ValueError(f"ไม่พบเทมเพลต {template_id}")

            # ตรวจสอบและแปลงข้อมูลตามโครงสร้างเทมเพลต
            processed_data = {}
            for field, field_type in template["structure"].items():
                if field in data:
                    # แปลงประเภทข้อมูลตามที่กำหนดในเทมเพลต
                    if field_type == "number":
                        processed_data[field] = float(data[field])
                    elif field_type == "date":
                        processed_data[field] = datetime.fromisoformat(data[field])
                    else:
                        processed_data[field] = data[field]

            return {
                "status": "success",
                "data": processed_data,
                "template_used": template_id
            }
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการประมวลผลด้วยเทมเพลต: {str(e)}")
            raise
    
    def backup_template(self, template_id: str) -> bool:
        """สำรองข้อมูลเทมเพลต"""
        try:
            template_file = self.templates_dir / f"{template_id}.json"
            if not template_file.exists():
                return False

            backup_dir = self.templates_dir / "backups"
            backup_dir.mkdir(exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = backup_dir / f"{template_id}_{timestamp}.json"

            shutil.copy2(template_file, backup_file)
            self.logger.info(f"สำรองเทมเพลต {template_id} ไปยัง {backup_file}")
            return True
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการสำรองเทมเพลต: {str(e)}")
            return False
    
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
    
    def suggest_template(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """แนะนำเทมเพลตที่เหมาะสมกับข้อมูล
        
        Args:
            data: ข้อมูลที่ต้องการหาเทมเพลตที่เหมาะสม
            
        Returns:
            List[Dict[str, Any]]: รายการเทมเพลตที่แนะนำพร้อมคะแนนความเหมาะสม
        """
        suggestions = []
        
        # ดึงรายการเทมเพลตทั้งหมด
        all_templates = self.list_templates()
        
        for template in all_templates:
            score = self._calculate_template_match_score(template, data)
            if score > 0:
                suggestions.append({
                    "template_id": template["id"],
                    "name": template["name"],
                    "description": template["description"],
                    "match_score": score,
                    "matching_fields": self._get_matching_fields(template, data)
                })
        
        # เรียงลำดับตามคะแนน
        suggestions.sort(key=lambda x: x["match_score"], reverse=True)
        return suggestions
        
    def _calculate_template_match_score(self, template: Dict[str, Any], data: Dict[str, Any]) -> float:
        """คำนวณคะแนนความเหมาะสมระหว่างเทมเพลตกับข้อมูล"""
        score = 0.0
        template_fields = self._extract_template_fields(template)
        data_fields = self._extract_data_fields(data)
        
        # คำนวณคะแนนจากจำนวนฟิลด์ที่ตรงกัน
        matching_fields = set(template_fields) & set(data_fields)
        if len(template_fields) > 0:
            score = len(matching_fields) / len(template_fields)
            
        # เพิ่มคะแนนจากความคล้ายคลึงของชื่อฟิลด์
        for tf in template_fields:
            for df in data_fields:
                if self._calculate_field_similarity(tf, df) > 0.8:  # ความคล้ายคลึงมากกว่า 80%
                    score += 0.1
                    
        return min(score, 1.0)  # คะแนนสูงสุดคือ 1.0
        
    def _extract_template_fields(self, template: Dict[str, Any]) -> List[str]:
        """ดึงรายการฟิลด์จากเทมเพลต"""
        fields = []
        if "structure" in template:
            for sheet in template["structure"].values():
                if "fields" in sheet:
                    fields.extend(sheet["fields"])
        return fields
        
    def _extract_data_fields(self, data: Dict[str, Any]) -> List[str]:
        """ดึงรายการฟิลด์จากข้อมูล"""
        fields = []
        for key, value in data.items():
            if isinstance(value, dict):
                fields.extend(self._extract_data_fields(value))
            else:
                fields.append(key)
        return fields
        
    def _calculate_field_similarity(self, field1: str, field2: str) -> float:
        """คำนวณความคล้ายคลึงระหว่างชื่อฟิลด์"""
        # ใช้ Levenshtein distance
        from difflib import SequenceMatcher
        return SequenceMatcher(None, field1.lower(), field2.lower()).ratio()
        
    def _get_matching_fields(self, template: Dict[str, Any], data: Dict[str, Any]) -> List[str]:
        """หาฟิลด์ที่ตรงกันระหว่างเทมเพลตกับข้อมูล"""
        template_fields = self._extract_template_fields(template)
        data_fields = self._extract_data_fields(data)
        return list(set(template_fields) & set(data_fields))
    
    def share_template(self, template_id: str, user_ids: List[str], permissions: Dict[str, bool] = None) -> Dict[str, Any]:
        """แชร์เทมเพลตให้กับผู้ใช้อื่น
        
        Args:
            template_id: ID ของเทมเพลต
            user_ids: รายการ ID ของผู้ใช้ที่ต้องการแชร์
            permissions: สิทธิ์การใช้งาน (อ่าน, แก้ไข, ลบ)
            
        Returns:
            Dict[str, Any]: ข้อมูลการแชร์
        """
        try:
            # ตั้งค่าสิทธิ์เริ่มต้น
            default_permissions = {
                "read": True,
                "edit": False,
                "delete": False
            }
            permissions = permissions or default_permissions
            
            # บันทึกข้อมูลการแชร์
            share_data = {
                "template_id": template_id,
                "shared_with": [
                    {
                        "user_id": user_id,
                        "permissions": permissions,
                        "shared_at": datetime.now().isoformat()
                    }
                    for user_id in user_ids
                ]
            }
            
            # บันทึกลงไฟล์
            share_file = os.path.join(self.templates_dir, f"{template_id}_shares.json")
            if os.path.exists(share_file):
                with open(share_file, 'r', encoding='utf-8') as f:
                    existing_shares = json.load(f)
                # อัพเดทข้อมูลการแชร์
                existing_users = {share["user_id"] for share in existing_shares["shared_with"]}
                new_shares = [
                    share for share in share_data["shared_with"]
                    if share["user_id"] not in existing_users
                ]
                existing_shares["shared_with"].extend(new_shares)
                share_data = existing_shares
            
            with open(share_file, 'w', encoding='utf-8') as f:
                json.dump(share_data, f, ensure_ascii=False, indent=2)
                
            self.logger.info(f"แชร์เทมเพลต {template_id} กับผู้ใช้ {len(user_ids)} คน")
            return share_data
            
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการแชร์เทมเพลต: {str(e)}")
            raise
            
    def get_shared_templates(self, user_id: str) -> List[Dict[str, Any]]:
        """ดึงรายการเทมเพลตที่ถูกแชร์กับผู้ใช้
        
        Args:
            user_id: ID ของผู้ใช้
            
        Returns:
            List[Dict[str, Any]]: รายการเทมเพลตที่ถูกแชร์
        """
        shared_templates = []
        
        # ค้นหาไฟล์การแชร์ทั้งหมด
        for file_name in os.listdir(self.templates_dir):
            if file_name.endswith('_shares.json'):
                share_file = os.path.join(self.templates_dir, file_name)
                template_id = file_name.replace('_shares.json', '')
                
                with open(share_file, 'r', encoding='utf-8') as f:
                    share_data = json.load(f)
                    
                # ตรวจสอบว่าผู้ใช้มีสิทธิ์ในเทมเพลตนี้หรือไม่
                for share in share_data["shared_with"]:
                    if share["user_id"] == user_id:
                        template = self.get_template(template_id)
                        if template:
                            template["permissions"] = share["permissions"]
                            shared_templates.append(template)
                            break
                            
        return shared_templates
        
    def revoke_share(self, template_id: str, user_ids: List[str]) -> bool:
        """ยกเลิกการแชร์เทมเพลต
        
        Args:
            template_id: ID ของเทมเพลต
            user_ids: รายการ ID ของผู้ใช้ที่ต้องการยกเลิกการแชร์
            
        Returns:
            bool: True ถ้าสำเร็จ
        """
        try:
            share_file = os.path.join(self.templates_dir, f"{template_id}_shares.json")
            if not os.path.exists(share_file):
                return False
                
            with open(share_file, 'r', encoding='utf-8') as f:
                share_data = json.load(f)
                
            # ลบข้อมูลการแชร์ของผู้ใช้ที่ระบุ
            share_data["shared_with"] = [
                share for share in share_data["shared_with"]
                if share["user_id"] not in user_ids
            ]
            
            with open(share_file, 'w', encoding='utf-8') as f:
                json.dump(share_data, f, ensure_ascii=False, indent=2)
                
            self.logger.info(f"ยกเลิกการแชร์เทมเพลต {template_id} กับผู้ใช้ {len(user_ids)} คน")
            return True
            
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการยกเลิกการแชร์เทมเพลต: {str(e)}")
            return False
            
    def create_template_version(self, template_id: str, changes: Dict[str, Any], version_note: str = "") -> str:
        """สร้างเวอร์ชันใหม่ของเทมเพลต
        
        Args:
            template_id: ID ของเทมเพลต
            changes: การเปลี่ยนแปลงที่จะบันทึก
            version_note: บันทึกการเปลี่ยนแปลง
            
        Returns:
            str: ID ของเวอร์ชันใหม่
        """
        try:
            # สร้าง ID เวอร์ชันใหม่
            version_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # ดึงข้อมูลเทมเพลตปัจจุบัน
            template = self.get_template(template_id)
            if not template:
                raise ValueError(f"ไม่พบเทมเพลต {template_id}")
                
            # สร้างข้อมูลเวอร์ชัน
            version_data = {
                "version_id": version_id,
                "template_id": template_id,
                "changes": changes,
                "version_note": version_note,
                "created_at": datetime.now().isoformat(),
                "template_data": template
            }
            
            # บันทึกเวอร์ชันใหม่
            versions_dir = os.path.join(self.templates_dir, f"{template_id}_versions")
            os.makedirs(versions_dir, exist_ok=True)
            
            version_file = os.path.join(versions_dir, f"{version_id}.json")
            with open(version_file, 'w', encoding='utf-8') as f:
                json.dump(version_data, f, ensure_ascii=False, indent=2)
                
            self.logger.info(f"สร้างเวอร์ชันใหม่ {version_id} สำหรับเทมเพลต {template_id}")
            return version_id
            
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการสร้างเวอร์ชันเทมเพลต: {str(e)}")
            raise
            
    def list_template_versions(self, template_id: str) -> List[Dict[str, Any]]:
        """ดึงรายการเวอร์ชันของเทมเพลต
        
        Args:
            template_id: ID ของเทมเพลต
            
        Returns:
            List[Dict[str, Any]]: รายการเวอร์ชันทั้งหมด
        """
        versions = []
        versions_dir = os.path.join(self.templates_dir, f"{template_id}_versions")
        
        if os.path.exists(versions_dir):
            for file_name in os.listdir(versions_dir):
                if file_name.endswith('.json'):
                    version_file = os.path.join(versions_dir, file_name)
                    with open(version_file, 'r', encoding='utf-8') as f:
                        version_data = json.load(f)
                        versions.append({
                            "version_id": version_data["version_id"],
                            "created_at": version_data["created_at"],
                            "version_note": version_data["version_note"],
                            "changes": version_data["changes"]
                        })
                        
        # เรียงตามเวลาจากใหม่ไปเก่า
        versions.sort(key=lambda x: x["created_at"], reverse=True)
        return versions
        
    def restore_template_version(self, template_id: str, version_id: str) -> bool:
        """กู้คืนเทมเพลตไปยังเวอร์ชันที่ระบุ
        
        Args:
            template_id: ID ของเทมเพลต
            version_id: ID ของเวอร์ชันที่ต้องการกู้คืน
            
        Returns:
            bool: True ถ้าสำเร็จ
        """
        try:
            # ดึงข้อมูลเวอร์ชันที่ต้องการ
            version_file = os.path.join(
                self.templates_dir,
                f"{template_id}_versions",
                f"{version_id}.json"
            )
            
            if not os.path.exists(version_file):
                raise ValueError(f"ไม่พบเวอร์ชัน {version_id}")
                
            with open(version_file, 'r', encoding='utf-8') as f:
                version_data = json.load(f)
                
            # บันทึกเวอร์ชันปัจจุบันก่อนกู้คืน
            current_template = self.get_template(template_id)
            if current_template:
                self.create_template_version(
                    template_id,
                    {"action": "backup_before_restore", "restored_to": version_id},
                    "สำรองข้อมูลก่อนกู้คืนเวอร์ชัน"
                )
                
            # กู้คืนข้อมูลเทมเพลต
            template_file = os.path.join(self.templates_dir, f"{template_id}.json")
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(version_data["template_data"], f, ensure_ascii=False, indent=2)
                
            self.logger.info(f"กู้คืนเทมเพลต {template_id} ไปยังเวอร์ชัน {version_id} สำเร็จ")
            return True
            
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการกู้คืนเวอร์ชันเทมเพลต: {str(e)}")
            return False
            
    def compare_template_versions(self, template_id: str, version_id1: str, version_id2: str) -> Dict[str, Any]:
        """เปรียบเทียบความแตกต่างระหว่างสองเวอร์ชัน
        
        Args:
            template_id: ID ของเทมเพลต
            version_id1: ID ของเวอร์ชันที่ 1
            version_id2: ID ของเวอร์ชันที่ 2
            
        Returns:
            Dict[str, Any]: ข้อมูลความแตกต่าง
        """
        try:
            # ดึงข้อมูลทั้งสองเวอร์ชัน
            versions_dir = os.path.join(self.templates_dir, f"{template_id}_versions")
            
            version1_file = os.path.join(versions_dir, f"{version_id1}.json")
            version2_file = os.path.join(versions_dir, f"{version_id2}.json")
            
            if not os.path.exists(version1_file) or not os.path.exists(version2_file):
                raise ValueError("ไม่พบเวอร์ชันที่ระบุ")
                
            with open(version1_file, 'r', encoding='utf-8') as f:
                version1_data = json.load(f)
            with open(version2_file, 'r', encoding='utf-8') as f:
                version2_data = json.load(f)
                
            # เปรียบเทียบความแตกต่าง
            differences = {
                "fields_added": [],
                "fields_removed": [],
                "fields_modified": [],
                "structure_changes": []
            }
            
            v1_fields = self._extract_template_fields(version1_data["template_data"])
            v2_fields = self._extract_template_fields(version2_data["template_data"])
            
            differences["fields_added"] = list(set(v2_fields) - set(v1_fields))
            differences["fields_removed"] = list(set(v1_fields) - set(v2_fields))
            
            # ตรวจสอบการเปลี่ยนแปลงในฟิลด์ที่มีอยู่
            common_fields = set(v1_fields) & set(v2_fields)
            for field in common_fields:
                v1_value = self._get_field_value(version1_data["template_data"], field)
                v2_value = self._get_field_value(version2_data["template_data"], field)
                if v1_value != v2_value:
                    differences["fields_modified"].append({
                        "field": field,
                        "old_value": v1_value,
                        "new_value": v2_value
                    })
                    
            return differences
            
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการเปรียบเทียบเวอร์ชัน: {str(e)}")
            raise
            
    def _get_field_value(self, template_data: Dict[str, Any], field: str) -> Any:
        """ดึงค่าของฟิลด์จากเทมเพลต"""
        if "structure" in template_data:
            for sheet in template_data["structure"].values():
                if "fields" in sheet and field in sheet["fields"]:
                    return sheet.get("field_properties", {}).get(field)
        return None 