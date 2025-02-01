"""
โมดูลสำหรับจัดการรูปแบบฟอร์มและการเชื่อมต่อกับ Data Server
"""
import os
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, String, DateTime
from sqlalchemy.orm import sessionmaker
from .processor import ExcelProcessor

logger = logging.getLogger(__name__)

class FormTemplate:
    """คลาสสำหรับจัดการรูปแบบฟอร์ม"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.created_at = datetime.now()
        self.columns = []
        self.sample_data = None
        self.validation_rules = {}
        
    def add_column(self, name: str, data_type: str, required: bool = False):
        """เพิ่มคอลัมน์ในฟอร์ม"""
        self.columns.append({
            "name": name,
            "data_type": data_type,
            "required": required
        })
        
    def set_validation_rule(self, column: str, rule: Dict):
        """กำหนดกฎการตรวจสอบข้อมูล"""
        self.validation_rules[column] = rule
        
    def to_dict(self) -> Dict:
        """แปลงข้อมูลเป็น Dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "columns": self.columns,
            "validation_rules": self.validation_rules
        }

class FormManager:
    """คลาสสำหรับจัดการฟอร์มทั้งหมด"""
    
    def __init__(self, storage_path: str, db_url: Optional[str] = None):
        self.storage_path = storage_path
        self.templates: Dict[str, FormTemplate] = {}
        self.db_engine = None
        if db_url:
            self.connect_db(db_url)
            
        # สร้างโฟลเดอร์เก็บ Template ถ้ายังไม่มี
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)
            
    def connect_db(self, db_url: str):
        """เชื่อมต่อกับฐานข้อมูล"""
        try:
            self.db_engine = create_engine(db_url)
            logger.info(f"เชื่อมต่อกับฐานข้อมูลสำเร็จ: {db_url}")
        except Exception as e:
            logger.error(f"ไม่สามารถเชื่อมต่อกับฐานข้อมูล: {str(e)}")
            raise
            
    def create_template(self, name: str, description: str) -> FormTemplate:
        """สร้างรูปแบบฟอร์มใหม่"""
        template = FormTemplate(name, description)
        self.templates[name] = template
        self._save_template(template)
        return template
    
    def learn_from_excel(self, file_path: str, name: str, description: str) -> FormTemplate:
        """เรียนรู้รูปแบบฟอร์มจากไฟล์ Excel"""
        processor = ExcelProcessor()
        df = processor.read_excel(file_path)
        
        template = self.create_template(name, description)
        
        # เรียนรู้โครงสร้างคอลัมน์
        for col in df.columns:
            data_type = str(df[col].dtype)
            template.add_column(col, data_type, required=True)
            
        # เก็บข้อมูลตัวอย่าง
        template.sample_data = df.head().to_dict()
        
        self._save_template(template)
        return template
    
    def _save_template(self, template: FormTemplate):
        """บันทึก Template ลงไฟล์"""
        file_path = os.path.join(self.storage_path, f"{template.name}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(template.to_dict(), f, ensure_ascii=False, indent=2)
            
    def load_templates(self) -> List[FormTemplate]:
        """โหลดรูปแบบฟอร์มทั้งหมด"""
        templates = []
        for file_name in os.listdir(self.storage_path):
            if file_name.endswith('.json'):
                file_path = os.path.join(self.storage_path, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    template = FormTemplate(data['name'], data['description'])
                    template.columns = data['columns']
                    template.validation_rules = data.get('validation_rules', {})
                    templates.append(template)
        return templates
    
    def save_to_db(self, template_name: str, data: pd.DataFrame):
        """บันทึกข้อมูลลงฐานข้อมูล"""
        if not self.db_engine:
            raise Exception("ยังไม่ได้เชื่อมต่อกับฐานข้อมูล")
            
        template = self.templates.get(template_name)
        if not template:
            raise Exception(f"ไม่พบ Template: {template_name}")
            
        # สร้างตารางถ้ายังไม่มี
        metadata = MetaData()
        columns = [Column('id', String(50), primary_key=True)]
        columns.extend([
            Column(col['name'], String(255))
            for col in template.columns
        ])
        columns.append(Column('created_at', DateTime, default=datetime.now))
        
        table = Table(template_name, metadata, *columns)
        metadata.create_all(self.db_engine)
        
        # บันทึกข้อมูล
        data.to_sql(
            template_name,
            self.db_engine,
            if_exists='append',
            index=False
        )
        
    def get_from_db(self, template_name: str) -> pd.DataFrame:
        """ดึงข้อมูลจากฐานข้อมูล"""
        if not self.db_engine:
            raise Exception("ยังไม่ได้เชื่อมต่อกับฐานข้อมูล")
            
        query = f"SELECT * FROM {template_name}"
        return pd.read_sql(query, self.db_engine) 