from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import font_manager, rc
from tkinter import *
from tkinter import filedialog
import math
from tkinter.font import Font

from Converter import VTIQQQM_ratio
from accountInfo import singleAccountInfo, mergeAccountInfo
from mss import mss

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
    Label(root, text='보정금액').grid(row=0, column=2)
    Label(root, text='공모주 수익 (포함: 1, 미포함: 0)').grid(row=0, column=3)
    for i in range(len(csv_list)):
        Label(root, text=csv_list[i]).grid(row=i+1, column=0)
        input_list.append((Entry(root), Entry(root), Entry(root)))
        input_list[-1][0].grid(row=i+1, column=1)
        input_list[-1][1].grid(row=i+1, column=2)
        input_list[-1][2].grid(row=i+1, column=3)

    names = []
    values = []
    IPOs = []
    def submit():
        for tp in input_list:
            name, value, IPO = tp
            names.append(name.get())
            values.append(value.get())
            IPOs.append(IPO.get())
        root.destroy()
    Button(root, text='완료', command=submit).grid(row=len(csv_list)+1, column=2)
    
    root.mainloop()
    return ' + '.join(names), values, IPOs


csv_list = getCSV()
accountNames, values, IPOs = setName(csv_list)

df_list = []
for i in range(len(csv_list)):
    df_list.append(singleAccountInfo(csv_list[i], int(values[i]), int(IPOs[i])))
df = mergeAccountInfo(df_list)





root = Tk()

root.geometry('3000x1618')

bigFont = Font(
    family="맑은 고딕",
    size=30,
)

midFont = Font(
    family="맑은 고딕",
    size=20,
)

fg = 'red'
lbg = '#F0F0F0'

def clearArea(row, col, color):    
    Label(root, bg=color).grid(row=row, column=col, sticky='nsew')

def showGraph():
    fig = Figure(figsize=(30, 30), dpi=150)
    ax = fig.add_subplot()

    ax.set_title(f'[{accountNames} 계좌] 월말 잔고 기록 ({df.index[-1][:4]}년 {df.index[-1][5:7]}월 기준) (세전)', fontdict={'fontsize':20})
    ax.fill_between(df.index, df['평가잔고'], color="C1", alpha=0.4)
    ax.fill_between(df.index, df['투자원금'], color="C0", alpha=0.5)
    ax.plot(df.index, df['평가잔고'], color="C1", label='평가금액')
    ax.plot(df.index, df['투자원금'], color="C0", label='투자원금')

    max_val = max(df['투자원금'].max(), df['평가잔고'].max())
    max_range = math.ceil(max_val * 1.2 / 10000000)
    y_label = []
    y_ticks = []
    for i in range(max_range + 1):
        y_label.append(f'{round(i * 0.1, 1)}억원')
        y_ticks.append(i * 10000000)

    x_label = df.index.str.replace('^20', '', regex=True)
    x_label = x_label.str.replace('-\d\d$', '월', regex=True)
    x_label = x_label.str.replace('-', '년')

    ax.set_xticks(df.index)
    ax.set_xticklabels(x_label, rotation=45)
    
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_label)
    
    ax.grid(color='C7')
    ax.legend(prop={'size': 15}, loc='upper left')

    pos_1 = ax.get_position()
    pos_2 = [pos_1.x0 + -0.05, pos_1.y0 + 0,  pos_1.width / 0.9, pos_1.height / 1]
    ax.set_position(pos_2)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=5)

    Grid.rowconfigure(root, index=0, weight=1)

