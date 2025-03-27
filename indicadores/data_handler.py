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
        self.df = calcular_indicadores_xgboost(self.df, timeframe)
        self.df = calcular_indicadores_mlp(self.df, timeframe)
        self.df = calcular_indicadores_lstm(self.df, timeframe)
        self.df = calcular_volatilidade_adp_volumes_direcional(self.df, timeframe)
        self.df = detectar_proximidade_topo_fundo(self.df, timeframe)
        self.df = self.df.dropna()
        self.df = gerar_sinal(self.df, timeframe)
        self.df.to_parquet(datasets_path, index=False)
        
        return self.df