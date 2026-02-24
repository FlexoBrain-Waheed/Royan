import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Royan Flexo Smart ERP", layout="wide", page_icon="⚙️")
st.title("مجموعة رويان - نظام المحاكاة الذكي للإنتاج والتكاليف")
st.markdown("---")

# --- تقسيم الشاشة إلى 5 أقسام (Tabs) ---
tab_materials, tab_printing, tab_lamination, tab_machines, tab_finance = st.tabs([
    "📦 1. المواد الخام (Materials)", 
    "🖨️ 2. قسم الطباعة (Printing)", 
    "🥪 3. قسم اللامنيشن (Lamination)", 
    "🏭 4. الماكينات والأصول (Machinery)",
    "📊 5. الخلاصة المالية (Financials)"
])

# ==========================================
# TAB 1: المواد الخام والتسعير
# ==========================================
with tab_materials:
    st.header("إعدادات المواد الخام (Raw Materials Setup)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Transparent BOPP")
        bopp_t_price = st.number_input("Price (SAR/Ton) - Trans BOPP", value=6000)
        bopp_t_density = st.number_input("Density (g/cm3) - Trans BOPP", value=0.91)
        
        st.subheader("White BOPP")
        bopp_w_price = st.number_input("Price (SAR/Ton) - White BOPP", value=6400)
        bopp_w_density = st.number_input("Density (g/cm3) - White BOPP", value=0.65)

    with col2:
        st.subheader("Metallized BOPP")
        bopp_m_price = st.number_input("Price (SAR/Ton) - Met BOPP", value=7000)
        bopp_m_density = st.number_input("Density (g/cm3) - Met BOPP", value=0.91)
        
        st.subheader("Polyester PET")
        pet_price = st.number_input("Price (SAR/Ton) - PET", value=5500)
        pet_density = st.number_input("Density (g/cm3) - PET", value=1.40)

    with col3:
        st.subheader("PE (Polyethylene)")
        pe_price = st.number_input("Price (SAR/Ton) - PE", value=5000)
        pe_density = st.number_input("Density (g/cm3) - PE", value=0.92)

    st.markdown("---")
    st.subheader("إعدادات الأحبار والمذيبات (Inks & Solvents)")
    col_m1, col_m2, col_m3 = st.columns(3)
    ink_price = col_m1.number_input("سعر كيلو الحبر (SAR/Kg)", value=15.0)
    solvent_price = col_m2.number_input("سعر كيلو السولفنت (SAR/Kg)", value=7.0)
    solvent_ratio = col_m3.number_input("نسبة السولفنت للحبر (مثلاً 1.2)", value=1.2)

