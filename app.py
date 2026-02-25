import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def fmt(num):
    return "{:,.0f}".format(num)

def fmt1(num):
    return "{:,.1f}".format(num)

st.set_page_config(layout="wide", page_title="Royan ERP", page_icon="⚙️")

st.title("Royan Smart ERP | رويان - نظام المحاكاة")
st.markdown("---")

t1 = "1. المواد الخام"
t2 = "2. الطباعة"
t3 = "3. اللامنيشن"
t4 = "4. الأصول"
t5 = "5. الموارد البشرية"
t6 = "6. المالية"
t7 = "7. مقارنة التقنيات"
t8 = "8. تحليل العميل"

tabs = st.tabs([t1, t2, t3, t4, t5, t6, t7, t8])
tab_mat = tabs[0]
tab_prn = tabs[1]
tab_lam = tabs[2]
tab_mac = tabs[3]
tab_hr = tabs[4]
tab_fin = tabs[5]
tab_comp = tabs[6]
tab_mix = tabs[7]

# ==========================================
# TAB 1: Materials
# ==========================================
with tab_mat:
    st.header("إعدادات المواد الخام")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.subheader("Transparent BOPP")
        bopp_t_price = st.number_input("سعر T.BOPP", value=6000)
        bopp_t_density = st.number_input("كثافة T.BOPP", value=0.91)
        st.subheader("White BOPP")
        bopp_w_price = st.number_input("سعر W.BOPP", value=6400)
        bopp_w_density = st.number_input("كثافة W.BOPP", value=0.65)
        
    with c2:
        st.subheader("Metallized BOPP")
        bopp_m_price = st.number_input("سعر M.BOPP", value=7000)
        bopp_m_density = st.number_input("كثافة M.BOPP", value=0.91)
        st.subheader("Polyester PET")
        pet_price = st.number_input("سعر PET", value=5500)
        pet_density = st.number_input("كثافة PET", value=1.40)
        
    with c3:
        st.subheader("Polyethylene PE")
        pe_price = st.number_input("سعر PE", value=5000)
        pe_density = st.number_input("كثافة PE", value=0.92)

    materials_db = {
        "Transparent BOPP": {"density": bopp_t_density, "price": bopp_t_price},
        "White BOPP": {"density": bopp_w_density, "price": bopp_w_price},
        "Metallized BOPP": {"density": bopp_m_density, "price": bopp_m_price},
        "Polyester PET": {"density": pet_density, "price": pet_price},
        "PE (Polyethylene)": {"density": pe_density, "price": pe_price}
    }

    st.markdown("---")
    st.subheader("الأحبار والمذيبات")
    cm1, cm2, cm3 = st.columns(3)
    ink_price = cm1.number_input("سعر الحبر", value=15.0)
    solvent_price = cm2.number_input("سعر السولفنت", value=7.0)
    solvent_ratio = cm3.number_input("نسبة السولفنت", value=1.2)

# ==========================================
# TAB 2: Printing
# ==========================================
with tab_prn:
    st.header("قسم الطباعة")
    cp1, cp2 = st.columns(2)
    
    with cp1:
        machine_speed = st.slider("سرعة الطباعة", 100, 500, 350)
        web_width_mm = st.slider("عرض الرول", 400, 1300, 1000)
        ink_coverage = st.number_input("تغطية الحبر", value=5.0)
        
        base_mat = st.selectbox("مادة الطباعة", list(materials_db.keys()))
        base_thickness = st.number_input("سماكة فيلم الطباعة", value=20)
        
        base_density = materials_db[base_mat]["density"]
        base_price = materials_db[base_mat]["price"]
        
    with cp2:
        jobs_per_month = st.slider("الطلبيات شهريا", 1, 150, 60)
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
    cr1, cr2, cr3 = st.columns(3)
    cr1.metric("أمتار طولية", fmt(linear_meters_per_month))
    cr2.metric("أمتار مربعة", fmt(sq_meters_per_month))
    cr3.metric("وزن الطباعة طن", fmt1(printing_prod_tons))

# ==========================================
# TAB 3: Lamination
# ==========================================
with tab_lam:
    st.header("قسم اللامنيشن")
    cl1, cl2 = st.columns([1, 2])
    
    with cl1:
        num_layers = st.selectbox("عدد الطبقات", [1, 2, 3, 4])
        passes = max(0, num_layers - 1)
        
        if passes > 0:
            adhesive_gsm = st.number_input("غراء للتمريرة", value=1.8)
            total_adhesive_gsm = adhesive_gsm * passes
        else:
            total_adhesive_gsm = 0.0

    with cl2:
        layers_gsm_list = [printed_roll_gsm]
        total_raw_cost = base_film_cost 
        
        if num_layers > 1:
            for i in range(2, num_layers + 1):
                cm, ct = st.columns(2)
                l_mat = cm.selectbox("مادة "+str(i), list(materials_db.keys()), key="m_"+str(i))
                l_thk = ct.number_input("سماكة "+str(i), value=20, key="t_"+str(i))
                
                l_den = materials_db[l_mat]["density"]
                l_price = materials_db[l_mat]["price"]
                l_
