# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 23:34:07 2020

@author: Laplace Consulting
"""

"Live 2 - Como as ações reagiram ao covid-19"

"Iremos selecionar ações para entender o impacto que o vírus trouxe para cada setor"

import pandas as pd
import numpy as np
from pandas_datareader import data as wb
import seaborn as sns
import matplotlib.pyplot as plt


#Betas anterior ao COVID-19

#Importando ibovespa
ibov_pre =  wb.DataReader('^BVSP', data_source = 'yahoo', start='2019-05-29', end='2020-01-29')
ibov_pre.rename(columns = {"Adj Close":"IBOV_PRE"}, inplace = True)
ibov_pre = ibov_pre.drop(ibov_pre.columns[[0,1,2,3,4]], axis =1)
ibov_retornos_pre = ibov_pre.pct_change()
ibov_retornos_pre = ibov_pre.round(2)
ibov_retornos_pre.plot(figsize=(8,8))

#cesta de ativos selecionados

ativos_pre = ['ABEV3.SA', 'VALE3.SA', 'BBDC4.SA', 'BTOW3.SA', 'CAML3.SA', 'PCAR3.SA', 'CVCB3.SA']

#criando um df

df_covid_pre = pd.DataFrame()

#armazena tudo em um df só
 for t in ativos_pre:
   df_covid_pre[t] = wb.DataReader(t, data_source='yahoo', start='2019-05-29', end='2020-01-29') ['Adj Close']

#beta regressão
import numpy as np
from sklearn import linear_model

retornos_pre = df_covid_pre.pct_change().dropna()
ibov_retornos_pre = ibov_pre.pct_change().dropna()
betas_pre = {}

                                                                  
for t in ativos_pre:
    reg = linear_model.LinearRegression().fit(ibov_retornos_pre[["IBOV_PRE"]], retornos_pre[t])
    betas_pre[t] = reg.coef_

betas_pre = pd.DataFrame(betas_pre, index=["IBOV_PRE"]).transpose()




ibov_pos = ibov.round(2)
ibov_pos.plot(figsize=(8,8))


#Importando dados Covid fonte:https://github.com/turicas/covid19-br/blob/master/api.md#caso_full
#covid = pd.read_csv(r"C:\Users\USUARIO\Desktop\Consultoria\Treinamento Python Gestão de Portfolio\lives\caso_full.csv", parse_dates=["date"], index_col="date")

#Importando dados Covid fonte:https://github.com/turicas/covid19-br/blob/master/api.md#caso_full
covid = pd.read_csv(r"C:\Users\USUARIO\Desktop\Consultoria\Treinamento Python Gestão de Portfolio\lives\brazil_covid19.csv", parse_dates=["date"], index_col="date")
covid.head()

#Dados Pós-Covid
#Importando ibovespa
ibov_pos =  wb.DataReader('^BVSP', data_source = 'yahoo', start='2020-02-25', end='2020-12-19')
ibov_pos.rename(columns = {"Adj Close":"IBOV_POS"}, inplace = True)
ibov_pos = ibov_pos.drop(ibov_pos.columns[[0,1,2,3,4]], axis =1)
ibov_pos = ibov_pos.pct_change()


covid['data'] = covid.index


novos_casos = covid.pivot_table(values=["cases"], index=["data"], aggfunc="sum")
novos_casos.head()
novos_casos.plot()
novos_casos.tail()

#gráficos_covid_ibovespa
fig, ax1 = plt.subplots(figsize=(9,7))

color = 'tab:red'
ax1.set_xlabel('Data')
ax1.set_ylabel('casos', color=color)
ax1.plot(novos_casos.diff(), color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()

color = 'tab:blue'
ax2.set_ylabel('ibov', color=color)
ax2.plot(ibov_pos, color=color)
ax2.tick_params(axis='y', labelcolor=color)
plt.show()





#Função para gráfico 2 eixos de comparação 
def comparativo(series1, series2, label1="1", label2="2", color1="darkblue", color2="darkred", figsize=(9,6)):
    fig, ax1 = plt.subplots(figsize=figsize)
    ax1.set_ylabel(label1, color=color1)
    series1.plot(ax=ax1, color=color1)
    ax1.tick_params(axis="y", labelcolor=color1)

    ax2 = ax1.twinx()  
    ax2.set_ylabel(label2, color=color2)  
    series2.plot(ax=ax2, color=color2)
    ax2.tick_params(axis='y', labelcolor=color2)

    fig.tight_layout()
    
#gráfico comparando novos casos e ibovespa 
comparativo(novos_casos.diff(), ibov_pos, "novos-casos", "ibov_pos")



#cesta de ativos selecionados

ativos = ['ABEV3.SA', 'VALE3.SA', 'BBDC4.SA', 'BTOW3.SA', 'CAML3.SA', 'PCAR3.SA', 'CVCB3.SA']

#criando um df

df_covid = pd.DataFrame()

#armazena tudo em um df só
 for t in ativos:
   df_covid[t] = wb.DataReader(t, data_source='yahoo', start='2020-02-25', end='2020-12-19') ['Adj Close']


#plota
df_covid.plot()


#juntar os dfs
base = pd.merge(df_covid, novos_casos, how='inner', left_index=True, right_index=True)
base_full = pd.merge(base, ibov_pos, how='inner', left_index=True, right_index=True)
base_full.head()

#beta regressão pós-covid

retornos = base_full.pct_change().dropna()
betas_pos = {}

#iterando os ativos na regressão                                                                  
for t in ativos:
    reg = linear_model.LinearRegression().fit(retornos[["cases","IBOV_POS"]], retornos[t])
    betas_pos[t] = reg.coef_


betas_pos = pd.DataFrame(betas_pos, index=["cases", "Adj Close"]).transpose()


betas_pos


#Unindo as bases
betas_full = pd.merge(betas_pos, betas_pre, how='inner', left_index=True, right_index=True)










