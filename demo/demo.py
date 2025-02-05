"""
ตัวอย่างการใช้งานระบบจัดการเทมเพลต Excel
โดยใช้ไฟล์ตัวอย่าง: นางสาว ราตรี สกุลวงษ์.xlsx

คำอธิบายสำหรับนักศึกษา:
1. โค้ดนี้แสดงตัวอย่างการใช้งานระบบจัดการเทมเพลต Excel แบบครบวงจร
2. มีการใช้เทคนิคการเขียนโปรแกรมหลายอย่าง เช่น:
   - การจัดการไฟล์ Excel ด้วย pandas
   - การตรวจสอบข้อมูลด้วย Regular Expression
   - การจัดการ Exception และ Error
   - การแสดงผลสวยงามด้วย colorama
3. นักศึกษาสามารถศึกษาและทดลองปรับแต่งโค้ดได้ตามต้องการ
"""

import os
import sys

# เพิ่ม path ของโปรเจคเข้าไปใน Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

import pandas as pd
from template_manager import TemplateManager
from datetime import datetime
import re
from colorama import init, Fore, Style
from ai_model_manager import AIModelManager

# เริ่มต้นใช้งาน colorama สำหรับแสดงสีในเทอร์มินอล
init()

def print_header(text):
    """แสดงหัวข้อให้สวยงาม
    
    สำหรับนักศึกษา: 
    - ใช้ colorama ในการแสดงสีข้อความ
    - ใช้เครื่องหมาย = ในการสร้างกรอบ
    - ใช้ Style.RESET_ALL เพื่อคืนค่าสีเป็นค่าเริ่มต้น
    """
    print(f"\n{Fore.CYAN}{'='*50}")
    print(f"  {text}")
    print(f"{'='*50}{Style.RESET_ALL}")

def print_success(text):
    """แสดงข้อความสำเร็จ"""
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")

def print_warning(text):
    """แสดงข้อความเตือน"""
    print(f"{Fore.YELLOW}⚠ {text}{Style.RESET_ALL}")

def print_error(text):
    """แสดงข้อความผิดพลาด"""
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")

def validate_personal_data(data):
    """ตรวจสอบความถูกต้องของข้อมูลส่วนบุคคล
    
    สำหรับนักศึกษา:
    1. สังเกตการใช้ Regular Expression (re.match) ในการตรวจสอบรูปแบบข้อมูล
    2. การแยกระหว่าง errors (ข้อผิดพลาดร้ายแรง) และ warnings (คำเตือน)
    3. การจัดการกับวันที่โดยใช้ datetime
    
    Args:
        data (dict): ข้อมูลส่วนบุคคลที่ต้องการตรวจสอบ
    
    Returns:
        tuple: (errors, warnings) รายการข้อผิดพลาดและคำเตือน
    """
    errors = []
    warnings = []
    
    # ตรวจสอบเลขบัตรประชาชน (13 หลัก)
    id_card = data["ข้อมูลส่วนบุคคล"]["เลขประจำตัวประชาชน"]
    if not re.match(r'^\d{13}$', id_card):
        errors.append("เลขประจำตัวประชาชนต้องมี 13 หลัก")
    
    # ตรวจสอบวันเดือนปีเกิด
    try:
        datetime.strptime(data["ข้อมูลส่วนบุคคล"]["วันเดือนปีเกิด"], "%d %B %Y")
    except ValueError:
        warnings.append("รูปแบบวันเดือนปีเกิดควรเป็น 'วัน เดือน ปี' เช่น '1 มกราคม 2540'")
    
    # ตรวจสอบอีเมล
    email = data["ข้อมูลติดต่อ"]["อีเมล"]
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        errors.append("รูปแบบอีเมลไม่ถูกต้อง")
    
    # ตรวจสอบเบอร์โทรศัพท์
    phone = data["ข้อมูลติดต่อ"]["เบอร์โทรศัพท์"]
    mobile = data["ข้อมูลติดต่อ"]["มือถือ"]
    if not (re.match(r'^\d{2}-\d{3}-\d{4}$', phone) or re.match(r'^\d{3}-\d{3}-\d{4}$', phone)):
        warnings.append("รูปแบบเบอร์โทรศัพท์ควรเป็น 'XX-XXX-XXXX' หรือ 'XXX-XXX-XXXX'")
    if not re.match(r'^\d{3}-\d{3}-\d{4}$', mobile):
        warnings.append("รูปแบบเบอร์มือถือควรเป็น 'XXX-XXX-XXXX'")
    
    return errors, warnings

