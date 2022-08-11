#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 11:27:07 2022

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


def RSI (DF, n= 14):
    df = DF.copy()
    df["change"] = df["Adj Close"] - df["Adj Close"].shift(1)
    df["gain"] = np.where(df["change"]>=0,df["change"],0)
    df["loss"] = np.where(df["change"]<0,-1*df["change"],0)
    df["avg gain"] = df["gain"].ewm(alpha = 1/n, min_periods = n).mean()
    df["avg loss"] = df["loss"].ewm(alpha = 1/n, min_periods = n).mean()
    df["rs"] =  df["avg gain"]/ df["avg loss"]
    df["RSI"] = 100 - (100/(1+df["rs"]))
    return df["RSI"]

for tickers in ohlcv:
    ohlcv[tickers]["RSI"] =RSI(ohlcv[tickers],14) 
    

fig, ax = plt.subplots(2,1,figsize =(16,9) )
#plt.style.available
plt.style.use( 'ggplot')
plt.subplot(211)
plt.plot(ohlcv["BTC-USD"]["Close"][:1000], color = "r" ,linewidth = 3, label = 'BTC Price')       
plt.subplot(212)      
plt.plot(ohlcv["BTC-USD"]["RSI"][:1000], color = "y" ,linewidth = 3, label = 'BTC Price')   
plt.axhline(70, color= 'r')
plt.axhline(30, color= 'r')



          
ax.set(title = "boll_band", xlabel = "date", ylabel = "price")
