"""
ระบบติดตามประสิทธิภาพการทำงานสำหรับ Excel Processor
รองรับ:
- การวัดเวลาประมวลผล
- การติดตามการใช้ทรัพยากร
- การวิเคราะห์ประสิทธิภาพ
- การสร้างรายงานประสิทธิภาพ
"""

import time
import psutil
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import json
from functools import wraps

# ตั้งค่า logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """ระบบติดตามประสิทธิภาพการทำงาน"""
    
    def __init__(self):
        """เริ่มต้นระบบติดตามประสิทธิภาพ"""
        self.start_time = datetime.now()
        self.performance_history = []
        logger.info("เริ่มต้นระบบติดตามประสิทธิภาพเรียบร้อย")
    
    def measure_time(self, func):
        """
        Decorator สำหรับวัดเวลาการทำงานของฟังก์ชัน
        
        Args:
            func: ฟังก์ชันที่ต้องการวัดเวลา
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            start_resources = self.get_resource_usage()
            
            result = func(*args, **kwargs)
            
            end_time = time.time()
            end_resources = self.get_resource_usage()
            duration = end_time - start_time
            
            # บันทึกข้อมูลประสิทธิภาพ
            self.performance_history.append({
                'timestamp': datetime.now().isoformat(),
                'function': func.__name__,
                'duration': duration,
                'start_resources': start_resources,
                'end_resources': end_resources
            })
            
            logger.info(f"ฟังก์ชัน {func.__name__} ใช้เวลา {duration:.2f} วินาที")
            return result
        return wrapper
    
    def get_resource_usage(self) -> Dict[str, float]:
        """
        ดึงข้อมูลการใช้ทรัพยากร
        
        Returns:
            Dict: ข้อมูลการใช้ทรัพยากร
        """
        process = psutil.Process()
        return {
            'cpu_percent': process.cpu_percent(),
            'memory_percent': process.memory_percent(),
            'memory_mb': process.memory_info().rss / 1024 / 1024,
            'threads': process.num_threads()
        }
    
    def analyze_performance(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        function_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        วิเคราะห์ประสิทธิภาพการทำงาน
        
        Args:
            start_date: วันที่เริ่มต้น
            end_date: วันที่สิ้นสุด
            function_name: ชื่อฟังก์ชันที่ต้องการวิเคราะห์
            
        Returns:
            Dict: ผลการวิเคราะห์
        """
        filtered_history = self.performance_history.copy()
        
        if start_date:
            filtered_history = [
                record for record in filtered_history
                if datetime.fromisoformat(record['timestamp']) >= start_date
            ]
        
        if end_date:
            filtered_history = [
                record for record in filtered_history
                if datetime.fromisoformat(record['timestamp']) <= end_date
            ]
        
        if function_name:
            filtered_history = [
                record for record in filtered_history
                if record['function'] == function_name
            ]
        
        if not filtered_history:
            return {
                'status': 'error',
                'message': 'ไม่พบข้อมูลประสิทธิภาพ'
            }
        
        # แปลงเป็น DataFrame
        df = pd.DataFrame(filtered_history)
        
        # วิเคราะห์เวลาการทำงาน
        time_analysis = {
            'mean_duration': df['duration'].mean(),
            'max_duration': df['duration'].max(),
            'min_duration': df['duration'].min(),
            'std_duration': df['duration'].std()
        }
        
        # วิเคราะห์การใช้ทรัพยากร
        resource_analysis = {
            'mean_cpu': df['end_resources'].apply(lambda x: x['cpu_percent']).mean(),
            'mean_memory': df['end_resources'].apply(lambda x: x['memory_mb']).mean(),
            'max_memory': df['end_resources'].apply(lambda x: x['memory_mb']).max()
        }
        
        return {
            'status': 'success',
            'record_count': len(filtered_history),
            'time_analysis': time_analysis,
            'resource_analysis': resource_analysis
        }
    
    def generate_performance_report(
        self,
        output_path: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ):
        """
        สร้างรายงานประสิทธิภาพ
        
        Args:
            output_path: พาธสำหรับบันทึกรายงาน
            start_date: วันที่เริ่มต้น
            end_date: วันที่สิ้นสุด
        """
        analysis = self.analyze_performance(start_date, end_date)
        if analysis['status'] != 'success':
            logger.error("ไม่สามารถสร้างรายงานได้: ไม่มีข้อมูล")
            return
        
        # สร้างกราฟประสิทธิภาพ
        df = pd.DataFrame(self.performance_history)
        
        # กราฟเวลาการทำงาน
        fig1 = go.Figure()
        for func in df['function'].unique():
            func_data = df[df['function'] == func]
            fig1.add_trace(go.Scatter(
                x=func_data['timestamp'].apply(datetime.fromisoformat),
                y=func_data['duration'],
                name=func,
                mode='lines+markers'
            ))
        fig1.update_layout(
            title='เวลาการทำงานของแต่ละฟังก์ชัน',
            xaxis_title='เวลา',
            yaxis_title='เวลาที่ใช้ (วินาที)'
        )
        
        # กราฟการใช้ทรัพยากร
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=df['timestamp'].apply(datetime.fromisoformat),
            y=df['end_resources'].apply(lambda x: x['memory_mb']),
            name='หน่วยความจำ (MB)',
            mode='lines'
        ))
        fig2.add_trace(go.Scatter(
            x=df['timestamp'].apply(datetime.fromisoformat),
            y=df['end_resources'].apply(lambda x: x['cpu_percent']),
            name='CPU %',
            mode='lines'
        ))
        fig2.update_layout(
            title='การใช้ทรัพยากรระบบ',
            xaxis_title='เวลา',
            yaxis_title='การใช้งาน'
        )
        
        # บันทึกรายงาน
        report_path = Path(output_path)
        report_path.mkdir(parents=True, exist_ok=True)
        
        # บันทึกกราฟ
        fig1.write_html(str(report_path / 'time_analysis.html'))
        fig2.write_html(str(report_path / 'resource_analysis.html'))
        
        # สร้างรายงานสรุป
        summary = {
            'generated_at': datetime.now().isoformat(),
            'period': {
                'start': start_date.isoformat() if start_date else None,
                'end': end_date.isoformat() if end_date else None
            },
            'analysis': analysis
        }
        
        with open(report_path / 'summary.json', 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        logger.info(f"สร้างรายงานประสิทธิภาพเรียบร้อย: {output_path}")
    
    def clear_performance_history(self):
        """ล้างประวัติประสิทธิภาพ"""
        self.performance_history = []
        logger.info("ล้างประวัติประสิทธิภาพเรียบร้อย") 