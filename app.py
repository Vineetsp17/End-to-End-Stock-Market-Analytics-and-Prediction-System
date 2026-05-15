import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import time

from src.data_collection import fetch_stock_data
from src.preprocessing import preprocess_data
from src.model_rf import run_rf
from src.model_gb import run_gb
from src.forecasting import forecast_rf_advanced
from src.live_data import fetch_live_price
from src.trading import place_order, get_account, get_positions
from src.signals import generate_signal

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Stock Dashboard", layout="wide")

# ---------------- SIDEBAR ----------------
st.sidebar.title("Dashboard Controls")

stocks = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]
selected_stock = st.sidebar.selectbox("Select Stock", stocks)

if st.sidebar.button("Load Data"):
    fetch_stock_data(selected_stock)
    preprocess_data()
    st.sidebar.success("Data Updated")

# ---------------- LIVE SETTINGS ----------------
st.sidebar.markdown("---")
st.sidebar.subheader("Live Settings")

live_mode = st.sidebar.checkbox("Enable Live Mode")
refresh_rate = st.sidebar.slider("Refresh Interval (sec)", 5, 60, 10)

# ---------------- LOAD DATA ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "data", "processed_stock_data.csv")

if not os.path.exists(file_path):
    st.warning("Click Load Data first")
    st.stop()

df = pd.read_csv(file_path)

# ---------------- CLEAN ----------------
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date").reset_index(drop=True)
df = df.dropna()

# ---------------- SESSION STATE ----------------
if "live_df" not in st.session_state:
    st.session_state.live_df = df.copy()

# ---------------- TIMEFRAME ----------------
timeframe = st.radio("Select Timeframe", ["1M", "3M", "6M", "1Y", "All"], horizontal=True)

def apply_timeframe(data):
    if timeframe == "1M":
        return data[data["Date"] >= data["Date"].max() - pd.Timedelta(days=30)]
    elif timeframe == "3M":
        return data[data["Date"] >= data["Date"].max() - pd.Timedelta(days=90)]
    elif timeframe == "6M":
        return data[data["Date"] >= data["Date"].max() - pd.Timedelta(days=180)]
    elif timeframe == "1Y":
        return data[data["Date"] >= data["Date"].max() - pd.Timedelta(days=365)]
    return data

# ---------------- INDICATORS ----------------
df["MA_20"] = df["Close"].rolling(20).mean()
df["MA_50"] = df["Close"].rolling(50).mean()

df["BB_Upper"] = df["MA_20"] + 2 * df["Close"].rolling(20).std()
df["BB_Lower"] = df["MA_20"] - 2 * df["Close"].rolling(20).std()

# ---------------- LAYOUT ----------------
def apply_layout(fig):
    fig.update_layout(
        template="plotly_dark",
        xaxis=dict(rangeslider=dict(visible=True)),
        hovermode="x unified"
    )
    return fig

# ---------------- TITLE ----------------
st.title(f"Stock Market Analytics Dashboard - {selected_stock}")

# ---------------- LIVE MODE ----------------
if live_mode:

    st.subheader("🔴 Live Market Feed")

    placeholder = st.empty()

    while True:

        live_data = fetch_live_price(selected_stock)

        if live_data:
            new_row = pd.DataFrame([live_data])

            st.session_state.live_df = pd.concat(
                [st.session_state.live_df, new_row],
                ignore_index=True
            )

            st.session_state.live_df.drop_duplicates(
                subset=["Date"], keep="last", inplace=True
            )

            st.session_state.live_df.sort_values("Date", inplace=True)

            if len(st.session_state.live_df) > 1000:
                st.session_state.live_df = st.session_state.live_df.tail(500)

        live_df = st.session_state.live_df.copy()
        live_df["Date"] = pd.to_datetime(live_df["Date"])

        live_filtered = apply_timeframe(live_df)

        with placeholder.container():

            current_price = live_df["Close"].iloc[-1]
            st.metric("Live Price", round(current_price, 2))

            fig_live = px.line(
                live_filtered,
                x="Date",
                y="Close",
                title="Live Price Movement"
            )

            st.plotly_chart(apply_layout(fig_live), use_container_width=True)

        time.sleep(refresh_rate)
        st.rerun()

# ---------------- NORMAL DASHBOARD ----------------
df_filtered = apply_timeframe(df)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Overview", "Indicators", "Models", "Forecast", "Trading"])

# ================= OVERVIEW =================
with tab1:
    st.subheader("Candlestick Chart")

    fig = go.Figure(data=[go.Candlestick(
        x=df_filtered["Date"],
        open=df_filtered["Open"],
        high=df_filtered["High"],
        low=df_filtered["Low"],
        close=df_filtered["Close"]
    )])
    st.plotly_chart(apply_layout(fig), use_container_width=True)

    st.subheader("Moving Averages")
    ma_df = df_filtered.dropna(subset=["MA_20", "MA_50"])
    if not ma_df.empty:
        fig_ma = px.line(ma_df, x="Date", y=["Close", "MA_20", "MA_50"])
        st.plotly_chart(apply_layout(fig_ma), use_container_width=True)

