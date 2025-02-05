import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.metric_cards import style_metric_cards
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
from excel_processor.processor import ExcelProcessor
from excel_processor.form_manager import FormManager
from excel_processor.ai_manager import AIModelManager
import pandas as pd
import numpy as np
import json
import os
import time
import logging
from datetime import datetime, timedelta

# ตั้งค่า logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ตั้งค่าหน้าเพจ
st.set_page_config(
    page_title="Excel Processor - ระบบประมวลผล Excel อัจฉริยะ",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# โหลดการตั้งค่าธีม
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# สร้าง instance ของ managers
if 'processor' not in st.session_state:
    st.session_state.processor = ExcelProcessor()
if 'form_manager' not in st.session_state:
    st.session_state.form_manager = FormManager()
if 'ai_manager' not in st.session_state:
    st.session_state.ai_manager = AIModelManager()

# สไตล์ CSS
st.markdown(f"""
<style>
    .main {{
        padding: 0rem 1rem;
    }}
    .stApp {{
        background-color: {('#f0f2f6' if st.session_state.theme == 'light' else '#1a1a1a')};
        color: {('#000000' if st.session_state.theme == 'light' else '#ffffff')};
    }}
    .stButton>button {{
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
    }}
    .stButton>button:hover {{
        background-color: #45a049;
    }}
    .upload-box {{
        border: 2px dashed {('#ccc' if st.session_state.theme == 'light' else '#666')};
        border-radius: 5px;
        padding: 2rem;
        text-align: center;
    }}
    .metric-card {{
        background-color: {('#ffffff' if st.session_state.theme == 'light' else '#2d2d2d')};
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    .chart-container {{
        background-color: {('#ffffff' if st.session_state.theme == 'light' else '#2d2d2d')};
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }}
</style>
""", unsafe_allow_html=True)

# สร้างเมนูด้านข้าง
with st.sidebar:
    selected = option_menu(
        "เมนูหลัก",
        ["หน้าแรก", "อัปโหลดไฟล์", "AI Analysis", "รายงาน", "การตั้งค่า", "เกี่ยวกับ"],
        icons=['house', 'upload', 'robot', 'graph-up', 'gear', 'info-circle'],
        menu_icon="list",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": ('#ffffff' if st.session_state.theme == 'light' else '#2d2d2d')},
            "icon": {"color": "orange", "font-size": "25px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px"},
            "nav-link-selected": {"background-color": "#4CAF50"},
        }
    )
    
    # สวิตช์เปลี่ยนธีม
    theme_switch = st.checkbox("โหมดกลางคืน", value=(st.session_state.theme == 'dark'))
    if theme_switch:
        st.session_state.theme = 'dark'
    else:
        st.session_state.theme = 'light'

# แสดงหน้าตามที่เลือก
if selected == "หน้าแรก":
    # หัวข้อ
    colored_header(
        label="ยินดีต้อนรับสู่ Excel Processor",
        description="ระบบประมวลผล Excel อัจฉริยะ พร้อมการวิเคราะห์ด้วย AI",
        color_name="green-70"
    )
    
    # เมตริกการใช้งาน
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="ไฟล์ที่ประมวลผล", value="150", delta="15 วันนี้")
    with col2:
        st.metric(label="ความแม่นยำ AI", value="95%", delta="2%")
    with col3:
        st.metric(label="เวลาที่ประหยัดได้", value="45 ชม.", delta="5 ชม.")
    with col4:
        st.metric(label="เทมเพลตที่สร้าง", value="25", delta="3")
    style_metric_cards()
    
    # กราฟแสดงสถิติ
    st.markdown("### 📊 สถิติการใช้งาน")
    
    # สร้างข้อมูลตัวอย่าง
    dates = pd.date_range(start='2024-01-01', end='2024-02-05', freq='D')
    daily_usage = np.random.randint(5, 20, size=len(dates))
    df_usage = pd.DataFrame({
        'วันที่': dates,
        'จำนวนไฟล์': daily_usage
    })
    
    # กราฟการใช้งานรายวัน
    fig_daily = px.line(df_usage, x='วันที่', y='จำนวนไฟล์',
                       title='การใช้งานรายวัน',
                       labels={'จำนวนไฟล์': 'จำนวนไฟล์ที่ประมวลผล'})
    fig_daily.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Kanit"
    )
    st.plotly_chart(fig_daily, use_container_width=True)
    
    # กราฟประเภทเอกสาร
    doc_types = ['ข้อมูลส่วนบุคคล', 'ประวัติการศึกษา', 'ประวัติการทำงาน', 'อื่นๆ']
    doc_counts = [40, 30, 20, 10]
    fig_types = go.Figure(data=[go.Pie(labels=doc_types, values=doc_counts)])
    fig_types.update_layout(
        title='สัดส่วนประเภทเอกสาร',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Kanit"
    )
    st.plotly_chart(fig_types, use_container_width=True)

