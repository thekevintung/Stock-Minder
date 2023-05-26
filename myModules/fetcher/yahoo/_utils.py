class FinanceInfo:
    overview = "走勢圖"
    technical_analysis = "技術分析"
    time_sales = "成交彙整"
    chip_trade = "法人買賣"
    chip_major = "主力進出"
    chip_margin = "資券變化"
    chip_major_holders = "大戶籌碼"
    chip_insider_transactions = "申報轉讓"
    dividend = "股利"
    revenue = "營收表"
    eps = "每股盈餘"
    income_statement = "損益表"
    balance_sheet = "資產負債表"
    cash_flow_statement = "現金流量表"
    profile = "基本"
    compare = "同業比較"
    calendar = "行事曆"

def get_url(sid:str, target_info:str):
    urls = {
        FinanceInfo.overview: f"https://tw.stock.yahoo.com/quote/{sid}",
        FinanceInfo.technical_analysis: f"https://tw.stock.yahoo.com/quote/{sid}/technical-analysis",
        FinanceInfo.time_sales: f"https://tw.stock.yahoo.com/quote/{sid}/time-sales",
        FinanceInfo.chip_trade: f"https://tw.stock.yahoo.com/quote/{sid}/institutional-trading",
        FinanceInfo.chip_major: f"https://tw.stock.yahoo.com/quote/{sid}/broker-trading",
        FinanceInfo.chip_margin: f"https://tw.stock.yahoo.com/quote/{sid}/margin",
        FinanceInfo.chip_major_holders: f"https://tw.stock.yahoo.com/quote/{sid}/major-holders",
        FinanceInfo.chip_insider_transactions: f"https://tw.stock.yahoo.com/quote/{sid}/insider-transactions",
        FinanceInfo.dividend: f"https://tw.stock.yahoo.com/quote/{sid}/dividend",
        FinanceInfo.revenue: f"https://tw.stock.yahoo.com/quote/{sid}/revenue",
        FinanceInfo.eps: f"https://tw.stock.yahoo.com/quote/{sid}/eps",
        FinanceInfo.income_statement: f"https://tw.stock.yahoo.com/quote/{sid}/income-statement",
        FinanceInfo.balance_sheet: f"https://tw.stock.yahoo.com/quote/{sid}/balance-sheet",
        FinanceInfo.cash_flow_statement: f"https://tw.stock.yahoo.com/quote/{sid}/cash-flow-statement",
        FinanceInfo.profile: f"https://tw.stock.yahoo.com/quote/{sid}/profile",
        FinanceInfo.compare: f"https://tw.stock.yahoo.com/quote/{sid}/compare",
        FinanceInfo.calendar: f"https://tw.stock.yahoo.com/quote/{sid}/calendar",
    }
    return urls.get(target_info, None)