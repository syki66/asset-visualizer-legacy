# 신한알파 MTS -> 자산현황 -> [1750] 계좌별 거래내역(원장) -> 기간선택 후 조회 -> 마우스 오른쪽 버튼 -> 엑셀로 내보내기 -> CSV

# 배당금 , 배당율, 수익률, 환율, 그래프 추이 한번 그려주고, etf 보유종목 현황이나 비율 정도.
# 공모주 여부 선택, 보유주식 잔고, 평가잔고, 보유종목 top10 계좌 여러개 보여주고 수익률 등 합산 가능하게, 거래내역 두개 비교해서 전산누락도 확인
# 예금과 수익률 비교, 기간, 파일이름을 계좌명으로 출력
# 가장 최근 수수료율 확인시키기

import csv
from datetime import datetime

def readCSV(file):
    f = open(file, 'r')
    reader = csv.reader(f)

    array = []
    for line in reader:
        array.append(line)
    f.close()

    return array

def preprocessData(list, start_date, end_date):
    '''데이터 전처리 함수'''
    array = []
    for i in range(0, len(list), 2):
        array.append(list[i] + list[i + 1])

    array.pop(0)

    for i in range(len(array)):
        array[i][0] = tuple(map(int, array[i][0].split('.')))

    if datetime(*array[0][0]) > datetime(*array[-1][0]):
        array.reverse()

    start = 0
    end = len(array)
    for i in range(len(array)):
        if datetime(*start_date) > datetime(*array[i][0]):
            start = i + 1
        if datetime(*end_date) >= datetime(*array[i][0]):
            end = i

    return array[start : end]

class Calculator:
    def __init__(self, list):
        self.list = list

    def calculateDW(self):
        '''입금고액, 출금고액 계산 함수'''
        deposit_keyword = ['은행이체입금', '(펌뱅킹)입금']
        withdraw_keyword = ['은행이체출금', '(펌뱅킹)출금', '체크카드승인']

        deposit = 0
        withdraw = 0
        for line in self.list:
            for dkw in deposit_keyword:
                if line[1].endswith(dkw):
                    deposit += int(line[4].replace(',', ''))
                    
            for wkw in withdraw_keyword:
                if line[1].endswith(wkw):
                    withdraw += int(line[4].replace(',', ''))
        
        return deposit, withdraw

    def calculatePrin(self, principal, correction):
        deposit, withdraw = self.calculateDW()
        principal_result = (deposit - withdraw) + (principal + correction)

        return principal_result

    
    # def calculateUSD(list):
    #     '''달러 예수금 (달러 소수점 절사)'''
    #     for i in range(len(list) - 1, -1, -1):
    #         if list[i][2] == 'USD' or list[i][22] == 'USD':
    #             if list[i][23] == '':
    #                 return 0
    #             else:
    #                 return int(list[i][23].replace(',', ''))

    # # def test(list):
    # #     in_kw = ['해외배당금', '외화RP매도입금', '은행이체외화입금']
    # #     out_kw = ['외국납부세액', '외화RP매수출금', ]
    # #     return 0
                
    # def calculateUSDRP(list):
    #     '''달러 RP 잔고 계산'''
    #     for i in range(len(list)):
    #         pass


    # '환전입금', '환전출금','외화RP재투자환매', '외화RP재투자매수', '외화매수환전', 
    # def calculateKRW(list):
    #     '''원화 잔고'''
    #     pass





# test = Calculator([10,20], 30, 40)


rawArray = readCSV('1111.csv')
data = preprocessData(rawArray,(2021, 10, 15), (2021, 11, 18))

cal = Calculator(data)
# cal.calculateDW()
print(cal.calculatePrin(0, 0))



# deposit, withdraw = calculateDW(data, (2021, 10, 15), (2021, 11, 18))
# principal = calculatePrin(deposit, withdraw, 0, 0)

# # USD = (calculateUSD(data))
# USD = (test(data))

# aaaa = []
# for i in data:
#     aaaa.append(i[1])
# print(set(aaaa))


# print(f'입금고액 : {deposit:,}원')
# print(f'출금고액 : {withdraw:,}원')
# print(f'투자 원금 : {principal:,}원')

# print(f'달러 예수금 : {USD}$')


# 주식수 계산은 타사대체입고, 장내매수, 해외증권해외주식매수, 해외증권해외주식매도, 장내매도, 계좌대체입고
# 외화 rp 계산하기

# 남은원화, 남은외화, 해외주식 평단까지 계산해서 세후 실제 수익률 보여주기
# 원금 시점 이후 월 수익률 그래프