# ==========================================
# TAB 2: قسم الطباعة والتغييرات
# ==========================================
with tab_printing:
    st.header("قسم الطباعة (Printing Department)")
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        machine_speed = st.slider("سرعة ماكينة الطباعة (متر/دقيقة)", 100, 500, 350)
        web_width_mm = st.slider("عرض رول الطباعة (ملم)", 400, 1300, 1000)
        ink_coverage = st.number_input("تغطية الحبر (جرام/متر مربع - Ink GSM)", value=5.0)
        
        st.markdown("**مواصفات فيلم الطباعة (الطبقة الأولى - المطبوعة)**")
        base_thickness = st.number_input("سماكة فيلم الطباعة (ميكرون)", value=20)
        base_density = st.number_input("كثافة فيلم الطباعة", value=0.91)
        
    with col_p2:
        st.warning("⏱️ تأثير تغييرات الأعمال (Job Changeovers)")
        jobs_per_month = st.slider("عدد تغييرات الأعمال شهرياً", 1, 150, 60)
        changeover_time = 120 # دقيقة لكل تغيير
        total_lost_time = jobs_per_month * changeover_time
        
        # حساب الوقت الفعلي للطباعة
        printing_available_mins = 2 * 12 * 26 * 60 * 0.85 # 85% كفاءة
        actual_printing_mins = printing_available_mins - total_lost_time
        
        st.write(f"إجمالي الدقائق المتاحة شهرياً: **{printing_available_mins:,.0f} دقيقة**")
        st.write(f"الوقت الضائع في التجهيز: **{total_lost_time:,.0f} دقيقة**")
        st.success(f"دقائق التشغيل الفعلي الصافي: **{actual_printing_mins:,.0f} دقيقة**")

    # حسابات المساحة والأطوال للطباعة
    web_width_m = web_width_mm / 1000.0
    linear_meters_per_month = machine_speed * actual_printing_mins
    sq_meters_per_month = linear_meters_per_month * web_width_m

    # مخرجات الطباعة
    st.markdown("---")
    st.subheader("📊 مخرجات قسم الطباعة (Printing Outputs)")
    
    col_len1, col_len2 = st.columns(2)
    col_len1.info(f"📏 **إجمالي الأمتار الطولية المطبوعة:** {linear_meters_per_month:,.0f} متر طول")
    col_len2.info(f"📐 **إجمالي الأمتار المربعة المطبوعة:** {sq_meters_per_month:,.0f} متر مربع")
    
    ink_kg_per_month = (sq_meters_per_month * ink_coverage) / 1000.0
    solvent_kg_per_month = ink_kg_per_month * solvent_ratio
    
    ink_cost_monthly = ink_kg_per_month * ink_price
    solvent_cost_monthly = solvent_kg_per_month * solvent_price
    
    base_film_gsm = base_thickness * base_density
    printed_roll_gsm = base_film_gsm + ink_coverage
    printing_production_tons = (sq_meters_per_month * printed_roll_gsm) / 1000000.0

    col_res1, col_res2, col_res3, col_res4, col_res5 = st.columns(5)
    col_res1.metric("كمية الحبر", f"{ink_kg_per_month:,.0f} كجم")
    col_res2.metric("كمية السولفنت", f"{solvent_kg_per_month:,.0f} كجم")
    col_res3.metric("تكلفة الحبر", f"{ink_cost_monthly:,.0f} ريال")
    col_res4.metric("تكلفة السولفنت", f"{solvent_cost_monthly:,.0f} ريال")
    col_res5.metric("الوزن الإجمالي المطبوع", f"{printing_production_tons:,.1f} طن")