def validate_education_data(data):
    """ตรวจสอบความถูกต้องของข้อมูลการศึกษา"""
    errors = []
    warnings = []
    
    for edu in data["ประวัติการศึกษา"]:
        # ตรวจสอบปีที่จบ
        try:
            year = int(edu["ปีที่จบ"])
            current_year = datetime.now().year + 543  # แปลงเป็นปี พ.ศ.
            if year > current_year:
                errors.append(f"ปีที่จบ {year} ไม่สามารถมากกว่าปีปัจจุบัน")
        except ValueError:
            errors.append(f"ปีที่จบ '{edu['ปีที่จบ']}' ต้องเป็นตัวเลขเท่านั้น")
        
        # ตรวจสอบเกรดเฉลี่ย
        try:
            gpa = float(edu["เกรดเฉลี่ย"])
            if not (0 <= gpa <= 4.0):
                errors.append(f"เกรดเฉลี่ย {gpa} ต้องอยู่ระหว่าง 0.00 - 4.00")
        except ValueError:
            errors.append(f"เกรดเฉลี่ย '{edu['เกรดเฉลี่ย']}' ต้องเป็นตัวเลขเท่านั้น")
    
    return errors, warnings

def validate_work_data(data):
    """ตรวจสอบความถูกต้องของข้อมูลการทำงาน"""
    errors = []
    warnings = []
    
    for work in data["ประวัติการทำงาน"]:
        # ตรวจสอบเงินเดือน
        try:
            salary = float(work["เงินเดือน"])
            if salary < 0:
                errors.append(f"เงินเดือนต้องไม่ติดลบ")
        except ValueError:
            errors.append(f"เงินเดือน '{work['เงินเดือน']}' ต้องเป็นตัวเลขเท่านั้น")
        
        # ตรวจสอบระยะเวลาการทำงาน
        period = work["ระยะเวลา"]
        if not re.match(r'^\d{4}-(\d{4}|ปัจจุบัน)$', period):
            warnings.append(f"รูปแบบระยะเวลาควรเป็น 'ปีเริ่ม-ปีสิ้นสุด' เช่น '2562-2565' หรือ '2562-ปัจจุบัน'")
    
    return errors, warnings

def display_validation_results(errors, warnings, section):
    """แสดงผลการตรวจสอบข้อมูล"""
    print(f"\n{Fore.CYAN}ผลการตรวจสอบ{section}:{Style.RESET_ALL}")
    
    if not errors and not warnings:
        print_success("ข้อมูลถูกต้องทั้งหมด")
        return
    
    if errors:
        print(f"\n{Fore.RED}พบข้อผิดพลาด:{Style.RESET_ALL}")
        for error in errors:
            print_error(error)
    
    if warnings:
        print(f"\n{Fore.YELLOW}คำเตือน:{Style.RESET_ALL}")
        for warning in warnings:
            print_warning(warning)

def read_all_sheets(file_path):
    """อ่านข้อมูลจากทุกหน้าในไฟล์ Excel
    
    สำหรับนักศึกษา:
    1. ใช้ pandas.ExcelFile ในการอ่านไฟล์ Excel
    2. ใช้ sheet_names เพื่อดูรายชื่อ sheet ทั้งหมด
    3. ใช้ read_excel เพื่ออ่านข้อมูลแต่ละ sheet
    4. แปลงข้อมูลเป็น dictionary ด้วย to_dict('records')
    
    Args:
        file_path (str): พาธของไฟล์ Excel
    
    Returns:
        dict: ข้อมูลจากทุก sheet ในรูปแบบ dictionary
    """
    print_header(f"กำลังอ่านข้อมูลจากไฟล์: {file_path}")
    
    excel_file = pd.ExcelFile(file_path)
    all_data = {}
    
    for sheet_name in excel_file.sheet_names:
        print(f"\n{Fore.CYAN}กำลังอ่านหน้า: {sheet_name}{Style.RESET_ALL}")
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        
        print_success(f"พบข้อมูล {len(df)} แถว, {len(df.columns)} คอลัมน์")
        print(f"{Fore.CYAN}คอลัมน์ที่พบ:{Style.RESET_ALL}")
        for col in df.columns:
            print(f"  • {col}")
            
        all_data[sheet_name] = df.to_dict('records')
    
    return all_data

