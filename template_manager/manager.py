"""
ระบบจัดการเทมเพลต Excel
สำหรับนักศึกษา: ไฟล์นี้เป็นคลาสหลักในการจัดการเทมเพลต Excel
"""

import os
import pandas as pd
from datetime import datetime
import json
import logging
from typing import Dict, List, Any, Optional, Union, TypedDict
from openpyxl import Workbook
from pathlib import Path
import shutil
from Levenshtein import distance
from fuzzywuzzy import fuzz

class TemplateMetadata(TypedDict):
    """Type definition สำหรับ metadata ของเทมเพลต"""
    name: str
    description: str
    created_at: str
    
class TemplateInfo(TypedDict):
    """Type definition สำหรับข้อมูลเทมเพลต"""
    id: str
    name: str
    description: str
    created_at: str
    path: str
    score: Optional[float]

class TemplateManager:
    """คลาสสำหรับจัดการเทมเพลต Excel"""
    
    def __init__(self, templates_dir: Optional[Path] = None) -> None:
        """
        กำหนดค่าเริ่มต้น
        
        Args:
            templates_dir: ไดเรกทอรีสำหรับเก็บเทมเพลต
        """
        self.templates_dir: Path = templates_dir or Path("templates")
        self.templates_dir.mkdir(exist_ok=True)
        self.metadata_file: Path = self.templates_dir / "metadata.json"
        self.metadata: Dict[str, TemplateMetadata] = {}
        self.load_metadata()
        
    def load_metadata(self) -> None:
        """โหลดข้อมูล metadata ของเทมเพลต"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
                else:
            self.metadata = {}
            self.save_metadata()
            
    def save_metadata(self) -> None:
        """บันทึกข้อมูล metadata ของเทมเพลต"""
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)
            
    def add_template(self, name: str, description: str, file_path: Union[str, Path]) -> bool:
        """
        เพิ่มเทมเพลตใหม่
        
        Args:
            name: ชื่อเทมเพลต
            description: คำอธิบายเทมเพลต
            file_path: พาธของไฟล์เทมเพลต
            
        Returns:
            bool: True ถ้าเพิ่มสำเร็จ False ถ้าไม่สำเร็จ
            
        Raises:
            FileNotFoundError: ถ้าไม่พบไฟล์เทมเพลต
            PermissionError: ถ้าไม่มีสิทธิ์เข้าถึงไฟล์
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"ไม่พบไฟล์: {file_path}")
            
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
            
    def get_template(self, template_id: str) -> Optional[TemplateInfo]:
        """
        ดึงข้อมูลเทมเพลต
        
        Args:
            template_id: รหัสเทมเพลต
            
        Returns:
            TemplateInfo หรือ None: ข้อมูลเทมเพลตหรือ None ถ้าไม่พบ
        """
        if template_id not in self.metadata:
            return None
            
        template_path = self.templates_dir / f"{template_id}.xlsx"
        if not template_path.exists():
            return None
            
        template_data = self.metadata[template_id]
        return {
            "id": template_id,
            **template_data,
            "path": str(template_path),
            "score": None
        }
        
    def search_templates(self, query: str, threshold: float = 60.0) -> List[TemplateInfo]:
        """
        ค้นหาเทมเพลต
        
        Args:
            query: คำค้นหา
            threshold: คะแนนขั้นต่ำสำหรับการจับคู่ (0-100)
            
        Returns:
            List[TemplateInfo]: รายการเทมเพลตที่ตรงกับคำค้นหา
        """
        results: List[TemplateInfo] = []
        for template_id, data in self.metadata.items():
            name_score = fuzz.partial_ratio(query.lower(), data["name"].lower())
            desc_score = fuzz.partial_ratio(query.lower(), data["description"].lower())
            score = max(name_score, desc_score)
            
            if score > threshold:
                results.append({
                    "id": template_id,
                    **data,
                    "path": str(self.templates_dir / f"{template_id}.xlsx"),
                    "score": score
                })
                
        return sorted(results, key=lambda x: x["score"], reverse=True)
