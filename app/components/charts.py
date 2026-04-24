import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# ─── DESIGN TOKENS ────────────────────────────────────────────
PAPRIKA  = "#EB5E28"
CARBON   = "#252422"
CHARCOAL = "#403D39"
CREAM    = "#FFFCF2"
DUST     = "#CCC5B9"
GREEN    = "#2D6A4F"
AMBER    = "#E9C46A"

BASE_LAYOUT = {
    "paper_bgcolor": CREAM,
    "plot_bgcolor": CREAM,
    "font": {"family": "DM Sans", "color": CARBON, "size": 12},
    "margin": {"l": 16, "r": 16, "t": 44, "b": 16},
    "title_font": {"family": "Playfair Display", "size": 17, "color": CARBON},
    "legend": {
        "bgcolor": "rgba(255,252,242,0.9)",
        "bordercolor": DUST,
        "borderwidth": 1,
        "font": {"family": "DM Sans", "size": 11},
    },
    "hoverlabel": {
        "bgcolor": CARBON,
        "font_color": CREAM,
        "font_family": "IBM Plex Mono",
        "font_size": 12,
        "bordercolor": PAPRIKA,
    },
}

def _grid_axes():
    return {
        "gridcolor": "rgba(204,197,185,0.4)",
        "gridwidth": 1,
        "zeroline": False,
        "linecolor": DUST,
        "linewidth": 1,
    }


# ─── DELAY DISTRIBUTION ───────────────────────────────────────
def plot_delay_distribution(df):
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=df["delay_hours"],
        nbinsx=30,
        marker_color=PAPRIKA,
        marker_opacity=0.85,
        marker_line=dict(width=0),
        name="Delay Hours",
        hovertemplate="<b>%{x:.1f}h</b><br>Count: %{y}<extra></extra>",
    ))
    fig.update_layout(BASE_LAYOUT)
    fig.update_layout(
        title="Delay Distribution",
        xaxis={**_grid_axes(), "title": "Hours"},
        yaxis={**_grid_axes(), "title": "Deliveries"},
        bargap=0.08,
    )
    return fig


# ─── PRIORITY BREAKDOWN ───────────────────────────────────────
def plot_priority_breakdown(df):
    grp = df.groupby("priority_level")["delay_hours"].mean().reset_index()
    colors = [PAPRIKA if p == "High" else (AMBER if p == "Medium" else GREEN)
              for p in grp["priority_level"]]
    fig = go.Figure(go.Bar(
        x=grp["priority_level"],
        y=grp["delay_hours"],
        marker_color=colors,
        marker_line=dict(width=0),
        text=[f"{v:.2f}h" for v in grp["delay_hours"]],
        textposition="outside",
        textfont=dict(family="IBM Plex Mono", size=11, color=CARBON),
        hovertemplate="<b>%{x}</b><br>Avg Delay: %{y:.2f}h<extra></extra>",
    ))
    fig.update_layout(BASE_LAYOUT)
    fig.update_layout(
        title="Avg Delay by Priority",
        xaxis={**_grid_axes(), "title": "Priority"},
        yaxis={**_grid_axes(), "title": "Avg Delay (h)"},
        showlegend=False,
    )
    return fig


# ─── SHAP GLOBAL IMPORTANCE ───────────────────────────────────
def plot_shap_global_importance(shap_df, feature_cols):
    shap_cols = [c for c in shap_df.columns if c.startswith("shap_")]
    if not shap_cols:
        shap_cols = [f"shap_{c}" for c in feature_cols if f"shap_{c}" in shap_df.columns]

    mean_abs = {c.replace("shap_", ""): shap_df[c].abs().mean()
                for c in shap_cols if c in shap_df.columns}
    if not mean_abs:
        return go.Figure()

    importance = pd.Series(mean_abs).sort_values()
    fig = go.Figure(go.Bar(
        x=importance.values,
        y=[f.upper().replace("_", " ") for f in importance.index],
        orientation="h",
        marker_color=[PAPRIKA if v == importance.max() else CHARCOAL for v in importance.values],
        marker_line=dict(width=0),
        text=[f"{v:.3f}" for v in importance.values],
        textposition="outside",
        textfont=dict(family="IBM Plex Mono", size=10, color=CARBON),
        hovertemplate="<b>%{y}</b><br>Mean |SHAP|: %{x:.3f}h<extra></extra>",
    ))
    fig.update_layout(BASE_LAYOUT)
    fig.update_layout(
        title="Global Feature Importance (Mean |SHAP|)",
        xaxis={**_grid_axes(), "title": "Mean Absolute SHAP Value (hours)"},
        yaxis={"tickfont": {"family": "IBM Plex Mono", "size": 10}},
        height=380,
    )
    return fig


# ─── FACTORY PERFORMANCE ──────────────────────────────────────
def plot_factory_performance(df):
    grp = df.groupby("factory_id")["delay_hours"].mean().reset_index().sort_values("delay_hours", ascending=False)
    fig = go.Figure(go.Bar(
        x=grp["factory_id"],
        y=grp["delay_hours"],
        marker_color=[PAPRIKA if i == 0 else (AMBER if i == 1 else CHARCOAL)
                      for i in range(len(grp))],
        marker_line=dict(width=0),
        text=[f"{v:.2f}h" for v in grp["delay_hours"]],
        textposition="outside",
        textfont=dict(family="IBM Plex Mono", size=10, color=CARBON),
        hovertemplate="<b>%{x}</b><br>Avg Delay: %{y:.2f}h<extra></extra>",
    ))
    fig.update_layout(BASE_LAYOUT)
    fig.update_layout(
        title="Avg Delay by Factory",
        xaxis={**_grid_axes(), "title": "Factory"},
        yaxis={**_grid_axes(), "title": "Avg Delay (h)"},
        showlegend=False,
    )
    return fig


