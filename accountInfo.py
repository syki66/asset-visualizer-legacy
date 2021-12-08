from SHCal import SHCal
from Converter import Converter

from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar
import pandas as pd

def singleAccountInfo(csv, corr_val=0.0):
    df = pd.DataFrame()
    i = 0
    while True:
        try:
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
        
            kr_stock_df = pd.DataFrame(columns=['종목', '수량', '평균단가', '현재가', '수익금'])
            us_stock_df = pd.DataFrame(columns=['종목', '수량', '평균단가', '현재가', '수익금'])
            for key in shcal.stock_KR().keys():
                price = tools.krCodeToPrice(key[1:])
                stocks = shcal.stock_KR()[key]
                name = tools.krCodeToName(key[1:])
                quantity = len(stocks)
                avg = round(sum(stocks) / quantity)
                profit = round((price * quantity) - sum(stocks))
                rate = round(profit / sum(stocks) * 100, 2)
                
                kr_stock_col = {
                    '종목' : name,
                    '수량' : quantity,
                    '평균단가' : avg,
                    '현재가' : price,
                    '수익금' : profit
                }
                kr_stock_df = kr_stock_df.append(kr_stock_col, ignore_index=True)
                
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
                
                us_stock_col = {
                    '종목' : ticker,
                    '수량' : quantity,
                    '평균단가' : avg,
                    '현재가' : price,
                    '수익금' : profit
                }
                us_stock_df = us_stock_df.append(us_stock_col, ignore_index=True)

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

            col = {
                '날짜': f'{end_date[0]}-{str(end_date[1]).zfill(2)}-{str(end_date[2]).zfill(2)}',
                '투자원금': shcal.principal(),
                '평가잔고': int(total_balance),
                '수익금액': int(total_balance) - shcal.principal(),

                '한국주식잔고': kr_stock_df.set_index('종목'),
                '미국주식잔고': us_stock_df.set_index('종목'),

                '한국배당금': shcal.dividend_KR()[0],
                '한국배당세': shcal.dividend_KR()[1],
                '미국배당금': shcal.dividend_US()[0],
                '미국배당세': shcal.dividend_US()[1],
                '전체배당금': round(shcal.dividend_US()[0] * tools.USDToKRW() + shcal.dividend_KR()[0]),
                '전체배당세': round(shcal.dividend_US()[1] * tools.USDToKRW() + shcal.dividend_KR()[1]),
                '입금고액': shcal.deposit(),
                '출금고액': shcal.withdraw(),
                '원화예수금': round(shcal.KRW()),
                '달러예수금': shcal.USD(),
                '달러RP': shcal.USD_RP(),
                '금': shcal.gold(),

                '세후평가금': int(total_after_tax),
                '세후수익금': int(total_after_tax) - shcal.principal(),
                '제비용': int(total_balance) - int(total_after_tax)
            }

            df = df.append(col, ignore_index=True)
            i += 1
            
        except ValueError:
            df = df.set_index('날짜')
            return df

def mergeAccountInfo(df_list):
    pd.set_option('mode.chained_assignment',  None) # SettingWithCopyWarning 경고 끄기

    df_merge = pd.DataFrame()
    for df in df_list:
        df_merge = df_merge.add(df, fill_value=0)

    date_list = []
    for df in df_list:
        date_list += list(df.index)
    date_list = list(set(date_list))
    
    for date in date_list:
        kr_stock_merge = pd.DataFrame()
        for df in df_list:
            if date in df.index:
                kr_stock_merge = kr_stock_merge.add(df['한국주식잔고'][date], fill_value=0)
        df_merge['한국주식잔고'][date] = kr_stock_merge.astype('int')

    for date in date_list:
        us_stock_merge = pd.DataFrame()
        for df in df_list:
            if date in df.index:
                us_stock_merge = us_stock_merge.add(df['미국주식잔고'][date], fill_value=0)
        us_stock_merge['수량'] = us_stock_merge['수량'].astype('int')
        df_merge['미국주식잔고'][date] = us_stock_merge

    df_merge['금'] = df_merge['금'].astype('int')
    df_merge['세후수익금'] = df_merge['세후수익금'].astype('int')
    df_merge['세후평가금'] = df_merge['세후평가금'].astype('int')
    df_merge['수익금액'] = df_merge['수익금액'].astype('int')
    df_merge['원화예수금'] = df_merge['원화예수금'].astype('int')
    df_merge['입금고액'] = df_merge['입금고액'].astype('int')
    df_merge['전체배당금'] = df_merge['전체배당금'].astype('int')
    df_merge['전체배당세'] = df_merge['전체배당세'].astype('int')
    df_merge['제비용'] = df_merge['제비용'].astype('int')
    df_merge['출금고액'] = df_merge['출금고액'].astype('int')
    df_merge['투자원금'] = df_merge['투자원금'].astype('int')
    df_merge['평가잔고'] = df_merge['평가잔고'].astype('int')
    df_merge['한국배당금'] = df_merge['한국배당금'].astype('int')
    df_merge['한국배당세'] = df_merge['한국배당세'].astype('int')

    return df_merge