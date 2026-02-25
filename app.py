import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Royan Flexo Smart ERP", layout="wide", page_icon="⚙️")
st.title("مجموعة رويان - نظام المحاكاة الذكي للإنتاج والتكاليف")
st.markdown("---")

# --- تقسيم الشاشة إلى 7 أقسام ---
tab_names = [
    "📦 1. المواد الخام", 
    "🖨️ 2. قسم الطباعة", 
    "🥪 3. قسم اللامنيشن", 
    "🏭 4. الماكينات والأصول",
    "👥 5. الموارد البشرية",
    "📊 6. الخلاصة المالية",
    "⚖️ 7. مقارنة روتو ضد فلكسو"
]

(
    tab_materials, 
    tab_printing, 
    tab_lamination, 
    tab_machines, 
    tab_hr_admin, 
    tab_finance,
    tab_compare
) = st.tabs(tab_names)

# ==========================================
# TAB 1: المواد الخام
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
        pe_price = st.number_input("السعر (ريال/طن) - بولي إيثيلين", value=5000)
        pe_density = st.number_input("الكثافة - بولي إيثيلين", value=0.92)

    materials_db = {
        "Transparent BOPP": {"density": bopp_t_density, "price": bopp_t_price},
        "White BOPP": {"density": bopp_w_density, "price": bopp_w_price},
        "Metallized BOPP": {"density": bopp_m_density, "price": bopp_m_price},
        "Polyester PET": {"density": pet_density, "price": pet_price},
        "PE (Polyethylene)": {"density": pe_density, "price": pe_price}
    }

    st.markdown("---")
    st.subheader("إعدادات الأحبار والمذيبات")
    col_m1, col_m2, col_m3 = st.columns(3)
    ink_price = col_m1.number_input("سعر كيلو الحبر (ريال)", value=15.0)
    solvent_price = col_m2.number_input("سعر كيلو السولفنت (ريال)", value=7.0)
    solvent_ratio = col_m3.number_input("نسبة خلط السولفنت للحبر", value=1.2)

# ==========================================
# TAB 2: قسم الطباعة
# ==========================================
with tab_printing:
    st.header("قسم الطباعة")
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        machine_speed = st.slider("سرعة ماكينة الطباعة (متر/دقيقة)", 100, 500, 350)
        web_width_mm = st.slider("عرض رول الطباعة (ملم)", 400, 1300, 1000)
        ink_coverage = st.number_input("تغطية الحبر (جرام/متر مربع)", value=5.0)
        
        st.markdown("**مواصفات فيلم الطباعة (الطبقة الأولى)**")
        base_material_name = st.selectbox("نوع مادة الطباعة", list(materials_db.keys()))
        base_thickness = st.number_input("سماكة فيلم الطباعة (ميكرون)", value=20)
        
        base_density = materials_db[base_material_name]["density"]
        base_price = materials_db[base_material_name]["price"]
        
    with col_p2:
        st.warning("⏱️ تأثير تغييرات الأعمال")
        jobs_per_month = st.slider("عدد تغييرات الأعمال شهرياً", 1, 150, 60)
        changeover_time = 120 
        total_lost_time = jobs_per_month * changeover_time
        
        printing_available_mins = 2 * 12 * 26 * 60 * 0.85 
        actual_printing_mins = printing_available_mins - total_lost_time
        
        st.success(f"دقائق التشغيل الفعلي الصافي: {actual_printing_mins:,.0f} دقيقة")

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
    col_len1, col_len2 = st.columns(2)
    col_len1.info(f"📏 الأمتار الطولية المطبوعة: {linear_meters_per_month:,.0f} متر")
    col_len2.info(f"📐 الأمتار المربعة المطبوعة: {sq_meters_per_month:,.0f} متر مربع")

# ==========================================
# TAB 3: قسم اللامنيشن 
# ==========================================
with tab_lamination:
    st.header("قسم اللامنيشن وبناء الطبقات")
    col_l1, col_l2 = st.columns([1, 2])
    
    with col_l1:
        num_layers = st.selectbox(
            "عدد طبقات المنتج", 
            [1, 2, 3, 4], 
            format_func=lambda x: "1 (بدون لامنيشن)" if x == 1 else str(x)
        )
        passes = max(0, num_layers - 1)
        
        if passes > 0:
            adhesive_gsm = st.number_input("وزن غراء اللامنيشن للتمريرة", value=1.8)
            total_adhesive_gsm = adhesive_gsm * passes
        else:
            total_adhesive_gsm = 0.0

    with col_l2:
        layers_gsm_list = [printed_roll_gsm]
        total_raw_materials_cost = base_film_cost_monthly 
        
        if num_layers > 1:
            for i in range(2, num_layers + 1):
                col_mat, col_thk = st.columns(2)
                layer_mat_name = col_mat.selectbox(
                    f"مادة الطبقة {i}", 
                    list(materials_db.keys()), 
                    key=f"mat_{i}"
                )
                layer_thk = col_thk.number_input(
                    "السماكة (ميكرون)", 
                    value=20, 
                    key=f"thk_{i}"
                )
                
                layer_density = materials_db[layer_mat_name]["density"]
                layer_price = materials_db[layer_mat_name]["price"]
                
                layer_gsm = layer_thk * layer_density
                layers_gsm_list.append(layer_gsm)
                
                layer_tons = (sq_meters_per_month * layer_gsm) / 1000000.0
                layer_cost = layer_tons * layer_price
                total_raw_materials_cost += layer_cost

    total_substrate_gsm = sum(layers_gsm_list)
    final_product_gsm = total_substrate_gsm + total_adhesive_gsm
    
    adhesive_consumed_kg = (sq_meters_per_month * total_adhesive_gsm) / 1000.0
    final_production_tons = (sq_meters_per_month * final_product_gsm) / 1000000.0

    st.markdown("---")
    col_cap1, col_cap2 = st.columns(2)
    with col_cap1:
        lam_machine_speed = st.slider("سرعة اللامنيشن (متر/دقيقة)", 100, 500, 350)
        lam_max_capacity_meters = lam_machine_speed * (2 * 12 * 26 * 60 * 0.85)

    with col_cap2:
        total_lam_run_meters = linear_meters_per_month * passes
        if lam_max_capacity_meters > 0:
            utilization = (total_lam_run_meters / lam_max_capacity_meters) * 100
        else:
            utilization = 0

        st.write(f"🔄 التشغيل المطلوب للامنيشن: {total_lam_run_meters:,.0f} متر")
        if passes == 0:
            st.success("✅ المنتج طباعة فقط ولا يمر على اللامنيشن.")
        elif utilization <= 100:
            st.success(f"✅ نسبة استهلاك الماكينة: {utilization:.1f}%")
        else:
            st.
