# Taiex_analysis
Taiex_analysis

# 台股資料爬蟲─Python筆記(1)
###### tags: `Python` `Coding`
![](https://i.imgur.com/buOtYgR.png)

## Python爬蟲基本知識
Python憑藉簡單易懂的程式語言寫法及廣大開發者的模組支援，可以非常容易的達到在網頁上抓取公開內容，再整理成特定資料型態的需求。開發一個Python爬蟲，我們要具備以下能力：
- 對Python語言的基本理解：了解模組的引用，資料的整理及保存(或進一步的使用資料)
- 對資料的基本理解：了解爬蟲收集而來的資料結構，並能篩選出需要的內容
- 努力的尋找解答：自學過程中常遇到各種Bug，多半都可以靠Google大神幫忙，但要能盡量評估自己遇到的狀況，再耐心的尋找合適的解答

## 要準備的東西
- Python開發環境(我的版本是3.8.2)
- 可連網的環境
- 要爬取的資訊：通常會選擇一個網頁作為目標，但這邊我想分享一個[超棒的Python模組「twstock」](https://github.com/mlouielu/twstock)，可以使用這個模組直接連線到[TWSE](http://www.twse.com.tw/)取得台股的所有資料。

## `twstock`
twstock是由[Louie Lu](https://github.com/mlouielu)開發的Python模組，使用這個模組便能輕易取得台灣證券交易所以及證券交易櫃買中心的資料，包括個股資訊、歷史價格、均價、均量、乖離值、及四大買賣點分析等，甚至能在盤中直接抓取即時價格資料。
## Python程式中使用的模組
在這個程式中會用到以下幾個模組：
- twstock：抓取台股資料
- pandas：處理抓到的資料並輸出為`.csv`檔案保存
## 抓取資料
首先引入twstock模組
```python=
import twstock
```
接著設定要查詢的股票代號變數(target_stock)，並將變數帶進模組中，再使用`fetch_from()`屬性抓取指定期間的交易資料存到股票價格的變數(target_price)裡面。
```python=
target_stock = '0050'
stock = twstock.Stock(target_stock)
target_price = stock.fetch_from(2020, 5)
```
如果把股價`print()`出來，會看到這樣的清單(list)：
```
[Data(date=datetime.datetime(2020, 5, 4, 0, 0), capacity=15648380, 
turnover=1296408090, open=82.4, high=83.3, low=82.2, close=83.0, 
change=-2.5, transaction=8848), 
Data(date=datetime.datetime(2020, 5, 5, 0,
0), capacity=7810636, turnover=651512279, open=83.5, high=83.8,
low=83.0, close=83.4, change=0.4, transaction=3986), .................
```
其中我們可以歸納出Data(Date)、Capacity、Turnover、Open、High、Low、Close、Change和Trascation幾個表頭屬性，接著便可以用pandas來整理這個資料，將這筆清單資料轉換成Data Frame便能進一步分析或繪圖。
## 處理資料
為了要將目前股價的清單轉換成方便操作的Data Frame格式，這裡要使用另一個在Python資料分析中超級重要的pandas模組。
```python=
import pandas as pd
```
接著要設定資料表裡面的表頭，也就是我們前面歸納出來的9個資料的名稱，在這裡我們設定了一個名為name_attribute的清單，清單中包含9個我們需要的表頭：
```python=
name_attribute = ['Date', 'Capacity', 'Turnover', 'Open', 'High', 'Low', 'Close', 'Change', 'Trascation']
```
將清單轉換成資料表要用到pandas模組中的`pd.Dataframe()`功能，而參數中我們便引入前面設計好的表頭，再指定要放入資料表的資料來源，就能將清單轉換成資料表格式了。
```python=
df = pd.Dataframe(colum = name_attribute, data = target_price)
```
將資料表`print()`出來可以看到資料已經整理好了，非常清楚易讀，接下來我們要將資料表的存成檔案，方便未來分析使用。
```
         Date  Capacity    Turnover   Open   High    Low  Close  Change  Trascation
0  2020-05-04  15648380  1296408090  82.40  83.30  82.20  83.00   -2.50        8848
1  2020-05-05   7810636   651512279  83.50  83.80  83.00  83.40    0.40        3986
2  2020-05-06   6142593   511218824  83.30  83.75  82.60  83.50    0.10        3610
3  2020-05-07   6140995   514715030  83.50  84.15  83.30  83.85    0.35        3429
4  2020-05-08   6034013   508981564  84.60  84.75  84.00  84.35    0.50        3530
5  2020-05-11   6655422   566557718  85.00  85.40  84.70  85.05    0.70        4065
```
## 保存資料
一般使用pandas模組保存Data Frame資料時，常會選用`.csv`檔案儲存，一方面檔案體積小，也易於與其他資料分析模組互動。

首先我們在Python程式的資料夾中建立一個'data'資料夾，準備用來存放股價資料，接著在程式中宣告一個檔案名稱+路徑的變數，這邊引用一開始使用的股票代號變數作為檔名，方便我們未來能快速的調用檔案。
```python=
filename = f'./data/{target_stock}.csv'
```
接著使用pandas模組中的`df.to_csv()`功能，參數中放入檔案的路徑，便能將資料表保存成`.csv`檔案啦！
```python=
df.to_csv(filename)
```
## 完整程式碼
以下為完整的程式碼內容：
```python=
import twstock
import pandas as pd
# 導入twstock及pandas模組，pandas模組縮寫為pd

target_stock = '0050'  #股票代號變數
stock = twstock.Stock(target_stock)  #告訴twstock我們要查詢的股票
target_price = stock.fetch_from(2020, 5)  #取用2020/05至今每天的交易資料

name_attribute = [
    'Date', 'Capacity', 'Turnover', 'Open', 'High', 'Low', 'Close', 'Change',
    'Trascation'
]  #幫收集到的資料設定表頭

df = pd.DataFrame(columns=name_attribute, data=target_price)
#將twstock抓到的清單轉成Data Frame格式的資料表

filename = f'./data/{target_stock}.csv'
#指定Data Frame轉存csv檔案的檔名與路徑

df.to_csv(filename)
#將Data Frame轉存為csv檔案
```
