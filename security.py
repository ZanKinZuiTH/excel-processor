"""
ระบบรักษาความปลอดภัยสำหรับระบบจัดการเทมเพลต Excel

สำหรับนักศึกษา:
1. ศึกษาการใช้งาน JWT (JSON Web Token):
   - ใช้สำหรับการยืนยันตัวตนแบบ stateless
   - มีโครงสร้าง: header.payload.signature
   - สามารถกำหนดเวลาหมดอายุได้

2. การเข้ารหัสข้อมูล:
   - ใช้ hashlib สำหรับการเข้ารหัสแบบ one-way
   - สามารถเพิ่มการเข้ารหัสแบบอื่นๆ เช่น AES, RSA
   - ควรใช้ salt เพื่อเพิ่มความปลอดภัย

3. การตรวจสอบไฟล์:
   - ตรวจสอบนามสกุลไฟล์ที่อนุญาต
   - จำกัดขนาดไฟล์
   - สามารถเพิ่มการตรวจสอบ malware ได้

4. การพัฒนาต่อยอด:
   - เพิ่มระบบ Rate Limiting
   - เพิ่มการตรวจจับการโจมตี
   - เพิ่มระบบ 2FA
"""

import os
import jwt
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional
from dotenv import load_dotenv
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# โหลดค่าคอนฟิก
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ตั้งค่า logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityManager:
    """
    จัดการความปลอดภัยของระบบ
    
    สำหรับนักศึกษา:
    1. ศึกษาการทำงานของแต่ละเมธอด
    2. ทดลองเพิ่มฟีเจอร์ความปลอดภัยใหม่ๆ
    3. ทดสอบการโจมตีในรูปแบบต่างๆ
    """
    
    def __init__(self):
        """
        กำหนดค่าเริ่มต้น
        
        Tips สำหรับนักศึกษา:
        - ใช้ HTTPBearer สำหรับจัดการ token ในส่วนของ FastAPI
        - blacklist ใช้เก็บ token ที่ถูกเพิกถอน (อาจใช้ Redis แทนได้)
        """
        self.security = HTTPBearer()
        self.blacklist = set()  # เก็บ token ที่ถูก revoke
    
    def create_access_token(self, data: dict) -> str:
        """
        สร้าง JWT token
        
        Tips สำหรับนักศึกษา:
        - ใช้ datetime.utcnow() เพื่อป้องกันปัญหา timezone
        - เพิ่ม claims อื่นๆ เช่น 'iss', 'aud' ได้
        - อาจเพิ่ม refresh token
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        
        try:
            encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
            logger.info(f"สร้าง token สำเร็จสำหรับผู้ใช้ {data.get('username')}")
            return encoded_jwt
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการสร้าง token: {str(e)}")
            raise HTTPException(status_code=500, detail="ไม่สามารถสร้าง token ได้")
    
    def verify_token(self, token: str) -> Dict:
        """
        ตรวจสอบความถูกต้องของ token
        
        Tips สำหรับนักศึกษา:
        - ตรวจสอบ token ใน blacklist ก่อน
        - จัดการ exceptions ที่อาจเกิดขึ้น
        - เพิ่มการตรวจสอบ claims เพิ่มเติม
        """
        try:
            if token in self.blacklist:
                raise HTTPException(status_code=401, detail="Token ถูกเพิกถอนแล้ว")
            
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            logger.info(f"ตรวจสอบ token สำเร็จสำหรับผู้ใช้ {payload.get('username')}")
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token หมดอายุ")
            raise HTTPException(status_code=401, detail="Token หมดอายุ")
        except jwt.JWTError:
            logger.warning("Token ไม่ถูกต้อง")
            raise HTTPException(status_code=401, detail="Token ไม่ถูกต้อง")
    
    def hash_password(self, password: str) -> str:
        """
        เข้ารหัสรหัสผ่าน
        
        Tips สำหรับนักศึกษา:
        - ควรใช้ bcrypt หรือ Argon2 แทน SHA-256
        - เพิ่ม salt ที่สุ่มขึ้นมา
        - อาจใช้ PBKDF2 เพื่อเพิ่มความปลอดภัย
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        ตรวจสอบรหัสผ่าน
        
        Tips สำหรับนักศึกษา:
        - ใช้ secrets.compare_digest() เพื่อป้องกัน timing attack
        - เพิ่มการตรวจสอบความซับซ้อนของรหัสผ่าน
        - เพิ่มการป้องกัน brute force
        """
        return self.hash_password(plain_password) == hashed_password
    
    def validate_file(self, file_path: str) -> bool:
        """
        ตรวจสอบความปลอดภัยของไฟล์
        
        Tips สำหรับนักศึกษา:
        - เพิ่มการตรวจสอบ MIME type
        - เพิ่มการสแกน malware
        - เพิ่มการตรวจสอบ metadata
        """
        # ตรวจสอบนามสกุลไฟล์
        allowed_extensions = {'.xlsx', '.xls'}
        if not any(file_path.endswith(ext) for ext in allowed_extensions):
            logger.warning(f"ไฟล์ไม่ได้รับอนุญาต: {file_path}")
            raise HTTPException(status_code=400, detail="รองรับเฉพาะไฟล์ Excel เท่านั้น")
        
        # ตรวจสอบขนาดไฟล์
        max_size = 10 * 1024 * 1024  # 10MB
        if os.path.getsize(file_path) > max_size:
            logger.warning(f"ไฟล์มีขนาดใหญ่เกินไป: {file_path}")
            raise HTTPException(status_code=400, detail="ไฟล์มีขนาดใหญ่เกินไป (สูงสุด 10MB)")
        
        return True
    
    def encrypt_data(self, data: str) -> str:
        """เข้ารหัสข้อมูล
        
        Args:
            data: ข้อมูลที่ต้องการเข้ารหัส
            
        Returns:
            str: ข้อมูลที่เข้ารหัสแล้ว
        """
        # TODO: เพิ่มการเข้ารหัสข้อมูลที่ซับซ้อนขึ้น
        return hashlib.sha256(data.encode()).hexdigest()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """ถอดรหัสข้อมูล
        
        Args:
            encrypted_data: ข้อมูลที่เข้ารหัสแล้ว
            
        Returns:
            str: ข้อมูลที่ถอดรหัสแล้ว
        """
        # TODO: เพิ่มการถอดรหัสข้อมูลที่ซับซ้อนขึ้น
        return encrypted_data
    
    def revoke_token(self, token: str):
        """เพิกถอน token
        
        Args:
            token: token ที่ต้องการเพิกถอน
        """
        self.blacklist.add(token)
        logger.info(f"เพิกถอน token สำเร็จ")
    
    async def get_current_user(
        self,
        credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())
    ) -> Dict:
        """ดึงข้อมูลผู้ใช้ปัจจุบัน
        
        Args:
            credentials: ข้อมูลการยืนยันตัวตน
            
        Returns:
            Dict: ข้อมูลผู้ใช้
        """
        token = credentials.credentials
        return self.verify_token(token) 