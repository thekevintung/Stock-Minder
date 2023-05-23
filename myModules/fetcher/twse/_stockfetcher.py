import os
import sys
import json
import requests
import pandas as pd
import yfinance as yf
from collections import OrderedDict
from myModules.fetcher import BaseFetcher

MARKET_URLS = {
    'twse': 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=2',
    'tpex': 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=4'
}

def get_cwd():
    # sys._MEIPASS is the path of a temporary folder created by PyInstaller 
    # when it bundles a Python application into a standalone executable.
    if hasattr(sys, "_MEIPASS"):
        # run as a script bundled by PyInstaller
        cwd = sys._MEIPASS
    else:
        # run as a script
        cwd = os.path.dirname(__file__)
    return cwd

class StockFetcher(BaseFetcher):
    def __init__(self, update:bool=False) -> None:
        if update: self.update()
    
    def fetch_data(self, url:str):
        response = requests.get(url, timeout=30)
        df = pd.read_html(response.text, header=0)[0]
        
        # remove fist row and last column, since them are useless
        df = df.iloc[1:,:].drop(columns=df.columns[-1])

        df.insert(0, "", "")
        df.columns = ["code", "name", "ISIN", "start", "market", "group", "CFI"]

        # split the codes and names based on the \u3000 delimiter
        df[["code", "name"]] = df.iloc[:,1].str.split('\u3000', expand=True)

        # remove invalid rows
        mask = df["code"].str.contains("[0-9a-zA-Z]+")
        return df[mask]
    
    def update(self):
        for market, url in MARKET_URLS.items():
            try:
                df = self.fetch_data(url)
                df.to_json(os.path.join(get_cwd(), f"{market}.json"))
            except:
                pass

    def get_market_data_from_json(self, file:str) -> OrderedDict:
        try:
            with open(file, "r") as f:
                data = OrderedDict(json.load(f))
            return data
        except:
            self.update()
            return self.get_market_data_from_json(file)

    def get_all_markets(self):
        return list(MARKET_URLS.keys())

    def get_all_stock_id(self, market:str) -> OrderedDict:
        file = os.path.join(get_cwd(), f"{market}.json")
        data = self.get_market_data_from_json(file)
        return OrderedDict(zip(data["name"].values(), data["code"].values()))
    
    def get_stock_dividend_info(self, stock_id) -> OrderedDict:
        ticker = yf.Ticker(f"{stock_id}.TW")
        dividend_data = ticker.dividends.tail(6)
        dividend_info = OrderedDict()
        for timestamp, cash in dividend_data.items():
            dividend_info[timestamp.strftime('%Y-%m-%d')] = cash
        return dividend_info
       
    
    def get_two_dividend_history(self, start_date: str, end_date: str):
        # parse YYYYMMDD to YYY/MM/DD
        start_date = f"{int(start_date[:4])-1911}/{start_date[4:6]}/{start_date[6:]}"
        end_date = f"{int(end_date[:4])-1911}/{end_date[4:6]}/{end_date[6:]}"
        url = f"https://www.tpex.org.tw/web/stock/exright/dailyquo/exDailyQ_result.php?l=zh-tw&d={start_date}&ed={end_date}"
        
        dividend_history_columns = [
            "除權息日期",
            "代號",
            "名稱",
            "除權息前收盤價",
            "除權息參考價",
            "權值",
            "息值",
            "權值+息值",
            "權/息",
            "漲停價",
            "跌停價",
            "開始交易基準價",
            "減除股利參考價",
            "現金股利",
            "每仟股無償配股",
            "現金增資股數",
            "現金增資認購價",
            "公開承銷股數",
            "員工認購股數",
            "原股東認購股數",
            "按持股比例仟股認購",
        ]
        res = requests.get(url)
        dividend_history = pd.DataFrame(
            res.json()["aaData"], columns=dividend_history_columns
        )
        return dividend_history
       
    