import pandas as pd
import numpy as np
import os

from sklearn.ensemble import RandomForestRegressor


def create_features(df):
    for lag in range(1, 11):
        df[f"Lag_{lag}"] = df["Close"].shift(lag)

    df["MA_10"] = df["Close"].rolling(10).mean()
    df["MA_30"] = df["Close"].rolling(30).mean()
    df["Momentum"] = df["Close"] - df["Close"].shift(5)

    return df


def forecast_rf_advanced(days=5):

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    df = pd.read_csv(os.path.join(BASE_DIR, "data", "processed_stock_data.csv"))

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    df = create_features(df)
    df["Target"] = df["Close"].shift(-1)
    df.dropna(inplace=True)

    features = [col for col in df.columns if col not in ["Date", "Close", "Target"]]

    X = df[features]
    y = df["Target"]

    model = RandomForestRegressor(n_estimators=600, random_state=42)
    model.fit(X, y)

    last_data = df.copy()

    future_dates = []
    future_prices = []

    for i in range(days):

        last_data = create_features(last_data)
        last_row = last_data.iloc[-1:]

        pred_price = model.predict(last_row[features])[0]

        new_date = last_data["Date"].iloc[-1] + pd.Timedelta(days=1)

        future_dates.append(new_date)
        future_prices.append(pred_price)

        new_row = last_row.copy()
        new_row["Date"] = new_date
        new_row["Close"] = pred_price

        last_data = pd.concat([last_data, new_row], ignore_index=True)

    return pd.DataFrame({
        "Date": future_dates,
        "Predicted Price": future_prices
    })