# 배당금 , 배당율, 수익률, 환율, 그래프 추이 한번 그려주고, etf 보유종목 현황이나 비율 정도.
# 보유주식 잔고, 평가잔고, 평단, 보유종목 top10 계좌 여러개 보여주고 수익률 등 합산 가능하게, 거래내역 두개 비교해서 전산누락도 확인, 평단과 주식수 체크
# 예금과 수익률 비교, 기간, 파일이름을 계좌명으로 출력
# 가장 최근 수수료율 확인시키기

from SHCal import SHCal

cal = SHCal('1111.csv', (2021, 11, 27))

print(cal.deposit())
# print(cal.withdraw())
# print(cal.principal())
# print(cal.USD())
# print(cal.KRW())
# print(cal.USD_RP())
# print(cal.dividend_KR())
# print(cal.dividend_US())
# print(cal.stock_KR())
# print(cal.stock_US())

# https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD


# 외화 RP값은 있다면 수동입력받기


# 남은원화, 남은외화, 해외주식 평단까지 계산해서 세후 실제 수익률 보여주기
# 원금 보정 시점 이후 월 수익률 그래프