# ============================================================
# train.py — XGBoost Training + Tuning + Overfitting Monitor
# ============================================================

import os
import json
import joblib
import warnings
import argparse

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from tqdm import tqdm
from xgboost import XGBRegressor
from xgboost.callback import TrainingCallback

from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import TimeSeriesSplit

warnings.filterwarnings("ignore")


# ============================================================
# CONFIG
# ============================================================
FEATURE_COLS = [
    'distance_km', 'weather_index', 'traffic_index',
    'base_production_per_week', 'production_variability',
    'routing_complexity', 'supply_risk', 'external_severity',
    'day_of_week', 'is_weekend', 'week_of_month', 'priority_encoded'
]

TARGET_COL = "delay_hours"

METADATA_COLS = ['factory_id', 'project_id', 'date', 'priority_level']


# ============================================================
# PROGRESS BAR CALLBACK
# ============================================================
class TQDMCallback(TrainingCallback):
    def __init__(self, total_rounds):
        self.pbar = tqdm(total=total_rounds, desc="Training")

    def after_iteration(self, model, epoch, evals_log):
        self.pbar.update(1)

        if "validation_1" in evals_log:
            val_mae = evals_log["validation_1"]["mae"][-1]
            self.pbar.set_postfix({"val_MAE": f"{val_mae:.3f}"})

        return False

    def after_training(self, model):
        self.pbar.close()
        return model


# ============================================================
# METRICS
# ============================================================
def evaluate(y_true, y_pred):
    mae  = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2   = r2_score(y_true, y_pred)

    mask = y_true > 0.5
    mape = np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

    return mae, rmse, r2, mape


def print_metrics(name, y_true, y_pred):
    mae, rmse, r2, mape = evaluate(y_true, y_pred)

    print(f"\n{name}")
    print(f"MAE  : {mae:.3f}")
    print(f"RMSE : {rmse:.3f}")
    print(f"R2   : {r2:.4f}")
    print(f"MAPE : {mape:.2f}%")

    return mae


# ============================================================
# LOAD DATA
# ============================================================
def load_data(data_dir):
    train = pd.read_csv(os.path.join(data_dir, "train_set.csv"))
    test  = pd.read_csv(os.path.join(data_dir, "test_set.csv"))
    return train, test


# ============================================================
# BASELINES
# ============================================================
def run_baselines(X_train, y_train, X_test, y_test):
    print("\n========== BASELINES ==========")

    # Null model
    mean_val = y_train.mean()
    null_pred = np.full(len(y_test), mean_val)
    print_metrics("Null Model", y_test, null_pred)

    # Ridge
    ridge = Ridge(alpha=1.0)
    ridge.fit(X_train, y_train)
    ridge_pred = ridge.predict(X_test)
    print_metrics("Ridge", y_test, ridge_pred)


# ============================================================
# TUNING
# ============================================================
def tune_xgboost(X_train, y_train):
    print("\n========== TUNING ==========")

    tscv = TimeSeriesSplit(n_splits=5)

    param_grid = [
        {'max_depth': 3, 'learning_rate': 0.05, 'subsample': 0.8, 'colsample_bytree': 0.8},
        {'max_depth': 4, 'learning_rate': 0.05, 'subsample': 0.8, 'colsample_bytree': 0.7},
        {'max_depth': 5, 'learning_rate': 0.05, 'subsample': 0.8, 'colsample_bytree': 0.8},
        {'max_depth': 3, 'learning_rate': 0.10, 'subsample': 0.7, 'colsample_bytree': 0.7},
    ]

    best_score = float("inf")
    best_params = None

    for params in param_grid:
        fold_scores = []

        for tr_idx, val_idx in tscv.split(X_train):
            X_tr, X_val = X_train.iloc[tr_idx], X_train.iloc[val_idx]
            y_tr, y_val = y_train.iloc[tr_idx], y_train.iloc[val_idx]

            model = XGBRegressor(
                n_estimators=500,
                eval_metric='mae',
                early_stopping_rounds=50,
                tree_method='hist',
                random_state=42,
                verbosity=0,
                **params
            )

            model.fit(
                X_tr, y_tr,
                eval_set=[(X_val, y_val)],
                verbose=False
            )

            pred = model.predict(X_val)
            mae = mean_absolute_error(y_val, pred)
            fold_scores.append(mae)

        mean_score = np.mean(fold_scores)
        print(f"{params} → MAE: {mean_score:.4f}")

        if mean_score < best_score:
            best_score = mean_score
            best_params = params

    print("\nBest Params:", best_params)
    return best_params


