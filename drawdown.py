import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sharpe_ratio import create_daily_returns, create_excess_returns

def calculateMaxDD(cumRet):
  pass

#==================== EDA ====================#
df = pd.read_csv('IGE.csv', header=0, parse_dates=[0], index_col=0)
# print(df.iat[0,0]) # [row,col]
# print(df.loc['2023-05']) # filter month / year
print(f'Size of dataset = {df.size}')
num_obs = df.shape[0]

#==================== Create daily returns dataset ====================#
adjCls = df[['Adj Close']] # or use .to_frame()
dailyRet = create_daily_returns(adjCls)
print(f'Number of observations of dailyRet = {num_obs - 1}')
# print(type(dailyRet))

#==================== Create excess returns dataset ====================#
rfr = 0.04
excessRet = create_excess_returns(dailyRet, rfr, num_obs)
print(f'Number of observations of excessRet = {num_obs - 1}')

cumRet = excessRet
cumRet += 1
cumRet = cumRet.cumprod(axis='index')
cumRet -= 1
plot = cumRet.plot()