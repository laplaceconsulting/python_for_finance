# -*- coding: utf-8 -*-
"""
Created on Fri May 29 18:41:52 2020

@author: USUARIO
"""

"Analise Quantitativa Carteira dos Menino"

import pandas as pd
import numpy as np
from pandas_datareader import data as wb
import quandl 
quandl.ApiConfig.api_key = "4NFLzs3fgqxK3JHsN-dX"
import matplotlib.pyplot as plt


#MACROECONOMINCO"
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



#RETORNOS"
itau = 'ITSA4.SA'
cvc = 'CVCB3.SA'
locaweb = 'LWSA3.SA'
taesa = 'TAEE11.SA'
mafrig = 'MRFG3.SA'

df_st = pd.DataFrame()

stocks = [itau, cvc, locaweb, taesa, mafrig]

for stock in stocks:
    df_st[stock]=wb.DataReader(stock, data_source='yahoo', start='2020-6-1')['Adj Close']

 
df_st = (df_st/df_st.iloc[0]*100)
plt.figure(figsize=(20,10)) 
plt.plot(df_st)
df_st.plot()

#"RISCO"
#Desvio_Padrão(Volatilidade)
df_st.std()


#AÇÕES
itau = wb.DataReader('ITSA4.SA', data_source = 'yahoo', start='2015-1-1')
itau.rename(columns = {"Adj Close":"ITAU"}, inplace = True)
itau = itau.drop(itau.columns[[0,1,2,3,4]], axis =1)
itau_ret = ((((itau/itau.shift(1))-1).mean())*100)*252
itau = np.log(itau/itau.shift(1))

petro = wb.DataReader('PETR4.SA', data_source = 'yahoo', start='2017-1-1')
petro.rename(columns = {"Adj Close":"PETRO"}, inplace = True)
petro = petro.drop(petro.columns[[0,1,2,3,4]], axis =1)
petro_ret = ((((petro/petro.shift(1))-1).mean())*100)*252
petro = np.log(petro/petro.shift(1))

cvc = wb.DataReader('CVCB3.SA', data_source = 'yahoo', start='2017-1-1')
cvc.rename(columns = {"Adj Close":"CVC"}, inplace = True)
cvc = cvc.drop(cvc.columns[[0,1,2,3,4]], axis =1)
cvc_ret = ((((cvc/cvc.shift(1))-1).mean())*100)*252
cvc = np.log(cvc/cvc.shift(1))

locaweb = wb.DataReader('LWSA3.SA', data_source = 'yahoo', start='2019-1-1')
locaweb.rename(columns = {"Adj Close":"LOCAWEB"}, inplace = True)
locaweb = locaweb.drop(locaweb.columns[[0,1,2,3,4]], axis =1)
locaweb_ret = ((((locaweb/locaweb.shift(1))-1).mean())*100)*252
locaweb = np.log(locaweb/locaweb.shift(1))

taesa = wb.DataReader('TAEE11.SA', data_source = 'yahoo', start='2017-1-1')
taesa.rename(columns = {"Adj Close": "TAESA"}, inplace = True)
taesa = taesa.drop(taesa.columns[[0,1,2,3,4]], axis =1)
taesa_ret = ((((taesa/taesa.shift(1))-1).mean())*100)*252
taesa = np.log(taesa/taesa.shift(1))
    
mafrig = wb.DataReader('MRFG3.SA', data_source = 'yahoo', start='2017-1-1')
mafrig.rename(columns = {"Adj Close": "MAFRIG"}, inplace = True)
mafrig = mafrig.drop(mafrig.columns[[0,1,2,3,4]], axis =1)
mafrig_ret = ((((mafrig/mafrig.shift(1))-1).mean())*100)*252
mafrig = np.log(mafrig/mafrig.shift(1)) 

#Juntando os dataframes"

from functools import reduce

dataframes = [itau, petro, cvc, locaweb, taesa, mafrig]
carteira = reduce(lambda left, right: pd.merge(left, right, on=['Date'], how = 'inner'), dataframes)

import seaborn as sns

sns.heatmap(carteira.corr(), annot = True)

