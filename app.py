import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def fmt(num):
    return "{:,.0f}".format(num)

def fmt1(num):
    return "{:,.1f}".format(num)

st.set_page_config(layout="wide", page_title="Royan ERP")

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
    st.header("اعدادات المواد الخام")
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
    st.subheader("الاحبار والمذيبات")
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
    cr1.metric("امتار طولية", fmt(linear_meters_per_month))
    cr2.metric("امتار مربعة", fmt(sq_meters_per_month))
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
                l_gsm = l_thk * l_den
                layers_gsm_list.append(l_gsm)
                
                l_tons = (sq_meters_per_month * l_gsm) / 1000000.0
                total_raw_cost += (l_tons * l_price)

    final_product_gsm = sum(layers_gsm_list) + total_adhesive_gsm
    adhesive_kg = (sq_meters_per_month * total_adhesive_gsm) / 1000.0
    final_tons = (sq_meters_per_month * final_product_gsm) / 1000000.0

    st.markdown("---")
    cc1, cc2 = st.columns(2)
    with cc1:
        lam_speed = st.slider("سرعة اللامنيشن", 100, 500, 350)
        lam_max_m = lam_speed * (2 * 12 * 26 * 60 * 0.85)

    with cc2:
        req_lam_m = linear_meters_per_month * passes
        if lam_max_m > 0:
            utilization = (req_lam_m / lam_max_m) * 100 
        else:
            utilization = 0
        st.write("استهلاك الماكينة: " + fmt1(utilization) + " %")

# ==========================================
# TAB 4: Machinery
# ==========================================
with tab_mac:
    st.header("ادارة الاصول")
    ce1, ce2 = st.columns(2)
    elec_rate = ce1.number_input("سعر الكيلوواط", value=0.18)
    work_hrs = ce2.number_input("ساعات العمل", value=624)

    mac_data = [
        {"Machine": "فلكسو", "Cost": 8000000, "Years": 15, "kW": 150},
        {"Machine": "لامنيشن", "Cost": 1200000, "Years": 15, "kW": 125},
        {"Machine": "اكسترودر", "Cost": 5000000, "Years": 15, "kW": 250},
        {"Machine": "قطاعة", "Cost": 800000, "Years": 15, "kW": 40},
        {"Machine": "اكياس", "Cost": 620000, "Years": 10, "kW": 50},
        {"Machine": "مبنى", "Cost": 4000000, "Years": 25, "kW": 0},
    ]

    df_mac = st.data_editor(pd.DataFrame(mac_data), use_container_width=True)
    df_mac["Deprec"] = df_mac["Cost"] / (df_mac["Years"] * 12)
    df_mac["Power"] = df_mac["kW"] * work_hrs * 0.85 * elec_rate

    tot_deprec = df_mac["Deprec"].sum()
    tot_power = df_mac["Power"].sum()

# ==========================================
# TAB 5: HR
# ==========================================
with tab_hr:
    st.header("الموارد البشرية")
    
    hr_data = [
        {"Job": "مدير", "Count": 1, "Salary": 15000},
        {"Job": "مهندس", "Count": 2, "Salary": 8000},
        {"Job": "فني", "Count": 8, "Salary": 4000},
        {"Job": "عامل", "Count": 8, "Salary": 1800},
        {"Job": "مبيعات", "Count": 3, "Salary": 4500},
        {"Job": "سائق", "Count": 3, "Salary": 2500},
    ]
    
    df_hr = st.data_editor(pd.DataFrame(hr_data), use_container_width=True)
    allowance = st.slider("نسبة البدلات", 10, 50, 25)
    iqama = st.number_input("رسوم اقامات", value=600)
    
    tot_basic = (df_hr["Count"] * df_hr["Salary"]).sum()
    tot_hr_cost = tot_basic + (tot_basic * allowance / 100) + (df_hr["Count"].sum() * iqama)

    trucks = st.number_input("سيارات", value=3)
    truck_cost = trucks * 2000 
    admin_cost = st.number_input("مصاريف ادارية", value=24000)
    
    grand_hr_admin = tot_hr_cost + truck_cost + admin_cost