elif selected == "อัปโหลดไฟล์":
    colored_header(
        label="อัปโหลดไฟล์ Excel",
        description="รองรับไฟล์ .xlsx, .xls",
        color_name="green-70"
    )
    
    # กล่องอัปโหลด
    uploaded_file = st.file_uploader("เลือกไฟล์ Excel", type=['xlsx', 'xls'])
    
    if uploaded_file is not None:
        with st.spinner('กำลังประมวลผลไฟล์...'):
            # บันทึกไฟล์
            temp_path = Path("temp") / uploaded_file.name
            temp_path.parent.mkdir(exist_ok=True)
            temp_path.write_bytes(uploaded_file.getvalue())
            
            try:
                # ประมวลผลไฟล์
                result = st.session_state.processor.process_file(str(temp_path))
                
                # แสดงผลลัพธ์
                st.success("ประมวลผลไฟล์สำเร็จ!")
                st.json(result)
                
                # แสดงตัวอย่างข้อมูล
                df = pd.read_excel(temp_path)
                st.dataframe(df)
                
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {str(e)}")
                logger.error(f"เกิดข้อผิดพลาดในการประมวลผลไฟล์: {str(e)}")
            
            finally:
                # ลบไฟล์ชั่วคราว
                temp_path.unlink()

elif selected == "AI Analysis":
    colored_header(
        label="การวิเคราะห์ด้วย AI",
        description="วิเคราะห์ข้อมูลด้วย AI",
        color_name="green-70"
    )
    
    # เลือกประเภทการวิเคราะห์
    analysis_type = st.radio(
        "เลือกประเภทการวิเคราะห์",
        ["วิเคราะห์เอกสาร", "สร้างเทมเพลต", "เทรนโมเดล"]
    )
    
    if analysis_type == "วิเคราะห์เอกสาร":
        uploaded_file = st.file_uploader("เลือกไฟล์ Excel สำหรับวิเคราะห์", type=['xlsx', 'xls'])
        
        if uploaded_file is not None:
            with st.spinner('กำลังวิเคราะห์...'):
                # บันทึกไฟล์
                temp_path = Path("temp") / uploaded_file.name
                temp_path.parent.mkdir(exist_ok=True)
                temp_path.write_bytes(uploaded_file.getvalue())
                
                try:
                    # วิเคราะห์โครงสร้าง
                    structure = st.session_state.ai_manager.analyze_structure(str(temp_path))
                    
                    # วิเคราะห์เนื้อหา
                    content = st.session_state.ai_manager.analyze_content(str(temp_path))
                    
                    # แสดงผลการวิเคราะห์
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("### 📊 ผลการวิเคราะห์โครงสร้าง")
                        st.json(structure)
                    with col2:
                        st.markdown("### 📝 ผลการวิเคราะห์เนื้อหา")
                        st.json(content)
                    
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {str(e)}")
                    logger.error(f"เกิดข้อผิดพลาดในการวิเคราะห์: {str(e)}")
                
                finally:
                    # ลบไฟล์ชั่วคราว
                    temp_path.unlink()
    
    elif analysis_type == "สร้างเทมเพลต":
        uploaded_file = st.file_uploader("เลือกไฟล์ Excel สำหรับสร้างเทมเพลต", type=['xlsx', 'xls'])
        
        if uploaded_file is not None:
            with st.spinner('กำลังสร้างเทมเพลต...'):
                # บันทึกไฟล์
                temp_path = Path("temp") / uploaded_file.name
                temp_path.parent.mkdir(exist_ok=True)
                temp_path.write_bytes(uploaded_file.getvalue())
                
                try:
                    # สร้างเทมเพลต
                    template = st.session_state.ai_manager.create_template(str(temp_path))
                    
                    # แสดงผลลัพธ์
                    st.success("สร้างเทมเพลตสำเร็จ!")
                    st.json(template)
                    
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {str(e)}")
                    logger.error(f"เกิดข้อผิดพลาดในการสร้างเทมเพลต: {str(e)}")
                
                finally:
                    # ลบไฟล์ชั่วคราว
                    temp_path.unlink()
    
    else:  # เทรนโมเดล
        st.markdown("### 🤖 เทรนโมเดล AI")
        
        # อัปโหลดไฟล์สำหรับเทรน
        uploaded_files = st.file_uploader(
            "เลือกไฟล์ Excel สำหรับเทรน (เลือกได้หลายไฟล์)",
            type=['xlsx', 'xls'],
            accept_multiple_files=True
        )
        
        # พารามิเตอร์การเทรน
        col1, col2 = st.columns(2)
        with col1:
            epochs = st.number_input("จำนวนรอบการเทรน", min_value=1, value=10)
        with col2:
            batch_size = st.number_input("ขนาดแบตช์", min_value=1, value=32)
        
        if st.button("เริ่มการเทรน") and uploaded_files:
            with st.spinner('กำลังเทรนโมเดล...'):
                try:
                    # บันทึกไฟล์
                    temp_paths = []
                    for file in uploaded_files:
                        temp_path = Path("temp") / file.name
                        temp_path.parent.mkdir(exist_ok=True)
                        temp_path.write_bytes(file.getvalue())
                        temp_paths.append(str(temp_path))
                    
                    # เทรนโมเดล
                    results = st.session_state.ai_manager.train(
                        temp_paths,
                        epochs=epochs,
                        batch_size=batch_size
                    )
                    
                    # แสดงผลการเทรน
                    st.success("เทรนโมเดลสำเร็จ!")
                    
                    # แสดงกราฟผลการเทรน
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("ความแม่นยำ (โครงสร้าง)", f"{results['structure_accuracy']:.2%}")
                        st.metric("Loss (โครงสร้าง)", f"{results['structure_loss']:.4f}")
                    with col2:
                        st.metric("ความแม่นยำ (เนื้อหา)", f"{results['content_accuracy']:.2%}")
                        st.metric("Loss (เนื้อหา)", f"{results['content_loss']:.4f}")
                    
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {str(e)}")
                    logger.error(f"เกิดข้อผิดพลาดในการเทรนโมเดล: {str(e)}")
                
                finally:
                    # ลบไฟล์ชั่วคราว
                    for path in temp_paths:
                        Path(path).unlink()

