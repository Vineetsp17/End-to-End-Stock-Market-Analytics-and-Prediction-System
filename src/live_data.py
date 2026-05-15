from dotenv import load_dotenv
import os
import requests
import pandas as pd

# ---------------- LOAD ENV ----------------
load_dotenv()

# ---------------- API KEY ----------------
FINNHUB_KEY = os.getenv("FINNHUB_API_KEY")


# ---------------- LIVE DATA ----------------
def fetch_live_price(symbol="AAPL"):

    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_KEY}"

    data = requests.get(url).json()

    if "c" not in data:
        return None

    return {
        "Date": pd.Timestamp.now(),
        "Open": data["o"],
        "High": data["h"],
        "Low": data["l"],
        "Close": data["c"],
        "Volume": data.get("v", 0)
    }