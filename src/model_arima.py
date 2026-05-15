import pandas as pd
import numpy as np
import os

from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def get_metrics(y_true, preds):
    rmse = np.sqrt(mean_squared_error(y_true, preds))
    mae = mean_absolute_error(y_true, preds)
    r2 = r2_score(y_true, preds)
    mape = np.mean(np.abs((y_true - preds) / y_true)) * 100

    return {"RMSE": rmse, "MAE": mae, "R2": r2, "MAPE": mape}


def find_best_arima(series):

    best_aic = float("inf")
    best_order = (1,1,1)

    # 🔥 GRID SEARCH
    for p in range(0,3):
        for d in range(0,2):
            for q in range(0,3):
                try:
                    model = ARIMA(series, order=(p,d,q))
                    result = model.fit()

                    if result.aic < best_aic:
                        best_aic = result.aic
                        best_order = (p,d,q)

                except:
                    continue

    return best_order


def run_arima():

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    df = pd.read_csv(os.path.join(BASE_DIR, "data", "processed_stock_data.csv"))

    series = df['Close']

    split = int(len(series) * 0.8)

    train, test = series[:split], series[split:]

    # 🔥 AUTO PARAMETER SELECTION
    best_order = find_best_arima(train)

    model = ARIMA(train, order=best_order)
    model_fit = model.fit()

    preds = model_fit.forecast(steps=len(test))

    metrics = get_metrics(test, preds)

    return test, preds, metrics