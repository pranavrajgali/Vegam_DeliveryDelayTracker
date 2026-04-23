# DESIGN SYSTEM — Smart Procurement Dashboard
### Végam | TVASTR '26

---

## Concept

**"Industrial Intelligence"** — the aesthetic of a serious operations tool.
Not a startup SaaS. Not a data science notebook. A war room.
Clean, confident, high-information density. Every pixel earns its place.

Inspired by: the NexaVerse reference dashboard but darker, more data-focused,
with the warmth of the Spicy Paprika accent cutting through carbon black.

---

## Color Palette

```
PRIMARY BACKGROUND     #FFFCF2   Floral White    -- page background, light cream
SECONDARY SURFACE      #CCC5B9   Dust Grey       -- cards, sidebars, muted sections
CHARCOAL               #403D39   Charcoal Brown  -- text, borders, secondary elements
CARBON                 #252422   Carbon Black    -- headers, nav, dark surfaces
ACCENT                 #EB5E28   Spicy Paprika   -- CTAs, highlights, alerts, badges

SEMANTIC COLORS:
  Positive / on-time   #2D6A4F   Forest Green
  Warning / mild       #E9C46A   Amber
  Danger / severe      #EB5E28   Spicy Paprika (reuse accent)
  Neutral              #CCC5B9   Dust Grey
```

---

## Typography

```
DISPLAY / HEADERS      "Playfair Display"  -- bold, editorial, premium feel
                        weights: 700, 900
                        use for: page titles, KPI numbers, section headers

BODY / DATA            "IBM Plex Mono"     -- technical, precise, readable
                        weights: 400, 500
                        use for: tables, metrics, labels, code

UI / NAVIGATION        "DM Sans"           -- clean, modern, neutral
                        weights: 400, 500, 600
                        use for: nav items, buttons, captions, descriptions

FONT SCALE:
  Display     48px / 900
  H1          32px / 700
  H2          24px / 700
  H3          18px / 600
  Body        14px / 400
  Caption     12px / 400
  Mono data   13px / 500
```

---

## Streamlit Theme Config
### Put this in .streamlit/config.toml

```toml
[theme]
primaryColor        = "#EB5E28"
backgroundColor     = "#FFFCF2"
secondaryBackgroundColor = "#CCC5B9"
textColor           = "#252422"
font                = "sans serif"
```

---

## Component Specs

### KPI Cards (top of dashboard)
```
Background:   #252422  Carbon Black
Text:         #FFFCF2  Floral White
Accent line:  #EB5E28  3px left border OR bottom border
Number:       Playfair Display 48px 900 weight
Label:        DM Sans 12px uppercase letter-spacing 0.1em
Padding:      24px
Border-radius: 4px (sharp, not bubbly)
Shadow:       none (flat, industrial)

Example card:
┌─────────────────────────┐
│                         │
│  -456                   │
│  BASELINE REWARD        │
│                         │
└─────────────────────────┘
  (left border in #EB5E28)
```

### Data Tables
```
Header:       #403D39 bg, #FFFCF2 text, DM Sans 11px uppercase
Row odd:      #FFFCF2
Row even:     #F5F0E8  (slightly darker cream)
Row hover:    #EB5E28 10% opacity
Border:       1px #CCC5B9
Font:         IBM Plex Mono 13px
Rank badge:   #EB5E28 circle, white number inside
```

### Status Badges
```
HIGH RISK:   bg #EB5E28   text #FFFCF2
DELAYED:     bg #403D39   text #FFFCF2
ON TIME:     bg #2D6A4F   text #FFFCF2
OPTIMIZED:   bg #EB5E28   text #FFFCF2   + checkmark icon
```

### Charts (Plotly config)
```python
PLOTLY_TEMPLATE = {
    "layout": {
        "paper_bgcolor": "#FFFCF2",
        "plot_bgcolor":  "#FFFCF2",
        "font":          {"family": "DM Sans", "color": "#252422"},
        "colorway":      ["#EB5E28", "#403D39", "#CCC5B9", "#2D6A4F", "#E9C46A"],
        "gridcolor":     "#CCC5B9",
        "title":         {"font": {"family": "Playfair Display", "size": 20}},
    }
}
```

### Sidebar
```
Background:   #252422  Carbon Black
Text:         #FFFCF2
Active item:  #EB5E28 left border + slightly lighter bg
Logo area:    top 60px, centered
Nav items:    DM Sans 14px, padding 12px 24px
```

### Buttons
```
Primary:      bg #EB5E28, text #FFFCF2, hover darken 10%
              DM Sans 14px 600, padding 10px 24px
              border-radius: 2px (sharp)
              letter-spacing: 0.05em uppercase

Secondary:    bg transparent, border 1px #403D39, text #403D39
              hover: bg #403D39, text #FFFCF2
```

### SHAP Waterfall Chart
```
Positive bars (increasing delay):   #EB5E28
Negative bars (reducing delay):     #2D6A4F
Base value line:                    #403D39 dashed
Feature labels:                     IBM Plex Mono 12px
```

---

## Page Layout

