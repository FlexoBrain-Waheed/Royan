import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Royan Flexo Smart ERP", layout="wide", page_icon="⚙️")
st.title("مجموعة رويان - نظام المحاكاة الذكي للإنتاج والتكاليف")
st.markdown("---")

# --- تقسيم الشاشة إلى 8 أقسام ---
tab_materials, tab_printing, tab_lamination, tab_machines, tab_hr_admin, tab_finance, tab_compare, tab_client_mix = st.tabs([
    "📦 1. المواد الخام",
    "🖨️ 2. قسم الطباعة",
    "🥪 3. قسم اللامنيشن",
    "🏭 4. الماكينات والأصول",
    "👥 5. الموارد البشرية",
    "📊 6. الخلاصة المالية",
    "⚖️ 7. مقارنة روتو ضد فلكسو",
    "🎯 8. تحليل كميات العميل"
])

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

        st.success("دقائق التشغيل الفعلي الصافي: " + "{:,.0f}".format(actual_printing_mins) + " دقيقة")

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
    col_len1.info("📏 إجمالي الأمتار الطولية المطبوعة: " + "{:,.0f}".format(linear_meters_per_month) + " متر")
    col_len2.info("📐 إجمالي الأمتار المربعة المطبوعة: " + "{:,.0f}".format(sq_meters_per_month) + " متر مربع")

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
                layer_mat_name = col_mat.selectbox("مادة الطبقة " + str(i), list(materials_db.keys()), key="mat_"+str(i))
                layer_thk = col_thk.number_input("السماكة (ميكرون) الطبقة " + str(i), value=20, key="thk_"+str(i))

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
        lam_machine_speed = st.slider("سرعة ماكينة اللامنيشن (متر/دقيقة)", 100, 500, 350)
        lam_max_capacity_meters = lam_machine_speed * (2 * 12 * 26 * 60 * 0.85)

    with col_cap2:
        total_lam_run_meters = linear_meters_per_month * passes
        if lam_max_capacity_meters > 0:
            utilization = (total_lam_run_meters / lam_max_capacity_meters) * 100
        else:
            utilization = 0

        st.write("🔄 التشغيل المطلوب للامنيشن: " + "{:,.0f}".format(total_lam_run_meters) + " متر")
        if passes == 0:
            st.success("✅ المنتج طباعة فقط ولا يمر على اللامنيشن.")
        elif utilization <= 100:
            st.success("✅ نسبة استهلاك الماكينة: " + "{:.1f}".format(utilization) + "%")
        else:
            st.error("⚠️ تحذير اختناق: نسبة الاستهلاك " + "{:.1f}".format(utilization) + "%")

# ==========================================
# TAB 4: الأصول والمعدات
# ==========================================
with tab_machines:
    st.header("إدارة الأصول واستهلاك الطاقة")
    col_elec1, col_elec2 = st.columns(2)
    electricity_rate = col_elec1.number_input("سعر الكيلوواط (ريال)", value=0.18)
    working_hours_per_month = col_elec2.number_input("ساعات التشغيل شهرياً", value=624)

    default_machines = pd.DataFrame([
        {"Machine": "طباعة فلكسو", "Cost_SAR": 8000000, "Life_Years": 15, "Power_kW": 150},
        {"Machine": "لامنيشن", "Cost_SAR": 1200000, "Life_Years": 15, "Power_kW": 125},
        {"Machine": "إكسترودر PE", "Cost_SAR": 5000000, "Life_Years": 15, "Power_kW": 250},
        {"Machine": "قطاعة", "Cost_SAR": 800000, "Life_Years": 15, "Power_kW": 40},
        {"Machine": "تقطيع أكياس", "Cost_SAR": 620000, "Life_Years": 10, "Power_kW": 50},
        {"Machine": "مبرد وكمبروسر", "Cost_SAR": 600000, "Life_Years": 15, "Power_kW": 90},
        {"Machine": "تجهيزات المبنى", "Cost_SAR": 4000000, "Life_Years": 25, "Power_kW": 0},
    ])

    edited_machines = st.data_editor(default_machines, num_rows="dynamic", use_container_width=True)
    edited_machines["Monthly_Depreciation"] = edited_machines["Cost_SAR"] / (edited_machines["Life_Years"] * 12)
    edited_machines["Monthly_Power"] = edited_machines["Power_kW"] * working_hours_per_month * 0.85 * electricity_rate

    total_monthly_depreciation = edited_machines["Monthly_Depreciation"].sum()
    total_monthly_power = edited_machines["Monthly_Power"].sum()

