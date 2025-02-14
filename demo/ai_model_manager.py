"""
AI Model Manager
--------------
ระบบจัดการโมเดล AI สำหรับวิเคราะห์เอกสาร Excel

สำหรับนักศึกษา:
1. ศึกษาการสร้างโมเดล CNN และ LSTM
2. เรียนรู้การประมวลผลภาพจาก Excel
3. ทำความเข้าใจการ train และ evaluate โมเดล
4. ศึกษาการจัดการ model weights และ checkpoints

Author: ZanKinZuiTH
Version: 1.1.0
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
import cv2
import pandas as pd
from pathlib import Path
import json
import uuid
import os
import logging
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from prophet import Prophet

# ตั้งค่า logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIModelManager:
    """จัดการโมเดล AI สำหรับวิเคราะห์เอกสาร Excel
    
    สำหรับนักศึกษา:
    1. ศึกษาการทำงานของแต่ละ method
    2. สังเกตการใช้ CNN สำหรับวิเคราะห์โครงสร้าง
    3. สังเกตการใช้ LSTM สำหรับวิเคราะห์เนื้อหา
    4. ทดลองปรับแต่ง hyperparameters
    """
    
    def __init__(self):
        """
        กำหนดค่าเริ่มต้นสำหรับ AI Model Manager
        
        สำหรับนักศึกษา:
        - สังเกตการสร้างโมเดลแยกสำหรับโครงสร้างและเนื้อหา
        - ศึกษาการกำหนด input shape ที่เหมาะสม
        """
        self.structure_model = self._create_structure_model()
        self.content_model = self._create_content_model()
        logger.info("สร้าง AI Model Manager สำเร็จ")
    
    def _create_structure_model(self):
        """
        สร้างโมเดล CNN สำหรับวิเคราะห์โครงสร้างเอกสาร
        
        สำหรับนักศึกษา:
        1. ศึกษาการออกแบบ CNN Architecture
        2. สังเกตการใช้ layers ต่างๆ
        3. ทดลองปรับ kernel size และ filters
        """
        model = models.Sequential([
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.Flatten(),
            layers.Dense(64, activation='relu'),
            layers.Dense(10, activation='softmax')
        ])
        model.compile(optimizer='adam',
                     loss='sparse_categorical_crossentropy',
                     metrics=['accuracy'])
        return model
    
    def _create_content_model(self):
        """
        สร้างโมเดล CNN+LSTM สำหรับวิเคราะห์เนื้อหา
        
        สำหรับนักศึกษา:
        1. ศึกษาการผสมผสาน CNN กับ LSTM
        2. สังเกตการจัดการ sequence data
        3. ทดลองปรับ LSTM units และ layers
        """
        model = models.Sequential([
            layers.Conv1D(64, 3, activation='relu', input_shape=(None, 100)),
            layers.MaxPooling1D(2),
            layers.Conv1D(128, 3, activation='relu'),
            layers.MaxPooling1D(2),
            layers.LSTM(64, return_sequences=True),
            layers.LSTM(32),
            layers.Dense(64, activation='relu'),
            layers.Dense(32, activation='relu'),
            layers.Dense(5, activation='softmax')
        ])
        model.compile(optimizer='adam',
                     loss='sparse_categorical_crossentropy',
                     metrics=['accuracy'])
        return model
    
    def analyze_structure(self, file_path):
        """
        วิเคราะห์โครงสร้างเอกสารด้วย CNN
        
        Args:
            file_path: พาธของไฟล์ Excel
            
        Returns:
            Dict: ผลการวิเคราะห์โครงสร้าง
            
        สำหรับนักศึกษา:
        1. ศึกษาการแปลงไฟล์ Excel เป็นรูปภาพ
        2. สังเกตการ preprocess ข้อมูล
        3. ทดลองปรับปรุงการวิเคราะห์
        """
        try:
            # แปลง Excel เป็นรูปภาพ
            image = self._convert_excel_to_image(file_path)
            
            # Preprocess
            image = cv2.resize(image, (224, 224))
            image = image / 255.0
            image = np.expand_dims(image, axis=0)
            
            # วิเคราะห์
            prediction = self.structure_model.predict(image)
            
            return {
                "structure_type": int(np.argmax(prediction[0])),
                "confidence": float(np.max(prediction[0]))
            }
            
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการวิเคราะห์โครงสร้าง: {str(e)}")
            raise
    
    def analyze_content(self, file_path):
        """
        วิเคราะห์เนื้อหาเอกสารด้วย CNN+LSTM
        
        Args:
            file_path: พาธของไฟล์ Excel
            
        Returns:
            Dict: ผลการวิเคราะห์เนื้อหา
            
        สำหรับนักศึกษา:
        1. ศึกษาการสกัด features จากข้อมูล
        2. สังเกตการจัดการ sequence data
        3. ทดลองปรับปรุงการวิเคราะห์
        """
        try:
            # อ่านข้อมูล
            df = pd.read_excel(file_path)
            
            # สกัด features
            features = self._extract_sequence_features(df)
            
            # Preprocess
            features = np.expand_dims(features, axis=0)
            
            # วิเคราะห์
            prediction = self.content_model.predict(features)
            
            return {
                "content_type": int(np.argmax(prediction[0])),
                "confidence": float(np.max(prediction[0])),
                "fields": self._extract_fields(df)
            }
            
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการวิเคราะห์เนื้อหา: {str(e)}")
            raise
    
    def create_template(self, file_path):
        """
        สร้าง Template อัตโนมัติจากการวิเคราะห์
        
        Args:
            file_path: พาธของไฟล์ Excel
            
        Returns:
            Dict: Template ที่สร้างขึ้น
            
        สำหรับนักศึกษา:
        1. ศึกษาการรวมผลการวิเคราะห์
        2. สังเกตการสร้าง Template
        3. ทดลองปรับปรุงการสร้าง Template
        """
        try:
            # วิเคราะห์โครงสร้างและเนื้อหา
            structure = self.analyze_structure(file_path)
            content = self.analyze_content(file_path)
            
            # สร้าง Template
            template = {
                "id": str(uuid.uuid4()),
                "structure_type": structure["structure_type"],
                "content_type": content["content_type"],
                "fields": content["fields"],
                "confidence": min(structure["confidence"], content["confidence"])
            }
            
            return template
            
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการสร้าง Template: {str(e)}")
            raise
    
    def train(self, files, epochs=10, batch_size=32):
        """
        เทรนโมเดลด้วยข้อมูลใหม่
        
        Args:
            files: List ของไฟล์สำหรับเทรน
            epochs: จำนวนรอบการเทรน
            batch_size: ขนาด batch
            
        Returns:
            Dict: ผลการเทรน
            
        สำหรับนักศึกษา:
        1. ศึกษาการเตรียมข้อมูลสำหรับเทรน
        2. สังเกตการใช้ callbacks
        3. ทดลองปรับ hyperparameters
        """
        try:
            # เตรียมข้อมูลสำหรับ structure model
            structure_images = []
            structure_labels = []
            
            # เตรียมข้อมูลสำหรับ content model
            content_sequences = []
            content_labels = []
            
            # โหลดและเตรียมข้อมูล
            for file in files:
                # Structure data
                image = self._convert_excel_to_image(file)
                image = cv2.resize(image, (224, 224))
                image = image / 255.0
                structure_images.append(image)
                structure_labels.append(self._get_structure_label(file))
                
                # Content data
                df = pd.read_excel(file)
                features = self._extract_sequence_features(df)
                content_sequences.append(features)
                content_labels.append(self._get_content_labels(df))
            
            # แปลงเป็น numpy array
            structure_images = np.array(structure_images)
            structure_labels = np.array(structure_labels)
            content_sequences = np.array(content_sequences)
            content_labels = np.array(content_labels)
            
            # เทรนโมเดล
            structure_history = self.structure_model.fit(
                structure_images, structure_labels,
                epochs=epochs,
                batch_size=batch_size,
                validation_split=0.2
            )
            
            content_history = self.content_model.fit(
                content_sequences, content_labels,
                epochs=epochs,
                batch_size=batch_size,
                validation_split=0.2
            )
            
            return {
                "structure_accuracy": float(structure_history.history['accuracy'][-1]),
                "structure_loss": float(structure_history.history['loss'][-1]),
                "content_accuracy": float(content_history.history['accuracy'][-1]),
                "content_loss": float(content_history.history['loss'][-1])
            }
            
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการเทรนโมเดล: {str(e)}")
            raise
    
    def save_model(self):
        """
        บันทึกโมเดลและ return model ID
        
        Returns:
            str: ID ของโมเดลที่บันทึก
            
        สำหรับนักศึกษา:
        1. ศึกษาการบันทึกโมเดลและ weights
        2. สังเกตการจัดการ model ID
        3. ทดลองปรับปรุงการบันทึกโมเดล
        """
        try:
            model_id = str(uuid.uuid4())
            
            # สร้างโฟลเดอร์
            os.makedirs(f"models/{model_id}", exist_ok=True)
            
            # บันทึกโมเดล
            self.structure_model.save(f"models/{model_id}/structure_model")
            self.content_model.save(f"models/{model_id}/content_model")
            
            return model_id
            
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการบันทึกโมเดล: {str(e)}")
            raise
    
    def load_model(self, model_id):
        """
        โหลดโมเดลจาก ID
        
        Args:
            model_id: ID ของโมเดลที่ต้องการโหลด
            
        สำหรับนักศึกษา:
        1. ศึกษาการโหลดโมเดลและ weights
        2. สังเกตการตรวจสอบความถูกต้อง
        3. ทดลองปรับปรุงการโหลดโมเดล
        """
        try:
            # โหลดโมเดล
            self.structure_model = tf.keras.models.load_model(f"models/{model_id}/structure_model")
            self.content_model = tf.keras.models.load_model(f"models/{model_id}/content_model")
            
            logger.info(f"โหลดโมเดล {model_id} สำเร็จ")
            
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการโหลดโมเดล: {str(e)}")
            raise
    
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

    def analyze_trends(self, file_path: str, target_column: str) -> Dict[str, Any]:
        """
        วิเคราะห์แนวโน้มของข้อมูลด้วย Prophet
        
        Args:
            file_path: พาธของไฟล์ Excel
            target_column: คอลัมน์ที่ต้องการวิเคราะห์
            
        Returns:
            Dict: ผลการวิเคราะห์แนวโน้ม
        """
        try:
            # อ่านข้อมูล
            df = pd.read_excel(file_path)
            
            # เตรียมข้อมูลสำหรับ Prophet
            df_prophet = pd.DataFrame({
                'ds': df.index,
                'y': df[target_column]
            })
            
            # สร้างและ fit โมเดล
            model = Prophet(yearly_seasonality=True, 
                           weekly_seasonality=True,
                           daily_seasonality=True)
            model.fit(df_prophet)
            
            # สร้างช่วงเวลาสำหรับการทำนาย
            future = model.make_future_dataframe(periods=30)
            forecast = model.predict(future)
            
            return {
                "trend": forecast['trend'].tolist(),
                "forecast": forecast['yhat'].tolist(),
                "forecast_lower": forecast['yhat_lower'].tolist(),
                "forecast_upper": forecast['yhat_upper'].tolist(),
                "seasonality": {
                    "yearly": model.yearly_seasonality,
                    "weekly": model.weekly_seasonality,
                    "daily": model.daily_seasonality
                }
            }
            
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการวิเคราะห์แนวโน้ม: {str(e)}")
            raise

    def predict_future_values(self, file_path: str, target_column: str, 
                             periods: int = 30) -> Dict[str, Any]:
        """
        คาดการณ์ค่าในอนาคต
        
        Args:
            file_path: พาธของไฟล์ Excel
            target_column: คอลัมน์ที่ต้องการคาดการณ์
            periods: จำนวนช่วงเวลาที่ต้องการคาดการณ์
            
        Returns:
            Dict: ผลการคาดการณ์
        """
        try:
            # อ่านและเตรียมข้อมูล
            df = pd.read_excel(file_path)
            
            # สร้างคุณลักษณะเพิ่มเติม
            df['month'] = df.index.month
            df['day_of_week'] = df.index.dayofweek
            df['quarter'] = df.index.quarter
            
            # แบ่งข้อมูล
            X = df.drop(columns=[target_column])
            y = df[target_column]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
            
            # สร้างและเทรนโมเดล LSTM
            model = tf.keras.Sequential([
                layers.LSTM(64, return_sequences=True),
                layers.LSTM(32),
                layers.Dense(16, activation='relu'),
                layers.Dense(1)
            ])
            
            model.compile(optimizer='adam', loss='mse')
            model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2)
            
            # คาดการณ์
            future_data = self._generate_future_features(df, periods)
            predictions = model.predict(future_data)
            
            return {
                "predictions": predictions.flatten().tolist(),
                "confidence_intervals": {
                    "lower": [p - 1.96 * np.std(predictions) for p in predictions],
                    "upper": [p + 1.96 * np.std(predictions) for p in predictions]
                },
                "metrics": {
                    "mse": float(model.evaluate(X_test, y_test)),
                    "feature_importance": self._calculate_feature_importance(model, X_train)
                }
            }
            
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการคาดการณ์: {str(e)}")
            raise

    def _generate_future_features(self, df: pd.DataFrame, periods: int) -> np.ndarray:
        """สร้างคุณลักษณะสำหรับการคาดการณ์ในอนาคต"""
        last_date = df.index[-1]
        future_dates = pd.date_range(start=last_date, periods=periods + 1)[1:]
        
        future_df = pd.DataFrame(index=future_dates)
        future_df['month'] = future_df.index.month
        future_df['day_of_week'] = future_df.index.dayofweek
        future_df['quarter'] = future_df.index.quarter
        
        return future_df.values

    def _calculate_feature_importance(self, model: tf.keras.Model, 
                                    X_train: np.ndarray) -> Dict[str, float]:
        """คำนวณความสำคัญของแต่ละคุณลักษณะ"""
        importances = {}
        base_pred = model.predict(X_train)
        
        for i, col in enumerate(X_train.columns):
            X_permuted = X_train.copy()
            X_permuted[col] = np.random.permutation(X_permuted[col])
            new_pred = model.predict(X_permuted)
            importance = np.mean(np.abs(base_pred - new_pred))
            importances[col] = float(importance)
        
        return importances 