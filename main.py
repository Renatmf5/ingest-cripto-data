import os
import sys
import asyncio
from api.fetch_data import fetch_data
from api.keys import *
from indicadores.data_handler import DataHandler
from services.load_to_lake_s3 import upload_to_s3
from dotenv import load_dotenv

load_dotenv()

# Adicione o caminho do diretório pai ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

async def main():
    # Definir os parâmetros
    pair = "BTCUSDT"
    timeframe = "1d"
    periodo = "semestral"
    bucket_name = os.getenv("BUCKET_NAME")
    
    # Criar path para candles e valor da variável periodo
    data_folder = os.path.join("data", "candles", f"{pair}", f"{timeframe}", f"{periodo}")
    datasets_folder = os.path.join("data", "datasets", f"{pair}", f"{timeframe}", f"{periodo}")
    data_path = os.path.join(data_folder, f"df_{timeframe}_{pair}_{periodo}.parquet")
    datasets_path = os.path.join(datasets_folder, f"df_{timeframe}_{pair}_{periodo}.parquet")
    os.makedirs(data_folder, exist_ok=True)
    os.makedirs(datasets_folder, exist_ok=True)
    
    # Buscar os dados
    fetch_data(pair=pair, timeframe=timeframe, periodo=periodo, data_path=data_path)
    
    # Instanciar a classe DataHandler
    data_handler = DataHandler()
    
    # Chamar o método cria_data_frame
    df = data_handler.cria_data_frame(data_path, datasets_path, timeframe)
    
    # Enviar ao S3
    await upload_to_s3(bucket_name=bucket_name, ticker=pair, timeframe=timeframe, period=periodo, data_path=datasets_path)
    
    # Exibir o DataFrame resultante
    print(df.head())

if __name__ == "__main__":
    asyncio.run(main())