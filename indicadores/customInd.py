import pandas as pd

def calcular_retorno_candle(df):
    df['retorno_candle'] = df['close'].pct_change().round(2)
    return df


def gerar_sinal(df, timeframe):
    # criar condição de valor de alvo_base com base no timeframe
    if timeframe == '1d':
        alvo_base = 2
    elif timeframe == '4h':
        alvo_base = 3
    elif timeframe == '1h':
        alvo_base = 4
    sinais = []
    for i in range(len(df)):
        soma_retorno = 0
        sinal = None
        linhas = 0
        #quando volatilidade nao tiver valor use alvo base com 2 casas decimais
        if pd.isna(df['volatilidade'].iloc[i]):
            alvo_ajustado = alvo_base
        else:
            alvo_ajustado = alvo_base * df['volatilidade'].iloc[i]
        for j in range(i, len(df)):
            soma_retorno += df['retorno_candle'].iloc[j]
            linhas += 1
            if soma_retorno >= alvo_ajustado:
                sinal = 1
                break
            elif soma_retorno <= -alvo_ajustado:
                sinal = 0
                break
        sinais.append(sinal)
    df['signal'] = sinais
    df = df.dropna()
    df['signal'] = df['signal'].astype('int64')
    return df

def calcular_volatilidade_adp_volumes_direcional(df, timeframe):
    # Calcular a volatilidade adaptada para volumes em BTC e USDT
    if timeframe == '1d':
        df['mean_volume'] = df['volume'].rolling(window=7).mean()
        df['std_volume'] = df['volume'].rolling(window=7).std()
        df['ATR_volume'] = df['std_volume']
        # Criar a proporção entre 'taker_buy_base_asset_volume' (BTC) e volume total (BTC)
        df['proportion_taker_BTC'] = df['taker_buy_base_asset_volume'] / df['volume']
        # Calcular a média histórica da proporção BTC e USDT
        df['mean_proportion_BTC'] = df['proportion_taker_BTC'].rolling(window=14).mean()
        # Calcular o desvio padrão histórico das proporções
        df['std_proportion_BTC'] = df['proportion_taker_BTC'].rolling(window=14).std()
        df['volatilidade'] = df['close'].pct_change().rolling(window=30).std()

    if timeframe == '4h':
        df['mean_volume'] = df['volume'].rolling(window=14).mean()
        df['std_volume'] = df['volume'].rolling(window=14).std()
        df['ATR_volume'] = df['std_volume']
        df['proportion_taker_BTC'] = df['taker_buy_base_asset_volume'] / df['volume']
        df['mean_proportion_BTC'] = df['proportion_taker_BTC'].rolling(window=28).mean()
        df['std_proportion_BTC'] = df['proportion_taker_BTC'].rolling(window=28).std()
        df['volatilidade'] = df['close'].pct_change().rolling(window=42).std()
        
    if timeframe == '1h':
        df['mean_volume'] = df['volume'].rolling(window=24).mean()
        df['std_volume'] = df['volume'].rolling(window=24).std()
        df['ATR_volume'] = df['std_volume']
        df['proportion_taker_BTC'] = df['taker_buy_base_asset_volume'] / df['volume']
        df['mean_proportion_BTC'] = df['proportion_taker_BTC'].rolling(window=48).mean()
        df['std_proportion_BTC'] = df['proportion_taker_BTC'].rolling(window=48).std()
        df['volatilidade'] = df['close'].pct_change().rolling(window=96).std()
        
    # Calcular o z-score (desvio em relação à média) para identificar desvios significativos
    df['z_score_BTC'] = (df['proportion_taker_BTC'] - df['mean_proportion_BTC']) / df['std_proportion_BTC']
    return df