# ==========================================
# TAB 5: الموارد البشرية
# ==========================================
with tab_hr_admin:
    st.header("الموارد البشرية والمصاريف الإدارية")

    default_hr = pd.DataFrame([
        {"Job Title": "مدير المصنع", "Count": 1, "Basic_Salary": 15000},
        {"Job Title": "مهندس إنتاج", "Count": 2, "Basic_Salary": 8000},
        {"Job Title": "فني فلكسو", "Count": 2, "Basic_Salary": 5000},
        {"Job Title": "فني لامنيشن", "Count": 2, "Basic_Salary": 4000},
        {"Job Title": "فني تقطيع", "Count": 4, "Basic_Salary": 3500},
        {"Job Title": "مراقب جودة", "Count": 2, "Basic_Salary": 4000},
        {"Job Title": "فني صيانة", "Count": 2, "Basic_Salary": 4500},
        {"Job Title": "عمال", "Count": 8, "Basic_Salary": 1800},
        {"Job Title": "إداري/محاسب", "Count": 2, "Basic_Salary": 4000},
        {"Job Title": "مندوب مبيعات", "Count": 3, "Basic_Salary": 4500},
        {"Job Title": "سائق", "Count": 3, "Basic_Salary": 2500},
    ])

    edited_hr = st.data_editor(default_hr, num_rows="dynamic", use_container_width=True)

    col_hr1, col_hr2 = st.columns(2)
    allowances_percent = col_hr1.slider("نسبة البدلات %", 10, 50, 25)
    iqama_insurance_per_employee = col_hr2.number_input("تأمين وإقامة للموظف", value=600)

    total_headcount = edited_hr["Count"].sum()
    total_basic_salaries = (edited_hr["Count"] * edited_hr["Basic_Salary"]).sum()
    total_allowances = total_basic_salaries * (allowances_percent / 100.0)
    total_iqama_insurance = total_headcount * iqama_insurance_per_employee

    total_payroll_monthly = total_basic_salaries + total_allowances + total_iqama_insurance

    st.markdown("---")
    col_log1, col_log2, col_log3 = st.columns(3)
    trucks_count = col_log1.number_input("عدد السيارات", value=3)
    fuel_per_truck = col_log2.number_input("بنزين السيارة", value=1500)
    maintenance_per_truck = col_log3.number_input("صيانة السيارة", value=500)
    total_logistics_cost = trucks_count * (fuel_per_truck + maintenance_per_truck)

    st.markdown("---")
    col_adm1, col_adm2, col_adm3 = st.columns(3)
    factory_maintenance = col_adm1.number_input("صيانة المصنع", value=15000)
    hospitality_office = col_adm2.number_input("ضيافة ومكتبية", value=5000)
    gov_fees = col_adm3.number_input("رسوم حكومية", value=4000)

    total_admin_ops_cost = factory_maintenance + hospitality_office + gov_fees
    grand_total_hr_admin = total_payroll_monthly + total_logistics_cost + total_admin_ops_cost

# ==========================================
# TAB 6: الخلاصة المالية
# ==========================================
with tab_finance:
    st.header("الخلاصة والنتائج")
    selling_price = st.slider("سعر بيع الطن (ريال)", 10000, 25000, 14000, step=100)

    adhesive_cost_monthly = adhesive_consumed_kg * 12

    total_monthly_cost = (
        total_raw_materials_cost +
        ink_cost_monthly +
        solvent_cost_monthly +
        adhesive_cost_monthly +
        total_monthly_power +
        total_monthly_depreciation +
        grand_total_hr_admin
    )

    monthly_revenue = final_production_tons * selling_price
    monthly_profit = monthly_revenue - total_monthly_cost

    if final_production_tons > 0:
        cost_per_ton = total_monthly_cost / final_production_tons
    else:
        cost_per_ton = 0

    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    col_f1.metric("الإنتاج (طن)", "{:,.1f}".format(final_production_tons))
    col_f2.metric("تكلفة الطن", "{:,.0f}".format(cost_per_ton))
    col_f3.metric("المبيعات", "{:,.0f}".format(monthly_revenue))
    col_f4.metric("صافي الربح", "{:,.0f}".format(monthly_profit))

    st.markdown("---")
    chart_data = {
        "البند": [
            "المواد الخام",
            "الحبر والغراء",
            "الكهرباء والإهلاك",
            "الرواتب",
            "اللوجستيات",
            "إدارية وحكومية"
        ],
        "التكلفة": [
            total_raw_materials_cost,
            (ink_cost_monthly + solvent_cost_monthly + adhesive_cost_monthly),
            (total_monthly_power + total_monthly_depreciation),
            total_payroll_monthly,
            (total_logistics_cost + factory_maintenance),
            (hospitality_office + gov_fees)
        ]
    }
    df_chart = pd.DataFrame(chart_data)
    fig = px.pie(df_chart, values='التكلفة', names='البند', hole=0.4)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# TAB 7: مقارنة الروتو والفلكسو 
