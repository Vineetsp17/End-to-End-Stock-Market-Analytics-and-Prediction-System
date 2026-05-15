from src.model_rf import run_rf
from src.model_arima import run_arima


def compare_models():

    _, _, _, _, rf_metrics = run_rf()
    _, _, arima_metrics = run_arima()

    return {
        "Random Forest (Tuned)": rf_metrics,
        "ARIMA": arima_metrics
    }


def get_best_model(results):

    best_model = min(results, key=lambda x: results[x]["RMSE"])

    reason = []

    best = results[best_model]

    reason.append(f"Lowest RMSE: {round(best['RMSE'],3)}")
    reason.append(f"Lower MAE: {round(best['MAE'],3)}")
    reason.append(f"Higher R2: {round(best['R2'],3)}")
    reason.append(f"Lower MAPE: {round(best['MAPE'],3)}")

    return best_model, reason