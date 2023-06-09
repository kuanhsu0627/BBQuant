''' 多股票量化策略 - 進出場訊號與報酬計算 '''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import platform
from BBQuant.dataframe import QuantDataFrame
from BBQuant.report import QuantReport


if platform.system() == "Windows":
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
    plt.rcParams['axes.unicode_minus'] = False
elif platform.system() == "Darwin":
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False


class QuantBacktest:
    
    def __init__(self, trade_price: QuantDataFrame, freq: str, nstocks: int, rank: QuantDataFrame, take_profit: float, stop_loss: float, fee: float, tax: float, rf: float):
        """
        進出場價格、策略頻率、持有檔數上限、停利條件、停損條件、手續費、交易稅、無風險利率
        """
        self.trade_price = trade_price
        self.freq = freq
        self.nstocks = nstocks
        self.rank = rank
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        self.fee = fee
        self.tax = tax
        self.rf = rf

    def strategy(self, entry: QuantDataFrame, exit: QuantDataFrame = None):
        """
        每日持有部位表
        """
        try:
            if exit == None:
                exit = QuantDataFrame(pd.DataFrame(True, index=entry.data.index, columns=entry.data.columns))

            if self.rank == None:
                self.rank = QuantDataFrame(pd.DataFrame(1, index=entry.data.index, columns=entry.data.columns))

            price = self.trade_price.data
            ranking = self.rank.data

            ### 進出場條件
            entries = entry.data.resample(self.freq).ffill()
            exits = exit.data.resample(self.freq).ffill()
            union_index = entries.index.union(exits.index)
            intersect_col = entries.columns.intersection(exits.columns)
            entries = entries.reindex(index=union_index, columns=intersect_col, fill_value=False)
            exits = exits.reindex(index=union_index, columns=intersect_col, fill_value=False)
            entries = entries.astype(int).replace(0, np.nan)
            exits = exits.astype(int).replace(0, np.nan).replace(1, 0)
            position = entries.copy()
            position.update(exits, overwrite=False)
            position = position.ffill().shift(1).fillna(0)
            position = position.resample('D').ffill()
            ranking = ranking.resample('D').ffill()
            intersect_index = position.index.intersection(price.index)
            intersect_col = position.columns.intersection(price.columns)
            position = position.reindex(index=intersect_index, columns=intersect_col)
            ranking = ranking.reindex(columns=position.columns)
            index = position[position.sum(axis=1) != 0].index[0]
            position = position.loc[index:]
            position.iloc[-1] = 0

            ### 停損停利條件 & 排名篩選條件
            if self.nstocks == None:
                self.nstocks = len(position.columns)

            temp = ranking.iloc[ranking.index.tolist().index(position.index[0])-1]
            ranking = ranking.reindex_like(position, method='ffill')
            max_rank = ranking.max().max()
            min_rank = ranking.min().min()
            ranking = pd.DataFrame((ranking - min_rank) / (max_rank - min_rank)).fillna(0)
            price = price.reindex_like(position)
            price_arr = np.array(price)
            entry = np.array((position != 0) & (position.shift(1) == 0))
            waiting = temp[position.values[0] == 1].nlargest(self.nstocks).reindex_like(temp).notna()
            position.iloc[0][~waiting] = 0
            entry_price = np.full(position.shape[1], np.nan)
            entry_price[position.values[0] == 1] = price_arr[0][position.values[0] == 1]

            for i in range(1, position.shape[0]-1):
                position.iloc[i][(position.iloc[i-1] == 0) & (entry[i] == False)] = 0
                if position.iloc[i].sum() > self.nstocks:
                    now = int(position.iloc[i].sum() - sum(entry[i]))
                    waiting = ranking.iloc[i-1][entry[i] == True]
                    waiting = waiting.nlargest(self.nstocks-now).reindex_like(ranking.iloc[i]).notna()
                    position.iloc[i][(~waiting) & (entry[i] == True)] = 0
                entry_price[(entry[i] == True) & (position.values[i] == 1)] = price_arr[i][(entry[i] == True) & (position.values[i] == 1)]          
                temp = np.full(position.shape[1], np.nan)
                temp[position.values[i] == 1] = price_arr[i][position.values[i] == 1] / entry_price[position.values[i] == 1]
                position.iloc[i+1][(temp > 1 + self.take_profit) | (temp < 1 - self.stop_loss)] = 0
                
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
        price = price.reindex_like(position)
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
            entry_date[entry.values[i]] = str(entry.index[i])
            entry_price[entry.values[i]] = price_arr[i][entry.values[i]]
            payoff_arr[i] = payoff_arr[i] / entry_price
            payoff_arr[i][entry.values[i-1]] = payoff_arr[i][entry.values[i-1]] - self.fee
            payoff_arr[i][exit.values[i]] = payoff_arr[i][exit.values[i]] - self.fee - self.tax
            temp = (price_arr[i][exit.values[i]] / entry_price[exit.values[i]] - 1 - 2 * self.fee - self.tax) * weight_arr[i][exit.values[i]]
            asset_list = np.append(asset_list, exit.columns[exit.values[i]])
            entry_date_list = np.append(entry_date_list, entry_date[exit.values[i]])
            exit_date_list = np.append(exit_date_list, np.full(sum(exit.values[i]), str(exit.index[i])[:10]))
            entry_price_list = np.append(entry_price_list, entry_price[exit.values[i]])
            exit_price_list = np.append(exit_price_list, price_arr[i][exit.values[i]])
            weight_list = np.append(weight_list, weight_arr[i][exit.values[i]])
            ret_list = np.append(ret_list, temp)

        trade_table = pd.DataFrame({
            'Asset': asset_list, 
            'Entry Date': entry_date_list, 
            'Exit Date': exit_date_list, 
            'Entry Price': entry_price_list, 
            'Exit Price': exit_price_list, 
            'Weight': weight_list, 
            'Return': ret_list}
        )
        payoff = pd.DataFrame(payoff_arr*weight_arr, index=payoff.index, columns=payoff.columns).fillna(0)
        payoff_table = pd.DataFrame()
        payoff_table['Strategy'] = payoff.sum(axis=1)
        taiex = pd.read_feather('c:\\Users\\warrantnew.brk\\Desktop\\code\\PROJ\\報酬指數.ftr')
        taiex = taiex.set_index('datetime', drop=True)
        taiex.index = pd.to_datetime(taiex.index)
        taiex = taiex.reindex(weight.index)
        taiex['Payoff'] = (taiex.Close - taiex.Close.shift(1)) / taiex.Close[0]
        taiex = taiex.fillna(0)
        payoff_table['Benchmark'] = taiex.Payoff.values
        equity_table = payoff_table.cumsum() + 1
        hold_table = position.sum(axis=1)
        return QuantReport(payoff_table, equity_table, trade_table, hold_table, self.rf)
    

    def bestsim(self, entry: list, exit: list = None, label: list = None):
        """
        對多個進出場條件進行最佳化
        """
        if exit == None:
            exit = [None] * len(entry)
        if label == None:
            label = ['cond '+str(i+1) for i in list(range(len(entry)))]

        cond_list = list(zip(entry, exit))
        plt.style.use('bmh')
        plt.figure(figsize=(12, 6), dpi=200)
        plt.ylabel('Equity')
        plt.xlabel('Time')
        plt.title('進出場條件 - 最佳化', fontsize=16)
        for i in range(len(cond_list)):
            position = self.strategy(cond_list[i][0], cond_list[i][1])
            report = self.sim(position)
            plt.plot(report.equity_table.Strategy, label=label[i])
        plt.legend()
        plt.show()


    def optimize(self, type: str, entry: QuantDataFrame, exit: QuantDataFrame = None):
        """
        對特定條件進行最佳化
        'stop': 停利/停損
        'nstocks': 持有檔數上限
        """

        assert type in ['stop', 'nstocks'], 'No such type for optimization'

        if type == 'stop':
            pair_list = [(0.20, 0.10), (0.20, 0.05), (0.10, 0.05), (np.inf, 0.10), (np.inf, 0.05), (np.inf, np.inf)]
            label_list = [('20%', '10%'), ('20%', ' 5%'), ('10%', ' 5%'), ('  X', '10%'), ('  X', ' 5%'), ('  X', '  X')]
            plt.style.use('bmh')
            plt.figure(figsize=(12, 6), dpi=200)
            plt.ylabel('Equity')
            plt.xlabel('Time')
            plt.title('停利/停損組合 - 最佳化', fontsize=16)
            for i in range(len(pair_list)):
                self.take_profit = pair_list[i][0]
                self.stop_loss = pair_list[i][1]
                position = self.strategy(entry, exit)
                report = self.sim(position)
                plt.plot(report.equity_table.Strategy, label='(停利, 停損) = ('+str(label_list[i][0])+', '+str(label_list[i][1])+')')
            plt.legend()
            plt.show()

        if type == 'nstocks':
            num_list = [5, 10, 20, 50, 100, None]
            label_list = ['5', '10', '20', '50', '100', 'NO']
            plt.style.use('bmh')
            plt.figure(figsize=(12, 6), dpi=200)
            plt.ylabel('Equity')
            plt.xlabel('Time')
            plt.title('持有檔數上限 - 最佳化', fontsize=16)
            for i in range(len(num_list)):
                self.nstocks = num_list[i]
                position = self.strategy(entry, exit)
                report = self.sim(position)
                plt.plot(report.equity_table.Strategy, label='持有檔數上限 = '+str(label_list[i]))
            plt.legend()
            plt.show()