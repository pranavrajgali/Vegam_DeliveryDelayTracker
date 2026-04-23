# ============================================================
# precompute.py — Run SHAP + Optimizer offline
#
# Usage: python precompute.py  (from project root)
#
# Uses XGBoost's native pred_contribs for exact SHAP values
# (no external shap library needed — same TreeSHAP algorithm).
#
# Generates:
#   app/data/shap_explanations.csv
#   app/data/shap_values.csv
#   app/data/final_delivery_report.csv
#   app/data/optimization_summary.json
# ============================================================

import os
import json
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import joblib
import xgboost
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error

DATA_DIR   = os.path.join(os.path.dirname(__file__), 'data')
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'xgb_model.pkl')


def load_inputs():
    """Load model, params, and all datasets."""
    model = joblib.load(MODEL_PATH)

    with open(os.path.join(DATA_DIR, 'best_params.json')) as f:
        bp = json.load(f)

    feature_cols = bp['feature_cols']
    threshold    = bp['threshold']

    train = pd.read_csv(os.path.join(DATA_DIR, 'train_set.csv'))
    test  = pd.read_csv(os.path.join(DATA_DIR, 'test_set.csv'))
    ext   = pd.read_csv(os.path.join(DATA_DIR, 'External_Factors.csv'))
    factories = pd.read_csv(os.path.join(DATA_DIR, 'Factories.csv'))
    projects  = pd.read_csv(os.path.join(DATA_DIR, 'Projects.csv'))

    test['date'] = pd.to_datetime(test['date'])
    ext['date']  = pd.to_datetime(ext['date'])

    return model, feature_cols, threshold, train, test, ext, factories, projects


# ============================================================
# STAGE 4: SHAP EXPLAINABILITY (XGBoost native TreeSHAP)
# ============================================================
def run_shap(model, feature_cols, threshold, train, test):
    """Compute SHAP values using XGBoost's built-in pred_contribs."""
    print("\n" + "="*55)
    print("STAGE 4: SHAP EXPLAINABILITY")
    print("="*55)

    X_test  = test[feature_cols]
    y_test  = test['delay_hours']
    test_preds = np.clip(model.predict(X_test), 0, None)

    metadata = ['factory_id', 'project_id', 'date', 'priority_level']

    # XGBoost native SHAP — pred_contribs=True returns an (N, F+1) array
    # where the last column is the base value (bias term).
    # This is the EXACT same TreeSHAP algorithm used by the shap library.
    print("Computing SHAP values (XGBoost native TreeSHAP)...")
    dmat = xgboost.DMatrix(X_test)
    contribs = model.get_booster().predict(dmat, pred_contribs=True)

    # contribs shape: (228, 13) — 12 feature contributions + 1 base value
    shap_array = contribs[:, :-1]  # (228, 12) — per-feature contributions
    base_value = float(contribs[0, -1])  # base value (same for all rows)

    print(f"Base value: {base_value:.3f}h | SHAP shape: {shap_array.shape}")

    # Verify: base_value + sum(shap) ≈ prediction
    check = base_value + shap_array[0].sum()
    print(f"Verify row 0: base({base_value:.3f}) + shap_sum({shap_array[0].sum():.3f}) "
          f"= {check:.3f} | model pred: {test_preds[0]:.3f}")

    # Global importance
    mean_abs_shap = pd.Series(
        np.abs(shap_array).mean(axis=0), index=feature_cols
    ).sort_values(ascending=False)
    print("\nGlobal Feature Importance (Mean |SHAP|):")
    for feat, val in mean_abs_shap.items():
        bar = "#" * int((val / mean_abs_shap.max()) * 25)
        print(f"  {feat:<30} {val:.4f}h  {bar}")

    # Per-delivery explanations
    explanations = []
    for idx in range(len(X_test)):
        row_shap  = shap_array[idx]
        row_meta  = test[metadata].iloc[idx]
        predicted = test_preds[idx]
        actual    = y_test.iloc[idx]
        risk      = "HIGH RISK" if predicted > threshold else "low risk"

        shap_series = pd.Series(row_shap, index=feature_cols).sort_values(ascending=False)
        drivers     = shap_series[shap_series > 0].head(3)
        mitigators  = shap_series[shap_series < 0].head(1)

        driver_text = " | ".join([f"{f}: +{v:.2f}h" for f, v in drivers.items()])
        mitig_text  = " | ".join([f"{f}: {v:.2f}h" for f, v in mitigators.items()]) if len(mitigators) else "none"

        explanations.append({
            'factory_id':        row_meta['factory_id'],
            'project_id':        row_meta['project_id'],
            'date':              str(row_meta['date'])[:10],
            'priority_level':    row_meta['priority_level'],
            'predicted_hours':   round(float(predicted), 2),
            'actual_hours':      round(float(actual), 2),
            'risk_label':        risk,
            'base_value':        round(base_value, 3),
            **{f'shap_{c}': round(float(row_shap[i]), 3) for i, c in enumerate(feature_cols)},
            'top_driver_1':      shap_series.index[0],
            'top_driver_1_shap': round(float(shap_series.iloc[0]), 3),
            'top_driver_2':      shap_series.index[1],
            'top_driver_2_shap': round(float(shap_series.iloc[1]), 3),
            'top_driver_3':      shap_series.index[2],
            'top_driver_3_shap': round(float(shap_series.iloc[2]), 3),
            'top_mitigator':     mitigators.index[0] if len(mitigators) else 'none',
            'mitigator_shap':    round(float(mitigators.iloc[0]), 3) if len(mitigators) else 0,
            'plain_explanation': f"Base: {base_value:.1f}h | Drivers: {driver_text} | Helping: {mitig_text}",
        })

    explanations_df = pd.DataFrame(explanations)
    explanations_df.to_csv(os.path.join(DATA_DIR, 'shap_explanations.csv'), index=False)
    print(f"\nSaved: shap_explanations.csv ({len(explanations_df)} rows)")

    # Raw SHAP values
    shap_export = pd.DataFrame(shap_array, columns=[f'shap_{c}' for c in feature_cols])
    shap_export['base_value'] = base_value
    shap_export.to_csv(os.path.join(DATA_DIR, 'shap_values.csv'), index=False)
    print(f"Saved: shap_values.csv")

    return explanations_df, shap_array, base_value