def demo_template_upload():
    """สาธิตการอัพโหลดเทมเพลต"""
    print("1. การอัพโหลดเทมเพลต")
    print("-" * 50)
    
    template_path = "นางสาว ราตรี สกุลวงษ์.xlsx"
    tm = TemplateManager()
    
    # อ่านข้อมูลจากทุกหน้า
    all_sheet_data = read_all_sheets(template_path)
    
    # อัพโหลดเทมเพลต
    template_id = tm.upload_template(
        file_path=template_path,
        name="แบบฟอร์มข้อมูลส่วนบุคคล",
        description="เทมเพลตสำหรับกรอกข้อมูลส่วนบุคคล ที่อยู่ และข้อมูลติดต่อ",
        sheet_data=all_sheet_data  # เพิ่มข้อมูลจากทุกหน้า
    )
    
    print(f"\n✓ อัพโหลดเทมเพลต '{template_path}' สำเร็จ")
    print(f"✓ Template ID: {template_id}")
    return template_id, all_sheet_data

def demo_data_entry(template_id, all_sheet_data):
    """สาธิตการกรอกข้อมูล
    
    สำหรับนักศึกษา:
    1. สังเกตโครงสร้างข้อมูลแบบ Nested Dictionary
    2. การตรวจสอบข้อมูลก่อนบันทึก
    3. การแสดงผลข้อมูลในรูปแบบที่อ่านง่าย
    4. การจัดการกับข้อผิดพลาดและการยืนยันจากผู้ใช้
    
    Args:
        template_id: ID ของเทมเพลต
        all_sheet_data: ข้อมูลทั้งหมดจากไฟล์ Excel
    
    Returns:
        str: ID ของข้อมูลที่บันทึก หรือ None ถ้ายกเลิก
    """
    print_header("การกรอกข้อมูล")
    
    tm = TemplateManager()
    
    # ข้อมูลส่วนบุคคล (หน้าที่ 1)
    personal_data = {
        "ข้อมูลส่วนบุคคล": {
            "ชื่อ-นามสกุล": "นายสมชาย รักเรียน",
            "เลขประจำตัวประชาชน": "1234567890123",
            "วันเดือนปีเกิด": "1 มกราคม 2540",
            "สถานภาพ": "โสด",
            "เพศ": "ชาย",
            "ศาสนา": "พุทธ"
        },
        "ที่อยู่ปัจจุบัน": {
            "บ้านเลขที่": "123/45",
            "ถนน": "พหลโยธิน",
            "ตำบล/แขวง": "จตุจักร",
            "อำเภอ/เขต": "จตุจักร",
            "จังหวัด": "กรุงเทพมหานคร",
            "รหัสไปรษณีย์": "10900"
        },
        "ข้อมูลติดต่อ": {
            "เบอร์โทรศัพท์": "02-123-4567",
            "มือถือ": "081-234-5678",
            "อีเมล": "somchai@email.com",
            "Line ID": "somchai_r"
        }
    }
    
    # ข้อมูลการศึกษา (หน้าที่ 2)
    education_data = {
        "ประวัติการศึกษา": [
            {
                "ระดับการศึกษา": "ปริญญาตรี",
                "สถาบัน": "มหาวิทยาลัยกรุงเทพ",
                "คณะ": "วิศวกรรมศาสตร์",
                "สาขา": "วิศวกรรมคอมพิวเตอร์",
                "ปีที่จบ": "2562",
                "เกรดเฉลี่ย": "3.50"
            },
            {
                "ระดับการศึกษา": "มัธยมศึกษาตอนปลาย",
                "สถาบัน": "โรงเรียนสวนกุหลาบวิทยาลัย",
                "แผนการเรียน": "วิทย์-คณิต",
                "ปีที่จบ": "2558",
                "เกรดเฉลี่ย": "3.75"
            }
        ]
    }
    
    # ข้อมูลการทำงาน (หน้าที่ 3)
    work_data = {
        "ประวัติการทำงาน": [
            {
                "บริษัท": "บริษัท ABC จำกัด",
                "ตำแหน่ง": "วิศวกรซอฟต์แวร์",
                "แผนก": "พัฒนาระบบ",
                "เงินเดือน": "45000",
                "ระยะเวลา": "2562-ปัจจุบัน"
            }
        ],
        "ทักษะพิเศษ": {
            "ภาษาต่างประเทศ": ["อังกฤษ", "ญี่ปุ่น"],
            "คอมพิวเตอร์": ["Python", "JavaScript", "SQL"],
            "อื่นๆ": ["ใบขับขี่รถยนต์", "ใบขับขี่รถจักรยานยนต์"]
        }
    }
    
    # ตรวจสอบความถูกต้องของข้อมูล
    personal_errors, personal_warnings = validate_personal_data(personal_data)
    education_errors, education_warnings = validate_education_data(education_data)
    work_errors, work_warnings = validate_work_data(work_data)
    
    # แสดงผลการตรวจสอบ
    display_validation_results(personal_errors, personal_warnings, "ข้อมูลส่วนบุคคล")
    display_validation_results(education_errors, education_warnings, "ประวัติการศึกษา")
    display_validation_results(work_errors, work_warnings, "ประวัติการทำงาน")
    
    # ถ้ามีข้อผิดพลาด ให้ถามผู้ใช้ว่าต้องการดำเนินการต่อหรือไม่
    if personal_errors or education_errors or work_errors:
        print_warning("\nพบข้อผิดพลาดในข้อมูล คุณต้องการดำเนินการต่อหรือไม่? (y/n)")
        if input().lower() != 'y':
            print_error("ยกเลิกการบันทึกข้อมูล")
            return None
    
    # รวมข้อมูลทั้งหมด
    complete_data = {
        "ข้อมูลส่วนบุคคล": personal_data,
        "ประวัติการศึกษา": education_data,
        "ประวัติการทำงาน": work_data
    }
    
    # บันทึกข้อมูล
    entry_id = tm.save_data_entry(template_id, complete_data)
    print_success("บันทึกข้อมูลสำเร็จ")
    print_success(f"Entry ID: {entry_id}")
    
    # แสดงสรุปข้อมูลที่บันทึก
    print(f"\n{Fore.CYAN}สรุปข้อมูลที่บันทึก:{Style.RESET_ALL}")
    for sheet_name, data in complete_data.items():
        print(f"\n{Fore.YELLOW}{sheet_name}:{Style.RESET_ALL}")
        if isinstance(data, dict):
            for section, section_data in data.items():
                print(f"\n  {Fore.CYAN}{section}:{Style.RESET_ALL}")
                if isinstance(section_data, dict):
                    for key, value in section_data.items():
                        print(f"    • {key}: {value}")
                elif isinstance(section_data, list):
                    for i, item in enumerate(section_data, 1):
                        print(f"    {i}. {item}")
    
    return entry_id

