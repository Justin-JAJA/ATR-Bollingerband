#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 14:28:09 2022

@author: justinyen
"""
import pandas as pd
from yahoofinancials import YahooFinancials
import datetime as dt
import matplotlib as mlt


twn_stock = ["6188.TWO","2915.TW","2104.TW", "6505.TW"]
stock = "6188.TWO"

yahoo = YahooFinancials(twn_stock)
data = yahoo.get_historical_price_data("2020-01-28", "2022-01-28" , "daily")
start =(dt.datetime.today()-dt.timedelta(1825)).strftime("%Y-%m-%d")
end = (dt.datetime.today().strftime)("%Y-%m-%d")
close_prices = pd.DataFrame()

for ticker in twn_stock:
    yahoo = YahooFinancials(ticker)
    json_obj = data = yahoo.get_historical_price_data(start, end , "daily")
    ohlv = json_obj[ticker]["prices"]
    temp = pd.DataFrame(ohlv)[["formatted_date", "adjclose"]]
    temp.set_index("formatted_date", inplace=True)
    temp.dropna(inplace=True)
    close_prices[ticker] = temp["adjclose"]
    

mlt.window()