# Rainbo 
## Intro
為參加[民生公共物聯網資料應用競賽](https://ci.taiwan.gov.tw/creativity/)串接雨量資料的原始碼分享，於使用其資料庫時所需資料處理的過程，並示範如何透過API即時取得資料。
## IMERG
除物聯網外亦有如何批次下載NASA的IMERG氣象資料的bash檔，需要其他教學則可以直接上他的官網：https://disc.gsfc.nasa.gov/datasets?keywords=IMERG&page=1
### Download
```bash!=
sh Download_IMERG_DL_Historical.sh [START_DATE] [END_DATE]
```
### 測站資訊

座標轉換WGS84->TW97可參考：
>http://blog.ez2learn.com/2009/08/15/lat-lon-to-twd97/
#### <font color=blue>generate_input_data.py</font>
```python=
def latlon2xy(lat, lon)
```
=> 最後拿來校正IMERG仍維持WGS84

~~目前測站資料有缺，網站上更新是到2018~~
結果發現是歷年來測站都可能會有更動，部分測站可能是到某一年之後才開始有資料(?)，然後也很多對不起來的ID... => 最後決定從real time API爬下整理所有測站（共**1146**個測站）

#### <font color=blue>generate_input_data.py</font>
```python！=
# 輸出一location.csv
# 格式：X;Y;Z;CODE;ERRP;NDEC;NAME
def parseStationInfoFromAPI()
```
之後校正需要的測站則以此為基準，根據日期填入雨量(mm)，若是沒有該時間點沒有某測站之數值，則以-999代替之。

---
## Rain IoT
台灣目前公開資料可提供雨量資訊的如下：
1. 中央氣象局自動雨量站(1146測站)
2. 農委會_雨量感測(9測站)
3. 水利署_雨量感測器(1測站)

## [感測資料-農委會_雨量感測器](https://ci.taiwan.gov.tw/dsp/environmental_iow10.aspx)
僅從2017-01-01開始有資料。

### 匯出input資料

#### <font color=blue>generate_input_data.py</font>
```python！=
def rain2inputAGR(root)
# 會輸出一input_agri.csv

# usage
rain2inputAGR(root='./Agriculture/')
```
> repo有一份2017-01-01至2020-08-31的

## [感測資料-水利署_雨量感測器](https://ci.taiwan.gov.tw/dsp/environmental_iow02.aspx)
僅從2019-12-16開始有資料。

### 匯出input資料

#### <font color=blue>generate_input_data.py</font>
```python！=
def rain2inputMOEA(root)
# 會輸出一input_MOEA.csv

# usage
rain2inputMOEA(root='./MOEA/')
```
> repo有一份2019-12-16至2020-08-31的

## [感測資料-中央氣象局自動雨量站（雨量觀測資料）](https://ci.taiwan.gov.tw/dsp/environmental_cwb_rain.aspx)
這邊因歷時悠久，且似乎有測站更新，將其分為三個時間點處理：
1. 1998-2017
2. 2018-01-01至2018-10-31
3. 2018-11-05迄今

---
### **Processing**
* **1998-2017**
僅只有<font color=blue>*PP01 降水量(mm)*</font>的欄位，從一個txt轉合併成不同天，依"yyyymmdd.csv"命名的檔案格式

#### <font color=blue>preprocessing.py</font>
```python!=
'''Special Value in the Data Array
Definition of the Parameters: PP01 降水量(mm)
-9991:儀器故障待修
-9996:資料累計於後
-9997:因不明原因或故障而無資料
-9998:雨跡(Trace)
-9999:未觀測而無資料
* In addition to the above columns, there will also be spaces for 'date' and 'stno'.
'''
def processRainHistory(txtPath)
```

---
* **2018/1-2018/10**
有AutoRain_\*和MetroRain_\*這兩種格式，但都只有雨量一欄資料，由於測站無重複，直接把兩個檔案合併為一天。這邊的時間相比之前固定區間來說較為混亂，應是雨量測站的raw data，需自行額外加總處理成想要的time scale，這邊方法是加總為一天。

#### <font color=blue>preprocessing.py</font>
```python!=
def processRain2018(folder_path)
```

---
* **2018-11-05迄今**

每天都有一個zip，有額外的zip是把一整個月份合在一起的，但只有部分才有，且看他目前規劃之儲存方式，每天都還是會有一個zip，所以自動化方式還是採解壓縮所有zip檔案後，呼叫python來整合產生input，保持每天的檔案分離存放（即每天各有一個csv）。

```bash!=
// the folder structure should be: zipped_rain_data/202001/
sh unzip_all_rain_csv.sh [ZIP_FOLDER]
```

### 匯出input資料

#### <font color=blue>generate_input_data.py</font>
```python！=
def rain2inputCWB(root_before_2017, root_in_2018, root_after_2018)
# 會輸出一input.csv

# usage
rain2inputCWB(root_before_2017='./Rain/Rain_1998-2017/',
              root_in_2018='./Rain/Processed_Rain_2018/',
              root_after_2018='./Rain/Rain_2018-2020/')
```

> repo有一份2000-06-01至2020-08-31的

---

## Real-time API
1. 農委會_雨量感測器
2. 水利署_雨量感測器
3. 中央氣象局自動雨量站（雨量觀測資料）

## 其他資料
可參考[「民生公共物聯網」資料集](https://ci.taiwan.gov.tw/dsp/environmental.aspx)