"""
ชุดทดสอบสำหรับระบบ Monitoring

สำหรับนักศึกษา:
1. ศึกษาการเขียน Unit Test ที่ครอบคลุม
2. เรียนรู้การใช้ pytest และ fixtures
3. ฝึกการจำลองข้อมูลสำหรับทดสอบ
4. ทำความเข้าใจการทดสอบแบบ async
"""

import pytest
from datetime import datetime, timedelta
import json
from pathlib import Path
from unittest.mock import Mock, patch
import tempfile
import os

from monitoring.system_monitor import SystemMonitor
from monitoring.alert_manager import AlertManager
from monitoring.performance_monitor import PerformanceMonitor

# --------------- Fixtures ---------------

@pytest.fixture
def temp_dir():
    """
    สร้างโฟลเดอร์ชั่วคราวสำหรับทดสอบ
    
    สำหรับนักศึกษา:
    - ใช้ tempfile.mkdtemp() สร้างโฟลเดอร์ชั่วคราว
    - ใช้ yield เพื่อคืนค่าและทำความสะอาดหลังเสร็จ
    - ศึกษาการใช้ with ในการจัดการทรัพยากร
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

@pytest.fixture
def mock_config():
    """
    สร้าง config จำลองสำหรับทดสอบ
    
    สำหรับนักศึกษา:
    - เรียนรู้การสร้างข้อมูลจำลอง
    - ทำความเข้าใจการตั้งค่าระบบ
    - ศึกษาการใช้ environment variables
    """
    return {
        'line_token': 'test_token',
        'smtp_server': 'test.smtp.com',
        'smtp_port': 587,
        'email_user': 'test@example.com',
        'email_password': 'test_password',
        'slack_webhook': 'https://test.slack.com/webhook',
        'alert_levels': ['INFO', 'WARNING', 'ERROR', 'CRITICAL']
    }

@pytest.fixture
def alert_manager(mock_config, temp_dir):
    """
    สร้าง AlertManager instance สำหรับทดสอบ
    
    สำหรับนักศึกษา:
    - ศึกษาการใช้ fixtures ร่วมกัน
    - เรียนรู้การ mock ระบบแจ้งเตือน
    - ทำความเข้าใจการจัดการ config
    """
    config_path = Path(temp_dir) / 'config.json'
    with open(config_path, 'w') as f:
        json.dump(mock_config, f)
    return AlertManager(str(config_path))

@pytest.fixture
def performance_monitor():
    """
    สร้าง PerformanceMonitor instance สำหรับทดสอบ
    
    สำหรับนักศึกษา:
    - เรียนรู้การสร้าง instance สำหรับทดสอบ
    - ศึกษาการจัดการประวัติประสิทธิภาพ
    - ทำความเข้าใจการวัดประสิทธิภาพ
    """
    return PerformanceMonitor()

@pytest.fixture
def system_monitor():
    """
    สร้าง SystemMonitor instance สำหรับทดสอบ
    
    สำหรับนักศึกษา:
    - เรียนรู้การ mock ระบบ metrics
    - ศึกษาการจำลองทรัพยากรระบบ
    - ทำความเข้าใจการติดตามระบบ
    """
    return SystemMonitor()

# --------------- Alert Manager Tests ---------------

def test_alert_manager_init(alert_manager, mock_config):
    """
    ทดสอบการเริ่มต้น AlertManager
    
    สำหรับนักศึกษา:
    - ตรวจสอบการโหลด config
    - ทดสอบค่าเริ่มต้น
    - ศึกษาการเขียน assertions
    """
    assert alert_manager.config['line_token'] == mock_config['line_token']
    assert alert_manager.config['smtp_server'] == mock_config['smtp_server']
    assert len(alert_manager.alert_history) == 0

@pytest.mark.asyncio
async def test_send_line_notification(alert_manager):
    """
    ทดสอบการส่งแจ้งเตือนผ่าน Line
    
    สำหรับนักศึกษา:
    - เรียนรู้การ mock HTTP requests
    - ศึกษาการทดสอบ async functions
    - ทำความเข้าใจการจัดการ exceptions
    """
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        result = alert_manager.send_line_notification("Test message")
        assert result == True
        mock_post.assert_called_once()

def test_send_email_notification(alert_manager):
    """
    ทดสอบการส่งแจ้งเตือนผ่าน Email
    
    สำหรับนักศึกษา:
    - เรียนรู้การ mock SMTP
    - ศึกษาการทดสอบการส่งอีเมล
    - ทำความเข้าใจการจัดการ credentials
    """
    with patch('smtplib.SMTP') as mock_smtp:
        result = alert_manager.send_email_notification(
            "Test Subject",
            "Test Message",
            "test@example.com"
        )
        assert result == True
        mock_smtp.assert_called_once()

# --------------- Performance Monitor Tests ---------------

def test_measure_time_decorator(performance_monitor):
    """
    ทดสอบ decorator วัดเวลา
    
    สำหรับนักศึกษา:
    - เรียนรู้การทดสอบ decorators
    - ศึกษาการวัดเวลาการทำงาน
    - ทำความเข้าใจการใช้ wraps
    """
    @performance_monitor.measure_time
    def test_function():
        return "test"
    
    result = test_function()
    assert result == "test"
    assert len(performance_monitor.performance_history) == 1
    assert 'duration' in performance_monitor.performance_history[0]

def test_analyze_performance(performance_monitor):
    """
    ทดสอบการวิเคราะห์ประสิทธิภาพ
    
    สำหรับนักศึกษา:
    - เรียนรู้การวิเคราะห์ข้อมูล
    - ศึกษาการใช้ pandas
    - ทำความเข้าใจการคำนวณสถิติ
    """
    # จำลองข้อมูลประวัติ
    performance_monitor.performance_history = [
        {
            'timestamp': datetime.now().isoformat(),
            'function': 'test_func',
            'duration': 1.5,
            'start_resources': {'cpu_percent': 10, 'memory_mb': 100},
            'end_resources': {'cpu_percent': 20, 'memory_mb': 150}
        }
    ]
    
    result = performance_monitor.analyze_performance()
    assert result['status'] == 'success'
    assert 'time_analysis' in result
    assert 'resource_analysis' in result

# --------------- System Monitor Tests ---------------

def test_system_metrics(system_monitor):
    """
    ทดสอบการเก็บ metrics ของระบบ
    
    สำหรับนักศึกษา:
    - เรียนรู้การใช้ psutil
    - ศึกษาการติดตามทรัพยากร
    - ทำความเข้าใจการทำงานของ Prometheus
    """
    metrics = system_monitor.get_system_metrics()
    assert 'cpu_percent' in metrics
    assert 'memory_percent' in metrics
    assert 'disk_percent' in metrics

def test_generate_report(system_monitor, temp_dir):
    """
    ทดสอบการสร้างรายงาน
    
    สำหรับนักศึกษา:
    - เรียนรู้การสร้างรายงาน
    - ศึกษาการใช้ Plotly
    - ทำความเข้าใจการจัดการไฟล์
    """
    system_monitor.generate_report(temp_dir)
    assert Path(temp_dir, 'system_metrics.html').exists()
    assert Path(temp_dir, 'summary.json').exists()

# --------------- Integration Tests ---------------

def test_monitoring_integration(
    system_monitor,
    alert_manager,
    performance_monitor,
    temp_dir
):
    """
    ทดสอบการทำงานร่วมกันของระบบ monitoring
    
    สำหรับนักศึกษา:
    - เรียนรู้การทดสอบแบบ integration
    - ศึกษาการทำงานร่วมกันของระบบ
    - ทำความเข้าใจการจัดการ dependencies
    """
    # ทดสอบการติดตามระบบและแจ้งเตือน
    metrics = system_monitor.get_system_metrics()
    if metrics['cpu_percent'] > 80:
        alert_manager.send_alert(
            'WARNING',
            'High CPU Usage',
            f"CPU usage is {metrics['cpu_percent']}%",
            ['email', 'line']
        )
    
    # ทดสอบการวัดประสิทธิภาพและสร้างรายงาน
    @performance_monitor.measure_time
    def test_function():
        return system_monitor.get_system_metrics()
    
    test_function()
    performance_monitor.generate_performance_report(temp_dir)
    
    # ตรวจสอบผลลัพธ์
    assert len(performance_monitor.performance_history) > 0
    assert Path(temp_dir, 'time_analysis.html').exists() 