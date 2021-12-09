import csv
import pandas as pd
from accountInfo import singleAccountInfo, mergeAccountInfo

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import font_manager, rc
import numpy as np
import json
import ast
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import math
import pickle


font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)




def getCSV():
    root = Tk()
    root.filename = filedialog.askopenfilenames(title='신한금융투자 거래내역 csv를 선택해주세요. (복수 선택 가능)', filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    csv_list = root.filename
    root.destroy()
    return csv_list

def setName(csv_list):
    input_list = []
    
    root = Tk()
    root.geometry('1280x720')
    Label(root, text='파일명').grid(row=0, column=0)
    Label(root, text='계좌명').grid(row=0, column=1)
    for i in range(len(csv_list)):
        Label(root, text=csv_list[i]).grid(row=i+1, column=0)
        input_list.append(Entry(root))
        input_list[-1].grid(row=i+1, column=1)

    names = []
    def submit():
        for i in input_list:
            names.append(i.get())
        root.destroy()
    Button(root, text='완료', command=submit).grid(row=len(csv_list)+1, column=1)
    
    root.mainloop()
    return ' + '.join(names)

def saveObject(csv_list):
    pass


# csv_list = getCSV()
# account_name = setName(csv_list)
# print(account_name)




f = open("test1.pkl", "rb")
df1 = pickle.load(f)
f.close()
f = open("test2.pkl", "rb")
df2 = pickle.load(f)
f.close()
f = open("test3.pkl", "rb")
df3 = pickle.load(f)
f.close()
f = open("test4.pkl", "rb")
df4 = pickle.load(f)
f.close()


# 바이너리값 저장할지 안할지 선택하는 함수 추가

# df_list = [singleAccountInfo('1111.csv', -12054), singleAccountInfo('2222.csv', +8806), singleAccountInfo('3333.csv', +382442), singleAccountInfo('4444.csv', +34570)]
df_list = [df1,df2,df3,df4]
# df_list = [df1]
df = mergeAccountInfo(df_list)

# print(df.dtypes)
# print(df)

# f = open("test1.pkl", "wb")
# pickle.dump(df_list[0], f)
# f.close()
# f = open("test2.pkl", "wb")
# pickle.dump(df_list[1], f)
# f.close()
# f = open("test3.pkl", "wb")
# pickle.dump(df_list[2], f)
# f.close()
# f = open("test4.pkl", "wb")
# pickle.dump(df_list[3], f)
# f.close()

# df1 = singleAccountInfo('1111.csv', -12054)
# df2 = singleAccountInfo('2222.csv', +8806)
# df3 = singleAccountInfo('3333.csv', +382442)








# df1.to_csv('test1.csv', mode='w')
# df2.to_csv('test2.csv', mode='w')
# df3.to_csv('test3.csv', mode='w')

# df1 = pd.read_csv('test1.csv')
# df2 = pd.read_csv('test2.csv')
# df3 = pd.read_csv('test3.csv')








root = Tk()

# root.title(f"{account_name} 계좌 정보 조회")
root.geometry('1920x1080')



fig = Figure(figsize=(20, 4), dpi=100)
ax = fig.add_subplot()

ax.set_title(f'월말 잔고 기록 ({df.index[-1][:4]}년 {df.index[-1][5:7]}월 기준) (세전)')
ax.fill_between(df.index, df['평가잔고'], color="C1", alpha=0.4)
ax.fill_between(df.index, df['투자원금'], color="C0", alpha=0.5)
ax.plot(df.index, df['평가잔고'], color="C1", label='평가금액')
ax.plot(df.index, df['투자원금'], color="C0", label='투자원금')

max_val = math.ceil(max(df['투자원금'].max(), df['평가잔고'].max()) // 10000000)
max_range = max_val * 10000000

x_label = df.index.str.replace('20', '')
x_label = x_label.str.replace('-\d\d$', '월', regex=True)
x_label = x_label.str.replace('-', '년')

ax.set_xticklabels(x_label, rotation=45)

# ax.set_yticks(np.arange(0, max_range, 10000000))

ax.set_ylabel('잔고 (단위: 억)')
ax.grid(color='C7')
ax.legend()


canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=0, column=0, columnspan=4, sticky='nsew')




Grid.rowconfigure(root, index=0, weight=1)

Grid.columnconfigure(root, index=1, weight=1)




def showStocks(date, column, weight):
    lbl = Label(root, borderwidth=1, relief="solid")
    lbl.grid(row=1, column=column, sticky='nsew')
    
    stocks = df['한국주식잔고'][date].add(df['미국주식잔고'][date], fill_value=0)
    stocks['수익률'] = (stocks['현재가'] - stocks['평균단가']) / stocks['평균단가'] * 100
    for col in stocks.columns:
        stocks[col] = round(stocks[col], 2)
    stocks['수량'] = stocks['수량'].astype('int')

    len_us = len(df['미국주식잔고'][date].index)

    Label(lbl, borderwidth=1, relief="solid", text='현재 보유 종목').grid(row=0, column=0, sticky='nsew', columnspan=6)
    Label(lbl, borderwidth=1, relief="solid", text=stocks.index.name).grid(row=1, column=0, sticky='nsew')
    for i, col in enumerate(stocks.columns):
        Label(lbl, borderwidth=1, relief="solid", text=col).grid(row=1, column=1+i, sticky='nsew')

    for i, row in enumerate(stocks.index):
        if len_us + 2 <= 2 + i :
            tp = int
            currency = '원'
        else:
            tp = float
            currency = '$'
        Label(lbl, borderwidth=1, relief="solid", text=row).grid(row=2+i, column=0, sticky='nsew')
        Label(lbl, borderwidth=1, relief="solid", text=f"{stocks['수량'][row]:,}").grid(row=2+i, column=1, sticky='nsew')
        Label(lbl, borderwidth=1, relief="solid", text=f"{tp(stocks['평균단가'][row]):,}{currency}").grid(row=2+i, column=2, sticky='nsew')
        Label(lbl, borderwidth=1, relief="solid", text=f"{tp(stocks['현재가'][row]):,}{currency}").grid(row=2+i, column=3, sticky='nsew')
        Label(lbl, borderwidth=1, relief="solid", text=f"{tp(stocks['수익금'][row]):,}{currency}").grid(row=2+i, column=4, sticky='nsew')
        Label(lbl, borderwidth=1, relief="solid", text=f"{stocks['수익률'][row]:,}%").grid(row=2+i, column=5, sticky='nsew')

    Grid.columnconfigure(root, index=column, weight=weight)
    for i in range(6):
        Grid.columnconfigure(lbl, index=i, weight=weight)
    
def showBeforeTax(date, column, weight):
    lbl = Label(root, borderwidth=1, relief="solid")
    lbl.grid(row=1, column=column, sticky='nsew')
    
    df['세전수익률'] = round(df['수익금액'] / df['투자원금'] * 100, 2)

    Label(lbl, borderwidth=1, relief="solid", text='세전').grid(row=0, column=0, sticky='nsew', columnspan=2)

    Label(lbl, borderwidth=1, relief="solid", text='원금').grid(row=1, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text=f"{df['투자원금'][date]:,}원").grid(row=1, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text='평가금').grid(row=2, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text=f"{df['평가잔고'][date]:,}원").grid(row=2, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text='수익금').grid(row=3, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text=f"{df['수익금액'][date]:,}원").grid(row=3, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text='수익률').grid(row=4, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text=f"{df['세전수익률'][date]:,}%").grid(row=4, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text='배당금 (최근 1년)').grid(row=5, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text=f"{df['전체배당금'][date]:,}원").grid(row=5, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text='원금 대비 배당율 (최근 1년)').grid(row=6, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text=f"{round(df['전체배당금'][date] / df['투자원금'][date] * 100, 2):,}%").grid(row=6, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text='평가금 대비 배당율 (최근 1년)').grid(row=7, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text=f"{round(df['전체배당금'][date] / df['평가잔고'][date] * 100, 2):,}%").grid(row=7, column=1, sticky='nsew')

    Grid.columnconfigure(root, index=column, weight=weight)
    for i in range(2):
        Grid.columnconfigure(lbl, index=i, weight=weight)

def showAfterTax(date, column, weight):
    lbl = Label(root, borderwidth=1, relief="solid")
    lbl.grid(row=1, column=column, sticky='nsew')
    
    df['세후수익률'] = round(df['세후수익금'] / df['투자원금'] * 100, 2)
    df['세후배당금'] = df['전체배당금'] - df['전체배당세']

    Label(lbl, borderwidth=1, relief="solid", text='세후').grid(row=0, column=0, sticky='nsew', columnspan=2)

    Label(lbl, borderwidth=1, relief="solid", text='원금').grid(row=1, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text=f"{df['투자원금'][date]:,}원").grid(row=1, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text='평가금').grid(row=2, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text=f"{df['세후평가금'][date]:,}원").grid(row=2, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text='수익금').grid(row=3, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text=f"{df['세후수익금'][date]:,}원").grid(row=3, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text='수익률').grid(row=4, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text=f"{df['세후수익률'][date]:,}%").grid(row=4, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text='배당금 (최근 1년)').grid(row=5, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text=f"{df['세후배당금'][date]:,}원").grid(row=5, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text='원금 대비 배당율 (최근 1년)').grid(row=6, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text=f"{round(df['세후배당금'][date] / df['투자원금'][date] * 100, 2):,}%").grid(row=6, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text='평가금 대비 배당율 (최근 1년)').grid(row=7, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text=f"{round(df['세후배당금'][date] / df['세후평가금'][date] * 100, 2):,}%").grid(row=7, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text='제비용').grid(row=8, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text=f"{df['제비용'][date]:,}원").grid(row=8, column=1, sticky='nsew')

    Grid.columnconfigure(root, index=column, weight=weight)
    for i in range(2):
        Grid.columnconfigure(lbl, index=i, weight=weight)


showStocks(df.index[-1], 0, 1)
showBeforeTax(df.index[-1], 1, 1)
showAfterTax(df.index[-1], 2, 1)






root.mainloop()






# 버튼이나 실렉트박스 제작해서 정보 날짜별로 바꾸기



# etf 보유종목 현황이나 비율 정도.
# 보유종목 top10 계좌 여러개 보여주고 수익률 등 합산 가능하게, 거래내역 두개 비교해서 전산누락도 확인, 평단과 주식수 체크 (매수날짜의 종가데이터와 스프레드 많이차이나는지, 전산에러만 확인)
# 가장 최근 수수료율 확인시키기



              






# 각 운용사 etf csv 다운로드, 상위 증권사들 가져오면 대부분의 etf 가능할거같음
# https://www.blackrock.com/au/individual/products/275304/fund/1478358644060.ajax?fileType=csv&fileName=IVV_holdings&dataType=fund
# https://www.invesco.com/us/financial-products/etfs/holdings/main/holdings/0?audienceType=Investor&action=download&ticker=QQQM
# https://www.schwabassetmanagement.com/sites/g/files/eyrktu361/files/product_files/SCHD/SCHD_FundHoldings_2021-11-26.CSV?1638005310=

