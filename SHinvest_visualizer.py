# 배당금 , 배당율, 수익률, 환율, 그래프 추이 한번 그려주고, etf 보유종목 현황이나 비율 정도.
# 보유주식 잔고, 평가잔고, 평단, 보유종목 top10 계좌 여러개 보여주고 수익률 등 합산 가능하게, 거래내역 두개 비교해서 전산누락도 확인, 평단과 주식수 체크
# 예금과 수익률 비교, 기간, 파일이름을 계좌명으로 출력
# 가장 최근 수수료율 확인시키기




from os import replace
from SHCal import SHCal



from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar
import json
import requests
import collections
import time
from bs4 import BeautifulSoup

now_year, now_month, now_day = map(int, datetime.now().strftime('%Y %m %d').split())
start_year, start_month, start_day = ('1990', '01', '01')
# 거래내역 받아서 필요한만큼부터  시작하고, 너무 느리면 캐시 함수 사용하기

def krCodeToPrice(code, year, month, day):
    url = f"https://api.finance.naver.com/siseJson.naver?symbol={code}&requestType=1&startTime={start_year}{start_month}{start_day}&endTime={str(year).zfill(2)}{str(month).zfill(2)}{str(day).zfill(2)}&timeframe=day"
    res = requests.get(url)
    raw = res.text
    for i in reversed(raw.split('\n')):
        if i.startswith('["20'):
            year_get = int(i.split(',')[0].split('\"')[1][:4])
            month_get = int(i.split(',')[0].split('\"')[1][4:6])
            day_get = int(i.split(',')[0].split('\"')[1][6:8])
            if datetime(year, month, day) >= datetime(year_get, month_get, day_get):
                return int(i.split(',')[4])

def krCodeToName(code):
    url = f'https://polling.finance.naver.com/api/realtime?query=SERVICE_ITEM:{code}'
    res = requests.get(url)
    raw = res.text
    return json.loads(raw)['result']['areas'][0]['datas'][0]['nm']

def usCodeToTicker(code):
    url = f'https://query2.finance.yahoo.com/v1/finance/search?q={code}'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    res = requests.get(url, headers=headers)
    raw = res.text
    return json.loads(raw)['quotes'][0]['symbol']

def usTickerToPrice(ticker, year, month, day):
    start_date = f'{start_year}-{start_month}-{start_day}'
    start_ts = int(time.mktime(datetime.strptime(start_date, "%Y-%m-%d").timetuple()))
    date = f'{year}-{month}-{day}'
    end_ts = int(time.mktime(datetime.strptime(date, "%Y-%m-%d").timetuple()))

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
        if datetime(year, month, day) >= datetime(year_get, month_get, day_get):
            return float(line[4])


def USDToKRW(year, month, day):
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
            if datetime(year, month, day) >= datetime(year_get, month_get, day_get):
                return float(rate[i].text.replace(',', ''))

        

        index += 1
        # print(date[i].text, rate[i].text)
# print(USDToKRW(2021, 9, 28))


# corr_val = -7954
corr_val = 0

array = []
i = 0
end = False
while not end:
    try:
        usd_balance = 0
        krw_balance = 0


        temp = []
        date = datetime.now() - relativedelta(months=i)
        year, month = map(int, date.strftime('%Y %m').split())
        last_day = calendar.monthrange(year, month)[1]
        # print(year, month, last_day)
        
        shcal = SHCal('2222.csv', (year, month, last_day), corr_val)
        temp.append((year, month, last_day))
        # temp.append(shcal.deposit())
        # temp.append(shcal.withdraw())
        temp.append(shcal.principal())

        temp.append(shcal.USD())
        usd_balance += shcal.USD()
        temp.append(shcal.KRW())
        krw_balance += shcal.KRW()

        temp.append(shcal.USD_RP())
        # temp.append(shcal.dividend_KR())
        # temp.append(shcal.dividend_US())
        


        
        print('\n')
        print(year, month, last_day)
        profit = 0
            

        
        for key in shcal.stock_KR().keys():
            KR_curr_price = krCodeToPrice(key[1:], year, month, last_day) # 여기에 시장값 가져오는 함수 사용하기

            kr_stocks = shcal.stock_KR()[key]
            stock_avg = len(kr_stocks) * (KR_curr_price - (sum(kr_stocks) / len(kr_stocks)))
            # print(krCodeToName(key[1:]), len(kr_stocks), KR_curr_price, stock_avg)
            
            krw_balance += len(kr_stocks) * KR_curr_price

        
        for key in shcal.stock_US().keys():
            ticker = usCodeToTicker(key)
            curr_price = usTickerToPrice(ticker, year, month, last_day) # 여기에 시장값 가져오는 함수 사용하기

            us_stocks = shcal.stock_US()[key]
            stock_avg = len(us_stocks) * (curr_price - (sum(us_stocks) / len(us_stocks)))
            # print(usCodeToTicker(key), len(us_stocks), curr_price, stock_avg)

            usd_balance += len(us_stocks) * curr_price
        
        usd_balance += shcal.USD_RP()
        print(krw_balance)
        print(usd_balance)
        total_balance = usd_balance * USDToKRW(year, month, last_day) + krw_balance
        print(f'원금 : {shcal.principal():,} 원')
        print(f'평가잔고 : {int(total_balance):,} 원')
        print(f'수익금 : {int(total_balance) - shcal.principal():,} 원')
        print(f'수익률 : {round((int(total_balance) - shcal.principal()) / shcal.principal() * 100, 2):,} %')
        


        # temp.append(shcal.stock_KR())
        # temp.append(shcal.stock_US())
        
        # temp.append(평가잔고)
        
        i += 1
        array.append(temp)
    except ValueError:
        end = True


