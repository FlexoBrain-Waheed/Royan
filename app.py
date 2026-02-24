import streamlit as st
import pandas as pd
import plotly.express as px

# دوال مساعدة لترتيب الأرقام بأمان بدون تدخل مع النصوص العربية
def fmt(num):
    return "{:,.0f}".format(num)

def fmt1(num):
    return "{:,.1f}".format(num)

st.set_page_config(page_title="Royan Flexo Smart ERP", layout="wide", page_icon="⚙️")
st.title("مجموعة رويان - نظام المحاكاة الذكي | Royan Group - Smart Simulation System")
st.markdown("---")

tab_materials, tab_printing, tab_lamination, tab_machines, tab_hr_admin, tab_finance = st.tabs([
    "📦 1. المواد الخام | Raw Materials", 
    "🖨️ 2. الطباعة | Printing", 
    "🥪 3. اللامنيشن | Lamination", 
    "🏭 4. الأصول | Assets",
    "👥 5. الموارد البشرية | HR & Admin",
    "📊 6. المالية | Financials"
])

# ==========================================
# TAB 1: Materials
# ==========================================
with tab_materials:
    st.header("إعدادات المواد الخام | Raw Materials Setup")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Transparent BOPP")
        bopp_t_price = st.number_input("السعر | Price (SAR/Ton) - T.BOPP", value=6000)
        bopp_t_density = st.number_input("الك
