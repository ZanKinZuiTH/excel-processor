"""
ระบบจัดการฐานข้อมูลสำหรับ Excel Processor
รองรับฐานข้อมูลหลายประเภท:
- MySQL
- PostgreSQL
- MSSQL
- SQLite
"""

import os
from typing import Dict, Any, Optional
import logging
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager

# ตั้งค่า logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """ระบบจัดการฐานข้อมูล"""
    
    def __init__(self, db_type: str):
        """
        เริ่มต้นระบบจัดการฐานข้อมูล
        
        Args:
            db_type: ประเภทฐานข้อมูล (mysql/postgresql/mssql/sqlite)
        """
        self.db_type = db_type.lower()
        self.engine = None
        self.Session = None
        self.metadata = MetaData()
        logger.info(f"เริ่มต้นระบบจัดการฐานข้อมูล {db_type}")
    
    def setup_connection(self, config: Dict[str, Any]) -> bool:
        """
        ตั้งค่าการเชื่อมต่อฐานข้อมูล
        
        Args:
            config: ข้อมูลการตั้งค่าการเชื่อมต่อ
            
        Returns:
            bool: True ถ้าเชื่อมต่อสำเร็จ
        """
        try:
            connection_url = self._build_connection_url(config)
            self.engine = create_engine(connection_url)
            self.Session = sessionmaker(bind=self.engine)
            
            # ทดสอบการเชื่อมต่อ
            with self.engine.connect() as conn:
                conn.execute("SELECT 1")
            
            logger.info(f"เชื่อมต่อฐานข้อมูล {self.db_type} สำเร็จ")
            return True
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการเชื่อมต่อฐานข้อมูล: {str(e)}")
            return False
    
    def _build_connection_url(self, config: Dict[str, Any]) -> str:
        """สร้าง URL สำหรับเชื่อมต่อฐานข้อมูล"""
        if self.db_type == "mysql":
            return f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
        elif self.db_type == "postgresql":
            return f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
        elif self.db_type == "mssql":
            return f"mssql+pyodbc://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}?driver=ODBC+Driver+17+for+SQL+Server"
        elif self.db_type == "sqlite":
            return f"sqlite:///{config['database']}"
        else:
            raise ValueError(f"ไม่รองรับฐานข้อมูลประเภท {self.db_type}")
    
    @contextmanager
    def get_session(self):
        """สร้าง session สำหรับทำงานกับฐานข้อมูล"""
        if not self.Session:
            raise RuntimeError("ยังไม่ได้ตั้งค่าการเชื่อมต่อฐานข้อมูล")
        
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def create_tables(self) -> bool:
        """สร้างตารางในฐานข้อมูล"""
        try:
            self.metadata.create_all(self.engine)
            logger.info("สร้างตารางในฐานข้อมูลสำเร็จ")
            return True
        except SQLAlchemyError as e:
            logger.error(f"เกิดข้อผิดพลาดในการสร้างตาราง: {str(e)}")
            return False
    
    def backup_database(self, backup_path: str) -> bool:
        """
        สำรองข้อมูลในฐานข้อมูล
        
        Args:
            backup_path: พาธที่จะเก็บไฟล์สำรองข้อมูล
            
        Returns:
            bool: True ถ้าสำรองข้อมูลสำเร็จ
        """
        try:
            if self.db_type == "mysql":
                return self._backup_mysql(backup_path)
            elif self.db_type == "postgresql":
                return self._backup_postgresql(backup_path)
            elif self.db_type == "mssql":
                return self._backup_mssql(backup_path)
            elif self.db_type == "sqlite":
                return self._backup_sqlite(backup_path)
            else:
                raise ValueError(f"ไม่รองรับการสำรองข้อมูลสำหรับฐานข้อมูลประเภท {self.db_type}")
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการสำรองข้อมูล: {str(e)}")
            return False
    
    def _backup_mysql(self, backup_path: str) -> bool:
        """สำรองข้อมูล MySQL"""
        try:
            os.system(f"mysqldump -u {self.config['user']} -p{self.config['password']} {self.config['database']} > {backup_path}")
            return True
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการสำรองข้อมูล MySQL: {str(e)}")
            return False
    
    def _backup_postgresql(self, backup_path: str) -> bool:
        """สำรองข้อมูล PostgreSQL"""
        try:
            os.system(f"pg_dump -U {self.config['user']} -W {self.config['password']} {self.config['database']} > {backup_path}")
            return True
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการสำรองข้อมูล PostgreSQL: {str(e)}")
            return False
    
    def _backup_mssql(self, backup_path: str) -> bool:
        """สำรองข้อมูล MSSQL"""
        try:
            backup_query = f"BACKUP DATABASE {self.config['database']} TO DISK = '{backup_path}'"
            with self.get_session() as session:
                session.execute(backup_query)
            return True
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการสำรองข้อมูล MSSQL: {str(e)}")
            return False
    
    def _backup_sqlite(self, backup_path: str) -> bool:
        """สำรองข้อมูล SQLite"""
        try:
            import shutil
            shutil.copy2(self.config['database'], backup_path)
            return True
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการสำรองข้อมูล SQLite: {str(e)}")
            return False
    
    def restore_database(self, backup_path: str) -> bool:
        """
        กู้คืนข้อมูลจากไฟล์สำรอง
        
        Args:
            backup_path: พาธของไฟล์สำรองข้อมูล
            
        Returns:
            bool: True ถ้ากู้คืนข้อมูลสำเร็จ
        """
        try:
            if self.db_type == "mysql":
                return self._restore_mysql(backup_path)
            elif self.db_type == "postgresql":
                return self._restore_postgresql(backup_path)
            elif self.db_type == "mssql":
                return self._restore_mssql(backup_path)
            elif self.db_type == "sqlite":
                return self._restore_sqlite(backup_path)
            else:
                raise ValueError(f"ไม่รองรับการกู้คืนข้อมูลสำหรับฐานข้อมูลประเภท {self.db_type}")
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการกู้คืนข้อมูล: {str(e)}")
            return False
    
    def get_database_info(self) -> Dict[str, Any]:
        """ดึงข้อมูลของฐานข้อมูล"""
        try:
            with self.get_session() as session:
                if self.db_type == "mysql":
                    result = session.execute("SELECT VERSION()").scalar()
                elif self.db_type == "postgresql":
                    result = session.execute("SELECT version()").scalar()
                elif self.db_type == "mssql":
                    result = session.execute("SELECT @@VERSION").scalar()
                elif self.db_type == "sqlite":
                    result = session.execute("SELECT sqlite_version()").scalar()
                
                return {
                    "type": self.db_type,
                    "version": result,
                    "connected": True,
                    "tables": [t.name for t in self.metadata.tables.values()]
                }
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการดึงข้อมูลฐานข้อมูล: {str(e)}")
            return {
                "type": self.db_type,
                "version": None,
                "connected": False,
                "error": str(e)
            } 