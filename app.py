import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Royan Flexo Smart ERP", layout="wide", page_icon="⚙️")
st.title("مجموعة رويان - نظام المحاكاة الذكي للإنتاج والتكاليف")
st.markdown("---")

# --- تقسيم الشاشة إلى 6 أقسام ---
tab_materials, tab_printing, tab_lamination, tab_machines, tab_hr_admin, tab_finance = st.tabs([
    "📦 1. المواد الخام", 
    "🖨️ 2. قسم الطباعة", 
    "🥪 3. قسم اللامنيشن", 
    "🏭 4. الماكينات والأصول",
    "👥 5. الموارد البشرية والإدارة",
    "📊 6. الخلاصة المالية"
])

# ==========================================
# TAB 1: المواد الخام والتسعير
# ==========================================
with tab_materials:
    st.header("إعدادات المواد الخام")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Transparent BOPP")
        bopp_t_price = st.number_input("السعر (ريال/طن) - شفاف", value=6000)
        bopp_t_density = st.number_input("الكثافة - شفاف", value=0.91)
        
        st.subheader("White BOPP")
        bopp_w_price = st.number_input("السعر (ريال/طن) - أبيض", value=6400)
        bopp_w_density = st.number_input("الكثافة - أبيض", value=0.65)

    with col2:
        st.subheader("Metallized BOPP")
        bopp_m_price = st.number_input("السعر (ريال/طن) - ميتاليز", value=7000)
        bopp_m_density = st.number_input("الكثافة - ميتاليز", value=0.91)
        
        st.subheader("Polyester PET")
        pet_price = st.number_input("السعر (ريال/طن) - بوليستر", value=5500)
        pet_density = st.number_input("الكثافة - بوليستر", value=1.40)

    with col3:
        st.subheader("PE (Polyethylene)")
        pe_price = st
