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

def preprocessData(list):
    '''데이터 전처리 함수'''
    array = []
    for i in range(0, len(list), 2):
        array.append(list[i] + list[i + 1])

    array.pop(0)

    for i in range(len(array)):
        array[i][0] = tuple(map(int, array[i][0].split('.')))

    if datetime(*array[0][0]) > datetime(*array[-1][0]):
        array.reverse()

    return array

def calculateDW(list, start_date, end_date):
    '''입금고액, 출금고액 계산 함수'''
    deposit_keyword = ['은행이체입금', '(펌뱅킹)입금']
    withdraw_keyword = ['은행이체출금', '(펌뱅킹)출금', '체크카드승인']

    start = 0
    end = len(list)
    for i in range(len(list)):
        if datetime(*start_date) > datetime(*list[i][0]):
            start = i + 1
        if datetime(*end_date) >= datetime(*list[i][0]):
            end = i

    d_sum = 0
    w_sum = 0
    for i in range(start, end + 1):
        for dkw in deposit_keyword:
            if list[i][1].endswith(dkw):
                d_sum += int(list[i][4].replace(',', ''))
                
        for wkw in withdraw_keyword:
            if list[i][1].endswith(wkw):
                w_sum += int(list[i][4].replace(',', ''))
    
    return d_sum, w_sum

def calculatePrin(deposit, withdraw, principal, correction):
    principal_result = (deposit - withdraw) + (principal + correction)

    return principal_result

def calculateUSD(list):
    '''달러 예수금 (달러 소수점 절사)'''
    for i in range(len(list) - 1, -1, -1):
        if list[i][2] == 'USD' or list[i][22] == 'USD':
            if list[i][23] == '':
                return 0
            else:
                return int(list[i][23].replace(',', ''))
            


def calculateKRW(list):
    '''원화 잔고'''
    pass




rawData = readCSV('1111.csv')
data = preprocessData(rawData)

deposit, withdraw = calculateDW(data, (2021, 10, 15), (2021, 11, 18))
principal = calculatePrin(deposit, withdraw, 0, 0)

USD = (calculateUSD(data))

# aaaa = []
# for i in data:
#     aaaa.append(i[1])
# print(set(aaaa))


print(f'입금고액 : {deposit:,}원')
print(f'출금고액 : {withdraw:,}원')
print(f'투자 원금 : {principal:,}원')

print(f'달러 예수금 : {USD}$')


# 주식수 계산은 타사대체입고, 장내매수, 해외증권해외주식매수, 해외증권해외주식매도, 장내매도, 계좌대체입고
# 외화 rp 계산하기

# 남은원화, 남은외화, 해외주식 평단까지 계산해서 세후 실제 수익률 보여주기
# 원금 시점 이후 월 수익률 그래프