import pandas as pd
import numpy as np

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def get_metrics(y_true, preds):
    return {
        "RMSE": np.sqrt(mean_squared_error(y_true, preds)),
        "MAE": mean_absolute_error(y_true, preds),
        "R2": r2_score(y_true, preds),
        "MAPE": np.mean(np.abs((y_true - preds) / y_true)) * 100
    }


def create_features(df):
    df = df.copy()

    for lag in range(1, 6):
        df[f"Lag_{lag}"] = df["Close"].shift(lag)

    df["MA_10"] = df["Close"].rolling(10).mean()

    return df


def run_gb(df):

    df = df.copy()
    df = df.sort_values("Date")

    # -------- SPLIT FIRST --------
    split = int(len(df) * 0.8)
    train = df.iloc[:split].copy()
    test = df.iloc[split:].copy()

    # -------- FEATURES --------
    train = create_features(train)
    test = create_features(test)

    train["Target"] = train["Close"].shift(-1)
    test["Target"] = test["Close"].shift(-1)

    train.dropna(inplace=True)
    test.dropna(inplace=True)

    features = [c for c in train.columns if c not in ["Date", "Close", "Target"]]

    X_train, y_train = train[features], train["Target"]
    X_test, y_test = test[features], test["Target"]

    model = GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=3,
        random_state=42
    )

    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    metrics = get_metrics(y_test, preds)

    return test["Date"], y_test, preds, metrics