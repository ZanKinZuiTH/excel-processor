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

class TemplateManager:
    """คลาสสำหรับจัดการเทมเพลต Excel"""
    
    def __init__(self):
        """กำหนดค่าเริ่มต้น"""
        self.templates_dir = Path("templates")
        self.templates_dir.mkdir(exist_ok=True)
        self.metadata_file = self.templates_dir / "metadata.json"
        self.load_metadata()
        
    def load_metadata(self):
        """โหลดข้อมูล metadata ของเทมเพลต"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {}
            self.save_metadata()
            
    def save_metadata(self):
        """บันทึกข้อมูล metadata ของเทมเพลต"""
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)
            
    def add_template(self, name: str, description: str, file_path: str) -> bool:
        """
        เพิ่มเทมเพลตใหม่
        
        Args:
            name: ชื่อเทมเพลต
            description: คำอธิบายเทมเพลต
            file_path: พาธของไฟล์เทมเพลต
            
        Returns:
            bool: True ถ้าเพิ่มสำเร็จ False ถ้าไม่สำเร็จ
        """
        if not os.path.exists(file_path):
            return False
            
        template_id = str(len(self.metadata) + 1)
        dest_path = self.templates_dir / f"{template_id}.xlsx"
        
        try:
            shutil.copy2(file_path, dest_path)
            self.metadata[template_id] = {
                "name": name,
                "description": description,
                "created_at": datetime.now().isoformat()
            }
            self.save_metadata()
            return True
        except Exception as e:
            logging.error(f"เกิดข้อผิดพลาดในการเพิ่มเทมเพลต: {e}")
            return False
            
    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """
        ดึงข้อมูลเทมเพลต
        
        Args:
            template_id: รหัสเทมเพลต
            
        Returns:
            Dict หรือ None: ข้อมูลเทมเพลตหรือ None ถ้าไม่พบ
        """
        if template_id not in self.metadata:
            return None
            
        template_path = self.templates_dir / f"{template_id}.xlsx"
        if not template_path.exists():
            return None
            
        return {
            **self.metadata[template_id],
            "path": str(template_path)
        }
        
    def search_templates(self, query: str) -> List[Dict[str, Any]]:
        """
        ค้นหาเทมเพลต
        
        Args:
            query: คำค้นหา
            
        Returns:
            List[Dict]: รายการเทมเพลตที่ตรงกับคำค้นหา
        """
        results = []
        for template_id, data in self.metadata.items():
            name_score = fuzz.partial_ratio(query.lower(), data["name"].lower())
            desc_score = fuzz.partial_ratio(query.lower(), data["description"].lower())
            score = max(name_score, desc_score)
            
            if score > 60:  # threshold สำหรับความเหมือน
                results.append({
                    "id": template_id,
                    **data,
                    "score": score
                })
                
        return sorted(results, key=lambda x: x["score"], reverse=True)
