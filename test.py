import os
import glob
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from statistics import correlation

minding_sid_list = [
    2330,
    2382,
    2618,
    5274,
    3443,
    2454
]

basedir = "/home/kevin/Downloads/Minder-data"

def get_sid_weekly_buy(sid:int, week:str) -> pd.DataFrame:
    csv_files = glob.glob(os.path.join(basedir, week) + f'/**/{sid}.csv')
    if not len(csv_files): return None
    
    corp_buy = pd.DataFrame()
    for csv in csv_files:
        df = pd.read_csv(csv)
        if any(["Unnamed" in col for col in df.columns]):
            df = df.iloc[:, 1:]
        data = np.concatenate([df.iloc[:,:4].values, df.iloc[:,4:].values])
        df = pd.DataFrame(data, columns=df.columns[0:4])
        buy = df.iloc[:, -1].replace(",", "", regex=True).astype(float)
        buy.index = df.iloc[:, 0]
        buy.name = "Buy"
        corp_buy = pd.concat([corp_buy, buy], axis=1)
        
    corp_buy = corp_buy.transpose()
    corp_buy.index = get_dates_from_filenames(csv_files)
    return corp_buy

def get_dates_from_filenames(filenames:list) -> list:
    dates = [os.path.dirname(f).split("/")[-1] for f in filenames]
    dates = [datetime.strptime(d, "%Y-%m-%d").strftime("%Y-%m-%d") for d in dates]
    dates = sorted(dates, key=lambda x: datetime.strptime(x, "%Y-%m-%d"))
    return dates

def check_period(dates:list) -> list:
    # insert a date at the beginning of the dates to be able to calculate the 
    # price change of the first day comparing with last day
    date = datetime.strptime(dates[0], "%Y-%m-%d")
    if date.weekday() == 0: # 0 correspond to Monday
        insert_date = date - timedelta(days=3) # insert last friday
    else:
        insert_date = date - timedelta(days=1) # insert last day
    dates.insert(0, insert_date.strftime("%Y-%m-%d"))

    # insert a date at the end of the dates to be able to get the 
    # complete data of a period
    date = datetime.strptime(dates[-1], "%Y-%m-%d")
    insert_date = date + timedelta(days=1)
    dates.append(insert_date.strftime("%Y-%m-%d"))
    return dates

def get_sid_price_change(sid:int, start:str, end:str) -> pd.Series:
    ticker = f"{sid}.TW"
    period = check_period([start, end])
    stock_data = yf.download(ticker, start=period[0], end=period[-1])

    price_change = stock_data['Close'].pct_change()*100
    # since the first day is inserted in runtime to be able 
    # to calculate the price change of the first day in a period, 
    # ignore the first day to remove the inserted date calculation
    return price_change[1:]

def calculate_correlation(df:pd.DataFrame, y:pd.Series):
    if len(set(df.iloc[:,0].to_list()))==1 or len(set(y.to_list()))==1:
        raise ValueError("The inputs need to be constant.")

    corr = pd.Series()
    for col_name, col in df.items():
        corr[col_name] = correlation(col.to_list(), y)
    return corr

if  __name__ == '__main__':
    for sid in minding_sid_list:
        for week in os.listdir(basedir):
            csv_files = glob.glob(os.path.join(basedir, week) + f'/**/{sid}.csv')
            dates = get_dates_from_filenames(csv_files)
            sid_weekly_buy = get_sid_weekly_buy(sid, week)
            price_change = get_sid_price_change(sid, start=dates[0], end=dates[-1])
            if len(sid_weekly_buy)!=len(price_change):
                raise ValueError(f"The number of files in {week} does not "
                                 f"match the valid number of price change days "
                                 f"in the period {dates[0]} to {dates[-1]}.")
            
            
            correlations = calculate_correlation(sid_weekly_buy, price_change)
     