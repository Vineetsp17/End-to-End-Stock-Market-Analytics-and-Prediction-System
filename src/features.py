import pandas as pd

def add_advanced_features(df):

    print("Adding advanced features...")

    df['Lag_1'] = df['Close'].shift(1)
    df['Lag_2'] = df['Close'].shift(2)
    df['Lag_3'] = df['Close'].shift(3)

    df['Rolling_Mean_5'] = df['Close'].rolling(5).mean()
    df['Rolling_Mean_10'] = df['Close'].rolling(10).mean()

    df['Rolling_Std_5'] = df['Close'].rolling(5).std()

    return df