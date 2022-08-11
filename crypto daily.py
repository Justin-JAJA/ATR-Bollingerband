#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 23:09:03 2022

@author: justinyen
"""


import yfinance as yf
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
cryptocurrency= ["BTC-USD","ETH-USD","SOL-USD","SAND-USD",
                 "ADA-USD","LINK-USD","LUNA1-USD","DOT-USD"]
cr_start =dt.datetime.today()-dt.timedelta(70)
cr_end = dt.datetime.today()
crypto_price = pd.DataFrame()


for ticker in cryptocurrency:
    crypto_price[ticker] = yf.download(ticker, cr_start, cr_end)["Adj Close"]
cr_daily_percentile = round(crypto_price/ crypto_price.shift(1)*100-100,2)
#%%
fig, ax = plt.subplots()
#plt.style.available
plt.style.use( 'ggplot')
ax.set(title = "crypto daily", xlabel = "crypto", ylabel = "standard deviation")
##mean of how much it drop everday 
cr_daily_percentile.mean().plot(kind = "bar")
## std of daily changes
cr_daily_percentile.std().plot(kind = "bar")
## how much i loss
cr_daily = 1+(round(crypto_price/ crypto_price.shift(1)*100-100,2))/100
cr_daily.cumprod().plot()