# ==========================================
# TAB 3: قسم اللامنيشن والهيكلة الديناميكية
# ==========================================
with tab_lamination:
    st.header("قسم اللامنيشن وبناء الطبقات (Structure & Lamination)")
    
    col_l1, col_l2 = st.columns([1, 2])
    
    with col_l1:
        num_layers = st.selectbox("عدد طبقات المنتج النهائي (Layers)", [2, 3, 4])
        passes = num_layers - 1
        adhesive_gsm = st.number_input("وزن غراء اللامنيشن (g/m2) للتمريرة", value=1.8)
        total_adhesive_gsm = adhesive_gsm * passes
        st.info(f"إجمالي الغراء للمنتج: **{total_adhesive_gsm} g/m2** (عدد التمريرات: {passes})")

    with col_l2:
        st.subheader("بناء الهيكل الهندسي (Product Structure)")
        layers_gsm_list = []
        
        st.markdown(f"**الطبقة 1 (الرول المطبوع):** سماكة {base_thickness} ميكرون + حبر = **{printed_roll_gsm:.2f} g/m2**")
        layers_gsm_list.append(printed_roll_gsm)
        
        materials_dict = {
            "Transparent BOPP": bopp_t_density,
            "White BOPP": bopp_w_density,
            "Metallized BOPP": bopp_m_density,
            "Polyester PET": pet_density,
            "PE (Polyethylene)": pe_density
        }
        
        for i in range(2, num_layers + 1):
            st.markdown(f"**الطبقة {i}:**")
            col_mat, col_thk = st.columns(2)
            layer_mat = col_mat.selectbox(f"نوع المادة", list(materials_dict.keys()), key=f"mat_{i}")
            layer_thk = col_thk.number_input(f"السماكة (ميكرون)", value=20, key=f"thk_{i}")
            
            layer_density = materials_dict[layer_mat]
            layer_gsm = layer_thk * layer_density
            layers_gsm_list.append(layer_gsm)
            st.caption(f"وزن {layer_mat}: {layer_gsm:.2f} g/m2 (الكثافة: {layer_density})")

    st.markdown("---")
    st.subheader("⚙️ طاقة ماكينة اللامنيشن والتوافق مع الطباعة (Machine Utilization)")
    
    col_cap1, col_cap2 = st.columns(2)
    with col_cap1:
        lam_machine_speed = st.slider("سرعة ماكينة اللامنيشن (متر/دقيقة)", 100, 500, 350)
        lam_available_mins = 2 * 12 * 26 * 60 * 0.85 
        lam_max_capacity_meters = lam_machine_speed * lam_available_mins

    with col_cap2:
        total_lam_run_meters = linear_meters_per_month * passes
        utilization = (total_lam_run_meters / lam_max_capacity_meters) * 100 if lam_max_capacity_meters > 0 else 0

        st.write(f"🔄 **إجمالي التشغيل الطولي المطلوب للامنيشن:** {total_lam_run_meters:,.0f} متر")
        st.write(f"🏭 **الطاقة القصوى لماكينة اللامنيشن شهرياً:** {lam_max_capacity_meters:,.0f} متر")

        if utilization <= 100:
            st.success(f"✅ نسبة استهلاك الماكينة: **{utilization:.1f}%**")
        else:
            st.error(f"⚠️ تحذير اختناق (Bottleneck): نسبة استهلاك الماكينة **{utilization:.1f}%**!")

    total_substrate_gsm = sum(layers_gsm_list)
    final_product_gsm = total_substrate_gsm + total_adhesive_gsm
    
    weight_without_adhesive_tons = (sq_meters_per_month * total_substrate_gsm) / 1000000.0
    adhesive_consumed_kg = (sq_meters_per_month * total_adhesive_gsm) / 1000.0
    final_production_tons = (sq_meters_per_month * final_product_gsm) / 1000000.0

    st.markdown("---")
    st.subheader("📊 مخرجات قسم اللامنيشن والإنتاج النهائي (Lamination Outputs)")
    
    col_out1, col_out2, col_out3 = st.columns(3)
    col_out1.metric("الوزن الصافي (بدون غراء)", f"{weight_without_adhesive_tons:,.1f} طن")
    col_out2.metric("كمية الغراء المستهلكة", f"{adhesive_consumed_kg:,.0f} كجم")
    col_out3.metric("الوزن النهائي (مع الغراء)", f"{final_production_tons:,.1f} طن")

# ==========================================
# TAB 4: الماكينات والأصول (القسم الجديد المضاف)
# ==========================================
with tab_machines:
    st.header("إدارة الأصول واستهلاك الطاقة (Assets & Utilities Management)")
    st.info("💡 يمكنك تعديل سعر الماكينة، سنوات إهلاكها، واستهلاكها للكهرباء مباشرة من الجدول بالأسفل. سيتم حساب الإهلاك الشهري وتكلفة الكهرباء تلقائياً وخصمها من الأرباح النهائية.")
    
    # إعدادات الكهرباء
    col_elec1, col_elec2 = st.columns(2)
    electricity_rate = col_elec1.number_input("سعر الكيلوواط/ساعة (SAR/kWh)", value=0.18, format="%.3f")
    working_hours_per_month = col_elec2.number_input("ساعات تشغيل المصنع شهرياً (ورديتين * 12 * 26)", value=624)

    # قائمة الماكينات الافتراضية
    default_machines = pd.DataFrame([
        {"Machine": "ماكينة طباعة فلكسو (CI Flexo)", "Cost_SAR": 8000000, "Life_Years": 15, "Power_kW": 150},
        {"Machine": "ماكينة لامنيشن (Solventless)", "Cost_SAR": 1200000, "Life_Years": 15, "Power_kW": 125},
        {"Machine": "إكسترودر (PE Extruder)", "Cost_SAR": 5000000, "Life_Years": 15, "Power_kW": 250},
        {"Machine": "قطاعة (Slitter)", "Cost_SAR": 800000, "Life_Years": 15, "Power_kW": 40},
        {"Machine": "ماكينات تقطيع الأكياس (1-5)", "Cost_SAR": 620000, "Life_Years": 10, "Power_kW": 50},
        {"Machine": "مبرد (Chiller)", "Cost_SAR": 400000, "Life_Years": 15, "Power_kW": 60},
        {"Machine": "كمبروسر هواء (Compressor)", "Cost_SAR": 200000, "Life_Years": 15, "Power_kW": 30},
        {"Machine": "تجهيزات المبنى والهنجر", "Cost_SAR": 4000000, "Life_Years": 25, "Power_kW": 0},
    ])

    st.markdown("### جدول الأصول (قابل للتعديل)")
    # استخدام st.data_editor ليتيح لك التعديل الحي على الأرقام وإضافة/حذف ماكينات!
    edited_machines = st.data_editor(default_machines, num_rows="dynamic", use_container_width=True)

    # الحسابات الذكية للإهلاك والكهرباء
    edited_machines["Monthly_Depreciation"] = edited_machines["Cost_SAR"] / (edited_machines["Life_Years"] * 12)
    # استهلاك الكهرباء = الكيلوواط * ساعات العمل * الكفاءة (نفترض 85% تشغيل فعلي للمواتير) * سعر الكيلوواط
    edited_machines["Monthly_Power_Cost"] = edited_machines["Power_kW"] * working_hours_per_month * 0.85 * electricity_rate

    total_capex = edited_machines["Cost_SAR"].sum()
    total_monthly_depreciation = edited_machines["Monthly_Depreciation"].sum()
    total_monthly_power = edited_machines["Monthly_Power_Cost"].sum()

    st.markdown("---")
    st.subheader("مخرجات قسم الأصول والتكاليف الثابتة (Overheads)")
    col_mac1, col_mac2, col_mac3 = st.columns(3)
    col_mac1.metric("إجمالي الأصول (CAPEX)", f"{total_capex:,.0f} ريال")
    col_mac2.metric("إجمالي الإهلاك الشهري", f"{total_monthly_depreciation:,.0f} ريال")
    col_mac3.metric("فاتورة الكهرباء الشهرية", f"{total_monthly_power:,.0f} ريال")

