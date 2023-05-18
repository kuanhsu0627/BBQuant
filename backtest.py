''' 多股票量化策略 - 進出場訊號與報酬計算 '''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from BBQuant.dataframe import QuantDataFrame
from BBQuant.report import QuantReport

class QuantBacktest:
    
    def __init__(self, trade_price: QuantDataFrame, take_profit: float, stop_loss: float, fee: float, tax: float, rf: float):
        """
        進出場價格、停利條件、停損條件、手續費、交易稅、無風險利率
        """
        self.trade_price = trade_price
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        self.fee = fee
        self.tax = tax
        self.rf = rf

    def strategy(self, entry: QuantDataFrame, exit: QuantDataFrame = None):
        """
        產生持有部位表
        """
        try:
            if exit == None:
                exits = QuantDataFrame(pd.DataFrame(True, index=entry.data.index, columns=entry.data.columns))

            entries = entry.data
            exits = exit.data
            price = self.trade_price.data

            ### 進出場條件
            union_index = entries.index.union(price.index)
            intersect_col = entries.columns.intersection(price.columns)
            entries = entries.reindex(index=union_index, columns=intersect_col, fill_value=False)
            entries = entries.astype(int).replace(0, np.nan)
            exits = exits.reindex(index=union_index, columns=intersect_col, fill_value=False)
            exits = exits.astype(int).replace(0, np.nan).replace(1, 0)
            position = entries.copy()
            position.update(exits, overwrite=False)
            position = position.ffill().shift(1)
            position = position.dropna(how='all').fillna(0)
            intersect_index = position.index.intersection(price.index)
            intersect_col = position.columns.intersection(price.columns)
            position = position.reindex(index=intersect_index, columns=intersect_col)
            position.iloc[-1] = 0

            ### 停損停利條件
            price = price.reindex_like(position)
            price_arr = np.array(price)
            temp = np.full(position.shape[1], np.nan)
            entry_price = np.full(position.shape[1], np.nan)
            entry_price[position.values[0] == 1] = price_arr[0][position.values[0] == 1]
            entry = (position != 0) & (position.shift(1) == 0)
            for i in range(1, position.shape[0]):
                position.iloc[i][(position.values[i-1] == 0) & (entry.values[i] == False)] = 0
                entry_price[entry.values[i]] = price_arr[i][entry.values[i]]
                temp[position.values[i] == 1] = price_arr[i][position.values[i] == 1] / entry_price[position.values[i] == 1]
                position.iloc[i][(temp > 1 + self.take_profit) | (temp < 1 - self.stop_loss)] = 0 

        except:
            print(f'There is NO entry signal!\n')
            position = pd.DataFrame(0, index=price.index, columns=price.columns)

        return position   
    

    def sim(self, position: pd.DataFrame):
        """
        回測數據 & 淨值走勢圖
        """
        price = self.trade_price.data
        weight = position.div(position.sum(axis=1), axis=0).fillna(0)
        weight = weight.shift(1).fillna(0)
        weight_arr = np.array(weight)
        payoff = (price - price.shift(1)).reindex(index=position.index, columns=position.columns)
        payoff_arr = np.array(payoff)
        price = price.reindex(index=position.index, columns=position.columns)
        price_arr = np.array(price)
        entry_price = np.full(position.shape[1], np.nan)
        entry_price[position.values[0] == 1] = price_arr[0][position.values[0] == 1]
        entry_date = np.full(position.shape[1], '0000-00-00')
        entry_date[position.values[0] == 1] = str(position.index[0])
        entry = (position != 0) & (position.shift(1) == 0)
        exit = (position == 0) & (position.shift(1) != 0) 
        asset_list = []
        entry_date_list = []
        exit_date_list = []
        entry_price_list = []
        exit_price_list = []
        weight_list = []
        ret_list = []

        for i in range(1, position.shape[0]):
            entry_date[entry.values[i]] = str(entry.index[i]) #
            entry_price[entry.values[i]] = price_arr[i][entry.values[i]]
            payoff_arr[i] = payoff_arr[i] / entry_price
            payoff_arr[i][entry.values[i-1]] = payoff_arr[i][entry.values[i-1]] - self.fee
            payoff_arr[i][exit.values[i]] = payoff_arr[i][exit.values[i]] - self.fee - self.tax
            temp = (price_arr[i][exit.values[i]] / entry_price[exit.values[i]] - 1 - 2 * self.fee - self.tax) * weight_arr[i][exit.values[i]]
            asset_list = np.append(asset_list, exit.columns[exit.values[i]])
            entry_date_list = np.append(entry_date_list, entry_date[exit.values[i]])
            exit_date_list = np.append(exit_date_list, np.full(exit.values[i].sum(), str(exit.index[i])[:10]))
            entry_price_list = np.append(entry_price_list, entry_price[exit.values[i]])
            exit_price_list = np.append(exit_price_list, price_arr[i][exit.values[i]])
            weight_list = np.append(weight_list, weight_arr[i][exit.values[i]])
            ret_list = np.append(ret_list, temp)

        trade_table_list = list(zip(asset_list, entry_date_list, exit_date_list, entry_price_list, exit_price_list, weight_list, ret_list))
        trade_table = pd.DataFrame(trade_table_list, columns=['asset', 'entry_date', 'exit_date', 'entry_price', 'exit_price', 'weight', 'ret'])
        payoff = pd.DataFrame(payoff_arr*weight_arr, index=payoff.index, columns=payoff.columns).fillna(0)
        payoff_table = pd.DataFrame()
        payoff_table['strategy'] = payoff.sum(axis=1)
        taiex = pd.read_csv('/Users/kuanhsu/Desktop/code/Python/FILE/報酬指數.txt')
        taiex = taiex[(taiex.datetime >= str(weight.index[0])[:10]) & (taiex.datetime <= str(weight.index[-1])[:10])]
        taiex = taiex.reset_index(drop=True)
        taiex['payoff'] = (taiex.Close - taiex.Close.shift(1)) / taiex.Close[0]
        taiex = taiex.fillna(0)
        payoff_table['benchmark'] = taiex.payoff.values
        equity_table = payoff_table.cumsum() + 1
        return QuantReport(payoff_table, equity_table, trade_table, self.rf)
        

    def optimize(self, entry: QuantDataFrame, exit: QuantDataFrame = None):
        pairlist = [(np.inf, 0.1), (np.inf, 0.05), (0.20, 0.10), (0.20, 0.05), (0.10, 0.05)]
        plt.style.use('bmh')
        plt.figure(figsize=(12, 6), dpi=200)
        plt.ylabel('Equity')
        plt.xlabel('Time')
        plt.title('停損/停利組合最佳化', fontsize=16)
        for pair in pairlist:
            self.take_profit = pair[0]
            self.stop_loss = pair[1]
            position = self.strategy(entry, exit)
            report = self.sim(position)
            plt.plot(report.equity_table.strategy, label='(停利, 停損) = '+str(pair[0])+', '+str(pair[1]))
        plt.legend()
        plt.show()

            
