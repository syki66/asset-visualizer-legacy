# 신한알파 MTS -> 자산현황 -> [1750] 계좌별 거래내역(원장) -> 기간선택 후 조회 -> 마우스 오른쪽 버튼 -> 엑셀로 내보내기 -> CSV

# 배당금 , 원금(보정), 배당율, 수익률, 환율, 그래프 추이 한번 그려주고, etf 보유종목 현황이나 비율 정도.
# 공모주 여부 선택, 보유주식 잔고, 평가잔고, 보유종목 top10 계좌 여러개 보여주고 수익률 등 합산 가능하게, 거래내역 두개 비교해서 전산누락도 확인
# 외화 평단

import csv

def readCSV(file):
    '''csv 읽고, 리스트로 리턴해주는 함수'''
    f = open(file, 'r')
    reader = csv.reader(f)

    array = []
    for line in reader:
        array.append(line)
    f.close()

    return array

def parsedArray(list):
    '''배열 2줄을 하나로 묶어주고 리스트 리턴'''
    array = []
    for i in range(0, len(list), 2):
        array.append(list[i] + list[i + 1])
    return array

# 결과에 대한 보정값이나 특정 시점에 기준값을 받아서 계산하는 방식으로하기
def calculatePrin(list, **value):
    '''투입 원금 계산기'''
    deposit_kw = ['은행이체입금', '(펌뱅킹)입금']
    withdraw_kw = ['은행이체출금', '(펌뱅킹)출금', '체크카드승인']

    d_sum = 0
    w_sum = 0
    for i in range(len(list)):
        for dkw in deposit_kw:
            if list[i][1].endswith(dkw):
                d_sum += int(list[i][4].replace(',', ''))
        for wkw in withdraw_kw:
            if list[i][1].endswith(wkw):
                w_sum += int(list[i][4].replace(',', ''))
    print(d_sum, w_sum)

test = readCSV('1111.csv')
calculatePrin(parsedArray(test))

