"""
ระบบผสานการทำงานระหว่าง Excel Processor และ DICOM
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd
import logging
from dicom_module.viewer import DicomViewer

try:
    import pydicom
    PYDICOM_AVAILABLE = True
except ImportError:
    PYDICOM_AVAILABLE = False

class DicomIntegration:
    """ระบบผสานการทำงานกับ DICOM"""
    
    def __init__(self, dicom_base_path: Path):
        """
        กำหนดค่าเริ่มต้นสำหรับ DicomIntegration
        
        Args:
            dicom_base_path: Path ที่ตั้งของโปรแกรม DICOM Viewer
        """
        self.viewer = DicomViewer(dicom_base_path)
        self.logger = logging.getLogger(__name__)
        
        if not PYDICOM_AVAILABLE:
            self.logger.warning("ไม่พบ pydicom - ฟังก์ชันบางส่วนอาจไม่สามารถใช้งานได้")
            
    def extract_dicom_info(self, dicom_path: Path) -> Dict[str, Any]:
        """
        ดึงข้อมูลจากไฟล์ DICOM
        
        Args:
            dicom_path: พาธของไฟล์ DICOM
            
        Returns:
            Dict[str, Any]: ข้อมูลที่ดึงได้จากไฟล์ DICOM
        """
        if not PYDICOM_AVAILABLE:
            self.logger.error("ไม่สามารถอ่านข้อมูล DICOM ได้ - ต้องติดตั้ง pydicom ก่อน")
            return {}
            
        try:
            ds = pydicom.dcmread(str(dicom_path))
            return {
                "patient_id": getattr(ds, "PatientID", ""),
                "patient_name": str(getattr(ds, "PatientName", "")),
                "study_date": getattr(ds, "StudyDate", ""),
                "modality": getattr(ds, "Modality", ""),
                "institution": getattr(ds, "InstitutionName", ""),
                "file_path": str(dicom_path)
            }
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการอ่านข้อมูล DICOM: {e}")
            return {}
            
    def dicom_to_excel(self, dicom_folder: Path, output_path: Optional[Path] = None) -> pd.DataFrame:
        """
        แปลงข้อมูล DICOM เป็น Excel
        
        Args:
            dicom_folder: โฟลเดอร์ที่เก็บไฟล์ DICOM
            output_path: พาธสำหรับบันทึกไฟล์ Excel (ถ้าต้องการบันทึก)
            
        Returns:
            pd.DataFrame: ข้อมูล DICOM ในรูปแบบ DataFrame
        """
        if not dicom_folder.exists():
            raise FileNotFoundError(f"ไม่พบโฟลเดอร์: {dicom_folder}")
            
        data = []
        for file in dicom_folder.glob("**/*.dcm"):
            info = self.extract_dicom_info(file)
            if info:
                data.append(info)
                
        df = pd.DataFrame(data)
        
        if output_path:
            df.to_excel(output_path, index=False)
            self.logger.info(f"บันทึกข้อมูลไปยัง: {output_path}")
            
        return df
        
    def view_dicom(self, path: Path) -> bool:
        """
        เปิดดูไฟล์ DICOM
        
        Args:
            path: พาธของไฟล์หรือโฟลเดอร์ DICOM
            
        Returns:
            bool: True ถ้าเปิดสำเร็จ, False ถ้าเกิดข้อผิดพลาด
        """
        return self.viewer.view_image(path)
        
    def check_system(self) -> Dict[str, bool]:
        """
        ตรวจสอบความพร้อมของระบบ
        
        Returns:
            Dict[str, bool]: สถานะของส่วนประกอบต่างๆ
        """
        return {
            "viewer_ready": self.viewer.check_viewer(),
            "pydicom_available": PYDICOM_AVAILABLE
        } 