import pandas as pd
import shutil
from pathlib import Path

# คัดลอกไฟล์ต้นฉบับไปยังโฟลเดอร์ tests/data
source_file = "นางสาว ราตรี สกุลวงษ์.xlsx"
target_dir = Path("tests/data")
target_file = target_dir / "test_invoice.xlsx"

# สร้างโฟลเดอร์ถ้ายังไม่มี
target_dir.mkdir(parents=True, exist_ok=True)

# คัดลอกไฟล์
shutil.copy2(source_file, target_file)

print(f"คัดลอกไฟล์ {source_file} ไปยัง {target_file} สำเร็จ") 