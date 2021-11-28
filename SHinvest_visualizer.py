# 배당금 , 배당율, 수익률, 환율, 그래프 추이 한번 그려주고, etf 보유종목 현황이나 비율 정도.
# 보유주식 잔고, 평가잔고, 평단, 보유종목 top10 계좌 여러개 보여주고 수익률 등 합산 가능하게, 거래내역 두개 비교해서 전산누락도 확인, 평단과 주식수 체크
# 예금과 수익률 비교, 기간, 파일이름을 계좌명으로 출력
# 가장 최근 수수료율 확인시키기




from SHCal import SHCal



from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar


corr_val = -7954


array = []
i = 0
end = False
while not end:
    try:
        temp = []
        date = datetime.now() - relativedelta(months=i)
        year, month = map(int, date.strftime('%Y %m').split())
        last_day = calendar.monthrange(year, month)[1]
        # print(year, month, last_day)
        
        shcal = SHCal('1111.csv', (year, month, last_day), corr_val)
        temp.append((year, month, last_day))
        # temp.append(shcal.deposit())
        # temp.append(shcal.withdraw())
        temp.append(shcal.principal())
        temp.append(shcal.USD())
        temp.append(shcal.KRW())
        # temp.append(shcal.USD_RP())
        # temp.append(shcal.dividend_KR())
        # temp.append(shcal.dividend_US())

        profit = 0
        for key in shcal.stock_KR().keys():
            curr_price = 73000 # 여기에 시장값 가져오는 함수 사용하기
            stocks = shcal.stock_KR()[key]
            print(len(stocks) * (curr_price - (sum(stocks) / len(stocks))) )

        temp.append(shcal.stock_KR())
        temp.append(shcal.stock_US())
        
        # temp.append(평가잔고)
        
        i += 1
        array.append(temp)
    except ValueError:
        end = True



# import requests
# stock_code = '005930'
# url = f"https://api.finance.naver.com/siseJson.naver?symbol={stock_code}&requestType=1&startTime=20120922&endTime=20211129&timeframe=day"
# res = requests.get(url)
# rawData = res.text
# for i in rawData.split('\n'):
#     if i.startswith('["20'):
#         print(i)





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


# 각 운용사 etf csv 다운로드, 상위 증권사들 가져오면 대부분의 etf 가능할거같음
# https://www.blackrock.com/au/individual/products/275304/fund/1478358644060.ajax?fileType=csv&fileName=IVV_holdings&dataType=fund
# https://www.invesco.com/us/financial-products/etfs/holdings/main/holdings/0?audienceType=Investor&action=download&ticker=QQQM
# https://www.schwabassetmanagement.com/sites/g/files/eyrktu361/files/product_files/SCHD/SCHD_FundHoldings_2021-11-26.CSV?1638005310=



