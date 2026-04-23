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

BASE_LAYOUT = dict(
    paper_bgcolor=CREAM,
    plot_bgcolor=CREAM,
    font=dict(family="DM Sans", color=CARBON, size=12),
    margin=dict(l=16, r=16, t=44, b=16),
    title_font=dict(family="Playfair Display", size=17, color=CARBON),
    legend=dict(
        bgcolor="rgba(255,252,242,0.9)",
        bordercolor=DUST,
        borderwidth=1,
        font=dict(family="DM Sans", size=11),
    ),
    hoverlabel=dict(
        bgcolor=CARBON,
        font_color=CREAM,
        font_family="IBM Plex Mono",
        font_size=12,
        bordercolor=PAPRIKA,
    ),
)

def _grid_axes():
    return dict(
        gridcolor="rgba(204,197,185,0.4)",
        gridwidth=1,
        zeroline=False,
        linecolor=DUST,
        linewidth=1,
    )


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
    fig.update_layout(
        **BASE_LAYOUT,
        title="Delay Distribution",
        xaxis=dict(title="Hours", **_grid_axes()),
        yaxis=dict(title="Deliveries", **_grid_axes()),
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
    fig.update_layout(
        **BASE_LAYOUT,
        title="Avg Delay by Priority",
        xaxis=dict(title="Priority", **_grid_axes()),
        yaxis=dict(title="Avg Delay (h)", **_grid_axes()),
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
    fig.update_layout(
        **BASE_LAYOUT,
        title="Global Feature Importance (Mean |SHAP|)",
        xaxis=dict(title="Mean Absolute SHAP Value (hours)", **_grid_axes()),
        yaxis=dict(tickfont=dict(family="IBM Plex Mono", size=10)),
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
    fig.update_layout(
        **BASE_LAYOUT,
        title="Avg Delay by Factory",
        xaxis=dict(title="Factory", **_grid_axes()),
        yaxis=dict(title="Avg Delay (h)", **_grid_axes()),
        showlegend=False,
    )
    return fig


# ─── REWARD COMPARISON (FIXED) ────────────────────────────────
def plot_reward_comparison(summary):
    baseline  = summary["baseline_total_reward"]
    optimized = summary["optimized_total_reward"]

    # Two clean vertical bars side by side
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

    # Add a zero-line annotation
    max_abs = max(abs(baseline), abs(optimized))
    y_range_pad = max_abs * 0.25

    fig.update_layout(
        **BASE_LAYOUT,
        title="Reward Optimization Impact",
        barmode="group",
        bargap=0.5,
        bargroupgap=0.1,
        xaxis=dict(
            showgrid=False,
            showline=False,
            tickfont=dict(family="DM Sans", size=13, color=CARBON),
        ),
        yaxis=dict(
            title="Points",
            zeroline=True,
            zerolinecolor=DUST,
            zerolinewidth=1.5,
            **_grid_axes(),
            range=[
                min(baseline, 0) - y_range_pad,
                max(optimized, 0) + y_range_pad,
            ],
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
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


# ─── SHAP WATERFALL (FIXED) ───────────────────────────────────
def plot_shap_waterfall(row, feature_cols):
    """
    Proper SHAP waterfall: base value → feature contributions → final prediction.
    Each bar shows the cumulative running total, colored by direction.
    """
    shap_data = {}
    for feat in feature_cols:
        col = f"shap_{feat}"
        if col in row.index:
            shap_data[feat] = float(row[col])

    if not shap_data:
        fig = go.Figure()
        fig.update_layout(**BASE_LAYOUT, title="SHAP Explanation (Waterfall)")
        return fig

    # Sort by absolute magnitude, top 10
    shap_series = pd.Series(shap_data).reindex(
        pd.Series(shap_data).abs().sort_values(ascending=False).index
    ).head(10)

    base = float(row.get("base_value", 7.0))
    final_pred = base + shap_series.sum()

    # Build waterfall segments
    labels = ["Base Value"] + [f.upper().replace("_", " ") for f in shap_series.index] + ["Prediction"]
    values = [base] + list(shap_series.values) + [final_pred]
    measures = ["absolute"] + ["relative"] * len(shap_series) + ["total"]

    # Color each bar
    bar_colors = [CHARCOAL]
    for v in shap_series.values:
        bar_colors.append(PAPRIKA if v > 0 else GREEN)
    bar_colors.append(PAPRIKA if final_pred > base else GREEN)

    fig = go.Figure(go.Waterfall(
        name="SHAP",
        orientation="h",
        measure=measures,
        y=labels,
        x=values,
        connector=dict(
            line=dict(color=DUST, width=1, dash="dot"),
        ),
        decreasing=dict(marker=dict(color=GREEN, line=dict(width=0))),
        increasing=dict(marker=dict(color=PAPRIKA, line=dict(width=0))),
        totals=dict(marker=dict(color=CHARCOAL, line=dict(width=0))),
        text=[f"{v:+.2f}h" if i != 0 else f"{v:.2f}h" for i, v in enumerate(values)],
        textposition="outside",
        textfont=dict(family="IBM Plex Mono", size=10, color=CARBON),
        hovertemplate="<b>%{y}</b><br>Value: %{x:+.3f}h<extra></extra>",
    ))

    fig.update_layout(
        **BASE_LAYOUT,
        title="SHAP Explanation (Waterfall)",
        xaxis=dict(
            title="Hours of Delay",
            **_grid_axes(),
        ),
        yaxis=dict(
            tickfont=dict(family="IBM Plex Mono", size=10),
            autorange="reversed",
        ),
        height=420,
        showlegend=False,
        margin=dict(l=160, r=60, t=44, b=16),
    )

    return fig
