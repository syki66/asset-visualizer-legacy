import pandas as pd
from accountInfo import accountInfo

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import font_manager, rc
import numpy as np
import json
import ast
from tkinter import *

font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)


# year = []
# principal = []
# balance = []
# profit = []
# rate = []
# kr_stock = []
# us_stock = []
# kr_div = []
# us_div = []
# total_div = []
# USD_RP = []
# USD = []
# KRW = []
# after_tax_balance = []
# after_tax_profit = []
# fees = []


# for line in accountInfo('1111.csv', -12054):
#     year.insert(0, line['날짜'])
#     principal.insert(0, line['투자원금'])
#     balance.insert(0, line['평가잔고'])
#     profit.insert(0, line['수익금액'])
#     rate.insert(0, line['수익률'])
#     kr_stock.insert(0, line['한국주식잔고'])
#     us_stock.insert(0, line['미국주식잔고'])
#     kr_div.insert(0, line['한국배당금'])
#     us_div.insert(0, line['미국배당금'])
#     total_div.insert(0, line['전체배당금'])
#     KRW.insert(0, line['원화예수금'])
#     USD.insert(0, line['달러예수금'])
#     USD_RP.insert(0, line['달러RP'])
#     after_tax_balance.insert(0, line['세후평가금'])
#     after_tax_profit.insert(0, line['세후수익금'])
#     fees.insert(0, line['제비용'])



# df1 = accountInfo('1111.csv', -12054)
# df2 = accountInfo('2222.csv', +8806)
# df3 = accountInfo('3333.csv', +382442)

# df1.to_csv('test1.csv', mode='w')
# df2.to_csv('test2.csv', mode='w')
# df3.to_csv('test3.csv', mode='w')

df1 = pd.read_csv('test1.csv')
# df2 = pd.read_csv('test2.csv')
# df3 = pd.read_csv('test3.csv')

df1 = df1.set_index('날짜')
# df2 = df2.set_index('날짜')
# df3 = df3.set_index('날짜')


print(ast.literal_eval(df1['한국주식잔고']['2021-12-31']))





# df1 = df1.drop(columns=['한국주식잔고', '미국주식잔고'])
# df2 = df2.drop(columns=['한국주식잔고', '미국주식잔고'])
# df3 = df3.drop(columns=['한국주식잔고', '미국주식잔고'])


# df_merge = df1.add(df2, fill_value=0)
# df_merge = df_merge.add(df3, fill_value=0)
# print(df_merge)

# root = Tk()

# root.title("test")
# root.geometry('1600x900')



# fig = Figure(figsize=(20, 4), dpi=100)
# ax = fig.add_subplot()

# ax.set_ylabel('잔고 (단위: 억)')


# ax.set_title(f'월말 잔고 기록 (20{year[-1]} 기준) (세전)')
 
# ax.fill_between(year, balance, color="C1", alpha=0.4)
# ax.fill_between(year, principal, color="C0", alpha=0.5)
# ax.plot(year, balance, color="C1", label='평가금액')
# ax.plot(year, principal, color="C0", label='투입원금')


# max_val = max(max(principal), max(balance))
# max_range = (((max_val) // 10000000 + 1) * 2) * 10000000

# ax.set_xticklabels(year, rotation=45)
# # ax.set_xticklabels(year)


# ax.set_yticks(np.arange(0,max_range, 10000000))

# ax.grid(color='C7')
# ax.legend()


# canvas = FigureCanvasTkAgg(fig, master=root)
# canvas.draw()
# canvas.get_tk_widget().grid(row=0, column=0, columnspan=4, sticky='nsew')


# Grid.rowconfigure(root, index=0, weight=1)
# Grid.columnconfigure(root, index=0, weight=1)
# Grid.columnconfigure(root, index=1, weight=1)
# Grid.columnconfigure(root, index=2, weight=1)
# Grid.columnconfigure(root, index=3, weight=1)


# lbl1 = Label(root, borderwidth=1, relief="solid", text='보유종목 및 섹터', anchor='n')
# lbl2 = Label(root, borderwidth=1, relief="solid")
# lbl3 = Label(root, borderwidth=1, relief="solid")
# lbl4 = Label(root, borderwidth=1, relief="solid")

# lbl1.grid(row=1, column=0, sticky='nsew')
# lbl2.grid(row=1, column=1, sticky='nsew')
# lbl3.grid(row=1, column=2, sticky='nsew')
# lbl4.grid(row=1, column=3, sticky='nsew')




