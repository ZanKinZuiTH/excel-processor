from fastapi import FastAPI, UploadFile, File, HTTPException, status
from main import ExcelProcessor
from printer import PrintManager
from template_manager import TemplateManager
import tempfile
import os
import uvicorn
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
import logging

# ตั้งค่า logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Excel Processor API",
    description="ระบบประมวลผลและจัดการเทมเพลต Excel อัจฉริยะ",
    version="1.0.0"
)

# สร้าง instances ที่ใช้งานร่วมกัน
print_manager = PrintManager()
template_manager = TemplateManager()

class Template(BaseModel):
    name: str
    structure: dict

class PrintJob(BaseModel):
    data: dict
    template_name: Optional[str] = None

class TemplateShare(BaseModel):
    user_ids: List[str]
    permissions: Optional[Dict[str, bool]] = None

class TemplateVersion(BaseModel):
    changes: Dict[str, Any]
    version_note: Optional[str] = None

class SystemStatus(BaseModel):
    """สถานะของระบบ"""
    status: str
    version: str
    components: Dict[str, bool]
    template_count: int
    printer_count: int

@app.post("/process-excel/")
async def process_excel_file(file: UploadFile = File(...)):
    """อัปโหลดและประมวลผลไฟล์ Excel"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_file_path = temp_file.name

    try:
        processor = ExcelProcessor(temp_file_path)
        result = processor.process_file()
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        os.unlink(temp_file_path)

@app.post("/save-template/")
async def save_template(template: Template):
    """บันทึกเทมเพลต"""
    try:
        processor = ExcelProcessor("")  # สร้างอินสแตนซ์เปล่า
        processor.save_as_template(template.name, template.structure)
        return {"status": "success", "message": f"บันทึกเทมเพลต {template.name} เรียบร้อยแล้ว"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/printers/")
async def get_printers() -> List[str]:
    """รับรายชื่อเครื่องพิมพ์ที่มีในระบบ"""
    return print_manager.get_available_printers()

@app.post("/set-printer/{printer_name}")
async def set_printer(printer_name: str):
    """เลือกเครื่องพิมพ์ที่จะใช้งาน"""
    if print_manager.set_printer(printer_name):
        return {"status": "success", "message": f"เลือกเครื่องพิมพ์ {printer_name} เรียบร้อยแล้ว"}
    raise HTTPException(status_code=400, detail=f"ไม่พบเครื่องพิมพ์ {printer_name}")

@app.post("/print/")
async def print_document(print_job: PrintJob):
    """พิมพ์เอกสาร"""
    try:
        if print_job.template_name:
            # TODO: ดึงข้อมูลเทมเพลตจากฐานข้อมูล
            template_formatting = {}  # ต้องดึงจากฐานข้อมูล
        else:
            template_formatting = None
        
        print_manager.add_to_queue(print_job.data, template_formatting)
        print_manager.print_all()
        return {"status": "success", "message": "ส่งงานพิมพ์เรียบร้อยแล้ว"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Excel Processor API is running"}

@app.post("/templates/{template_id}/share")
async def share_template(template_id: str, share_data: TemplateShare):
    """แชร์เทมเพลตให้กับผู้ใช้อื่น"""
    try:
        result = template_manager.share_template(
            template_id,
            share_data.user_ids,
            share_data.permissions
        )
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/templates/shared/{user_id}")
async def get_shared_templates(user_id: str):
    """ดึงรายการเทมเพลตที่ถูกแชร์กับผู้ใช้"""
    try:
        templates = template_manager.get_shared_templates(user_id)
        return {"status": "success", "data": templates}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/templates/{template_id}/versions")
async def create_template_version(template_id: str, version_data: TemplateVersion):
    """สร้างเวอร์ชันใหม่ของเทมเพลต"""
    try:
        version_id = template_manager.create_template_version(
            template_id,
            version_data.changes,
            version_data.version_note
        )
        return {"status": "success", "version_id": version_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/templates/{template_id}/versions")
async def list_template_versions(template_id: str):
    """ดึงรายการเวอร์ชันของเทมเพลต"""
    try:
        versions = template_manager.list_template_versions(template_id)
        return {"status": "success", "data": versions}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/templates/{template_id}/restore/{version_id}")
async def restore_template_version(template_id: str, version_id: str):
    """กู้คืนเทมเพลตไปยังเวอร์ชันที่ระบุ"""
    try:
        success = template_manager.restore_template_version(template_id, version_id)
        if success:
            return {"status": "success", "message": f"กู้คืนเวอร์ชัน {version_id} สำเร็จ"}
        raise HTTPException(status_code=400, detail="ไม่สามารถกู้คืนเวอร์ชันได้")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/templates/{template_id}/compare")
async def compare_template_versions(
    template_id: str,
    version_id1: str,
    version_id2: str
):
    """เปรียบเทียบความแตกต่างระหว่างสองเวอร์ชัน"""
    try:
        differences = template_manager.compare_template_versions(
            template_id,
            version_id1,
            version_id2
        )
        return {"status": "success", "data": differences}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/templates/suggest")
async def suggest_template(data: Dict[str, Any]):
    """แนะนำเทมเพลตที่เหมาะสมกับข้อมูล"""
    try:
        suggestions = template_manager.suggest_template(data)
        return {"status": "success", "data": suggestions}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/status", response_model=SystemStatus)
async def check_system_status():
    """ตรวจสอบสถานะของระบบ"""
    try:
        # ตรวจสอบส่วนประกอบต่างๆ
        components = {
            "printer": print_manager.get_available_printers() is not None,
            "template": template_manager.is_ready(),
            "database": template_manager.check_database_connection()
        }
        
        return {
            "status": "online",
            "version": "1.0.0",
            "components": components,
            "template_count": len(template_manager.list_templates()),
            "printer_count": len(print_manager.get_available_printers())
        }
    except Exception as e:
        logger.error(f"เกิดข้อผิดพลาดในการตรวจสอบสถานะ: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ไม่สามารถตรวจสอบสถานะระบบได้"
        )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """จัดการข้อผิดพลาดทั้งหมดในระบบ"""
    logger.error(f"เกิดข้อผิดพลาด: {str(exc)}")
    return {
        "status": "error",
        "message": str(exc),
        "path": request.url.path
    }

@app.post("/templates/bulk-suggest")
async def bulk_suggest_templates(files: List[UploadFile] = File(...)):
    """แนะนำเทมเพลตสำหรับไฟล์หลายไฟล์พร้อมกัน"""
    try:
        results = []
        for file in files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
                content = await file.read()
                temp_file.write(content)
                
                # วิเคราะห์และแนะนำเทมเพลต
                processor = ExcelProcessor(temp_file.name)
                data = processor.process_file()
                suggestions = template_manager.suggest_template(data)
                
                results.append({
                    "filename": file.filename,
                    "suggestions": suggestions
                })
                
                os.unlink(temp_file.name)
                
        return {"status": "success", "data": results}
    except Exception as e:
        logger.error(f"เกิดข้อผิดพลาดในการแนะนำเทมเพลต: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@app.post("/templates/batch-process")
async def batch_process_files(
    files: List[UploadFile] = File(...),
    template_id: Optional[str] = None
):
    """ประมวลผลไฟล์หลายไฟล์พร้อมกัน"""
    try:
        results = []
        for file in files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
                content = await file.read()
                temp_file.write(content)
                
                # ประมวลผลไฟล์
                processor = ExcelProcessor(temp_file.name)
                if template_id:
                    result = processor.process_with_template(template_id)
                else:
                    result = processor.process_file()
                    
                results.append({
                    "filename": file.filename,
                    "result": result
                })
                
                os.unlink(temp_file.name)
                
        return {"status": "success", "data": results}
    except Exception as e:
        logger.error(f"เกิดข้อผิดพลาดในการประมวลผลแบบกลุ่ม: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 