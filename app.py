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
# TAB 1: المواد الخام والتسعير (العقل المدبر)
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

    # 🌟 إنشاء القاموس المركزي للمواد (يحتوي الكثافة والسعر معاً)
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
# TAB 2: قسم الطباعة المترابط
# ==========================================
with tab_printing:
    st.header("قسم الطباعة (Printing Department)")
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        machine_speed = st.slider("سرعة ماكينة الطباعة (متر/دقيقة)", 100, 500, 350)
        web_width_mm = st.slider("عرض رول الطباعة (ملم)", 400, 1300, 1000)
        ink_coverage = st.number_input("تغطية الحبر (جرام/متر مربع - Ink GSM)", value=5.0)
        
        st.markdown("**مواصفات فيلم الطباعة (الطبقة الأولى - المطبوعة)**")
        # 🌟 الترابط الذكي: سحب المادة من القسم الأول
        base_material_name = st.selectbox("نوع مادة الطباعة", list(materials_db.keys()))
        base_thickness = st.number_input("سماكة فيلم الطباعة (ميكرون)", value=20)
        
        # استخراج الكثافة والسعر تلقائياً
        base_density = materials_db[base_material_name]["density"]
        base_price = materials_db[base_material_name]["price"]
        st.caption(f"تم الربط بنجاح 🔗 | الكثافة: **{base_density}** | السعر: **{base_price:,.0f} ريال/طن**")
        
    with col_p2:
        st.warning("⏱️ تأثير تغييرات الأعمال (Job Changeovers)")
        jobs_per_month = st.slider("عدد تغييرات الأعمال شهرياً", 1, 150, 60)
        changeover_time = 120 # دقيقة لكل تغيير
        total_lost_time = jobs_per_month * changeover_time
        
        printing_available_mins = 2 * 12 * 26 * 60 * 0.85 
        actual_printing_mins = printing_available_mins - total_lost_time
        
        st.write(f"إجمالي الدقائق المتاحة شهرياً: **{printing_available_mins:,.0f} دقيقة**")
        st.write(f"الوقت الضائع في التجهيز: **{total_lost_time:,.0f} دقيقة**")
        st.success(f"دقائق التشغيل الفعلي الصافي: **{actual_printing_mins:,.0f} دقيقة**")

    # الحسابات
    web_width_m = web_width_mm / 1000.0
    linear_meters_per_month = machine_speed * actual_printing_mins
    sq_meters_per_month = linear_meters_per_month * web_width_m

    # مخرجات الطباعة والتكاليف الدقيقة
    st.markdown("---")
    st.subheader("📊 مخرجات قسم الطباعة (Printing Outputs)")
    
    col_len1, col_len2 = st.columns(2)
    col_len1.info(f"📏 **إجمالي الأمتار الطولية المطبوعة:** {linear_meters_per_month:,.0f} متر طول")
    col_len2.info(f"📐 **إجمالي الأمتار المربعة المطبوعة:** {sq_meters_per_month:,.0f} متر مربع")
    
    ink_kg_per_month = (sq_meters_per_month * ink_coverage) / 1000.0
    solvent_kg_per_month = ink_kg_per_month * solvent_ratio
    ink_cost_monthly = ink_kg_per_month * ink_price
    solvent_cost_monthly = solvent_kg_per_month * solvent_price
    
    # 🌟 حساب التكلفة الدقيقة لفيلم الطباعة
    base_film_gsm = base_thickness * base_density
    base_film_tons_per_month = (sq_meters_per_month * base_film_gsm) / 1000000.0
    base_film_cost_monthly = base_film_tons_per_month * base_price
    
    printed_roll_gsm = base_film_gsm + ink_coverage
    printing_production_tons = (sq_meters_per_month * printed_roll_gsm) / 1000000.0

    col_res1, col_res2, col_res3, col_res4 = st.columns(4)
    col_res1.metric("كمية الحبر والسولفنت", f"{(ink_kg_per_month + solvent_kg_per_month):,.0f} كجم")
    col_res2.metric("تكلفة الحبر والسولفنت", f"{(ink_cost_monthly + solvent_cost_monthly):,.0f} ريال")
    col_res3.metric("وزن المادة الخام (للطباعة)", f"{base_film_tons_per_month:,.1f} طن")
    col_res4.metric("تكلفة المادة الخام (للطباعة)", f"{base_film_cost_monthly:,.0f} ريال")

