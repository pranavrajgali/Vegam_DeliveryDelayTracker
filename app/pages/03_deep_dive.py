import streamlit as st
import pandas as pd
import os
import json
from components.style import apply_custom_style
from components.charts import plot_shap_waterfall

apply_custom_style()

st.title("🔍 DELIVERY DEEP DIVE")

report_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "final_delivery_report.csv")
params_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "best_params.json")

if os.path.exists(report_path) and os.path.exists(params_path):
    df = pd.read_csv(report_path)
    with open(params_path) as f:
        params = json.load(f)
    
    # Create searchable delivery ID
    df['delivery_label'] = df['project_id'] + " | " + df['factory_id'] + " | " + df['date']
    
    st.subheader("Select Delivery for Forensic Analysis")
    selected_label = st.selectbox("Search by Project, Factory or Date", df['delivery_label'].unique())
    
    row = df[df['delivery_label'] == selected_label].iloc[0]
    
    st.markdown("---")
    
    # SECTION 1: DELIVERY SUMMARY
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.write("**FACTORY**")
        st.write(row['factory_id'])
    with col2:
        st.write("**PROJECT**")
        st.write(row['project_id'])
    with col3:
        st.write("**PRIORITY**")
        st.write(row['priority_level'])
    with col4:
        st.write("**DATE**")
        st.write(row['date'])
        
    st.markdown("---")
    
    # SECTION 2: PREDICTION & SHAP
    col_pred, col_shap = st.columns([1, 2])
    
    with col_pred:
        st.markdown("### PREDICTION")
        color = "#EB5E28" if row['risk_label'] == 'HIGH RISK' else "#2D6A4F"
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; border: 2px solid {color}; border-radius: 8px;">
            <h1 style="color: {color} !important; margin: 0;">{row['predicted_delay_hours']:.2f}h</h1>
            <p style="font-weight: 600; margin-bottom: 0;">PREDICTED DELAY</p>
            <span class="badge-risk" style="background: {color};">{row['risk_label']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.metric("CURRENT REWARD", f"{row['current_reward']:+.1f}")
        st.metric("DISPATCH RANK", f"#{int(row['dispatch_rank'])}")
        
    with col_shap:
        st.plotly_chart(plot_shap_waterfall(row, params['feature_cols']), use_container_width=True)
        
    st.markdown("---")
    
    # SECTION 3: RECOMMENDATION
    st.markdown("### OPTIMIZATION STRATEGY")
    
    action_class = "action-badge-reschedule" if row['best_action'] == 'reschedule' else "action-badge-swap"
    if row['best_action'] in ['none_needed', 'no_change']:
        action_class = "badge-ok"
        
    st.markdown(f"""
    <div class="recommendation-card">
        <span class="{action_class}">{row['best_action'].replace('_', ' ')}</span>
        <h3 style="margin-top: 15px;">{row['recommendation']}</h3>
        <p>Predicted delay reduction: <b>{(row['predicted_delay_hours'] - row['new_pred_hours']):.2f} hours</b></p>
        <p>Potential reward gain: <span style="color: #EB5E28; font-weight: 900;">+{row['reward_delta']:.1f} points</span></p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.error("Data files not found.")
