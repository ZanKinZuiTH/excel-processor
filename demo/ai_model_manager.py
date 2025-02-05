import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
import cv2
import pandas as pd
from pathlib import Path
import json
import uuid

class AIModelManager:
    """จัดการระบบ AI สำหรับวิเคราะห์เอกสาร Excel"""
    
    def __init__(self):
        """สร้าง AI Model Manager"""
        self.structure_model = self._create_structure_model()
        self.content_model = self._create_content_model()
        self.current_model = None
    
    def _create_structure_model(self):
        """สร้างโมเดล CNN สำหรับวิเคราะห์โครงสร้างเอกสาร"""
        model = models.Sequential([
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.Flatten(),
            layers.Dense(64, activation='relu'),
            layers.Dense(3, activation='softmax')  # 3 ประเภทเอกสาร
        ])
        model.compile(optimizer='adam',
                     loss='categorical_crossentropy',
                     metrics=['accuracy'])
        return model
    
    def _create_content_model(self):
        """สร้างโมเดล CNN+LSTM สำหรับวิเคราะห์เนื้อหา"""
        # CNN สำหรับสกัดคุณลักษณะ
        cnn_input = layers.Input(shape=(224, 224, 3))
        x = layers.Conv2D(32, (3, 3), activation='relu')(cnn_input)
        x = layers.MaxPooling2D((2, 2))(x)
        x = layers.Conv2D(64, (3, 3), activation='relu')(x)
        x = layers.MaxPooling2D((2, 2))(x)
        x = layers.Flatten()(x)
        
        # LSTM สำหรับวิเคราะห์ลำดับ
        lstm_input = layers.Input(shape=(None, 100))
        y = layers.LSTM(64, return_sequences=True)(lstm_input)
        y = layers.LSTM(32)(y)
        
        # รวม CNN และ LSTM
        combined = layers.concatenate([x, y])
        output = layers.Dense(128, activation='relu')(combined)
        output = layers.Dense(10, activation='softmax')(output)  # 10 ประเภทฟิลด์
        
        model = models.Model(inputs=[cnn_input, lstm_input], outputs=output)
        model.compile(optimizer='adam',
                     loss='categorical_crossentropy',
                     metrics=['accuracy'])
        return model
    
    def analyze_structure(self, file_path):
        """วิเคราะห์โครงสร้างเอกสารด้วย CNN
        
        Args:
            file_path: พาธของไฟล์ Excel
            
        Returns:
            dict: ผลการวิเคราะห์โครงสร้าง เช่น
                {
                    "ข้อมูลส่วนบุคคล": 0.95,
                    "ประวัติการศึกษา": 0.85,
                    "ประวัติการทำงาน": 0.90
                }
        """
        # แปลงไฟล์ Excel เป็นรูปภาพ
        image = self._convert_excel_to_image(file_path)
        
        # ทำนายด้วยโมเดล
        prediction = self.structure_model.predict(np.array([image]))
        
        # แปลงผลลัพธ์
        sections = ["ข้อมูลส่วนบุคคล", "ประวัติการศึกษา", "ประวัติการทำงาน"]
        return {section: float(conf) for section, conf in zip(sections, prediction[0])}
    
    def analyze_content(self, file_path):
        """วิเคราะห์เนื้อหาเอกสารด้วย CNN+LSTM
        
        Args:
            file_path: พาธของไฟล์ Excel
            
        Returns:
            dict: ผลการวิเคราะห์เนื้อหา เช่น
                {
                    "ชื่อ-นามสกุล": {
                        "value": "นายสมชาย รักเรียน",
                        "confidence": 0.95
                    },
                    "เลขประจำตัวประชาชน": {
                        "value": "1234567890123",
                        "confidence": 0.98
                    }
                }
        """
        # อ่านข้อมูลจากไฟล์ Excel
        df = pd.read_excel(file_path)
        
        # แปลงข้อมูลเป็นรูปแบบที่เหมาะสม
        image = self._convert_excel_to_image(file_path)
        sequence = self._extract_sequence_features(df)
        
        # ทำนายด้วยโมเดล
        prediction = self.content_model.predict([np.array([image]), np.array([sequence])])
        
        # แปลงผลลัพธ์
        fields = self._extract_fields(df)
        result = {}
        for field, value, conf in zip(fields, df.iloc[0], prediction[0]):
            result[field] = {
                "value": str(value),
                "confidence": float(conf)
            }
        return result
    
    def create_template(self, file_path):
        """สร้างเทมเพลตอัตโนมัติจากการวิเคราะห์
        
        Args:
            file_path: พาธของไฟล์ Excel
            
        Returns:
            dict: ข้อมูลเทมเพลต เช่น
                {
                    "id": "template-123",
                    "fields": ["ชื่อ-นามสกุล", "เลขประจำตัวประชาชน", ...]
                }
        """
        # วิเคราะห์โครงสร้างและเนื้อหา
        structure = self.analyze_structure(file_path)
        content = self.analyze_content(file_path)
        
        # สร้างเทมเพลต
        template = {
            "id": f"template-{uuid.uuid4().hex[:8]}",
            "fields": list(content.keys())
        }
        
        # บันทึกเทมเพลต
        template_path = Path("templates") / f"{template['id']}.json"
        template_path.parent.mkdir(exist_ok=True)
        with open(template_path, "w", encoding="utf-8") as f:
            json.dump(template, f, ensure_ascii=False, indent=2)
        
        return template
    
    def train(self, files, epochs=10, batch_size=32):
        """ฝึกฝนโมเดลด้วยข้อมูลใหม่
        
        Args:
            files: รายการไฟล์สำหรับฝึกฝน
            epochs: จำนวนรอบการฝึกฝน
            batch_size: ขนาดแบตช์
            
        Returns:
            dict: ผลการฝึกฝน เช่น
                {
                    "accuracy": 0.95,
                    "loss": 0.05
                }
        """
        # เตรียมข้อมูลสำหรับฝึกฝน
        X_structure = []
        y_structure = []
        X_content_image = []
        X_content_sequence = []
        y_content = []
        
        for file in files:
            # อ่านข้อมูล
            df = pd.read_excel(file)
            image = self._convert_excel_to_image(file)
            sequence = self._extract_sequence_features(df)
            
            # เพิ่มข้อมูลสำหรับโมเดลโครงสร้าง
            X_structure.append(image)
            y_structure.append(self._get_structure_label(file))
            
            # เพิ่มข้อมูลสำหรับโมเดลเนื้อหา
            X_content_image.append(image)
            X_content_sequence.append(sequence)
            y_content.append(self._get_content_labels(df))
        
        # แปลงเป็น numpy array
        X_structure = np.array(X_structure)
        y_structure = np.array(y_structure)
        X_content_image = np.array(X_content_image)
        X_content_sequence = np.array(X_content_sequence)
        y_content = np.array(y_content)
        
        # ฝึกฝนโมเดลโครงสร้าง
        structure_history = self.structure_model.fit(
            X_structure, y_structure,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.2
        )
        
        # ฝึกฝนโมเดลเนื้อหา
        content_history = self.content_model.fit(
            [X_content_image, X_content_sequence], y_content,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.2
        )
        
        # คำนวณผลรวม
        return {
            "accuracy": (structure_history.history['accuracy'][-1] + 
                       content_history.history['accuracy'][-1]) / 2,
            "loss": (structure_history.history['loss'][-1] + 
                    content_history.history['loss'][-1]) / 2
        }
    
    def save_model(self):
        """บันทึกโมเดลปัจจุบัน
        
        Returns:
            str: ID ของโมเดล
        """
        model_id = f"model-{uuid.uuid4().hex[:8]}"
        model_dir = Path("models") / model_id
        model_dir.mkdir(parents=True, exist_ok=True)
        
        # บันทึกโมเดล
        self.structure_model.save(model_dir / "structure_model")
        self.content_model.save(model_dir / "content_model")
        
        return model_id
    
    def load_model(self, model_id):
        """โหลดโมเดลจาก ID
        
        Args:
            model_id: ID ของโมเดล
            
        Returns:
            bool: True ถ้าโหลดสำเร็จ
        """
        model_dir = Path("models") / model_id
        if not model_dir.exists():
            return False
        
        # โหลดโมเดล
        self.structure_model = models.load_model(model_dir / "structure_model")
        self.content_model = models.load_model(model_dir / "content_model")
        self.current_model = model_id
        
        return True
    
    def _convert_excel_to_image(self, file_path):
        """แปลงไฟล์ Excel เป็นรูปภาพ"""
        # จำลองการแปลงไฟล์เป็นรูปภาพ
        return np.random.rand(224, 224, 3)
    
    def _extract_sequence_features(self, df):
        """สกัดคุณลักษณะลำดับจาก DataFrame"""
        # จำลองการสกัดคุณลักษณะ
        return np.random.rand(10, 100)
    
    def _extract_fields(self, df):
        """สกัดรายการฟิลด์จาก DataFrame"""
        return list(df.columns)
    
    def _get_structure_label(self, file_path):
        """รับป้ายกำกับโครงสร้างจากชื่อไฟล์"""
        # จำลองการรับป้ายกำกับ
        return np.array([0.8, 0.1, 0.1])
    
    def _get_content_labels(self, df):
        """รับป้ายกำกับเนื้อหาจาก DataFrame"""
        # จำลองการรับป้ายกำกับ
        return np.random.rand(10) 