elif selected == "รายงาน":
    colored_header(
        label="รายงานและการวิเคราะห์",
        description="แสดงสถิติและรายงานการใช้งานระบบ",
        color_name="green-70"
    )
    
    # ช่วงเวลาที่ต้องการดูรายงาน
    report_range = st.selectbox(
        "เลือกช่วงเวลา",
        ["7 วันล่าสุด", "30 วันล่าสุด", "ทั้งหมด"]
    )
    
    # สร้างข้อมูลตัวอย่างตามช่วงเวลา
    if report_range == "7 วันล่าสุด":
        days = 7
    elif report_range == "30 วันล่าสุด":
        days = 30
    else:
        days = 90
    
    dates = pd.date_range(end=datetime.now(), periods=days)
    daily_files = np.random.randint(5, 20, size=days)
    accuracy = np.random.normal(0.95, 0.02, size=days)
    processing_time = np.random.normal(5, 1, size=days)
    
    df_stats = pd.DataFrame({
        'วันที่': dates,
        'จำนวนไฟล์': daily_files,
        'ความแม่นยำ': accuracy,
        'เวลาประมวลผล': processing_time
    })
    
    # แสดงกราฟ
    st.markdown("### 📈 แนวโน้มการใช้งาน")
    
    # กราฟจำนวนไฟล์
    fig_files = px.line(df_stats, x='วันที่', y='จำนวนไฟล์',
                       title='จำนวนไฟล์ที่ประมวลผลต่อวัน')
    st.plotly_chart(fig_files, use_container_width=True)
    
    # กราฟความแม่นยำ
    fig_accuracy = px.line(df_stats, x='วันที่', y='ความแม่นยำ',
                          title='ความแม่นยำของ AI')
    st.plotly_chart(fig_accuracy, use_container_width=True)
    
    # กราฟเวลาประมวลผล
    fig_time = px.line(df_stats, x='วันที่', y='เวลาประมวลผล',
                       title='เวลาประมวลผลเฉลี่ย (วินาที)')
    st.plotly_chart(fig_time, use_container_width=True)
    
    # ตารางสรุป
    st.markdown("### 📊 สรุปสถิติ")
    summary = {
        'เมตริก': ['จำนวนไฟล์ทั้งหมด', 'ความแม่นยำเฉลี่ย', 'เวลาประมวลผลเฉลี่ย'],
        'ค่า': [
            f"{df_stats['จำนวนไฟล์'].sum()} ไฟล์",
            f"{df_stats['ความแม่นยำ'].mean():.2%}",
            f"{df_stats['เวลาประมวลผล'].mean():.2f} วินาที"
        ]
    }
    st.table(pd.DataFrame(summary))

