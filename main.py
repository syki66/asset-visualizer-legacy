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
from tkinter.font import Font

from Converter import VTIQQQM_ratio


font_path = "C:/WINDOWS/FONTS/MALGUNSL.TTF"
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
# df_list = [df2]
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
root.geometry('2560x1440')

bigFont = Font(
    family="맑은 고딕",
    size=30,
)

midFont = Font(
    family="맑은 고딕",
    size=20,
)

fg = 'red'


def showGraph():
    fig = Figure(figsize=(30, 30), dpi=150)
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

    pos_1 = ax.get_position()
    pos_2 = [pos_1.x0 + -0.05, pos_1.y0 + 0,  pos_1.width / 0.9, pos_1.height / 1]
    ax.set_position(pos_2)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=5)

def showStocks(date, column, weight):
    lbl = Label(root, borderwidth=1, relief="solid", anchor='e')
    lbl.grid(row=1, column=column)

    # 미국주식
    us_lbl = Label(lbl, borderwidth=1, relief="solid")
    us_lbl.grid(row=0, column=column, sticky='nsew')

    us_stocks = df['미국주식잔고'][date]
    us_stocks['수익률'] = (us_stocks['현재가'] - us_stocks['평균단가']) / us_stocks['평균단가'] * 100

    Label(us_lbl, borderwidth=1, relief="solid", font=midFont, text='미국 주식 잔고').grid(row=0, column=0, sticky='nsew', columnspan=6)
    Label(us_lbl, borderwidth=1, relief="solid", padx=15, text=us_stocks.index.name).grid(row=1, column=0, sticky='nsew')
    for i, col in enumerate(us_stocks.columns):
        Label(us_lbl, borderwidth=1, relief="solid", padx=15, text=col).grid(row=1, column=1+i, sticky='nsew')

    for i, row in enumerate(us_stocks.index):
        Label(us_lbl, borderwidth=1, relief="solid", padx=15, text=row).grid(row=2+i, column=0, sticky='nsew')
        Label(us_lbl, borderwidth=1, relief="solid", padx=15, text=f"{round(us_stocks['수량'][row]):,}").grid(row=2+i, column=1, sticky='nsew')
        Label(us_lbl, borderwidth=1, relief="solid", padx=15, text=f"{round(us_stocks['평균단가'][row], 2):,} 달러", anchor='e').grid(row=2+i, column=2, sticky='nsew')
        Label(us_lbl, borderwidth=1, relief="solid", padx=15, text=f"{round(us_stocks['현재가'][row], 2):,} 달러", anchor='e').grid(row=2+i, column=3, sticky='nsew')
        Label(us_lbl, borderwidth=1, relief="solid", padx=15, text=f"{round(us_stocks['수익금'][row], 2):,} 달러", anchor='e').grid(row=2+i, column=4, sticky='nsew')
        Label(us_lbl, borderwidth=1, relief="solid", padx=15, text=f"{round(us_stocks['수익률'][row], 2):,} %", anchor='e').grid(row=2+i, column=5, sticky='nsew')

    # 여백
    span_lbl = Label(lbl, text=' ', font=midFont)
    span_lbl.grid(row=2, column=column, sticky='nsew')

    # 한국주식
    kr_lbl = Label(lbl, borderwidth=1, relief="solid")
    kr_lbl.grid(row=3, column=column, sticky='nsew')

    kr_stocks = df['한국주식잔고'][date]
    kr_stocks['수익률'] = (kr_stocks['현재가'] - kr_stocks['평균단가']) / kr_stocks['평균단가'] * 100

    Label(kr_lbl, borderwidth=1, relief="solid", font=midFont, text='한국 주식 잔고').grid(row=0, column=0, sticky='nsew', columnspan=6)
    Label(kr_lbl, borderwidth=1, relief="solid", padx=15, text=kr_stocks.index.name).grid(row=1, column=0, sticky='nsew')
    for i, col in enumerate(kr_stocks.columns):
        Label(kr_lbl, borderwidth=1, relief="solid", padx=15, text=col).grid(row=1, column=1+i, sticky='nsew')

    for i, row in enumerate(kr_stocks.index):
        Label(kr_lbl, borderwidth=1, relief="solid", padx=15, text=row).grid(row=2+i, column=0, sticky='nsew')
        Label(kr_lbl, borderwidth=1, relief="solid", padx=15, text=f"{round(kr_stocks['수량'][row]):,}").grid(row=2+i, column=1, sticky='nsew')
        Label(kr_lbl, borderwidth=1, relief="solid", padx=15, text=f"{round(kr_stocks['평균단가'][row]):,} 원", anchor='e').grid(row=2+i, column=2, sticky='nsew')
        Label(kr_lbl, borderwidth=1, relief="solid", padx=15, text=f"{round(kr_stocks['현재가'][row]):,} 원", anchor='e').grid(row=2+i, column=3, sticky='nsew')
        Label(kr_lbl, borderwidth=1, relief="solid", padx=15, text=f"{round(kr_stocks['수익금'][row]):,} 원", anchor='e').grid(row=2+i, column=4, sticky='nsew')
        Label(kr_lbl, borderwidth=1, relief="solid", padx=15, text=f"{round(kr_stocks['수익률'][row], 2):,} %", anchor='e').grid(row=2+i, column=5, sticky='nsew')

    # 그리드 weight 설정
    Grid.columnconfigure(root, index=column, weight=weight)
    Grid.columnconfigure(lbl, index=0, weight=1)
    for i in range(6):
        Grid.columnconfigure(us_lbl, index=i, weight=1)
        Grid.columnconfigure(kr_lbl, index=i, weight=1)
    
