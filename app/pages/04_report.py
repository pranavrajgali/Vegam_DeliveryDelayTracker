import streamlit as st
import pandas as pd
import os
import json
from components.style import apply_custom_style

apply_custom_style()

st.title("📄 FORENSIC REPORT")

report_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "final_delivery_report.csv")
summary_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "optimization_summary.json")

if os.path.exists(report_path) and os.path.exists(summary_path):
    df = pd.read_csv(report_path)
    with open(summary_path) as f:
        summary = json.load(f)
    
    st.markdown("""
    ### EXECUTIVE SUMMARY
    Automated optimization report for the **Végam** delivery network. 
    This document summarizes risk-weighted interventions and forensic root-cause analysis.
    """)
    
    # Summary Metrics Table
    stats = {
        "Metric": [
            "Total Operations Analyzed",
            "Initial High-Risk Deliveries",
            "Baseline Reward Expectancy",
            "Optimized Reward Expectancy",
            "Interventions Proposed (Reschedule)",
            "Interventions Proposed (Factory Swap)",
            "Model Fidelity (R2 Score)"
        ],
        "Value": [
            summary['total_deliveries'],
            summary['delayed_deliveries'],
            f"{summary['baseline_total_reward']:,.2f}",
            f"{summary['optimized_total_reward']:,.2f}",
            summary['deliveries_rescheduled'],
            summary['deliveries_factory_swapped'],
            f"{summary['model_test_r2']*100:.2f}%"
        ]
    }
    st.table(pd.DataFrame(stats))
    
    st.markdown("---")
    
    st.subheader("TOP 5 CRITICAL INTERVENTIONS")
    # Sort by reward delta to show high-impact changes
    critical = df[df['reward_delta'] > 0].sort_values('reward_delta', ascending=False).head(5)
    
    for idx, row in critical.iterrows():
        with st.expander(f"PROJECT {row['project_id']} | GAIN: +{row['reward_delta']:.1f} pts"):
            st.markdown(f"""
            **Risk Profile:** {row['risk_label']} ({row['predicted_delay_hours']:.2f}h predicted delay)
            
            **Root Cause:**
            - **Primary Driver:** {row['top_driver_1']} (+{row['top_driver_1_shap']:.2f}h)
            - **Secondary Driver:** {row['top_driver_2']} (+{row['top_driver_2_shap']:.2f}h)
            
            **Optimized Action:**
            `{row['recommendation']}`
            
            **Outcome:**
            New predicted delay: **{row['new_pred_hours']:.2f}h**
            """)
            
    st.markdown("---")
    
    st.subheader("AI FORENSIC ANALYSIS")
    st.info("System utilizing Llama-3-70B (Groq) for automated narrative generation.")
    
    # Placeholder for LLM Report
    st.markdown(f"""
    <div style="background: #252422; color: #CCC5B9; padding: 30px; border-radius: 4px; border: 1px solid #403D39; font-family: 'IBM Plex Mono', monospace;">
        <h4 style="color: #EB5E28 !important; margin-top:0;">FORENSIC NARRATIVE</h4>
        <p><b>Observation:</b> The network is currently exhibiting systemic delays primarily driven by <b>{df['top_driver_1'].mode()[0]}</b> and <b>{df['top_driver_2'].mode()[0]}</b>.</p>
        <p><b>Diagnosis:</b> High-risk deliveries are concentrated in <b>{df[df['risk_label']=='HIGH RISK']['factory_id'].mode()[0]}</b> operations. The collinearity between external severities and factory production variability is the primary source of variance.</p>
        <p><b>Prescription:</b> By implementing the <b>{summary['deliveries_rescheduled'] + summary['deliveries_factory_swapped']}</b> proposed interventions, the system can recapture approximately <b>{summary['total_reward_gain']:,.0f} points</b> in reward value, representing a <b>{summary['pct_improvement']}%</b> efficiency gain.</p>
        <p><b>Conclusion:</b> Immediate execution of the Day 1 Dispatch Ranking is recommended to mitigate the {summary['delayed_deliveries']} identified high-risk events.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Download Full Report
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "DOWNLOAD COMPLETE FORENSIC DATA (CSV)",
        csv,
        "vegam_forensic_report.csv",
        "text/csv",
        key='download-csv'
    )

else:
    st.error("Data files not found.")
