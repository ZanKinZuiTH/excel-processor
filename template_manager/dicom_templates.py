"""
ระบบจัดการเทมเพลตสำหรับ DICOM
"""

from pathlib import Path
from typing import Dict, Any, Optional
import json
import logging

class DicomTemplateManager:
    """ระบบจัดการเทมเพลต DICOM"""
    
    def __init__(self, template_dir: Path):
        """
        กำหนดค่าเริ่มต้นสำหรับ DicomTemplateManager
        
        Args:
            template_dir: โฟลเดอร์ที่เก็บไฟล์เทมเพลต
        """
        self.template_dir = template_dir
        self.logger = logging.getLogger(__name__)
        self.templates: Dict[str, Dict[str, Any]] = {}
        self._load_templates()
        
    def _load_templates(self):
        """โหลดเทมเพลตทั้งหมดจากไฟล์"""
        if not self.template_dir.exists():
            self.template_dir.mkdir(parents=True)
            return
            
        for file in self.template_dir.glob("*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    template = json.load(f)
                self.templates[file.stem] = template
            except Exception as e:
                self.logger.error(f"เกิดข้อผิดพลาดในการโหลดเทมเพลต {file.name}: {e}")
                
    def get_template(self, name: str) -> Optional[Dict[str, Any]]:
        """
        ดึงเทมเพลตตามชื่อ
        
        Args:
            name: ชื่อเทมเพลต
            
        Returns:
            Optional[Dict[str, Any]]: ข้อมูลเทมเพลต หรือ None ถ้าไม่พบ
        """
        return self.templates.get(name)
        
    def save_template(self, name: str, template: Dict[str, Any]):
        """
        บันทึกเทมเพลตใหม่
        
        Args:
            name: ชื่อเทมเพลต
            template: ข้อมูลเทมเพลต
        """
        file_path = self.template_dir / f"{name}.json"
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(template, f, indent=2, ensure_ascii=False)
            self.templates[name] = template
            self.logger.info(f"บันทึกเทมเพลต {name} สำเร็จ")
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการบันทึกเทมเพลต {name}: {e}")
            
    def delete_template(self, name: str) -> bool:
        """
        ลบเทมเพลต
        
        Args:
            name: ชื่อเทมเพลตที่ต้องการลบ
            
        Returns:
            bool: True ถ้าลบสำเร็จ, False ถ้าไม่สำเร็จ
        """
        file_path = self.template_dir / f"{name}.json"
        try:
            if file_path.exists():
                file_path.unlink()
                del self.templates[name]
                self.logger.info(f"ลบเทมเพลต {name} สำเร็จ")
                return True
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการลบเทมเพลต {name}: {e}")
        return False
        
    def list_templates(self) -> Dict[str, Dict[str, Any]]:
        """
        แสดงรายการเทมเพลตทั้งหมด
        
        Returns:
            Dict[str, Dict[str, Any]]: รายการเทมเพลตทั้งหมด
        """
        return self.templates.copy()
        
    def update_template(self, name: str, updates: Dict[str, Any]) -> bool:
        """
        อัปเดตเทมเพลตที่มีอยู่
        
        Args:
            name: ชื่อเทมเพลต
            updates: ข้อมูลที่ต้องการอัปเดต
            
        Returns:
            bool: True ถ้าอัปเดตสำเร็จ, False ถ้าไม่สำเร็จ
        """
        if name not in self.templates:
            self.logger.error(f"ไม่พบเทมเพลต {name}")
            return False
            
        try:
            template = self.templates[name]
            template.update(updates)
            self.save_template(name, template)
            return True
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการอัปเดตเทมเพลต {name}: {e}")
            return False 