import streamlit as st
import pandas as pd
import plotly.express as px

def fmt(num):
    return "{:,.0f}".format(num)

def fmt1(num):
    return "{:,.1f}".format(num)

st.set_page_config(page_title="Royan Flexo Smart ERP", layout="wide", page_icon="⚙️")
st.title("Royan Smart ERP | مجموعة رويان - نظام المحاكاة الذكي")
st.markdown("---")

# --- تقسيم الشاشة ---
tab_materials, tab_printing, tab_lamination, tab_machines, tab_hr_admin, tab_finance = st.tabs([
    "1. Materials | المواد الخام", 
    "2. Printing | الطباعة", 
    "3. Lamination | اللامنيشن", 
    "4. Assets | الأصول",
    "5. HR & Admin | الموارد البشرية",
    "6. Financials | المالية"
])

# ==========================================
# TAB 1: المواد الخام 
# ==========================================
with tab_materials:
    st.header("Raw Materials | إعدادات المواد الخام")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Transparent BOPP")
        bopp_t_price = st.number_input("Price (SAR/Ton) - T.BOPP | السعر", value=6000)
        bopp_t_density = st.number_input("Density - T.BOPP | الكثافة", value=0.91)
        st.subheader("White BOPP")
        bopp_w_price = st.number_input("Price (SAR/Ton) - W.BOPP | السعر", value=6400)
        bopp_w_density = st.number_input("Density - W.BOPP | الكثافة", value=0.65)
        
    with col2:
        st.subheader("Metallized BOPP")
        bopp_m_price = st.number_input("Price (SAR/Ton) - M.BOPP | السعر", value=7000)
        bopp_m_density = st.number_input("Density - M.BOPP | الكثافة", value=0.91)
        st.subheader("Polyester PET")
        pet_price = st.number_input("Price (SAR/Ton) - PET | السعر", value=5500)
        pet_density = st.number_input("Density - PET | الكثافة", value=1.40)
        
    with col3:
        st.subheader("PE (Polyethylene)")
        pe_price = st.number_input("Price (SAR/Ton) - PE | السعر", value=5000)
        pe_density = st.number_input("Density - PE | الكثافة", value=0.92)

    materials_db = {
        "Transparent BOPP": {"density": bopp_t_density, "price": bopp_t_price},
        "White BOPP": {"density": bopp_w_density, "price": bopp_w_price},
        "Metallized BOPP": {"density": bopp_m_density, "price": bopp_m_price},
        "Polyester PET": {"density": pet_density, "price": pet_price},
        "PE (Polyethylene)": {"density": pe_density, "price": pe_price}
    }

    st.markdown("---")
    col_m1, col_m2, col_m3 = st.columns(3)
    ink_price = col_m1.number_input("Ink Price | سعر الحبر", value=15.0)
    solvent_price = col_m2.number_input("Solvent Price | سعر السولفنت", value=7.0)
    solvent_ratio = col_m3.number_input("Solvent Ratio | نسبة السولفنت", value=1.2)

# ==========================================
# TAB 2: الطباعة 
# ==========================================
with tab_printing:
    st.header("Printing | قسم الطباعة")
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        machine_speed = st.slider("Speed (m/min) | السرعة", 100, 500, 350)
        web_width_mm = st.slider("Width (mm) | العرض", 400, 1300, 1000)
        ink_coverage = st.number_input("Ink Coverage | تغطية الحبر", value=5.0)
        
        base_mat = st.selectbox("Material Type | نوع المادة", list(materials_db.keys()))
        base_thickness = st.number_input("Thickness (Microns) | السماكة", value=20)
        
        base_density = materials_db[base_mat]["density"]
        base_price = materials_db[base_mat]["price"]
        
    with col_p2:
        jobs_per_month = st.slider("Jobs/Month | عدد الطلبيات", 1, 150, 60)
        total_lost_time = jobs_per_month * 120 
        printing_available_mins = 2 * 12 * 26 * 60 * 0.85 
        actual_printing_mins = printing_available_mins - total_lost_time

    web_width_m = web_width_mm / 1000.0
    linear_meters_per_month = machine_speed * actual_printing_mins
    sq_meters_per_month = linear_meters_per_month * web_width_m

    ink_kg_per_month = (sq_meters_per_month * ink_coverage) / 1000.0
    solvent_kg_per_month = ink_kg_per_month * solvent_ratio
    ink_cost_monthly = ink_kg_per_month * ink_price
    solvent_cost_monthly = solvent_kg_per_month * solvent_price
    
    base_film_gsm = base_thickness * base_density
    base_film_tons = (sq_meters_per_month * base_film_gsm) / 1000000.0
    base_film_cost = base_film_tons * base_price
    
    printed_roll_gsm = base_film_gsm + ink_coverage
    printing_prod_tons = (sq_meters_per_month * printed_roll_gsm) / 1000000.0

    st.markdown("---")
    col_res1, col_res2, col_res3 = st.columns(3)
    col_res1.metric("Linear M | أمتار طولية", fmt(linear_meters_per_month))
    col_res2.metric("Square M | أمتار مربعة", fmt(sq_meters_per_month))
    col_res3.metric("Weight (Ton) | الوزن", fmt1(printing_prod_tons))

