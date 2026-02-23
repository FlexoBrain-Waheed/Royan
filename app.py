import streamlit as st
import pandas as pd
import plotly.express as px

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Royan Flexo Project Dashboard", layout="wide", page_icon="📈")

# --- عنوان اللوحة ---
st.title("مجموعة رويان - دراسة الجدوى الذكية (تقنية الفلكسو)")
st.markdown("لوحة قيادة تفاعلية لتحليل التكاليف والعائد على الاستثمار لمنظومة الفلكسو واللامنيشن بدون مذيبات.")
st.markdown("---")

# --- 1. قراءة الأرقام الأساسية (مستمدة من ملفات الإكسيل) ---
# إجمالي الأصول الثابتة (CAPEX)
capex_items = {
    "CI Flexo": 8000000, "Solventless Lamination": 1200000, "PE Extruder": 5000000, 
    "Slitter Machine": 800000, "Bag Converting 1-5": 620000, "Lab Test Equipment": 100000, 
    "Building": 4000000, "Chiller": 400000, "Air Compressor": 200000
}
total_capex = sum(capex_items.values())

# --- 2. القائمة الجانبية (للتفاعل والمحاكاة أمام الإدارة) ---
st.sidebar.header("محاكي الاستثمار التشغيلي")
st.sidebar.info("غيّر الأرقام أدناه لرؤية تأثيرها المباشر على الأرباح وفترة الاسترداد.")

# استخدام سرعة الإكسترودر (500 كجم/ساعة) لحساب الإنتاج الشهري كقيمة افتراضية
# 500 * 24 ساعة * 26 يوم = 312 طن شهرياً
production_tons = st.sidebar.slider("الإنتاج والمبيعات الشهرية (طن)", min_value=100, max_value=500, value=312, step=10)
selling_price = st.sidebar.slider("متوسط سعر بيع الطن للمنتج النهائي (ريال)", min_value=10000, max_value=18000, value=12887, step=100)
pe_cost_per_ton = st.sidebar.number_input("تكلفة طن حبيبات البلاستيك (ريال)", value=5000)

# --- 3. الحسابات المالية (OPEX & ROI) ---
# التكاليف التشغيلية الشهرية التقريبية للطن (بناء على مدخلاتك)
ink_cost = 15 * 30  # افتراض 30 كيلو حبر للطن
solvent_cost = 7 * 35 # افتراض 35 كيلو سولفنت للطباعة
adhesive_cost = 12 * 25 # غراء السولفنتلس
plates_cost = 3000 / 50 # إهلاك البليتات موزع على الأطنان
power_cost = 0.18 * 400 # تكلفة تقريبية للكهرباء للطن
salaries = 200000 / production_tons # الرواتب موزعة على حجم الإنتاج

cost_per_ton = pe_cost_per_ton + ink_cost + solvent_cost + adhesive_cost + plates_cost + power_cost + salaries

monthly_revenue = production_tons * selling_price
monthly_cost = production_tons * cost_per_ton
monthly_profit = monthly_revenue - monthly_cost

# رأس المال العامل لـ 3 أشهر
working_capital = monthly_cost * 3 
total_investment = total_capex + working_capital

roi = (monthly_profit * 12) / total_investment * 100
payback_years = total_investment / (monthly_profit * 12) if monthly_profit > 0 else 0

# --- 4. عرض المؤشرات العلوية الرئيسية (KPIs) ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("إجمالي الاستثمار (CAPEX + OPEX)", f"{total_investment:,.0f} ريال")
col2.metric("صافي الربح الشهري المتوقع", f"{monthly_profit:,.0f} ريال")
col3.metric("العائد على الاستثمار (ROI)", f"{roi:.1f} %")
col4.metric("فترة الاسترداد", f"{payback_years:.2f} سنوات")

st.markdown("---")

# --- 5. الرسوم البيانية التفاعلية ---
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("توزيع الأصول الثابتة (CAPEX)")
    df_capex = pd.DataFrame(list(capex_items.items()), columns=['Equipment', 'Cost'])
    fig_capex = px.pie(df_capex, values='Cost', names='Equipment', hole=0.4, 
                       color_discrete_sequence=px.colors.sequential.YlOrBr)
    fig_capex.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_capex, use_container_width=True)

with col_chart2:
    st.subheader("تحليل تكلفة الطن (OPEX Breakdown)")
    # تجهيز بيانات التكلفة
    opex_data = {
        "المواد الخام (PE)": pe_cost_per_ton,
        "أحبار ومذيبات الفلكسو": ink_cost + solvent_cost,
        "غراء (Solventless)": adhesive_cost,
        "بليتات الفلكسو": plates_cost,
        "طاقة ورواتب": power_cost + salaries
    }
    df_opex = pd.DataFrame(list(opex_data.items()), columns=['Item', 'Cost'])
    fig_opex = px.bar(df_opex, x='Item', y='Cost', text='Cost', 
                      color='Item', color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_opex.update_layout(showlegend=False, xaxis_title="", yaxis_title="التكلفة (ريال / طن)")
    st.plotly_chart(fig_opex, use_container_width=True)

# --- 6. رسالة الختام ونقاط القوة ---
st.success("""
**لماذا تقنية الفلكسو هي الأنسب لمشروع رويان؟**
* **سرعة الإنجاز:** تجهيز بليتات الفلكسو أسرع وأرخص بكثير من حفر أسطوانات الروتوجرافيور.
* **توفير التكاليف:** تقنية الـ Solventless تلغي تكاليف مذيبات اللامنيشن وتخفض استهلاك الطاقة لعدم الحاجة لأفران تجفيف.
* **التكامل:** وجود الإكسترودر (PE) يضمن التحكم بجودة الفيلم وتوفير هوامش ربح إضافية بدلاً من الشراء من السوق المحلي.
""")
