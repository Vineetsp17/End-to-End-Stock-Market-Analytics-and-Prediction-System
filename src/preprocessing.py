import pandas as pd
import os
from src.features import add_advanced_features

def preprocess_data():

    print("Starting preprocessing...")

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(BASE_DIR, "data", "raw_stock_data.csv")

    if not os.path.exists(file_path):
        print("❌ raw_stock_data.csv NOT FOUND")
        return

    df = pd.read_csv(file_path)

    # -------- DATE --------
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values("Date")

    # -------- BASIC FEATURES --------
    df['Returns'] = df['Close'].pct_change()
    df['Volatility'] = df['Returns'].rolling(5).std()

    df['MA_20'] = df['Close'].rolling(20).mean()
    df['MA_50'] = df['Close'].rolling(50).mean()

    # -------- RSI --------
    delta = df['Close'].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # -------- MACD --------
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema12 - ema26

    # -------- BOLLINGER BANDS --------
    rolling_mean = df['Close'].rolling(window=20).mean()
    rolling_std = df['Close'].rolling(window=20).std()

    df['BB_Upper'] = rolling_mean + (2 * rolling_std)
    df['BB_Lower'] = rolling_mean - (2 * rolling_std)

    # -------- ADVANCED FEATURES --------
    df = add_advanced_features(df)

    # -------- FINAL CLEAN --------
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)

    save_path = os.path.join(BASE_DIR, "data", "processed_stock_data.csv")
    df.to_csv(save_path, index=False)

    print("✅ Preprocessing completed")
    print(f"Saved at: {save_path}")


if __name__ == "__main__":
    preprocess_data()