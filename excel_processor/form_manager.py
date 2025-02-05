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
import tensorflow as tf
import numpy as np
from tensorflow.keras import layers, Model
from sklearn.preprocessing import LabelEncoder
import cv2

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

class DeepFormAnalyzer:
    """คลาสสำหรับวิเคราะห์เอกสารด้วย Deep Learning"""
    
    def __init__(self):
        self.document_model = self._build_document_model()
        self.field_model = self._build_field_model()
        self.label_encoder = LabelEncoder()
        
    def _build_document_model(self):
        """สร้างโมเดลสำหรับวิเคราะห์รูปแบบเอกสาร"""
        inputs = layers.Input(shape=(None, None, 3))
        
        # CNN Backbone
        x = layers.Conv2D(32, 3, activation='relu')(inputs)
        x = layers.MaxPooling2D()(x)
        x = layers.Conv2D(64, 3, activation='relu')(x)
        x = layers.MaxPooling2D()(x)
        x = layers.Conv2D(128, 3, activation='relu')(x)
        x = layers.MaxPooling2D()(x)
        
        # Feature Extraction
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dense(256, activation='relu')(x)
        x = layers.Dropout(0.5)(x)
        
        # Document Type Classification
        outputs = layers.Dense(10, activation='softmax')(x)
        
        return Model(inputs=inputs, outputs=outputs)
        
    def _build_field_model(self):
        """สร้างโมเดลสำหรับวิเคราะห์ฟิลด์ข้อมูล"""
        inputs = layers.Input(shape=(None, None, 3))
        
        # CNN for Field Detection
        x = layers.Conv2D(32, 3, activation='relu')(inputs)
        x = layers.MaxPooling2D()(x)
        x = layers.Conv2D(64, 3, activation='relu')(x)
        x = layers.MaxPooling2D()(x)
        
        # LSTM for Sequential Field Analysis
        x = layers.Reshape((-1, x.shape[-1]))(x)
        x = layers.Bidirectional(layers.LSTM(128, return_sequences=True))(x)
        x = layers.Bidirectional(layers.LSTM(64))(x)
        
        # Field Type Classification
        outputs = layers.Dense(5, activation='softmax')(x)
        
        return Model(inputs=inputs, outputs=outputs)
        
    def analyze_document_structure(self, excel_file: str):
        """วิเคราะห์โครงสร้างเอกสาร"""
        # แปลงไฟล์ Excel เป็นภาพ
        image = self._convert_excel_to_image(excel_file)
        
        # ปรับขนาดภาพ
        image = cv2.resize(image, (224, 224))
        image = image / 255.0
        
        # ทำนายประเภทเอกสาร
        doc_type = self.document_model.predict(np.expand_dims(image, axis=0))
        
        return {
            'document_type': self.label_encoder.inverse_transform(np.argmax(doc_type, axis=1))[0],
            'confidence': float(np.max(doc_type))
        }
        
    def analyze_fields(self, excel_file: str):
        """วิเคราะห์ฟิลด์ข้อมูลในเอกสาร"""
        # อ่านข้อมูลจาก Excel
        df = pd.read_excel(excel_file)
        
        field_info = {}
        for col in df.columns:
            # สร้างภาพจากข้อมูลในคอลัมน์
            field_image = self._visualize_field_data(df[col])
            
            # ทำนายประเภทฟิลด์
            field_type = self.field_model.predict(np.expand_dims(field_image, axis=0))
            
            field_info[col] = {
                'type': self.label_encoder.inverse_transform(np.argmax(field_type, axis=1))[0],
                'confidence': float(np.max(field_type)),
                'pattern': self._analyze_field_pattern(df[col])
            }
            
        return field_info
        
    def _convert_excel_to_image(self, excel_file: str):
        """แปลงไฟล์ Excel เป็นภาพ"""
        # TODO: ใช้ library เช่น pdf2image หรือ win32com สำหรับการแปลงไฟล์
        # สำหรับตัวอย่างนี้ สร้างภาพจำลอง
        return np.zeros((224, 224, 3))
        
    def _visualize_field_data(self, series):
        """สร้างภาพแสดงข้อมูลในฟิลด์"""
        # สร้างภาพขนาด 224x224
        image = np.zeros((224, 224, 3))
        
        try:
            # วาดกราฟข้อมูล
            if pd.api.types.is_numeric_dtype(series):
                # สร้างกราฟสำหรับข้อมูลตัวเลข
                values = series.values
                if len(values) > 0:
                    normalized = (values - values.min()) / (values.max() - values.min())
                    for i, v in enumerate(normalized[:223]):
                        cv2.line(image, (i, 223), (i, int(223 * (1-v))), (0, 255, 0), 1)
            else:
                # สร้างภาพสำหรับข้อความ
                text_data = str(series.iloc[0])
                cv2.putText(image, text_data[:20], (10, 112), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        except:
            pass
            
        return image
        
    def _analyze_field_pattern(self, series):
        """วิเคราะห์รูปแบบข้อมูลในฟิลด์"""
        pattern = {
            'data_type': str(series.dtype),
            'unique_ratio': len(series.unique()) / len(series),
            'null_ratio': series.isnull().sum() / len(series)
        }
        
        # วิเคราะห์รูปแบบเพิ่มเติมตามประเภทข้อมูล
        if pd.api.types.is_numeric_dtype(series):
            pattern.update({
                'mean': float(series.mean()),
                'std': float(series.std()),
                'distribution': 'normal' if abs(series.skew()) < 0.5 else 'skewed'
            })
        elif pd.api.types.is_string_dtype(series):
            pattern.update({
                'avg_length': float(series.str.len().mean()),
                'contains_numbers': bool(series.str.contains(r'\d').any()),
                'contains_special': bool(series.str.contains(r'[^a-zA-Z0-9\s]').any())
            })
            
        return pattern

class AIFormLearner:
    """คลาสสำหรับการเรียนรู้รูปแบบเอกสารด้วย AI"""
    
    def __init__(self):
        self.model = None
        self.layout_patterns = {}
        self.field_patterns = {}
        self.deep_analyzer = DeepFormAnalyzer()
        
    def learn_layout(self, excel_file: str):
        """เรียนรู้รูปแบบการจัดวางของเอกสาร"""
        df = pd.read_excel(excel_file)
        
        # วิเคราะห์การจัดวางคอลัมน์
        layout = {
            'columns': list(df.columns),
            'merged_cells': self._detect_merged_cells(df),
            'header_style': self._analyze_header_style(df),
            'data_patterns': self._analyze_data_patterns(df)
        }
        
        # เพิ่มการวิเคราะห์ด้วย Deep Learning
        doc_structure = self.deep_analyzer.analyze_document_structure(excel_file)
        field_analysis = self.deep_analyzer.analyze_fields(excel_file)
        
        layout.update({
            'document_type': doc_structure,
            'field_analysis': field_analysis
        })
        
        self.layout_patterns[excel_file] = layout
        return layout
        
    def _detect_merged_cells(self, df):
        """ตรวจจับเซลล์ที่ถูกรวม"""
        merged_cells = []
        try:
            if hasattr(df, 'sheet'):
                for range_ in df.sheet.merged_cells.ranges:
                    merged_cells.append({
                        'start_row': range_.min_row,
                        'end_row': range_.max_row,
                        'start_col': range_.min_col,
                        'end_col': range_.max_col
                    })
        except:
            pass
        return merged_cells
        
    def _analyze_header_style(self, df):
        """วิเคราะห์รูปแบบส่วนหัว"""
        header_style = {
            'font': None,
            'alignment': None,
            'border': None,
            'fill': None
        }
        
        try:
            if hasattr(df, 'sheet'):
                header_row = df.sheet[1]
                cell = header_row[0]
                header_style.update({
                    'font': {
                        'name': cell.font.name,
                        'size': cell.font.size,
                        'bold': cell.font.bold,
                        'italic': cell.font.italic
                    },
                    'alignment': {
                        'horizontal': cell.alignment.horizontal,
                        'vertical': cell.alignment.vertical
                    },
                    'border': {
                        'top': bool(cell.border.top.style),
                        'bottom': bool(cell.border.bottom.style),
                        'left': bool(cell.border.left.style),
                        'right': bool(cell.border.right.style)
                    }
                })
        except:
            pass
        return header_style
        
    def _analyze_data_patterns(self, df):
        """วิเคราะห์รูปแบบข้อมูล"""
        patterns = {}
        
        for col in df.columns:
            col_data = df[col].dropna()
            if len(col_data) == 0:
                continue
                
            patterns[col] = {
                'type': str(col_data.dtype),
                'unique_values': col_data.nunique(),
                'sample_values': col_data.head().tolist(),
                'format_pattern': self._detect_format_pattern(col_data)
            }
            
        return patterns
        
    def _detect_format_pattern(self, series):
        """ตรวจจับรูปแบบการจัดรูปแบบข้อมูล"""
        if pd.api.types.is_numeric_dtype(series):
            return {
                'type': 'numeric',
                'decimals': self._count_decimals(series),
                'has_thousand_sep': self._has_thousand_separator(series)
            }
        elif pd.api.types.is_datetime64_any_dtype(series):
            return {
                'type': 'datetime',
                'format': self._detect_date_format(series)
            }
        else:
            return {
                'type': 'text',
                'avg_length': series.str.len().mean(),
                'max_length': series.str.len().max()
            }
            
    def _count_decimals(self, series):
        """นับจำนวนทศนิยม"""
        try:
            return max(str(x)[::-1].find('.') for x in series if '.' in str(x))
        except:
            return 0
            
    def _has_thousand_separator(self, series):
        """ตรวจสอบตัวคั่นหลักพัน"""
        try:
            return any(',' in str(x) for x in series)
        except:
            return False
            
    def _detect_date_format(self, series):
        """ตรวจจับรูปแบบวันที่"""
        common_formats = [
            '%Y-%m-%d',
            '%d/%m/%Y',
            '%m/%d/%Y',
            '%d-%m-%Y',
            '%Y/%m/%d'
        ]
        
        for fmt in common_formats:
            try:
                pd.to_datetime(series.iloc[0], format=fmt)
                return fmt
            except:
                continue
        return None
        
    def suggest_template(self, excel_file: str) -> FormTemplate:
        """แนะนำ Template ที่เหมาะสม"""
        layout = self.learn_layout(excel_file)
        
        # สร้าง Template ใหม่
        template = FormTemplate(
            name=f"template_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            description=f"Template ที่สร้างโดย AI (ประเภทเอกสาร: {layout['document_type']['document_type']})"
        )
        
        # เพิ่มคอลัมน์และกฎการตรวจสอบ
        for col, field_info in layout['field_analysis'].items():
            template.add_column(
                name=col,
                data_type=field_info['type'],
                required=field_info['pattern']['null_ratio'] < 0.1
            )
            
            # สร้างกฎการตรวจสอบตามรูปแบบข้อมูล
            validation_rule = {
                'type': field_info['type'],
                'confidence': field_info['confidence']
            }
            
            if field_info['pattern'].get('distribution'):
                validation_rule.update({
                    'mean': field_info['pattern']['mean'],
                    'std': field_info['pattern']['std'],
                    'distribution': field_info['pattern']['distribution']
                })
            elif field_info['pattern'].get('avg_length'):
                validation_rule.update({
                    'max_length': int(field_info['pattern']['avg_length'] * 1.5),
                    'contains_numbers': field_info['pattern']['contains_numbers'],
                    'contains_special': field_info['pattern']['contains_special']
                })
                
            template.set_validation_rule(col, validation_rule)
            
        return template

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
            
        self.ai_learner = AIFormLearner()
            
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
        """เรียนรู้รูปแบบฟอร์มจากไฟล์ Excel ด้วย AI"""
        # ใช้ AI เรียนรู้และแนะนำ Template
        suggested_template = self.ai_learner.suggest_template(file_path)
        
        # สร้าง Template จากคำแนะนำของ AI
        template = self.create_template(name, description)
        template.columns = suggested_template.columns
        template.validation_rules = suggested_template.validation_rules
        
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