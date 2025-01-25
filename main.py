import os
import sys
from api.fetch_data import fetch_data
from api.keys import *
from indicadores.data_handler import DataHandler


# Adicione o caminho do diretório pai ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


if __name__ == "__main__":
    # Definir os parâmetros
    pair = "BTCUSDT"
    timeframe = "1d"
    periodo = "semestral"
    
    # Criar path por dara canldes e valor da caraviel periodo
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
    
    # Exibir o DataFrame resultante
    print(df.head())