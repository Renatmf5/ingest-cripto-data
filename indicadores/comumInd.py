import pandas_ta as ta

def calcular_medias_moveis(df):
    sma_9 = ta.sma(df['close'], length=9)
    sma_21 = ta.sma(df['close'], length=21)
    sma_50 = ta.sma(df['close'], length=50)
    sma_100 = ta.sma(df['close'], length=100)
        
    df['sma_9_21_diff'] = sma_9 - sma_21 # positiva significa que é alta
    df['sma_9_50_diff'] = sma_9 - sma_50 # positiva significa que é alta
    df['sma_21_100_diff'] = sma_21 - sma_100 # positiva significa que é alta
    return df
        
def calcular_volatilidade_candles(df, timeframe):
    if timeframe == '1d':
        df['ATR_Candle'] = ta.atr(df['high'], df['low'], df['close'], length=7)
    elif timeframe == '4h':
        df['ATR_Candle'] = ta.atr(df['high'], df['low'], df['close'], length=14)
    elif timeframe == '1h':
        df['ATR_Candle'] = ta.atr(df['high'], df['low'], df['close'], length=24)
    
    return df