# app.py - Main Streamlit application
import streamlit as st
import pandas as pd
from config import MILL_OPTIONS, CROP_OPTIONS
from farmers_data import get_default_farmers, add_farmer, get_group_stats
from contract_engine import negotiate_contract, add_agent_log
from payment_utils import distribute_payment_pro_rata, distribute_payment_equal, update_farmer_dues
from antigravity_trace import show_trace

st.set_page_config(page_title="AgriCollect - 50 Kisan Group", layout="wide")
st.title("🚜 AgriCollect: 50 Kisanon Ka Group Contract Engine")
st.caption("Chote kisan → Bara farmer → Direct mill contract | Pro-rata / Equal distribution")

# ------------------- SESSION STATE -------------------
if "farmers" not in st.session_state:
    st.session_state.farmers = get_default_farmers()
    st.session_state.group_formed = True
    st.session_state.contract_active = False
    st.session_state.contract_details = None
    st.session_state.mill_payment_received = 0
    st.session_state.agent_logs = []
    st.session_state.distribution_method = "Pro-rata (by land)"

# ------------------- TAB LAYOUT -------------------
tab1, tab2, tab3, tab4 = st.tabs(["👥 Farmer Group (50+)", "📄 Mill Contract", "💰 Payment Distribution", "🧠 Antigravity Trace"])

with tab1:
    st.header("Kisan Group - Collective Power")
    total_land, crops, df, total_investment = get_group_stats(st.session_state.farmers)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Farmers", len(st.session_state.farmers))
    col2.metric("Total Land", f"{total_land:.1f} acres")
    col3.metric("Total Investment", f"PKR {total_investment:,.0f}")
    st.dataframe(df[["id", "name", "land_acres", "crop", "payment_due", "investment"]], use_container_width=True)
    if st.button("➕ Add New Farmer"):
        st.session_state.farmers = add_farmer(st.session_state.farmers)
        add_agent_log(st.session_state.agent_logs, f"New farmer added, total now {len(st.session_state.farmers)}")
        st.rerun()

with tab2:
    st.header("Mill Contract Negotiation")
    col1, col2 = st.columns(2)
    with col1:
        mill = st.selectbox("Select Mill", MILL_OPTIONS)
        crop_type = st.selectbox("Crop for contract", CROP_OPTIONS)
    with col2:
        quantity_kg = st.number_input("Quantity (kg)", min_value=1000, value=50000, step=5000)
        offered_price = st.number_input("Offered Price (PKR per kg)", min_value=50, value=100, step=5)
    if st.button("🚀 Start Negotiation (AI Agent)"):
        with st.spinner("Agent negotiating..."):
            success, final_price, market_rate = negotiate_contract(mill, offered_price, crop_type, quantity_kg, st.session_state.agent_logs)
            if success:
                total_value = final_price * quantity_kg
                st.session_state.contract_active = True
                st.session_state.contract_details = {
                    "mill": mill, "crop": crop_type, "quantity_kg": quantity_kg,
                    "price_per_kg": final_price, "total_value": total_value,
                    "market_rate": market_rate, "date": pd.Timestamp.now().strftime("%Y-%m-%d")
                }
                st.session_state.mill_payment_received = total_value
                add_agent_log(st.session_state.agent_logs, f"✅ Contract signed! Total PKR {total_value:,.0f}")
                st.success(f"Contract signed! PKR {total_value:,.0f}")
            else:
                st.error("Negotiation failed. Try higher price.")
    if st.session_state.contract_active:
        st.subheader("Active Contract")
        st.json(st.session_state.contract_details)

with tab3:
    st.header("Payment Distribution Engine")
    if st.session_state.contract_active and st.session_state.mill_payment_received > 0:
        st.info(f"💰 Mill payment received: PKR {st.session_state.mill_payment_received:,.0f}")
        
        # Distribution method selection
        method = st.radio("Distribution method", ["Pro-rata (by land acres)", "Equal (every farmer same)"])
        crop_filter = st.checkbox("Distribute only to farmers of this crop", value=True)
        crop_type = st.session_state.contract_details["crop"] if crop_filter else None
        
        if st.button("📤 Distribute Payment"):
            if method == "Pro-rata (by land acres)":
                dist = distribute_payment_pro_rata(st.session_state.farmers, st.session_state.mill_payment_received, crop_type)
            else:
                dist = distribute_payment_equal(st.session_state.farmers, st.session_state.mill_payment_received, crop_type)
            
            st.session_state.farmers = update_farmer_dues(st.session_state.farmers, dist)
            add_agent_log(st.session_state.agent_logs, f"Payment distributed using {method} to {len(dist)} farmers")
            st.success(f"Payment distributed using {method}")
            dist_df = pd.DataFrame([{"Farmer ID": k, "Amount (PKR)": v} for k, v in dist.items()])
            st.dataframe(dist_df)
            st.rerun()
        
        # Show updated dues
        st.subheader("Individual Payment Due")
        due_df = pd.DataFrame(st.session_state.farmers)[["id", "name", "payment_due"]]
        st.dataframe(due_df)
    else:
        st.warning("No active contract or payment received. Go to Mill Contract tab first.")

with tab4:
    show_trace(st.session_state.agent_logs)

st.sidebar.header("📊 Group Summary")
total_land, crops, _, _ = get_group_stats(st.session_state.farmers)
st.sidebar.metric("Total Land", f"{total_land:.1f} acres")
st.sidebar.metric("Farmers", len(st.session_state.farmers))
if st.session_state.contract_active:
    st.sidebar.success("✅ Contract Active")
else:
    st.sidebar.warning("No Contract")