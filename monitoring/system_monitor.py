"""
ระบบติดตามการทำงานของระบบ (System Monitor)

สำหรับนักศึกษา:
1. ศึกษาการใช้ psutil ในการติดตามทรัพยากรระบบ
2. เรียนรู้การสร้างกราฟด้วย Plotly
3. ทำความเข้าใจการทำงานของ Prometheus
4. ฝึกการจัดการ metrics และการสร้างรายงาน
"""

import psutil
import json
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, List, Any, Optional
import logging
from prometheus_client import start_http_server, Gauge
import numpy as np
import time
import threading
from dataclasses import dataclass
from enum import Enum

# ตั้งค่า logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AlertLevel(Enum):
    """
    ระดับความสำคัญของการแจ้งเตือน
    
    สำหรับนักศึกษา:
    - ศึกษาการใช้ Enum
    - เรียนรู้การกำหนดระดับความสำคัญ
    """
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"

@dataclass
class AlertThreshold:
    """
    เกณฑ์การแจ้งเตือน
    
    สำหรับนักศึกษา:
    - ศึกษาการใช้ dataclass
    - เรียนรู้การกำหนดเกณฑ์
    """
    warning: float
    critical: float
    check_interval: int = 60  # ตรวจสอบทุก 60 วินาที
    consecutive_checks: int = 3  # จำนวนครั้งที่ต้องเกินเกณฑ์ติดต่อกัน

@dataclass
class Alert:
    """
    ข้อมูลการแจ้งเตือน
    
    สำหรับนักศึกษา:
    - เรียนรู้การเก็บข้อมูลการแจ้งเตือน
    - ศึกษาการจัดการเวลา
    """
    timestamp: datetime
    level: AlertLevel
    message: str
    metric_name: str
    metric_value: float
    threshold: float

