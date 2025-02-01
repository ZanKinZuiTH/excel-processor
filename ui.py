import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
from pathlib import Path
import plotly.graph_objects as go
from excel_processor.processor import ExcelProcessor
import pandas as pd
import json
import os
from excel_processor.form_manager import FormManager

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

"""
โมดูลสำหรับส่วนติดต่อผู้ใช้
"""

def init_session_state():
    """เริ่มต้น Session State"""
    if 'form_manager' not in st.session_state:
        st.session_state.form_manager = FormManager(
            storage_path='templates',
            db_url=st.secrets.get("DATABASE_URL")
        )

def show_form_management():
    """แสดงส่วนจัดการฟอร์ม"""
    st.header("📝 จัดการรูปแบบฟอร์ม")
    
    # เมนูด้านข้าง
    menu = st.sidebar.selectbox(
        "เลือกการทำงาน",
        ["เรียนรู้ฟอร์มใหม่", "จัดการฟอร์มที่มี", "นำเข้าข้อมูล", "ดูข้อมูล"]
    )
    
    if menu == "เรียนรู้ฟอร์มใหม่":
        show_learn_form()
    elif menu == "จัดการฟอร์มที่มี":
        show_manage_forms()
    elif menu == "นำเข้าข้อมูล":
        show_import_data()
    else:
        show_view_data()

def show_learn_form():
    """แสดงส่วนเรียนรู้ฟอร์มใหม่"""
    st.subheader("🎓 เรียนรู้ฟอร์มใหม่")
    
    # อัพโหลดไฟล์
    uploaded_file = st.file_uploader(
        "อัพโหลดไฟล์ Excel ตัวอย่าง",
        type=['xlsx', 'xls']
    )
    
    if uploaded_file:
        # แสดงตัวอย่างข้อมูล
        df = pd.read_excel(uploaded_file)
        st.write("ตัวอย่างข้อมูล:")
        st.dataframe(df.head())
        
        # กรอกข้อมูลฟอร์ม
        form_name = st.text_input("ชื่อฟอร์ม")
        description = st.text_area("คำอธิบาย")
        
        if st.button("สร้างฟอร์ม"):
            try:
                # บันทึกไฟล์ชั่วคราว
                with open("temp.xlsx", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # เรียนรู้ฟอร์ม
                template = st.session_state.form_manager.learn_from_excel(
                    "temp.xlsx",
                    form_name,
                    description
                )
                
                st.success(f"สร้างฟอร์ม {form_name} สำเร็จ!")
                
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {str(e)}")

def show_manage_forms():
    """แสดงส่วนจัดการฟอร์มที่มี"""
    st.subheader("📋 จัดการฟอร์มที่มี")
    
    # โหลดรายการฟอร์ม
    templates = st.session_state.form_manager.load_templates()
    
    if not templates:
        st.info("ยังไม่มีฟอร์ม กรุณาสร้างฟอร์มใหม่")
        return
        
    # เลือกฟอร์ม
    selected = st.selectbox(
        "เลือกฟอร์ม",
        [t.name for t in templates]
    )
    
    template = next(t for t in templates if t.name == selected)
    
    # แสดงรายละเอียด
    st.write("รายละเอียด:", template.description)
    st.write("คอลัมน์:")
    for col in template.columns:
        st.write(f"- {col['name']} ({col['data_type']})")
        
    # ปุ่มลบ
    if st.button("ลบฟอร์ม"):
        try:
            st.session_state.form_manager.delete_template(selected)
            st.success("ลบฟอร์มสำเร็จ")
            st.rerun()
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {str(e)}")

def show_import_data():
    """แสดงส่วนนำเข้าข้อมูล"""
    st.subheader("📥 นำเข้าข้อมูล")
    
    # โหลดรายการฟอร์ม
    templates = st.session_state.form_manager.load_templates()
    
    if not templates:
        st.info("ยังไม่มีฟอร์ม กรุณาสร้างฟอร์มใหม่")
        return
        
    # เลือกฟอร์ม
    selected = st.selectbox(
        "เลือกฟอร์ม",
        [t.name for t in templates]
    )
    
    # อัพโหลดไฟล์
    uploaded_file = st.file_uploader(
        "อัพโหลดไฟล์ Excel",
        type=['xlsx', 'xls']
    )
    
    if uploaded_file:
        try:
            # อ่านข้อมูล
            df = pd.read_excel(uploaded_file)
            st.write("ตัวอย่างข้อมูล:")
            st.dataframe(df.head())
            
            if st.button("นำเข้าข้อมูล"):
                # บันทึกลงฐานข้อมูล
                st.session_state.form_manager.save_to_db(selected, df)
                st.success("นำเข้าข้อมูลสำเร็จ!")
                
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {str(e)}")

def show_view_data():
    """แสดงส่วนดูข้อมูล"""
    st.subheader("📊 ดูข้อมูล")
    
    # โหลดรายการฟอร์ม
    templates = st.session_state.form_manager.load_templates()
    
    if not templates:
        st.info("ยังไม่มีฟอร์ม กรุณาสร้างฟอร์มใหม่")
        return
        
    # เลือกฟอร์ม
    selected = st.selectbox(
        "เลือกฟอร์ม",
        [t.name for t in templates]
    )
    
    try:
        # ดึงข้อมูล
        df = st.session_state.form_manager.get_from_db(selected)
        
        # แสดงข้อมูล
        st.write("ข้อมูลทั้งหมด:")
        st.dataframe(df)
        
        # ดาวน์โหลด
        if st.button("ดาวน์โหลด Excel"):
            df.to_excel("temp_download.xlsx", index=False)
            with open("temp_download.xlsx", "rb") as f:
                st.download_button(
                    "คลิกเพื่อดาวน์โหลด",
                    f,
                    file_name=f"{selected}.xlsx"
                )
                
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {str(e)}")

def main():
    """ฟังก์ชันหลัก"""
    st.set_page_config(
        page_title="Excel Processor",
        page_icon="📊",
        layout="wide"
    )
    
    init_session_state()
    
    st.title("📊 Excel Processor")
    
    # เมนูหลัก
    menu = ["หน้าหลัก", "จัดการฟอร์ม", "ประมวลผล Excel", "การตั้งค่า"]
    choice = st.sidebar.selectbox("เมนู", menu)
    
    if choice == "หน้าหลัก":
        st.write("ยินดีต้อนรับสู่ Excel Processor")
        st.write("เลือกเมนูด้านซ้ายเพื่อเริ่มใช้งาน")
        
    elif choice == "จัดการฟอร์ม":
        show_form_management()
        
    elif choice == "ประมวลผล Excel":
        show_excel_processing()
        
    else:
        show_settings()

if __name__ == "__main__":
    main() 