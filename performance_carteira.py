# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 00:03:31 2020

@author: USUARIO
"""

# -*- coding: utf-8 -*-

Created on Sat Nov  7 13:26:01 2020

@author: Arthur

#Racional das apostas


#importando bibliotecas

import pandas as pd
import numpy as np
from pandas_datareader import data as wb
import matplotlib.pyplot as plt
import seaborn as sns
import pypfopt

#Importando os tickers

#Seleção de Ativos para Carteira

ativos = ['ITSA4.SA', 'PETR4.SA', 'CVCB3.SA', 'LWSA3.SA', 'TAEE11.SA', 'MRFG3.SA']

#criando um df em branco para abrigar os valores

df = pd.DataFrame()

#Fazer um loop para popular o df com os ativos e campos desejados
 for t in ativos:
   df[t] = wb.DataReader(t, data_source='yahoo', start='2020-06-09') ['Adj Close']


#Visualizar os preços 
df.plot()

#atribuir pesos para cada posição
pesos = np.array([0.31, 0.09, 0.32, 0.10, 0.09, 0.09])


#calcular retornos diários
retorno = df.pct_change()

#matriz de diagramas de dispersão dos retornos
sns.pairplot(retorno[1:])

#correlação entre os ativos
matriz_correlaçao = retorno.corr()

#mapa de calor correlação
sns.heatmap(retorno.corr(), annot = True)

#retorno acumulado
returns_acm = (1 + retorno).cumprod()

#plota retornos acumulados
returns_acm.plot()

#calcula retorno carteira x pesos   
retorno_total = retorno * pesos

#calcula retoerno total da carteira
retorno_carteira = retorno_total.sum(axis=1)

#gráfico comportamento retorno da carteira
retorno_carteira.plot()

#retorno_acumulado da carteira
retorno_carteira_acm = (1 + retorno_carteira).cumprod()

#desempenho da carteira até agora
retorno_carteira_acm.tail(1)

#gráfico evolução do retorno acumulado da carteira
retorno_carteira_acm.plot()

#distribuição dos retornos da carteira
retorno_carteira.plot.hist(bins = 60)

#matriz covariancia
cov_matrix = retorno.cov()
cov_matrix

#mapa de calor da covariância
sns.heatmap(retorno.cov(), annot = True, cmap="YlGnBu")

#voltilidade do portfólio
port_volatility = np.sqrt(np.dot(pesos.T, np.dot(cov_matrix, pesos)))

#volatilidade para o ano
vol_ano = port_volatility*np.sqrt(252)
print(port_volatility)

#benchmark da carteira IBOV

#Importando o Ibovespa
ibov = wb.DataReader('^BVSP', data_source = 'yahoo', start='2019-1-1')
ibov.rename(columns = {"Adj Close":"IBOV"}, inplace = True)
ibov = ibov.drop(ibov.columns[[0,1,2,3,4]], axis =1)
ibov_retornos = ibov.pct_change()
ibov_retornos_acm = (1 + ibov_retornos).cumprod()

#gráfico comparação Ibov vs Carteira
fig, ax1 = plt.subplots(figsize=(9,7))

color = 'tab:red'
ax1.set_xlabel('Data')
ax1.set_ylabel('Ibov', color=color)
ax1.plot(ibov_retornos_acm, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()

color = 'tab:blue'
ax2.set_ylabel('Carteira', color=color)
ax2.plot(retorno_carteira_acm, color=color)
ax2.tick_params(axis='y', labelcolor=color)
plt.show()

#Sharpe Ratio da Carteira

#selic diária
risk_free = 0.0052
med_retorno = retorno_carteira.mean()
sharpe_ratio = (med_retorno - 0.0052)/port_volatility

print(sharpe_ratio)

#Otimização de Carteira: Método Fronteira eficiente

from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.expected_returns import mean_historical_return
from pypfopt import plotting


#Retornos esperados baseados na média histórica
mu = mean_historical_return(df)

#Modelo de risco
S = CovarianceShrinkage(df).ledoit_wolf()

#visualizar matriz de covariancia
plotting.plot_covariance(S, plot_correlation= True)

#Aplicando a otimização
from pypfopt.efficient_frontier import EfficientFrontier

#Fronteira eficiente
fronteira_eficiente = EfficientFrontier(mu,S)

#Definindo peso com objetivo de maximizar o Índice de Sharpe da Carteira
pesos = fronteira_eficiente.max_sharpe()

#Melhorando os pesos
clean_pesos = fronteira_eficiente.clean_weights()

