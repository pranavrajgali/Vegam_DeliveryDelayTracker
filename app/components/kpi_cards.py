import streamlit as st

def kpi_card(label, value, delta=None):
    st.metric(label=label, value=value, delta=delta)
