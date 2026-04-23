import streamlit as st

def apply_custom_style():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=IBM+Plex+Mono:wght@400;500&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&display=swap');

/* ─── ROOT VARIABLES ─── */
:root {
    --floral-white:  #FFFCF2;
    --dust-grey:     #CCC5B9;
    --charcoal:      #403D39;
    --carbon:        #1C1A17;
    --carbon-mid:    #252422;
    --paprika:       #EB5E28;
    --paprika-dim:   rgba(235,94,40,0.12);
    --green:         #2D6A4F;
    --amber:         #E9C46A;
    --border:        rgba(204,197,185,0.25);
    --shadow:        0 4px 24px rgba(0,0,0,0.18);
    --shadow-sm:     0 2px 8px rgba(0,0,0,0.10);
    --radius:        10px;
    --radius-sm:     6px;
}

/* ─── PAGE BACKGROUND ─── */
.stApp {
    background-color: var(--floral-white) !important;
    background-image:
        radial-gradient(ellipse at 80% 0%, rgba(235,94,40,0.04) 0%, transparent 60%),
        radial-gradient(ellipse at 10% 90%, rgba(45,106,79,0.03) 0%, transparent 50%);
}

/* ─── HIDE STREAMLIT CHROME ─── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none !important; }

/* ─── SIDEBAR ─── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--carbon) 0%, #1A1815 100%) !important;
    border-right: 1px solid rgba(235,94,40,0.2) !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.3) !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
}
[data-testid="stSidebar"] * {
    color: var(--floral-white) !important;
}
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stSelectbox label {
    color: var(--dust-grey) !important;
    font-family: 'DM Sans', sans-serif;
    font-size: 13px;
    letter-spacing: 0.05em;
}

/* Sidebar nav items */
[data-testid="stSidebarNav"] a {
    border-radius: var(--radius-sm) !important;
    margin: 2px 8px !important;
    transition: all 0.18s ease !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    color: var(--dust-grey) !important;
    padding: 10px 16px !important;
}
[data-testid="stSidebarNav"] a:hover {
    background: rgba(235,94,40,0.12) !important;
    color: var(--floral-white) !important;
    padding-left: 20px !important;
}
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: rgba(235,94,40,0.18) !important;
    border-left: 3px solid var(--paprika) !important;
    color: var(--floral-white) !important;
}

/* ─── MAIN CONTENT PADDING ─── */
.main .block-container {
    padding: 2rem 2.5rem 4rem !important;
    max-width: 1280px !important;
}

/* ─── HEADINGS ─── */
h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 2rem !important;
    font-weight: 900 !important;
    color: var(--carbon) !important;
    letter-spacing: -0.01em !important;
    margin-bottom: 0.1rem !important;
}
h2 {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    color: var(--charcoal) !important;
}
h3 {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    color: var(--carbon) !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
p, span, div, label {
    font-family: 'DM Sans', sans-serif;
    color: var(--charcoal);
}

/* ─── METRIC CARDS ─── */
[data-testid="stMetric"] {
    background: var(--carbon-mid) !important;
    border: 1px solid rgba(235,94,40,0.2) !important;
    border-left: 3px solid var(--paprika) !important;
    border-radius: var(--radius) !important;
    padding: 20px 22px !important;
    box-shadow: var(--shadow) !important;
    transition: transform 0.18s ease, box-shadow 0.18s ease !important;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.25) !important;
}
[data-testid="stMetric"] * { color: var(--floral-white) !important; }
[data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.1rem !important;
    font-weight: 900 !important;
    color: var(--floral-white) !important;
    line-height: 1.1 !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: var(--dust-grey) !important;
    margin-bottom: 4px !important;
}
[data-testid="stMetricDelta"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 12px !important;
}

/* ─── BUTTONS ─── */
.stButton > button {
    background: var(--paprika) !important;
    color: var(--floral-white) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    padding: 10px 28px !important;
    box-shadow: 0 2px 12px rgba(235,94,40,0.35) !important;
    transition: all 0.18s ease !important;
}
.stButton > button:hover {
    background: #d4522a !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(235,94,40,0.45) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ─── DOWNLOAD BUTTON ─── */
[data-testid="stDownloadButton"] button {
    background: transparent !important;
    color: var(--paprika) !important;
    border: 1.5px solid var(--paprika) !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    transition: all 0.18s ease !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: var(--paprika) !important;
    color: white !important;
}

/* ─── SELECTBOX / INPUTS ─── */
.stSelectbox > div > div,
.stDateInput > div > div > input,
.stTextInput > div > div > input {
    background: white !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    color: var(--carbon) !important;
    box-shadow: var(--shadow-sm) !important;
    transition: border-color 0.15s ease !important;
}
.stSelectbox > div > div:focus-within,
.stTextInput > div > div:focus-within {
    border-color: var(--paprika) !important;
    box-shadow: 0 0 0 3px var(--paprika-dim) !important;
}

/* ─── SLIDERS ─── */
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: var(--paprika) !important;
    border-color: var(--paprika) !important;
}
.stSlider [data-baseweb="slider"] [data-testid="stTickBar"] {
    background: var(--paprika) !important;
}