#Média dos Retornos
raiz = np.sqrt(252)

#Volatilidade"
itau_std = (itau.std()*raiz)
locaweb_std = (locaweb.std()*raiz)
taesa_std = (taesa.std()*raiz)
mafrig_std = (mafrig.std()*raiz)
cvc_std = (cvc.std()*raiz)
petro_std = (petro.std()*raiz)

volatilidade_carteira = [itau_std, locaweb_std, taesa_std, mafrig_std]


#Betas"

ibov = wb.DataReader('^BVSP', data_source = 'yahoo', start='2017-1-1')
ibov.rename(columns = {"Adj Close":"IBOV"}, inplace = True)
ibov = ibov.drop(ibov.columns[[0,1,2,3,4]], axis =1)
ibov = np.log(ibov/ibov.shift(1))
ibov.plot(figsize=(20,10))
plt.ylabel('ADJ_CLOSE')
plt.xlabel('DATE')
plt.show() 

#Betas"

#Variancia Ibov"
ibov_var = ibov.var()

#Covariancia entre mercado e ativos"
#ITAU"
from functools import reduce

cov_itau_frames = ([itau,ibov])
cov_itau = reduce(lambda left, right: pd.merge(left, right, on=['Date'], how = 'inner'), cov_itau_frames)
cov_itau = cov_itau[['ITAU','IBOV']].cov()
cov_itau_coef = cov_itau.iloc[0,1]
beta_itau = cov_itau_coef/ibov_var
print(beta_itau)

cov_petro_frames = ([petro,ibov])
cov_petro = reduce(lambda left, right: pd.merge(left, right, on=['Date'], how = 'inner'), cov_petro_frames)
cov_petro = cov_petro[['PETRO','IBOV']].cov()
cov_petro_coef = cov_petro.iloc[0,1]
beta_petro = cov_petro_coef/ibov_var
print(beta_petro)

cov_cvc_frames = ([cvc,ibov])
cov_cvc = reduce(lambda left, right: pd.merge(left, right, on=['Date'], how = 'inner'), cov_cvc_frames)
cov_cvc = cov_cvc[['CVC','IBOV']].cov()
cov_cvc_coef = cov_cvc.iloc[0,1]
beta_cvc = cov_cvc_coef/ibov_var
print(beta_cvc)


cov_locaweb_frames = ([locaweb,ibov])
cov_locaweb = reduce(lambda left, right: pd.merge(left, right, on=['Date'], how = 'inner'), cov_locaweb_frames)
cov_locaweb = cov_locaweb[['LOCAWEB','IBOV']].cov()
cov_locaweb_coef = cov_locaweb.iloc[0,1]
beta_locaweb = cov_locaweb_coef/ibov_var
print(beta_locaweb)

cov_taesa_frames = ([taesa,ibov])
cov_taesa = reduce(lambda left, right: pd.merge(left, right, on=['Date'], how = 'inner'), cov_taesa_frames)
cov_taesa = cov_taesa[['TAESA','IBOV']].cov()
cov_taesa_coef = cov_taesa.iloc[0,1]
beta_taesa = cov_taesa_coef/ibov_var
print(beta_taesa)

cov_mafrig_frames = ([mafrig,ibov])
cov_mafrig = reduce(lambda left, right: pd.merge(left, right, on=['Date'], how = 'inner'), cov_mafrig_frames)
cov_mafrig = cov_mafrig[['MAFRIG','IBOV']].cov()
cov_mafrig_coef = cov_mafrig.iloc[0,1]
beta_mafrig = cov_mafrig_coef/ibov_var
print(beta_mafrig)



#VAR95"


sorted_95_itau = itau.sort_values(['ITAU'])
var_95_itau = np.percentile(sorted_95_itau, 5)
print(var_95_itau)

sorted_95_itau

plt.hist(sorted_95_itau, normed=True)
plt.axvline(x=var_95_itau, color='r', linestyle='-', label="VaR 95: {0:.2f}%".format(var_95_itau))
plt.show()


var_95_cvc = np.percentile(cvc, 5)
print(var_95_cvc)


