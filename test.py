import os
import glob
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from statistics import correlation

minding_sid_list = [
    "2330.TW",
    "2382.TW",
    "2618.TW",
    "5274.TWO",
    "3443.TW",
    "2454.TW"
]

DATE_FORMAT = "%Y-%m-%d"

homepath = os.path.expanduser("~")
basedir = os.path.join(homepath, "Downloads", "Major-Chip-data")
output_report = os.path.join(homepath, "Downloads", "Major-Chip-data", "analysis.xlsx")

# Define a custom sorting function that extracts the numeric part of the week string
def extract_week_number(week: str):
    return int(week.split()[1])

def get_sid_weekly_buy_from_csv_files(csv_files:str) -> pd.DataFrame:
    corp_buy = pd.DataFrame()
    for i, csv in enumerate(csv_files):
        df = pd.read_csv(csv)
        if any(["Unnamed" in col for col in df.columns]):
            df = df.iloc[:, 1:]
        data = np.concatenate([df.iloc[:,:4].values, df.iloc[:,4:].values])
        df = pd.DataFrame(data, columns=df.columns[0:4])
        buy = (df.iloc[:, -1].replace(",", "", regex=True).astype(float))
        buy.name = i
        buy.index = df.iloc[:, 0]
        corp_buy = pd.concat([corp_buy, buy], axis=1)
        
    corp_buy = corp_buy.fillna(0)
    # remove rows with empty index
    corp_buy = corp_buy[corp_buy.index.notnull()] 
    corp_buy = corp_buy.transpose()
    corp_buy.index = get_dates_from_filenames(csv_files)
    return corp_buy

def get_sid_price_change(sid:str, start:str, end:str, timeout=15) -> pd.Series:
    period = check_period([start, end])
    stock_data = yf.download(sid, start=period[0], end=period[-1], timeout=timeout)
    if len(stock_data)==0:
        raise ValueError(f"Failed to download sid {sid} data from "\
                         f"{period[0]} to {period[-1]} after {timeout}s timeout")

    price_change = stock_data['Close'].pct_change()*100
    price_change.index = [idx.date().strftime(DATE_FORMAT) for idx in price_change.index]
    # since the first day is inserted in runtime to be able 
    # to calculate the price change of the first day in a period, 
    # ignore the first day to remove the inserted date calculation
    return price_change[1:]

def get_dates_from_filenames(filenames:list) -> list:
    dates = [os.path.dirname(f).split("/")[-1] for f in filenames]
    dates = [datetime.strptime(d, DATE_FORMAT).strftime(DATE_FORMAT) for d in dates]
    dates = sorted(dates, key=lambda x: datetime.strptime(x, DATE_FORMAT))
    return dates

def check_period(dates:list) -> list:
    # insert a date at the beginning of the dates to be able to calculate the 
    # price change of the first day comparing with last day
    date = datetime.strptime(dates[0], DATE_FORMAT)
    if date.weekday() == 0: # 0 correspond to Monday
        insert_date = date - timedelta(days=3) # insert last friday
    else:
        insert_date = date - timedelta(days=1) # insert last day
    dates.insert(0, insert_date.strftime(DATE_FORMAT))

    # insert a date at the end of the dates to be able to get the 
    # complete data of a period
    date = datetime.strptime(dates[-1], DATE_FORMAT)
    insert_date = date + timedelta(days=1)
    dates.append(insert_date.strftime(DATE_FORMAT))
    return dates

def calculate_correlation(df:pd.DataFrame, y:pd.Series) -> pd.DataFrame:
    corr = list()
    for col_name, col in df.items():
        if len(set(col.to_list()))==1: # check if the inputs are constant.
            corr.append([col_name, "Error"])
        else:
            corr.append([col_name, round(correlation(col.to_list(), y), 4)])
  
    return pd.DataFrame(corr)

if  __name__ == '__main__':
    # remove the output report if exists
    if os.path.exists(output_report):
        os.remove(output_report)

    weeks = [d for d in os.listdir(basedir) if os.path.isdir(os.path.join(basedir, d))]
    weeks = sorted(weeks, key=extract_week_number)

    writer = pd.ExcelWriter(output_report)
    
    for sid in minding_sid_list:
        history_corr = pd.DataFrame()
        for week in weeks:
            try:
                # get all csv files in week folder
                path = os.path.join(basedir, week)
                csv_files = glob.glob(path + f'/**/{sid}.csv')
                if len(csv_files)==0:
                    # if failed, try to get csv files by remove the suffix
                    csv_files = glob.glob(path + f'/**/{sid.split(".")[0]}.csv')
                if len(csv_files)==0:
                    continue

                dates = get_dates_from_filenames(csv_files)
                sid_weekly_buy = get_sid_weekly_buy_from_csv_files(csv_files)
                price_change = get_sid_price_change(sid, start=dates[0], end=dates[-1])
                if len(sid_weekly_buy)!=len(price_change):
                    print(f"The number of files in {week} does not "
                          f"match the valid number of price change days "
                          f"of stock {sid} in the period {dates[0]} to {dates[-1]}. "
                          f"Unmatched dates will be automatically truncated.")
                
                # find the intersection dates and truncate the data and 
                # remove columns that only contains zeros
                intersection = set(sid_weekly_buy.index).intersection(price_change.index)
                intersection = list(intersection)
                sid_weekly_buy = sid_weekly_buy.loc[intersection]
                sid_weekly_buy = sid_weekly_buy.loc[:, (sid_weekly_buy != 0).any(axis=0)]
                price_change = price_change.loc[intersection]

                # calculate the correlation of weekly buy and price change
                corr = calculate_correlation(sid_weekly_buy, price_change)
                corr.columns = [f"{week} Corp", f"{week} Corr"]
                history_corr = pd.concat([history_corr, corr], axis=1)
                history_corr.insert(history_corr.shape[-1], history_corr.shape[-1], "")
            except Exception as e:
                print(e)

        try:
            history_corr = history_corr.fillna("")
            history_corr.to_excel(writer, sheet_name=str(sid), index=False)

            # auto-adjust columns' width
            for col in history_corr:
                col_width = max(history_corr[col].astype(str).map(len).max(), len(str(col)))
                if col_width < 10: col_width=10
                col_idx = history_corr.columns.get_loc(col)
                writer.sheets[str(sid)].set_column(col_idx, col_idx, col_width)
        except Exception as e:
            print(e)
    writer.close()