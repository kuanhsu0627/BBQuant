''' 多股票量化策略 - 回測結果分析 '''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import platform


if platform.system() == "Windows":
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
    plt.rcParams['axes.unicode_minus'] = False
elif platform.system() == "Darwin":
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False


class QuantReport:
    """
    plot(): 繪製淨值走勢圖
    analyze(): 策略報酬分析
    stats(): 詳細回測數據
    trades(): 逐筆交易資料
    best_trade(): 最佳交易標的
    worst_trade(): 最差交易標的
    """
    
    def __init__(self, payoff_table: pd.DataFrame, equity_table: pd.DataFrame, trade_table: pd.DataFrame, hold_table: pd.Series, rf: float):
        """
        每日報酬表、每日淨值表、逐筆交易明細、持有檔數明細、無風險利率
        """
        self.payoff_table = payoff_table
        self.equity_table = equity_table
        self.trade_table = trade_table
        self.hold_table = hold_table
        self.rf = rf

    def display(self, name: str = 'Unnamed Strategy'):
        """
        繪製淨值走勢圖
        """
        period = len(self.payoff_table.index)
        totalRet = self.equity_table.Strategy[-1] - 1
        ret = (1+totalRet)**(252/period) - 1 if totalRet > -1 else -((1-totalRet)**(252/period) - 1)
        vol = self.payoff_table.Strategy.std() * np.sqrt(252)
        mdd = abs((self.equity_table.Strategy / self.equity_table.Strategy.cummax() - 1).min())
        winRate = len([i for i in self.trade_table.Return.values if i > 0]) / len(self.trade_table.Return.values) if len(self.trade_table.Return.values) != 0 else 0.0
        sharpe = (self.payoff_table.Strategy.mean() * 252 - self.rf) / vol if vol != 0 else 0.0

        plt.style.use('bmh')
        plt.figure(figsize=(12, 6), dpi=200)
        plt.fill_between(self.equity_table.index, 1, self.equity_table.Strategy, color='skyblue', alpha=0.5)
        plt.fill_between(self.equity_table.index, 1, self.equity_table.Benchmark, color='pink', alpha=0.5)
        plt.plot(self.equity_table.Strategy, label='strategy')
        plt.plot(self.equity_table.Benchmark, label='benchmark', lw=1.5)
        plt.legend(loc=4, frameon=True, facecolor='w')
        plt.ylabel('Equity')
        plt.xlabel('Time')
        plt.xlim([self.equity_table.index[0], self.equity_table.index[-1]])
        plt.title(name, fontsize=16)
        plt.table(
            cellText=[[np.round(ret*100, 1)], [np.round(sharpe, 1)], [np.round(mdd*100, 1)], [np.round(winRate*100, 1)]], 
            rowLabels=['Return [%]', 'Sharpe Ratio', 'MDD [%]', 'Win Rate [%]'], 
            rowColours=np.full(4, 'linen'),
            loc='center',
            bbox=[0.12, 0.68, 0.1, 0.3],
            zorder=2
        )
        plt.show()


    def analyze(self):
        """
        策略報酬分析
        """
        ### 策略累積報酬
        temp = self.payoff_table.cumsum()
        fig = go.Figure().set_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)
        fig.append_trace(go.Scatter(x=temp.index, y=temp.Strategy, fill='tozeroy', name='策略報酬'), row=1, col=1)
        fig.append_trace(go.Scatter(x=temp.index, y=temp.Benchmark, name='基準報酬'), row=1, col=1)
        fig.append_trace(go.Scatter(x=self.hold_table.index, y=self.hold_table.values, fill='tozeroy', fillcolor='pink', name='持有檔數'), row=2, col=1)
        fig.update_layout(height=400, width=800, title_text='策略累積報酬', title_x=0.5, hovermode='x unified')
        fig.update_xaxes(
            row=1,
            col=1,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")]
                )
            )
        )
        fig.update_yaxes(
            row=1,
            col=1,
            tickformat='.0%'
        )
        fig.show()

        ### 策略月報酬
        temp = self.payoff_table.resample('M').sum()
        temp['Month'] = temp.index.map(lambda x: x.month)
        temp['Year'] = temp.index.map(lambda x: x.year)
        temp = temp.pivot(index='Year', columns='Month', values='Strategy').fillna(0)
        temp = temp * 100
        temp.columns = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        fig = px.imshow(
            temp, 
            labels=dict(x='月', y='年', color='報酬率'), 
            color_continuous_scale='RdBu_r',
            color_continuous_midpoint=0,
            text_auto='.1f', 
            aspect="auto"
        )
        fig.update_layout(height=400, width=800, title='策略月報酬', title_x=0.5, xaxis_title=None, yaxis_title=None, coloraxis_colorbar=None)
        fig.show()


    def stats(self):
        """
        詳細回測數據
        """
        start = str(self.equity_table.index[0])[:10]
        end = str(self.equity_table.index[-1])[:10]
        period = len(self.payoff_table.index)
        winPeriod = (self.payoff_table.Strategy > 0).sum()
        totalRet = self.equity_table.Strategy[-1] - 1
        totalRetBM = self.equity_table.Benchmark[-1] - 1
        ret = (1+totalRet)**(252/period) - 1 if totalRet > -1 else -((1-totalRet)**(252/period) - 1)
        retBM = (1+totalRetBM)**(252/period) - 1 if totalRetBM > -1 else -((1-totalRetBM)**(252/period) - 1)
        vol = self.payoff_table.Strategy.std() * np.sqrt(252)
        volNeg = self.payoff_table.Strategy[self.payoff_table.Strategy < 0].std() * np.sqrt(252) if vol != 0 else 0.0
        mdd = abs((self.equity_table.Strategy / self.equity_table.Strategy.cummax() - 1).min())
        tend = (self.equity_table.Strategy / self.equity_table.Strategy.cummax() - 1).idxmin()
        tstart = self.equity_table.Strategy.loc[:tend].idxmax()
        mddDuration = str(tend - tstart).split()[0]
        trades = len(self.trade_table.Return.values)
        winRate = len([i for i in self.trade_table.Return.values if i > 0]) / trades if trades != 0 else 0.0
        bestTrade = np.nanmax(self.trade_table.Return.values) if trades !=0 else 0.0
        worstTrade = np.nanmin(self.trade_table.Return.values) if trades !=0 else 0.0
        avgTrade = np.nanmean(self.trade_table.Return.values) if trades !=0 else 0.0
        profitFactor = sum([i for i in self.trade_table.Return.values if i > 0]) / abs(sum([i for i in self.trade_table.Return.values if i < 0])) if trades != 0 else 0.0
        winLossRatio = np.mean([i for i in self.trade_table.Return.values if i > 0]) / abs(np.mean([i for i in self.trade_table.Return.values if i < 0])) if trades != 0 else 0.0
        sharpe = (self.payoff_table.Strategy.mean() * 252 - self.rf) / vol if vol != 0 else 0.0
        sortino = (self.payoff_table.Strategy.mean() * 252 - self.rf) / volNeg if volNeg != 0 else 0.0
        calmar = ret / mdd if mdd != 0 else 0.0

        result = pd.Series(
            data=[
                start,
                end,
                period,
                winPeriod,
                np.round(totalRet*100, 2),
                np.round(totalRetBM*100, 2),
                np.round(ret*100, 2),
                np.round(retBM*100, 2),
                np.round(vol*100, 2),
                np.round(mdd*100, 2),
                mddDuration,
                trades,
                np.round(winRate*100, 2),
                np.round(bestTrade*100, 2),
                np.round(worstTrade*100, 2),
                np.round(avgTrade*100, 2),
                np.round(profitFactor, 2),
                np.round(winLossRatio, 2),
                np.round(sharpe, 2),
                np.round(sortino, 2),
                np.round(calmar, 2)
            ],
            index=[
                'Start Date',
                'End Date',
                'Period [days]',
                'Win Period [days]',
                'Total Return [%]',
                'Total Benchmark Return [%]',
                'Return [%]',
                'Benchmark Return [%]',
                'Volatility [%]',
                'MDD [%]',
                'MDD Duration [days]',
                'Total Trades',
                'Win Rate [%]',
                'Best Trade [%]',
                'Worst Trade [%]',
                'Average Trade [%]',
                'Profit Factor',
                'Win Loss Ratio',
                'Sharpe Ratio',
                'Sortino Ratio',
                'Calmar Ratio'
            ]
        )
        return result

    def trades(self):
        """
        逐筆交易資料
        """
        return self.trade_table
    
    def best_trade(self):
        """
        最佳交易標的
        """
        return self.trade_table.iloc[self.trade_table.Return.idxmax()]
    
    def worst_trade(self):
        """
        最差交易標的
        """
        return self.trade_table.iloc[self.trade_table.Return.idxmin()]