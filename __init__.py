''' 多股票量化策略 - 函式庫 '''

import pandas as pd
import numpy as np
from BBQuant.dataframe import QuantDataFrame
from BBQuant.backtest import QuantBacktest


def get(data: pd.DataFrame, column: str):
    """
    將需要的欄位轉為樞紐表 (Index: 時間, Columns: 標的)
    """
    data.datetime = pd.to_datetime(data.datetime)
    data = data.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'})
 
    ### 日資料
    if data.datetime[0].hour == 0:
        df = data.pivot(index='datetime', columns='asset', values=column)
        df = df.replace('', np.nan).ffill().astype(float)
        return QuantDataFrame(df)
    
    ### 日內資料
    else:   
        func = {'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'}
        df = data.pivot_table(index=data.datetime.dt.date, columns='asset', values=column, aggfunc=func[column])
        df = df.replace('', np.nan).ffill().astype(float) 
        return QuantDataFrame(df)

def transform(data: pd.DataFrame):
    """
    將 pd.DataFrame 轉成自定義 QuantDataFrame
    """
    return QuantDataFrame(data)

def setting(trade_price: QuantDataFrame, freq: str = 'D', nstocks: int = None, rank: QuantDataFrame = None, take_profit: float = np.inf, stop_loss: float = np.inf, fee: float = 0.001425, tax: float = 0.003, rf: float = 0.015):
    """
    設定回測變數
    trade_price: 進出場價格
    freq: 調倉頻率
    nstocks: 持有檔數上限
    rank: 優先篩選條件
    take_profit: 停利條件
    stop_loss: 停損條件
    fee: 手續費
    tax: 交易稅
    rf: 無風險利率
    """
    return QuantBacktest(trade_price, freq, nstocks, rank, take_profit, stop_loss, fee, tax, rf)