elif selected == "การตั้งค่า":
    colored_header(
        label="การตั้งค่าระบบ",
        description="ปรับแต่งการทำงานของระบบ",
        color_name="green-70"
    )
    
    # แท็บการตั้งค่า
    tab1, tab2, tab3 = st.tabs(["ทั่วไป", "AI", "การแจ้งเตือน"])
    
    with tab1:
        st.markdown("### ⚙️ การตั้งค่าทั่วไป")
        
        # ภาษา
        language = st.selectbox(
            "ภาษา",
            ["ไทย", "English"],
            index=0
        )
        
        # โฟลเดอร์จัดเก็บ
        storage_path = st.text_input(
            "ตำแหน่งจัดเก็บไฟล์",
            value="./data"
        )
        
        # การสำรองข้อมูล
        enable_backup = st.checkbox("เปิดใช้งานการสำรองข้อมูลอัตโนมัติ", value=True)
        if enable_backup:
            backup_interval = st.selectbox(
                "ความถี่ในการสำรองข้อมูล",
                ["ทุกวัน", "ทุกสัปดาห์", "ทุกเดือน"]
            )
    
    with tab2:
        st.markdown("### 🤖 การตั้งค่า AI")
        
        # โมเดล
        model_path = st.text_input(
            "ตำแหน่งโมเดล AI",
            value="./models/latest"
        )
        
        # ความแม่นยำ
        confidence_threshold = st.slider(
            "ค่าความเชื่อมั่นขั้นต่ำ",
            min_value=0.0,
            max_value=1.0,
            value=0.8,
            step=0.1
        )
        
        # GPU
        use_gpu = st.checkbox("ใช้งาน GPU (ถ้ามี)", value=True)
    
    with tab3:
        st.markdown("### 🔔 การแจ้งเตือน")
        
        # อีเมล
        enable_email = st.checkbox("เปิดใช้งานการแจ้งเตือนทางอีเมล", value=False)
        if enable_email:
            email_address = st.text_input("อีเมลผู้รับ")
        
        # Line Notify
        enable_line = st.checkbox("เปิดใช้งานการแจ้งเตือนผ่าน Line", value=False)
        if enable_line:
            line_token = st.text_input("Line Notify Token")
    
    # บันทึกการตั้งค่า
    if st.button("บันทึกการตั้งค่า"):
        settings = {
            "general": {
                "language": language,
                "storage_path": storage_path,
                "backup": {
                    "enabled": enable_backup,
                    "interval": backup_interval if enable_backup else None
                }
            },
            "ai": {
                "model_path": model_path,
                "confidence_threshold": confidence_threshold,
                "use_gpu": use_gpu
            },
            "notifications": {
                "email": {
                    "enabled": enable_email,
                    "address": email_address if enable_email else None
                },
                "line": {
                    "enabled": enable_line,
                    "token": line_token if enable_line else None
                }
            }
        }
        
        try:
            # บันทึกการตั้งค่า
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            st.success("บันทึกการตั้งค่าสำเร็จ!")
            
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {str(e)}")
            logger.error(f"เกิดข้อผิดพลาดในการบันทึกการตั้งค่า: {str(e)}")

else:  # เกี่ยวกับ
    colored_header(
        label="เกี่ยวกับระบบ",
        description="ข้อมูลเกี่ยวกับ Excel Processor",
        color_name="green-70"
    )
    
    st.markdown("""
    ### 📊 Excel Processor
    
    ระบบประมวลผล Excel อัจฉริยะ พัฒนาโดยทีม ZanKinZuiTH
    
    #### ความสามารถหลัก
    - 📝 ประมวลผลไฟล์ Excel อัตโนมัติ
    - 🤖 วิเคราะห์ข้อมูลด้วย AI
    - 📊 สร้างรายงานและกราฟอัตโนมัติ
    - 🔄 ระบบเทมเพลตอัจฉริยะ
    
    #### เวอร์ชัน
    - เวอร์ชันปัจจุบัน: 1.0.0
    - อัปเดตล่าสุด: กุมภาพันธ์ 2024
    
    #### การติดต่อ
    - อีเมล: support@zankinzui.com
    - เว็บไซต์: https://zankinzui.com
    - GitHub: https://github.com/ZanKinZuiTH
    
    #### ลิขสิทธิ์
    © 2024 ZanKinZuiTH. All rights reserved.
    """)
    
    # แสดงสถานะระบบ
    st.markdown("### 🔧 สถานะระบบ")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "หน่วยความจำที่ใช้",
            "45%",
            "ปกติ"
        )
    with col2:
        st.metric(
            "การใช้งาน CPU",
            "30%",
            "ปกติ"
        )
    with col3:
        st.metric(
            "พื้นที่เหลือ",
            "5.2 GB",
            "-250 MB"
        ) 