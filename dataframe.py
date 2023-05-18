''' 多股票量化策略 - 自定義 DataFrame 運算 '''

import pandas as pd
import numpy as np
import operator
from IPython.display import display

class QuantDataFrame:
    """
    重新定義 DataFrame 運算元: +, -, *, /, >, <, ==, !=, >=, <=, &, |
    對 Index 取聯集, Columns 取交集
    """
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def __add__(self, other):
        """
        ex. df + 20
        """
        if isinstance(other, (int, float)):
            temp = pd.DataFrame(other, index=self.data.index, columns=self.data.columns)
            df = np.add(self.data, temp)
            return QuantDataFrame(df)

        if isinstance(other, (pd.DataFrame)):
            df = np.add(self.data, other)
            return QuantDataFrame(df)

        if isinstance(other, (QuantDataFrame)):
            df = np.add(self.data, other.data)
            return QuantDataFrame(df)
    
    def __sub__(self, other):
        """
        ex. df - 20
        """
        if isinstance(other, (int, float)):
            temp = pd.DataFrame(other, index=self.data.index, columns=self.data.columns)
            df = np.subtract(self.data, temp)
            return QuantDataFrame(df)

        if isinstance(other, (pd.DataFrame)):
            df = np.subtract(self.data, other)
            return QuantDataFrame(df)

        if isinstance(other, (QuantDataFrame)):
            df = np.subtract(self.data, other.data)
            return QuantDataFrame(df)
    
    def __mul__(self, other):
        """
        ex. df * 20
        """
        if isinstance(other, (int, float)):
            temp = pd.DataFrame(other, index=self.data.index, columns=self.data.columns)
            df = np.multiply(self.data, temp)
            return QuantDataFrame(df)

        if isinstance(other, (pd.DataFrame)):
            df = np.multiply(self.data, other)
            return QuantDataFrame(df)

        if isinstance(other, (QuantDataFrame)):
            df = np.multiply(self.data, other.data)
            return QuantDataFrame(df)
    
    def __truediv__(self, other):
        """
        ex. df / 20
        """
        if isinstance(other, (int, float)):
            temp = pd.DataFrame(other, index=self.data.index, columns=self.data.columns)
            df = np.true_divide(self.data, temp)
            return QuantDataFrame(df)

        if isinstance(other, (pd.DataFrame)):
            df = np.true_divide(self.data, other)
            return QuantDataFrame(df)

        if isinstance(other, (QuantDataFrame)):
            df = np.true_divide(self.data, other.data)
            return QuantDataFrame(df)

    def __gt__(self, other):
        """
        ex. df > 20
        """
        if isinstance(other, (int, float)):
            temp = pd.DataFrame(other, index=self.data.index, columns=self.data.columns)
            df = operator.__gt__(self.data, temp)
            return QuantDataFrame(df)

        if isinstance(other, (pd.DataFrame)):
            union_index = self.data.index.union(other.index)
            intersect_col = self.data.columns.intersection(other.columns)
            self.data = self.data.reindex(index=union_index, columns=intersect_col, fill_value=False)
            other = other.reindex(index=union_index, columns=intersect_col, fill_value=False)
            df = operator.__gt__(self.data, other)
            return QuantDataFrame(df)

        if isinstance(other, (QuantDataFrame)):
            union_index = self.data.index.union(other.data.index)
            intersect_col = self.data.columns.intersection(other.data.columns)
            self.data = self.data.reindex(index=union_index, columns=intersect_col, fill_value=False)
            other.data = other.data.reindex(index=union_index, columns=intersect_col, fill_value=False)
            df = operator.__gt__(self.data, other.data)
            return QuantDataFrame(df)

    def __lt__(self, other):
        """
        ex. df < 20
        """
        if isinstance(other, (int, float)):
            temp = pd.DataFrame(other, index=self.data.index, columns=self.data.columns)
            df = operator.__lt__(self.data, temp)
            return QuantDataFrame(df)

        if isinstance(other, (pd.DataFrame)):
            union_index = self.data.index.union(other.index)
            intersect_col = self.data.columns.intersection(other.columns)
            self.data = self.data.reindex(index=union_index, columns=intersect_col, fill_value=False)
            other = other.reindex(index=union_index, columns=intersect_col, fill_value=False)
            df = operator.__lt__(self.data, other)
            return QuantDataFrame(df)

        if isinstance(other, (QuantDataFrame)):
            union_index = self.data.index.union(other.data.index)
            intersect_col = self.data.columns.intersection(other.data.columns)
            self.data = self.data.reindex(index=union_index, columns=intersect_col, fill_value=False)
            other.data = other.data.reindex(index=union_index, columns=intersect_col, fill_value=False)
            df = operator.__lt__(self.data, other.data)
            return QuantDataFrame(df)
    
    def __eq__(self, other):
        """
        ex. df == 20
        """
        if isinstance(other, (int, float)):
            temp = pd.DataFrame(other, index=self.data.index, columns=self.data.columns)
            df = operator.__eq__(self.data, temp)
            return QuantDataFrame(df)

        if isinstance(other, (pd.DataFrame)):
            union_index = self.data.index.union(other.index)
            intersect_col = self.data.columns.intersection(other.columns)
            self.data = self.data.reindex(index=union_index, columns=intersect_col, fill_value=False)
            other = other.reindex(index=union_index, columns=intersect_col, fill_value=False)
            df = operator.__eq__(self.data, other)
            return QuantDataFrame(df)

        if isinstance(other, (QuantDataFrame)):
            union_index = self.data.index.union(other.data.index)
            intersect_col = self.data.columns.intersection(other.data.columns)
            self.data = self.data.reindex(index=union_index, columns=intersect_col, fill_value=False)
            other.data = other.data.reindex(index=union_index, columns=intersect_col, fill_value=False)
            df = operator.__eq__(self.data, other.data)
            return QuantDataFrame(df)
    
    def __ne__(self, other):
        """
        ex. df != 20
        """
        if isinstance(other, (int, float)):
            temp = pd.DataFrame(other, index=self.data.index, columns=self.data.columns)
            df = operator.__ne__(self.data, temp)
            return QuantDataFrame(df)

        if isinstance(other, (pd.DataFrame)):
            union_index = self.data.index.union(other.index)
            intersect_col = self.data.columns.intersection(other.columns)
            self.data = self.data.reindex(index=union_index, columns=intersect_col, fill_value=False)
            other = other.reindex(index=union_index, columns=intersect_col, fill_value=False)
            df = operator.__ne__(self.data, other)
            return QuantDataFrame(df)

        if isinstance(other, (QuantDataFrame)):
            union_index = self.data.index.union(other.data.index)
            intersect_col = self.data.columns.intersection(other.data.columns)
            self.data = self.data.reindex(index=union_index, columns=intersect_col, fill_value=False)
            other.data = other.data.reindex(index=union_index, columns=intersect_col, fill_value=False)
            df = operator.__ne__(self.data, other.data)
            return QuantDataFrame(df)
    
    def __ge__(self, other):
        """
        ex. df >= 20
        """
        if isinstance(other, (int, float)):
            temp = pd.DataFrame(other, index=self.data.index, columns=self.data.columns)
            df = operator.__ge__(self.data, temp)
            return QuantDataFrame(df)

        if isinstance(other, (pd.DataFrame)):
            union_index = self.data.index.union(other.index)
            intersect_col = self.data.columns.intersection(other.columns)
            self.data = self.data.reindex(index=union_index, columns=intersect_col, fill_value=False)
            other = other.reindex(index=union_index, columns=intersect_col, fill_value=False)
            df = operator.__ge__(self.data, other)
            return QuantDataFrame(df)

        if isinstance(other, (QuantDataFrame)):
            union_index = self.data.index.union(other.data.index)
            intersect_col = self.data.columns.intersection(other.data.columns)
            self.data = self.data.reindex(index=union_index, columns=intersect_col, fill_value=False)
            other.data = other.data.reindex(index=union_index, columns=intersect_col, fill_value=False)
            df = operator.__ge__(self.data, other.data)
            return QuantDataFrame(df)

    def __le__(self, other):
        """
        ex. df <= 20
        """
        if isinstance(other, (int, float)):
            temp = pd.DataFrame(other, index=self.data.index, columns=self.data.columns)
            df = operator.__le__(self.data, temp)
            return QuantDataFrame(df)

        if isinstance(other, (pd.DataFrame)):
            union_index = self.data.index.union(other.index)
            intersect_col = self.data.columns.intersection(other.columns)
            self.data = self.data.reindex(index=union_index, columns=intersect_col, fill_value=False)
            other = other.reindex(index=union_index, columns=intersect_col, fill_value=False)
            df = operator.__le__(self.data, other)
            return QuantDataFrame(df)

        if isinstance(other, (QuantDataFrame)):
            union_index = self.data.index.union(other.data.index)
            intersect_col = self.data.columns.intersection(other.data.columns)
            self.data = self.data.reindex(index=union_index, columns=intersect_col, fill_value=False)
            other.data = other.data.reindex(index=union_index, columns=intersect_col, fill_value=False)
            df = operator.__le__(self.data, other.data)
            return QuantDataFrame(df)

    def __and__(self, other):
        """
        對條件取交集 ex. cond1 & cond2
        """
        if isinstance(other, (pd.DataFrame)):
            union_index = self.data.index.union(other.index)
            intersect_col = self.data.columns.intersection(other.columns)
            self.data = self.data.reindex(index=union_index, columns=intersect_col, fill_value=False)
            other = other.reindex(index=union_index, columns=intersect_col, fill_value=False)
            df = np.logical_and(self.data, other)
            return QuantDataFrame(df)

        if isinstance(other, (QuantDataFrame)):
            union_index = self.data.index.union(other.data.index)
            intersect_col = self.data.columns.intersection(other.data.columns)
            self.data = self.data.reindex(index=union_index, columns=intersect_col, fill_value=False)
            other.data = other.data.reindex(index=union_index, columns=intersect_col, fill_value=False)
            df = np.logical_and(self.data, other.data)
            return QuantDataFrame(df)

    def __or__(self, other):
        """
        對條件取聯集 ex. cond1 | cond2
        """
        if isinstance(other, (pd.DataFrame)):
            union_index = self.data.index.union(other.index)
            intersect_col = self.data.columns.intersection(other.columns)
            self.data = self.data.reindex(index=union_index, columns=intersect_col, fill_value=False)
            other = other.reindex(index=union_index, columns=intersect_col, fill_value=False)
            df = np.logical_or(self.data, other)
            return QuantDataFrame(df)

        if isinstance(other, (QuantDataFrame)):
            union_index = self.data.index.union(other.data.index)
            intersect_col = self.data.columns.intersection(other.data.columns)
            self.data = self.data.reindex(index=union_index, columns=intersect_col, fill_value=False)
            other.data = other.data.reindex(index=union_index, columns=intersect_col, fill_value=False)
            df = np.logical_or(self.data, other.data)
            return QuantDataFrame(df)
        
    def average(self, n):
        """
        前Ｎ日平均值
        """
        df = self.data.rolling(n).mean()
        return QuantDataFrame(df)

    def fall(self, n=1):
        """
        今日數值是否比前Ｎ日低
        """
        df = operator.__lt__(self.data, self.data.shift(n))
        return QuantDataFrame(df)

    def rise(self, n=1):
        """
        今日數值是否比前Ｎ日高
        """
        df = operator.__gt__(self.data, self.data.shift(n))
        return QuantDataFrame(df)
    
    def largest(self, n):
        """
        取每列數值中最大的前Ｎ筆
        """   
        df = self.data.astype(float).apply(lambda x: x.nlargest(n), axis=1).reindex_like(self).notna()
        return QuantDataFrame(df)
    
    def smallest(self, n):
        """
        取每列數值中最小的前Ｎ筆
        """
        df = self.data.astype(float).apply(lambda x: x.smallest(n), axis=1).reindex_like(self).notna()
        return QuantDataFrame(df)
    
    def sustain(self, n=1):
        """
        條件持續滿足Ｎ天
        """
        df = operator.__ge__(self.data.rolling(n).sum(), n)
        return QuantDataFrame(df)     
        
    def __repr__(self):
        display(self.data)
        return ""

    def __str__(self):
        print(self.data)
        return ""