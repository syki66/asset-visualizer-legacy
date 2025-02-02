# asset-visualizer-legacy

[새 버전 저장소 링크](https://github.com/syki66/asset-visualizer)

# asset-visualizer

신금투 종합거래내역을 입력받아서, 계좌 정보를 시각화 해주는 프로그램

python으로 제작되었으며, pandas, numpy, matplotlib, BeautifulSoup 등의 라이브러리를 이용하여 제작함

|실행 화면 (가상 정보)|
|:---:|
|![fake](https://user-images.githubusercontent.com/59393359/150634014-cf2d8a6a-9c57-4cf6-8b34-bdcb2c0b7785.png)|

---

## Feature

- 계좌 여러개를 합산해서 계산 가능
- 원금값 보정 가능
- 월별 잔고 추이 그래프 (투자원금, 평가잔고)
- 시점별 보유 주식 잔고 확인
- 시점별 세전 세후 계좌정보 표시
    - `투자원금`, `평가금`, `수익금`, `수익률`, `배당금`, `배당율`, `제비용` 등
- 특정 ETF일 경우, 섹터구성 및 주식 보유량 그래프 시각화
- 공모주 수익 포함 여부 선택

---

## Usage

1. 신한금융투자 거래내역 가져오기
    - 신한알파 HTS -> 자산현황 -> [1750] 계좌별 거래내역(원장) -> 기간선택 후 조회 -> 마우스 오른쪽 버튼 -> 엑셀로 내보내기 -> CSV
2. `SHinvest_visualizer.exe` 실행
    - CSV 1개 또는 여러개 선택 -> `계좌명`과 `보정금액` 입력 -> `완료` 클릭

---

## Caution

- 4k 해상도에 최적화 됨
- 외화RP의 경우 이자 추적이 불가능해서 정확하게 계산하려면 직접 입력해야됨
- 금현물 계좌의 경우 입금 출금 추적만 가능하고 수익률 추적 못함
- 외화잔고는 거래내역 파일의 정보부족으로 인해 소수점이하 절사됨
- SHCal 클래스는 거래내역 처음부터 입력 날짜값까지 계산 (특정기간의 값을 원한다면 차집합 이용하기)
- `은행이체외화입금`과 `타사대체입고`는 이전날짜 중 가장 최근의 `환전입금(USD)` 값을 불러와서 원화로 계산함 (기본값 1150원)
- 보정값을 입력받으면 `은행이체입금` 형식으로 거래내역에 가장 빠른날짜로 삽입됨

---

## Change Log

- [CHANGELOG.MD](https://github.com/syki66/SHinvest_visualizer/blob/master/CHANGELOG.MD)

---

## Todo List

- FutureWarning 오류 해결
- 공모주 수수료 계산 추가
- 그래프에 예금과 수익률 추가
- 전산오류 검출
- 그래프 y축 가격 20단계로 고정하기
- 로그 스케일 선택
- 수익률 마이너스일 경우 세금 계산
- Web 또는 모바일 앱 기반으로 변경

---

## Build

```
pyinstaller --onefile --add-data "C:/Users/syki66/AppData/Local/Programs/Python/Python39/Lib/site-packages/matplotlib/mpl-data/matplotlibrc;." main.py
```
