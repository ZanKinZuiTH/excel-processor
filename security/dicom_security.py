"""
ระบบรักษาความปลอดภัยสำหรับข้อมูล DICOM
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import logging
import json
from datetime import datetime
import hashlib
import shutil

class DicomSecurity:
    """ระบบรักษาความปลอดภัยสำหรับข้อมูล DICOM"""
    
    def __init__(self, security_config_path: Path):
        """
        กำหนดค่าเริ่มต้นสำหรับ DicomSecurity
        
        Args:
            security_config_path: พาธของไฟล์ตั้งค่าความปลอดภัย
        """
        self.config_path = security_config_path
        self.logger = logging.getLogger(__name__)
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """โหลดการตั้งค่าความปลอดภัย"""
        if not self.config_path.exists():
            default_config = {
                "encryption_enabled": True,
                "anonymization_enabled": True,
                "access_log_enabled": True,
                "backup_enabled": True,
                "backup_interval_days": 7,
                "allowed_users": []
            }
            self._save_config(default_config)
            return default_config
            
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการโหลดการตั้งค่า: {e}")
            return {}
            
    def _save_config(self, config: Dict[str, Any]):
        """บันทึกการตั้งค่าความปลอดภัย"""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการบันทึกการตั้งค่า: {e}")
            
    def anonymize_dicom(self, dicom_path: Path, output_path: Optional[Path] = None) -> Optional[Path]:
        """
        ลบข้อมูลส่วนตัวออกจากไฟล์ DICOM
        
        Args:
            dicom_path: พาธของไฟล์ DICOM ต้นฉบับ
            output_path: พาธสำหรับบันทึกไฟล์ที่ลบข้อมูลแล้ว (ถ้าไม่ระบุจะใช้ชื่อไฟล์เดิมต่อท้ายด้วย _anon)
            
        Returns:
            Optional[Path]: พาธของไฟล์ที่ลบข้อมูลแล้ว หรือ None ถ้าไม่สำเร็จ
        """
        if not self.config.get("anonymization_enabled", False):
            self.logger.warning("การลบข้อมูลส่วนตัวถูกปิดใช้งาน")
            return None
            
        try:
            import pydicom
            ds = pydicom.dcmread(str(dicom_path))
            
            # ลบข้อมูลส่วนตัว
            sensitive_tags = [
                "PatientName",
                "PatientID",
                "PatientBirthDate",
                "PatientAddress",
                "PatientPhone"
            ]
            
            for tag in sensitive_tags:
                if hasattr(ds, tag):
                    setattr(ds, tag, "ANONYMOUS")
                    
            # กำหนดพาธสำหรับบันทึก
            if output_path is None:
                output_path = dicom_path.parent / f"{dicom_path.stem}_anon{dicom_path.suffix}"
                
            ds.save_as(str(output_path))
            self.logger.info(f"ลบข้อมูลส่วนตัวจากไฟล์ {dicom_path.name} สำเร็จ")
            return output_path
            
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการลบข้อมูลส่วนตัว: {e}")
            return None
            
    def backup_dicom(self, dicom_path: Path, backup_dir: Path) -> bool:
        """
        สำรองข้อมูลไฟล์ DICOM
        
        Args:
            dicom_path: พาธของไฟล์ DICOM
            backup_dir: โฟลเดอร์สำหรับเก็บไฟล์สำรอง
            
        Returns:
            bool: True ถ้าสำรองข้อมูลสำเร็จ, False ถ้าไม่สำเร็จ
        """
        if not self.config.get("backup_enabled", False):
            self.logger.warning("การสำรองข้อมูลถูกปิดใช้งาน")
            return False
            
        try:
            if not backup_dir.exists():
                backup_dir.mkdir(parents=True)
                
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = backup_dir / f"{dicom_path.stem}_{timestamp}{dicom_path.suffix}"
            
            shutil.copy2(dicom_path, backup_path)
            self.logger.info(f"สำรองข้อมูลไฟล์ {dicom_path.name} สำเร็จ")
            return True
            
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการสำรองข้อมูล: {e}")
            return False
            
    def check_file_integrity(self, dicom_path: Path, stored_hash: Optional[str] = None) -> bool:
        """
        ตรวจสอบความถูกต้องของไฟล์ DICOM
        
        Args:
            dicom_path: พาธของไฟล์ DICOM
            stored_hash: แฮชที่เก็บไว้สำหรับเปรียบเทียบ (ถ้ามี)
            
        Returns:
            bool: True ถ้าไฟล์ถูกต้อง, False ถ้าไม่ถูกต้อง
        """
        try:
            with open(dicom_path, "rb") as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
                
            if stored_hash is None:
                return True
                
            is_valid = file_hash == stored_hash
            if not is_valid:
                self.logger.warning(f"พบความไม่ถูกต้องของไฟล์ {dicom_path.name}")
            return is_valid
            
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการตรวจสอบความถูกต้องของไฟล์: {e}")
            return False
            
    def log_access(self, user: str, action: str, file_path: Path):
        """
        บันทึกการเข้าถึงไฟล์ DICOM
        
        Args:
            user: ชื่อผู้ใช้
            action: การกระทำ (เช่น view, edit, delete)
            file_path: พาธของไฟล์ที่ถูกเข้าถึง
        """
        if not self.config.get("access_log_enabled", False):
            return
            
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user,
            "action": action,
            "file": str(file_path),
            "success": True
        }
        
        try:
            log_file = self.config_path.parent / "access_log.json"
            logs = []
            
            if log_file.exists():
                with open(log_file, "r", encoding="utf-8") as f:
                    logs = json.load(f)
                    
            logs.append(log_entry)
            
            with open(log_file, "w", encoding="utf-8") as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการบันทึกการเข้าถึง: {e}")
            
    def update_security_settings(self, updates: Dict[str, Any]) -> bool:
        """
        อัปเดตการตั้งค่าความปลอดภัย
        
        Args:
            updates: การตั้งค่าที่ต้องการอัปเดต
            
        Returns:
            bool: True ถ้าอัปเดตสำเร็จ, False ถ้าไม่สำเร็จ
        """
        try:
            self.config.update(updates)
            self._save_config(self.config)
            self.logger.info("อัปเดตการตั้งค่าความปลอดภัยสำเร็จ")
            return True
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการอัปเดตการตั้งค่าความปลอดภัย: {e}")
            return False 