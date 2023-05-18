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
 
    ### 日資料
    if data.datetime[0].hour == 0:
        df = data.pivot(index='datetime', columns='asset', values=column)
        df = df.replace('', np.nan).ffill().astype(np.float64)
        return QuantDataFrame(df)
    
    ### 日內資料
    else:   
        func = {'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'}
        df = data.pivot_table(index=data.datetime.dt.date, columns='asset', values=column, aggfunc=func[column])
        df = df.replace('', np.nan).ffill().astype(np.float64) 
        return QuantDataFrame(df)
    
def setting(trade_price: QuantDataFrame, take_profit: float = np.inf, stop_loss: float = np.inf, fee: float = 0.001425, tax: float = 0.003, rf: float = 0.015):
    """
    設定回測變數: 進出場價格、停利條件、停損條件、手續費、交易稅、無風險利率
    """
    return QuantBacktest(trade_price, take_profit, stop_loss, fee, tax, rf)