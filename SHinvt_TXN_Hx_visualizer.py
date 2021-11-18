# 신한알파 MTS -> 자산현황 -> [1750] 계좌별 거래내역(원장) -> 기간선택 후 조회 -> 마우스 오른쪽 버튼 -> 엑셀로 내보내기 -> CSV

# 배당금 , 배당율, 수익률, 환율, 그래프 추이 한번 그려주고, etf 보유종목 현황이나 비율 정도.
# 공모주 여부 선택, 보유주식 잔고, 평가잔고, 보유종목 top10 계좌 여러개 보여주고 수익률 등 합산 가능하게, 거래내역 두개 비교해서 전산누락도 확인
# 예금과 수익률 비교, 기간, 파일이름을 계좌명으로 출력
# 현재 수수료율

import csv
from datetime import datetime

def readCSV(file):
    '''csv 읽고, 리스트로 리턴해주는 함수'''
    f = open(file, 'r')
    reader = csv.reader(f)

    array = []
    for line in reader:
        array.append(line)
    f.close()

    return array

def parseData(list):
    '''배열 2줄을 1줄로 묶고, 컬럼제거, 날짜 기준 오름차순 정렬, 날짜 정수변환 후 튜플로 묶기'''
    array = []
    for i in range(0, len(list), 2):
        array.append(list[i] + list[i + 1])

    array.sort()
    array.pop(-1)

    for i in range(len(array)):
        array[i][0] = tuple(map(int, array[i][0].split('.')))

    return array

def calculatePrin(list, start_date, end_date, principal, correction):
    '''투입 원금 계산기'''
    deposit_kw = ['은행이체입금', '(펌뱅킹)입금']
    withdraw_kw = ['은행이체출금', '(펌뱅킹)출금', '체크카드승인']

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
        for dkw in deposit_kw:
            if list[i][1].endswith(dkw):
                d_sum += int(list[i][4].replace(',', ''))
                
        for wkw in withdraw_kw:
            if list[i][1].endswith(wkw):
                w_sum += int(list[i][4].replace(',', ''))

    principal_result = d_sum - w_sum + principal + correction

    return d_sum, w_sum, principal_result



test = readCSV('1111.csv')
array = parseData(test)
t1, t2, t3 = calculatePrin(array, (2021, 10, 15), (2021, 11, 18), 0, 0)

aaaa = []
for i in array:
    aaaa.append(i[1])
print(set(aaaa))


print(f'입금고액 : {t1:,}원')
print(f'출금고액 : {t2:,}원')
print(f'투자 원금 : {t3:,}원')


# 주식수 계산은 타사대체입고, 장내매수, 해외증권해외주식매수, 해외증권해외주식매도, 장내매도, 계좌대체입고
# 남은 원화는 가장 최근의 원화 최종금액, 외화는 rp 등 고려해서 계산되나