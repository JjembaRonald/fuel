import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Uganda Fuel Price Regulation Portal",
    page_icon="⛽",
    layout="wide"
)

# Premium Dark Glassmorphism Styling
st.markdown("""
    <style>
    .metric-card {
        background-color: #1E293B;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #3B82F6;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    .metric-title { color: #94A3B8; font-size: 14px; font-weight: 600; }
    .metric-value { color: #F8FAFC; font-size: 28px; font-weight: 700; margin-top: 5px; }
    .metric-delta { color: #10B981; font-size: 12px; margin-top: 2px; }
    </style>
""", unsafe_allow_html=True) # <-- Fixed argument typo here

st.title("National Fuel Price Monitoring System")
st.markdown("##### 🏛️ Ministry of Energy and Mineral Development (Uganda) • Regulatory Oversight Portal")
st.divider()

# --- DEMO DATA ENGINES ---
mock_indicators = {"brent_crude_usd_per_bbl": 78.45, "usd_ugx_exchange_rate": 3780.00}
mock_caps = {
    "Petrol": {"predicted_price_ugx": 5420.00, "mae_score": 12.50},
    "Diesel": {"predicted_price_ugx": 5290.00, "mae_score": 15.10}
}
mock_audit = [
    {"station_name": "Shell Kira Road", "location": "Kampala", "fuel_type": "Petrol", "active_pump_price": 5550.00, "maximum_legal_cap": 5420.00, "violation_margin_ugx": 130.00, "compliance_status": "VIOLATION"},
    {"station_name": "TotalEnergies Mukono", "location": "Mukono", "fuel_type": "Petrol", "active_pump_price": 5410.00, "maximum_legal_cap": 5420.00, "violation_margin_ugx": 0.00, "compliance_status": "COMPLIANT"},
    {"station_name": "Stabex Nalya", "location": "Kampala", "fuel_type": "Diesel", "active_pump_price": 5450.00, "maximum_legal_cap": 5290.00, "violation_margin_ugx": 160.00, "compliance_status": "VIOLATION"},
    {"station_name": "Mogas Gulu Hub", "location": "Gulu", "fuel_type": "Diesel", "active_pump_price": 5280.00, "maximum_legal_cap": 5290.00, "violation_margin_ugx": 0.00, "compliance_status": "COMPLIANT"}
]

# Grid Layout Generation
st.markdown("##### High-Frequency Market Anchors & Dynamic Price Ceilings")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""<div class='metric-card'><div class='metric-title'>BRENT CRUDE BENCHMARK</div>
    <div class='metric-value'>${mock_indicators['brent_crude_usd_per_bbl']:.2f}</div>
    <div class='metric-delta'>Global Import Base Cost</div></div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class='metric-card' style='border-left-color: #8B5CF6;'><div class='metric-title'>EXCHANGE RATE (BOU)</div>
    <div class='metric-value'>{mock_indicators['usd_ugx_exchange_rate']:,} UGX</div>
    <div class='metric-delta'>Official USD/UGX Value</div></div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div class='metric-card' style='border-left-color: #F59E0B;'><div class='metric-title'>PETROL LEGAL CEILING</div>
    <div class='metric-value'>UGX {mock_caps['Petrol']['predicted_price_ugx']:,.0f}</div>
    <div class='metric-delta' style='color: #EF4444;'>Max Allowed Market Pump</div></div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""<div class='metric-card' style='border-left-color: #EC4899;'><div class='metric-title'>DIESEL LEGAL CEILING</div>
    <div class='metric-value'>UGX {mock_caps['Diesel']['predicted_price_ugx']:,.0f}</div>
    <div class='metric-delta' style='color: #EF4444;'>Max Allowed Market Pump</div></div>""", unsafe_allow_html=True)

st.divider()

# Market Compliance Section
st.subheader("Real-Time Station Audits & Price Violations")

audit_df = pd.DataFrame(mock_audit)
audit_df.columns = ["Station Terminal", "District", "Fuel Class", "Active Pump (UGX)", "Maximum Cap (UGX)", "Overcharge Margin", "Status"]
st.dataframe(audit_df.style.format({"Active Pump (UGX)": "{:,.0f}", "Maximum Cap (UGX)": "{:,.0f}", "Overcharge Margin": "{:,.0f}"}), use_container_width=True, hide_index=True)
