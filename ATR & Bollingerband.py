#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 13:46:16 2022

@author: justinyen
"""

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

cryptocurrency= ["BTC-USD","ETH-USD","SOL-USD","SAND-USD",
                 "ADA-USD","LINK-USD","LUNA1-USD","DOT-USD"]
ohlcv = {}

for ticker in cryptocurrency:
    temp = yf.download(ticker, period="1mo", interval="5m")
    temp.dropna(how="any",inplace = True)
    ohlcv[ticker] = temp



def ATR(DF, n = 14):
    df = DF.copy()
    df["H-L"] = df["High"] - df["Low"]
    df["H-PC"] = df["High"] - df["Adj Close"].shift(1)
    df["L-PC"] = df["Low"] - df["Adj Close"].shift(1)
    df["TR"] = df[["H-L","H-PC","L-PC"]].max(axis = 1, skipna = False)
    df["ATR"] = df["TR"].ewm(com = n, min_periods = n).mean()
    return df["ATR"]


def Boll_band(DF, n = 14):
    df = DF.copy()
    df["MB"] = df["Adj Close"].rolling(n).mean()
    df["UB"] = df["MB"] + 2*df["Adj Close"].rolling(n).std(ddof = 0)
    df["LB"] = df["MB"] - 2*df["Adj Close"].rolling(n).std(ddof = 0)
    df["BB_Width"] = df["UB"] - df["LB"]
    return df[["MB","UB", "LB", "BB_Width"]]

for ticker in ohlcv:
    ohlcv[ticker]["ATR"] = ATR(ohlcv[ticker])
    ohlcv[ticker][["MB","UB", "LB", "BB_Width"]] = Boll_band(ohlcv[ticker], 20)
    
fig, ax = plt.subplots(figsize =(24,9) )
plt.style.available
plt.style.use( 'ggplot')
ax.set(title = "boll_band", xlabel = "date", ylabel = "price")
line1, = plt.plot(ohlcv["BTC-USD"]["Close"][:1000], color = "r" ,linewidth = 3, label = 'BTC Price')             
line2, = plt.plot(ohlcv["BTC-USD"]["UB"][:1000], color = "g" ,linewidth = 3, label = 'UB') 
line3, = plt.plot(ohlcv["BTC-USD"]["LB"][:1000], color = "b" ,linewidth = 3, label = 'LB') 
plt.legend(handles = [line1, line2, line3], loc='upper right')


fig, ax = plt.subplots(figsize =(24,9) )
plt.style.available
plt.style.use( 'ggplot')
ax.set(title = "boll_band", xlabel = "date", ylabel = "price")
#line1, = plt.plot(ohlcv["BTC-USD"]["Close"], color = "r" ,linewidth = 3, label = 'BTC Price')             
line2, = plt.plot(ohlcv["BTC-USD"]["ATR"][:1000], color = "g" ,linewidth = 3, label = 'UB') 
#line3, = plt.plot(ohlcv["BTC-USD"]["LB"], color = "b" ,linewidth = 3, label = 'LB') 
#plt.legend(handles = [line1, line2, line3], loc='upper right')

#plt.bar(x = tw_price.columns, height=daily_return_1.mean(),color = ["red","blue","green","orange"])
#plt.bar(x = tw_price.columns, height=daily_return_1.std())
    