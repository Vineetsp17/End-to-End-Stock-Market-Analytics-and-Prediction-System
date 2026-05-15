from dotenv import load_dotenv
import requests
import pandas as pd
import os
import time
import streamlit as st

# ---------------- LOAD ENV ----------------
load_dotenv()

# ---------------- API KEYS ----------------
ALPHA_KEY = os.getenv("ALPHA_KEY") or st.secrets["ALPHA_KEY"]
FINNHUB_KEY = os.getenv("FINNHUB_KEY") or st.secrets["FINNHUB_KEY"]
MARKETSTACK_KEY = os.getenv("MARKETSTACK_KEY") or st.secrets["MARKETSTACK_KEY"]


# ---------------- ALPHA DAILY ----------------
def fetch_alpha_daily(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_KEY}&outputsize=compact"

    data = requests.get(url).json()

    if "Time Series (Daily)" not in data:
        return None

    df = pd.DataFrame.from_dict(
        data["Time Series (Daily)"],
        orient="index"
    )

    df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    }, inplace=True)

    df = df.astype(float)

    df.index = pd.to_datetime(df.index)

    df.reset_index(inplace=True)

    df.rename(columns={"index": "Date"}, inplace=True)

    return df


# ---------------- ALPHA WEEKLY ----------------
def fetch_alpha_weekly(symbol):

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={ALPHA_KEY}"

    data = requests.get(url).json()

    if "Weekly Time Series" not in data:
        return None

    df = pd.DataFrame.from_dict(
        data["Weekly Time Series"],
        orient="index"
    )

    df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    }, inplace=True)

    df = df.astype(float)

    df.index = pd.to_datetime(df.index)

    df.reset_index(inplace=True)

    df.rename(columns={"index": "Date"}, inplace=True)

    return df


# ---------------- ALPHA MONTHLY ----------------
def fetch_alpha_monthly(symbol):

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={ALPHA_KEY}"

    data = requests.get(url).json()

    if "Monthly Time Series" not in data:
        return None

    df = pd.DataFrame.from_dict(
        data["Monthly Time Series"],
        orient="index"
    )

    df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    }, inplace=True)

    df = df.astype(float)

    df.index = pd.to_datetime(df.index)

    df.reset_index(inplace=True)

    df.rename(columns={"index": "Date"}, inplace=True)

    return df


# ---------------- MARKETSTACK ----------------
def fetch_marketstack(symbol):

    url = f"http://api.marketstack.com/v1/eod?access_key={MARKETSTACK_KEY}&symbols={symbol}&limit=365"

    data = requests.get(url).json()

    if "data" not in data:
        return None

    df = pd.DataFrame([
        {
            "Date": pd.to_datetime(item["date"]),
            "Open": item["open"],
            "High": item["high"],
            "Low": item["low"],
            "Close": item["close"],
            "Volume": item["volume"]
        }
        for item in data["data"]
    ])

    return df


# ---------------- FINNHUB ----------------
def fetch_finnhub(symbol):

    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_KEY}"

    data = requests.get(url).json()

    if "c" not in data:
        return None

    df = pd.DataFrame([{
        "Date": pd.Timestamp.now(),
        "Open": data["o"],
        "High": data["h"],
        "Low": data["l"],
        "Close": data["c"],
        "Volume": data.get("v", 0)
    }])

    return df


# ---------------- MAIN ----------------
def fetch_stock_data(symbol="AAPL"):

    print("Building long-term dataset...")

    df_list = []

    functions = [
        fetch_alpha_daily,
        fetch_alpha_weekly,
        fetch_alpha_monthly,
        fetch_marketstack,
        fetch_finnhub
    ]

    for func in functions:

        try:
            df = func(symbol)

            if df is not None:

                # STANDARDIZE DATE FORMAT
                df["Date"] = pd.to_datetime(
                    df["Date"],
                    errors="coerce"
                )

                # Convert timezone-aware → naive
                if df["Date"].dt.tz is not None:
                    df["Date"] = df["Date"].dt.tz_convert(None)

                df_list.append(df)

                print(f"✔ {func.__name__} success")

            time.sleep(12)

        except Exception as e:
            print(f"❌ {func.__name__} failed:", e)

    if not df_list:
        print("❌ No data fetched")
        return

    df = pd.concat(df_list, ignore_index=True)

    # FINAL CLEAN
    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    df.dropna(subset=["Date"], inplace=True)

    df.sort_values("Date", inplace=True)

    df.drop_duplicates(
        subset=["Date"],
        keep="last",
        inplace=True
    )

    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    save_path = os.path.join(
        BASE_DIR,
        "data",
        "raw_stock_data.csv"
    )

    df.to_csv(save_path, index=False)

    print("✅ LONG-TERM DATASET CREATED")
    print(f"Saved at: {save_path}")


if __name__ == "__main__":
    fetch_stock_data()
