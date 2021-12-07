from SHCal import SHCal
from Converter import Converter

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

            tools = Converter(start_date, end_date)

            print(f'계산중 : {csv}계좌 -> {end_date[0]}년 {end_date[1]}월')
        
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

            us_profit = 0
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

                us_profit += (quantity * price) - (quantity * avg)


            kr_tax = 0.23 * 0.01 # 매도세
            kr_fee = 0.00363960 * 0.01 # 유관제비용
            us_tax = 22 * 0.01 # 양도세
            us_fee_1 = 0.05 * 0.01 # 매매 수수료
            us_fee_2 = 0.0000051 # SEC 수수료

            us_after_tax = 0
            kr_after_tax = 0
            
            kr_after_tax += krw_balance
            kr_after_tax -= krw_balance * (kr_tax + kr_fee)

            us_total_fee = usd_balance * (us_fee_1 + us_fee_2)

            us_after_tax += usd_balance 
            us_after_tax -= us_total_fee


            if us_profit >= 2500000 / tools.USDToKRW():
                us_after_tax -= (us_profit - us_total_fee - (2500000 / tools.USDToKRW())) * us_tax

            us_after_tax += shcal.USD()
            us_after_tax += shcal.USD_RP()
            kr_after_tax += shcal.KRW()
            kr_after_tax += shcal.gold()

            total_after_tax = us_after_tax * tools.USDToKRW() + kr_after_tax


            usd_balance += shcal.USD()
            usd_balance += shcal.USD_RP()
            krw_balance += shcal.KRW()
            krw_balance += shcal.gold()

            total_balance = usd_balance * tools.USDToKRW() + krw_balance   
            
            dict['날짜'] = f'{end_date[0] - 2000}년 {end_date[1]}월'
            dict['투자원금'] = shcal.principal()
            dict['평가잔고'] = int(total_balance)
            dict['수익금액'] = int(total_balance) - shcal.principal()
            
            dict['수익률'] = 0
            if shcal.principal() != 0:
                dict['수익률'] = round((int(total_balance) - shcal.principal()) / shcal.principal() * 100, 2)

            dict['한국주식잔고'] = kr_stock_info
            dict['미국주식잔고'] = us_stock_info

            dict['한국배당금'] = shcal.dividend_KR()
            dict['미국배당금'] = shcal.dividend_US()
            dict['전체배당금'] = (round(shcal.dividend_US()[0] * tools.USDToKRW() + shcal.dividend_KR()[0]), round(shcal.dividend_US()[1] * tools.USDToKRW() + shcal.dividend_KR()[1]))
            dict['입금고액'] = shcal.deposit()
            dict['출금고액'] = shcal.withdraw()
            dict['원화예수금'] = round(shcal.KRW())
            dict['달러예수금'] = shcal.USD()
            dict['달러RP'] = shcal.USD_RP()
            dict['금'] = shcal.gold()

            dict['세후평가금'] = int(total_after_tax)
            dict['세후수익금'] = int(total_after_tax) - shcal.principal()
            dict['제비용'] = int(total_balance) - int(total_after_tax)

            array.append(dict)
            i += 1
            
        except ValueError:
            return array