# ============================================================
# TRAIN FINAL MODEL
# ============================================================
def train_final_model(X_train, y_train, params):

    val_size = int(len(X_train) * 0.1)

    X_tr = X_train.iloc[:-val_size]
    y_tr = y_train.iloc[:-val_size]

    X_val = X_train.iloc[-val_size:]
    y_val = y_train.iloc[-val_size:]

    model = XGBRegressor(
        n_estimators=1000,
        early_stopping_rounds=50,
        eval_metric='mae',
        tree_method='hist',
        random_state=42,
        verbosity=0,
        callbacks=[TQDMCallback(1000)],
        **params
    )

    model.fit(
        X_tr, y_tr,
        eval_set=[(X_tr, y_tr), (X_val, y_val)],
        verbose=False
    )

    return model


# ============================================================
# LEARNING CURVE + OVERFITTING CHECK
# ============================================================
def analyze_learning(model):

    results = model.evals_result()

    train_mae = results['validation_0']['mae']
    val_mae   = results['validation_1']['mae']

    plt.figure()
    plt.plot(train_mae, label='Train MAE')
    plt.plot(val_mae, label='Validation MAE')
    plt.xlabel("Boosting Rounds")
    plt.ylabel("MAE")
    plt.title("Learning Curve")
    plt.legend()
    # Save plot instead of showing it to avoid blocking
    os.makedirs("outputs", exist_ok=True)
    plot_path = os.path.join("outputs", "learning_curve.png")
    plt.savefig(plot_path)
    plt.close()
    print(f"\nLearning curve saved to: {plot_path}")

    print(f"\nBest iteration: {model.best_iteration}")

    # Overfitting detection
    if val_mae[-1] > min(val_mae):
        print("⚠️ Overfitting detected (validation error increased)")
    else:
        print("✓ No strong overfitting trend")

    gap = np.mean(val_mae[-10:]) - np.mean(train_mae[-10:])
    print(f"Train-Val Gap: {gap:.3f}")

    if gap > 1.0:
        print("⚠️ Strong overfitting")
    elif gap > 0.5:
        print("⚠️ Mild overfitting")
    else:
        print("✓ Good generalisation")


# ============================================================
# MAIN
# ============================================================
def main(args):

    train, test = load_data(args.data_dir)

    X_train = train[FEATURE_COLS]
    y_train = train[TARGET_COL]

    X_test  = test[FEATURE_COLS]
    y_test  = test[TARGET_COL]

    # baselines
    run_baselines(X_train, y_train, X_test, y_test)

    # tuning
    if args.tune:
        best_params = tune_xgboost(X_train, y_train)
    else:
        best_params = {
            'max_depth': 4,
            'learning_rate': 0.05,
            'subsample': 0.8,
            'colsample_bytree': 0.8
        }

    # training
    model = train_final_model(X_train, y_train, best_params)

    # predictions
    train_pred = np.clip(model.predict(X_train), 0, None)
    test_pred  = np.clip(model.predict(X_test), 0, None)

    # evaluation
    print_metrics("XGBoost Train", y_train, train_pred)
    print_metrics("XGBoost Test", y_test, test_pred)

    # learning curve + overfitting
    analyze_learning(model)

    # save outputs
    os.makedirs(args.output_dir, exist_ok=True)

    # Clear callbacks before saving to avoid pickling errors (tqdm contains file handles)
    model.set_params(callbacks=None)
    joblib.dump(model, os.path.join(args.output_dir, "model.pkl"))

    pd.DataFrame({
        "actual": y_test,
        "predicted": test_pred
    }).to_csv(os.path.join(args.output_dir, "predictions.csv"), index=False)

    with open(os.path.join(args.output_dir, "params.json"), "w") as f:
        json.dump(best_params, f, indent=2)

    print("\nSaved outputs to:", args.output_dir)


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--data_dir", type=str, default="data")
    parser.add_argument("--output_dir", type=str, default="outputs")
    parser.add_argument("--tune", action="store_true")

    args = parser.parse_args()

    main(args)