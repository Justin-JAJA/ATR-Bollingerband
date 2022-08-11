#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 10:58:54 2022

@author: justinyen
"""

import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np



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


def ADX(DF, n = 20):
    df = DF.copy()
    df["ATR"] = ATR(df,n)
    df["upmove"] = df["High"]-df["High"].shift(1)
    df["downmove"] = df["Low"].shift(1)-df["Low"]
    df["+dm"] = np.where((df["upmove"]>df["downmove"])& (df["upmove"]>0), df["upmove"],0)
    df["-dm"] = np.where((df["upmove"]<df["downmove"])& (df["downmove"]>0), df["downmove"],0)
    df["+di"] = 100 * (df["+dm"]/df["ATR"]).ewm(com = n, min_periods = n).mean()
    df["-di"] = 100 * (df["-dm"]/df["ATR"]).ewm(com = n, min_periods = n).mean()
    df["ADX"] = 100 * abs((df["+di"]-df["-di"])/(df["+di"]+df["-di"])).ewm(com = n, min_periods = n).mean()
    return df["ADX"]


for tickers in ohlcv:
    ohlcv[tickers]["ADX"] =ADX(ohlcv[tickers],20)
    
plt.style.use( 'ggplot')
plt.subplot(211)
plt.plot(ohlcv["BTC-USD"]["Close"][8914-2000:8914], color = "r" ,linewidth = 3, label = 'BTC Price')       
plt.subplot(212)      
plt.plot(ohlcv["BTC-USD"]["ADX"][8914-2000:8914], color = "y" ,linewidth = 3, label = 'BTC Price')   
plt.axhline(25, color= 'r')
plt.axhline(50, color= 'r')
plt.axhline(75, color= 'r')

    
