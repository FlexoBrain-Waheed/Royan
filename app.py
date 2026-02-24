import streamlit as st
import pandas as pd
import plotly.express as px

def fmt(num):
    return "{:,.0f}".format(num)

def fmt1(num):
    return "{:,.1f}".format(num)

st.set_page_config(
    page_title="Royan Flexo Smart ERP", 
    layout="wide", 
    page_icon="⚙️"
)

st.title("Royan Smart ERP | رويان - نظام المحاكاة")
st.markdown("---")

tabs_names = [
    "1. Materials | المواد الخام", 
    "2. Printing | الطباعة", 
    "3. Lamination | اللامنيشن", 
    "4. Assets | الأصول",
    "5. HR & Admin | الموارد البشرية",
    "6. Financials | المالية"
]

(
    tab_materials, 
    tab_printing, 
    tab_lamination, 
    tab_machines, 
    tab_hr_admin, 
    tab_finance
) = st.tabs(tabs_names)

# ==========================================
# TAB 1: المواد الخام
# ==========================================
with tab_materials:
    st.header("Raw Materials | المواد الخام")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Transparent BOPP")
        bopp_t_price = st.number_input(
            "Price (SAR/Ton) - T.BOPP | السعر", value=6000
        )
        bopp_t_density = st.number_input(
            "Density - T.BOPP | الكثافة", value=0.91
        )
        st.subheader("White BOPP")
        bopp_w_price = st.number_input(
            "Price (SAR/Ton) - W.BOPP | السعر", value=6400
        )
        bopp_w_density = st.number_input(
            "Density - W.BOPP | الكثافة", value=0.65
        )
        
    with col2:
        st.subheader("Metallized BOPP")
        bopp_m_price = st.number_input(
            "Price (SAR/Ton) - M.BOPP | السعر", value=7000
        )
        bopp_m_density = st.number_input(
            "Density - M.BOPP | الكثافة", value=0.91
        )
        st.subheader("Polyester PET")
        pet_price = st.number_input(
            "Price (SAR/Ton) - PET | السعر", value=5500
        )
        pet_density = st.number_input(
            "Density - PET | الكثافة", value=1.40
        )
        
    with col3:
        st.subheader("PE (Polyethylene)")
        pe_price = st.number_input(
            "Price (SAR/Ton) - PE | السعر", value=5000
        )
        pe_density = st.number_input(
            "Density - PE | الكثافة", value=0.92
        )

    materials_db = {
        "Transparent BOPP": {
            "density": bopp_t_density, "price": bopp_t_price
        },
        "White BOPP": {
            "density": bopp_w_density, "price": bopp_w_price
        },
        "Metallized BOPP": {
            "density": bopp_m_density, "price": bopp_m_price
        },
        "Polyester PET": {
            "density": pet_density, "price": pet_price
        },
        "PE (Polyethylene)": {
            "density": pe_density, "price": pe_price
        }
    }

    st.markdown("---")
    col_m1, col_m2, col_m3 = st.columns(3)
    ink_price = col_m1.number_input(
        "Ink Price | سعر الحبر", value
