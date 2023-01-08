import os
import pandas as pd


class TTMScanner:
    def __init__(self, ma_period, m):
        self.ma_period = ma_period
        self.m = m

    def _calculate_indicators(self, df):
        """Assumes df is a DataFrame with 4 columns,
        Open, High, Low, Close"""
        ma_period, m = self.ma_period, self.m

        # statistics required to calculate indicators
        df["sma"] = df["Close"].rolling(window=ma_period).mean()
        df["ema"] = df["Close"].ewm(span=ma_period).mean()
        df["typical_price"] = (df["Close"] + df["High"] + df["Low"]) / 3
        df["std"] = df["typical_price"].rolling(window=ma_period).std()
        df["atr"] = (df["High"] - df["Low"]).rolling(window=ma_period).mean()

        # bolinger bands
        df["upper_bb"] = df["sma"] + m * df["std"]
        df["lower_bb"] = df["sma"] - m * df["std"]

        # keltner channels
        df["upper_kc"] = df["ema"] + m * df["atr"]
        df["lower_kc"] = df["ema"] - m * df["atr"]

        # determine if in squeeze
        data["in_squeeze"] = data.apply(
            lambda x: x["lower_bb"] > x["lower_kc"] and x["upper_bb"] < x["upper_kc"],
            axis=1,
        )

        return df

    def _break_out(self, df):
        df = _calculate_indicators(df)
        if df.iloc[-2]["in_squeeze"] and not df.iloc[-1]["in_squeeze"]:
            return True
