from fastapi import FastAPI, UploadFile, File, HTTPException
from main import ExcelProcessor
from printer import PrintManager
import tempfile
import os
import uvicorn
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI(title="Excel Processor API")
print_manager = PrintManager()

class Template(BaseModel):
    name: str
    structure: dict

class PrintJob(BaseModel):
    data: dict
    template_name: Optional[str] = None

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 