# ============================================================
# STAGE 5: OPTIMIZATION LAYER
# ============================================================
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    a = (np.sin((lat2 - lat1) / 2) ** 2
         + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2)
    return R * 2 * np.arcsin(np.sqrt(np.clip(a, 0, 1)))


def compute_reward(predicted_hours, priority, threshold):
    reward = 10 if predicted_hours <= threshold else -15
    if priority == 'High':
        reward += 5
    reward -= 2 * max(0, predicted_hours - threshold)
    return round(reward, 2)


def build_feature_row(distance_km, routing_complexity, weather_row,
                      factory_row, priority_encoded, date_ts):
    return {
        'distance_km':              distance_km,
        'weather_index':            weather_row['weather_index'],
        'traffic_index':            weather_row['traffic_index'],
        'base_production_per_week': factory_row['base_production_per_week'],
        'production_variability':   factory_row['production_variability'],
        'routing_complexity':       routing_complexity,
        'supply_risk':              factory_row['base_production_per_week'] * factory_row['production_variability'],
        'external_severity':        (weather_row['weather_index'] + weather_row['traffic_index']) / 2,
        'day_of_week':              date_ts.dayofweek,
        'is_weekend':               int(date_ts.dayofweek >= 5),
        'week_of_month':            (date_ts.day - 1) // 7,
        'priority_encoded':         priority_encoded,
    }


