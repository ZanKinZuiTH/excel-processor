"""
ระบบจัดการการตั้งค่าสำหรับโปรแกรม

สำหรับนักศึกษา:
1. การใช้งาน Environment Variables:
   - ใช้ python-dotenv เพื่อโหลดค่าจากไฟล์ .env
   - แยกค่าที่เป็นความลับออกจากโค้ด
   - สามารถกำหนดค่าเริ่มต้นได้

2. การใช้งาน Pydantic:
   - ใช้ BaseSettings สำหรับตรวจสอบค่าอัตโนมัติ
   - กำหนด type hints เพื่อความชัดเจน
   - สามารถเพิ่ม validators ได้

3. การพัฒนาต่อยอด:
   - เพิ่มการโหลดค่าจาก JSON/YAML
   - เพิ่มระบบ configuration versioning
   - เพิ่มการ validate ค่าแบบซับซ้อน
"""

import os
from typing import Dict, Any, Optional, List
from pydantic import BaseSettings, validator, DirectoryPath
from pathlib import Path
from dotenv import load_dotenv
import json

# โหลดค่าจาก .env
load_dotenv()

class AISettings(BaseSettings):
    """
    การตั้งค่าสำหรับระบบ AI
    
    สำหรับนักศึกษา:
    1. ศึกษาการตั้งค่าโมเดล AI
    2. ปรับแต่งพารามิเตอร์
    3. เพิ่มการตรวจสอบค่า
    """
    MODEL_PATH: str = "./models/latest"
    CONFIDENCE_THRESHOLD: float = 0.8
    USE_GPU: bool = True
    BATCH_SIZE: int = 32
    MAX_EPOCHS: int = 100
    LEARNING_RATE: float = 0.001
    
    @validator('CONFIDENCE_THRESHOLD')
    def validate_confidence(cls, v):
        if not 0 <= v <= 1:
            raise ValueError('ค่าความเชื่อมั่นต้องอยู่ระหว่าง 0 และ 1')
        return v

class NotificationSettings(BaseSettings):
    """
    การตั้งค่าการแจ้งเตือน
    
    สำหรับนักศึกษา:
    1. ศึกษาการตั้งค่าการแจ้งเตือน
    2. เพิ่มช่องทางการแจ้งเตือน
    3. ปรับแต่งรูปแบบข้อความ
    """
    ENABLE_EMAIL: bool = False
    EMAIL_FROM: Optional[str] = None
    EMAIL_TO: Optional[List[str]] = None
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    ENABLE_LINE: bool = False
    LINE_TOKEN: Optional[str] = None
    
    @validator('EMAIL_TO', pre=True)
    def validate_email_list(cls, v):
        if isinstance(v, str):
            return v.split(',')
        return v

