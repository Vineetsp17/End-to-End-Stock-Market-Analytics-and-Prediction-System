from dotenv import load_dotenv
import os
import streamlit as st

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY") or st.secrets["ALPACA_API_KEY"]
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY") or st.secrets["ALPACA_SECRET_KEY"]

client = TradingClient(API_KEY, SECRET_KEY, paper=True)


def place_order(symbol, side, qty=1):
    try:
        order_data = MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            side=OrderSide.BUY if side == "BUY" else OrderSide.SELL,
            time_in_force=TimeInForce.GTC
        )

        order = client.submit_order(order_data)
        return f"✅ {side} order placed for {symbol}"

    except Exception as e:
        return f"❌ Error: {e}"


def get_account():
    acc = client.get_account()
    return {
        "cash": float(acc.cash),
        "portfolio_value": float(acc.portfolio_value)
    }


def get_positions():
    positions = client.get_all_positions()

    return [
        {
            "symbol": p.symbol,
            "qty": float(p.qty),
            "avg_price": float(p.avg_entry_price)
        }
        for p in positions
    ]
