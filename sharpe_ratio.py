import pandas as pd
import numpy as np

def create_daily_returns(adjCls):
  # dailyRet = adjCls.pct_change(periods=1)

  # alternative method
  firstDiff = adjCls.diff(periods=1)
  dailyRet = firstDiff / adjCls.shift(periods=1)
  # compare_df = dailyRet2 - dailyRet
  # print(compare_df.sum())

  return dailyRet

def create_excess_returns(dailyRet, rfr, num_obs):
  excessRet = dailyRet - rfr/num_obs

  return excessRet

def calculate_sharpe_ratio(excessRet, num_obs):
  # print(np.mean(excessRet))
  # print(excessRet.mean(axis=0))
  # print(np.sum(excessRet) / 251)
  # print(excessRet.sum(axis=0) / 251)
  avg = excessRet.mean(axis=0)
  std = excessRet.std(ddof=0)
  # std = excessRet.std(ddof=1) # degree of freedom?
  sharpe_ratio = np.sqrt(num_obs) * avg / std

  return sharpe_ratio.values[0]

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

#==================== Calculate sharpe ratio ====================#
sharpe_ratio = calculate_sharpe_ratio(excessRet, num_obs)
print(f'Sharpe Ratio = {sharpe_ratio}')
