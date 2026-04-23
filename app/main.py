import streamlit as st
from components.style import apply_custom_style

st.set_page_config(
    page_title="Végam | Delay Tracker",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply premium industrial styling
apply_custom_style()

def main():
    # Sidebar Branding
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: #FFFCF2; margin: 0; letter-spacing: 0.1em;">VÉGAM</h2>
        <hr style="border-color: #EB5E28; margin: 10px 0;">
        <p style="color: #CCC5B9; font-size: 12px; text-transform: uppercase; letter-spacing: 0.2em;">
            Predict · Prioritize · Optimize
        </p>
        <p style="color: #EB5E28; font-weight: 600; margin-top: 20px;">Team Végam</p>
        <p style="color: #CCC5B9; font-size: 10px;">TVASTR '26</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Main Page Content
    st.title("OPERATIONAL INTELLIGENCE")
    st.subheader("Predictive Delay Tracking & Supply Chain Optimization")
    
    st.markdown("""
    ---
    ### Welcome to Végam
    This war room dashboard provides real-time predictive forensics for the **Végam** logistics network. 
    Using deep gradient boosting, we identify bottlenecks before they impact your delivery timeline.
    
    **Select a module from the left to begin analysis.**
    """)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.image("https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80", 
                 caption="Strategic Logistics Oversight")
    
    with col2:
        # Load summary if exists
        import json
        import os
        summary_path = os.path.join(os.path.dirname(__file__), "data", "optimization_summary.json")
        if os.path.exists(summary_path):
            with open(summary_path) as f:
                summary = json.load(f)
            st.info(f"""
            **System Status:**
            - Model: XGBoost v3.2.0
            - Test MAE: {summary['model_test_mae']}h
            - Accuracy: {summary['model_test_r2']*100:.1f}% (R2)
            - Data Latency: Real-time (Batch)
            """)
        else:
            st.info("""
            **System Status:**
            - Model: XGBoost v3.2.0
            - Status: Ready for analysis
            - Data Latency: Real-time (Batch)
            """)

if __name__ == "__main__":
    main()