/* ─── DATAFRAME / TABLES ─── */
.stDataFrame {
    border-radius: var(--radius) !important;
    overflow: hidden !important;
    box-shadow: var(--shadow-sm) !important;
    border: 1px solid var(--border) !important;
}
.stDataFrame table {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 12.5px !important;
}
.stDataFrame thead th {
    background: var(--carbon-mid) !important;
    color: var(--floral-white) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 10px 14px !important;
}
.stDataFrame tbody tr:nth-child(even) {
    background: rgba(204,197,185,0.12) !important;
}
.stDataFrame tbody tr:hover {
    background: var(--paprika-dim) !important;
}

/* ─── EXPANDERS ─── */
details {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    margin-bottom: 8px !important;
    overflow: hidden !important;
    box-shadow: var(--shadow-sm) !important;
    transition: box-shadow 0.18s ease !important;
}
details:hover {
    box-shadow: var(--shadow) !important;
}
details summary {
    background: white !important;
    padding: 14px 18px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    color: var(--carbon) !important;
    cursor: pointer !important;
}
details[open] summary {
    border-bottom: 1px solid var(--border) !important;
    color: var(--paprika) !important;
}

/* ─── ALERTS / INFO BOXES ─── */
[data-testid="stAlert"] {
    border-radius: var(--radius) !important;
    border: none !important;
    box-shadow: var(--shadow-sm) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
}

/* ─── DIVIDER ─── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* ─── PLOTLY CHART CONTAINERS ─── */
[data-testid="stPlotlyChart"] {
    border-radius: var(--radius) !important;
    overflow: hidden !important;
    box-shadow: var(--shadow-sm) !important;
    border: 1px solid var(--border) !important;
    background: var(--floral-white) !important;
}

/* ─── BADGE CLASSES ─── */
.badge-risk {
    display: inline-block;
    background: var(--paprika);
    color: white;
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 10px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.badge-ok {
    display: inline-block;
    background: var(--green);
    color: white;
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 10px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.badge-warn {
    display: inline-block;
    background: var(--amber);
    color: var(--carbon);
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 10px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* ─── RECOMMENDATION CARD ─── */
.recommendation-card {
    background: var(--carbon-mid);
    border: 1px solid rgba(235,94,40,0.25);
    border-left: 4px solid var(--paprika);
    border-radius: var(--radius);
    padding: 24px 28px;
    color: var(--floral-white);
    box-shadow: var(--shadow);
}
.recommendation-card h3 {
    color: var(--floral-white) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 15px !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
    margin-top: 12px !important;
    margin-bottom: 16px !important;
}
.recommendation-card p {
    color: var(--dust-grey) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
    margin: 6px 0 !important;
}

/* ─── ACTION BADGES ─── */
.action-badge-reschedule {
    display: inline-block;
    background: var(--amber);
    color: var(--carbon);
    padding: 4px 12px;
    border-radius: 4px;
    font-size: 10px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
.action-badge-swap {
    display: inline-block;
    background: var(--paprika);
    color: white;
    padding: 4px 12px;
    border-radius: 4px;
    font-size: 10px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

/* ─── KPI GRID SPACING ─── */
[data-testid="column"] {
    gap: 0 !important;
}

/* ─── SCROLLBAR ─── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--dust-grey); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--charcoal); }

/* ─── PAGE TITLE BLOCK ─── */
.page-header {
    border-bottom: 2px solid var(--border);
    margin-bottom: 1.5rem;
    padding-bottom: 0.75rem;
}
.page-header .page-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: var(--paprika);
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 4px;
}
</style>
""", unsafe_allow_html=True)


def sidebar_logo():
    """Render the Vegam sidebar logo — call once per page after apply_custom_style()."""
    st.sidebar.markdown("""
<div style="
    background: linear-gradient(135deg, #1C1A17 0%, #252422 100%);
    border-bottom: 1px solid rgba(235,94,40,0.3);
    padding: 28px 20px 22px;
    text-align: center;
    margin-bottom: 8px;
">
    <div style="
        font-family: 'Playfair Display', serif;
        font-size: 26px;
        font-weight: 900;
        color: #FFFCF2;
        letter-spacing: 0.18em;
        margin-bottom: 6px;
    ">VEGAM</div>
    <div style="
        height: 2px;
        background: linear-gradient(90deg, transparent, #EB5E28, transparent);
        margin: 8px auto;
        width: 80%;
    "></div>
    <div style="
        font-family: 'DM Sans', sans-serif;
        font-size: 9px;
        color: #CCC5B9;
        letter-spacing: 0.28em;
        text-transform: uppercase;
        margin-bottom: 16px;
    ">Predict &middot; Prioritize &middot; Optimize</div>
    <div style="
        font-family: 'DM Sans', sans-serif;
        font-size: 12px;
        font-weight: 600;
        color: #EB5E28;
    ">Team Vegam</div>
    <div style="
        font-family: 'IBM Plex Mono', monospace;
        font-size: 10px;
        color: #403D39;
        margin-top: 4px;
        letter-spacing: 0.1em;
    ">TVASTR '26</div>
</div>
""", unsafe_allow_html=True)
