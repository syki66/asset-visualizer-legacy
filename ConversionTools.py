from datetime import datetime
import json
import requests
import time
from bs4 import BeautifulSoup

class ConversionTools:
    def __init__(self, start_date, end_date):
        self.start_year, self.start_month, self.start_day = start_date
        self.end_year, self.end_month, self.end_day = end_date

    def krCodeToPrice(self, code):
        url = f"https://api.finance.naver.com/siseJson.naver?symbol={code}&requestType=1&startTime={self.start_year}{self.start_month}{self.start_day}&endTime={self.end_year}{self.end_month}{self.end_day}&timeframe=day"
        res = requests.get(url)
        raw = res.text
        for i in reversed(raw.split('\n')):
            if i.startswith('["20'):
                year_get = int(i.split(',')[0].split('\"')[1][:4])
                month_get = int(i.split(',')[0].split('\"')[1][4:6])
                day_get = int(i.split(',')[0].split('\"')[1][6:8])
                if datetime(int(self.end_year), int(self.end_month), int(self.end_day)) >= datetime(year_get, month_get, day_get):
                    return int(i.split(',')[4])

    def usTickerToPrice(self, ticker):
        start_ts = int(time.mktime(datetime.strptime(f'{self.start_year}{self.start_month}{self.start_day}', "%Y%m%d").timetuple()))
        end_ts = int(time.mktime(datetime.strptime(f'{self.end_year}{self.end_month}{self.end_day}', "%Y%m%d").timetuple())) + 86400

        url = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={start_ts}&period2={end_ts}&interval=1d&events=history&includeAdjustedClose=true'
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        res = requests.get(url, headers=headers)
        raw = res.text

        array = []
        for line in raw.split('\n'):
            array.append(line.split(','))
        array.pop(0)
        
        for line in reversed(array):
            year_get = int(line[0].split('-')[0])
            month_get = int(line[0].split('-')[1])
            day_get = int(line[0].split('-')[2])
            if datetime(int(self.end_year), int(self.end_month), int(self.end_day)) >= datetime(year_get, month_get, day_get):
                return float(line[4])

    def krCodeToName(self, code):
        url = f'https://polling.finance.naver.com/api/realtime?query=SERVICE_ITEM:{code}'
        res = requests.get(url)
        raw = res.text
        return json.loads(raw)['result']['areas'][0]['datas'][0]['nm']

    def usCodeToTicker(self, code):
        url = f'https://query2.finance.yahoo.com/v1/finance/search?q={code}'
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        res = requests.get(url, headers=headers)
        raw = res.text
        return json.loads(raw)['quotes'][0]['symbol']

    def USDToKRW(self):
        index = 1
        while True:
            url = f'https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_USDKRW_SHB&page={index}'
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            date = soup.select('body > div > table > tbody > tr > td.date')
            rate = soup.select('body > div > table > tbody > tr> td:nth-child(2)')
        
            for i in range(len(date)):
                year_get = int(date[i].text.split('.')[0])
                month_get = int(date[i].text.split('.')[1])
                day_get = int(date[i].text.split('.')[2])
                if datetime(int(self.end_year), int(self.end_month), int(self.end_day)) >= datetime(year_get, month_get, day_get):
                    return float(rate[i].text.replace(',', ''))
            index += 1