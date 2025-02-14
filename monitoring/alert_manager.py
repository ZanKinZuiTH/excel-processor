"""
ระบบจัดการการแจ้งเตือน (Alert Manager)

สำหรับนักศึกษา:
1. ศึกษาการส่งการแจ้งเตือนผ่านช่องทางต่างๆ
2. เรียนรู้การจัดการประวัติการแจ้งเตือน
3. ทำความเข้าใจการตั้งค่าการแจ้งเตือน
"""

import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
from dataclasses import dataclass, asdict
from enum import Enum

# ตั้งค่า logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AlertLevel(Enum):
    """ระดับความสำคัญของการแจ้งเตือน"""
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"

@dataclass
class AlertConfig:
    """การตั้งค่าการแจ้งเตือน"""
    # Line Notify
    line_token: Optional[str] = None
    
    # Email
    smtp_host: Optional[str] = None
    smtp_port: Optional[int] = None
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    from_email: Optional[str] = None
    
    # Slack
    slack_webhook: Optional[str] = None
    
    # ตั้งค่าทั่วไป
    alert_history_limit: int = 1000
    batch_size: int = 10
    retry_count: int = 3
    retry_delay: int = 5

class AlertManager:
    def __init__(self, config_path: Optional[str] = None):
        """
        เริ่มต้นระบบจัดการการแจ้งเตือน
        
        Args:
            config_path: พาธของไฟล์ตั้งค่า (ถ้ามี)
        """
        self.config = self._load_config(config_path)
        self.alert_history: List[Dict] = []
        logger.info("เริ่มต้นระบบจัดการการแจ้งเตือน")
    
    def _load_config(self, config_path: Optional[str]) -> AlertConfig:
        """โหลดการตั้งค่าจากไฟล์"""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                return AlertConfig(**config_data)
        return AlertConfig()
    
    def send_line_notification(self, message: str) -> bool:
        """
        ส่งการแจ้งเตือนผ่าน Line Notify
        
        Args:
            message: ข้อความที่ต้องการส่ง
            
        Returns:
            bool: True ถ้าส่งสำเร็จ
        """
        if not self.config.line_token:
            logger.warning("ไม่ได้ตั้งค่า Line Token")
            return False
        
        try:
            response = requests.post(
                'https://notify-api.line.me/api/notify',
                headers={'Authorization': f'Bearer {self.config.line_token}'},
                data={'message': message}
            )
            if response.status_code == 200:
                logger.info(f"ส่งการแจ้งเตือน Line สำเร็จ: {message}")
                return True
            else:
                logger.error(f"ส่งการแจ้งเตือน Line ไม่สำเร็จ: {response.text}")
                return False
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการส่งการแจ้งเตือน Line: {str(e)}")
            return False
    
    def send_email_notification(
        self,
        subject: str,
        message: str,
        to_email: str
    ) -> bool:
        """
        ส่งการแจ้งเตือนผ่าน Email
        
        Args:
            subject: หัวข้อ
            message: เนื้อหา
            to_email: อีเมลผู้รับ
            
        Returns:
            bool: True ถ้าส่งสำเร็จ
        """
        if not all([
            self.config.smtp_host,
            self.config.smtp_port,
            self.config.smtp_username,
            self.config.smtp_password,
            self.config.from_email
        ]):
            logger.warning("ไม่ได้ตั้งค่า SMTP")
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain', 'utf-8'))
            
            with smtplib.SMTP(self.config.smtp_host, self.config.smtp_port) as server:
                server.starttls()
                server.login(self.config.smtp_username, self.config.smtp_password)
                server.send_message(msg)
            
            logger.info(f"ส่งอีเมลสำเร็จถึง {to_email}")
            return True
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการส่งอีเมล: {str(e)}")
            return False
    
    def send_slack_notification(self, message: str) -> bool:
        """
        ส่งการแจ้งเตือนผ่าน Slack
        
        Args:
            message: ข้อความที่ต้องการส่ง
            
        Returns:
            bool: True ถ้าส่งสำเร็จ
        """
        if not self.config.slack_webhook:
            logger.warning("ไม่ได้ตั้งค่า Slack Webhook")
            return False
        
        try:
            response = requests.post(
                self.config.slack_webhook,
                json={'text': message}
            )
            if response.status_code == 200:
                logger.info(f"ส่งการแจ้งเตือน Slack สำเร็จ: {message}")
                return True
            else:
                logger.error(f"ส่งการแจ้งเตือน Slack ไม่สำเร็จ: {response.text}")
                return False
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการส่งการแจ้งเตือน Slack: {str(e)}")
            return False
    
    def send_alert(
        self,
        level: AlertLevel,
        title: str,
        message: str,
        channels: List[str]
    ) -> Dict[str, bool]:
        """
        ส่งการแจ้งเตือนไปยังหลายช่องทาง
        
        Args:
            level: ระดับความสำคัญ
            title: หัวข้อ
            message: เนื้อหา
            channels: รายการช่องทางที่ต้องการส่ง
            
        Returns:
            Dict[str, bool]: ผลการส่งแต่ละช่องทาง
        """
        results = {}
        formatted_message = f"[{level.value}] {title}\n{message}"
        
        for channel in channels:
            if channel == 'line':
                results['line'] = self.send_line_notification(formatted_message)
            elif channel == 'email':
                results['email'] = self.send_email_notification(
                    title,
                    message,
                    self.config.smtp_username
                )
            elif channel == 'slack':
                results['slack'] = self.send_slack_notification(formatted_message)
        
        # เก็บประวัติ
        self.alert_history.append({
            'timestamp': datetime.now().isoformat(),
            'level': level.value,
            'title': title,
            'message': message,
            'channels': channels,
            'results': results
        })
        
        # จำกัดขนาดประวัติ
        if len(self.alert_history) > self.config.alert_history_limit:
            self.alert_history = self.alert_history[-self.config.alert_history_limit:]
        
        return results
    
    def get_alert_history(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        level: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        ดึงประวัติการแจ้งเตือน
        
        Args:
            start_date: วันที่เริ่มต้น
            end_date: วันที่สิ้นสุด
            level: ระดับความสำคัญ
            
        Returns:
            List[Dict]: รายการประวัติการแจ้งเตือน
        """
        alerts = self.alert_history
        
        if start_date:
            alerts = [
                a for a in alerts
                if datetime.fromisoformat(a['timestamp']) >= start_date
            ]
        
        if end_date:
            alerts = [
                a for a in alerts
                if datetime.fromisoformat(a['timestamp']) <= end_date
            ]
        
        if level:
            alerts = [a for a in alerts if a['level'] == level]
        
        return alerts
    
    def clear_alert_history(self):
        """ล้างประวัติการแจ้งเตือน"""
        self.alert_history.clear()
        logger.info("ล้างประวัติการแจ้งเตือนเรียบร้อย") 