def showBeforeTax(date, column, weight):
    lbl = Label(root, borderwidth=1, relief="solid")
    lbl.grid(row=1, column=column)
    
    df['세전수익률'] = round(df['수익금액'] / df['투자원금'] * 100, 2)

    Label(lbl, borderwidth=1, relief="solid", font=bigFont, text='세전').grid(row=0, column=0, sticky='nsew', columnspan=2)

    Label(lbl, borderwidth=1, relief="solid", font=bigFont, fg=fg, padx=10, text='원금').grid(row=1, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", font=bigFont, fg=fg, padx=10, text=f"{df['투자원금'][date]:,}원", anchor='e').grid(row=1, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", font=bigFont, fg=fg, padx=10, text='평가금').grid(row=2, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", font=bigFont, fg=fg, padx=10, text=f"{df['평가잔고'][date]:,}원", anchor='e').grid(row=2, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", font=bigFont, fg=fg, padx=10, text='수익금').grid(row=3, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", font=bigFont, fg=fg, padx=10, text=f"{df['수익금액'][date]:,}원", anchor='e').grid(row=3, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", font=bigFont, fg=fg, padx=10, text='수익률').grid(row=4, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", font=bigFont, fg=fg, padx=10, text=f"{df['세전수익률'][date]:,}%", anchor='e').grid(row=4, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text='배당금 (최근 1년)').grid(row=5, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text=f"{df['전체배당금'][date]:,} 원", anchor='e').grid(row=5, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text='원금 대비 배당율 (최근 1년)').grid(row=6, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text=f"{round(df['전체배당금'][date] / df['투자원금'][date] * 100, 2):,} %", anchor='e').grid(row=6, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text='평가금 대비 배당율 (최근 1년)').grid(row=7, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text=f"{round(df['전체배당금'][date] / df['평가잔고'][date] * 100, 2):,} %", anchor='e').grid(row=7, column=1, sticky='nsew')

    Grid.columnconfigure(root, index=column, weight=weight)
    for i in range(2):
        Grid.columnconfigure(lbl, index=i, weight=weight)

def showAfterTax(date, column, weight):
    lbl = Label(root, borderwidth=1, relief="solid")
    lbl.grid(row=1, column=column)
    
    df['세후수익률'] = round(df['세후수익금'] / df['투자원금'] * 100, 2)
    df['세후배당금'] = df['전체배당금'] - df['전체배당세']

    Label(lbl, borderwidth=1, relief="solid", font=bigFont, text='세후').grid(row=0, column=0, sticky='nsew', columnspan=2)

    Label(lbl, borderwidth=1, relief="solid", font=bigFont, fg=fg, padx=10, text='원금').grid(row=1, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", font=bigFont, fg=fg, padx=10, text=f"{df['투자원금'][date]:,}원", anchor='e').grid(row=1, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", font=bigFont, fg=fg, padx=10, text='평가금').grid(row=2, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", font=bigFont, fg=fg, padx=10, text=f"{df['세후평가금'][date]:,}원", anchor='e').grid(row=2, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", font=bigFont, fg=fg, padx=10, text='수익금').grid(row=3, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", font=bigFont, fg=fg, padx=10, text=f"{df['세후수익금'][date]:,}원", anchor='e').grid(row=3, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", font=bigFont, fg=fg, padx=10, text='수익률').grid(row=4, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", font=bigFont, fg=fg, padx=10, text=f"{df['세후수익률'][date]:,}%", anchor='e').grid(row=4, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text='배당금 (최근 1년)').grid(row=5, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text=f"{df['세후배당금'][date]:,} 원", anchor='e').grid(row=5, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text='원금 대비 배당율 (최근 1년)').grid(row=6, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text=f"{round(df['세후배당금'][date] / df['투자원금'][date] * 100, 2):,} %", anchor='e').grid(row=6, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text='평가금 대비 배당율 (최근 1년)').grid(row=7, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text=f"{round(df['세후배당금'][date] / df['세후평가금'][date] * 100, 2):,} %", anchor='e').grid(row=7, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text='제비용').grid(row=8, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", text=f"{df['제비용'][date]:,} 원", anchor='e').grid(row=8, column=1, sticky='nsew')

    Grid.columnconfigure(root, index=column, weight=weight)
    for i in range(2):
        Grid.columnconfigure(lbl, index=i, weight=weight)

def showSector(column):
    fig = Figure(figsize=(25, 17), dpi=25)
    ax = fig.add_subplot()

    labels, ratio = VTIQQQM_ratio(0.5,0.5)[1]

    ratio[labels.index('Cash and/or Derivatives')] += ratio.pop(labels.index('Investment Companies'))
    labels.pop(labels.index('Investment Companies'))

    ratio = [str(round(num, 1)).rjust(4,' ') for num in ratio]

    for i in range(len(labels)):
        if labels[i] == 'Information Technology': labels[i] = f'{ratio[i]}% IT'
        if labels[i] == 'Consumer Discretionary': labels[i] = f'{ratio[i]}% 임의소비재'
        if labels[i] == 'Communication Services': labels[i] = f'{ratio[i]}% 통신'
        if labels[i] == 'Health Care': labels[i] = f'{ratio[i]}% 헬스케어'
        if labels[i] == 'Industrials': labels[i] = f'{ratio[i]}% 산업'
        if labels[i] == 'Financials': labels[i] = f'{ratio[i]}% 금융'
        if labels[i] == 'Consumer Staples': labels[i] = f'{ratio[i]}% 필수소비재'
        if labels[i] == 'Real Estate': labels[i] = f'{ratio[i]}% 부동산'
        if labels[i] == 'Utilities': labels[i] = f'{ratio[i]}% 유틸리티'
        if labels[i] == 'Energy': labels[i] = f'{ratio[i]}% 에너지'
        if labels[i] == 'Materials': labels[i] = f'{ratio[i]}% 원자재'
        if labels[i] == 'Cash and/or Derivatives': labels[i] = f'{ratio[i]}% 기타'

    ax.set_title('섹터 구성', fontdict={'fontsize':100})

    wedgeprops={'width': 0.5, 'edgecolor': 'black', 'linewidth': 5}
    colors = ['C0','C1','C2','C3','C4','C5','C6','C7','C8','C9','darkslategray','black']
    ax.pie(ratio, counterclock=False, startangle=90, wedgeprops=wedgeprops, colors=colors)
    ax.legend(labels, prop={'size': 58}, bbox_to_anchor=(1, 1.05))
    
    pos_1 = ax.get_position()
    pos_2 = [pos_1.x0 + -0.3, pos_1.y0 + -0.2,  pos_1.width / 0.8, pos_1.height / 0.8]
    ax.set_position(pos_2)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=column)

    Grid.columnconfigure(root, index=column, weight=1)