# ==========================================
# TAB 3: اللامنيشن 
# ==========================================
with tab_lamination:
    st.header("Lamination | اللامنيشن")
    col_l1, col_l2 = st.columns([1, 2])
    
    with col_l1:
        lam_opts = [1, 2, 3, 4]
        num_layers = st.selectbox("Layers | الطبقات", lam_opts)
        passes = max(0, num_layers - 1)
        
        if passes > 0:
            adhesive_gsm = st.number_input("Adhesive | غراء", value=1.8)
            total_adhesive_gsm = adhesive_gsm * passes
        else:
            total_adhesive_gsm = 0.0

    with col_l2:
        layers_gsm_list = [printed_roll_gsm]
        total_raw_cost = base_film_cost 
        
        if num_layers > 1:
            for i in range(2, num_layers + 1):
                col_m, col_t = st.columns(2)
                l_mat = col_m.selectbox("Mat "+str(i)+" | مادة "+str(i), list(materials_db.keys()), key="m_"+str(i))
                l_thk = col_t.number_input("Thk "+str(i)+" | سماكة "+str(i), value=20, key="t_"+str(i))
                
                l_den = materials_db[l_mat]["density"]
                l_price = materials_db[l_mat]["price"]
                l_gsm = l_thk * l_den
                layers_gsm_list.append(l_gsm)
                
                l_tons = (sq_meters_per_month * l_gsm) / 1000000.0
                total_raw_cost += (l_tons * l_price)

    final_product_gsm = sum(layers_gsm_list) + total_adhesive_gsm
    adhesive_kg = (sq_meters_per_month * total_adhesive_gsm) / 1000.0
    final_tons = (sq_meters_per_month * final_product_gsm) / 1000000.0

    st.markdown("---")
    col_cap1, col_cap2 = st.columns(2)
    with col_cap1:
        lam_speed = st.slider("Lam Speed | سرعة اللامنيشن", 100, 500, 350)
        lam_max_m = lam_speed * (2 * 12 * 26 * 60 * 0.85)

    with col_cap2:
        req_lam_m = linear_meters_per_month * passes
        utilization = (req_lam_m / lam_max_m) * 100 if lam_max_m > 0 else 0
        st.write("Utilization | استهلاك الماكينة: **" + fmt1(utilization) + "%**")

# ==========================================
# TAB 4: الأصول 
# ==========================================
with tab_machines:
    st.header("Assets & Utilities | الأصول")
    col_e1, col_e2 = st.columns(2)
    elec_rate = col_e1.number_input("kWh Rate | الكيلوواط", value=0.18)
    work_hrs = col_e2.number_input("Work Hours | ساعات العمل", value=624)

    mac_data = [
        {"Machine": "Flexo / فلكسو", "Cost": 8000000, "Years": 15, "kW": 150},
        {"Machine": "Lamination / لامنيشن", "Cost": 1200000, "Years": 15, "kW": 125},
        {"Machine": "Extruder / إكسترودر", "Cost": 5000000, "Years": 15, "kW": 250},
        {"Machine": "Slitter / قطاعة", "Cost": 800000, "Years": 15, "kW": 40},
        {"Machine": "Bags / أكياس", "Cost": 620000, "Years": 10, "kW": 50},
        {"Machine": "Building / مبنى", "Cost": 4000000, "Years": 25, "kW": 0},
    ]

    df_mac = st.data_editor(pd.DataFrame(mac_data), use_container_width=True)
    df_mac["Deprec"] =
