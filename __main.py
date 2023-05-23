import yfinance as yf
from collections import namedtuple
import mplfinance as mpf
import twstock
from lxml import etree
from myModules.fetcher import StockFetcher



import requests
from bs4 import BeautifulSoup

# coding:utf-8
import requests
import urllib3
from lxml import etree
urllib3.disable_warnings()

url = "https://blog.51cto.com/u_15249893"
r = requests.get(url, verify=False)

with open("/home/kevin/Downloads/ttttt.txt", "w") as f:
    f.write(r.content.decode("utf-8"))
# print(r.text)

dom = etree.HTML(r.content.decode("utf-8"))

block = dom.xpath("//*[@id='profile_block']")


t1 = block[0].xpath('text()')    # 获取当前节点文本元素
print(t1)
t2 = block[0].xpath('a')    # 定位a标签

# 打印结果
for i, j in zip(t1, t2):
    print("%s%s" % (i, j.text))

url = 'https://tw.stock.yahoo.com/quote/2330.TW'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

dom = etree.HTML(r.content.decode("utf-8"))

# Extract the desired data
company_name = soup.find('h1', {'data-reactid': '7'}).text
stock_price = soup.find('span', {'data-reactid': '21'}).text
# Add more data extraction as needed

# Print the extracted data
print("Company Name:", company_name)
print("Stock Price:", stock_price)


TWSE_STOCKS_URL = 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
TPEX_STOCKS_URL = 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=4'

ROW = namedtuple('Row', ['type', 'code', 'name', 'ISIN', 'start',
                         'market', 'group', 'CFI'])

def make_row_tuple(typ, row):
    code, name = row[1].split('\u3000')
    return ROW(typ, code, name, *row[2: -1])

if  __name__ == '__main__':
    # Get all Listed Stock IDs in Taiwan Stock Exchange
    stock_fetcher = StockFetcher()
    stock_ids = stock_fetcher.get_all_stock_id(market='twse')
    for name, id in stock_ids.items():
        info = stock_fetcher.get_stock_dividend_info(id)
    print(stock_ids)