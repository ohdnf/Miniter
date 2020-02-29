import requests
import json


api = "https://www.nlotto.co.kr/common.do?method=getLottoNumber&drwNo={round}"
keys = ("totSellamnt", "returnValue", "drwNoDate", "firstWinamnt", "drwtNo6", "drwtNo4", "firstPrzwnerCo","drwtNo5", "bnusNo", "firstAccumamnt", "drwNo", "drwtNo2", "drwtNo3", "drwtNo1")

# for num in range(887, 800, -1):

num = 887
url = api.format(round=num)

r = requests.get(url)
data = json.loads(r.text)

for k in keys:
    print("%s: %s" % (k, data[k]))
