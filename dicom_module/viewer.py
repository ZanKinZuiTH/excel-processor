"""
ระบบจัดการการแสดงผลภาพ DICOM
"""

from pathlib import Path
import subprocess
import platform
import logging
from typing import Optional

class DicomViewer:
    """ระบบจัดการการแสดงผลภาพ DICOM"""
    
    def __init__(self, base_path: Path):
        """
        กำหนดค่าเริ่มต้นสำหรับ DicomViewer
        
        Args:
            base_path: Path ที่ตั้งของโปรแกรม DICOM Viewer
        """
        self.base_path = Path(base_path)
        self.viewer_path = self._get_viewer_path()
        self.logger = logging.getLogger(__name__)
        
        # ตั้งค่า logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
    def _get_viewer_path(self) -> Path:
        """
        เลือก path ของ viewer ตามระบบปฏิบัติการ
        
        Returns:
            Path: พาธของโปรแกรม DICOM Viewer
        """
        is_64bit = platform.machine().endswith('64')
        viewer_dir = "x64" if is_64bit else "Win32"
        return self.base_path / viewer_dir / "mdicom.exe"
        
    def view_image(self, image_path: Optional[Path] = None) -> bool:
        """
        เปิดดูภาพ DICOM
        
        Args:
            image_path: พาธของไฟล์หรือโฟลเดอร์ที่ต้องการเปิด
            
        Returns:
            bool: True ถ้าเปิดสำเร็จ, False ถ้าเกิดข้อผิดพลาด
        """
        try:
            if not self.viewer_path.exists():
                raise FileNotFoundError(f"ไม่พบโปรแกรม DICOM Viewer ที่: {self.viewer_path}")
                
            cmd = [str(self.viewer_path)]
            if image_path:
                if not image_path.exists():
                    raise FileNotFoundError(f"ไม่พบไฟล์หรือโฟลเดอร์ที่: {image_path}")
                cmd.extend(["/scan", str(image_path)])
            else:
                cmd.extend(["/scan", "."])
                
            self.logger.info(f"กำลังเปิด DICOM Viewer ด้วยคำสั่ง: {' '.join(cmd)}")
            subprocess.Popen(cmd)
            self.logger.info(f"เปิดภาพ DICOM สำเร็จ: {image_path}")
            return True
            
        except FileNotFoundError as e:
            self.logger.error(f"ไม่พบไฟล์: {e}")
            return False
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการเปิดภาพ: {e}")
            return False
            
    def check_viewer(self) -> bool:
        """
        ตรวจสอบว่าโปรแกรม DICOM Viewer พร้อมใช้งานหรือไม่
        
        Returns:
            bool: True ถ้าพร้อมใช้งาน, False ถ้าไม่พร้อม
        """
        return self.viewer_path.exists() 