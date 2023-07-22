import os
import schedule
import time
from datetime import datetime
from myModules.fetcher import FinanceInfo, YhaooTWStockFetcher
from myModules.utils import generate_correlation_analysis

minding_sid_list = [
    "2618.TW",
    "2330.TW",
    "2382.TW",
    "2618.TW",
    "5274.TWO",
    "3443.TW",
    "2454.TW",
    "1904.TW",
    "1905.TW"
]
 
def get_chip_major():
    fetcher = YhaooTWStockFetcher()
    today = datetime.now().date().strftime("%Y-%m-%d")
    week = f"Week {datetime.now().isocalendar()[1]}"
    homepath = os.path.expanduser("~")
    basedir = os.path.join(homepath, "Downloads", "Major-Chip-data", week)
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

def generate_analysis():
    print(f"Start generating the weekly analysis report...")
    homepath = os.path.expanduser("~")
    database_dir = os.path.join(homepath, "Downloads", "Major-Chip-data")
    output_file = os.path.join(database_dir, "analysis.xlsx")
    generate_correlation_analysis(minding_sid_list, database_dir, output_file)

if  __name__ == '__main__':
    print("Start fetching the chip major data...")
    timing = "08:30"
    # generate the weekly analysis report every Monday
    schedule.every().monday.at(timing).do(generate_analysis)
    schedule.every().monday.at(timing).do(get_chip_major)
    schedule.every().tuesday.at(timing).do(get_chip_major)
    schedule.every().wednesday.at(timing).do(get_chip_major)
    schedule.every().thursday.at(timing).do(get_chip_major)
    schedule.every().friday.at(timing).do(get_chip_major)
    while True:
        schedule.run_pending()
        time.sleep(30)