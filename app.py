import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Royan Flexo Smart ERP", layout="wide", page_icon="⚙️")
st.title("مجموعة رويان - نظام المحاكاة الذكي للإنتاج والتكاليف")
st.markdown("---")

# --- تقسيم الشاشة إلى 6 أقسام (Tabs) ---
tab_materials, tab_printing, tab_lamination, tab_machines, tab_hr_admin, tab_finance = st.tabs([
    "📦 1. المواد الخام (Materials)", 
    "🖨️ 2. قسم الطباعة (Printing)", 
    "🥪 3. قسم اللامنيشن (Lamination)", 
    "🏭 4. الماكينات والأصول (Machinery)",
    "👥 5. الموارد البشرية والإدارة (HR & Admin)",
    "📊 6. الخلاصة المالية (Financials)"
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

    materials_db = {
        "Transparent BOPP": {"density": bopp_t_density, "price": bopp_t_price},
        "White BOPP": {"density": bopp_w_density, "price": bopp_w_price},
        "Metallized BOPP": {"density": bopp_m_density, "price": bopp_m_price},
        "Polyester PET": {"density": pet_density, "price": pet_price},
        "PE (Polyethylene)": {"density": pe_density, "price": pe_price}
    }

    st.markdown("---")
    st.subheader("إعدادات الأحبار والمذيبات (Inks & Solvents)")
    col_m1, col_m2, col_m3 = st.columns(3)
    ink_price = col_m1.number_input("سعر كيلو الحبر (SAR/Kg)", value=15.0)
    solvent_price = col_m2.number_input("سعر كيلو السولفنت (SAR/Kg)", value=7.0)
    solvent_ratio = col_m3.number_input("نسبة السولفنت للحبر (مثلاً 1.2)", value=1.2)

# ==========================================
# TAB 2: قسم الطباعة
# ==========================================
with tab_printing:
    st.header("قسم الطباعة (Printing Department)")
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        machine_speed = st.slider("سرعة ماكينة الطباعة (متر/دقيقة)", 100, 500, 350)
        web_width_mm = st.slider("عرض رول الطباعة (ملم)", 400, 1300, 1000)
        ink_coverage = st.number_input("تغطية الحبر (جرام/متر مربع - Ink GSM)", value=5.0)
        
        st.markdown("**مواصفات فيلم الطباعة (الطبقة الأولى)**")
        base_material_name = st.selectbox("نوع مادة الطباعة", list(materials_db.keys()))
        base_thickness = st.number_input("سماكة فيلم الطباعة (ميكرون)", value=20)
        
        base_density = materials_db[base_material_name]["density"]
        base_price = materials_db[base_material_name]["price"]
        st.caption(f"الكثافة: **{base_density}** | السعر: **{base_price:,.0f} ريال/طن**")
        
    with col_p2:
        st.warning("⏱️ تأثير تغييرات الأعمال (Job Changeovers)")
        jobs_per_month = st.slider("عدد تغييرات الأعمال شهرياً", 1, 150, 60)
        changeover_time = 120 
        total_lost_time = jobs_per_month * changeover_time
        
        printing_available_mins = 2 * 12 * 26 * 60 * 0.85 
        actual_printing_mins = printing_available_mins - total_lost_time
        
        st.success(f"دقائق التشغيل الفعلي الصافي: **{actual_printing_mins:,.0f} دقيقة**")

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

# ==========================================
# TAB 3: قسم اللامنيشن 
# ==========================================
with tab_lamination:
    st.header("قسم اللامنيشن وبناء الطبقات (Structure & Lamination)")
    col_l1, col_l2 = st.columns([1, 2])
    
    with col_l1:
        num_layers = st.selectbox("عدد طبقات المنتج النهائي (Layers)", [1, 2, 3, 4], format_func=lambda x: "1 (بدون لامنيشن)" if x == 1 else str(x))
        passes = max(0, num_layers - 1)
        
        if passes > 0:
            adhesive_gsm = st.number_input("وزن غراء اللامنيشن (g/m2) للتمريرة", value=1.8)
            total_adhesive_gsm = adhesive_gsm * passes
        else:
            total_adhesive_gsm = 0.0

    with col_l2:
        layers_gsm_list = [printed_roll_gsm]
        total_raw_materials_cost = base_film_cost_monthly 
        
        if num_layers > 1:
            for i in range(2, num_layers + 1):
                col_mat, col_thk = st.columns(2)
                layer_mat_name = col_mat.selectbox(f"نوع مادة الطبقة {i}", list(materials_db.keys()), key=f"mat_{i}")
                layer_thk = col_thk.number_input(f"السماكة (ميكرون)", value=20, key=f"thk_{i}")
                
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

# ==========================================
# TAB 4: الماكينات والأصول 
# ==========================================
with tab_machines:
    st.header("إدارة الأصول واستهلاك الطاقة (Assets & Utilities)")
    col_elec1, col_elec2 = st.columns(2)
    electricity_rate = col_elec1.number_input("سعر الكيلوواط/ساعة (SAR/kWh)", value=0.18)
    working_hours_per_month = col_elec2.number_input("ساعات التشغيل شهرياً", value=624)

    default_machines = pd.DataFrame([
        {"Machine": "طباعة فلكسو (CI Flexo)", "Cost_SAR": 8000000, "Life_Years": 15, "Power_kW": 150},
        {"Machine": "لامنيشن (Solventless)", "Cost_SAR": 1200000, "Life_Years": 15, "Power_kW": 125},
        {"Machine": "إكسترودر (PE Extruder)", "Cost_SAR": 5000000, "Life_Years": 15, "Power_kW": 250},
        {"Machine": "قطاعة (Slitter)", "Cost_SAR": 800000, "Life_Years": 15, "Power_kW": 40},
        {"Machine": "تقطيع الأكياس (1-5)", "Cost_SAR": 620000, "Life_Years": 10, "Power_kW": 50},
        {"Machine": "مبرد وكمبروسر", "Cost_SAR": 600000, "Life_Years": 15, "Power_kW": 90},
        {"Machine": "تجهيزات المبنى", "Cost_SAR": 4000000, "Life_Years": 25, "Power_kW": 0},
    ])

    edited_machines = st.data_editor(default_machines, num_rows="dynamic", use_container_width=True)
    edited_machines["Monthly_Depreciation"] = edited_machines["Cost_SAR"] / (edited_machines["Life_Years"] * 12)
    edited_machines["Monthly_Power"] = edited_machines["Power_kW"] * working_hours_per_month * 0.85 * electricity_rate

    total_capex = edited_machines["Cost_SAR"].sum()
    total_monthly_depreciation = edited_machines["Monthly_Depreciation"].sum()
    total_monthly_power = edited_machines["Monthly_Power"].sum()

# ==========================================
# TAB 5: الموارد البشرية والمصاريف الإدارية (القسم الجديد المذهل)
# ==========================================
with tab_hr_admin:
    st.header("إدارة الموارد البشرية والمصاريف الإدارية واللوجستية (HR, Admin & Logistics)")
    
    st.subheader("👥 1. القوى العاملة والرواتب (Manpower & Payroll)")
    st.info("قم بتعديل العدد والراتب الأساسي. النظام سيحسب تلقائياً البدلات والتأمينات ورسوم الإقامات كنسبة إضافية.")
    
    default_hr = pd.DataFrame([
        {"Job Title": "مدير المصنع (Plant Manager)", "Count": 1, "Basic_Salary": 15000},
        {"Job Title": "مهندس إنتاج (Production Engineer)", "Count": 2, "Basic_Salary": 8000},
        {"Job Title": "فني طباعة فلكسو (Flexo Operator)", "Count": 2, "Basic_Salary": 5000},
        {"Job Title": "فني لامنيشن (Lam Operator)", "Count": 2, "Basic_Salary": 4000},
        {"Job Title": "فني تقطيع وأكياس (Slitter/Bags)", "Count": 4, "Basic_Salary": 3500},
        {"Job Title": "مراقب جودة (QC Inspector)", "Count": 2, "Basic_Salary": 4000},
        {"Job Title": "فني صيانة (Maintenance Tech)", "Count": 2, "Basic_Salary": 4500},
        {"Job Title": "عمال تحميل وتعبئة (Helpers)", "Count": 8, "Basic_Salary": 1800},
        {"Job Title": "محاسب / إداري (Accountant/Admin)", "Count": 2, "Basic_Salary": 4000},
        {"Job Title": "مندوب مبيعات (Sales Rep)", "Count": 3, "Basic_Salary": 4500},
        {"Job Title": "سائق توزيع (Driver)", "Count": 3, "Basic_Salary": 2500},
    ])
    
    edited_hr = st.data_editor(default_hr, num_rows="dynamic", use_container_width=True)
    
    col_hr1, col_hr2 = st.columns(2)
    allowances_percent = col_hr1.slider("نسبة البدلات (سكن ومواصلات) من الراتب الأساسي %", 10, 50, 25)
    iqama_insurance_per_employee = col_hr2.number_input("متوسط تكلفة (التأمين الطبي/الجوازات/تأمينات) للموظف شهرياً", value=600)
    
    # حسابات الموارد البشرية
    total_headcount = edited_hr["Count"].sum()
    edited_hr["Total_Basic"] = edited_hr["Count"] * edited_hr["Basic_Salary"]
    total_basic_salaries = edited_hr["Total_Basic"].sum()
    
    total_allowances = total_basic_salaries * (allowances_percent / 100.0)
    total_iqama_insurance = total_headcount * iqama_insurance_per_employee
    
    total_payroll_monthly = total_basic_salaries + total_allowances + total_iqama_insurance

    st.markdown("---")
    st.subheader("🚚 2. سيارات التوزيع واللوجستيات (Distribution Logistics)")
    col_log1, col_log2, col_log3 = st.columns(3)
    trucks_count = col_log1.number_input("عدد سيارات التوزيع (Trucks)", value=3)
    fuel_per_truck = col_log2.number_input("مصروف البنزين/الديزل للسيارة شهرياً (SAR)", value=1500)
    maintenance_per_truck = col_log3.number_input("صيانة السيارة شهرياً (غيار زيت/كفرات)", value=500)
    
    total_logistics_cost = trucks_count * (fuel_per_truck + maintenance_per_truck)

    st.markdown("---")
    st.subheader("🏢 3. المصاريف الإدارية والتشغيلية (Admin & Operations expenses)")
    col_adm1, col_adm2, col_adm3 = st.columns(3)
    factory_maintenance = col_adm1.number_input("ميزانية صيانة المصنع وقطع الغيار شهرياً", value=15000)
    hospitality_office = col_adm2.number_input("ضيافة، بوفيه، أدوات مكتبية واتصالات", value=5000)
    gov_fees = col_adm3.number_input("رسوم حكومية (زكاة، رخص، دفاع مدني) موزعة شهرياً", value=4000)
    
    total_admin_ops_cost = factory_maintenance + hospitality_office + gov_fees
    
    # إجمالي مصاريف هذا القسم
    grand_total_hr_admin = total_payroll_monthly + total_logistics_cost + total_admin_ops_cost

    st.markdown("---")
    col_res1, col_res2, col_res3, col_res4 = st.columns(4)
    col_res1.metric("إجمالي عدد الموظفين", f"{total_headcount} موظف")
    col_res2.metric("إجمالي الرواتب (شامل البدلات والتأمين)", f"{total_payroll_monthly:,.0f} ريال")
    col_res3.metric("إجمالي اللوجستيات والمصاريف الإدارية", f"{(total_logistics_cost + total_admin_ops_cost):,.0f} ريال")
    col_res4.metric("💰 الإجمالي الشهري للقسم", f"{grand_total_hr_admin:,.0f} ريال")

# ==========================================
# TAB 6: الخلاصة المالية
# ==========================================
with tab_finance:
    st.header("الخلاصة والنتائج (Financial Dashboard)")
    selling_price = st.slider("متوسط سعر بيع الطن للمنتج النهائي (ريال)", 10000, 25000, 14000, step=100)
    
    adhesive_cost_monthly = adhesive_consumed_kg * 12 
    
    # 🌟 التكلفة الإجمالية الآن تقرأ من كل الأقسام (بما فيها قسم الرواتب والإدارة الجديد!)
    total_monthly_cost = (
        total_raw_materials_cost + 
        ink_cost_monthly + 
        solvent_cost_monthly + 
        adhesive_cost_monthly + 
        total_monthly_power + 
        total_monthly_depreciation + 
        grand_total_hr_admin # <--- الإضافة الجديدة هنا
    )
    
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
    # تم تفصيل الرسم البياني ليعكس جميع البنود الجديدة باحترافية
    chart_data = {
        "البند": [
            "المواد الخام الأساسية", 
            "الحبر والسولفنت الغراء", 
            "الكهرباء وإهلاك المعدات", 
            "الرواتب والقوى العاملة", 
            "صيانة المصنع والسيارات (لوجستيات)", 
            "رسوم حكومية وضيافة"
        ],
        "التكلفة": [
            total_raw_materials_cost, 
            (ink_cost_monthly + solvent_cost_monthly + adhesive_cost_monthly), 
            (total_monthly_power + total_monthly_depreciation), 
            total_payroll_monthly, 
            (factory_maintenance + total_logistics_cost), 
            (hospitality_office + gov_fees)
        ]
    }
    df_chart = pd.DataFrame(chart_data)
    fig = px.pie(df_chart, values='التكلفة', names='البند', hole=0.4, title="التحليل الشامل والدقيق لهيكل التكاليف (Total Cost Breakdown)")
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)