# ==========================================
with tab_compare:
    st.header("مقارنة التكلفة والربحية: فلكسو ضد روتوجرافيور")
    st.info("تشمل المحاكاة التجهيز (سلندرات/بليتات)، الهالك، والمستهلكات الدقيقة (أنيلوكس ودكتور بليد)!")

    col_c1, col_c2 = st.columns(2)

    with col_c1:
        st.subheader("1. إعدادات طلبية العميل")
        job_colors = st.number_input("عدد ألوان التصميم", min_value=1, max_value=10, value=8)
        avg_material_cost_per_ton = st.number_input("متوسط تكلفة مواد التغليف للطن (ريال)", value=9000)
        meters_per_ton = st.number_input("متوسط الأمتار الطولية في الطن الواحد (متر)", value=20000)

    with col_c2:
        st.subheader("2. مقارنة التجهيز والهالك")
        flexo_plate_cost_per_color = st.number_input("تكلفة البليت للون - فلكسو (ريال)", value=400)
        roto_cyl_cost_per_color = st.number_input("تكلفة السلندر للون - روتو (ريال)", value=1500)

        flexo_waste_kg = st.number_input("هالك التجهيز - فلكسو (كجم)", value=50)
        roto_waste_kg = st.number_input("هالك التجهيز - روتو (كجم)", value=250)

    st.markdown("---")
    st.subheader("3. المستهلكات الدقيقة (أنيلوكس، رول مطاطي، دكتور بليد)")
    
    col_cons1, col_cons2 = st.columns(2)
    with col_cons1:
        st.markdown("**مستهلكات الفلكسو (لكل لون)**")
        anilox_price = st.number_input("سعر الأنيلوكس (ريال)", value=15000)
        anilox_life = st.number_input("عمر الأنيلوكس (متر طولي)", value=200000000)
        
        flexo_blade_price = st.number_input("سعر متر الدكتور بليد (ريال)", value=9.0)
        flexo_blade_length = st.number_input("طول الدكتور بليد للشمبر (متر)", value=1.3)
        flexo_blade_life = st.number_input("عمر الدكتور بليد - فلكسو (متر طولي)", value=500000)
        st.caption("ملاحظة: الشمبر في الفلكسو يستهلك عدد (2) دكتور بليد للون.")

    with col_cons2:
        st.markdown("**مستهلكات الروتو (لكل لون)**")
        roto_roller_price = st.number_input("سعر الرول المطاطي / Impression (ريال)", value=1500)
        roto_roller_life = st.number_input("عمر الرول المطاطي (متر طولي)", value=15000000)
        
        roto_blade_price = st.number_input("سعر متر شفرة الروتو (ريال)", value=9.0)
        roto_blade_length = st.number_input("طول شفرة الروتو (متر)", value=1.3)
        roto_blade_life = st.number_input("عمر شفرة الروتو (متر طولي)", value=500000)
        st.caption("ملاحظة: وحدة الروتو تستهلك عدد (1) دكتور بليد للون.")

    flexo_setup_cost = job_colors * flexo_plate_cost_per_color
    roto_setup_cost = job_colors * roto_cyl_cost_per_color

    material_cost_per_kg = avg_material_cost_per_ton / 1000.0
    flexo_waste_cost = flexo_waste_kg * material_cost_per_kg
    roto_waste_cost = roto_waste_kg * material_cost_per_kg

    total_flexo_fixed_cost = flexo_setup_cost + flexo_waste_cost
    total_roto_fixed_cost = roto_setup_cost + roto_waste_cost

    flexo_anilox_cost_per_m = (anilox_price / anilox_life) * job_colors
    flexo_blade_cost_per_m = ((2 * flexo_blade_length * flexo_blade_price) / flexo_blade_life) * job_colors
    total_flexo_cons_per_m = flexo_anilox_cost_per_m + flexo_blade_cost_per_m

    roto_roller_cost_per_m = (roto_roller_price / roto_roller_life) * job_colors
    roto_blade_cost_per_m = ((1 * roto_blade_length * roto_blade_price) / roto_blade_life) * job_colors
    total_roto_cons_per_m = roto_roller_cost_per_m + roto_blade_cost_per_m

    st.markdown("---")
    st.subheader("📊 تحليل
