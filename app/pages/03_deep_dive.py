import streamlit as st
import pandas as pd
import os
import json
import joblib
import numpy as np
from components.style import apply_custom_style
from components.charts import plot_shap_waterfall

apply_custom_style()

st.title("🔍 DELIVERY DEEP DIVE")

report_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "final_delivery_report.csv")
params_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "best_params.json")
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "xgb_model.pkl")

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
        st.plotly_chart(plot_shap_waterfall(row, params['feature_cols']), width='stretch')
        
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
    
    # ========== WHAT-IF SIMULATOR ==========
    st.markdown("---")
    st.markdown("### 🎮 WHAT-IF SIMULATOR")
    st.markdown("*Adjust factors below to see real-time impact on predictions.*")
    
    # Load model if available
    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            feature_cols = params['feature_cols']
            
            # Create sliders in columns
            col_sim1, col_sim2 = st.columns(2)
            
            with col_sim1:
                weather_sim = st.slider(
                    "Weather Index",
                    min_value=0.0,
                    max_value=10.0,
                    value=float(row['weather_index']),
                    step=0.1
                )
                distance_sim = st.slider(
                    "Distance (km)",
                    min_value=float(df['distance_km'].min()),
                    max_value=float(df['distance_km'].max()),
                    value=float(row['distance_km']),
                    step=1.0
                )
            
            with col_sim2:
                traffic_sim = st.slider(
                    "Traffic Index",
                    min_value=0.0,
                    max_value=10.0,
                    value=float(row['traffic_index']),
                    step=0.1
                )
                routing_sim = st.slider(
                    "Routing Complexity",
                    min_value=0.0,
                    max_value=1.0,
                    value=float(row['routing_complexity']),
                    step=0.05
                )
            
            # Build simulated feature row
            sim_features = {
                'distance_km': distance_sim,
                'weather_index': weather_sim,
                'traffic_index': traffic_sim,
                'base_production_per_week': float(row['base_production_per_week']),
                'production_variability': float(row['production_variability']),
                'routing_complexity': routing_sim,
                'supply_risk': float(row['supply_risk']),
                'external_severity': (weather_sim + traffic_sim) / 2,
                'day_of_week': float(row['day_of_week']),
                'is_weekend': float(row['is_weekend']),
                'week_of_month': float(row['week_of_month']),
                'priority_encoded': float(row['priority_encoded']),
            }
            
            sim_df = pd.DataFrame([sim_features])
            sim_pred = float(np.clip(model.predict(sim_df[feature_cols]), 0, None)[0])
            
            baseline_pred = float(row['predicted_delay_hours'])
            delta_pred = sim_pred - baseline_pred
            
            # Show results
            col_res1, col_res2, col_res3 = st.columns(3)
            
            with col_res1:
                st.metric("BASELINE", f"{baseline_pred:.2f}h")
            
            with col_res2:
                color_delta = "#EB5E28" if delta_pred > 0 else "#2D6A4F"
                sim_pred_val = f"{sim_pred:.2f}h"
                st.markdown(f"""
                <div style="text-align: center; padding: 15px; border-left: 3px solid {color_delta}; border-radius: 4px;">
                    <p style="margin: 0; font-size: 12px; color: #403D39;">SIMULATED PREDICTION</p>
                    <h3 style="margin: 5px 0 0 0; color: {color_delta};">{sim_pred_val}</h3>
                </div>
                """, unsafe_allow_html=True)
            
            with col_res3:
                delta_color = "#EB5E28" if delta_pred > 0 else "#2D6A4F"
                delta_sign = "+" if delta_pred > 0 else ""
                delta_val = f"{delta_sign}{delta_pred:.2f}h"
                st.markdown(f"""
                <div style="text-align: center; padding: 15px; border-left: 3px solid {delta_color}; border-radius: 4px;">
                    <p style="margin: 0; font-size: 12px; color: #403D39;">DELTA</p>
                    <h3 style="margin: 5px 0 0 0; color: {delta_color};">{delta_val}</h3>
                </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            st.warning(f"⚠️ Model loading failed: {str(e)}")
    else:
        st.info("💡 Model file not found for What-If simulation")

else:
    st.error("Data files not found.")