def showStocks(date, column, weight):
    clearArea(1,column,lbg)
    lbl = Label(root, borderwidth=1, relief="solid", anchor='e')
    lbl.grid(row=1, column=column)

    # 미국주식
    us_lbl = Label(lbl, borderwidth=1, relief="solid")
    us_lbl.grid(row=0, column=column, sticky='nsew')

    us_stocks = df['미국주식잔고'][date]
    us_stocks['평균단가'] = us_stocks['매수금액'] / us_stocks['수량']
    us_stocks['현재가'] = us_stocks['평가금액'] / us_stocks['수량']
    us_stocks['수익금'] = us_stocks['평가금액'] - us_stocks['매수금액']
    us_stocks['수익률'] = us_stocks['수익금'] / us_stocks['매수금액'] * 100

    Label(us_lbl, borderwidth=1, relief="solid", bg=lbg, font=midFont, text='미국 주식 잔고').grid(row=0, column=0, sticky='nsew', columnspan=8)
    Label(us_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text='종목').grid(row=1, column=0, sticky='nsew')
    Label(us_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text='수량').grid(row=1, column=1, sticky='nsew')
    Label(us_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text='평균단가').grid(row=1, column=2, sticky='nsew')
    Label(us_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text='현재가').grid(row=1, column=3, sticky='nsew')
    Label(us_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text='매수금액').grid(row=1, column=4, sticky='nsew')
    Label(us_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text='평가금액').grid(row=1, column=5, sticky='nsew')
    Label(us_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text='수익금').grid(row=1, column=6, sticky='nsew')
    Label(us_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text='수익률').grid(row=1, column=7, sticky='nsew')

    for i, row in enumerate(us_stocks.index):
        Label(us_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text=row).grid(row=2+i, column=0, sticky='nsew')
        Label(us_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text=f"{round(us_stocks['수량'][row]):,}").grid(row=2+i, column=1, sticky='nsew')
        Label(us_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text=f"{round(us_stocks['평균단가'][row]):,} 달러", anchor='e').grid(row=2+i, column=2, sticky='nsew')
        Label(us_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text=f"{round(us_stocks['현재가'][row]):,} 달러", anchor='e').grid(row=2+i, column=3, sticky='nsew')
        Label(us_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text=f"{round(us_stocks['매수금액'][row]):,} 달러", anchor='e').grid(row=2+i, column=4, sticky='nsew')
        Label(us_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text=f"{round(us_stocks['평가금액'][row]):,} 달러", anchor='e').grid(row=2+i, column=5, sticky='nsew')
        Label(us_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text=f"{round(us_stocks['수익금'][row]):,} 달러", anchor='e').grid(row=2+i, column=6, sticky='nsew')
        Label(us_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text=f"{round(us_stocks['수익률'][row], 2):,} %", anchor='e').grid(row=2+i, column=7, sticky='nsew')

    # 여백
    span_lbl = Label(lbl, text=' ', font=midFont, bg=lbg)
    span_lbl.grid(row=2, column=column, sticky='nsew')

    # 한국주식
    kr_lbl = Label(lbl, borderwidth=1, relief="solid")
    kr_lbl.grid(row=3, column=column, sticky='nsew')

    kr_stocks = df['한국주식잔고'][date]
    kr_stocks['평균단가'] = kr_stocks['매수금액'] / kr_stocks['수량']
    kr_stocks['현재가'] = kr_stocks['평가금액'] / kr_stocks['수량']
    kr_stocks['수익금'] = kr_stocks['평가금액'] - kr_stocks['매수금액']
    kr_stocks['수익률'] = kr_stocks['수익금'] / kr_stocks['매수금액'] * 100

    Label(kr_lbl, borderwidth=1, relief="solid", bg=lbg, font=midFont, text='한국 주식 잔고').grid(row=0, column=0, sticky='nsew', columnspan=8)
    Label(kr_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text='종목').grid(row=1, column=0, sticky='nsew')
    Label(kr_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text='수량').grid(row=1, column=1, sticky='nsew')
    Label(kr_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text='평균단가').grid(row=1, column=2, sticky='nsew')
    Label(kr_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text='현재가').grid(row=1, column=3, sticky='nsew')
    Label(kr_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text='매수금액').grid(row=1, column=4, sticky='nsew')
    Label(kr_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text='평가금액').grid(row=1, column=5, sticky='nsew')
    Label(kr_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text='수익금').grid(row=1, column=6, sticky='nsew')
    Label(kr_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text='수익률').grid(row=1, column=7, sticky='nsew')

    for i, row in enumerate(kr_stocks.index):
        Label(kr_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text=row).grid(row=2+i, column=0, sticky='nsew')
        Label(kr_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text=f"{round(kr_stocks['수량'][row]):,}").grid(row=2+i, column=1, sticky='nsew')
        Label(kr_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text=f"{round(kr_stocks['평균단가'][row]):,} 원", anchor='e').grid(row=2+i, column=2, sticky='nsew')
        Label(kr_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text=f"{round(kr_stocks['현재가'][row]):,} 원", anchor='e').grid(row=2+i, column=3, sticky='nsew')
        Label(kr_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text=f"{round(kr_stocks['매수금액'][row]):,} 원", anchor='e').grid(row=2+i, column=4, sticky='nsew')
        Label(kr_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text=f"{round(kr_stocks['평가금액'][row]):,} 원", anchor='e').grid(row=2+i, column=5, sticky='nsew')
        Label(kr_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text=f"{round(kr_stocks['수익금'][row]):,} 원", anchor='e').grid(row=2+i, column=6, sticky='nsew')
        Label(kr_lbl, borderwidth=1, relief="solid", bg=lbg, padx=15, text=f"{round(kr_stocks['수익률'][row], 2):,} %", anchor='e').grid(row=2+i, column=7, sticky='nsew')

    # 그리드 weight 설정
    Grid.columnconfigure(root, index=column, weight=weight)
    Grid.columnconfigure(lbl, index=0, weight=1)
    for i in range(7):
        Grid.columnconfigure(us_lbl, index=i, weight=1)
        Grid.columnconfigure(kr_lbl, index=i, weight=1)
    
