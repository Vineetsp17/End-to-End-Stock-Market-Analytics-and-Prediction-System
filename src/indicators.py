import pandas as pd

def add_indicators(df):

    # RSI
    delta = df['Close'].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = -delta.clip(upper=0).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # MACD
    exp1 = df['Close'].ewm(span=12).mean()
    exp2 = df['Close'].ewm(span=26).mean()
    df['MACD'] = exp1 - exp2

    # Bollinger Bands
    df['BB_Middle'] = df['Close'].rolling(20).mean()
    df['BB_Upper'] = df['BB_Middle'] + 2 * df['Close'].rolling(20).std()
    df['BB_Lower'] = df['BB_Middle'] - 2 * df['Close'].rolling(20).std()

    return df