# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 20:00:34 2021

@author: USUARIO
"""

#Aula básica de nivelamento em Python para Finanças

#PARTE 1 - Pandas DataReader

#Função mais utilizada na Biblioteca Pandas DataReader
from pandas_datareader import data as wb

#importar um ativo

#Risco Individual do Ativo ITSA.4
itau_prices = wb.DataReader('ITSA4.SA', data_source = 'yahoo', start='2019-1-1')
itau_prices.head()

#importar um df usando loop

#crirar uma lista com o nome dos ativos

ativos = ['ITSA4.SA', 'PETR4.SA', 'ABEV3.SA', 'VALE3.SA']

#criando um dataframe vazio

df = pd.DataFrame()

#armazena os preços no df criado
 for t in ativos:
   df[t] = wb.DataReader(t, data_source='yahoo', start='2019-01-01') ['Adj Close']


#PARTE 2 - Pandas

#Funções mais utilizadas na Biblioteca Pandas

#Importando
import pandas as pd

#renomeia a coluna adj close
itau_prices.rename(columns = {"Adj Close":"ITAU"}, inplace = True)

#remove as colunas 
itau = itau_prices.drop(itau_prices.columns[[0,1,2,3,4]], axis =1)

#retornos percentuais
itau_retornos = itau_prices.pct_change()

#remover nan
itau_retornos = itau_retornos.dropna()

#união

#juntar os dfs
base = pd.merge(df_covid, novos_casos, how='inner', left_index=True, right_index=True)

#correlação
df.corr()

#covariancia
df.cov()


#PARTE 3 - Numpy

import numpy as np

#criando um array

pesos = np.array([0.30,0.20,0.25,0.25])

#propriedades
#mímino
pesos.min()
#máximo
pesos.max()
#média
pesos.mean()
#desvio padrão
pesos.std()

#tamanho
len(pesos)

#raiz quadrada
raiz = np.sqrt(pesos)
print(raiz)

#transpor
pesos_t = np.transpose(pesos)
print(pesos_t)


#PARTE 4 - PyPortfolio

#P1[Pesos] P2[Covariância] P3[Retornos esperados]

#P3 RETORNOS ESPERADOS
from pypfopt import expected_returns

media_historica = expected_returns.mean_historical_return()
print(media_historica)

#P2 COVARIÂNCIA

from pypfopt.risk_models import CovarianceShrinkage

modelo_risco = CovarianceShrinkage(carteira).ledoit_wolf()

from pypfopt import plotting

plotting.plot_covariance(modelo_risco)

#P1 PESOS - OTIMIZAÇÃO

from pypfopt.efficient_frontier import EfficientFrontier

ef = EfficientFrontier(media_historica, modelo_risco)

ef.max_sharpe()


#PARTE 5 - Gráficos

#Matplotlib

import matplotlib.pyplot as plt

#gráfico de linhas

itau_prices['Adj Close'].plot(figsize=(12,8))

#histograma

itau_retornos['Adj Close'].plot.hist(bins=60)

#gráfico de barras
itau_prices['Volume'].iloc



#Seaborn
import seaborn as sns


#heatmap







