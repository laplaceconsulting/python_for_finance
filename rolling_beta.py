# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 11:32:08 2021

@author: USUARIO
"""

#utilizando a função rolling para calcular beta e alfa

#importando bibliotecas
import pandas as pd
from pandas_datareader import data as wb
import matplotlib.pyplot as plt

#Rolling Beta Itau com Ibovespa

#Importando ibovespa
ibov =  wb.DataReader('^BVSP', data_source = 'yahoo', start='2019-01-01', end='2020-12-31')
ibov.rename(columns = {"Adj Close":"IBOV"}, inplace = True)
ibov = ibov.drop(ibov.columns[[0,1,2,3,4]], axis =1)

#Importando Itau
itau =  wb.DataReader('ITSA4.SA', data_source = 'yahoo', start='2019-01-01', end='2020-12-31')
itau.rename(columns = {"Adj Close":"ITAU"}, inplace = True)
itau = itau.drop(itau.columns[[0,1,2,3,4]], axis =1)


#calcular retornos remover nan's
itau_retornos = itau.pct_change().dropna()
ibov_retornos = ibov.pct_change().dropna()

#rolling beta
import statsmodels.api as sm
from statsmodels.regression.rolling import RollingOLS

regressao = RollingOLS(ibov_retornos, itau_retornos, window=60).fit()
beta_rolling = regressao.params

beta_rolling.plot()
