#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 17:37:17 2022

@author: justinyen
"""

import yfinance as yf
import pandas as pd

cryptocurrency= ["BTC-USD","ETH-USD","SOL-USD","SAND-USD",
                 "ADA-USD","LINK-USD","LUNA1-USD","DOT-USD"]
ohlcv = {}

for ticker in cryptocurrency:
    temp = yf.download(ticker, period="1mo", interval="15m")
    temp.dropna(how="any",inplace = True)
    ohlcv[ticker] = temp
    
    
def MACD(DF, a=12, b = 26, c=9):
    df = DF.copy()
    df["ma_fast"] = df["Adj Close"].ewm(span = a, min_periods = a).mean()
    df["ma_slow"] = df["Adj Close"].ewm(span = b, min_periods = b).mean()
    df["MACD"] = df["ma_fast"] -df["ma_slow"]
    df["signal"] = df["MACD"].ewm(span = c, min_periods = c).mean()
    return df.loc[:,["MACD","signal"]]

for ticker in ohlcv:
    ohlcv[ticker][["MACD", "SIGNAL"]] = MACD(ohlcv[ticker])