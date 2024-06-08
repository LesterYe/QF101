import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
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

cumRet = excessRet.copy(deep=True)
cumRet += 1
cumRet = cumRet.cumprod(axis='index')
cumRet -= 1
cumRet.dropna(inplace=True)
# print(cumRet)
# excessRet.plot(kind='kde')
# excessRet.hist()
# cumRet.plot()
# plt.show()

highWaterMark = cumRet * 0
drawdown = cumRet * 0
drawdownDuration = cumRet * 0

# print(highWaterMark.iat[1,0]) # [row,col]

for t in range(1, num_obs-1):
  highWaterMark.iat[t,0] = max(highWaterMark.iat[t-1,0], cumRet.iat[t,0])
  # print(t, highWaterMark.iat[t,0])
  drawdown.iat[t,0] = (1 + highWaterMark.iat[t,0]) / (1 + cumRet.iat[t,0]) - 1
  if (drawdown.iat[t,0] == 0):
    drawdownDuration.iat[t,0] = 0
  else:
    drawdownDuration.iat[t,0] = drawdownDuration.iat[t-1,0] + 1

  # if t == 200:
  #   break

# print(highWaterMark.head(10))

maxDD = drawdown.max()
print(f'Maximum Drawdown = {maxDD.values[0]}')

maxDDD = drawdownDuration.max()
print(f'Maximum Drawdown Duration = {maxDDD.values[0]}')

# print(drawdown)
# print(drawdownDuration)