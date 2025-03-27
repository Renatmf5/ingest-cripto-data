# Projeto: Sistema de Coleta e Refinamento de Dados de Candles da Binance Futures

**Descrição do Projeto**:
- Este projeto é um sistema automatizado para buscar, processar e armazenar dados históricos de candles da Binance Futures. Ele permite a coleta de dados em modo batch para um período e timeframe específicos, refinando os dados com indicadores técnicos e armazenando-os em um Data Lake. O objetivo principal é fornecer um conjunto de dados consolidado e enriquecido para ser utilizado em experimentos de Machine Learning e Inteligência Artificial.

**Funcionalidades Principais**:
1. **Coleta de Dados Históricos**: Busca dados de candles históricos da Binance Futures para um par de moedas, intervalo de tempo (timeframe) e período especificados.
2. **Processamento e Refinamento**: Aplica indicadores técnicos e cálculos personalizados aos dados coletados.
3. **Armazenamento no Data Lake**: Salva os dados refinados em um Data Lake no formato Parquet, organizado por partições.
4. **Preparação para Machine Learning**: Gera um DataFrame consolidado com sinais e indicadores técnicos prontos para uso em modelos de aprendizado de máquina.

---

## Estrutura do Projeto

Abaixo está a estrutura dos principais arquivos e suas responsabilidades:

### 1. **`keys.py`**
Gerencia as chaves de API da Binance, carregando-as de variáveis de ambiente.

### 2. **`functions.py`**
Contém funções auxiliares para manipulação de dados, como:
- Conversão de datas para timestamps.
- Coleta de candles em modo batch com suporte a grandes intervalos de tempo.
- Criação de DataFrames a partir dos dados de candles.

### 3. **`fetch_data.py`**
Função principal para buscar os dados de candles da Binance Futures:
- Calcula as datas de início e fim com base no período especificado.
- Utiliza a função `get_candles_batched` para coletar os dados.
- Salva os dados brutos em um arquivo Parquet.

### 4. **`parameterServiceAws.py`**
Gerencia a integração com o AWS SSM Parameter Store para buscar parâmetros sensíveis, como chaves de API.

### 5. **`binance.py`**
Implementa a classe `Binance_API` para comunicação com a API da Binance:
- Geração de assinaturas HMAC para autenticação.
- Requisições HTTP para endpoints da Binance.
- Coleta de candles com parâmetros específicos.

### 6. **`load_to_lake_s3.py`**
Gerencia o upload dos dados refinados para o Data Lake no Amazon S3:
- Organiza os dados em partições baseadas no par, timeframe e período.
- Envia os arquivos para o bucket S3 especificado.

### 7. **`comumInd.py`**
Aplica indicadores técnicos aos dados:
- Indicadores como MACD, RSI, Bandas de Bollinger, ATR, entre outros.
- Diferentes conjuntos de indicadores para modelos XGBoost, MLP e LSTM.

### 8. **`customInd.py`**
Adiciona cálculos personalizados aos dados:
- Retornos de candles.
- Geração de sinais baseados em volatilidade e alvos ajustados.
- Cálculo de volatilidade adaptada e proximidade de topos e fundos.

### 9. **`data_handler.py`**
Classe principal para manipulação de dados:
- Lê os dados brutos do arquivo Parquet.
- Aplica os cálculos e indicadores técnicos.
- Gera o DataFrame consolidado e salva o resultado refinado.

### 10. **`main.py`**
Script principal para execução do sistema:
- Define os parâmetros de coleta (par, timeframe, período).
- Busca os dados de candles.
- Processa os dados com a classe `DataHandler`.
- Envia os dados refinados para o Data Lake no S3.
- Exibe o DataFrame resultante.

---

## Fluxo de Execução

1. **Definição de Parâmetros**:
   - Par de moedas (ex.: `BTCUSDT`).
   - Timeframe (ex.: `15m`).
   - Período (ex.: `1ano`).

2. **Coleta de Dados**:
   - Os dados de candles são buscados da Binance Futures utilizando a API oficial.
   - A coleta é feita em modo batch para lidar com grandes intervalos de tempo.

3. **Processamento e Refinamento**:
   - Os dados brutos são transformados em um DataFrame.
   - Indicadores técnicos e cálculos personalizados são aplicados.
   - Sinais são gerados com base em volatilidade e alvos ajustados.

4. **Armazenamento no Data Lake**:
   - Os dados refinados são salvos no formato Parquet.
   - Os arquivos são enviados para um bucket S3, organizados por partições.

5. **Preparação para Machine Learning**:
   - O DataFrame consolidado está pronto para ser utilizado em experimentos de IA.

---

## Tecnologias Utilizadas

- **Python**: Linguagem principal do projeto.
- **Pandas**: Manipulação e análise de dados.
- **Pandas TA**: Cálculo de indicadores técnicos.
- **TQDM**: Barra de progresso para operações demoradas.
- **Boto3**: Integração com AWS S3 e SSM Parameter Store.
- **Requests**: Comunicação com a API da Binance.
- **Parquet**: Formato de armazenamento eficiente para grandes volumes de dados.

---

## Como Executar o Projeto

1. **Pré-requisitos**:
   - Python 3.10 ou superior.
   - Conta na Binance com acesso à API.
   - AWS S3 configurado para armazenar os dados.
   - Chaves de API da Binance e AWS armazenadas no SSM Parameter Store.

2. **Instalação**:
   - Clone o repositório.
   - Instale as dependências com `pip install -r requirements.txt`.

3. **Configuração**:
   - Crie um arquivo `.env` com as variáveis de ambiente necessárias:
     ```
     BUCKET_NAME=seu-bucket-s3
     BINANCE_API_KEY=sua-chave-api
     BINANCE_SECRET_KEY=sua-chave-secreta
     ```
   - Configure os parâmetros no AWS SSM Parameter Store.

4. **Execução**:
   - Execute o script principal:
     ```bash
     python main.py
     ```

---

## Futuras Melhorias

1. **Integração com Sentimentos de Notícias**:
   - Incorporar dados de notícias positivas ou negativas como indicadores adicionais.

2. **Análise de Redes Sociais**:
   - Adicionar métricas baseadas em menções e sentimentos de redes sociais.

3. **Otimização de Performance**:
   - Melhorar o desempenho do processamento em grandes volumes de dados.

4. **Visualização de Dados**:
   - Criar dashboards para análise exploratória dos dados refinados.

---
