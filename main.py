import os
import schedule
import time
from datetime import datetime
from myModules.fetcher import FinanceInfo, YhaooTWStockFetcher

minding_sid_list = [
    2330,
    2382,
    2618,
    5274,
    3443,
    2454
]

def get_chip_major():
    fetcher = YhaooTWStockFetcher()
    today = datetime.now().date().strftime("%Y-%m-%d")
    homepath = os.path.expanduser("~")
    basedir = os.path.join(homepath, "Downloads", "Major-Chip-data")
    savefolder = os.path.join(basedir, today)
    os.makedirs(savefolder, exist_ok=True)
    for sid in minding_sid_list:
        try:
            filename = os.path.join(savefolder, f"{sid}.csv")
            start_time = datetime.now()
            print(f"[{start_time}] Fetching {sid} chip major data...")
            df = fetcher.fetch_data(sid=sid, finance_info=FinanceInfo.chip_major)
            df.to_csv(filename, index=False)
            end_time = datetime.now()
            print(f"[{end_time}] Finished to fetch {sid} chip major data. "
                  f"Elapsed time: {end_time - start_time}")
        except Exception as e:
            print(f"[{datetime.now()}] Occured ab error: {e}")

if  __name__ == '__main__':
    print("Start Fetching the chip major data...")
    job = schedule.every().day.at("08:30").do(get_chip_major)
    while True:
        schedule.run_pending()
        time.sleep(30)