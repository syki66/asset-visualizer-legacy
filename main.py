

from SHinvest_visualizer import accountInfo

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import font_manager, rc
import numpy as np

font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)


year = []
principal = []
balance = []




# for line in accountInfo('3333.csv', -12054):
#     year.insert(0, line['날짜'])
#     principal.insert(0, line['투자원금'])
#     balance.insert(0, line['평가잔고'])
#     # print(line['수익금액'])
#     # print(line['수익률'])



# profit = balance - principal
# print(profit)
# # ypos = np.array(len(year))
# plt.title('월말 잔고 기록')

# 회색 분홍 초록
# 스택으로 

# plt.bar(year, principal)
# plt.bar(year, profit, bottom=principal)

# plt.bar(year, balance, label='평가금액', color='C1', alpha=0.8, width=0.6)
# plt.bar(year, principal, label='투자원금', color='C0', alpha=0.8)

year = np.array([1,2,3,4,5,6,7,8,9,10])
principal = np.array([10,25,20,30,25,50,70,100,90,130])
balance =  np.array([13,14,50,30,60,30,100,200,50,80])

# plt.ylabel('잔고')

# bal_bar = plt.bar(year, balance, color='C0')
# prin_bar = plt.bar(year, principal, color='C0')



# Change the style of plot
# plt.style.use('seaborn-darkgrid')
 
# Make the same graph
plt.fill_between(year, balance, color="C1", alpha=0.4)
plt.fill_between(year, principal, color="C0", alpha=0.5)
plt.plot(year, balance, color="C1", label='평가금액')
plt.plot(year, principal, color="C0", label='투입원금')

max_val = max(principal.max(), balance.max())
max_range = (((max_val) // 10000000 + 1) * 2) * 10000000

plt.yticks(np.arange(0,max_range, 10000000))

 
# Add titles
plt.title("An area chart", loc="left")
plt.xlabel("Value of X")
plt.ylabel("Value of Y")

plt.grid(True)
plt.legend()

# Show the graph
plt.show()


# for i in range(len(year)):
#     if principal[i] < balance[i]:
#         bal_bar[i].set_color('C1')
#         prin_bar[i].set_color('C0')
#     if principal[i] > balance[i]:
#         prin_bar[i].set_zorder(0)
#         bal_bar[i].set_zorder(1)
#         prin_bar[i].set_color('C0')
#         bal_bar[i].set_color('C0')
#         prin_bar[i].set_alpha(0.2)

# C0_patch = mpatches.Patch(color='C0', alpha=0.2, label='손실금')
# C1_patch = mpatches.Patch(color='C1', label='수익금')
# plt.legend(handles=[C0_patch, C1_patch])

plt.show()






# for line in accountInfo('2222.csv', +8806):
#     for key in line.keys():
#         print(f'{key} : {line[key]}')
#     print('')

# for line in accountInfo('3333.csv', +382442):
#     for key in line.keys():
#         print(f'{key} : {line[key]}')
#     print('')




# 불러온 계좌 체크박스 누른것들 합산해서 계산되게끔