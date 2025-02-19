"""
ระบบติดตามการใช้งาน DICOM
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import logging
import json
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

class DicomMonitor:
    """ระบบติดตามการใช้งาน DICOM"""
    
    def __init__(self, monitor_dir: Path):
        """
        กำหนดค่าเริ่มต้นสำหรับ DicomMonitor
        
        Args:
            monitor_dir: โฟลเดอร์สำหรับเก็บข้อมูลการติดตาม
        """
        self.monitor_dir = monitor_dir
        self.logger = logging.getLogger(__name__)
        self._setup_monitoring()
        
    def _setup_monitoring(self):
        """ตั้งค่าระบบติดตาม"""
        if not self.monitor_dir.exists():
            self.monitor_dir.mkdir(parents=True)
            
        self.usage_log_path = self.monitor_dir / "usage_log.json"
        self.performance_log_path = self.monitor_dir / "performance_log.json"
        self.error_log_path = self.monitor_dir / "error_log.json"
        
        # สร้างไฟล์ log ถ้ายังไม่มี
        for log_path in [self.usage_log_path, self.performance_log_path, self.error_log_path]:
            if not log_path.exists():
                with open(log_path, "w", encoding="utf-8") as f:
                    json.dump([], f)
                    
    def log_viewer_usage(self, user: str, file_path: Path, action: str, duration: Optional[float] = None):
        """
        บันทึกการใช้งาน DICOM Viewer
        
        Args:
            user: ชื่อผู้ใช้
            file_path: พาธของไฟล์ที่เปิด
            action: การกระทำ (เช่น view, edit)
            duration: ระยะเวลาที่ใช้งาน (วินาที)
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user,
            "file": str(file_path),
            "action": action,
            "duration": duration
        }
        
        try:
            logs = self._read_log(self.usage_log_path)
            logs.append(log_entry)
            self._write_log(self.usage_log_path, logs)
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการบันทึกการใช้งาน: {e}")
            
    def log_performance(self, operation: str, execution_time: float, success: bool):
        """
        บันทึกประสิทธิภาพการทำงาน
        
        Args:
            operation: ชื่อการดำเนินการ
            execution_time: เวลาที่ใช้ (วินาที)
            success: สถานะความสำเร็จ
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "execution_time": execution_time,
            "success": success
        }
        
        try:
            logs = self._read_log(self.performance_log_path)
            logs.append(log_entry)
            self._write_log(self.performance_log_path, logs)
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการบันทึกประสิทธิภาพ: {e}")
            
    def log_error(self, error_type: str, message: str, stack_trace: Optional[str] = None):
        """
        บันทึกข้อผิดพลาด
        
        Args:
            error_type: ประเภทข้อผิดพลาด
            message: ข้อความแสดงข้อผิดพลาด
            stack_trace: รายละเอียด stack trace (ถ้ามี)
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "error_type": error_type,
            "message": message,
            "stack_trace": stack_trace
        }
        
        try:
            logs = self._read_log(self.error_log_path)
            logs.append(log_entry)
            self._write_log(self.error_log_path, logs)
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการบันทึกข้อผิดพลาด: {e}")
            
    def analyze_usage(self, days: int = 30) -> Dict[str, Any]:
        """
        วิเคราะห์การใช้งานระบบ
        
        Args:
            days: จำนวนวันย้อนหลังที่ต้องการวิเคราะห์
            
        Returns:
            Dict[str, Any]: ผลการวิเคราะห์
        """
        try:
            logs = self._read_log(self.usage_log_path)
            if not logs:
                return {}
                
            # แปลงข้อมูลเป็น DataFrame
            df = pd.DataFrame(logs)
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            
            # กรองข้อมูลตามช่วงเวลา
            start_date = datetime.now() - timedelta(days=days)
            df = df[df["timestamp"] >= start_date]
            
            if df.empty:
                return {}
                
            # วิเคราะห์ข้อมูล
            analysis = {
                "total_views": len(df[df["action"] == "view"]),
                "total_edits": len(df[df["action"] == "edit"]),
                "unique_users": df["user"].nunique(),
                "unique_files": df["file"].nunique(),
                "avg_duration": df["duration"].mean() if "duration" in df else None,
                "most_active_users": df["user"].value_counts().head(5).to_dict(),
                "most_viewed_files": df["file"].value_counts().head(5).to_dict()
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการวิเคราะห์การใช้งาน: {e}")
            return {}
            
    def generate_usage_report(self, output_path: Path, days: int = 30):
        """
        สร้างรายงานการใช้งาน
        
        Args:
            output_path: พาธสำหรับบันทึกรายงาน
            days: จำนวนวันย้อนหลังที่ต้องการวิเคราะห์
        """
        try:
            analysis = self.analyze_usage(days)
            if not analysis:
                self.logger.warning("ไม่มีข้อมูลสำหรับสร้างรายงาน")
                return
                
            # สร้างกราฟการใช้งานรายวัน
            logs = self._read_log(self.usage_log_path)
            df = pd.DataFrame(logs)
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df = df[df["timestamp"] >= datetime.now() - timedelta(days=days)]
            
            daily_usage = df.groupby(df["timestamp"].dt.date).size()
            
            plt.figure(figsize=(12, 6))
            daily_usage.plot(kind="bar")
            plt.title("การใช้งานรายวัน")
            plt.xlabel("วันที่")
            plt.ylabel("จำนวนครั้ง")
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # บันทึกรายงาน
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("รายงานการใช้งานระบบ DICOM\n")
                f.write(f"ช่วงเวลา: {days} วันย้อนหลัง\n\n")
                
                f.write(f"จำนวนการดู: {analysis['total_views']}\n")
                f.write(f"จำนวนการแก้ไข: {analysis['total_edits']}\n")
                f.write(f"จำนวนผู้ใช้: {analysis['unique_users']}\n")
                f.write(f"จำนวนไฟล์: {analysis['unique_files']}\n")
                
                if analysis['avg_duration']:
                    f.write(f"เวลาเฉลี่ยต่อครั้ง: {analysis['avg_duration']:.2f} วินาที\n\n")
                    
                f.write("ผู้ใช้ที่ใช้งานมากที่สุด:\n")
                for user, count in analysis['most_active_users'].items():
                    f.write(f"- {user}: {count} ครั้ง\n")
                    
                f.write("\nไฟล์ที่ถูกเปิดดูมากที่สุด:\n")
                for file, count in analysis['most_viewed_files'].items():
                    f.write(f"- {file}: {count} ครั้ง\n")
                    
            # บันทึกกราฟ
            plt.savefig(output_path.with_suffix(".png"))
            plt.close()
            
            self.logger.info(f"สร้างรายงานสำเร็จ: {output_path}")
            
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการสร้างรายงาน: {e}")
            
    def _read_log(self, log_path: Path) -> List[Dict[str, Any]]:
        """อ่านข้อมูลจากไฟล์ log"""
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการอ่านไฟล์ log: {e}")
            return []
            
    def _write_log(self, log_path: Path, logs: List[Dict[str, Any]]):
        """เขียนข้อมูลลงไฟล์ log"""
        try:
            with open(log_path, "w", encoding="utf-8") as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการเขียนไฟล์ log: {e}")
            
    def get_error_summary(self, days: int = 7) -> Dict[str, int]:
        """
        สรุปข้อผิดพลาดที่เกิดขึ้น
        
        Args:
            days: จำนวนวันย้อนหลังที่ต้องการวิเคราะห์
            
        Returns:
            Dict[str, int]: จำนวนข้อผิดพลาดแยกตามประเภท
        """
        try:
            logs = self._read_log(self.error_log_path)
            if not logs:
                return {}
                
            df = pd.DataFrame(logs)
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df = df[df["timestamp"] >= datetime.now() - timedelta(days=days)]
            
            return dict(Counter(df["error_type"]))
            
        except Exception as e:
            self.logger.error(f"เกิดข้อผิดพลาดในการสรุปข้อผิดพลาด: {e}")
            return {} 