import os
import pandas as pd
from indicadores import *

class DataHandler:
    def cria_data_frame(self, data_path, datasets_path, timeframe):
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"O arquivo {data_path} não foi encontrado.")
        try:
            self.df = pd.read_parquet(data_path)
        except Exception as e:
            raise ValueError(f"Erro ao ler o arquivo Parquet: {e}")
        
        self.df = calcular_retorno_candle(self.df)
        self.df = calcular_medias_moveis(self.df)
        self.df = calcular_volatilidade_candles(self.df, timeframe)
        self.df = calcular_volatilidade_adp_volumes_direcional(self.df, timeframe)
        self.df = self.df.dropna()
        self.df = gerar_sinal(self.df, timeframe)
        self.df.to_parquet(datasets_path, index=False)
        
        return self.df