def run_optimizer(model, feature_cols, threshold, test, ext, factories, projects, shap_exp):
    """Run reschedule + factory swap simulations, build final report."""
    print("\n" + "="*55)
    print("STAGE 5: OPTIMIZATION LAYER")
    print("="*55)

    test_preds = np.clip(model.predict(test[feature_cols]), 0, None)
    test = test.copy()
    test['predicted_delay_hours'] = test_preds

    metadata = ['factory_id', 'project_id', 'date', 'priority_level']

    # Current rewards
    test['current_reward'] = test.apply(
        lambda r: compute_reward(r['predicted_delay_hours'], r['priority_level'], threshold),
        axis=1
    )

    print(f"Test set: {len(test)} deliveries")
    print(f"Delayed (pred > {threshold:.2f}h): {(test_preds > threshold).sum()}")
    print(f"Baseline reward: {test['current_reward'].sum():.1f}")

    ext_idx = ext.set_index('date')
    delayed_mask = test['predicted_delay_hours'] > threshold

    # ── Reschedule simulation ─────────────────────────────────
    print("\nRescheduling simulation...")
    reschedule_results = {}
    for idx, row in test[delayed_mask].iterrows():
        f_row = factories[factories['factory_id'] == row['factory_id']].iloc[0]
        best_pred = row['predicted_delay_hours']
        best_date = None
        best_sev  = row['external_severity']

        for cdate, crow in ext_idx.iterrows():
            if cdate == row['date']:
                continue
            fv = build_feature_row(row['distance_km'], row['routing_complexity'],
                                   crow, f_row, row['priority_encoded'], pd.Timestamp(cdate))
            np_ = float(np.clip(model.predict(pd.DataFrame([fv])[feature_cols]), 0, None)[0])
            if np_ < best_pred:
                best_pred = np_
                best_date = cdate
                best_sev  = (crow['weather_index'] + crow['traffic_index']) / 2

        new_reward = compute_reward(best_pred, row['priority_level'], threshold)
        reschedule_results[idx] = {
            'best_date':    best_date,
            'pred':         round(best_pred, 3),
            'reward':       new_reward,
            'reward_delta': round(new_reward - row['current_reward'], 2),
            'delay_red':    round(float(row['predicted_delay_hours'] - best_pred), 3),
            'severity':     round(best_sev, 3),
        }

    # ── Factory swap simulation ───────────────────────────────
    print("Factory swap simulation...")
    swap_results = {}
    for idx, row in test[delayed_mask].iterrows():
        f_row   = factories[factories['factory_id'] == row['factory_id']].iloc[0]
        cur_var = f_row['production_variability']
        p_match = projects[projects['project_id'] == row['project_id']]

        best_pred = row['predicted_delay_hours']
        best_fac  = None
        best_dist = row['distance_km']

        if len(p_match) and row['date'] in ext_idx.index:
            prow   = p_match.iloc[0]
            w_row  = ext_idx.loc[row['date']]

            for _, af in factories.iterrows():
                if af['factory_id'] == row['factory_id']:
                    continue
                if af['production_variability'] > cur_var + 0.05:
                    continue
                alt_dist = haversine_km(
                    af['latitude'], af['longitude'],
                    prow['latitude'], prow['longitude']
                ) * row['routing_complexity']
                fv = build_feature_row(alt_dist, row['routing_complexity'],
                                       w_row, af, row['priority_encoded'],
                                       pd.Timestamp(row['date']))
                np_ = float(np.clip(model.predict(pd.DataFrame([fv])[feature_cols]), 0, None)[0])
                if np_ < best_pred:
                    best_pred = np_
                    best_fac  = af['factory_id']
                    best_dist = alt_dist

        new_reward = compute_reward(best_pred, row['priority_level'], threshold)
        swap_results[idx] = {
            'best_factory': best_fac,
            'pred':         round(best_pred, 3),
            'reward':       new_reward,
            'reward_delta': round(new_reward - row['current_reward'], 2),
            'delay_red':    round(float(row['predicted_delay_hours'] - best_pred), 3),
            'distance':     round(best_dist, 2),
        }

    # ── Best recommendation per delivery ──────────────────────
    print("Selecting best recommendations...")
    rows_out = []
    # Get all shap columns from shap_exp if it exists
    shap_cols = []
    if shap_exp is not None:
        shap_cols = [c for c in shap_exp.columns if c not in metadata + ['predicted_hours', 'actual_hours', 'risk_label']]
    
    for idx, row in test.iterrows():
        pred       = row['predicted_delay_hours']
        cur_reward = row['current_reward']

        base_row = {c: row[c] for c in metadata + feature_cols + ['delay_hours']}
        base_row['predicted_delay_hours'] = round(float(pred), 2)
        base_row['risk_label'] = 'HIGH RISK' if pred > threshold else 'low risk'
        base_row['current_reward'] = cur_reward
        base_row['reward_at_risk'] = abs(cur_reward) + (5 if row['priority_level'] == 'High' else 0)

        if idx in reschedule_results:
            r = reschedule_results[idx]
            s = swap_results[idx]
            if max(r['reward_delta'], s['reward_delta']) > 0:
                if r['reward_delta'] >= s['reward_delta']:
                    base_row['best_action']    = 'reschedule'
                    base_row['reward_delta']   = r['reward_delta']
                    base_row['new_pred_hours'] = r['pred']
                    base_row['recommendation'] = (
                        f"Reschedule to {str(r['best_date'])[:10]} "
                        f"(severity {r['severity']:.2f}) → "
                        f"pred {r['pred']:.2f}h [Δ {r['reward_delta']:+.1f}]"
                    )
                else:
                    base_row['best_action']    = 'factory_swap'
                    base_row['reward_delta']   = s['reward_delta']
                    base_row['new_pred_hours'] = s['pred']
                    base_row['recommendation'] = (
                        f"Swap to {s['best_factory']} "
                        f"(dist {s['distance']:.0f}km) → "
                        f"pred {s['pred']:.2f}h [Δ {s['reward_delta']:+.1f}]"
                    )
            else:
                base_row['best_action']    = 'no_change'
                base_row['reward_delta']   = 0
                base_row['new_pred_hours'] = round(float(pred), 2)
                base_row['recommendation'] = 'No better option in available window'
        else:
            base_row['best_action']    = 'none_needed'
            base_row['reward_delta']   = 0
            base_row['new_pred_hours'] = round(float(pred), 2)
            base_row['recommendation'] = 'On-time — no action needed'

        # Merge SHAP if available
        if shap_exp is not None and idx < len(shap_exp):
            for c in shap_cols:
                base_row[c] = shap_exp.iloc[idx][c]

        rows_out.append(base_row)

    final_report = pd.DataFrame(rows_out)
    final_report['date'] = pd.to_datetime(final_report['date'])
    final_report['dispatch_rank'] = final_report.groupby('date')['reward_at_risk'].rank(
        ascending=False, method='first'
    ).astype(int)

    # ── Save ──────────────────────────────────────────────────
    final_report.to_csv(os.path.join(DATA_DIR, 'final_delivery_report.csv'), index=False)
    print(f"\nSaved: final_delivery_report.csv ({final_report.shape})")

    # Summary stats
    baseline_total  = float(final_report['current_reward'].sum())
    total_gain      = float(final_report['reward_delta'].sum())
    optimized_total = baseline_total + total_gain
    pct_improvement = abs(total_gain / baseline_total) * 100 if baseline_total != 0 else 0

    y_test = test['delay_hours']
    mae  = float(mean_absolute_error(y_test, test_preds))
    r2   = float(r2_score(y_test, test_preds))
    rmse = float(np.sqrt(mean_squared_error(y_test, test_preds)))

    summary = {
        'total_deliveries':           int(len(test)),
        'delayed_deliveries':         int((test_preds > threshold).sum()),
        'ontime_deliveries':          int((test_preds <= threshold).sum()),
        'baseline_total_reward':      round(baseline_total, 2),
        'optimized_total_reward':     round(optimized_total, 2),
        'total_reward_gain':          round(total_gain, 2),
        'pct_improvement':            round(pct_improvement, 2),
        'deliveries_rescheduled':     int((final_report['best_action'] == 'reschedule').sum()),
        'deliveries_factory_swapped': int((final_report['best_action'] == 'factory_swap').sum()),
        'no_better_option':           int((final_report['best_action'] == 'no_change').sum()),
        'threshold_hours':            round(threshold, 3),
        'model_test_mae':             round(mae, 3),
        'model_test_r2':              round(r2, 4),
        'model_test_rmse':            round(rmse, 3),
    }
    with open(os.path.join(DATA_DIR, 'optimization_summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"Saved: optimization_summary.json")

    print(f"\nBaseline reward: {baseline_total:+.1f}")
    print(f"Optimized reward: {optimized_total:+.1f}")
    print(f"Gain: {total_gain:+.1f} ({pct_improvement:.1f}%)")

    return final_report, summary


# ============================================================
# MAIN
# ============================================================
def main():
    print("Loading inputs...")
    model, feature_cols, threshold, train, test, ext, factories, projects = load_inputs()
    print(f"Model loaded | Features: {len(feature_cols)} | "
          f"Train: {len(train)} | Test: {len(test)}")

    # Stage 4: SHAP
    shap_exp, shap_array, base_value = run_shap(model, feature_cols, threshold, train, test)

    # Stage 5: Optimizer
    final_report, summary = run_optimizer(
        model, feature_cols, threshold, test, ext, factories, projects, shap_exp
    )

    print("\n" + "="*55)
    print("PRECOMPUTATION COMPLETE")
    print("="*55)
    print("Generated files in data/:")
    for f in ['shap_explanations.csv', 'shap_values.csv',
              'final_delivery_report.csv', 'optimization_summary.json']:
        path = os.path.join(DATA_DIR, f)
        size = os.path.getsize(path) / 1024
        print(f"  {f:<35} {size:.1f} KB")


if __name__ == '__main__':
    main()
