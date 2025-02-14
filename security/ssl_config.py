"""
ระบบจัดการการตั้งค่า SSL/TLS สำหรับ Excel Processor
รองรับ:
- การตั้งค่า SSL Certificate
- การกำหนด SSL Version
- การตั้งค่า Cipher Suites
- การตรวจสอบความปลอดภัย
"""

import os
import ssl
from typing import Dict, Any, Optional
import logging
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta
import OpenSSL.SSL

# ตั้งค่า logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SSLConfig:
    """ระบบจัดการการตั้งค่า SSL"""
    
    def __init__(self):
        """เริ่มต้นระบบจัดการ SSL"""
        self.cert_path = None
        self.key_path = None
        self.ssl_version = ssl.PROTOCOL_TLS_SERVER
        self.ciphers = "HIGH:!aNULL:!MD5:!3DES"
        logger.info("เริ่มต้นระบบจัดการ SSL")
    
    def setup_ssl(self, cert_path: str, key_path: str) -> Dict[str, Any]:
        """
        ตั้งค่า SSL Certificate
        
        Args:
            cert_path: พาธของ certificate
            key_path: พาธของ private key
            
        Returns:
            Dict: ข้อมูลการตั้งค่า SSL
        """
        try:
            self.cert_path = cert_path
            self.key_path = key_path
            
            # ตรวจสอบไฟล์ certificate
            if not os.path.exists(cert_path):
                raise FileNotFoundError(f"ไม่พบไฟล์ certificate ที่ {cert_path}")
            if not os.path.exists(key_path):
                raise FileNotFoundError(f"ไม่พบไฟล์ private key ที่ {key_path}")
            
            # ตรวจสอบความถูกต้องของ certificate
            self._validate_certificate()
            
            return {
                "ssl_context": (cert_path, key_path),
                "ssl_version": "TLS1.3",
                "ciphers": self.ciphers
            }
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการตั้งค่า SSL: {str(e)}")
            raise
    
    def _validate_certificate(self):
        """ตรวจสอบความถูกต้องของ certificate"""
        try:
            cert = OpenSSL.SSL.load_certificate(
                OpenSSL.SSL.FILETYPE_PEM,
                open(self.cert_path).read()
            )
            
            # ตรวจสอบวันหมดอายุ
            not_after = datetime.strptime(
                cert.get_notAfter().decode('ascii'),
                '%Y%m%d%H%M%SZ'
            )
            if not_after < datetime.now():
                raise ValueError("Certificate หมดอายุแล้ว")
            
            # ตรวจสอบ key usage
            for i in range(cert.get_extension_count()):
                ext = cert.get_extension(i)
                if ext.get_short_name() == b'keyUsage':
                    if not ext.get_data():
                        raise ValueError("Certificate ไม่มี key usage ที่ถูกต้อง")
            
            logger.info("ตรวจสอบ certificate สำเร็จ")
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการตรวจสอบ certificate: {str(e)}")
            raise
    
    def generate_self_signed_cert(
        self,
        common_name: str,
        output_dir: str,
        days_valid: int = 365
    ) -> Dict[str, str]:
        """
        สร้าง self-signed certificate
        
        Args:
            common_name: ชื่อ domain
            output_dir: โฟลเดอร์สำหรับเก็บไฟล์
            days_valid: จำนวนวันที่ certificate มีอายุ
            
        Returns:
            Dict: พาธของไฟล์ certificate และ key
        """
        try:
            # สร้าง private key
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            
            # สร้าง certificate
            subject = issuer = x509.Name([
                x509.NameAttribute(x509.NameOID.COMMON_NAME, common_name)
            ])
            
            cert = x509.CertificateBuilder().subject_name(
                subject
            ).issuer_name(
                issuer
            ).public_key(
                private_key.public_key()
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                datetime.utcnow()
            ).not_valid_after(
                datetime.utcnow() + timedelta(days=days_valid)
            ).add_extension(
                x509.BasicConstraints(ca=True, path_length=None),
                critical=True
            ).sign(private_key, hashes.SHA256())
            
            # บันทึกไฟล์
            cert_path = os.path.join(output_dir, "certificate.pem")
            key_path = os.path.join(output_dir, "private_key.pem")
            
            with open(cert_path, "wb") as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))
            
            with open(key_path, "wb") as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))
            
            logger.info(f"สร้าง self-signed certificate สำเร็จ: {cert_path}")
            return {
                "cert_path": cert_path,
                "key_path": key_path
            }
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการสร้าง certificate: {str(e)}")
            raise
    
    def set_ssl_version(self, version: str):
        """
        กำหนดเวอร์ชัน SSL/TLS
        
        Args:
            version: เวอร์ชันที่ต้องการใช้ (TLS1.2, TLS1.3)
        """
        versions = {
            "TLS1.2": ssl.PROTOCOL_TLSv1_2,
            "TLS1.3": ssl.PROTOCOL_TLS_SERVER
        }
        
        if version not in versions:
            raise ValueError(f"ไม่รองรับ SSL/TLS เวอร์ชัน {version}")
        
        self.ssl_version = versions[version]
        logger.info(f"ตั้งค่า SSL/TLS เวอร์ชัน {version}")
    
    def set_cipher_suites(self, ciphers: str):
        """
        กำหนด cipher suites
        
        Args:
            ciphers: รายการ cipher suites ที่ต้องการใช้
        """
        self.ciphers = ciphers
        logger.info(f"ตั้งค่า cipher suites: {ciphers}")
    
    def get_ssl_context(self) -> ssl.SSLContext:
        """
        สร้าง SSL context
        
        Returns:
            ssl.SSLContext: context สำหรับใช้งาน SSL
        """
        if not (self.cert_path and self.key_path):
            raise ValueError("ยังไม่ได้ตั้งค่า certificate และ private key")
        
        context = ssl.SSLContext(self.ssl_version)
        context.load_cert_chain(self.cert_path, self.key_path)
        context.set_ciphers(self.ciphers)
        
        # ตั้งค่าความปลอดภัยเพิ่มเติม
        context.options |= ssl.OP_NO_SSLv2
        context.options |= ssl.OP_NO_SSLv3
        context.options |= ssl.OP_NO_TLSv1
        context.options |= ssl.OP_NO_TLSv1_1
        
        return context
    
    def get_certificate_info(self) -> Dict[str, Any]:
        """
        ดึงข้อมูลของ certificate
        
        Returns:
            Dict: ข้อมูล certificate
        """
        if not self.cert_path:
            return {"error": "ยังไม่ได้ตั้งค่า certificate"}
        
        try:
            cert = OpenSSL.SSL.load_certificate(
                OpenSSL.SSL.FILETYPE_PEM,
                open(self.cert_path).read()
            )
            
            return {
                "subject": cert.get_subject().CN,
                "issuer": cert.get_issuer().CN,
                "valid_from": datetime.strptime(
                    cert.get_notBefore().decode('ascii'),
                    '%Y%m%d%H%M%SZ'
                ),
                "valid_until": datetime.strptime(
                    cert.get_notAfter().decode('ascii'),
                    '%Y%m%d%H%M%SZ'
                ),
                "serial_number": cert.get_serial_number(),
                "version": cert.get_version() + 1
            }
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการดึงข้อมูล certificate: {str(e)}")
            return {"error": str(e)} 