# ==========================================
# TAB 3: قسم اللامنيشن والهيكلة الديناميكية
# ==========================================
with tab_lamination:
    st.header("قسم اللامنيشن وبناء الطبقات (Structure & Lamination)")
    
    col_l1, col_l2 = st.columns([1, 2])
    
    with col_l1:
        num_layers = st.selectbox("عدد طبقات المنتج النهائي (Layers)", [1, 2, 3, 4], format_func=lambda x: "1 (طباعة فقط - بدون لامنيشن)" if x == 1 else str(x))
        passes = max(0, num_layers - 1)
        
        if passes > 0:
            adhesive_gsm = st.number_input("وزن غراء اللامنيشن (g/m2) للتمريرة", value=1.8)
            total_adhesive_gsm = adhesive_gsm * passes
            st.info(f"إجمالي الغراء للمنتج: **{total_adhesive_gsm} g/m2** (عدد التمريرات: {passes})")
        else:
            adhesive_gsm = 0.0
            total_adhesive_gsm = 0.0
            st.success("🚫 المنتج سيذهب للتقطيع مباشرة (لا يوجد استهلاك غراء أو تشغيل لامنيشن).")

    with col_l2:
        st.subheader("بناء الهيكل الهندسي (Product Structure)")
        layers_gsm_list = []
        
        # 🌟 تكلفة المواد الإجمالية تبدأ من تكلفة طبقة الطباعة
        total_raw_materials_cost = base_film_cost_monthly 
        
        st.markdown(f"**الطبقة 1 (الرول المطبوع):** {base_material_name} ({base_thickness}μ) = **{printed_roll_gsm:.2f} g/m2**")
        layers_gsm_list.append(printed_roll_gsm)
        
        if num_layers > 1:
            for i in range(2, num_layers + 1):
                st.markdown(f"**الطبقة {i}:**")
                col_mat, col_thk = st.columns(2)
                # 🌟 الترابط الذكي مع القاموس المركزي للامنيشن أيضاً
                layer_mat_name = col_mat.selectbox(f"نوع المادة", list(materials_db.keys()), key=f"mat_{i}")
                layer_thk = col_thk.number_input(f"السماكة (ميكرون)", value=20, key=f"thk_{i}")
                
                layer_density = materials_db[layer_mat_name]["density"]
                layer_price = materials_db[layer_mat_name]["price"]
                
                layer_gsm = layer_thk * layer_density
                layers_gsm_list.append(layer_gsm)
                
                # حساب تكلفة هذه الطبقة بدقة
                layer_tons = (sq_meters_per_month * layer_gsm) / 1000000.0
                layer_cost = layer_tons * layer_price
                total_raw_materials_cost += layer_cost
                
                st.caption(f"وزن {layer_mat_name}: {layer_gsm:.2f} g/m2 | تكلفة الطبقة: {layer_cost:,.0f} ريال")

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

        if passes == 0:
            st.success("✅ المنتج عبارة عن طبقة واحدة مطبوعة ولا يحتاج إلى التشغيل على ماكينة اللامنيشن نهائياً.")
        elif utilization <= 100:
            st.success(f"✅ نسبة استهلاك الماكينة: **{utilization:.1f}%**")
        else:
            st.error(f"⚠️ تحذير اختناق (Bottleneck): نسبة استهلاك الماكينة **{utilization:.1f}%**!")

    total_substrate_gsm = sum(layers_gsm_list)
    final_product_gsm = total_substrate_gsm + total_adhesive_gsm
    
    weight_without_adhesive_tons = (sq_meters_per_month * total_substrate_gsm) / 1000000.0
    adhesive_consumed_kg = (sq_meters_per_month * total_adhesive_gsm) / 1000.0
    final_production_tons = (sq_meters_per_month * final_product_gsm) / 1000000.0

    st.markdown("---")
    st.subheader("📊 مخرجات قسم اللامنيشن والإنتاج النهائي (Final Outputs)")
    
    col_out1, col_out2, col_out3 = st.columns(3)
    col_out1.metric("إجمالي تكلفة المواد الخام المجمعة", f"{total_raw_materials_cost:,.0f} ريال")
    col_out2.metric("كمية الغراء المستهلكة", f"{adhesive_consumed_kg:,.0f} كجم")
    col_out3.metric("الوزن النهائي للبيع", f"{final_production_tons:,.1f} طن")

# ==========================================
# TAB 4: الماكينات والأصول 
# ==========================================
with tab_machines:
    st.header("إدارة الأصول واستهلاك الطاقة (Assets & Utilities Management)")
    
    col_elec1, col_elec2 = st.columns(2)
    electricity_rate = col_elec1.number_input("سعر الكيلوواط/ساعة (SAR/kWh)", value=0.18, format="%.3f")
    working_hours_per_month = col_elec2.number_input("ساعات تشغيل المصنع شهرياً (ورديتين * 12 * 26)", value=624)

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
    edited_machines = st.data_editor(default_machines, num_rows="dynamic", use_container_width=True)

    edited_machines["Monthly_Depreciation"] = edited_machines["Cost_SAR"] / (edited_machines["Life_Years"] * 12)
    edited_machines["Monthly_Power_Cost"] = edited_machines["Power_kW"] * working_hours_per_month * 0.85 * electricity_rate

    total_capex = edited_machines["Cost_SAR"].sum()
    total_monthly_depreciation = edited_machines["Monthly_Depreciation"].sum()
    total_monthly_power = edited_machines["Monthly_Power_Cost"].sum()

# ==========================================
# TAB 5: الخلاصة المالية (دقيقة 100%)
# ==========================================
with tab_finance:
    st.header("الخلاصة والنتائج (Financial Dashboard)")
    selling_price = st.slider("متوسط سعر بيع الطن للمنتج النهائي (ريال)", 10000, 25000, 14000, step=100)
    monthly_salaries = st.number_input("إجمالي الرواتب الشهرية والمصاريف الإدارية (SAR)", value=200000)
    
    adhesive_cost_monthly = adhesive_consumed_kg * 12 
    
    # 🌟 التكلفة الإجمالية الآن أصبحت دقيقة وتعتمد على خياراتك للمواد في كل طبقة!
    total_monthly_cost = total_raw_materials_cost + ink_cost_monthly + solvent_cost_monthly + adhesive_cost_monthly + total_monthly_power + total_monthly_depreciation + monthly_salaries
    
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
        "البند": ["تكلفة المواد الخام (دقيقة)", "الحبر والسولفنت", "غراء اللامنيشن", "الكهرباء", "الإهلاك للمعدات", "الرواتب والمصاريف"],
        "التكلفة": [total_raw_materials_cost, ink_cost_monthly + solvent_cost_monthly, adhesive_cost_monthly, total_monthly_power, total_monthly_depreciation, monthly_salaries]
    }
    df_chart = pd.DataFrame(chart_data)
    fig = px.pie(df_chart, values='التكلفة', names='البند', hole=0.4, title="التحليل الدقيق للتكاليف التشغيلية (OPEX + Overheads)")
    st.plotly_chart(fig, use_container_width=True)