# ==========================================
# TAB 6: Finance
# ==========================================
with tab_fin:
    st.header("الخلاصة المالية")
    selling_price = st.slider("سعر البيع", 10000, 25000, 14000)
    
    adhesive_cost = adhesive_kg * 12 
    
    total_cost = (
        total_raw_cost + ink_cost_monthly + solvent_cost_monthly + 
        adhesive_cost + tot_power + tot_deprec + grand_hr_admin
    )
    
    revenue = final_tons * selling_price
    profit = revenue - total_cost
    
    if final_tons > 0:
        cpt = total_cost / final_tons 
    else:
        cpt = 0

    cf1, cf2, cf3, cf4 = st.columns(4)
    cf1.metric("الانتاج", fmt1(final_tons))
    cf2.metric("تكلفة الطن", fmt(cpt))
    cf3.metric("مبيعات", fmt(revenue))
    cf4.metric("الربح", fmt(profit))

    chart_data = {
        "Item": ["مواد خام", "حبر وغراء", "طاقة واهلاك", "رواتب", "ادارة"],
        "Cost": [
            total_raw_cost, 
            (ink_cost_monthly + solvent_cost_monthly + adhesive_cost), 
            (tot_power + tot_deprec), 
            tot_hr_cost, 
            (truck_cost + admin_cost)
        ]
    }
    fig = px.pie(pd.DataFrame(chart_data), values='Cost', names='Item', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# TAB 7: Compare Roto vs Flexo
# ==========================================
with tab_comp:
    st.header("مقارنة فلكسو وروتو")

    st.subheader("اعدادات الطلبية")
    cc1, cc2 = st.columns(2)
    with cc1:
        job_colors = st.number_input("عدد الالوان", value=8)
        avg_mat_cost = st.number_input("تكلفة مواد الطن", value=9000)
    with cc2:
        meters_per_ton = st.number_input("امتار الطن", value=20000)

    st.markdown("---")
    st.subheader("التجهيز والهالك")
    cw1, cw2 = st.columns(2)
    with cw1:
        f_plate = st.number_input("سعر بليت فلكسو", value=400)
        f_waste = st.number_input("هالك فلكسو (كجم)", value=50)
    with cw2:
        r_cyl = st.number_input("سعر سلندر روتو", value=1500)
        r_waste = st.number_input("هالك روتو (كجم)", value=250)

    st.markdown("---")
    st.subheader("المستهلكات الدقيقة")
    c_cons1, c_cons2 = st.columns(2)
    with c_cons1:
        anilox_p = st.number_input("سعر انيلوكس", value=15000)
        anilox_l = st.number_input("عمر انيلوكس", value=200000000)
        fb_p = st.number_input("سعر بليد فلكسو", value=9.0)
        fb_len = st.number_input("طول بليد فلكسو", value=1.3)
        fb_life = st.number_input("عمر بليد فلكسو", value=500000)
    with c_cons2:
        r_roll_p = st.number_input("سعر رول روتو", value=1500)
        r_roll_l = st.number_input("عمر رول روتو", value=15000000)
        rb_p = st.number_input("سعر بليد روتو", value=9.0)
        rb_len = st.number_input("طول بليد روتو", value=1.3)
        rb_life = st.number_input("عمر بليد روتو", value=500000)

    st.markdown("---")
    st.subheader("الماكينة والطاقة")
    
    c_mac1, c_mac2 = st.columns(2)
    with c_mac1:
        f_mac_price = st.number_input("سعر ماكينة فلكسو", value=8000000)
        f_kw = st.number_input("طاقة فلكسو (kW)", value=150)
    with c_mac2:
        r_mac_price = st.number_input("سعر ماكينة روتو", value=10000000)
        r_boiler_price = st.number_input("سعر غلاية روتو", value=1500000)
        r_kw = st.number_input("طاقة روتو (kW)", value=350)

    c_gen1, c_gen2, c_gen3 = st.columns(3)
    mac_life_years = c_gen1.number_input("عمر الماكينات", value=15)
    work_hrs_month = c_gen2.number_input("ساعات المصنع", value=624)
    avg_prod_month = c_gen3.number_input("متوسط الانتاج الشهري", value=300)

    f_setup = job_colors * f_plate
    r_setup = job_colors * r_cyl
    mat_kg_cost = avg_mat_cost / 1000.0
    f_waste_cost = f_waste * mat_kg_cost
    r_waste_cost = r_waste * mat_kg_cost
    tot_f_fixed = f_setup + f_waste_cost
    tot_r_fixed = r_setup + r_waste_cost

    f_ani_m = (anilox_p / anilox_l) * job_colors
    f_bld_m = ((2 * fb_len * fb_p) / fb_life) * job_colors
    tot_f_cons = f_ani_m + f_bld_m

    r_rol_m = (r_roll_p / r_roll_l) * job_colors
    r_bld_m = ((1 * rb_len * rb_p) / rb_life) * job_colors
    tot_r_cons = r_rol_m + r_bld_m

    f_dep_m = f_mac_price / (mac_life_years * 12)
    f_pow_m = f_kw * work_hrs_month * 0.18
    f_mac_per_ton = (f_dep_m + f_pow_m) / avg_prod_month

    r_total_inv = r_mac_price + r_boiler_price
    r_dep_m = r_total_inv / (mac_life_years * 12)
    r_pow_m = r_kw * work_hrs_month * 0.18
    r_mac_per_ton = (r_dep_m + r_pow_m) / avg_prod_month

    st.markdown("---")
    st.subheader("الرسم البياني")

    job_sizes = list(range(1, 51))
    f_cost_list = []
    r_cost_list = []

    for t in job_sizes:
        f_c = avg_mat_cost + (tot_f_fixed / t) + (tot_f_cons * meters_per_ton) + f_mac_per_ton
        r_c = avg_mat_cost + (tot_r_fixed / t) + (tot_r_cons * meters_per_ton) + r_mac_per_ton
        f_cost_list.append(f_c)
        r_cost_list.append(r_c)

    df_comp = pd.DataFrame({
        "الطن": job_sizes,
        "فلكسو": f_cost_list,
        "روتو": r_cost_list
    })

    fig_comp = go.Figure()
    fig_comp.add_trace(go.Scatter(x=df_comp["الطن"], y=df_comp["فلكسو"], name='فلكسو'))
    fig_comp.add_trace(go.Scatter(x=df_comp["الطن"], y=df_comp["روتو"], name='روتو'))
    st.plotly_chart(fig_comp, use_container_width=True)

# ==========================================
# TAB 8: Client Mix
# ==========================================
with tab_mix:
    st.header("تحليل مبيعات العميل")
    
    tot_vol = st.number_input("الطلب السنوي (طن)", value=1200)

    crm1, crm2 = st.columns(2)

    with crm1:
        st.subheader("مبيعات الروتو")
        r_data = [
            {"هيكل": "طبقة", "نسبة": 30.0, "سعر": 13.0},
            {"هيكل": "طبقتين", "نسبة": 50.0, "سعر": 13.5},
            {"هيكل": "3 طبقات", "نسبة": 20.0, "سعر": 15.0},
        ]
        df_r_mix = st.data_editor(pd.DataFrame(r_data), use_container_width=True, key="r_mix")
        
        df_r_mix["كمية"] = tot_vol * (df_r_mix["نسبة"] / 100.0)
        df_r_mix["ايراد"] = df_r_mix["كمية"] * df_r_mix["سعر"] * 1000
        
        r_tot_rev = df_r_mix["ايراد"].sum()
        r_avg_p = r_tot_rev / (tot_vol * 1000) if tot_vol > 0 else 0
            
        st.metric("ايرادات الروتو", fmt(r_tot_rev))
        st.metric("متوسط سعر الروتو", fmt1(r_avg_p))

    with crm2:
        st.subheader("مبيعات الفلكسو")
        f_data = [
            {"هيكل": "طبقة", "نسبة": 60.0, "سعر": 12.0},
            {"هيكل": "طبقتين", "نسبة": 30.0, "سعر": 13.0},
            {"هيكل": "3 طبقات", "نسبة": 10.0, "سعر": 15.0},
        ]
        df_f_mix = st.data_editor(pd.DataFrame(f_data), use_container_width=True, key="f_mix")

        df_f_mix["كمية"] = tot_vol * (df_f_mix["نسبة"] / 100.0)
        df_f_mix["ايراد"] = df_f_mix["كمية"] * df_f_mix["سعر"] * 1000
        
        f_tot_rev = df_f_mix["ايراد"].sum()
        f_avg_p = f_tot_rev / (tot_vol * 1000) if tot_vol > 0 else 0
            
        st.metric("ايرادات الفلكسو", fmt(f_tot_rev))
        st.metric("متوسط سعر الفلكسو", fmt1(f_avg_p))

    st.markdown("---")
    st.subheader("الرسم البياني")
    
    df_r_mix["التقنية"] = "روتو"
    df_f_mix["التقنية"] = "فلكسو"
    
    df_cmb = pd.concat([df_r_mix, df_f_mix])
    
    cv1, cv2 = st.columns(2)
    with cv1:
        fig_v = px.bar(df_cmb, x="التقنية", y="كمية", color="هيكل", barmode="group")
        st.plotly_chart(fig_v, use_container_width=True)
        
    with cv2:
        fig_r = px.bar(df_cmb, x="التقنية", y="ايراد", color="هيكل", barmode="group")
        st.plotly_chart(fig_r, use_container_width=True)
