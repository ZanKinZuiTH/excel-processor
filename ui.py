import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
from pathlib import Path
import plotly.graph_objects as go
from excel_processor.processor import ExcelProcessor
import pandas as pd
import json
import os

# ตั้งค่าหน้าเพจ
st.set_page_config(
    page_title="Excel Processor - ระบบประมวลผล Excel อัจฉริยะ",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# สไตล์ CSS
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stApp {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .upload-box {
        border: 2px dashed #ccc;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    .info-box {
        background-color: #e8f4f8;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# เมนูด้านข้าง
with st.sidebar:
    st.image("previews/logo.png", width=200)
    selected = option_menu(
        "เมนูหลัก",
        ["หน้าแรก", "อัพโหลดไฟล์", "ตั้งค่า", "เกี่ยวกับ"],
        icons=['house', 'cloud-upload', 'gear', 'info-circle'],
        menu_icon="list",
        default_index=0,
    )

# หน้าแรก
if selected == "หน้าแรก":
    st.title("🏠 ยินดีต้อนรับสู่ Excel Processor")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("📌 เริ่มต้นใช้งาน", icon="ℹ️")
        st.write("""
        1. อัพโหลดไฟล์ Excel ของคุณ
        2. เลือกรูปแบบการประมวลผล
        3. รับผลลัพธ์ทันที
        """)
    
    with col2:
        st.success("✨ คุณสมบัติเด่น", icon="✅")
        st.write("""
        - รองรับไฟล์ Excel ทุกรูปแบบ
        - ประมวลผลอัตโนมัติ
        - ส่งออกในรูปแบบที่ต้องการ
        - ปลอดภัยด้วยการเข้ารหัส
        """)

# อัพโหลดไฟล์
elif selected == "อัพโหลดไฟล์":
    st.title("📤 อัพโหลดไฟล์ Excel")
    
    uploaded_file = st.file_uploader(
        "เลือกไฟล์ Excel ของคุณ",
        type=['xlsx', 'xls'],
        help="รองรับไฟล์นามสกุล .xlsx และ .xls"
    )
    
    if uploaded_file:
        # บันทึกไฟล์ชั่วคราว
        temp_path = Path("temp") / uploaded_file.name
        temp_path.parent.mkdir(exist_ok=True)
        temp_path.write_bytes(uploaded_file.getvalue())
        
        # ประมวลผลไฟล์
        processor = ExcelProcessor(temp_path)
        
        # แสดงข้อมูลเบื้องต้น
        with st.expander("ข้อมูลไฟล์", expanded=True):
            info = processor.extract_customer_info()
            st.json(info)
        
        # ตัวเลือกการประมวลผล
        process_type = st.selectbox(
            "เลือกรูปแบบการประมวลผล",
            ["วิเคราะห์ข้อมูลทั้งหมด", "สรุปข้อมูลรายเดือน", "สร้างรายงาน PDF"]
        )
        
        if st.button("เริ่มประมวลผล"):
            with st.spinner("กำลังประมวลผล..."):
                result = processor.process_file()
                
                # แสดงผลลัพธ์
                st.success("ประมวลผลเสร็จสิ้น!")
                
                # แสดงกราฟ
                fig = go.Figure(data=[
                    go.Bar(name='มูลค่า', x=result['processed_data']['dates'], y=result['processed_data']['values'])
                ])
                fig.update_layout(title='สรุปข้อมูลรายเดือน')
                st.plotly_chart(fig, use_container_width=True)
                
                # ปุ่มดาวน์โหลด
                st.download_button(
                    "⬇️ ดาวน์โหลดผลลัพธ์",
                    data=json.dumps(result, ensure_ascii=False),
                    file_name="result.json",
                    mime="application/json"
                )

# ตั้งค่า
elif selected == "ตั้งค่า":
    st.title("⚙️ ตั้งค่าระบบ")
    
    # โหลดการตั้งค่าจากไฟล์
    config_path = Path("config.json")
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    else:
        config = {
            "template_path": "templates",
            "output_path": "output",
            "language": "th",
            "theme": "light"
        }
    
    # ฟอร์มตั้งค่า
    with st.form("settings_form"):
        st.subheader("การตั้งค่าทั่วไป")
        
        template_path = st.text_input(
            "ที่อยู่เทมเพลต",
            value=config["template_path"]
        )
        
        output_path = st.text_input(
            "ที่อยู่ผลลัพธ์",
            value=config["output_path"]
        )
        
        language = st.selectbox(
            "ภาษา",
            ["ไทย", "English"],
            index=0 if config["language"] == "th" else 1
        )
        
        theme = st.selectbox(
            "ธีม",
            ["สว่าง", "มืด"],
            index=0 if config["theme"] == "light" else 1
        )
        
        if st.form_submit_button("บันทึกการตั้งค่า"):
            # อัพเดทและบันทึกการตั้งค่า
            config.update({
                "template_path": template_path,
                "output_path": output_path,
                "language": "th" if language == "ไทย" else "en",
                "theme": "light" if theme == "สว่าง" else "dark"
            })
            
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
            
            st.success("บันทึกการตั้งค่าเรียบร้อย!")

# เกี่ยวกับ
else:
    st.title("ℹ️ เกี่ยวกับโปรแกรม")
    
    st.markdown("""
    ### Excel Processor - ระบบประมวลผล Excel อัจฉริยะ
    
    โปรแกรมนี้พัฒนาขึ้นเพื่อช่วยให้การจัดการไฟล์ Excel เป็นเรื่องง่าย
    รองรับการทำงานหลากหลายรูปแบบ พร้อมฟีเจอร์ที่ช่วยให้คุณทำงานได้อย่างมีประสิทธิภาพ
    
    **เวอร์ชัน:** 0.1.0
    **ผู้พัฒนา:** ZanKinZuiTH
    **ติดต่อ:** zankinzuith@example.com
    
    ---
    
    ### วิธีใช้งาน
    1. อัพโหลดไฟล์ Excel ของคุณ
    2. เลือกรูปแบบการประมวลผลที่ต้องการ
    3. รับผลลัพธ์ทันที
    
    ### การสนับสนุน
    หากพบปัญหาหรือต้องการความช่วยเหลือ สามารถติดต่อได้ที่:
    - GitHub Issues
    - อีเมล: support@example.com
    - Line Official: @excelprocessor
    """) 