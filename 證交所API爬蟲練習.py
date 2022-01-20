import requests
import time


url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json' #證交所網站API


def Content(id_stock, date):
    resp = requests.get(url + '&date=' + date + '&stockNo=' + id_stock) #可指定日期區間與股票代碼
    if resp.status_code != 200: #網頁回傳是否正常
        return None
    else:
        return resp.json()


def Data(id_stock, date):
    info = list() #儲存股票資訊
    name =list() #儲存股票名稱
    resp = Content(id_stock, date)
    if resp is None:
        return None
    else:
        if resp['data']:
            for data in resp['data']:
                record = {
                    
                    '日期': data[0],
                    '開盤價': data[3],
                    '最高價': data[4],
                    '最低價': data[5],
                    '收盤價': data[6]
                } #api個欄位
                info.append(record) #存到股票資訊
                
        if resp['title']:
            for title  in resp['title']:
                tit = {'title': title[0]}
                name+=title
                s = "".join(name)
        print(s)
        return info


def Main():
    id_stock = '0050'
    date = time.strftime('%Y%m%d')
    Data(id_stock, date)
    coll_info = Data(id_stock, date)
    for info in coll_info:
        print(info)


if __name__ == '__main__':
    Main()
