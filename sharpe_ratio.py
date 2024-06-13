import pandas as pd
import numpy as np


risk_free_rate = 0.04

df_ige = pd.read_csv("data/IGE.csv")

# set trading period to number of observation
trading_period = df_ige.shape[0]

def sharpe_ratio(df_adjclosing, risk_free_rate, trading_period):
    df_adjclosing["Adj Close Prev Period"] = df_adjclosing["Adj Close"].shift(1)
    df_adjclosing["Dailyret"] = (df_adjclosing["Adj Close"] - df_adjclosing["Adj Close Prev Period"])/df_adjclosing["Adj Close Prev Period"]
    df_adjclosing["Excess Dailyret"] = df_adjclosing["Dailyret"] - (risk_free_rate/trading_period)
    
    # remove first value since it will be NA
    excess_dailyret = df_adjclosing["Excess Dailyret"][1:]
    return np.sqrt(trading_period) * np.average(excess_dailyret) / np.std(excess_dailyret)

print("sharpe_ratio: ", sharpe_ratio(df_ige[["Adj Close"]], risk_free_rate, trading_period))
