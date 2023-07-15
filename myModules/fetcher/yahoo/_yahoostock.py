import requests
from lxml import etree
from myModules.fetcher import BaseFetcher
from ._parse import Parser
from ._utils import FinanceInfo, get_url

NOT_SUPPORT = None

class YhaooTWStockFetcher(BaseFetcher):
    def __init__(self) -> None:
        super().__init__()
        self.base_url = "https://tw.stock.yahoo.com/quote"

        self.parse_handles = {
            FinanceInfo.overview: NOT_SUPPORT,
            FinanceInfo.technical_analysis: NOT_SUPPORT,
            FinanceInfo.time_sales: NOT_SUPPORT,
            FinanceInfo.chip_trade: Parser.get_chip_trade,
            FinanceInfo.chip_major: Parser.get_chip_major,
            FinanceInfo.chip_margin: NOT_SUPPORT,
            FinanceInfo.chip_major_holders: NOT_SUPPORT,
            FinanceInfo.chip_insider_transactions: NOT_SUPPORT,
            FinanceInfo.dividend: Parser.get_dividend,
            FinanceInfo.revenue: NOT_SUPPORT,
            FinanceInfo.eps: NOT_SUPPORT,
            FinanceInfo.income_statement: NOT_SUPPORT,
            FinanceInfo.balance_sheet: NOT_SUPPORT,
            FinanceInfo.cash_flow_statement: NOT_SUPPORT,
            FinanceInfo.profile: NOT_SUPPORT,
            FinanceInfo.compare: NOT_SUPPORT,
            FinanceInfo.calendar: NOT_SUPPORT,
        }

    def fetch_data(self, sid:int, finance_info:str):
        url = get_url(sid, finance_info)
        response = requests.get(url, timeout=5)
        root = etree.HTML(response.text)
        handler = self.parse_handles.get(finance_info)
        if handler is NOT_SUPPORT:
            raise NotImplementedError(
                f"The functionality of {finance_info} is not yet supported.")
        return handler(root)