"""
Excel Template Web Application
----------------------------
เว็บแอปพลิเคชันสำหรับจัดการเทมเพลตและข้อมูล Excel

ระบบนี้ถูกออกแบบมาเพื่อ:
1. จัดการเทมเพลตและข้อมูลผ่าน Web UI
2. แสดงตัวอย่างเอกสารแบบ Real-time
3. พิมพ์เอกสารโดยตรงจากระบบ

Author: ZanKinZuiTH
Version: 1.0.0
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import uvicorn
import logging
from template_manager import TemplateManager
from printer import PrintManager
import json
from typing import Optional, Dict, Any
import tempfile
import shutil

# ตั้งค่า logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# สร้าง FastAPI app
app = FastAPI(
    title="Excel Template System",
    description="ระบบจัดการเทมเพลตและข้อมูล Excel",
    version="1.0.0"
)

# ตั้งค่าโฟลเดอร์สำหรับไฟล์ static
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/previews", StaticFiles(directory="previews"), name="previews")

# ตั้งค่า templates
templates = Jinja2Templates(directory="templates")

# สร้าง instance ของ manager
template_manager = TemplateManager()
print_manager = PrintManager()

@app.get("/")
async def home(request: Request):
    """หน้าหลักของระบบ"""
    templates_list = template_manager.list_templates()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "templates": templates_list}
    )

@app.post("/templates/upload")
async def upload_template(
    file: UploadFile = File(...),
    name: str = Form(...),
    description: str = Form(...)
):
    """อัพโหลดไฟล์ Excel เพื่อสร้างเทมเพลตใหม่"""
    try:
        # บันทึกไฟล์ชั่วคราว
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name
        
        # แยกและบันทึกเทมเพลต
        template_data = template_manager.extract_template(temp_path, name, description)
        template_id = template_manager.save_template(template_data)
        
        # ลบไฟล์ชั่วคราว
        Path(temp_path).unlink()
        
        return {"template_id": template_id, "message": "อัพโหลดเทมเพลตเรียบร้อย"}
    except Exception as e:
        logger.error(f"เกิดข้อผิดพลาดในการอัพโหลดเทมเพลต: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/templates/{template_id}")
async def get_template_details(request: Request, template_id: int):
    """แสดงรายละเอียดของเทมเพลต"""
    template = template_manager.get_template(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="ไม่พบเทมเพลต")
    
    data_entries = template_manager.list_data_entries(template_id)
    return templates.TemplateResponse(
        "template_details.html",
        {
            "request": request,
            "template": template,
            "data_entries": data_entries
        }
    )

@app.post("/data/save/{template_id}")
async def save_data(template_id: int, data: Dict[str, Any]):
    """บันทึกข้อมูลใหม่"""
    try:
        entry_id = template_manager.save_data_entry(template_id, data)
        return {"entry_id": entry_id, "message": "บันทึกข้อมูลเรียบร้อย"}
    except Exception as e:
        logger.error(f"เกิดข้อผิดพลาดในการบันทึกข้อมูล: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/preview/{template_id}")
async def preview_template(
    template_id: int,
    data: Optional[Dict[str, Any]] = None
):
    """สร้างตัวอย่างเอกสาร"""
    try:
        preview_path = template_manager.create_preview(template_id, data or {})
        return FileResponse(preview_path)
    except Exception as e:
        logger.error(f"เกิดข้อผิดพลาดในการสร้างตัวอย่าง: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/print/{template_id}")
async def print_document(
    template_id: int,
    data: Dict[str, Any],
    printer_name: Optional[str] = None
):
    """พิมพ์เอกสาร"""
    try:
        # ตั้งค่าเครื่องพิมพ์ (ถ้าระบุ)
        if printer_name:
            print_manager.set_printer(printer_name)
        
        # สร้างไฟล์ตัวอย่างและส่งไปพิมพ์
        preview_path = template_manager.create_preview(template_id, data)
        success = print_manager.print_file(preview_path)
        
        if success:
            return {"message": "ส่งงานพิมพ์เรียบร้อย"}
        else:
            raise HTTPException(status_code=500, detail="เกิดข้อผิดพลาดในการพิมพ์")
    except Exception as e:
        logger.error(f"เกิดข้อผิดพลาดในการพิมพ์: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/printers")
async def list_printers():
    """แสดงรายการเครื่องพิมพ์ที่ใช้งานได้"""
    return {"printers": print_manager.get_available_printers()}

if __name__ == "__main__":
    # สร้างโฟลเดอร์ที่จำเป็น
    Path("static").mkdir(exist_ok=True)
    Path("templates").mkdir(exist_ok=True)
    Path("previews").mkdir(exist_ok=True)
    
    # รัน server
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 