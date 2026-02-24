import streamlit as st
import pandas as pd
import plotly.express as px

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Royan Flexo Project Dashboard", layout="wide", page_icon="📈")
st.title("مجموعة رويان - دراسة الجدوى الذكية (تقنية الفلكسو)")
st.markdown("---")

# --- 1. الأصول الثابتة (CAPEX) ---
capex_items = {
    "CI Flexo": 8000000, "Solventless Lamination": 1200000, "PE Extruder": 5000000, 
    "Slitter Machine": 800000, "Bag Converting 1-5": 620000, "Lab Test Equipment": 100000, 
    "Building": 4000000, "Chiller": 400000, "Air Compressor": 200000
}
total_capex = sum(capex_items.values())

# --- 2. محاكي مواصفات الطلبية (Job Profile) ---
st.sidebar.header("مواصفات التشغيل (للتأثير على الإنتاجية)")

# اختيار المادة وكثافتها
material = st.sidebar.selectbox("نوع المادة المطبوعة", ["PE (بولي إيثيلين)", "PET (بوليستر)", "BOPP"])
if material == "PE (بولي إيثيلين)":
    density = 0.92
elif material == "PET (بوليستر)":
    density = 1.40
else:
    density = 0.91

thickness = st.sidebar.slider("السماكة (ميكرون)", 10, 150, 70, step=1)
web_width_mm = st.sidebar.slider("عرض رول الطباعة (ملم)", 400, 1300, 1200, step=50)
machine_speed = st.sidebar.slider("سرعة الماكينة (متر/دقيقة)", 100, 500, 400, step=10)

st.sidebar.markdown("---")
st.sidebar.header("الأسعار والتكاليف")
selling_price = st.sidebar.slider("متوسط سعر بيع الطن (ريال)", 10000, 18000, 12887, step=100)
ink_coverage = st.sidebar.number_input("تغطية الحبر (جرام/متر مربع)", value=5.0)

# --- 3. الحسابات الفيزيائية والتشغيلية ---
web_width_m = web_width_mm / 1000.0
gsm = thickness * density  # وزن المتر المربع جرام

# حساب المساحة المطبوعة شهرياً (افتراض 2 وردية * 12 ساعة * 26 يوم * 85% كفاءة)
# 24 ساعة * 60 دقيقة * 26 يوم * 0.85 = 31,824 دقيقة تشغيل فعلية شهرياً
operating_minutes_per_month = 31824
linear_meters_per_month = machine_speed * operating_minutes_per_month
sq_meters_per_month = linear_meters_per_month * web_width_m

# الإنتاج الشهري بالطن
production_tons = (sq_meters_per_month * gsm) / 1000000.0

# --- 4. حساب استهلاك المواد والتكاليف ---
ink_kg_per_month = (sq_meters_per_month * ink_coverage) / 1000.0
ink_cost_monthly = ink_kg_per_month * 15  # 15 ريال لكيلو الحبر
solvent_cost_monthly = (ink_kg_per_month * 1.2) * 7  # نسبة السولفنت للحبر 1.2 * سعر 7 ريال

pe_cost_monthly = production_tons * 5000  # تكلفة الراتنج
adhesive_cost_monthly = production_tons * (12 * 25) # غراء افتراضي للطن
plates_cost_monthly = production_tons * (3000 / 50)
power_cost_monthly = production_tons * (0.18 * 400)
salaries_monthly = 200000

total_monthly_cost = pe_cost_monthly + ink_cost_monthly + solvent_cost_monthly + adhesive_cost_monthly + plates_cost_monthly + power_cost_monthly + salaries_monthly
cost_per_ton = total_monthly_cost / production_tons

monthly_revenue = production_tons * selling_price
monthly_profit = monthly_revenue - total_monthly_cost

# رأس المال العامل لـ 3 أشهر
total_investment = total_capex + (total_monthly_cost * 3)
roi = (monthly_profit * 12) / total_investment * 100
payback_years = total_investment / (monthly_profit * 12) if monthly_profit > 0 else 0

# --- 5. عرض المؤشرات العلوية ---
st.info(f"💡 **طاقة الإنتاج المحسوبة بناءً على المواصفات:** {production_tons:,.1f} طن/شهر | **مساحة الطباعة:** {sq_meters_per_month:,.0f} متر مربع/شهر")

col1, col2, col3, col4 = st.columns(4)
col1.metric("إجمالي الاستثمار المطلوب", f"{total_investment:,.0f} ريال")
col2.metric("التكلفة الفعلية للطن", f"{cost_per_ton:,.0f} ريال")
col3.metric("صافي الربح الشهري", f"{monthly_profit:,.0f} ريال")
col4.metric("العائد على الاستثمار (ROI)", f"{roi:.1f} %")

st.markdown("---")

# --- 6. الرسوم البيانية ---
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("توزيع التكاليف التشغيلية الشهرية (OPEX)")
    opex_data = {
        "المواد الخام (PE)": pe_cost_monthly,
        "أحبار ومذيبات": ink_cost_monthly + solvent_cost_monthly,
        "غراء السولفنتلس": adhesive_cost_monthly,
        "بليتات الفلكسو": plates_cost_monthly,
        "طاقة ورواتب": power_cost_monthly + salaries_monthly
    }
    df_opex = pd.DataFrame(list(opex_data.items()), columns=['Item', 'Cost'])
    fig_opex = px.pie(df_opex, values='Cost', names='Item', hole=0.4, color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_opex, use_container_width=True)

with col_chart2:
    st.subheader("تحليل تكلفة استهلاك الحبر")
    st.write(f"**استهلاك الحبر الشهري:** {ink_kg_per_month:,.0f} كجم")
    st.write(f"**تكلفة الحبر الشهرية:** {ink_cost_monthly:,.0f} ريال")
    st.write(f"**تكلفة المذيبات الشهرية:** {solvent_cost_monthly:,.0f} ريال")
    st.success("زيادة التغطية (g/m2) أو عرض الرول سيرفع استهلاك الحبر مباشرة هنا.")
