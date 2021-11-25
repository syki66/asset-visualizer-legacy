import csv
from datetime import datetime

class SHCal:
    def __init__(self, csv, cor, prin):
        raw_list = self.readCSV(csv)
        self.full_list, self.crop_list = self.preprocessData(raw_list, cor)
        self.prin = prin

    def readCSV(self, file):
        '''CSV 읽기'''
        f = open(file, 'r')
        reader = csv.reader(f)
        array = []
        for line in reader:
            array.append(line)
        f.close()
        return array

    def preprocessData(self, list, cor_date):
        '''데이터 전처리'''
        array = []
        for i in range(0, len(list), 2):
            array.append(list[i] + list[i + 1])
        array.pop(0)
        for i in range(len(array)):
            for j in range(len(array[i])):
                if array[i][j] == '':
                    array[i][j] = '0'
        for i in range(len(array)):
            array[i][0] = tuple(map(int, array[i][0].split('.')))
            array[i][4] = float(array[i][4].replace(',', ''))
            array[i][23] = float(array[i][23].replace(',', ''))
            array[i][10] = float(array[i][10].replace(',', ''))
            array[i][20] = float(array[i][20].replace(',', ''))
            array[i][16] = float(array[i][16].replace(',', ''))
            array[i][3] = int(float(array[i][3].replace(',', '')))
        if datetime(*array[0][0]) > datetime(*array[-1][0]):
            array.reverse()
        start = 0
        for i in range(len(array)):
            if datetime(*cor_date) > datetime(*array[i][0]):
                start = i + 1
        return array, array[start:]

    def deposit(self):
        '''입금고액'''
        keyword = ['은행이체입금', '(펌뱅킹)입금']
        deposit = 0
        for line in self.crop_list:
            for kw in keyword:
                if line[1].endswith(kw):
                    deposit += line[4]
        return deposit
    
    def withdraw(self):
        '''출금고액'''
        keyword = ['은행이체출금', '(펌뱅킹)출금', '체크카드승인']
        withdraw = 0
        for line in self.crop_list:
            for kw in keyword:
                if line[1].endswith(kw):
                    withdraw += line[4]
        return withdraw

    def principal(self):
        '''투자원금'''
        principal_result = (self.deposit() - self.withdraw()) + self.prin
        return principal_result

    def USD(self):
        '''달러 예수금 (소수점 절사)'''
        for line in list(reversed(self.full_list)):
            if line[2] == 'USD' or line[22] == 'USD':
                return line[23]

    def KRW(self):
        '''원화 예수금'''
        for line in list(reversed(self.full_list)):
            if line[2] != 'USD' and line[22] != 'USD':
                return line[23]

    def USD_RP(self):
        '''달러 RP 잔고 (이자 추적 불가)'''
        deposit = 0
        withdraw = 0
        for line in self.full_list:
            if line[1] == '외화RP매도입금':
                withdraw += line[10]
            if line[1] == '외화RP매수출금':
                deposit += line[10]
        return round(deposit - withdraw, 2)

    def dividend_US(self):
        '''미국주식 배당금'''
        div = 0
        tax = 0
        for line in self.full_list:
            if line[1] == '해외배당금':
                div += line[10]
            if line[1] == '외국납부세액':
                tax += line[10]
        return div, tax

    def dividend_KR(self):
        '''국내주식 배당금'''
        div = 0
        tax = 0
        for line in self.full_list:
            if line[1] == '배당금':
                div += line[4]
                tax += line[20]
        return div, tax

    def stock_US(self):
        '''미국주식 잔고'''
        dict = {}
        for line in self.full_list:
            if line[1] == '해외증권해외주식매수' or line[1] == '타사대체입고':
                if not line[2] in dict:
                    dict[line[2]] = []
                for _ in range(line[3]):
                    dict[line[2]].append(line[16])
            if line[1] == '해외증권해외주식매도':
                for _ in range(line[3]):
                    dict[line[2]].pop(0)
        trash = []
        for key in dict.keys():
            if not dict[key]:
                trash.append(key)
        for t in trash:
            del dict[t]
        return dict

    def stock_KR(self):
        '''국내주식 잔고'''
        dict = {}
        for line in self.full_list:
            if line[1] == '계좌대체입고' or line[1] == '장내매수':
                if not line[2] in dict:
                    dict[line[2]] = []
                for _ in range(line[3]):
                    dict[line[2]].append(line[16])
            if line[1] == '장내매도':
                for _ in range(line[3]):
                    dict[line[2]].pop(0)
        trash = []
        for key in dict.keys():
            if not dict[key]:
                trash.append(key)
        for t in trash:
            del dict[t]
        return dict