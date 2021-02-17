# -*- coding: utf-8 -*-
"""
Created on Tue May 26 20:05:53 2020

@author: USUARIO
"""

"analise setorial"

"Bancos"

import pandas as pd
import numpy as np
from pandas_datareader import data as wb
import quandl 
quandl.ApiConfig.api_key = "4NFLzs3fgqxK3JHsN-dX"
import matplotlib.pyplot as plt

"MACROECONOMINCO"
pib = quandl.get("ODA/BRA_NGDPD", start_date="2000-01-01")
plt.figure(figsize=(20,10))
plt.plot(pib)
dolar.rename(columns = {"Value" : "pib"}, inplace = True)

'pib_crescimento_nominal
st_pib = pib
st_pib1 = pib.shift(1)
pib_cresc_nominal = (st_pib - st_pib1)/st_pib1

selic = quandl.get("BCB/432", start_date = "2015-01-01")
plt.figure(figsize=(20,10))
plt.plot(selic)
ouro.rename(columns = {"Value" : "selic"}, inplace = True)

dolar = quandl.get("BCB/10813", start_date="2000-01-01")
plt.figure(figsize=(20,10))
plt.plot(dolar)
dolar.rename(columns = {"Value" : "dolar"}, inplace = True)


"RETORNOS"
itau = 'ITSA4.SA'
bradesco = 'BBDC3.SA'
pan = 'BIDI4.SA'
santander = 'SANB4.SA'
btg = 'BPAC3.SA'
bb = 'BBAS3.SA'
inter = 'BIDI11.SA'

df_st = pd.DataFrame()

stocks = [itau, bradesco, pan, santander, btg,bb]

for stock in stocks:
    df_st[stock]=wb.DataReader(stock, data_source='yahoo', start='2017-1-1')['Adj Close']

 
df_st = (df_st/df_st.iloc[0]*100)
plt.figure(figsize=(20,10)) 
plt.plot(df_st)
df_st.plot()

"RISCO"
"Desvio_Padrão(Volatilidade)
df_st.std()


'AÇÕES
itau = wb.DataReader('ITSA4.SA', data_source = 'yahoo', start='2020-6-1')
itau.rename(columns = {"Adj Close":"ITAU"}, inplace = True)
itau = itau.drop(itau.columns[[0,1,2,3,4]], axis =1)
itau = (itau/itau.iloc[0])*100
itau.plot(figsize=(20,10))
plt.ylabel('ADJ_CLOSE')
plt.xlabel('DATE')
plt.show()

bradesco = wb.DataReader('BBDC3.SA', data_source = 'yahoo', start='2017-1-1')
bradesco.rename(columns = {"Adj Close":"BRADESCO"}, inplace = True)
bradesco = bradesco.drop(bradesco.columns[[0,1,2,3,4]], axis =1)
bradesco = (bradesco/bradesco.iloc[0])*100
bradesco.plot(figsize=(20,10))
plt.ylabel('ADJ_CLOSE')
plt.xlabel('DATE')
plt.show()

btg = wb.DataReader('BPAC3.SA', data_source = 'yahoo', start='2017-1-1')
btg.rename(columns = {"Adj Close":"BTG"}, inplace = True)
btg = btg.drop(btg.columns[[0,1,2,3,4]], axis =1)
btg = (btg/btg.iloc[0])*100
btg.plot(figsize=(20,10))
plt.ylabel('ADJ_CLOSE')
plt.xlabel('DATE')
plt.show()

bb = wb.DataReader('BBAS3.SA', data_source = 'yahoo', start='2017-1-1')
bb.rename(columns = {"Adj Close":"BB"}, inplace = True)
bb = bb.drop(bb.columns[[0,1,2,3,4]], axis =1)
bb = (bb/bb.iloc[0])*100
bb.plot(figsize=(20,10))
plt.ylabel('ADJ_CLOSE')
plt.xlabel('DATE')
plt.show() 

inter = wb.DataReader('BIDI11.SA', data_source = 'yahoo', start='2017-1-1')
inter.rename(columns = {"Adj Close":"INTER"}, inplace = True)
inter = inter.drop(inter.columns[[0,1,2,3,4]], axis =1)
inter = (bb/bb.iloc[0])*100



ibov = wb.DataReader('^BVSP', data_source = 'yahoo', start='2017-1-1')
ibov.rename(columns = {"Adj Close":"IBOV"}, inplace = True)
ibov = ibov.drop(ibov.columns[[0,1,2,3,4]], axis =1)
ibov = (ibov/ibov.iloc[0])*100
ibov.plot(figsize=(20,10))
plt.ylabel('ADJ_CLOSE')
plt.xlabel('DATE')
plt.show() 

"Betas"

"Variancia Ibov"
ibov_var = ibov.var()

"Covariancia entre mercado e ativos"
"ITAU"
from functools import reduce

cov_itau_frames = ([itau,ibov])
cov_itau = reduce(lambda left, right: pd.merge(left, right, on=['Date'], how = 'inner'), cov_itau_frames)
cov_itau = cov_itau[['ITAU','IBOV']].cov()
cov_itau_coef = cov_itau.iloc[0,1]
beta_itau = cov_itau_coef/ibov_var
print(beta_itau)

"BRADESCO"
cov_bradesco_frames = ([bradesco,ibov])
cov_bradesco = reduce(lambda left, right: pd.merge(left, right, on=['Date'], how = 'inner'), cov_bradesco_frames)
cov_bradesco = cov_bradesco[['BRADESCO','IBOV']].cov()
cov_bradesco_coef = cov_bradesco.iloc[0,1]
beta_bradesco = cov_bradesco_coef/ibov_var
print(beta_bradesco)

"BANCO DO BRASIL"
cov_bb_frames = ([bb,ibov])
cov_bb = reduce(lambda left, right: pd.merge(left, right, on=['Date'], how = 'inner'), cov_bb_frames)
cov_bb = cov_bradesco[['BB','IBOV']].cov()
cov_bb_coef = cov_bb.iloc[0,1]
beta_bb = cov_bb_coef/ibov_var
print(beta_bb)


"GRÁFICO
fig, ax1 = plt.subplots(figsize=(9,7))

color = 'tab:red'
ax1.set_xlabel('Data')
ax1.set_ylabel('selic', color=color)
ax1.plot(selic, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()

color = 'tab:blue'
ax2.set_ylabel('itau', color=color)
ax2.plot(itau, color=color)
ax2.tick_params(axis='y', labelcolor=color)
plt.show()