# 종목, 수량, 매입금액, 평가금액, 평가손익, 평가수익률 계산하기
# HTS에서 월간거래내역 비교로 에러 찾기

# 평가잔고에 전환입금 전환출금도 계산해야됨



# cal = SHCal('1111.csv', (2021, 11, 27), -7954)

# # cal2 = SHCal('1111.csv', (2021, 7, 27), -7954)
# print("\n\n\n")
# print(cal.deposit())
# print(cal.withdraw())
# print(cal.principal())
# print(cal.USD())
# print(cal.KRW())
# # print(cal.USD_RP())
# print(cal.dividend_KR())
# print(cal.dividend_US())
# print(cal.stock_KR())
# print(cal.stock_US())

# # print(cal.stock_KR().keys())













# 외화 RP값은 있다면 수동입력받기


# 남은원화, 남은외화, 해외주식 평단까지 계산해서 세후 실제 수익률 보여주기
# 월 수익률 그래프


# 미국주식은 코드랑 티커 매칭시켜줘야됨
# 국내, 해외 주식 종가 데이터 hist
# 환율 종가 데이터 hist

#https://api.polygon.io/v2/reference/dividends/IVV?apiKey=AciB5tx_lEwCiVv5aP3b79zFCLoGGC20
# https://api.stock.naver.com/chart/foreign/item/QQQM.O?periodType=monthCandle&stockExchangeType=NASDAQ



# 국내주식
# https://api.finance.naver.com/siseJson.naver?symbol=005930&requestType=1&startTime=20120922&endTime=20210420&timeframe=month


# 네이버 환율 크롤링해야됨
# https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_USDKRW_SHB&page=1

# 종목 코드를 티커로, 크롤링
# https://kr.investing.com/search/?q=US78467X1090&tab=quotes

# 미국 배당 및 주가 데이터
# https://api.nasdaq.com/api/quote/IVV/dividends?assetclass=etf
# https://api.nasdaq.com/api/quote/IVV/chart?assetclass=etf&fromdate=2001-11-28&todate=2021-11-28

# https://seekingalpha.com/api/v3/symbols/spy/dividend_history?&sort=-date
# https://finance.api.seekingalpha.com/v2/chart?period=max&symbol=ivv

# https://query1.finance.yahoo.com/v7/finance/download/IVV?period1=958780800&period2=1638230400&interval=1d&events=history&includeAdjustedClose=true
# https://finance.yahoo.com/quote/IVV/history?period1=1606671434&period2=1638207434&interval=capitalGain%7Cdiv%7Csplit&filter=div&frequency=1d&includeAdjustedClose=true
# https://api.polygon.io/v2/aggs/ticker/IVV/range/1/day/2020-06-01/2021-12-10?apiKey=AciB5tx_lEwCiVv5aP3b79zFCLoGGC20

# 각 운용사 etf csv 다운로드, 상위 증권사들 가져오면 대부분의 etf 가능할거같음
# https://www.blackrock.com/au/individual/products/275304/fund/1478358644060.ajax?fileType=csv&fileName=IVV_holdings&dataType=fund
# https://www.invesco.com/us/financial-products/etfs/holdings/main/holdings/0?audienceType=Investor&action=download&ticker=QQQM
# https://www.schwabassetmanagement.com/sites/g/files/eyrktu361/files/product_files/SCHD/SCHD_FundHoldings_2021-11-26.CSV?1638005310=



