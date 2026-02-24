import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Royan Flexo Smart ERP", layout="wide", page_icon="⚙️")
st.title("مجموعة رويان - نظام المحاكاة الذكي للإنتاج والتكاليف")
st.markdown("---")

# --- تقسيم الشاشة إلى 4 أقسام (Tabs) ---
tab_materials, tab_printing, tab_lamination, tab_finance = st.tabs([
    "📦 1. المواد الخام (Materials)", 
    "🖨️ 2. قسم الطباعة (Printing)", 
    "🥪 3. قسم اللامنيشن (Lamination)", 
    "📊 4. الخلاصة المالية (Financials)"
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
        
        st.markdown("**مواصفات فيلم الطباعة (الطبقة المطبوعة فقط)**")
        base_thickness = st.number_input("سماكة فيلم الطباعة (ميكرون)", value=20)
        base_density = st.number_input("كثافة فيلم الطباعة", value=0.91)
        
    with col_p2:
        st.warning("⏱️ تأثير تغييرات الأعمال (Job Changeovers)")
        jobs_per_month = st.slider("عدد تغييرات الأعمال شهرياً", 1, 150, 60)
        changeover_time = 120 # دقيقة لكل تغيير
        total_lost_time = jobs_per_month * changeover_time
        
        # حساب الوقت الفعلي
        total_available_mins = 2 * 12 * 26 * 60 * 0.85 # (وردتين * 12 ساعة * 26 يوم * 60 دقيقة * 85% كفاءة)
        actual_printing_mins = total_available_mins - total_lost_time
        
        st.write(f"إجمالي الدقائق المتاحة شهرياً: **{total_available_mins:,.0f} دقيقة**")
        st.write(f"الوقت الضائع في التجهيز: **{total_lost_time:,.0f} دقيقة**")
        st.success(f"دقائق التشغيل الفعلي الصافي: **{actual_printing_mins:,.0f} دقيقة**")

    # حسابات الإنتاج الطولي والمساحي
    web_width_m = web_width_mm / 1000.0
    linear_meters_per_month = machine_speed * actual_printing_mins
    sq_meters_per_month = linear_meters_per_month * web_width_m

    # --- مخرجات قسم الطباعة (حسب طلبك) ---
    st.markdown("---")
    st.subheader("📊 مخرجات قسم الطباعة (Printing Outputs)")
    
    ink_kg_per_month = (sq_meters_per_month * ink_coverage) / 1000.0
    solvent_kg_per_month = ink_kg_per_month * solvent_ratio
    
    ink_cost_monthly = ink_kg_per_month * ink_price
    solvent_cost_monthly = solvent_kg_per_month * solvent_price
    
    # حساب وزن الرول المطبوع فقط (الفيلم الأساسي + الحبر)
    base_film_gsm = base_thickness * base_density
    printed_roll_gsm = base_film_gsm + ink_coverage
    printing_production_tons = (sq_meters_per_month * printed_roll_gsm) / 1000000.0

    col_res1, col_res2, col_res3, col_res4, col_res5 = st.columns(5)
    col_res1.metric("كمية الحبر المطلوبة", f"{ink_kg_per_month:,.0f} كجم")
    col_res2.metric("كمية السولفنت", f"{solvent_kg_per_month:,.0f} كجم")
    col_res3.metric("قيمة الحبر", f"{ink_cost_monthly:,.0f} ريال")
    col_res4.metric("قيمة السولفنت", f"{solvent_cost_monthly:,.0f} ريال")
    col_res5.metric("الوزن الإجمالي للطباعة", f"{printing_production_tons:,.1f} طن")

# ==========================================
# TAB 3: قسم اللامنيشن والهيكلة
# ==========================================
with tab_lamination:
    st.header("قسم اللامنيشن وبناء الطبقات (Lamination & Structure)")
    col_l1, col_l2 = st.columns(2)
    
    with col_l1:
        num_layers = st.selectbox("عدد طبقات المنتج النهائي (Layers)", [2, 3, 4])
        passes = num_layers - 1 # عدد التمريرات في الماكينة
        adhesive_gsm = st.number_input("وزن غراء اللامنيشن للمتر المربع (Adhesive GSM) للتمريرة الواحدة", value=1.8)
        
        total_adhesive_gsm = adhesive_gsm * passes
        st.info(f"🔄 المادة ستدخل ماكينة اللامنيشن **{passes} مرات**. إجمالي وزن الغراء المضاف للمنتج: **{total_adhesive_gsm} g/m2**")

    with col_l2:
        st.write("متوسط سماكة المادة الخام الإجمالية (بما فيها فيلم الطباعة والطبقات الأخرى)")
        avg_thickness = st.slider("السماكة الإجمالية للفيلم (ميكرون)", 20, 200, 70)
        avg_density = st.slider("متوسط الكثافة للفيلم المدمج", 0.90, 1.40, 0.95)
        
        film_gsm = avg_thickness * avg_density
        final_gsm = film_gsm + ink_coverage + total_adhesive_gsm
        
        st.success(f"⚖️ الوزن النهائي للمتر المربع المطبوع والمبطن: **{final_gsm:.1f} g/m2**")

    # حساب الإنتاج النهائي بالطن بعد اللامنيشن
    final_production_tons = (sq_meters_per_month * final_gsm) / 1000000.0

# ==========================================
# TAB 4: الخلاصة المالية
# ==========================================
with tab_finance:
    st.header("الخلاصة والنتائج (Financial Dashboard)")
    selling_price = st.slider("متوسط سعر بيع الطن للمنتج النهائي (ريال)", 10000, 25000, 14000, step=100)
    
    # التكاليف الشهرية التقريبية
    adhesive_cost_monthly = ((sq_meters_per_month * total_adhesive_gsm) / 1000.0) * 12 # افترضنا سعر غراء السولفنتلس بـ 12
    raw_material_avg_cost = final_production_tons * 6000 # متوسط تكلفة افتراضي للطن
    salaries_and_power = 250000
    
    total_monthly_cost = raw_material_avg_cost + ink_cost_monthly + solvent_cost_monthly + adhesive_cost_monthly + salaries_and_power
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
    # رسم بياني لتوضيح تأثير الطبقات وتغيير الأعمال
    chart_data = {
        "البند": ["تكلفة المواد الخام", "الحبر", "السولفنت", "غراء اللامنيشن", "مصاريف تشغيلية"],
        "التكلفة": [raw_material_avg_cost, ink_cost_monthly, solvent_cost_monthly, adhesive_cost_monthly, salaries_and_power]
    }
    df_chart = pd.DataFrame(chart_data)
    fig = px.pie(df_chart, values='التكلفة', names='البند', hole=0.4, title="تحليل التكاليف التشغيلية")
    st.plotly_chart(fig, use_container_width=True)
