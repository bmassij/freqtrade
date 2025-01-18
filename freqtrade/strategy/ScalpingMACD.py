Codevoorbeeld van een eenvoudige MACD-strategie:
python
Kopiëren
Bewerken
from freqtrade.strategy import IStrategy
from pandas import DataFrame
import talib.abstract as ta

class ScalpingMACD(IStrategy):
    # Define minimal ROI and stop loss settings
    minimal_roi = {"0": 0.01}  # 1% take-profit
    stoploss = -0.01  # 1% stop-loss

    # Define timeframe for the strategy
    timeframe = '5m'

    # Define the indicators
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['macd'], dataframe['macdsignal'], dataframe['macdhist'] = ta.MACD(dataframe['close'], fastperiod=12, slowperiod=26, signalperiod=9)
        return dataframe

    # Define the entry (buy) signal
    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['macd'] > dataframe['macdsignal']) &  # MACD crosses above the signal line
                (dataframe['macdhist'] > 0)  # MACD histogram is positive
            ),
            'buy'] = 1
        return dataframe

    # Define the exit (sell) signal
    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['macd'] < dataframe['macdsignal']) &  # MACD crosses below the signal line
                (dataframe['macdhist'] < 0)  # MACD histogram is negative
            ),
            'sell'] = 1
        return dataframe