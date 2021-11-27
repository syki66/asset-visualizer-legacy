# SHinvest_visualizer


---

## Feature

-

---

## Usage

- 신한알파 MTS -> 자산현황 -> [1750] 계좌별 거래내역(원장) -> 기간선택 후 조회 -> 마우스 오른쪽 버튼 -> 엑셀로 내보내기 -> CSV

---

## Caution

- 외화RP의 경우 이자 추적이 불가능해서 정확하게 계산하려면 직접 입력해야됨
- 외화잔고는 거래내역 파일의 정보부족으로 인해 소수점이하 절사됨
- SHCal 클래스는 거래내역 처음부터 입력 날짜값까지 계산 (특정기간의 값을 원한다면 차집합 이용하기)
- `은행이체외화입금`과 `타사대체입고`는 이전날짜 중 가장 최근의 `환전입금(USD)` 값을 불러와서 원화로 계산함 (기본값 1150원)
- 보정값을 입력받으면 `은행이체입금` 형식으로 거래내역에 가장 빠른날짜로 삽입됨

---

## Change Log

- [CHANGELOG.MD](https://github.com/syki66/SHinvest_visualizer/blob/master/CHANGELOG.MD)

---

## Todo List

- 공모주 on/off 추가

---

## Build
