from datetime import datetime
import json
import requests
import time
from bs4 import BeautifulSoup

import pandas as pd
import csv
import numpy as np

class Converter:
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

def VTIQQQM_ratio(VTI_weight, QQQM_weight):
    VTI_url = 'https://www.ishares.com/us/products/239724/ishares-core-sp-total-us-stock-market-etf/1467271812596.ajax?fileType=csv&fileName=ITOT_holdings&dataType=fund'
    res = requests.get(VTI_url)
    raw = res.text
    VTI_lines = raw.split('\xa0')[1].strip().splitlines()
    VTI_array = np.array(list(csv.reader(VTI_lines, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)))
    VTI_df = pd.DataFrame(VTI_array)
    VTI_df = pd.DataFrame(VTI_array[1:], columns=VTI_array[0], index=VTI_array[:,0][1:])
    VTI_df = VTI_df[['Weight (%)', 'Name', 'Sector']].rename(columns={'Weight (%)': 'Weight'})
    VTI_df['Weight'] = VTI_df['Weight'].astype('float')

    QQQM_url = 'https://www.invesco.com/us/financial-products/etfs/holdings/main/holdings/0?audienceType=Investor&action=download&ticker=QQQM'
    res = requests.get(QQQM_url)
    raw = res.text
    raw = raw.replace(' ,"', ',"')
    QQQM_lines = raw.splitlines()
    QQQM_array = np.array(list(csv.reader(QQQM_lines, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)))
    QQQM_df = pd.DataFrame(QQQM_array[1:], columns=QQQM_array[0], index=QQQM_array[:,2][1:])
    QQQM_df = QQQM_df[['Weight', 'Name', 'Sector']]
    QQQM_df['Weight'] = QQQM_df['Weight'].astype('float')

    # 가중치 곱하기
    VTI_df['new_weight'] = VTI_df['Weight'] * VTI_weight
    QQQM_df['new_weight'] = QQQM_df['Weight'] * QQQM_weight

    # 주식 비중
    stock_df = pd.DataFrame(VTI_df['new_weight'].add(QQQM_df['new_weight'], fill_value=0))

    # 구글 티커 합치기
    if 'GOOG' in stock_df.index and 'GOOGL' in stock_df.index:
        stock_df['new_weight']['GOOGL'] = stock_df['new_weight']['GOOG'] + stock_df['new_weight']['GOOGL']
        stock_df = stock_df.drop(['GOOG'], axis=0)
        
    # 회사명 추가 (에러 때문에 보유비중 0.01% 이상만 남겨둠)
    stock_df = stock_df[stock_df['new_weight'] >= 0.01]
    stock_df['Name'] = QQQM_df['Name'].combine_first(VTI_df[VTI_df['new_weight'] >= 0.01]['Name'])
    stock_df = stock_df.sort_values('new_weight', ascending=False)

    # 섹터 비중
    sector_df = pd.concat([VTI_df, QQQM_df]).groupby(['Sector']).sum()
    sector_df = sector_df.drop(['Weight'], axis=1)

    # 같은 섹터 이름 합치기
    if 'Cash' in sector_df.index:
        sector_df['new_weight']['Cash and/or Derivatives'] = sector_df['new_weight']['Cash'] + sector_df['new_weight']['Cash and/or Derivatives']
        sector_df = sector_df.drop(['Cash'], axis=0)
    if 'Communication' in sector_df.index:
        sector_df['new_weight']['Communication Services'] = sector_df['new_weight']['Communication'] + sector_df['new_weight']['Communication Services']
        sector_df = sector_df.drop(['Communication'], axis=0)

    sector_df = sector_df.sort_values('new_weight', ascending=False)

    return stock_df, sector_df