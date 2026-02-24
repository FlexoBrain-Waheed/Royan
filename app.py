import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Royan Flexo Smart ERP", layout="wide", page_icon="⚙️")
st.title("مجموعة رويان - نظام المحاكاة الذكي | Royan Group - Smart Simulation System")
st.markdown("---")

# --- تقسيم الشاشة إلى 6 أقسام ثنائية اللغة ---
tab_materials, tab_printing, tab_lamination, tab_machines, tab_hr_admin, tab_finance = st.tabs([
    "📦 1. المواد الخام | Raw Materials", 
    "🖨️ 2. الطباعة | Printing", 
    "🥪 3. اللامنيشن | Lamination", 
    "🏭 4. الأصول | Assets",
    "👥 5. الموارد البشرية | HR & Admin",
    "📊 6. المالية | Financials"
])

# ==========================================
# TAB 1: المواد الخام (Materials)
# ==========================================
with tab_materials:
    st.header("إعدادات المواد الخام | Raw Materials Setup")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Transparent BOPP")
        bopp_t_price = st.number_input("السعر | Price (SAR/Ton) - Trans BOPP", value=6000)
        bopp_t_density = st.number_input("الكثافة | Density (g/cm3) - Trans BOPP", value=0.91)
        
        st.subheader("White BOPP")
        bopp_w_price = st.number_input("السعر | Price (SAR/Ton) - White BOPP", value=6400)
        bopp_w_density = st.number_input("الكثافة | Density (g/cm3) - White BOPP", value=0.65)

    with col2:
        st.subheader("Metallized BOPP")
        bopp_m_price = st.number_input("السعر | Price (SAR/Ton) - Met BOPP", value=7000)
        bopp_m_density = st.number_input("الكثافة | Density (g/cm3) - Met BOPP", value=0.91)
        
        st.subheader("Polyester PET")
        pet_price = st.number_input("السعر | Price (SAR/Ton) - PET", value=5500)
        pet_density = st.number_input("الكثافة | Density (g/cm3) - PET", value=1.40)

    with col3:
        st.subheader("PE (Polyethylene)")
        pe_price = st.number_input("السعر | Price (SAR/Ton) - PE", value=5000)
        pe_density = st.number_input("الكثافة | Density (g/cm3) - PE", value=0.92)

    materials_db = {
        "Transparent BOPP": {"density": bopp_t_density, "price": bopp_t_price},
        "White BOPP": {"density": bopp_w_density, "price": bopp_w_price},
        "Metallized BOPP": {"density": bopp_m_density, "price": bopp_m_price},
        "Polyester PET": {"density": pet_density, "price": pet_price},
        "PE (Polyethylene)": {"density": pe_density, "price": pe_price}
    }

    st.markdown("---")
    st.subheader("الأحبار والمذيبات | Inks & Solvents")
    col_m1, col_m2, col_m3 = st.columns(3)
    ink_price = col_m1.number_input("سعر الحبر | Ink Price (SAR/Kg)", value=15.0)
    solvent_price = col_m2.number_input("سعر السولفنت | Solvent Price (SAR/Kg)", value=7.0)
    solvent_ratio = col_m3.number_input("نسبة خلط السولفنت | Solvent to Ink Ratio", value=1.2)

# ==========================================
# TAB 2: قسم الطباعة (Printing)
# ==========================================
with tab_printing:
    st.header("قسم الطباعة | Printing Department")
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        machine_speed = st.slider("سرعة الطباعة | Machine Speed (m/min)", 100, 500, 350)
        web_width_mm = st.slider("عرض الرول | Web Width (mm)", 400, 1300, 1000)
        ink_coverage = st.number_input("تغطية الحبر | Ink Coverage (g/m2)", value=5.0)
        
        st.markdown("**فيلم الطباعة (الطبقة 1) | Base Printing Film (Layer 1)**")
        base_material_name = st.selectbox("نوع المادة | Material Type", list(materials_db.keys()))
        base_thickness = st.number_input("السماكة | Thickness (Microns)", value=20)
        
        base_density = materials_db[base_material_name]["density"]
        base_price = materials_db[base_material_name]["price"]
        st.caption(f"الكثافة | Density: **{base_density}** --- السعر | Price: **{base_price:,.0f} SAR/Ton**")
        
    with col_p2:
        st.warning("⏱️ تغييرات الأعمال | Job Changeovers Impact")
        jobs_per_month = st.slider("عدد الطلبيات شهرياً | Jobs per month", 1, 150, 60)
        changeover_time = 120 
        total_lost_time = jobs_per_month * changeover_time
        
        printing_available_mins = 2 * 12 * 26 * 60 * 0.85 
        actual_printing_mins = printing_available_mins - total_lost_time
        
        st.success(f"دقائق التشغيل الصافي | Net Operating Mins: **{actual_printing_mins:,.0f}**")

    web_width_m = web_width_mm / 1000.0
    linear_meters_per_month = machine_speed * actual_printing_mins
    sq_meters_per_month = linear_meters_per_month * web_width_m

    ink_kg_per_month = (sq_meters_per_month * ink_coverage) / 1000.0
    solvent_kg_per_month = ink_kg_per_month * solvent_ratio
    ink_cost_monthly = ink_kg_per_month * ink_price
    solvent_cost_monthly = solvent_kg_per_month * solvent_price
    
    base_film_gsm = base_thickness * base_density
    base_film_tons_per_month = (sq_meters_per_month * base_film_gsm) / 1000000.0
    base_film_cost_monthly = base_film_tons_per_month * base_price
    
    printed_roll_gsm = base_film_gsm + ink_coverage
    printing_production_tons = (sq_meters_per_month * printed_roll_gsm) / 1000000.0

    st.markdown("---")
    st.subheader("📊 مخرجات الطباعة | Printing Outputs")
    col_len1, col_len2 = st.columns(2)
    col_len1.info(f"📏 أمتار طولية | Linear Meters: **{linear_meters_per_month:,.0f} m**")
    col_len2.info(f"📐 أمتار مربعة | Square Meters: **{sq_meters_per_month:,.0f} m2**")
    
    col_res1, col_res2, col_res3, col_res4 = st.columns(4)
    col_res1.metric("حبر وسولفنت | Ink & Solv