# ================= INDICATORS =================
with tab2:

    st.subheader("Bollinger Bands")
    bb_df = df_filtered.dropna(subset=["BB_Upper", "BB_Lower"])
    if not bb_df.empty:
        fig_bb = px.line(bb_df, x="Date", y=["Close", "BB_Upper", "BB_Lower"])
        st.plotly_chart(apply_layout(fig_bb), use_container_width=True)

    if "RSI" in df.columns:
        st.subheader("RSI")
        fig_rsi = px.line(df_filtered, x="Date", y="RSI")
        st.plotly_chart(apply_layout(fig_rsi), use_container_width=True)

    if "MACD" in df.columns:
        st.subheader("MACD")
        fig_macd = px.line(df_filtered, x="Date", y="MACD")
        st.plotly_chart(apply_layout(fig_macd), use_container_width=True)

# ================= MODELS =================
with tab3:

    st.write("## Model Predictions")

    # -------- RANDOM FOREST --------
    st.subheader("Random Forest")
    try:
        dates_rf, y_rf, pred_rf, rf_metrics = run_rf(df)

        rf_df = pd.DataFrame({
            "Date": dates_rf.values,
            "Actual": y_rf.values,
            "Predicted": pred_rf
        })

        rf_df = apply_timeframe(rf_df)

        if not rf_df.empty:
            fig_rf = px.line(rf_df, x="Date", y=["Actual", "Predicted"])
            st.plotly_chart(apply_layout(fig_rf), use_container_width=True)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("RMSE", round(rf_metrics["RMSE"], 3))
            c2.metric("MAE", round(rf_metrics["MAE"], 3))
            c3.metric("R2", round(rf_metrics["R2"], 3))
            c4.metric("MAPE", round(rf_metrics["MAPE"], 2))

    except Exception as e:
        st.error(f"RF Error: {e}")

    # -------- GRADIENT BOOSTING --------
    st.subheader("Gradient Boosting")
    try:
        dates_gb, y_gb, pred_gb, gb_metrics = run_gb(df)

        gb_df = pd.DataFrame({
            "Date": dates_gb.values,
            "Actual": y_gb.values,
            "Predicted": pred_gb
        })

        gb_df = apply_timeframe(gb_df)

        if not gb_df.empty:
            fig_gb = px.line(gb_df, x="Date", y=["Actual", "Predicted"])
            st.plotly_chart(apply_layout(fig_gb), use_container_width=True)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("RMSE", round(gb_metrics["RMSE"], 3))
            c2.metric("MAE", round(gb_metrics["MAE"], 3))
            c3.metric("R2", round(gb_metrics["R2"], 3))
            c4.metric("MAPE", round(gb_metrics["MAPE"], 2))

    except Exception as e:
        st.error(f"GB Error: {e}")

# ================= FORECAST =================
with tab4:

    st.subheader("Future Prediction")

    days = st.slider("Days", 1, 15, 5)

    try:
        future_df = forecast_rf_advanced(days)

        future_df["Date"] = pd.to_datetime(future_df["Date"])

        fig_future = px.line(future_df, x="Date", y="Predicted Price")
        st.plotly_chart(apply_layout(fig_future), use_container_width=True)

        st.dataframe(future_df)

    except Exception as e:
        st.error(f"Forecast Error: {e}")

# (Only showing Trading section change — rest of your code stays SAME)

# ================= TRADING =================
with tab5:

    st.subheader("📈 Paper Trading (Alpaca)")

    # -------- ACCOUNT --------
    try:
        acc = get_account()

        c1, c2 = st.columns(2)
        c1.metric("Cash", f"${acc['cash']:.2f}")
        c2.metric("Portfolio Value", f"${acc['portfolio_value']:.2f}")

    except Exception as e:
        st.error(f"Account Error: {e}")

    st.markdown("---")

    # -------- SIGNAL --------
    try:
        current_price = df["Close"].iloc[-1]

        future_df = forecast_rf_advanced(1)
        predicted_price = future_df["Predicted Price"].iloc[0]

        # ❌ RSI REMOVED
        signal = generate_signal(current_price, predicted_price)

        st.subheader(f"Signal: {signal}")
        st.write(f"Current: {round(current_price,2)} | Predicted: {round(predicted_price,2)}")

    except Exception as e:
        st.error(f"Signal Error: {e}")
        signal = "HOLD"

    st.markdown("---")

    # -------- EXECUTION --------
    qty = st.number_input("Quantity", min_value=1, value=1)

    if st.button(f"Execute {signal} Order"):
        result = place_order(selected_stock, signal, qty)
        st.success(result)

    # -------- POSITIONS --------
    st.subheader("Open Positions")

    try:
        positions = get_positions()

        if positions:
            st.dataframe(pd.DataFrame(positions))
        else:
            st.write("No open positions")

    except Exception as e:
        st.error(f"Positions Error: {e}")