# # 보유주식
# Label(lbl2, borderwidth=1, relief='solid', text='현재 보유 종목').grid(row=0, column=0, columnspan=10, sticky='nsew')
# Grid.columnconfigure(lbl2, index=0, weight=1)

# all_stocks = kr_stock[-1] + us_stock[-1]
# all_stocks.insert(0, ['종목', '수량', '평균단가','현재가','수익금','수익률'])

# for i in range(len(all_stocks)):
#     for j in range(len(all_stocks[0])):
#         stock_text = all_stocks[i][j]
#         if type(all_stocks[i][j]) == int or type(all_stocks[i][j]) == float:
#             stock_text = f'{all_stocks[i][j]:,}'
#         Label(lbl2, borderwidth=1, relief='solid', text=stock_text, anchor='w').grid(row=i+1, column=j, sticky='nsew')
#         Grid.columnconfigure(lbl2, index=i+1, weight=1)

# # 세전
# Grid.columnconfigure(lbl3, index=0, weight=1)
# Grid.columnconfigure(lbl3, index=1, weight=1)
# Label(lbl3, borderwidth=1, relief='solid', text='세전').grid(row=0, column=0, columnspan=10, sticky='nsew')

# Label(lbl3, borderwidth=1, relief='solid', text=f'원금', anchor='w').grid(row=1, column=0, sticky='nsew')
# Label(lbl3, borderwidth=1, relief='solid', text=f'{principal[-1]:,}원', anchor='w').grid(row=1, column=1, sticky='nsew')
# Label(lbl3, borderwidth=1, relief='solid', text=f'평가금', anchor='w').grid(row=2, column=0, sticky='nsew')
# Label(lbl3, borderwidth=1, relief='solid', text=f'{balance[-1]:,}원', anchor='w').grid(row=2, column=1, sticky='nsew')
# Label(lbl3, borderwidth=1, relief='solid', text=f'수익금', anchor='w').grid(row=3, column=0, sticky='nsew')
# Label(lbl3, borderwidth=1, relief='solid', text=f'{profit[-1]:,}원', anchor='w').grid(row=3, column=1, sticky='nsew')
# Label(lbl3, borderwidth=1, relief='solid', text=f'수익률', anchor='w').grid(row=4, column=0, sticky='nsew')
# Label(lbl3, borderwidth=1, relief='solid', text=f'{rate[-1]}%', anchor='w').grid(row=4, column=1, sticky='nsew')
# try:
#     one_year_div = total_div[-1][0] - total_div[-13][0]
# except IndexError:
#     one_year_div = total_div[-1][0]
# Label(lbl3, borderwidth=1, relief='solid', text=f'배당금 (최근 1년)', anchor='w').grid(row=5, column=0, sticky='nsew')
# Label(lbl3, borderwidth=1, relief='solid', text=f'{one_year_div:,}원', anchor='w').grid(row=5, column=1, sticky='nsew')
# Label(lbl3, borderwidth=1, relief='solid', text=f'원금 대비 배당율 (최근 1년)', anchor='w').grid(row=6, column=0, sticky='nsew')
# Label(lbl3, borderwidth=1, relief='solid', text=f'{round(one_year_div / principal[-1] * 100, 2):,}%', anchor='w').grid(row=6, column=1, sticky='nsew')
# Label(lbl3, borderwidth=1, relief='solid', text=f'평가금 대비 배당율 (최근 1년)', anchor='w').grid(row=7, column=0, sticky='nsew')
# Label(lbl3, borderwidth=1, relief='solid', text=f'{round(one_year_div / balance[-1] * 100, 2):,}%', anchor='w').grid(row=7, column=1, sticky='nsew')

# # 세후
# Grid.columnconfigure(lbl4, index=0, weight=1)
# Grid.columnconfigure(lbl4, index=1, weight=1)
# Label(lbl4, borderwidth=1, relief='solid', text='세후').grid(row=0, column=0, columnspan=10, sticky='nsew')

