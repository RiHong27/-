import requests
from bs4 import BeautifulSoup
import time

url = 'https://tip.railway.gov.tw/tra-tip-web/tip'
staDic = {}
today = time.strftime('%Y/%m/%d')
sTime = '04:00'
eTime = '23:00'

def getTrip():
    resp = requests.get(url)
    if resp.status_code != 200:
        print('URL ERROR：' + url)
        return
    soup = BeautifulSoup(resp.text, 'html5lib')
    stations = soup.find(id = 'cityHot').ul.find_all('li') #li包含各車站名稱與代碼
    for station in stations:
        stationName = station.button.text #名稱被標籤button包起來,轉為字串
        stationId = station.button['title']
        staDic[stationName] = stationId
    csrf = soup.find(id = 'queryForm').find('input',{'name':'_csrf'})['value']
    formData = {
            'trainTypeList':'ALL',
            'transfer':'ONE',
            'startOrEndTime':'true',
            'startStation':staDic['臺北'],
            'endStation':staDic['新竹'],
            'rideDate':today,
            'startTime':sTime,
            'endTime':eTime,
           '_csrf':csrf}
    queryUrl = soup.find(id='queryForm')['action']
    qResp = requests.post('https://tip.railway.gov.tw'+queryUrl, data=formData)
    qSoup = BeautifulSoup(qResp.text, 'html5lib')
    trs = qSoup.find_all('tr', 'trip-column')
    for tr in trs:
        td = tr.find_all('td')
        print('車種%s : 出發時間%s, 抵達時間%s,行駛時間%s,經由%s' % (td[0].ul.li.a.text, td[1].text, td[2].text,td[3].text,td[4].text))
getTrip()
