import streamlit as st
from components.style import apply_custom_style, sidebar_logo

st.set_page_config(
    page_title="Vegam | Operational Intelligence",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_custom_style()
sidebar_logo()

def main():
    import json, os

    # ── HERO HEADER ─────────────────────────────────────────────
    hero_html = """
<div style="background: linear-gradient(135deg, #1C1A17 0%, #252422 60%, #2d1f15 100%); border-radius: 14px; padding: 52px 48px; margin-bottom: 2rem; position: relative; overflow: hidden; box-shadow: 0 8px 40px rgba(0,0,0,0.22); border: 1px solid rgba(235,94,40,0.18);">
    <div style="position: absolute; top: -60px; right: -60px; width: 300px; height: 300px; border-radius: 50%; background: radial-gradient(circle, rgba(235,94,40,0.12) 0%, transparent 70%); pointer-events: none;"></div>
    <div style="position: absolute; bottom: -80px; left: 20%; width: 250px; height: 250px; border-radius: 50%; background: radial-gradient(circle, rgba(45,106,79,0.08) 0%, transparent 70%); pointer-events: none;"></div>
    <div style="position: relative; z-index: 1;">
        <div style="font-family: 'IBM Plex Mono', monospace; font-size: 10px; color: #EB5E28; letter-spacing: 0.3em; text-transform: uppercase; margin-bottom: 10px;">Operational Intelligence Platform</div>
        <div style="font-family: 'Playfair Display', serif; font-size: 3.2rem; font-weight: 900; color: #FFFCF2; line-height: 1.1; margin-bottom: 16px; letter-spacing: -0.02em;">VEGAM</div>
        <div style="width: 64px; height: 3px; background: linear-gradient(90deg, #EB5E28, transparent); margin-bottom: 20px;"></div>
        <p style="font-family: 'DM Sans', sans-serif; font-size: 15px; color: #CCC5B9; max-width: 520px; line-height: 1.65; margin: 0;">Real-time predictive forensics for supply chain resilience. Identify bottlenecks before they impact your delivery timeline using deep gradient boosting and game-theoretic explainability.</p>
    </div>
</div>
"""
    st.markdown(hero_html, unsafe_allow_html=True)

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
            "icon": "◈",
            "title": "Operations Overview",
            "desc": "Fleet-level KPIs, delay distributions, factory performance rankings, and global SHAP importance across all deliveries.",
            "tag": "Page 01",
            "color": "#2D6A4F",
        },
        {
            "icon": "⚖",
            "title": "Delivery Optimizer",
            "desc": "Daily dispatch priority rankings with automated reschedule and factory-swap recommendations to maximize reward.",
            "tag": "Page 02",
            "color": "#EB5E28",
        },
        {
            "icon": "◉",
            "title": "Deep Dive Analysis",
            "desc": "Per-delivery forensic reports with SHAP waterfall decomposition, what-if simulator, and granular root-cause attribution.",
            "tag": "Page 03",
            "color": "#E9C46A",
        },
        {
            "icon": "≡",
            "title": "Forensic Report",
            "desc": "Executive-grade summary with AI-powered narrative analysis, top critical interventions, and downloadable full dataset.",
            "tag": "Page 04",
            "color": "#CCC5B9",
        },
    ]

    cols = st.columns(4)
    for col, m in zip(cols, modules):
        with col:
            st.markdown(f"""
<div style="background: white; border: 1px solid rgba(204,197,185,0.5); border-top: 3px solid {m['color']}; border-radius: 10px; padding: 22px 20px; height: 100%; box-shadow: 0 2px 12px rgba(0,0,0,0.07); transition: all 0.2s ease;">
    <div style="font-size: 22px; margin-bottom: 10px;">{m['icon']}</div>
    <div style="font-family: 'IBM Plex Mono', monospace; font-size: 9px; color: {m['color']}; letter-spacing: 0.18em; text-transform: uppercase; margin-bottom: 6px;">{m['tag']}</div>
    <div style="font-family: 'DM Sans', sans-serif; font-size: 14px; font-weight: 700; color: #252422; margin-bottom: 10px;">{m['title']}</div>
    <div style="font-family: 'DM Sans', sans-serif; font-size: 12px; color: #403D39; line-height: 1.55;">{m['desc']}</div>
</div>
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