### Overall structure
```
┌──────────────────────────────────────────────────────┐
│  SIDEBAR (240px)          │  MAIN CONTENT AREA        │
│  Carbon Black             │  Floral White             │
│                           │                           │
│  [LOGO / TITLE]           │  [PAGE HEADER]            │
│                           │                           │
│  > Overview               │  [KPI CARDS ROW]          │
│  > Daily Optimizer        │                           │
│  > Delivery Deep Dive     │  [CHARTS / TABLES]        │
│  > LLM Report             │                           │
│                           │  [DETAIL SECTIONS]        │
│  ─────────────────        │                           │
│  [team name]              │                           │
│  [hackathon name]         │                           │
└──────────────────────────────────────────────────────┘
```

### KPI row (4 cards)
```
[ Total Deliveries ]  [ Avg Delay Hours ]  [ Baseline Reward ]  [ Optimized Reward ]
      228                   7.53h               -456.2              +2598.4
```

### Chart grid
```
Row 1: [Delay Distribution - histogram 60%]  [By Priority - bar 40%]
Row 2: [SHAP Global Importance - horizontal bar 50%]  [Factory Perf - bar 50%]
Row 3: [30-day Heatmap - full width]
```

---

## Page-Specific Design

### Page 2 — Daily Optimizer
```
Top: Date picker + truck slots slider side by side
Middle: Two columns
  LEFT:  "Attempt Today" table (green header)
  RIGHT: "Defer" table (charcoal header)
Bottom: Reward delta bar (before vs after)
Button: "Generate Groq Report" → triggers Page 4
```

### Page 3 — Delivery Deep Dive
```
Top: Delivery ID dropdown (searchable)
     Auto-fills all fields on selection

Section 1 — Delivery Summary (3-col)
  Factory | Project | Priority | Date | Distance

Section 2 — Prediction (2-col)
  LEFT:  Big number — predicted delay hours
         Status badge (HIGH RISK / ON TIME)
         Reward score
  RIGHT: SHAP waterfall chart

Section 3 — Recommendation (full width card)
  Action type badge (RESCHEDULE / FACTORY SWAP)
  Current reward → Optimized reward
  Arrow showing delta
  Specific instruction:
    "Swap to Factory F5 (294km) → predicted 6.93h delay"
    "Reschedule to Apr 24 (severity 0.32) → predicted 7.22h"
```

### Page 4 — LLM Report
```
Clean centered layout
Big "Generate Report" button (Spicy Paprika)
Loading spinner while Groq API calls
Output in a styled text card (Carbon Black bg, white text)
Monospace font for the report
Download button below
```

---

## Streamlit Custom CSS Injection
### Add this to every page via st.markdown

```python
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
</style>
""", unsafe_allow_html=True)
```

---

## App Title and Branding

```
App name:     ProcureIQ
Tagline:      Predict. Prioritize. Optimize.
Team:         BackProp Bandits
Event:        Udhbhav 2026

Sidebar header:
  PROCURE IQ
  ──────────
  Predict · Prioritize · Optimize
  BackProp Bandits
```

---

## File Structure

```
app/
├── main.py                  -- entry point, sidebar nav
├── pages/
│   ├── 01_overview.py       -- dashboard
│   ├── 02_optimizer.py      -- daily scheduler
│   ├── 03_deep_dive.py      -- delivery lookup
│   └── 04_report.py         -- groq LLM report
├── components/
│   ├── kpi_cards.py         -- reusable metric cards
│   ├── charts.py            -- plotly chart functions
│   └── style.py             -- CSS injection function
├── data/
│   ├── test_set.csv
│   ├── train_set.csv
│   └── final_output.csv     -- stage 6 output with SHAP + recommendations
├── models/
│   └── xgb_model.pkl        -- saved trained model
└── .streamlit/
    └── config.toml          -- theme config
```

---

## Inference Flow (How Page 3 Works)

```python
# Load once at app start
import pickle, pandas as pd

model = pickle.load(open('models/xgb_model.pkl', 'rb'))
df_test = pd.read_csv('data/test_set.csv')
df_output = pd.read_csv('data/final_output.csv')  # has SHAP + recommendations

# When judge selects delivery ID
selected_id = st.selectbox("Select Delivery", df_test['delivery_id'])
row = df_test[df_test['delivery_id'] == selected_id]

# Inference
pred_delay = model.predict(row[FEATURE_COLS])[0]

# Pull SHAP and recommendation from precomputed output
report = df_output[df_output['delivery_id'] == selected_id].iloc[0]

# Display
st.metric("Predicted Delay", f"{pred_delay:.2f}h")
st.write(f"Top cause: {report['shap_cause_1']}")
st.write(f"Recommendation: {report['action']}")
st.write(f"Reward delta: {report['reward_delta']:+.1f}")
```

No retraining. Just load model + precomputed outputs. Instant.

---

## What Makes This Design Premium

```
1. Playfair Display for numbers -- editorial, expensive feeling
   Big KPI numbers in serif = confidence, not dashboard-template

2. IBM Plex Mono for data -- signals precision and technical depth
   Tables in monospace = every character aligned, professional

3. Spicy Paprika accent -- warm but strong, not aggressive
   One accent color used sparingly = everything else steps back

4. Carbon Black sidebar -- creates depth and hierarchy
   Dark nav + light content = clear visual separation

5. Sharp corners (border-radius: 2-4px) -- industrial, not startup-bubbly
   Rounded corners = friendly toy, sharp = serious tool

6. Left border on KPI cards -- editorial magazine style
   The 3px paprika line = instant visual anchor

7. Flat shadows -- no depth theater
   Real operations tools are flat, not skeuomorphic
```
