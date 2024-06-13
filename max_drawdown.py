import pandas as pd
import numpy as np


trading_period = 252
risk_free_rate = 0.04

df_ige = pd.read_csv("data/IGE.csv")

def calculate_drawdown(df_adjclosing, risk_free_rate, trading_period):
    df_adjclosing["Adj Close Prev Period"] = df_adjclosing["Adj Close"].shift(1)
    df_adjclosing["Dailyret"] = (df_adjclosing["Adj Close"] - df_adjclosing["Adj Close Prev Period"])/df_adjclosing["Adj Close Prev Period"]

    temp = [None, df_adjclosing["Dailyret"][1]]
    for x in range(2, len(df_adjclosing["Dailyret"])):
        temp.append(((1 + temp[-1]) * (1 + df_adjclosing["Dailyret"][x])) -1)
    df_adjclosing["Cumulative return"] = temp
    df_adjclosing["Cumulative return-1"] = df_adjclosing["Cumulative return"].shift(1)
    df_adjclosing["High Watermark"] = df_adjclosing[["Cumulative return", "Cumulative return-1"]].max(axis=1)
    df_adjclosing["Drawdown"] = ((1 + df_adjclosing["Cumulative return"]) / (1 + df_adjclosing["High Watermark"])) -1
    drawdown_duration = [0, ]
    counter = 0
    for x in range(1, len(df_adjclosing["Drawdown"])):
        if df_adjclosing["Drawdown"][x] == 0:
            counter = 0 
        else:
            counter += 1
        drawdown_duration.append(counter)
    df_adjclosing["Max Drawdown Duration"] = drawdown_duration

    max_drawdown = - df_adjclosing["Drawdown"].min()
    max_drawdown_duration = df_adjclosing["Max Drawdown Duration"].max()

    return max_drawdown, max_drawdown_duration

max_drawdown, max_drawdown_duration = calculate_drawdown(df_ige[["Adj Close"]], risk_free_rate, trading_period)

print("Max drawdown: ", max_drawdown)
print("Max drawdown Duration: ", max_drawdown_duration)

