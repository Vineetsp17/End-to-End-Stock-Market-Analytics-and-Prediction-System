# 📈 Stock Market Analytics Dashboard

A complete Machine Learning based Stock Market Analytics and Forecasting Dashboard built using **Python, Streamlit, Plotly, and Scikit-learn**.

The project provides:
- Interactive stock visualizations
- Technical indicator analysis
- Machine Learning based stock prediction
- Future forecasting
- Live stock market data
- Paper trading integration using Alpaca API

---

# 🚀 Features

## 📊 Interactive Stock Visualization
- Candlestick charts
- Zoomable and movable charts
- Range slider support
- Dynamic timeframe selection:
  - 1 Month
  - 3 Months
  - 6 Months
  - 1 Year
  - All

---

## 📈 Technical Indicators
Implemented indicators include:

### Moving Averages
- 5-Day Moving Average
- 20-Day Moving Average

### Bollinger Bands
- Upper Band
- Lower Band
- Volatility analysis

### RSI (Relative Strength Index)
- Overbought/Oversold detection

### MACD
- MACD line
- Signal line
- Trend momentum analysis

---

## 🤖 Machine Learning Models

### Random Forest Regressor
Used for:
- Stock price prediction
- Trend analysis
- Historical learning

### Gradient Boosting Regressor
Used for:
- Advanced regression forecasting
- Improved generalization
- Sequential boosting prediction

---

## 🔮 Forecasting
- Future stock price forecasting
- Dynamic forecast duration
- Interactive forecast visualization

---

## 📡 Live Market Data
- Real-time stock price fetching
- Finnhub API integration

---

## 💹 Trading Integration
Integrated with Alpaca Paper Trading API:
- Buy orders
- Sell orders
- Portfolio monitoring
- Account information

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend Development |
| Streamlit | Dashboard UI |
| Plotly | Interactive Charts |
| Pandas | Data Processing |
| NumPy | Numerical Computation |
| Scikit-learn | Machine Learning |
| Alpaca API | Trading Integration |
| Finnhub API | Live Market Data |
| Alpha Vantage API | Historical Stock Data |
| MarketStack API | Long-term Stock Data |

---

# 📂 Project Structure

```text
stock_analytics_project/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── raw_stock_data.csv
│   └── processed_stock_data.csv
│
├── src/
│   ├── data_collection.py
│   ├── preprocessing.py
│   ├── indicators.py
│   ├── forecasting.py
│   ├── live_data.py
│   ├── trading.py
│   ├── model_rf.py
│   └── model_gb.py
│
├── assets/
│
└── .streamlit/
    └── config.toml
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone YOUR_GITHUB_REPO_LINK
cd stock_analytics_project
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 API Configuration

Create a `.env` file in project root.

Example:

```env
ALPHA_VANTAGE_API_KEY=your_alpha_key
FINNHUB_API_KEY=your_finnhub_key
MARKETSTACK_API_KEY=your_marketstack_key

ALPACA_API_KEY=your_alpaca_api_key
ALPACA_SECRET_KEY=your_alpaca_secret_key
```

---

# ▶️ Running the Application

Run:

```bash
streamlit run app.py
```

Application opens at:

```text
http://localhost:8501
```

---

# 📥 Data Collection

To rebuild stock dataset:

```bash
python -m src.data_collection
```

This fetches:
- Alpha Vantage Data
- Finnhub Data
- MarketStack Data

And generates:
- `raw_stock_data.csv`

---

# 🧹 Data Preprocessing

Run preprocessing:

```bash
python -m src.preprocessing
```

Generates:
- `processed_stock_data.csv`

---

# 📊 Dashboard Tabs

## 1️⃣ Overview Tab
Contains:
- Candlestick chart
- Volume visualization
- Moving averages
- Interactive timeframe controls

---

## 2️⃣ Indicators Tab
Contains:
- Bollinger Bands
- RSI
- MACD

---

## 3️⃣ Models Tab
Contains:
- Random Forest Predictions
- Gradient Boosting Predictions
- Actual vs Predicted visualization
- RMSE, MAE, R², MAPE metrics
- Model comparison chart

---

## 4️⃣ Forecast Tab
Contains:
- Future stock prediction
- Forecast visualization
- Forecast table

---

# 📈 Evaluation Metrics

The following metrics are used:

| Metric | Description |
|---|---|
| RMSE | Root Mean Square Error |
| MAE | Mean Absolute Error |
| R² | Coefficient of Determination |
| MAPE | Mean Absolute Percentage Error |

---

# ☁️ Streamlit Cloud Deployment

## 1️⃣ Push Project to GitHub

```bash
git init
git add .
git commit -m "Initial Commit"
git branch -M main
git remote add origin YOUR_REPO_LINK
git push -u origin main
```

---

## 2️⃣ Open Streamlit Cloud

https://share.streamlit.io

---

## 3️⃣ Create New App

Fill:
- Repository
- Branch = `main`
- Main file = `app.py`

---

## 4️⃣ Add Secrets

In Streamlit Cloud:

```toml
ALPHA_VANTAGE_API_KEY="your_key"
FINNHUB_API_KEY="your_key"
MARKETSTACK_API_KEY="your_key"

ALPACA_API_KEY="your_key"
ALPACA_SECRET_KEY="your_key"
```

---

# 🔒 Security Features

- API keys stored using `.env`
- Secrets hidden from GitHub
- `.gitignore` protection
- Secure Streamlit Cloud Secrets integration

---

# 🚧 Challenges Faced

- API rate limits
- Timezone inconsistencies
- Model overfitting
- Streamlit rendering issues
- Interactive chart synchronization
- Forecast visualization stability

---

# 🚀 Future Enhancements

- LSTM Deep Learning Models
- Sentiment Analysis Integration
- Buy/Sell Signal Automation
- Portfolio Optimization
- Cryptocurrency Support
- Real-time Notifications

---

# 📸 Screenshots

## Dashboard Overview
(Add screenshot here)

## Technical Indicators
(Add screenshot here)

## Model Predictions
(Add screenshot here)

## Forecasting
(Add screenshot here)

---

# 👨‍💻 Author

**Vineet Peerapur**  
Electronics and Communication Engineering  
KLE Technological University, Hubli

---

# 📄 License

This project is developed for academic and educational purposes.

---

# ⭐ Acknowledgements

- Streamlit
- Plotly
- Scikit-learn
- Finnhub API
- Alpha Vantage API
- Alpaca API
- MarketStack API# End-to-End-Stock-Market-Analytics-and-Prediction-System