def showHoldings(column):
    fig = Figure(figsize=(25, 17), dpi=25)
    ax = fig.add_subplot()

    labels, ratio = VTIQQQM_ratio(0.5,0.5)[0]

    top_sum = round(sum(map(float, ratio)), 2)
    ratio = [str(round(num, 1)).rjust(4,' ') for num in ratio]
    
    labels.append('나머지')
    ratio.append(round(100 - top_sum, 1))

    for i in range(len(labels)):
        labels[i] = f'{ratio[i]}% {labels[i]}'

    ax.set_title(f'상위 10종목 : {top_sum}%', fontdict={'fontsize':100})

    wedgeprops={'width': 0.5, 'edgecolor': 'black', 'linewidth': 5}
    colors = ['C0','C1','C2','C3','C4','C5','C6','C7','C8','C9','darkslategray']
    ax.pie(ratio, counterclock=False, startangle=90, wedgeprops=wedgeprops, colors=colors)
    ax.legend(labels, prop={'size': 58}, bbox_to_anchor=(1, 1.05))
    
    pos_1 = ax.get_position()
    pos_2 = [pos_1.x0 + -0.3, pos_1.y0 + -0.2,  pos_1.width / 0.8, pos_1.height / 0.8]
    ax.set_position(pos_2)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=column)

    Grid.columnconfigure(root, index=column, weight=1)



def showInfo(date):
    showStocks(date, 0, 5)
    showBeforeTax(date, 1, 5)
    showAfterTax(date, 2, 5)
    showSector(3)
    showHoldings(4)

def changeDate():
    options = df.index
    clicked = StringVar()
    clicked.set(options[-1])

    drop = OptionMenu(root, clicked, *options, command=showInfo)
    drop.grid(row=2, column=1)

def init():
    Grid.rowconfigure(root, index=0, weight=1)
    # Grid.rowconfigure(root, index=1, weight=1)
    # Grid.rowconfigure(root, index=2, weight=1)
    showGraph()
    showInfo(df.index[-1])
    changeDate()



init()


# print(VTIQQQM_ratio(0.5,0.5)[0])
# print(VTIQQQM_ratio(0.5,0.5)[1])


# 종목 top 30~50정도 원화로 환전해서 보유종목 얼마 들어갔나 보여주기

# 날짜바꿀때 기존 grid 삭제했다가 다시 보여주기


root.mainloop()




# etf 보유종목 현황이나 비율 정도.
# 보유종목 top10 계좌 여러개 보여주고 수익률 등 합산 가능하게, 거래내역 두개 비교해서 전산누락도 확인, 평단과 주식수 체크 (매수날짜의 종가데이터와 스프레드 많이차이나는지, 전산에러만 확인)
# 가장 최근 수수료율 확인시키기

