import requests
import json
import time
from datetime import datetime

data = requests.get(
    'https://api-gateway.coinone.co.kr/exchange/chart/v1/KRW/ETH?lastDt=1689980400000&interval=1H&1691420424423')

# data -> json 타입
# python에서 다루기 위해 dictionary로 변환

dict = json.loads(data.content)

# 필요한 정보인 close와 volume을 찾아보기 ( 첫번째 인덱스의 )
print('첫번째 인덱스의 종가', dict['body']['candles'][0]['close'])
print('첫번째 인덱스의 거래량', dict['body']['candles'][0]['volume'])

# 위의 정보를 반복문을 이용해서 리스트에 담기
closePriceETH = []

for i in range(len(dict['body']['candles'])):
    closePriceETH.append(dict['body']['candles'][i]['close'])

print('종가 리스트', closePriceETH)

# volumeETH = []

# for i in range(len(dict['body']['candles'])):
#     volumeETH.append(dict['body']['candles'][i]['volume'])

# print('거래량 리스트', volumeETH)


# epoch / UNIX 시간 -> 년월일시분초 변환
# epoch 시간은 10자리임 / / 뒤 부분은 밀리초나 마이크로초와 같이 좀 더 정밀한 시간단위를 위해 사용
# 성능 측정, 로깅, 타이밍 분석 등에서 밀리초나 마이크로초 단위의 시간 정보가 필요할 수도 있음
timeETH = []

for i in range(len(dict['body']['candles'])):
    knowTime = time.strftime(   # string format time
        '%Y-%m-%d %H:%M:%S', time.localtime(dict['body']['candles'][i]['dt']/1000))
    timeETH.append(knowTime)

print('시간 리스트', timeETH)


# 시간 - 종가 단위로 묶어서 딕셔너리로 표현
timeCloseETH = {}
for i in timeETH:
    for j in closePriceETH:
        timeCloseETH[i] = j

print(timeCloseETH)


# 특정 시간대의 가격 정보 뿐만 아니라 다른 시간대의 가격 정보도 가져오려면?
# 주소를 분석하기                                                                   1시간 간격    # 지워도 json 파일 변화 X
# https://api-gateway.coinone.co.kr/exchange/chart/v1/KRW/ETH?lastDt=1689980400000&interval=1H&1691420424423
# 원 코인이름   시간이 1689980400000 이전인 정보 전까지
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1691243100)))


# 함수로 만들기
# 입력 날짜(형식: '2023-08-08 07:00:00' 부터 현재까지에 대한 종가 정보)
# 정보는 총 200개씩 넘겨줌
# 입력 날짜 & 시간을 epoch 시간으로 변경
# 첫 번째 자료와 마지막 자료의 epoch 시간 차이 계산
# 다음 lastDT값은 이전 값에서 720000000 만큼을 추가함

def 시간별ETH종가확인(시간):
    # 현재 시간을 epoch 시간으로 변환
    리스트 = []
    current_time = time.time()
    # timestamp를 사용하기 위해서 datetime을 이용해서 문자열 -> 시간 데이터로 변환

    i = datetime.strptime(시간, '%Y-%m-%d %H:%M:%S').timestamp()
    i = int(i * 1000)
    while i < int(current_time)*1000:
        data = requests.get(
            f'https://api-gateway.coinone.co.kr/exchange/chart/v1/KRW/ETH?lastDt={i}&interval=1H')
        dict = json.loads(data.content)
        print('딕샤너리 구분', dict)
        for j in range(len(dict['body']['candles'])):
            리스트.append(dict['body']['candles'][j]['close'])
        i += 720000000

    return 리스트


print(시간별ETH종가확인('2023-07-16 01:00:00'))

# 해결해야 할 문제
# 1. 함수가 주어진 시간부터 ~~~ 현재시간까지의 정보를 가져오는게 아닌 주어진 시간에서부터 720000 에폭시 시간, 즉 8일 8시간 정도 전부터의
# 자료에서부터 현재 시간까지의 정보를 가져오는중
# 2. 현재 시간까지의 정보에서 정말 현재 시간까지의 정보를 제대로 가져오고 있는지 불명확함 => 체크해봐야 함
