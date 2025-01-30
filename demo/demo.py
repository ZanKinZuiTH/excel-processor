import requests
import json
import time
from pathlib import Path

def demo_system():
    """สาธิตการทำงานของระบบด้วยไฟล์จริงจากลูกค้า"""
    BASE_URL = "http://localhost:8000"
    
    print("🚀 เริ่มการสาธิตระบบ Excel Processor")
    print("=" * 50)
    
    # 1. ตรวจสอบการทำงานของ API
    print("\n1. ตรวจสอบการทำงานของระบบ...")
    response = requests.get(f"{BASE_URL}/")
    print(f"สถานะระบบ: {response.json()['message']}")
    time.sleep(1)
    
    # 2. แสดงรายชื่อเครื่องพิมพ์
    print("\n2. ตรวจสอบเครื่องพิมพ์ในระบบ...")
    response = requests.get(f"{BASE_URL}/printers/")
    printers = response.json()
    print(f"พบเครื่องพิมพ์ {len(printers)} เครื่อง:")
    for printer in printers:
        print(f"   - {printer}")
    time.sleep(1)
    
    # 3. อัปโหลดและประมวลผลไฟล์ของลูกค้า
    print("\n3. ทดสอบการประมวลผลไฟล์...")
    file_path = Path("นางสาว ราตรี สกุลวงษ์.xlsx")
    if file_path.exists():
        files = {"file": open(file_path, "rb")}
        response = requests.post(f"{BASE_URL}/process-excel/", files=files)
        result = response.json()
        print("ผลการประมวลผล:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("ไม่พบไฟล์ของลูกค้า")
    time.sleep(1)
    
    # 4. บันทึกเทมเพลตจากไฟล์ของลูกค้า
    print("\n4. บันทึกเทมเพลต...")
    template_data = {
        "name": "customer_template",
        "structure": {
            "Sheet1": {
                "content": [
                    {"type": "header", "text": "ข้อมูลลูกค้า"},
                    {"type": "field", "name": "name", "label": "ชื่อ-นามสกุล"},
                    {"type": "field", "name": "id", "label": "รหัสประจำตัว"},
                    {"type": "field", "name": "address", "label": "ที่อยู่"},
                    {"type": "field", "name": "phone", "label": "เบอร์โทรศัพท์"},
                    {"type": "field", "name": "email", "label": "อีเมล"}
                ]
            }
        }
    }
    response = requests.post(
        f"{BASE_URL}/save-template/",
        json=template_data
    )
    print(f"ผลการบันทึกเทมเพลต: {response.json()['message']}")
    time.sleep(1)
    
    # 5. ทดสอบการพิมพ์ด้วยข้อมูลจริง
    print("\n5. ทดสอบการพิมพ์...")
    print_data = {
        "data": {
            "Sheet1": {
                "content": [
                    {
                        "name": "นางสาว ราตรี สกุลวงษ์",
                        "id": "1234567890123",
                        "address": "123/456 ถ.สุขุมวิท",
                        "phone": "02-123-4567",
                        "email": "ratree@example.com"
                    }
                ]
            }
        },
        "template_name": "customer_template"
    }
    response = requests.post(
        f"{BASE_URL}/print/",
        json=print_data
    )
    print(f"ผลการสั่งพิมพ์: {response.json()['message']}")
    
    print("\n✨ การสาธิตเสร็จสิ้น")
    print("=" * 50)

if __name__ == "__main__":
    demo_system() 