# ─── REWARD COMPARISON (FIXED) ────────────────────────────────
def plot_reward_comparison(summary):
    baseline  = summary["baseline_total_reward"]
    optimized = summary["optimized_total_reward"]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Baseline",
        x=["Baseline Reward"],
        y=[baseline],
        marker_color=CHARCOAL,
        marker_line=dict(width=0),
        text=[f"{baseline:+,.0f}"],
        textposition="outside" if baseline >= 0 else "inside",
        textfont=dict(family="IBM Plex Mono", size=13, color=CREAM),
        width=0.35,
        hovertemplate="<b>Baseline</b><br>%{y:+,.1f} pts<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name="Optimized",
        x=["Optimized Reward"],
        y=[optimized],
        marker_color=PAPRIKA,
        marker_line=dict(width=0),
        text=[f"{optimized:+,.0f}"],
        textposition="outside",
        textfont=dict(family="IBM Plex Mono", size=13, color=CARBON),
        width=0.35,
        hovertemplate="<b>Optimized</b><br>%{y:+,.1f} pts<extra></extra>",
    ))

    max_abs = max(abs(baseline), abs(optimized))
    y_range_pad = max_abs * 0.25

    fig.update_layout(BASE_LAYOUT)
    fig.update_layout(
        title="Reward Optimization Impact",
        barmode="group",
        bargap=0.5,
        bargroupgap=0.1,
        xaxis={
            "showgrid": False,
            "showline": False,
            "tickfont": {"family": "DM Sans", "size": 13, "color": CARBON},
        },
        yaxis={
            **_grid_axes(),
            "title": "Points",
            "zeroline": True,
            "zerolinecolor": DUST,
            "zerolinewidth": 1.5,
            "range": [
                min(baseline, 0) - y_range_pad,
                max(optimized, 0) + y_range_pad,
            ],
        },
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
        },
        height=320,
        annotations=[
            dict(
                x=0.5,
                y=max(optimized, 0) + y_range_pad * 0.5,
                xref="paper",
                yref="y",
                text=f"<b>+{summary.get('total_reward_gain', optimized - baseline):,.0f} pts gain</b>  "
                     f"({summary.get('pct_improvement', 0):.1f}% improvement)",
                showarrow=False,
                font=dict(family="IBM Plex Mono", size=12, color=GREEN),
                align="center",
            )
        ],
    )
    return fig


def plot_shap_waterfall(row, feature_cols):
    """
    Redesigned as a Diverging Impact Chart (Force Field) for maximum explainability
    to non-technical judges, as horizontal waterfalls with alternating signs are visually confusing.
    """
    shap_data = {f: float(row[f"shap_{f}"]) for f in feature_cols if f"shap_{f}" in row.index}

    if not shap_data:
        fig = go.Figure()
        fig.update_layout(BASE_LAYOUT)
        fig.update_layout(title="Forensic Impact Breakdown")
        return fig

    # 1. Sort by absolute impact
    sorted_features = sorted(shap_data.keys(), key=lambda x: abs(shap_data[x]), reverse=True)[:10]
    
    y_labels = [f.upper().replace("_", " ") for f in sorted_features]
    deltas = [shap_data[f] for f in sorted_features]
    
    # Reverse lists so the biggest impact is at the top of the Plotly horizontal chart
    y_labels.reverse()
    deltas.reverse()

    fig = go.Figure()

    # Positive = PAPRIKA (Increases Delay), Negative = GREEN (Decreases Delay)
    colors = [PAPRIKA if d >= 0 else GREEN for d in deltas]
    
    fig.add_trace(go.Bar(
        name="Impact",
        orientation="h",
        y=y_labels,
        x=deltas,
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"{d:+.2f}h" for d in deltas],
        textposition="outside",
        textfont=dict(family="DM Mono", size=11, color=CARBON, weight=600),
        hovertemplate="<b>%{y}</b><br>Impact: %{text}<extra></extra>",
        cliponaxis=False
    ))

    # Add a zero line
    fig.add_vline(x=0, line_width=2, line_color=CHARCOAL)

    # Add explanatory annotations for judges
    max_abs_val = max([abs(d) for d in deltas]) if deltas else 1.0
    
    fig.add_annotation(
        x=max_abs_val * 0.5,
        y=len(y_labels) - 0.5,
        text="INCREASES DELAY →",
        showarrow=False,
        font=dict(family="DM Mono", size=10, color=PAPRIKA, weight=700),
        xanchor="center",
        yanchor="bottom"
    )
    
    fig.add_annotation(
        x=-max_abs_val * 0.5,
        y=len(y_labels) - 0.5,
        text="← DECREASES DELAY",
        showarrow=False,
        font=dict(family="DM Mono", size=10, color=GREEN, weight=700),
        xanchor="center",
        yanchor="bottom"
    )

    fig.update_layout(BASE_LAYOUT)
    fig.update_layout(
        title="Forensic Impact Breakdown (SHAP)",
        xaxis={
            **_grid_axes(), 
            "title": "Impact on Predicted Delay (Hours)",
            "zeroline": False,
            "range": [-(max_abs_val * 1.3), max_abs_val * 1.3] # Symmetrical padding
        },
        yaxis={
            "tickfont": {"family": "DM Mono", "size": 10},
        },
        height=480,
        showlegend=False,
        margin={"l": 160, "r": 60, "t": 80, "b": 40},
        bargap=0.3,
    )

    return fig
