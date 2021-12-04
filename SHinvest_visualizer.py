# 배당금 , 배당율, 수익률, 환율, 그래프 추이 한번 그려주고, etf 보유종목 현황이나 비율 정도.
# 보유주식 잔고, 평가잔고, 평단, 보유종목 top10 계좌 여러개 보여주고 수익률 등 합산 가능하게, 거래내역 두개 비교해서 전산누락도 확인, 평단과 주식수 체크
# 예금과 수익률 비교, 기간, 파일이름을 계좌명으로 출력
# 가장 최근 수수료율 확인시키기

from SHCal import SHCal
from ConversionTools import ConversionTools

from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar

def accountInfo(csv, corr_val=0.0):
    array = []
    i = 0
    while True:
        try:
            dict = {}
            usd_balance = 0
            krw_balance = 0

            date = datetime.now() - relativedelta(months=i)
            year, month = map(int, date.strftime('%Y %m').split())
            last_day = calendar.monthrange(year, month)[1]

            shcal = SHCal(csv, (year, month, last_day), corr_val)

            start_date = shcal.dateRange()[0]
            end_date = (year, month, last_day)

            tools = ConversionTools(start_date, end_date)

            print(f'계산중 : {csv}계좌 -> {end_date[0]}년 {end_date[1]}월\n')
            
            usd_balance += shcal.USD()
            usd_balance += shcal.USD_RP()
            krw_balance += shcal.KRW()
        
            kr_stock_info = []
            us_stock_info = []
            for key in shcal.stock_KR().keys():
                price = tools.krCodeToPrice(key[1:])
                stocks = shcal.stock_KR()[key]
                name = tools.krCodeToName(key[1:])
                quantity = len(stocks)
                avg = round(sum(stocks) / quantity)
                profit = round((price * quantity) - sum(stocks))
                rate = round(profit / sum(stocks) * 100, 2)
                
                kr_stock_info.append([name, quantity, avg, price, profit, rate])
                
                krw_balance += quantity * price

            for key in shcal.stock_US().keys():
                ticker = tools.usCodeToTicker(key)
                price = round(tools.usTickerToPrice(ticker), 2)
                stocks = shcal.stock_US()[key]
                quantity = len(stocks)
                avg = round(sum(stocks) / quantity, 2)
                profit = round((price * quantity) - sum(stocks), 2)
                rate = round(profit / sum(stocks) * 100, 2)
                
                us_stock_info.append([ticker, quantity, avg, price, profit, rate])

                usd_balance += quantity * price
            
            total_balance = usd_balance * tools.USDToKRW() + krw_balance         
            
            dict['날짜'] = f'{end_date[0]}년 {end_date[1]}월 {end_date[2]}일'
            dict['투자원금'] = shcal.principal()
            dict['평가잔고'] = int(total_balance)
            dict['수익금'] = int(total_balance) - shcal.principal()
            dict['수익률'] = round((int(total_balance) - shcal.principal()) / shcal.principal() * 100, 2)
            dict['한국주식잔고'] = kr_stock_info
            dict['미국주식잔고'] = us_stock_info

            # dict['한국배당금'] = shcal.dividend_KR()
            # dict['미국배당금'] = shcal.dividend_US()
            # dict['입금고액'] = shcal.deposit()
            # dict['출금고액'] = shcal.withdraw()
            dict['원화예수금'] = round(shcal.KRW())
            dict['달러예수금'] = shcal.USD()
            dict['달러RP'] = shcal.USD_RP()

            array.append(dict)
            i += 1
            
        except ValueError:
            return array

for line in accountInfo('1111.csv', -7954):
    for key in line.keys():
        print(line[key])
    print('')



# 종목, 수량, 매입금액, 평가금액, 평가손익, 평가수익률 계산하기
# HTS에서 일자별 잔고 비교로 에러 찾기

# 평가잔고에 전환입금 전환출금도 계산해야됨















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



