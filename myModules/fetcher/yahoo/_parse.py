import pandas as pd
from lxml import etree

class Parser:
    def get_chip_trade(root:etree._Element):
        # get table headers
        xpaths = [
            '//*[@id="qsp-trading-by-day"]/div[3]/div/div[1]/div/div[1]/div',
            '//*[@id="qsp-trading-by-day"]/div[3]/div/div[1]/div/div']
        xpaths = '|'.join(xpaths)
        elements = root.xpath(xpaths)
        headers = [element.text for element in elements if element.text]
        
        # get table data (excluding column 7, which is quote change(%))
        xpaths = [
            '//*[@id="qsp-trading-by-day"]/div[3]/div/div[2]/div/div/ul/li/div/div/div',
            '//*[@id="qsp-trading-by-day"]/div[3]/div/div[2]/div/div/ul/li/div/div[not(position()=7)]/span'
        ]
        xpaths = '|'.join(xpaths)
        elements = root.xpath(xpaths)
        data = [element.text for element in elements if element.text]
        data = [data[i:i+7] for i in range(0, len(data), 7)]

        # get table data quote change(%) for column 7
        xpath = '//*[@id="qsp-trading-by-day"]/div[3]/div/div[2]/div/div/ul/li/div/div[7]/span'
        text_xpath = '//*[@id="qsp-trading-by-day"]/div[3]/div/div[2]/div/div/ul/li/div/div[7]/span/text()'
        buf = []
        for element, text in zip(root.xpath(xpath), root.xpath(text_xpath)):
            if element is not None:
                # check if the trend is down and convert the value to negative
                if 'C($c-trend-down)' in element.get('class', ''):
                    text = '-' + text
            buf.append(float(text.rstrip('%')))

        df = pd.DataFrame(data)
        df.insert(6, '', buf)   # insert quote change(%) column 7
        df.columns = headers
        return df

    def get_chip_major(root:etree._Element):
        # get table headers
        xpath = '//*[@id="main-3-QuoteChipMajor-Proxy"]/div/section/div/div/div[1]/span'
        elements = root.xpath(xpath)
        headers = [element.text for element in elements]
        
        # get table data, position() > 1 means start from second row
        xpaths = [
            '//*[@id="main-3-QuoteChipMajor-Proxy"]/div/section/div/div[1]/div[position() > 1]/span',
            '//*[@id="main-3-QuoteChipMajor-Proxy"]/div/section/div/div[2]/div[position() > 1]/span']
        elements = list(map(lambda xpath: root.xpath(xpath), xpaths))

        df = pd.DataFrame()
        for xpath in xpaths:
            elements = root.xpath(xpath)
            data, buf = [], []
            for element in elements:
                if element.text is not None:
                    buf.append(element.text)
                else:
                    data.append(buf)
                    buf = []
            df = pd.concat([df, pd.DataFrame(data)], axis=1)
        df.columns = headers
        return df
    
    def get_dividend(root:etree._Element):
        # get table headers
        xpaths = [
            '//*[@id="main-2-QuoteDividend-Proxy"]/div/section[2]/div[2]/div[1]/div/div[1]/div[1]',
            '//*[@id="main-2-QuoteDividend-Proxy"]/div/section[2]/div[2]/div[1]/div/div']
        xpaths = '|'.join(xpaths)
        elements = root.xpath(xpaths)
        headers = [element.text for element in elements if element.text]

        # get table data
        xpaths = [
            '//*[@id="main-2-QuoteDividend-Proxy"]/div/section[2]/div[2]/div[2]/div/div/ul/li/div/div[1]/div[1]',
            '//*[@id="main-2-QuoteDividend-Proxy"]/div/section[2]/div[2]/div[2]/div/div/ul/li/div/div/span',
            '//*[@id="main-2-QuoteDividend-Proxy"]/div/section[2]/div[2]/div[2]/div/div/ul/li/div/div']
        xpaths = '|'.join(xpaths)
        elements = root.xpath(xpaths)
        data = [element.text for element in elements if element.text]
        data = [data[i:i+9] for i in range(0, len(data), 9)]

        df = pd.DataFrame(data, columns=headers)
        return df