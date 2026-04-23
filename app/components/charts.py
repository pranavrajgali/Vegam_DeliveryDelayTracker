import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

PLOTLY_TEMPLATE = {
    "layout": {
        "paper_bgcolor": "#FFFCF2",
        "plot_bgcolor":  "#FFFCF2",
        "font":          {"family": "DM Sans", "color": "#252422"},
        "colorway":      ["#EB5E28", "#403D39", "#CCC5B9", "#2D6A4F", "#E9C46A"],
        "xaxis":         {"gridcolor": "#CCC5B9", "linecolor": "#403D39"},
        "yaxis":         {"gridcolor": "#CCC5B9", "linecolor": "#403D39"},
        "title":         {"font": {"family": "Playfair Display", "size": 24, "weight": 700}, "x": 0, "xanchor": "left"},
    }
}

def apply_template(fig, title_text):
    fig.update_layout(PLOTLY_TEMPLATE["layout"])
    fig.update_layout(title_text=title_text)
    return fig

def plot_delay_distribution(df):
    fig = px.histogram(df, x="predicted_delay_hours", nbins=30, 
                       labels={"predicted_delay_hours": "PREDICTED DELAY (HOURS)"})
    apply_template(fig, "DELAY DISTRIBUTION")
    fig.update_traces(marker_line_color="#252422", marker_line_width=1)
    return fig

def plot_actual_vs_predicted(df):
    fig = px.scatter(df, x="delay_hours", y="predicted_delay_hours", 
                     labels={"delay_hours": "ACTUAL", "predicted_delay_hours": "PREDICTED"},
                     trendline="ols")
    apply_template(fig, "ACTUAL VS PREDICTED DELAYS")
    return fig

def plot_shap_global_importance(shap_values_df, feature_cols):
    mean_abs_shap = shap_values_df[[f'shap_{c}' for c in feature_cols]].abs().mean().sort_values(ascending=True)
    # Clean up labels for the plot
    labels = [c.replace('shap_', '').replace('_', ' ').upper() for c in mean_abs_shap.index]
    
    fig = px.bar(x=mean_abs_shap.values, y=labels, orientation='h',
                 labels={'x': 'MEAN |SHAP VALUE| (HOURS)', 'y': 'FEATURE'})
    apply_template(fig, "GLOBAL FEATURE IMPORTANCE (SHAP)")
    fig.update_traces(marker_color="#EB5E28")
    return fig

def plot_shap_waterfall(row, feature_cols):
    # Base value
    base_value = row['base_value']
    
    # SHAP values for the features
    shap_vals = [row[f'shap_{c}'] for c in feature_cols]
    feature_names = [c.replace('_', ' ').upper() for c in feature_cols]
    
    # Sort by absolute value for a better waterfall
    sorted_indices = np.argsort(np.abs(shap_vals))
    sorted_vals = [shap_vals[i] for i in sorted_indices]
    sorted_names = [feature_names[i] for i in sorted_indices]
    
    fig = go.Figure(go.Waterfall(
        name="SHAP", orientation="h",
        measure=["relative"] * len(sorted_vals),
        x=sorted_vals,
        y=sorted_names,
        base=base_value,
        connector={"line":{"color":"#403D39"}},
        decreasing={"marker":{"color":"#2D6A4F"}},
        increasing={"marker":{"color":"#EB5E28"}}
    ))
    
    fig.update_layout(PLOTLY_TEMPLATE["layout"])
    fig.update_layout(title_text="SHAP EXPLANATION (WATERFALL)")
    return fig

def plot_reward_comparison(summary):
    fig = go.Figure(data=[
        go.Bar(name='Baseline', x=['Total Reward'], y=[summary['baseline_total_reward']], marker_color='#403D39'),
        go.Bar(name='Optimized', x=['Total Reward'], y=[summary['optimized_total_reward']], marker_color='#EB5E28')
    ])
    fig.update_layout(barmode='group')
    apply_template(fig, "REWARD OPTIMIZATION IMPACT")
    return fig

def plot_factory_performance(df):
    # Mean delay per factory
    fac_perf = df.groupby('factory_id')['predicted_delay_hours'].mean().reset_index()
    fig = px.bar(fac_perf, x='factory_id', y='predicted_delay_hours',
                 labels={'predicted_delay_hours': 'AVG DELAY (HOURS)', 'factory_id': 'FACTORY'})
    apply_template(fig, "AVG PREDICTED DELAY BY FACTORY")
    fig.update_traces(marker_color="#403D39")
    return fig

def plot_priority_breakdown(df):
    pri_counts = df['priority_level'].value_counts().reset_index()
    pri_counts.columns = ['priority_level', 'count']
    fig = px.pie(pri_counts, values='count', names='priority_level',
                 color_discrete_sequence=["#EB5E28", "#403D39", "#CCC5B9"])
    apply_template(fig, "DELIVERY PRIORITY MIX")
    return fig
