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
from typing import Dict, Any, Optional
from pydantic import BaseSettings, validator
from dotenv import load_dotenv

# โหลดค่าจาก .env
load_dotenv()

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
    
    # ตั้งค่าความปลอดภัย
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ตั้งค่าฐานข้อมูล
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./excel_data.db")
    
    # ตั้งค่าไฟล์
    UPLOAD_DIR: str = "uploads"
    TEMPLATE_DIR: str = "templates"
    PREVIEW_DIR: str = "previews"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {'.xlsx', '.xls'}
    
    # ตั้งค่า logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: Optional[str] = "app.log"
    
    @validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        """
        ตรวจสอบค่า SECRET_KEY
        
        Tips สำหรับนักศึกษา:
        - ตรวจสอบความยาวขั้นต่ำ
        - ตรวจสอบความซับซ้อน
        - เพิ่มการสร้างค่าอัตโนมัติ
        """
        if not v:
            raise ValueError("SECRET_KEY ต้องไม่ว่าง")
        if len(v) < 32:
            raise ValueError("SECRET_KEY ต้องมีความยาวอย่างน้อย 32 ตัวอักษร")
        return v
    
    @validator("DATABASE_URL")
    def validate_database_url(cls, v):
        """
        ตรวจสอบค่า DATABASE_URL
        
        Tips สำหรับนักศึกษา:
        - ตรวจสอบรูปแบบ URL
        - ตรวจสอบการเชื่อมต่อ
        - เพิ่มการเข้ารหัส credentials
        """
        if not v:
            raise ValueError("DATABASE_URL ต้องไม่ว่าง")
        if not v.startswith(("sqlite:///", "postgresql://", "mysql://")):
            raise ValueError("DATABASE_URL ต้องเป็น URL ที่ถูกต้อง")
        return v
    
    @validator("LOG_LEVEL")
    def validate_log_level(cls, v):
        """
        ตรวจสอบค่า LOG_LEVEL
        
        Tips สำหรับนักศึกษา:
        - ตรวจสอบค่าที่อนุญาต
        - เพิ่มระดับการบันทึกล็อก
        - ปรับแต่งรูปแบบการบันทึก
        """
        allowed_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in allowed_levels:
            raise ValueError(f"LOG_LEVEL ต้องเป็นหนึ่งใน {allowed_levels}")
        return v.upper()
    
    class Config:
        """
        การตั้งค่าเพิ่มเติมสำหรับ Pydantic
        
        Tips สำหรับนักศึกษา:
        - ศึกษาการใช้ env_file
        - เพิ่มการแปลงค่าอัตโนมัติ
        - กำหนดค่าเริ่มต้นที่ปลอดภัย
        """
        env_file = ".env"
        case_sensitive = True

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