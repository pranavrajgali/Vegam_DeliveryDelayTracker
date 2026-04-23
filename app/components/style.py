import streamlit as st

def apply_custom_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=IBM+Plex+Mono:wght@400;500&family=DM+Sans:wght@400;500;600&display=swap');

    /* Root variables */
    :root {
        --floral-white:  #FFFCF2;
        --dust-grey:     #CCC5B9;
        --charcoal:      #403D39;
        --carbon:        #252422;
        --paprika:       #EB5E28;
        --green:         #2D6A4F;
        --amber:         #E9C46A;
    }

    /* Page background */
    .stApp { background-color: var(--floral-white); }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--carbon);
        border-right: 1px solid var(--charcoal);
    }
    [data-testid="stSidebar"] * { color: var(--floral-white) !important; }

    /* Headers */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: var(--carbon) !important;
    }
    h1 { font-size: 32px !important; font-weight: 900 !important; }

    /* Body text */
    p, span, div, label {
        font-family: 'DM Sans', sans-serif;
        color: var(--carbon);
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: var(--carbon);
        border-left: 3px solid var(--paprika);
        padding: 20px;
        border-radius: 4px;
    }
    [data-testid="stMetric"] * { color: var(--floral-white) !important; }
    [data-testid="stMetricValue"] {
        font-family: 'Playfair Display', serif !important;
        font-size: 36px !important;
        font-weight: 900 !important;
    }

    /* Primary button */
    .stButton > button {
        background-color: var(--paprika) !important;
        color: var(--floral-white) !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        border: none !important;
        border-radius: 2px !important;
        padding: 10px 28px !important;
    }
    .stButton > button:hover {
        background-color: #d4522a !important;
        transform: translateY(-1px);
        transition: all 0.15s ease;
    }

    /* Dataframe / tables */
    .stDataFrame {
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 13px !important;
    }

    /* Selectbox, date input */
    .stSelectbox, .stDateInput {
        font-family: 'DM Sans', sans-serif;
    }

    /* Divider */
    hr { border-color: var(--dust-grey); }

    /* Badge helper classes */
    .badge-risk {
        background: var(--paprika);
        color: white;
        padding: 2px 8px;
        border-radius: 2px;
        font-size: 11px;
        font-family: 'DM Sans', sans-serif;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    .badge-ok {
        background: var(--green);
        color: white;
        padding: 2px 8px;
        border-radius: 2px;
        font-size: 11px;
        font-family: 'DM Sans', sans-serif;
        font-weight: 600;
    }
    
    /* Recommendation Card */
    .recommendation-card {
        background: var(--carbon);
        padding: 24px;
        border-radius: 4px;
        border-left: 5px solid var(--paprika);
        color: var(--floral-white);
        margin: 10px 0;
    }
    .recommendation-card h3 {
        color: var(--floral-white) !important;
        margin-top: 0;
    }
    .recommendation-card p {
        color: var(--dust-grey) !important;
    }
    
    /* Action Badges */
    .action-badge-reschedule {
        background: var(--green);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
    }
    .action-badge-swap {
        background: var(--amber);
        color: var(--carbon);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    </style>
    """, unsafe_allow_html=True)
