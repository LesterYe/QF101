import pandas as pd
import numpy as np


df_ige = pd.read_csv("data/IGE.csv")
df_ige["Adj Close Prev Period"] = df_ige["Adj Close"].shift(1)
df_ige["Dailyret"] = (df_ige["Adj Close"] - df_ige["Adj Close Prev Period"])/df_ige["Adj Close Prev Period"]

def calculate_drawdown(df_dailyret):
    temp = [None, df_dailyret["Dailyret"][1]]
    for x in range(2, len(df_dailyret["Dailyret"])):
        temp.append(((1 + temp[-1]) * (1 + df_dailyret["Dailyret"][x])) -1)
    df_dailyret["Cumulative return"] = temp
    df_dailyret["Cumulative return-1"] = df_dailyret["Cumulative return"].shift(1)
    df_dailyret["High Watermark"] = df_dailyret[["Cumulative return", "Cumulative return-1"]].max(axis=1)
    df_dailyret["Drawdown"] = ((1 + df_dailyret["Cumulative return"]) / (1 + df_dailyret["High Watermark"])) -1
    drawdown_duration = [0, ]
    counter = 0
    for x in range(1, len(df_dailyret["Drawdown"])):
        if df_dailyret["Drawdown"][x] == 0:
            counter = 0 
        else:
            counter += 1
        drawdown_duration.append(counter)
    df_dailyret["Max Drawdown Duration"] = drawdown_duration

    max_drawdown = - df_dailyret["Drawdown"].min()
    max_drawdown_duration = df_dailyret["Max Drawdown Duration"].max()

    return max_drawdown, max_drawdown_duration

max_drawdown, max_drawdown_duration = calculate_drawdown(df_ige[["Dailyret"]])

print("Max drawdown: ", max_drawdown)
print("Max drawdown Duration: ", max_drawdown_duration)

