"""
ระบบจัดการการ Deploy สำหรับ Excel Processor
รองรับการ Deploy หลายรูปแบบ:
- Docker
- Kubernetes
- Windows Server
- Linux Server
"""

import os
import yaml
import json
from typing import Dict, Any, Optional
import logging

# ตั้งค่า logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DeploymentConfig:
    """ระบบจัดการการ Deploy"""
    
    def __init__(self, server_type: str):
        """
        เริ่มต้นระบบ Deploy
        
        Args:
            server_type: ประเภทของ server (docker/kubernetes/windows/linux)
        """
        self.server_type = server_type.lower()
        self.config = self._load_config()
        logger.info(f"เริ่มต้นระบบ Deploy สำหรับ {server_type}")
    
    def _load_config(self) -> Dict[str, Any]:
        """โหลดการตั้งค่าจากไฟล์"""
        config_path = os.path.join("config", f"{self.server_type}_config.yml")
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"ไม่พบไฟล์ตั้งค่า {config_path} ใช้ค่าเริ่มต้น")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """สร้างการตั้งค่าเริ่มต้น"""
        return {
            "docker": {
                "image": "excel-processor:latest",
                "ports": {"8000": "8000"},
                "volumes": {"/data": "/app/data"}
            },
            "kubernetes": {
                "replicas": 3,
                "namespace": "excel-processor",
                "resources": {
                    "requests": {"cpu": "100m", "memory": "256Mi"},
                    "limits": {"cpu": "500m", "memory": "512Mi"}
                }
            },
            "windows": {
                "app_pool": "ExcelProcessorPool",
                "site_name": "ExcelProcessor",
                "port": 8000
            },
            "linux": {
                "user": "excel-processor",
                "group": "excel-processor",
                "port": 8000
            }
        }.get(self.server_type, {})
    
    def setup_server(self) -> Dict[str, Any]:
        """ตั้งค่า Server ตามประเภทที่กำหนด"""
        setup_methods = {
            "docker": self._setup_docker,
            "kubernetes": self._setup_kubernetes,
            "windows": self._setup_windows_server,
            "linux": self._setup_linux_server
        }
        
        if self.server_type not in setup_methods:
            error_msg = f"ไม่รองรับ server ประเภท {self.server_type}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}
        
        try:
            return setup_methods[self.server_type]()
        except Exception as e:
            error_msg = f"เกิดข้อผิดพลาดในการตั้งค่า: {str(e)}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}
    
    def _setup_docker(self) -> Dict[str, Any]:
        """ตั้งค่า Docker deployment"""
        try:
            # สร้าง docker-compose.yml
            compose_config = {
                "version": "3.8",
                "services": {
                    "excel-processor": {
                        "image": self.config["image"],
                        "ports": self.config["ports"],
                        "volumes": self.config["volumes"],
                        "environment": {
                            "PRODUCTION": "true",
                            "DB_URL": "${DB_URL}"
                        },
                        "restart": "always"
                    }
                }
            }
            
            with open("docker-compose.prod.yml", "w") as f:
                yaml.dump(compose_config, f)
            
            logger.info("สร้าง docker-compose.prod.yml สำเร็จ")
            return {"status": "success", "message": "ตั้งค่า Docker สำเร็จ"}
        except Exception as e:
            raise Exception(f"ข้อผิดพลาดในการตั้งค่า Docker: {str(e)}")
    
    def _setup_kubernetes(self) -> Dict[str, Any]:
        """ตั้งค่า Kubernetes deployment"""
        try:
            # สร้าง k8s deployment manifest
            k8s_config = {
                "apiVersion": "apps/v1",
                "kind": "Deployment",
                "metadata": {
                    "name": "excel-processor",
                    "namespace": self.config["namespace"]
                },
                "spec": {
                    "replicas": self.config["replicas"],
                    "selector": {
                        "matchLabels": {"app": "excel-processor"}
                    },
                    "template": {
                        "metadata": {
                            "labels": {"app": "excel-processor"}
                        },
                        "spec": {
                            "containers": [{
                                "name": "excel-processor",
                                "image": "excel-processor:prod",
                                "resources": self.config["resources"],
                                "ports": [{"containerPort": 8000}],
                                "env": [{
                                    "name": "DB_URL",
                                    "valueFrom": {
                                        "secretKeyRef": {
                                            "name": "db-secret",
                                            "key": "url"
                                        }
                                    }
                                }]
                            }]
                        }
                    }
                }
            }
            
            with open("k8s/deployment.yaml", "w") as f:
                yaml.dump(k8s_config, f)
            
            logger.info("สร้าง k8s/deployment.yaml สำเร็จ")
            return {"status": "success", "message": "ตั้งค่า Kubernetes สำเร็จ"}
        except Exception as e:
            raise Exception(f"ข้อผิดพลาดในการตั้งค่า Kubernetes: {str(e)}")
    
    def _setup_windows_server(self) -> Dict[str, Any]:
        """ตั้งค่า Windows Server"""
        try:
            # สร้างไฟล์ PowerShell script สำหรับตั้งค่า IIS
            iis_script = f"""
            Import-Module WebAdministration
            
            # สร้าง Application Pool
            New-WebAppPool -Name "{self.config['app_pool']}"
            Set-ItemProperty IIS:\AppPools\{self.config['app_pool']} -name "managedRuntimeVersion" -value "v4.0"
            
            # สร้าง Website
            New-Website -Name "{self.config['site_name']}" -Port {self.config['port']} -PhysicalPath "C:\inetpub\wwwroot\excel-processor" -ApplicationPool "{self.config['app_pool']}"
            
            # ตั้งค่า Windows Service
            $servicePath = "C:\Program Files\Python39\python.exe C:\inetpub\wwwroot\excel-processor\app.py"
            New-Service -Name "ExcelProcessor" -BinaryPathName $servicePath -DisplayName "Excel Processor Service" -StartupType Automatic
            """
            
            with open("windows_setup.ps1", "w") as f:
                f.write(iis_script)
            
            logger.info("สร้าง windows_setup.ps1 สำเร็จ")
            return {"status": "success", "message": "ตั้งค่า Windows Server สำเร็จ"}
        except Exception as e:
            raise Exception(f"ข้อผิดพลาดในการตั้งค่า Windows Server: {str(e)}")
    
    def _setup_linux_server(self) -> Dict[str, Any]:
        """ตั้งค่า Linux Server"""
        try:
            # สร้าง systemd service file
            service_config = f"""[Unit]
            Description=Excel Processor Service
            After=network.target
            
            [Service]
            User={self.config['user']}
            Group={self.config['group']}
            WorkingDirectory=/opt/excel-processor
            ExecStart=/usr/local/bin/gunicorn app:app --workers 4 --bind 0.0.0.0:{self.config['port']}
            Restart=always
            
            [Install]
            WantedBy=multi-user.target
            """
            
            with open("excel-processor.service", "w") as f:
                f.write(service_config)
            
            logger.info("สร้าง excel-processor.service สำเร็จ")
            return {"status": "success", "message": "ตั้งค่า Linux Server สำเร็จ"}
        except Exception as e:
            raise Exception(f"ข้อผิดพลาดในการตั้งค่า Linux Server: {str(e)}")
    
    def validate_config(self) -> bool:
        """ตรวจสอบความถูกต้องของการตั้งค่า"""
        required_configs = {
            "docker": ["image", "ports", "volumes"],
            "kubernetes": ["replicas", "namespace", "resources"],
            "windows": ["app_pool", "site_name", "port"],
            "linux": ["user", "group", "port"]
        }
        
        if self.server_type not in required_configs:
            logger.error(f"ไม่รองรับ server ประเภท {self.server_type}")
            return False
        
        for config in required_configs[self.server_type]:
            if config not in self.config:
                logger.error(f"ไม่พบการตั้งค่า {config} สำหรับ {self.server_type}")
                return False
        
        return True
    
    def get_deployment_status(self) -> Dict[str, Any]:
        """ตรวจสอบสถานะการ Deploy"""
        return {
            "server_type": self.server_type,
            "config_valid": self.validate_config(),
            "config": self.config
        } 