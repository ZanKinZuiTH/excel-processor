import win32print
import win32api
from typing import List, Optional
import json
from pathlib import Path
import tempfile
import os
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side

class PrintManager:
    def __init__(self):
        self.default_printer = win32print.GetDefaultPrinter()
        self.print_queue = []

    def get_available_printers(self) -> List[str]:
        """รับรายชื่อเครื่องพิมพ์ที่มีในระบบ"""
        printers = []
        for printer in win32print.EnumPrinters(2):
            printers.append(printer[2])
        return printers

    def set_printer(self, printer_name: str):
        """เลือกเครื่องพิมพ์ที่จะใช้งาน"""
        if printer_name in self.get_available_printers():
            self.default_printer = printer_name
            return True
        return False

    def create_excel_from_data(self, data: dict, template_formatting: Optional[dict] = None) -> str:
        """สร้างไฟล์ Excel จากข้อมูลและการจัดรูปแบบ"""
        wb = Workbook()
        
        for sheet_name, sheet_data in data.items():
            ws = wb.create_sheet(title=sheet_name)
            
            # ใส่ข้อมูลและจัดรูปแบบ
            for row_idx, row_data in enumerate(sheet_data["content"], 1):
                for col_idx, (key, value) in enumerate(row_data.items(), 1):
                    cell = ws.cell(row=row_idx, column=col_idx, value=value)
                    
                    if template_formatting and sheet_name in template_formatting:
                        formatting = template_formatting[sheet_name]["structure"][row_idx-1]["formatting"][col_idx-1]
                        
                        # จัดรูปแบบตัวอักษร
                        font_data = formatting["font"]
                        cell.font = Font(
                            name=font_data["name"],
                            size=font_data["size"],
                            bold=font_data["bold"],
                            italic=font_data["italic"]
                        )
                        
                        # จัดรูปแบบการจัดวาง
                        align_data = formatting["alignment"]
                        cell.alignment = Alignment(
                            horizontal=align_data["horizontal"],
                            vertical=align_data["vertical"],
                            wrap_text=align_data["wrap_text"]
                        )
                        
                        # จัดรูปแบบเส้นขอบ
                        border_data = formatting["border"]
                        cell.border = Border(
                            left=Side(style=border_data["left"]) if border_data["left"] else None,
                            right=Side(style=border_data["right"]) if border_data["right"] else None,
                            top=Side(style=border_data["top"]) if border_data["top"] else None,
                            bottom=Side(style=border_data["bottom"]) if border_data["bottom"] else None
                        )
        
        if "Sheet" in wb.sheetnames:
            wb.remove(wb["Sheet"])
        
        # บันทึกไฟล์ชั่วคราว
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
        wb.save(temp_file.name)
        return temp_file.name

    def add_to_queue(self, data: dict, template_formatting: Optional[dict] = None):
        """เพิ่มงานพิมพ์เข้าคิว"""
        excel_file = self.create_excel_from_data(data, template_formatting)
        self.print_queue.append(excel_file)

    def print_all(self):
        """พิมพ์งานทั้งหมดในคิว"""
        for file_path in self.print_queue:
            try:
                win32api.ShellExecute(0, "print", file_path, f'/d:"{self.default_printer}"', ".", 0)
            finally:
                # ลบไฟล์ชั่วคราวหลังจากส่งไปพิมพ์
                os.unlink(file_path)
        self.print_queue.clear()

    def print_file(self, file_path: str):
        """พิมพ์ไฟล์ทันที"""
        if Path(file_path).exists():
            win32api.ShellExecute(0, "print", file_path, f'/d:"{self.default_printer}"', ".", 0)
            return True
        return False 