class SystemMonitor:
    """
    ระบบติดตามการทำงานของระบบ
    
    สำหรับนักศึกษา:
    - ศึกษาการใช้ psutil ในการติดตามทรัพยากร
    - เรียนรู้การสร้างกราฟและรายงาน
    - ทำความเข้าใจการจัดเก็บ metrics
    """
    
    def __init__(self, collection_interval: int = 60):
        """
        เริ่มต้นระบบติดตาม
        
        Args:
            collection_interval: ระยะเวลาในการเก็บข้อมูล (วินาที)
            
        สำหรับนักศึกษา:
        - เรียนรู้การตั้งค่า Prometheus metrics
        - ศึกษาการเก็บประวัติข้อมูล
        - ทำความเข้าใจการใช้ Gauge
        """
        # Prometheus metrics
        self.cpu_gauge = Gauge('system_cpu_percent', 'CPU usage in percent')
        self.memory_gauge = Gauge('system_memory_percent', 'Memory usage in percent')
        self.disk_gauge = Gauge('system_disk_percent', 'Disk usage in percent')
        self.network_in_gauge = Gauge('system_network_in_bytes', 'Network bytes received')
        self.network_out_gauge = Gauge('system_network_out_bytes', 'Network bytes sent')
        
        # ประวัติ metrics
        self.metrics_history: List[Dict[str, Any]] = []
        self.max_history_size = 1000  # เก็บข้อมูลล่าสุด 1000 จุด
        
        # ตั้งค่าการเก็บข้อมูล
        self.collection_interval = collection_interval
        self.is_collecting = False
        self.collection_thread = None
        
        # เก็บค่าเครือข่ายล่าสุด
        self._last_net_io = psutil.net_io_counters()
        self._last_net_time = time.time()
        
        # เพิ่ม attributes สำหรับการแจ้งเตือน
        self.alert_thresholds = {
            'cpu': AlertThreshold(warning=70, critical=85),
            'memory': AlertThreshold(warning=75, critical=90),
            'disk': AlertThreshold(warning=80, critical=95),
            'network': AlertThreshold(warning=80, critical=90)
        }
        
        self.alert_history: List[Alert] = []
        self.consecutive_alerts = {
            'cpu': 0,
            'memory': 0,
            'disk': 0,
            'network': 0
        }
        
        self.alert_callbacks = []
        
        # เพิ่ม Prometheus metrics สำหรับการแจ้งเตือน
        self.alert_gauge = Gauge('system_alerts_total', 'Total number of active alerts')
        
        logger.info(f"เริ่มต้นระบบติดตามด้วยระยะเวลาเก็บข้อมูล {collection_interval} วินาที")
    
    def start_collecting(self):
        """
        เริ่มการเก็บข้อมูลอัตโนมัติ
        
        สำหรับนักศึกษา:
        - ศึกษาการใช้ threading
        - เรียนรู้การทำงานแบบ background
        - ทำความเข้าใจการจัดการ resources
        """
        if not self.is_collecting:
            self.is_collecting = True
            self.collection_thread = threading.Thread(target=self._collect_metrics)
            self.collection_thread.daemon = True
            self.collection_thread.start()
            logger.info("เริ่มการเก็บข้อมูลอัตโนมัติ")
    
    def stop_collecting(self):
        """
        หยุดการเก็บข้อมูลอัตโนมัติ
        
        สำหรับนักศึกษา:
        - เรียนรู้การจัดการ thread
        - ศึกษาการทำความสะอาดทรัพยากร
        """
        self.is_collecting = False
        if self.collection_thread:
            self.collection_thread.join()
        logger.info("หยุดการเก็บข้อมูลอัตโนมัติ")
    
    def _collect_metrics(self):
        """
        ฟังก์ชันสำหรับเก็บข้อมูลต่อเนื่อง
        
        สำหรับนักศึกษา:
        - เรียนรู้การทำงานแบบ loop
        - ศึกษาการจัดการ exceptions
        - ทำความเข้าใจการใช้ threading
        """
        while self.is_collecting:
            try:
                self.get_system_metrics()
                time.sleep(self.collection_interval)
            except Exception as e:
                logger.error(f"เกิดข้อผิดพลาดในการเก็บข้อมูล: {str(e)}")
    
    def get_system_metrics(self) -> Dict[str, float]:
        """
        เก็บข้อมูล metrics ของระบบ
        
        Returns:
            Dict[str, float]: metrics ของระบบ
            
        สำหรับนักศึกษา:
        - ศึกษาการใช้ psutil
        - เรียนรู้การคำนวณการใช้ทรัพยากร
        - ทำความเข้าใจหน่วยวัดต่างๆ
        """
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_freq = psutil.cpu_freq()
            cpu_count = psutil.cpu_count()
            
            # Memory
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            # Disk
            disk = psutil.disk_usage('/')
            disk_io = psutil.disk_io_counters()
            
            # Network
            current_net = psutil.net_io_counters()
            current_time = time.time()
            
            # คำนวณ network throughput
            time_diff = current_time - self._last_net_time
            bytes_sent = (current_net.bytes_sent - self._last_net_io.bytes_sent) / time_diff
            bytes_recv = (current_net.bytes_recv - self._last_net_io.bytes_recv) / time_diff
            
            # อัพเดทค่าล่าสุด
            self._last_net_io = current_net
            self._last_net_time = current_time
            
            # สร้าง metrics
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'cpu': {
                    'percent': cpu_percent,
                    'freq_current': cpu_freq.current,
                    'freq_max': cpu_freq.max,
                    'count': cpu_count
                },
                'memory': {
                    'percent': memory.percent,
                    'used_mb': memory.used / (1024 * 1024),
                    'total_mb': memory.total / (1024 * 1024),
                    'swap_percent': swap.percent
                },
                'disk': {
                    'percent': disk.percent,
                    'used_gb': disk.used / (1024**3),
                    'total_gb': disk.total / (1024**3),
                    'read_mb': disk_io.read_bytes / (1024 * 1024),
                    'write_mb': disk_io.write_bytes / (1024 * 1024)
                },
                'network': {
                    'bytes_sent_per_sec': bytes_sent,
                    'bytes_recv_per_sec': bytes_recv,
                    'packets_sent': current_net.packets_sent,
                    'packets_recv': current_net.packets_recv
                }
            }
            
            # อัพเดท Prometheus metrics
            self.cpu_gauge.set(cpu_percent)
            self.memory_gauge.set(memory.percent)
            self.disk_gauge.set(disk.percent)
            self.network_in_gauge.set(bytes_recv)
            self.network_out_gauge.set(bytes_sent)
            
            # เก็บประวัติ
            self.metrics_history.append(metrics)
            if len(self.metrics_history) > self.max_history_size:
                self.metrics_history.pop(0)
            
            # เพิ่มการตรวจสอบการแจ้งเตือน
            self._check_alerts(metrics)
            
            logger.debug(f"เก็บ metrics เรียบร้อย: {metrics}")
            return metrics
            
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการเก็บ metrics: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def analyze_metrics(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        วิเคราะห์ metrics ย้อนหลัง
        
        Args:
            start_time: เวลาเริ่มต้นที่ต้องการวิเคราะห์
            end_time: เวลาสิ้นสุดที่ต้องการวิเคราะห์
            
        Returns:
            Dict[str, Any]: ผลการวิเคราะห์
            
        สำหรับนักศึกษา:
        - เรียนรู้การวิเคราะห์ข้อมูลด้วย pandas
        - ศึกษาการคำนวณสถิติ
        - ทำความเข้าใจการกรองข้อมูลตามช่วงเวลา
        """
        try:
            # แปลงประวัติเป็น DataFrame
            df = pd.DataFrame(self.metrics_history)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # กรองตามช่วงเวลา
            if start_time:
                df = df[df['timestamp'] >= start_time]
            if end_time:
                df = df[df['timestamp'] <= end_time]
            
            if len(df) == 0:
                return {
                    'status': 'error',
                    'error': 'ไม่พบข้อมูลในช่วงเวลาที่ระบุ'
                }
            
            # วิเคราะห์แต่ละส่วน
            analysis = {
                'cpu': {
                    'mean': df['cpu.percent'].mean(),
                    'max': df['cpu.percent'].max(),
                    'min': df['cpu.percent'].min(),
                    'std': df['cpu.percent'].std(),
                    'peak_times': df[df['cpu.percent'] > 80]['timestamp'].tolist()
                },
                'memory': {
                    'mean': df['memory.percent'].mean(),
                    'max': df['memory.percent'].max(),
                    'min': df['memory.percent'].min(),
                    'std': df['memory.percent'].std(),
                    'peak_times': df[df['memory.percent'] > 80]['timestamp'].tolist()
                },
                'disk': {
                    'mean': df['disk.percent'].mean(),
                    'max': df['disk.percent'].max(),
                    'min': df['disk.percent'].min(),
                    'std': df['disk.percent'].std(),
                    'usage_trend': np.polyfit(range(len(df)), df['disk.percent'], 1)[0]
                },
                'network': {
                    'mean_in': df['network.bytes_recv_per_sec'].mean(),
                    'mean_out': df['network.bytes_sent_per_sec'].mean(),
                    'max_in': df['network.bytes_recv_per_sec'].max(),
                    'max_out': df['network.bytes_sent_per_sec'].max()
                }
            }
            
            # คำนวณแนวโน้ม
            analysis['trends'] = {
                'cpu_trend': np.polyfit(range(len(df)), df['cpu.percent'], 1)[0],
                'memory_trend': np.polyfit(range(len(df)), df['memory.percent'], 1)[0],
                'disk_trend': np.polyfit(range(len(df)), df['disk.percent'], 1)[0]
            }
            
            logger.info("วิเคราะห์ metrics เรียบร้อย")
            return {
                'status': 'success',
                'analysis': analysis,
                'period': {
                    'start': df['timestamp'].min().isoformat(),
                    'end': df['timestamp'].max().isoformat(),
                    'points': len(df)
                }
            }
            
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการวิเคราะห์: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def generate_report(self, output_dir: str) -> Dict[str, str]:
        """
        สร้างรายงานและกราฟ
        
        Args:
            output_dir: โฟลเดอร์สำหรับบันทึกรายงาน
            
        Returns:
            Dict[str, str]: พาธของไฟล์รายงาน
            
        สำหรับนักศึกษา:
        - เรียนรู้การสร้างกราฟด้วย Plotly
        - ศึกษาการสร้างรายงาน HTML
        - ทำความเข้าใจการจัดการไฟล์
        """
        try:
            # สร้างโฟลเดอร์ถ้ายังไม่มี
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # แปลงข้อมูลเป็น DataFrame
            df = pd.DataFrame(self.metrics_history)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # สร้างกราฟ CPU, Memory, Disk
            fig = go.Figure()
            
            # CPU Usage
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['cpu.percent'],
                name='CPU Usage',
                line=dict(color='red')
            ))
            
            # Memory Usage
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['memory.percent'],
                name='Memory Usage',
                line=dict(color='blue')
            ))
            
            # Disk Usage
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['disk.percent'],
                name='Disk Usage',
                line=dict(color='green')
            ))
            
            # ปรับแต่งกราฟ
            fig.update_layout(
                title='System Resource Usage',
                xaxis_title='Time',
                yaxis_title='Usage (%)',
                hovermode='x unified'
            )
            
            # บันทึกกราฟ
            metrics_path = output_path / 'system_metrics.html'
            fig.write_html(str(metrics_path))
            
            # สร้างกราฟ Network
            net_fig = go.Figure()
            
            # Network In
            net_fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['network.bytes_recv_per_sec'],
                name='Network In',
                line=dict(color='purple')
            ))
            
            # Network Out
            net_fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['network.bytes_sent_per_sec'],
                name='Network Out',
                line=dict(color='orange')
            ))
            
            # ปรับแต่งกราฟ
            net_fig.update_layout(
                title='Network Usage',
                xaxis_title='Time',
                yaxis_title='Bytes per second',
                hovermode='x unified'
            )
            
            # บันทึกกราฟ
            network_path = output_path / 'network_metrics.html'
            net_fig.write_html(str(network_path))
            
            # สร้างรายงานสรุป
            analysis = self.analyze_metrics()
            summary_path = output_path / 'summary.json'
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            
            logger.info(f"สร้างรายงานเรียบร้อย: {output_dir}")
            return {
                'metrics_graph': str(metrics_path),
                'network_graph': str(network_path),
                'summary_report': str(summary_path)
            }
            
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการสร้างรายงาน: {str(e)}")
            return {
                'error': str(e)
            }
    
    def start_prometheus_server(self, port: int = 8000):
        """
        เริ่ม Prometheus metrics server
        
        Args:
            port: พอร์ตที่ต้องการใช้
            
        สำหรับนักศึกษา:
        - เรียนรู้การใช้ Prometheus
        - ศึกษาการเปิด HTTP server
        - ทำความเข้าใจ metrics exposition
        """
        try:
            start_http_server(port)
            logger.info(f"เริ่ม Prometheus server ที่พอร์ต {port}")
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการเริ่ม Prometheus server: {str(e)}")
    
    def clear_history(self):
        """
        ล้างประวัติ metrics
        
        สำหรับนักศึกษา:
        - เรียนรู้การจัดการหน่วยความจำ
        - ศึกษาการทำความสะอาดข้อมูล
        """
        self.metrics_history.clear()
        logger.info("ล้างประวัติ metrics เรียบร้อย")
    
    def add_alert_callback(self, callback):
        """
        เพิ่ม callback function สำหรับการแจ้งเตือน
        
        Args:
            callback: ฟังก์ชันที่จะถูกเรียกเมื่อมีการแจ้งเตือน
            
        สำหรับนักศึกษา:
        - เรียนรู้การใช้ callbacks
        - ศึกษาการส่งการแจ้งเตือน
        """
        self.alert_callbacks.append(callback)
    
    def set_alert_threshold(
        self,
        metric: str,
        warning: float,
        critical: float,
        check_interval: int = 60,
        consecutive_checks: int = 3
    ):
        """
        ตั้งค่าเกณฑ์การแจ้งเตือน
        
        Args:
            metric: ชื่อ metric ที่ต้องการตั้งค่า
            warning: เกณฑ์ระดับ warning
            critical: เกณฑ์ระดับ critical
            check_interval: ระยะเวลาในการตรวจสอบ (วินาที)
            consecutive_checks: จำนวนครั้งที่ต้องเกินเกณฑ์ติดต่อกัน
            
        สำหรับนักศึกษา:
        - เรียนรู้การตั้งค่าเกณฑ์
        - ศึกษาการตรวจสอบค่า
        """
        if metric not in self.alert_thresholds:
            raise ValueError(f"ไม่พบ metric: {metric}")
            
        self.alert_thresholds[metric] = AlertThreshold(
            warning=warning,
            critical=critical,
            check_interval=check_interval,
            consecutive_checks=consecutive_checks
        )
        logger.info(f"ตั้งค่าเกณฑ์การแจ้งเตือนสำหรับ {metric} เรียบร้อย")
    
    def _check_alerts(self, metrics: Dict[str, Any]):
        """
        ตรวจสอบและสร้างการแจ้งเตือน
        
        Args:
            metrics: ข้อมูล metrics ที่ต้องการตรวจสอบ
            
        สำหรับนักศึกษา:
        - เรียนรู้การตรวจสอบเงื่อนไข
        - ศึกษาการสร้างการแจ้งเตือน
        """
        # ตรวจสอบ CPU
        cpu_percent = metrics['cpu']['percent']
        self._check_metric_threshold(
            'cpu',
            cpu_percent,
            f"CPU usage is {cpu_percent}%"
        )
        
        # ตรวจสอบ Memory
        memory_percent = metrics['memory']['percent']
        self._check_metric_threshold(
            'memory',
            memory_percent,
            f"Memory usage is {memory_percent}%"
        )
        
        # ตรวจสอบ Disk
        disk_percent = metrics['disk']['percent']
        self._check_metric_threshold(
            'disk',
            disk_percent,
            f"Disk usage is {disk_percent}%"
        )
        
        # ตรวจสอบ Network (ถ้ามีการใช้งานสูง)
        network_usage = max(
            metrics['network']['bytes_sent_per_sec'],
            metrics['network']['bytes_recv_per_sec']
        ) / (1024 * 1024)  # แปลงเป็น MB/s
        self._check_metric_threshold(
            'network',
            network_usage,
            f"Network usage is {network_usage:.2f} MB/s"
        )
    
    def _check_metric_threshold(
        self,
        metric_name: str,
        value: float,
        message: str
    ):
        """
        ตรวจสอบค่ากับเกณฑ์และสร้างการแจ้งเตือน
        
        Args:
            metric_name: ชื่อ metric
            value: ค่าที่ต้องการตรวจสอบ
            message: ข้อความแจ้งเตือน
            
        สำหรับนักศึกษา:
        - เรียนรู้การตรวจสอบเกณฑ์
        - ศึกษาการนับจำนวนครั้ง
        - ทำความเข้าใจการสร้างการแจ้งเตือน
        """
        threshold = self.alert_thresholds[metric_name]
        
        if value >= threshold.critical:
            self.consecutive_alerts[metric_name] += 1
            if self.consecutive_alerts[metric_name] >= threshold.consecutive_checks:
                self._create_alert(
                    AlertLevel.CRITICAL,
                    f"CRITICAL: {message}",
                    metric_name,
                    value,
                    threshold.critical
                )
        elif value >= threshold.warning:
            self.consecutive_alerts[metric_name] += 1
            if self.consecutive_alerts[metric_name] >= threshold.consecutive_checks:
                self._create_alert(
                    AlertLevel.WARNING,
                    f"WARNING: {message}",
                    metric_name,
                    value,
                    threshold.warning
                )
        else:
            self.consecutive_alerts[metric_name] = 0
    
    def _create_alert(
        self,
        level: AlertLevel,
        message: str,
        metric_name: str,
        metric_value: float,
        threshold: float
    ):
        """
        สร้างและส่งการแจ้งเตือน
        
        Args:
            level: ระดับความสำคัญ
            message: ข้อความแจ้งเตือน
            metric_name: ชื่อ metric
            metric_value: ค่าที่เกินเกณฑ์
            threshold: เกณฑ์ที่ใช้
            
        สำหรับนักศึกษา:
        - เรียนรู้การสร้างการแจ้งเตือน
        - ศึกษาการเรียกใช้ callbacks
        - ทำความเข้าใจการจัดการประวัติ
        """
        alert = Alert(
            timestamp=datetime.now(),
            level=level,
            message=message,
            metric_name=metric_name,
            metric_value=metric_value,
            threshold=threshold
        )
        
        # เก็บประวัติ
        self.alert_history.append(alert)
        
        # อัพเดท Prometheus metric
        self.alert_gauge.inc()
        
        # เรียก callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                logger.error(f"เกิดข้อผิดพลาดในการเรียก alert callback: {str(e)}")
        
        logger.warning(f"สร้างการแจ้งเตือน: {message}")
    
    def get_alerts(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        level: Optional[AlertLevel] = None
    ) -> List[Alert]:
        """
        ดึงประวัติการแจ้งเตือน
        
        Args:
            start_time: เวลาเริ่มต้น
            end_time: เวลาสิ้นสุด
            level: ระดับความสำคัญที่ต้องการ
            
        Returns:
            List[Alert]: รายการการแจ้งเตือน
            
        สำหรับนักศึกษา:
        - เรียนรู้การกรองข้อมูล
        - ศึกษาการจัดการเวลา
        """
        alerts = self.alert_history
        
        if start_time:
            alerts = [a for a in alerts if a.timestamp >= start_time]
        if end_time:
            alerts = [a for a in alerts if a.timestamp <= end_time]
        if level:
            alerts = [a for a in alerts if a.level == level]
        
        return alerts
    
    def clear_alerts(self):
        """
        ล้างประวัติการแจ้งเตือน
        
        สำหรับนักศึกษา:
        - เรียนรู้การจัดการประวัติ
        - ศึกษาการทำความสะอาดข้อมูล
        """
        self.alert_history.clear()
        self.alert_gauge.set(0)
        logger.info("ล้างประวัติการแจ้งเตือนเรียบร้อย") 