#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import yfinance as yf
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

#%%
stocks = ["AMZN","GOOG", "MSFT"]
twn_stock = ["6188.TWO","2915.TW","2104.TW", "6505.TW"]
start =dt.datetime.today()-dt.timedelta(1350)
end = dt.datetime.today()
cl_price = pd.DataFrame()
tw_price = pd.DataFrame()

for ticker in stocks:
    cl_price[ticker] = yf.download(ticker, start, end)["Adj Close"]

for ticker in twn_stock:
    tw_price[ticker] = yf.download(ticker, start, end)["Adj Close"]
###
ohlcv = {}
for ticker in twn_stock:
    ohlcv[ticker] = yf.download(ticker, start, end)

#%%
tw_price.dropna(axis=0, how = "any")

#tw_price.mean()
#tw_price.describe()
#tw_price.head(10)
daily_return = tw_price.pct_change()
daily_return_1 = tw_price/ tw_price.shift(1)-1
daily_return_1.mean()
daily_return_1.std()
##simple moving average
##.rolling(10) only give it operation, it didn't change the data
daily_return_1.rolling(10).mean()
##esponential moving average
daily_return_1.ewm(com =10, min_periods=10).mean()
#%%
tw_price.plot(subplots = True, layout = (2,2),grid = True)
## daily change product
##cumprod = product change from begining to end
daily_return_2 = daily_return_1+1
daily_return_2.cumprod().plot()
#%%
fig, ax = plt.subplots()
plt.style.available
plt.style.use( 'ggplot')
ax.set(title = "taiwan stocks daily", xlabel = "stocks", ylabel = "earn")
plt.bar(x = tw_price.columns, height=daily_return_1.mean(),color = ["red","blue","green","orange"])
plt.bar(x = tw_price.columns, height=daily_return_1.std())

