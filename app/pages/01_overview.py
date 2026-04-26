import streamlit as st
import pandas as pd
import os
import json
from components.style import apply_custom_style, sidebar_logo
from components.charts import (
    plot_delay_distribution, 
    plot_shap_global_importance,
    plot_factory_performance,
    plot_priority_breakdown
)

st.set_page_config(
    page_title="Vegam | Operations Overview",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Ensure styling is applied
apply_custom_style()
sidebar_logo()

st.title("OPERATIONS OVERVIEW")

# Load data
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
report_path = os.path.join(BASE_DIR, "data", "final_delivery_report.csv")
summary_path = os.path.join(BASE_DIR, "data", "optimization_summary.json")
shap_path = os.path.join(BASE_DIR, "data", "shap_values.csv")
params_path = os.path.join(BASE_DIR, "data", "best_params.json")

if os.path.exists(report_path) and os.path.exists(summary_path):
    df = pd.read_csv(report_path)
    with open(summary_path) as f:
        summary = json.load(f)
    with open(params_path) as f:
        params = json.load(f)
    
    # KPI ROW
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("TOTAL DELIVERIES", f"{summary['total_deliveries']}")
    with col2:
        st.metric("AVG DELAY", f"{df['delay_hours'].mean():.2f}h")
    with col3:
        st.metric("BASELINE REWARD", f"{summary['baseline_total_reward']:+,.0f}")
    with col4:
        st.metric("OPTIMIZED REWARD", f"{summary['optimized_total_reward']:+,.0f}")
    
    st.markdown("---")
    
    # CHART GRID
    col_a, col_b = st.columns([3, 2])
    with col_a:
        st.plotly_chart(plot_delay_distribution(df), width='stretch')
    with col_b:
        st.markdown(f"""
        <div class="recommendation-card">
            <h3 style="margin-top:0;">RISK SUMMARY</h3>
            <p>Analysis of <b>{summary['total_deliveries']}</b> deliveries indicates critical bottlenecks.</p>
            <p><span class="badge-risk">HIGH RISK</span> {summary['delayed_deliveries']} deliveries</p>
            <p><span class="badge-ok">OPTIMIZED</span> {summary['total_deliveries'] - summary['delayed_deliveries']} deliveries</p>
            <hr style="border-color: #403D39;">
            <p style="font-size: 14px;">Optimization gain: <b>+{summary['total_reward_gain']:,.0f}</b> points ({summary['pct_improvement']}% improvement)</p>
        </div>
        """, unsafe_allow_html=True)
        
    col_c, col_d = st.columns(2)
    with col_c:
        if os.path.exists(shap_path):
            shap_df = pd.read_csv(shap_path)
            st.plotly_chart(plot_shap_global_importance(shap_df, params['feature_cols']), width='stretch')
    with col_d:
        st.plotly_chart(plot_factory_performance(df), width='stretch')
        
    st.markdown("---")
    st.plotly_chart(plot_priority_breakdown(df), width='stretch')

else:
    st.error("Data files not found. Please ensure precompute.py has been run.")
