import os
import datetime as dt
from api.functions import *
from api.keys import *

def fetch_data(pair, timeframe, periodo, data_path):
    """
    Função para buscar dados de candles de um par específico e intervalo de tempo.

    Parâmetros:
    pair (str): Nome do par (ex: "BTCUSDT").
    timeframe (str): Intervalo de tempo (ex: "5m").
    periodo (str): Período para ajustar as datas (ex: "mensal", "semestral", "1ano", "3anos", "5anos").
    """
    # Load the binance keys
    client = api.Binance_API(api_key=BINANCE_API_KEY, secret_key=BINANCE_SECRET_KEY)

    # Calcular o último dia do mês passado
    today = dt.date.today()
    first_day_of_current_month = today.replace(day=1)
    last_day_of_last_month = first_day_of_current_month - dt.timedelta(days=1)

    # Ajustar as datas de início e fim com base no período especificado
    if periodo == "mensal":
        start_date = (first_day_of_current_month - dt.timedelta(days=last_day_of_last_month.day)).strftime('%Y-%m-%d')
    elif periodo == "semestral":
        start_date = (first_day_of_current_month - dt.timedelta(days=last_day_of_last_month.day + 6*30)).strftime('%Y-%m-%d')
    elif periodo == "1ano":
        start_date = (first_day_of_current_month - dt.timedelta(days=last_day_of_last_month.day + 12*30)).strftime('%Y-%m-%d')
    elif periodo == "3anos":
        start_date = (first_day_of_current_month - dt.timedelta(days=last_day_of_last_month.day + 36*30)).strftime('%Y-%m-%d')
    elif periodo == "5anos":
        start_date = (first_day_of_current_month - dt.timedelta(days=last_day_of_last_month.day + 60*30)).strftime('%Y-%m-%d')
    else:
        raise ValueError("Período inválido. Use 'mensal', 'semestral', '1ano', '3anos' ou '5anos'.")

    end_date = last_day_of_last_month.strftime('%Y-%m-%d')

    # Collect the candles
    candles = get_candles_batched(client, symbol=pair, interval=timeframe, start_date=start_date, end_date=end_date, delay=0.4)

    # Convert the candles to a dataframe
    df = create_df(candles)

    # Visualise and save the data
    print(df)
    df.to_parquet(data_path, index=False)