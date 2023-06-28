# BBQuant

# 多股票量化交易策略回測框架

## **QuantDataFrame : 自定義 DataFrame 運算**
<br>

```python
class QuantDataFrame:
    """
    重新定義 DataFrame 運算元: +, -, *, /, >, <, ==, !=, >=, <=, &, |
    shift(): 將資料平移Ｎ天
    total(): 前Ｎ日總和
    max(): 前Ｎ日最大值    
    min(): 前Ｎ日最小值
    diff(): 今日與前Ｎ日數值的差
    average(): 前Ｎ日平均值
    fall(): 今日數值是否比前Ｎ日低
    rise(): 今日數值是否比前Ｎ日高
    largest(): 取每列數值中最大的前Ｎ筆 
    smallest(): 取每列數值中最小的前Ｎ筆
    rank(): 取每列數值中最大的前Ｎ等分
    sustain(): 條件持續滿足Ｎ天
    """
```

### **shift**  
<br>

```python
shift(n)
```
> 將資料平移Ｎ天

---

### **total**  
<br>

```python
total(n)
```
> 前Ｎ日總和

---

### **max**  
<br>

```python
max(n)
```
> 前Ｎ日最大值

---

### **min**  
<br>

```python
min(n)
```
> 前Ｎ日最小值

---

### **diff**  
<br>

```python
diff(n)
```
> 今日與前Ｎ日數值的差

---

### **average**  
<br>

```python
average(n)
```
> 前Ｎ日平均值

---

### **fall**  
<br>

```python
fall(n=1)
```
> 今日數值是否比前Ｎ日低

---

### **rise**  
<br>

```python
rise(n=1)
```
> 今日數值是否比前Ｎ日高

---

### **largest**  
<br>

```python
largest(n)
```
> 取每列數值中最大的前Ｎ筆

---

### **smallest**  
<br>

```python
smallest(n)
```
> 取每列數值中最小的前Ｎ筆

---

### **rank**  
<br>

```python
rank(n)
```
> 取每列數值中最大的前Ｎ等分 ex. 前50% -> 0.5

---

### **sustain**  
<br>

```python
sustain(n)
```
> 條件持續滿足Ｎ天

---

<br>
<br>

## **QuantBacktest : 進出場訊號與報酬計算**
<br>

```python
class QuantBacktest:
    """
    strategy(): 產生每日持有部位表
    sim(): 模擬回測績效並產生各類報表
    bestsim(): 對多個進出場條件進行最佳化
    optimize(): 對特定條件進行最佳化
    """
```

### **strategy**  
<br>

```python
strategy(entry: QuantDataFrame, exit: QuantDataFrame = None)
```
> 產生每日持有部位表

  | datetime            |   1101 |   1102 |   1103 |   1104 |   1108 |
  |:--------------------|-------:|-------:|-------:|-------:|-------:|
  | 2016-04-08 00:00:00 |      0 |      0 |      1 |      0 |      0 |
  | 2016-04-11 00:00:00 |      1 |      0 |      1 |      0 |      0 |
  | 2016-04-12 00:00:00 |      1 |      0 |      1 |      0 |      0 |
  | 2016-04-13 00:00:00 |      1 |      0 |      1 |      1 |      0 |
  | 2016-04-14 00:00:00 |      0 |      0 |      0 |      0 |      0 |

---

### **sim**  
<br>

```python
sim(position: pd.DataFrame)
```
> 模擬回測績效並產生各類報表

---

### **bestsim**  
<br>

```python
bestsim(entry: list, exit: list = None, label: list = None)
```
> 對多個進出場條件組合進行最佳化

---

### **optimize**  
<br>

```python
optimize(type: str, entry: QuantDataFrame, exit: QuantDataFrame = None)
```

> 對特定條件進行最佳化 (type)
>>  'stop': 停利/停損 <br>
>>  'nstocks': 持有檔數上限 <br>
>>  'freq': 調倉頻率 <br>

---

<br>
<br>

## **QuantReport : 回測結果分析**
<br>

```python
class QuantReport:
    """
    display(): 繪製淨值走勢圖
    analyze(): 策略報酬分析
    stats(): 詳細回測數據
    trades(): 逐筆交易資料
    best_trade(): 最佳交易標的
    worst_trade(): 最差交易標的
    """
```

### **display**  
<br>

```python
display(name: str = 'Unnamed Strategy')
```
> 繪製淨值走勢圖

---

### **analyze**  
<br>

```python
analyze()
```
> 策略報酬分析

---

### **stats**  
<br>

```python
stats()
```
> 詳細回測數據

---

### **trades**  
<br>

```python
trades()
```
> 逐筆交易資料

---

### **best_trade**  
<br>

```python
best_trade()
```
> 最佳交易標的

---

### **worst_trade**  
<br>

```python
worst_trade()
```
> 最差交易標的

---

<br>
<br>

## **函式庫**

### **get**  
<br>

```python
get(data: pd.DataFrame, column: str)
```
> 將需要的欄位轉為樞紐表

  | datetime            |   1101 |   1102 |   1103 |   1104 |   1108 |
  |:--------------------|-------:|-------:|-------:|-------:|-------:|
  | 2016-01-04 00:00:00 |  13.69 |  18.05 |   7.06 |  14.60 |   7.61 |
  | 2016-01-05 00:00:00 |  13.83 |  17.88 |   7.03 |  14.50 |   7.60 |
  | 2016-01-06 00:00:00 |  13.64 |  17.84 |   6.97 |  14.43 |   7.58 |
  | 2016-01-07 00:00:00 |  14.32 |  17.98 |   6.96 |  14.43 |   7.46 |
  | 2016-01-08 00:00:00 |  14.14 |  17.88 |   6.94 |  14.39 |   7.52 |

---

### **transform**  
<br>

```python
transform(data: pd.DataFrame)
```
> 將 pd.DataFrame 轉成自定義 QuantDataFrame

---

### **setting**  
<br>

```python
setting(trade_price: QuantDataFrame, freq: str = 'D', nstocks: int = None, rank: QuantDataFrame = None, take_profit: float = np.inf, stop_loss: float = np.inf, fee: float = 0.001425, tax: float = 0.003, rf: float = 0.015)
```
> 設定回測變數
>>  trade_price: 進出場價格 <br>
>>  freq: 調倉頻率 <br>
>>  nstocks: 持有檔數上限 <br>
>>  rank: 優先篩選條件 <br>
>>  take_profit: 停利條件 <br>
>>  stop_loss: 停損條件 <br>
>>  fee: 手續費 <br>
>>  tax: 交易稅 <br>
>>  rf: 無風險利率 <br>

- **trade_price**

  進出場價格 <p align="right">`Type: QuantDataFrame`</p>

- **freq**

  調倉頻率，預設日頻率 <p align="right">`Type: str`</p>

- **nstocks**

  持有檔數上限，預設無上限 <p align="right">`Type: int`</p>

- **rank**

  優先篩選條件，預設無優先順序 <p align="right">`Type: QuantDataFrame`</p>

- **take_profit**

  停利條件，預設值 inf <p align="right">`Type: float`</p>

- **stop_loss**

  停損條件，預設值 inf <p align="right">`Type: float`</p>

- **fee**

  手續費，預設值 0.001425 <p align="right">`Type: float`</p>

- **tax**

  交易稅，預設值 0.003 <p align="right">`Type: float`</p>

- **rf**

  無風險利率，預設值 0.015 <p align="right">`Type: float`</p>

---