def demo_preview(template_id, entry_id):
    """สาธิตการดูตัวอย่างเอกสาร"""
    print_header("การดูตัวอย่างเอกสาร")
    
    tm = TemplateManager()
    
    for sheet_name in ["ข้อมูลส่วนบุคคล", "ประวัติการศึกษา", "ประวัติการทำงาน"]:
        preview = tm.create_preview(template_id, entry_id, sheet_name)
        print_success(f"สร้างตัวอย่างเอกสารหน้า '{sheet_name}' สำเร็จ")
        print(f"  • Preview URL: {preview['url']}")

def demo_print(template_id, entry_id):
    """สาธิตการพิมพ์เอกสาร"""
    print_header("การพิมพ์เอกสาร")
    
    tm = TemplateManager()
    
    printer = "Microsoft Print to PDF"
    result = tm.print_document(
        template_id,
        entry_id,
        printer,
        sheets=["ข้อมูลส่วนบุคคล", "ประวัติการศึกษา", "ประวัติการทำงาน"]
    )
    print_success(f"ส่งเอกสารไปยังเครื่องพิมพ์ '{printer}' สำเร็จ")

def demo_ai_analysis():
    """สาธิตการใช้งานระบบ AI สำหรับวิเคราะห์เอกสาร"""
    print_header("การวิเคราะห์เอกสารด้วย AI")
    
    # สร้าง AI Model Manager
    ai_model = AIModelManager()
    
    # ตัวอย่างการวิเคราะห์เอกสารใหม่
    sample_file = "ตัวอย่างเอกสาร.xlsx"
    print(f"\n{Fore.CYAN}กำลังวิเคราะห์ไฟล์: {sample_file}{Style.RESET_ALL}")
    
    # วิเคราะห์โครงสร้างเอกสารด้วย CNN
    structure = ai_model.analyze_structure(sample_file)
    print(f"\n{Fore.YELLOW}ผลการวิเคราะห์โครงสร้าง:{Style.RESET_ALL}")
    for section, confidence in structure.items():
        print(f"  • {section}: {confidence*100:.1f}%")
    
    # วิเคราะห์เนื้อหาด้วย CNN+LSTM
    content = ai_model.analyze_content(sample_file)
    print(f"\n{Fore.YELLOW}ผลการวิเคราะห์เนื้อหา:{Style.RESET_ALL}")
    for field, prediction in content.items():
        print(f"  • {field}:")
        print(f"    - ค่าที่พบ: {prediction['value']}")
        print(f"    - ความมั่นใจ: {prediction['confidence']*100:.1f}%")
    
    # สร้างเทมเพลตอัตโนมัติ
    template = ai_model.create_template(sample_file)
    print(f"\n{Fore.GREEN}✓ สร้างเทมเพลตอัตโนมัติสำเร็จ{Style.RESET_ALL}")
    print(f"  • Template ID: {template['id']}")
    print(f"  • จำนวนฟิลด์ที่พบ: {len(template['fields'])}")
    
    return template['id']

