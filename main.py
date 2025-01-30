import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, Border
from typing import Dict, List, Any, Optional
import json
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, JSON
from pathlib import Path
import re

class ExcelProcessor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.workbook = load_workbook(file_path) if file_path else None
        self.engine = create_engine('sqlite:///excel_data.db')
        self.setup_database()

    def setup_database(self):
        metadata = MetaData()
        
        self.content_table = Table(
            'Content', metadata,
            Column('entry_id', Integer, primary_key=True),
            Column('sheet_name', String),
            Column('column_name', String),
            Column('cell_value', String)
        )

        self.structure_table = Table(
            'Structure', metadata,
            Column('entry_id', Integer, primary_key=True),
            Column('sheet_name', String),
            Column('row_number', Integer),
            Column('formatting', JSON)
        )

        self.template_table = Table(
            'Template', metadata,
            Column('template_id', Integer, primary_key=True),
            Column('name', String),
            Column('structure', JSON)
        )

        metadata.create_all(self.engine)

    def extract_customer_info(self, cell_value: str) -> Optional[Dict[str, str]]:
        """แยกข้อมูลลูกค้าจากข้อความ"""
        if not cell_value or not isinstance(cell_value, str):
            return None

        # แยกชื่อ-นามสกุล
        name_match = re.match(r'^(นาย|นาง|นางสาว)\s+(.+?)\s+(.+)$', cell_value)
        if name_match:
            return {
                "title": name_match.group(1),
                "first_name": name_match.group(2),
                "last_name": name_match.group(3)
            }
        return None

    def get_cell_formatting(self, cell) -> dict:
        """อ่านข้อมูลการจัดรูปแบบของเซลล์"""
        font = cell.font
        alignment = cell.alignment
        border = cell.border
        
        return {
            "font": {
                "name": font.name,
                "size": font.size,
                "bold": font.bold,
                "italic": font.italic,
                "color": font.color.rgb if font.color else None
            },
            "alignment": {
                "horizontal": alignment.horizontal,
                "vertical": alignment.vertical,
                "wrap_text": alignment.wrap_text
            },
            "border": {
                "left": border.left.style if border.left else None,
                "right": border.right.style if border.right else None,
                "top": border.top.style if border.top else None,
                "bottom": border.bottom.style if border.bottom else None
            }
        }

    def read_excel_content(self) -> Dict[str, List[Any]]:
        sheet_data = {}
        
        for sheet_name in self.workbook.sheetnames:
            sheet = self.workbook[sheet_name]
            data = []
            formatting = []
            
            for row in sheet.iter_rows():
                row_data = []
                row_formatting = []
                
                for cell in row:
                    cell_value = str(cell.value) if cell.value is not None else ""
                    # ตรวจสอบและแยกข้อมูลลูกค้า
                    customer_info = self.extract_customer_info(cell_value)
                    if customer_info:
                        row_data.append(customer_info)
                    else:
                        row_data.append(cell_value)
                    row_formatting.append(self.get_cell_formatting(cell))
                
                data.append(row_data)
                formatting.append(row_formatting)
            
            sheet_data[sheet_name] = {
                "data": data,
                "formatting": formatting
            }
            
        return sheet_data

    def separate_structure_and_content(self, sheet_data: Dict[str, Dict]) -> Dict[str, Dict]:
        result = {}
        
        for sheet_name, data in sheet_data.items():
            structure = []
            content = []
            
            headers = data["data"][0] if data["data"] else []
            header_formatting = data["formatting"][0] if data["formatting"] else []
            
            # เก็บข้อมูลส่วนหัว
            structure.append({
                "row_number": 0,
                "type": "header",
                "formatting": header_formatting
            })
            
            for row_idx, (row, row_formatting) in enumerate(zip(data["data"][1:], data["formatting"][1:]), 1):
                row_content = {}
                row_structure = {
                    "row_number": row_idx,
                    "type": "data",
                    "formatting": row_formatting
                }
                
                for header, cell, cell_format in zip(headers, row, row_formatting):
                    if isinstance(cell, dict):  # กรณีเป็นข้อมูลลูกค้าที่แยกแล้ว
                        row_content.update(cell)
                    elif cell and not (isinstance(cell, str) and cell.isspace()):
                        row_content[str(header)] = cell
                
                if row_content:
                    content.append(row_content)
                structure.append(row_structure)
            
            result[sheet_name] = {
                "content": content,
                "structure": structure
            }
        
        return result

    def save_to_database(self, processed_data: Dict[str, Dict]):
        with self.engine.connect() as conn:
            for sheet_name, data in processed_data.items():
                # บันทึกข้อมูล Content
                for content_row in data["content"]:
                    for col_name, value in content_row.items():
                        if isinstance(value, dict):  # กรณีเป็นข้อมูลลูกค้าที่แยกแล้ว
                            for k, v in value.items():
                                conn.execute(
                                    self.content_table.insert().values(
                                        sheet_name=sheet_name,
                                        column_name=f"{col_name}_{k}",
                                        cell_value=v
                                    )
                                )
                        else:
                            conn.execute(
                                self.content_table.insert().values(
                                    sheet_name=sheet_name,
                                    column_name=col_name,
                                    cell_value=value
                                )
                            )
                
                # บันทึกข้อมูล Structure
                for structure_row in data["structure"]:
                    conn.execute(
                        self.structure_table.insert().values(
                            sheet_name=sheet_name,
                            row_number=structure_row["row_number"],
                            formatting=json.dumps(structure_row["formatting"])
                        )
                    )

    def save_as_template(self, name: str, processed_data: Dict[str, Dict]):
        """บันทึกข้อมูลเป็นเทมเพลต"""
        with self.engine.connect() as conn:
            conn.execute(
                self.template_table.insert().values(
                    name=name,
                    structure=json.dumps(processed_data)
                )
            )

    def process_file(self) -> Dict[str, Dict]:
        sheet_data = self.read_excel_content()
        processed_data = self.separate_structure_and_content(sheet_data)
        self.save_to_database(processed_data)
        return processed_data

def main():
    # ตัวอย่างการใช้งาน
    file_path = "นางสาว ราตรี สกุลวงษ์.xlsx"
    if Path(file_path).exists():
        processor = ExcelProcessor(file_path)
        result = processor.process_file()
        
        # บันทึกเป็นเทมเพลต
        processor.save_as_template("customer_template", result)
        
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"ไม่พบไฟล์ {file_path}")

if __name__ == "__main__":
    main() 