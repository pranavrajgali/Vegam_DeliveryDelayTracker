import streamlit as st
from components.style import apply_custom_style, sidebar_logo

st.set_page_config(
    page_title="Vegam | Operational Intelligence",
    page_icon="box",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_custom_style()
sidebar_logo()

def main():
    import json, os

    # ── WELCOME HEADER ──────────────────────────────────────────
    welcome_html = """
<div style="background: white; border: 1px solid rgba(204,197,185,0.4); border-left: 4px solid #EB5E28; border-radius: 10px; padding: 30px; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
    <h2 style="margin-top: 0; color: #252422;">Intelligence Command Center</h2>
    <p style="color: #403D39; margin-bottom: 0;">Welcome to the <b>Vegam</b> operational dashboard. Access predictive forensics, delivery optimization, and root-cause analysis modules below.</p>
</div>
"""
    st.markdown(welcome_html, unsafe_allow_html=True)

    # ── SYSTEM STATUS + QUICK STATS ─────────────────────────────
    summary_path = os.path.join(os.path.dirname(__file__), "data", "optimization_summary.json")

    if os.path.exists(summary_path):
        with open(summary_path) as f:
            summary = json.load(f)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("TOTAL DELIVERIES", summary["total_deliveries"])
        with c2:
            st.metric("MODEL MAE", f"{summary['model_test_mae']}h")
        with c3:
            st.metric("MODEL R²", f"{summary['model_test_r2']*100:.1f}%")
        with c4:
            gain_pct = summary.get("pct_improvement", 0)
            st.metric("REWARD GAIN", f"+{gain_pct:.1f}%")

        st.markdown("<br>", unsafe_allow_html=True)

    # ── MODULE CARDS ────────────────────────────────────────────
    st.markdown("""
<div style="font-family: 'DM Sans', sans-serif; font-size: 10px; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: #403D39; margin-bottom: 16px;">Select a Module</div>
""", unsafe_allow_html=True)

    modules = [
        {
            "url": "overview",
            "title": "Operations Overview",
            "desc": "Fleet-level KPIs, delay distributions, factory performance rankings, and global SHAP importance across all deliveries.",
            "tag": "Page 01",
            "color": "#2D6A4F",
        },
        {
            "url": "optimizer",
            "title": "Delivery Optimizer",
            "desc": "Daily dispatch priority rankings with automated reschedule and factory-swap recommendations to maximize reward.",
            "tag": "Page 02",
            "color": "#EB5E28",
        },
        {
            "url": "deep_dive",
            "title": "Deep Dive Analysis",
            "desc": "Per-delivery forensic reports with SHAP waterfall decomposition, what-if simulator, and granular root-cause attribution.",
            "tag": "Page 03",
            "color": "#E9C46A",
        },
        {
            "url": "report",
            "title": "Forensic Report",
            "desc": "Executive-grade summary with AI-powered narrative analysis, top critical interventions, and downloadable full dataset.",
            "tag": "Page 04",
            "color": "#CCC5B9",
        },
    ]

    st.markdown("""
    <style>
    .module-card {
        background: white; 
        border: 1px solid rgba(204,197,185,0.5); 
        border-radius: 10px; 
        padding: 22px 20px; 
        height: 100%; 
        box-shadow: 0 2px 12px rgba(0,0,0,0.07); 
        transition: all 0.2s ease; 
        cursor: pointer;
    }
    .module-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        border-color: #EB5E28;
    }
    </style>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    for col, m in zip(cols, modules):
        with col:
            st.markdown(f"""
<a href="{m['url']}" target="_self" style="text-decoration: none;">
    <div class="module-card" style="border-top: 3px solid {m['color']};">
        <div style="font-family: 'DM Mono', monospace; font-size: 9px; color: {m['color']}; letter-spacing: 0.18em; text-transform: uppercase; margin-bottom: 6px;">{m['tag']}</div>
        <div style="font-family: 'DM Sans', sans-serif; font-size: 14px; font-weight: 700; color: #252422; margin-bottom: 10px;">{m['title']}</div>
        <div style="font-family: 'DM Sans', sans-serif; font-size: 12px; color: #403D39; line-height: 1.55;">{m['desc']}</div>
    </div>
</a>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── TECH STACK FOOTER ───────────────────────────────────────
    footer_html = """
<div style="display: flex; gap: 12px; flex-wrap: wrap; margin-top: 8px;">
""" + "".join([f"""
<div style="background: #252422; color: #CCC5B9; padding: 5px 14px; border-radius: 20px; font-family: 'IBM Plex Mono', monospace; font-size: 10px; letter-spacing: 0.06em;">{tag}</div>
""" for tag in ["XGBoost v3.2.0", "TreeSHAP", "Streamlit", "Plotly", "TVASTR '26"]]) + """
</div>
"""
    st.markdown(footer_html, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
