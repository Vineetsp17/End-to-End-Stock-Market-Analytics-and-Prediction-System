import pandas as pd
import numpy as np
import os

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def get_metrics(y_true, preds):
    rmse = np.sqrt(mean_squared_error(y_true, preds))
    mae = mean_absolute_error(y_true, preds)
    r2 = r2_score(y_true, preds)
    mape = np.mean(np.abs((y_true - preds) / y_true)) * 100

    return {
        "RMSE": rmse,
        "MAE": mae,
        "R2": r2,
        "MAPE": mape
    }


def create_features(df):
    for lag in range(1, 15):
        df[f"Lag_{lag}"] = df["Close"].shift(lag)

    df["MA_10"] = df["Close"].rolling(10).mean()
    df["MA_20"] = df["Close"].rolling(20).mean()
    df["Momentum"] = df["Close"] - df["Close"].shift(5)

    return df


def run_gb():

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    df = pd.read_csv(os.path.join(BASE_DIR, "data", "processed_stock_data.csv"))

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    df = create_features(df)
    df["Target"] = df["Close"].shift(-1)

    df.dropna(inplace=True)

    features = [c for c in df.columns if c not in ["Date", "Close", "Target"]]

    X = df[features]
    y = df["Target"]

    split = int(len(df) * 0.8)

    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]

    model = GradientBoostingRegressor(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=5,
        random_state=42
    )

    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    metrics = get_metrics(y_test, preds)

    return y_test, preds, metrics