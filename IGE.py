import pandas as pd
import numpy as np

df = pd.read_csv('IGE.csv', header=0, parse_dates=[0], index_col=0)

# print(df.iat[0,0]) # [row,col]
print(f'Size of dataset = {df.size}')
# print(df.loc['2023-05']) # filter month / year

dailyRet = df[['Adj Close']] # or use .to_frame()
# print(type(dailyRet))
print(f'Number of observations of dailyRet = {dailyRet.size}')
dailyRet = dailyRet.pct_change(periods=1)

excessRet = dailyRet - 0.04/252
print(f'Number of observations of excessRet = {dailyRet.size - 1}')

# print(np.mean(excessRet))
# print(excessRet.mean(axis=0))
# print(np.sum(excessRet) / 251)
# print(excessRet.sum(axis=0) / 251)
avg = excessRet.mean(axis=0)
std = excessRet.std(ddof=0)
# std = excessRet.std()

sharpeRatio = np.sqrt(252) * avg / std
print(f'Sharpe Ratio = {sharpeRatio.values[0]}')