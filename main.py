from myModules.fetcher import FinanceInfo, YhaooTWStockFetcher

if  __name__ == '__main__':
    fetcher = YhaooTWStockFetcher()

    url = "https://tw.stock.yahoo.com/quote/2330"

    data = fetcher.fetch_data(sid=2330, finance_info=FinanceInfo.chip_major)
    # data = fetcher.fetch(2382, Info.chip_major)
    # data = fetcher.fetch(2330, Info.chip_trade)
    a = 1