def demo_ai_training():
    """สาธิตการฝึกฝนระบบ AI ด้วยข้อมูลใหม่"""
    print_header("การฝึกฝนระบบ AI")
    
    # สร้าง AI Model Manager
    ai_model = AIModelManager()
    
    # ข้อมูลสำหรับฝึกฝน
    training_files = [
        "ตัวอย่าง1.xlsx",
        "ตัวอย่าง2.xlsx",
        "ตัวอย่าง3.xlsx"
    ]
    
    print(f"\n{Fore.CYAN}เริ่มการฝึกฝนด้วยไฟล์:{Style.RESET_ALL}")
    for file in training_files:
        print(f"  • {file}")
    
    # เริ่มการฝึกฝน
    training_result = ai_model.train(
        files=training_files,
        epochs=10,
        batch_size=32
    )
    
    print(f"\n{Fore.YELLOW}ผลการฝึกฝน:{Style.RESET_ALL}")
    print(f"  • ความแม่นยำ: {training_result['accuracy']*100:.1f}%")
    print(f"  • ค่าความสูญเสีย: {training_result['loss']:.4f}")
    
    # บันทึกโมเดล
    model_id = ai_model.save_model()
    print(f"\n{Fore.GREEN}✓ บันทึกโมเดลสำเร็จ{Style.RESET_ALL}")
    print(f"  • Model ID: {model_id}")
    
    return model_id

def main():
    """ฟังก์ชันหลักสำหรับการสาธิต
    
    สำหรับนักศึกษา:
    1. สังเกตการทำงานตามลำดับขั้นตอน
    2. การตรวจสอบผลลัพธ์ในแต่ละขั้นตอน
    3. การจัดการกรณีที่เกิดข้อผิดพลาด
    """
    print_header("สาธิตการใช้งานระบบจัดการเทมเพลต Excel")
    
    # สาธิตการใช้งานพื้นฐาน
    template_id, all_sheet_data = demo_template_upload()
    if not template_id:
        return
    
    entry_id = demo_data_entry(template_id, all_sheet_data)
    if not entry_id:
        return
    
    demo_preview(template_id, entry_id)
    demo_print(template_id, entry_id)
    
    # สาธิตการใช้งานระบบ AI
    print("\nเริ่มการสาธิตระบบ AI...")
    ai_template_id = demo_ai_analysis()
    model_id = demo_ai_training()
    
    print_header("จบการสาธิต")

if __name__ == "__main__":
    main() 