def showBeforeTax(date, column, weight):
    clearArea(1,column,lbg)
    lbl = Label(root, borderwidth=1, relief="solid")
    lbl.grid(row=1, column=column)
    
    df['세전수익률'] = round(df['수익금액'] / df['투자원금'] * 100, 2)

    Label(lbl, borderwidth=1, relief="solid", bg=lbg, font=bigFont, text='세전').grid(row=0, column=0, sticky='nsew', columnspan=2)

    Label(lbl, borderwidth=1, relief="solid", bg=lbg, font=bigFont, fg=fg, padx=10, text='원금').grid(row=1, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", bg=lbg, font=bigFont, fg=fg, padx=10, text=f"{df['투자원금'][date]:,}원", anchor='e').grid(row=1, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", bg=lbg, font=bigFont, fg=fg, padx=10, text='평가금').grid(row=2, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", bg=lbg, font=bigFont, fg=fg, padx=10, text=f"{df['평가잔고'][date]:,}원", anchor='e').grid(row=2, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", bg=lbg, font=bigFont, fg=fg, padx=10, text='수익금').grid(row=3, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", bg=lbg, font=bigFont, fg=fg, padx=10, text=f"{df['수익금액'][date]:,}원", anchor='e').grid(row=3, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", bg=lbg, font=bigFont, fg=fg, padx=10, text='수익률').grid(row=4, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", bg=lbg, font=bigFont, fg=fg, padx=10, text=f"{df['세전수익률'][date]:,}%", anchor='e').grid(row=4, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", bg=lbg, text='배당금 (최근 1년)').grid(row=5, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", bg=lbg, text=f"{df['전체배당금'][date]:,} 원", anchor='e').grid(row=5, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", bg=lbg, text='원금 대비 배당율 (최근 1년)').grid(row=6, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", bg=lbg, text=f"{round(df['전체배당금'][date] / df['투자원금'][date] * 100, 2):,} %", anchor='e').grid(row=6, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", bg=lbg, text='평가금 대비 배당율 (최근 1년)').grid(row=7, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", bg=lbg, text=f"{round(df['전체배당금'][date] / df['평가잔고'][date] * 100, 2):,} %", anchor='e').grid(row=7, column=1, sticky='nsew')

    Grid.columnconfigure(root, index=column, weight=weight)
    for i in range(2):
        Grid.columnconfigure(lbl, index=i, weight=weight)

def showAfterTax(date, column, weight):
    clearArea(1,column,lbg)
    lbl = Label(root, borderwidth=1, relief="solid")
    lbl.grid(row=1, column=column)
    
    df['세후수익률'] = round(df['세후수익금'] / df['투자원금'] * 100, 2)
    df['세후배당금'] = df['전체배당금'] - df['전체배당세']

    Label(lbl, borderwidth=1, relief="solid", bg=lbg, font=bigFont, text='세후').grid(row=0, column=0, sticky='nsew', columnspan=2)

    Label(lbl, borderwidth=1, relief="solid", bg=lbg, font=bigFont, fg=fg, padx=10, text='원금').grid(row=1, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", bg=lbg, font=bigFont, fg=fg, padx=10, text=f"{df['투자원금'][date]:,}원", anchor='e').grid(row=1, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", bg=lbg, font=bigFont, fg=fg, padx=10, text='평가금').grid(row=2, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", bg=lbg, font=bigFont, fg=fg, padx=10, text=f"{df['세후평가금'][date]:,}원", anchor='e').grid(row=2, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", bg=lbg, font=bigFont, fg=fg, padx=10, text='수익금').grid(row=3, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", bg=lbg, font=bigFont, fg=fg, padx=10, text=f"{df['세후수익금'][date]:,}원", anchor='e').grid(row=3, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", bg=lbg, font=bigFont, fg=fg, padx=10, text='수익률').grid(row=4, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", bg=lbg, font=bigFont, fg=fg, padx=10, text=f"{df['세후수익률'][date]:,}%", anchor='e').grid(row=4, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", bg=lbg, text='배당금 (최근 1년)').grid(row=5, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", bg=lbg, text=f"{df['세후배당금'][date]:,} 원", anchor='e').grid(row=5, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", bg=lbg, text='원금 대비 배당율 (최근 1년)').grid(row=6, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", bg=lbg, text=f"{round(df['세후배당금'][date] / df['투자원금'][date] * 100, 2):,} %", anchor='e').grid(row=6, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", bg=lbg, text='평가금 대비 배당율 (최근 1년)').grid(row=7, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", bg=lbg, text=f"{round(df['세후배당금'][date] / df['세후평가금'][date] * 100, 2):,} %", anchor='e').grid(row=7, column=1, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", bg=lbg, text='제비용').grid(row=8, column=0, sticky='nsew')
    Label(lbl, borderwidth=1, relief="solid", bg=lbg, text=f"{df['제비용'][date]:,} 원", anchor='e').grid(row=8, column=1, sticky='nsew')

    Grid.columnconfigure(root, index=column, weight=weight)
    for i in range(2):
        Grid.columnconfigure(lbl, index=i, weight=weight)

def showSector(column, vq_weight):
    clearArea(1,column,lbg)
    fig = Figure(figsize=(25, 17), dpi=25)
    fig.set_facecolor(lbg)
    ax = fig.add_subplot()

    labels, ratio = VTIQQQM_ratio(*vq_weight)[1]

    # ratio[labels.index('Cash and/or Derivatives')] += ratio.pop(labels.index('Investment Companies'))
    # labels.pop(labels.index('Investment Companies'))

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

def showHoldings(column, vq_weight):
    clearArea(1,column,lbg)
    fig = Figure(figsize=(25, 17), dpi=25)
    fig.set_facecolor(lbg)
    ax = fig.add_subplot()

    labels, ratio, name = VTIQQQM_ratio(*vq_weight)[0]
    labels = labels[:10]
    ratio = ratio[:10]

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

def showHoldingDetail(vq_weight, balance):
    lbl = Label(root, borderwidth=1, relief="solid")
    lbl.grid(row=0, column=5, rowspan=3)

    stocks, weight, name = VTIQQQM_ratio(*vq_weight)[0]

    Label(lbl, borderwidth=1, relief="solid", bg=lbg, text='보유주식금액').grid(row=0, column=0, sticky='nsew', columnspan=3)
    for i in range(0, 200):
        Label(lbl, borderwidth=1, relief="solid", bg=lbg, text=i+1).grid(row=1+i, column=0, sticky='nsew')
        Label(lbl, borderwidth=1, relief="solid", bg=lbg, text=name[i]).grid(row=1+i, column=1, sticky='nsew')
        Label(lbl, borderwidth=1, relief="solid", bg=lbg, text=f'{round(weight[i] * balance * 0.01):,} 원' ).grid(row=1+i, column=2, sticky='nsew')









def showInfo(date):
    showStocks(date, 0, 5)
    showBeforeTax(date, 1, 5)
    showAfterTax(date, 2, 5)

def captureBtn():
    def clickBtn(monitor):
        filename = filedialog.asksaveasfilename(filetypes=[('png file','.png'),('All files', '*')], title='스크린샷 저장', initialfile=accountNames)
        if not filename.lower().endswith('.png'):
            filename = filename + '.png'
        if filename:
            sct.shot(mon=monitor, output=filename)
    lbl = Label(root)
    lbl.grid(row=2, column=0)
    with mss() as sct:
        for i in range(1, len(sct.monitors)):
            height = sct.monitors[i]['height']
            width = sct.monitors[i]['width']
            Button(lbl, text=f'모니터{i} 캡쳐 [{width}x{height}]', command=lambda i=i: clickBtn(i)).grid(row=0, column=i-1)

def changeDateBtn():
    options = df.index
    clicked = StringVar()
    clicked.set(options[-1])

    drop = OptionMenu(root, clicked, *options, command=showInfo)
    drop.grid(row=2, column=2)

def winFullBtn():
    lbl = Label(root)
    lbl.grid(row=2, column=1)
    Button(lbl, text='창모드', command=lambda: root.attributes('-fullscreen', False)).grid(row=0, column=0)
    Button(lbl, text='풀스크린', command=lambda: root.attributes('-fullscreen', True)).grid(row=0, column=1)


VTI_sum = 0
QQQM_sum = 0
if 'IVV' in df['미국주식잔고'][-1].index:
    VTI_sum += df['미국주식잔고'][-1]['평가금액']['IVV']
if 'VTI' in df['미국주식잔고'][-1].index:
    VTI_sum += df['미국주식잔고'][-1]['평가금액']['VTI']
if 'QQQM' in df['미국주식잔고'][-1].index:
    QQQM_sum += df['미국주식잔고'][-1]['평가금액']['QQQM']

VTI_ratio = VTI_sum / (VTI_sum + QQQM_sum)
QQQM_ratio = QQQM_sum / (VTI_sum + QQQM_sum)

showGraph()

showSector(3,(VTI_ratio,QQQM_ratio))
showHoldings(4,(VTI_ratio,QQQM_ratio))
showHoldingDetail((VTI_ratio,QQQM_ratio), df['평가잔고'][-1])

showInfo(df.index[-1])
captureBtn()
changeDateBtn()
winFullBtn()


for col in df.columns:
    if col == '한국주식잔고' or col == '미국주식잔고':
        pass
    else:
        print(f'{col} : {df[col][-1]}')

root.mainloop()