class Settings(BaseSettings):
    """
    กำหนดการตั้งค่าของระบบโดยใช้ Pydantic
    
    สำหรับนักศึกษา:
    1. ศึกษาการใช้ BaseSettings
    2. เพิ่มการตรวจสอบค่าด้วย validators
    3. ทดลองเพิ่มการตั้งค่าใหม่ๆ
    """
    
    # ตั้งค่าพื้นฐาน
    APP_NAME: str = "ระบบจัดการเทมเพลต Excel"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    LANGUAGE: str = "th"
    
    # ตั้งค่าความปลอดภัย
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ตั้งค่าฐานข้อมูล
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./excel_data.db")
    
    # ตั้งค่าพาธ
    STORAGE_PATH: DirectoryPath = Path("./data")
    TEMPLATE_PATH: DirectoryPath = Path("./templates")
    PREVIEW_PATH: DirectoryPath = Path("./previews")
    
    # ตั้งค่าการสำรองข้อมูล
    ENABLE_BACKUP: bool = True
    BACKUP_INTERVAL: str = "daily"  # daily, weekly, monthly
    BACKUP_PATH: DirectoryPath = Path("./backups")
    
    # ตั้งค่า AI
    ai: AISettings = AISettings()
    
    # ตั้งค่าการแจ้งเตือน
    notification: NotificationSettings = NotificationSettings()
    
    @validator('LANGUAGE')
    def validate_language(cls, v):
        if v not in ['th', 'en']:
            raise ValueError('รองรับเฉพาะภาษาไทยและอังกฤษ')
        return v
    
    @validator('BACKUP_INTERVAL')
    def validate_backup_interval(cls, v):
        if v not in ['daily', 'weekly', 'monthly']:
            raise ValueError('รองรับเฉพาะการสำรองข้อมูลรายวัน รายสัปดาห์ และรายเดือน')
        return v
    
    def save_to_json(self, path: str = "config.json"):
        """บันทึกการตั้งค่าลงในไฟล์ JSON"""
        config_dict = {
            "app": {
                "name": self.APP_NAME,
                "version": self.APP_VERSION,
                "debug": self.DEBUG,
                "language": self.LANGUAGE
            },
            "security": {
                "algorithm": self.ALGORITHM,
                "token_expire_minutes": self.ACCESS_TOKEN_EXPIRE_MINUTES
            },
            "paths": {
                "storage": str(self.STORAGE_PATH),
                "template": str(self.TEMPLATE_PATH),
                "preview": str(self.PREVIEW_PATH),
                "backup": str(self.BACKUP_PATH)
            },
            "backup": {
                "enabled": self.ENABLE_BACKUP,
                "interval": self.BACKUP_INTERVAL
            },
            "ai": {
                "model_path": self.ai.MODEL_PATH,
                "confidence_threshold": self.ai.CONFIDENCE_THRESHOLD,
                "use_gpu": self.ai.USE_GPU,
                "batch_size": self.ai.BATCH_SIZE,
                "max_epochs": self.ai.MAX_EPOCHS,
                "learning_rate": self.ai.LEARNING_RATE
            },
            "notification": {
                "email": {
                    "enabled": self.notification.ENABLE_EMAIL,
                    "from": self.notification.EMAIL_FROM,
                    "to": self.notification.EMAIL_TO,
                    "smtp": {
                        "host": self.notification.SMTP_HOST,
                        "port": self.notification.SMTP_PORT,
                        "user": self.notification.SMTP_USER
                    }
                },
                "line": {
                    "enabled": self.notification.ENABLE_LINE,
                    "token": self.notification.LINE_TOKEN
                }
            }
        }
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load_from_json(cls, path: str = "config.json") -> 'Settings':
        """โหลดการตั้งค่าจากไฟล์ JSON"""
        if not os.path.exists(path):
            return cls()
        
        with open(path, 'r', encoding='utf-8') as f:
            config_dict = json.load(f)
        
        # สร้าง environment variables จาก config
        os.environ['APP_NAME'] = config_dict['app']['name']
        os.environ['APP_VERSION'] = config_dict['app']['version']
        os.environ['DEBUG'] = str(config_dict['app']['debug']).lower()
        os.environ['LANGUAGE'] = config_dict['app']['language']
        
        # สร้าง instance ใหม่
        return cls()

# สร้าง instance ของการตั้งค่า
settings = Settings()

def get_settings() -> Settings:
    """ดึงการตั้งค่าระบบ
    
    Returns:
        Settings: การตั้งค่าระบบ
    """
    return settings

def setup_directories():
    """สร้างโฟลเดอร์ที่จำเป็น"""
    directories = [
        settings.UPLOAD_DIR,
        settings.TEMPLATE_DIR,
        settings.PREVIEW_DIR
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

def get_file_config() -> Dict[str, Any]:
    """ดึงการตั้งค่าเกี่ยวกับไฟล์
    
    Returns:
        Dict[str, Any]: การตั้งค่าเกี่ยวกับไฟล์
    """
    return {
        "max_size": settings.MAX_FILE_SIZE,
        "allowed_extensions": settings.ALLOWED_EXTENSIONS
    }

def get_security_config() -> Dict[str, Any]:
    """ดึงการตั้งค่าความปลอดภัย
    
    Returns:
        Dict[str, Any]: การตั้งค่าความปลอดภัย
    """
    return {
        "secret_key": settings.SECRET_KEY,
        "algorithm": settings.ALGORITHM,
        "token_expire_minutes": settings.ACCESS_TOKEN_EXPIRE_MINUTES
    }

def get_database_config() -> Dict[str, Any]:
    """ดึงการตั้งค่าฐานข้อมูล
    
    Returns:
        Dict[str, Any]: การตั้งค่าฐานข้อมูล
    """
    return {
        "url": settings.DATABASE_URL
    }

def get_logging_config() -> Dict[str, Any]:
    """ดึงการตั้งค่า logging
    
    Returns:
        Dict[str, Any]: การตั้งค่า logging
    """
    return {
        "level": settings.LOG_LEVEL,
        "format": settings.LOG_FORMAT,
        "file": settings.LOG_FILE
    }

def setup_logging():
    """ตั้งค่าระบบ logging"""
    log_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
            'detailed': {
                'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'standard',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'DEBUG',
                'formatter': 'detailed',
                'filename': 'app.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            },
            'error_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'ERROR',
                'formatter': 'detailed',
                'filename': 'error.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            }
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['console', 'file', 'error_file'],
                'level': 'INFO',
                'propagate': True
            },
            'excel_processor': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': False
            }
        }
    }
    
    import logging.config
    logging.config.dictConfig(log_config)

# ตัวอย่างการใช้งาน
if __name__ == "__main__":
    print(f"แอปพลิเคชัน: {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"โหมดดีบัก: {'เปิด' if settings.DEBUG else 'ปิด'}")
    print(f"ระดับการบันทึกล็อก: {settings.LOG_LEVEL}") 