import streamlit as st
import pandas as pd
import os
import json
from components.style import apply_custom_style
from components.charts import plot_reward_comparison

apply_custom_style()

st.title("⚖️ DELIVERY OPTIMIZER")

report_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "final_delivery_report.csv")
summary_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "optimization_summary.json")

if os.path.exists(report_path) and os.path.exists(summary_path):
    df = pd.read_csv(report_path)
    with open(summary_path) as f:
        summary = json.load(f)
    
    # Date selection for the day's batch
    available_dates = sorted(df['date'].unique())
    selected_date = st.selectbox("Select Operation Date", available_dates)
    
    day_df = df[df['date'] == selected_date].sort_values('dispatch_rank')
    
    # Top Metrics for the day
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("DAILY DELIVERIES", len(day_df))
    with col2:
        st.metric("HIGH RISK", len(day_df[day_df['risk_label'] == 'HIGH RISK']))
    with col3:
        daily_gain = day_df['reward_delta'].sum()
        st.metric("OPT. REWARD GAIN", f"+{daily_gain:,.1f}")
        
    st.markdown("---")
    
    # Comparison Chart
    st.plotly_chart(plot_reward_comparison(summary), use_container_width=True)
    
    st.subheader(f"Dispatch Priority Ranking — {selected_date}")
    
    # Display the dispatch table
    display_cols = [
        'dispatch_rank', 'project_id', 'factory_id', 'priority_level', 
        'predicted_delay_hours', 'risk_label', 'best_action', 'recommendation'
    ]
    
    # Formatted version for display
    styled_df = day_df[display_cols].copy()
    styled_df.columns = [
        'RANK', 'PROJECT', 'FACTORY', 'PRIORITY', 
        'PRED DELAY (H)', 'RISK', 'ACTION', 'RECOMMENDATION'
    ]
    
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    st.markdown("### Strategy Breakdown")
    col_x, col_y = st.columns(2)
    with col_x:
        st.markdown(f"""
        <div style="background: #2D6A4F; padding: 20px; border-radius: 4px; color: white;">
            <h4 style="color: white !important; margin-top:0;">RESCHEDULE SUCCESS</h4>
            <p>Model identified <b>{summary['deliveries_rescheduled']}</b> deliveries where shifting the date mitigates weather/traffic risk.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_y:
        st.markdown(f"""
        <div style="background: #E9C46A; padding: 20px; border-radius: 4px; color: #252422;">
            <h4 style="color: #252422 !important; margin-top:0;">FACTORY SWAP SUCCESS</h4>
            <p>Model identified <b>{summary['deliveries_factory_swapped']}</b> deliveries where changing source factory reduces distance-based delay.</p>
        </div>
        """, unsafe_allow_html=True)

else:
    st.error("Data files not found.")