# ==========================================
# TAB 5: الخلاصة المالية (تم تحديثها لترتبط بالماكينات)
# ==========================================
with tab_finance:
    st.header("الخلاصة والنتائج (Financial Dashboard)")
    selling_price = st.slider("متوسط سعر بيع الطن للمنتج النهائي (ريال)", 10000, 25000, 14000, step=100)
    monthly_salaries = st.number_input("إجمالي الرواتب الشهرية والمصاريف الإدارية (SAR)", value=200000)
    
    adhesive_cost_monthly = adhesive_consumed_kg * 12 
    raw_material_avg_cost = final_production_tons * 6000 
    
    # التكلفة الإجمالية الآن تقرأ فاتورة الكهرباء والإهلاك من جدول الماكينات!
    total_monthly_cost = raw_material_avg_cost + ink_cost_monthly + solvent_cost_monthly + adhesive_cost_monthly + total_monthly_power + total_monthly_depreciation + monthly_salaries
    
    monthly_revenue = final_production_tons * selling_price
    monthly_profit = monthly_revenue - total_monthly_cost
    
    cost_per_ton = total_monthly_cost / final_production_tons if final_production_tons > 0 else 0

    st.markdown("### مؤشرات الأداء الرئيسية")
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    
    col_f1.metric("الإنتاج الشهري النهائي", f"{final_production_tons:,.1f} طن")
    col_f2.metric("التكلفة الفعلية للطن", f"{cost_per_ton:,.0f} ريال")
    col_f3.metric("المبيعات الشهرية", f"{monthly_revenue:,.0f} ريال")
    col_f4.metric("صافي الربح الشهري", f"{monthly_profit:,.0f} ريال")

    st.markdown("---")
    chart_data = {
        "البند": ["تكلفة المواد الخام", "الحبر والسولفنت", "غراء اللامنيشن", "الكهرباء", "الإهلاك الشهري للمعدات", "الرواتب والمصاريف"],
        "التكلفة": [raw_material_avg_cost, ink_cost_monthly + solvent_cost_monthly, adhesive_cost_monthly, total_monthly_power, total_monthly_depreciation, monthly_salaries]
    }
    df_chart = pd.DataFrame(chart_data)
    fig = px.pie(df_chart, values='التكلفة', names='البند', hole=0.4, title="التحليل الدقيق للتكاليف التشغيلية (OPEX + Overheads)")
    st.plotly_chart(fig, use_container_width=True)