# Label(lbl4, borderwidth=1, relief='solid', text=f'원금', anchor='w').grid(row=1, column=0, sticky='nsew')
# Label(lbl4, borderwidth=1, relief='solid', text=f'{principal[-1]:,}원', anchor='w').grid(row=1, column=1, sticky='nsew')
# Label(lbl4, borderwidth=1, relief='solid', text=f'평가금', anchor='w').grid(row=2, column=0, sticky='nsew')
# Label(lbl4, borderwidth=1, relief='solid', text=f'{after_tax_balance[-1]:,}원', anchor='w').grid(row=2, column=1, sticky='nsew')
# Label(lbl4, borderwidth=1, relief='solid', text=f'수익금', anchor='w').grid(row=3, column=0, sticky='nsew')
# Label(lbl4, borderwidth=1, relief='solid', text=f'{after_tax_profit[-1]:,}원', anchor='w').grid(row=3, column=1, sticky='nsew')
# Label(lbl4, borderwidth=1, relief='solid', text=f'수익률', anchor='w').grid(row=4, column=0, sticky='nsew')
# Label(lbl4, borderwidth=1, relief='solid', text=f'{round(after_tax_profit[-1] / principal[-1] * 100, 2)}%', anchor='w').grid(row=4, column=1, sticky='nsew')
# try:
#     one_year_div = (total_div[-1][0] - total_div[-13][0]) - (total_div[-1][1] - total_div[-13][1])
# except IndexError:
#     one_year_div = total_div[-1][0] - total_div[-1][1]
# Label(lbl4, borderwidth=1, relief='solid', text=f'배당금 (최근 1년)', anchor='w').grid(row=5, column=0, sticky='nsew')
# Label(lbl4, borderwidth=1, relief='solid', text=f'{one_year_div:,}원', anchor='w').grid(row=5, column=1, sticky='nsew')
# Label(lbl4, borderwidth=1, relief='solid', text=f'원금 대비 배당율 (최근 1년)', anchor='w').grid(row=6, column=0, sticky='nsew')
# Label(lbl4, borderwidth=1, relief='solid', text=f'{round(one_year_div / principal[-1] * 100, 2):,}%', anchor='w').grid(row=6, column=1, sticky='nsew')
# Label(lbl4, borderwidth=1, relief='solid', text=f'평가금 대비 배당율 (최근 1년)', anchor='w').grid(row=7, column=0, sticky='nsew')
# Label(lbl4, borderwidth=1, relief='solid', text=f'{round(one_year_div / balance[-1] * 100, 2):,}%', anchor='w').grid(row=7, column=1, sticky='nsew')
# Label(lbl4, borderwidth=1, relief='solid', text=f'제비용', anchor='w').grid(row=8, column=0, sticky='nsew')
# Label(lbl4, borderwidth=1, relief='solid', text=f'{fees[-1]:,}원', anchor='w').grid(row=8, column=1, sticky='nsew')





# root.mainloop()









# 과거 정보들은 콘솔창에 프린트 해주기

# 자료들이 어떻게 계산되는지 표기하기


# for line in accountInfo('1111.csv', -12054):
#     for key in line.keys():
#         print(f'{key} : {line[key]}')
#     print('')

# for line in accountInfo('2222.csv', +8806):
#     for key in line.keys():
#         print(f'{key} : {line[key]}')
#     print('')

# for line in accountInfo('3333.csv', +382442):
#     for key in line.keys():
#         print(f'{key} : {line[key]}')
#     print('')




# 불러온 계좌 체크박스 누른것들 합산해서 계산되게끔


# etf 보유종목 현황이나 비율 정도.
# 보유종목 top10 계좌 여러개 보여주고 수익률 등 합산 가능하게, 거래내역 두개 비교해서 전산누락도 확인, 평단과 주식수 체크 (매수날짜의 종가데이터와 스프레드 많이차이나는지, 전산에러만 확인)
# 가장 최근 수수료율 확인시키기





# HTS에서 일자별 잔고 비교로 에러 찾기

   
              



# 외화 RP값은 있다면 수동입력받기



# 각 운용사 etf csv 다운로드, 상위 증권사들 가져오면 대부분의 etf 가능할거같음
# https://www.blackrock.com/au/individual/products/275304/fund/1478358644060.ajax?fileType=csv&fileName=IVV_holdings&dataType=fund
# https://www.invesco.com/us/financial-products/etfs/holdings/main/holdings/0?audienceType=Investor&action=download&ticker=QQQM
# https://www.schwabassetmanagement.com/sites/g/files/eyrktu361/files/product_files/SCHD/SCHD_FundHoldings_2021-11-26.CSV?1638005310=

