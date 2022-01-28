# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 21:15:14 2021

@author: USUARIO
"""

#live 18-01-2020 - Criptomoedas

#bibliotecas
import pandas as pd
import numpy as np
import pandas_datareader as wb
import matplotlib.pyplot as plt
import seaborn as sns


#cesta de ativos

carteira_cripto = pd.DataFrame()

criptos = ['ETH-USD', 'XRP-USD', 'LTC-USD', 'XMR-USD', 'BTC-USD']

for i in criptos:
    carteira_cripto[i] = wb.DataReader(i, data_source='yahoo', start='2019-01-18')['Adj Close']

    
#atribuindo pesos
pesos = np.array([0.20, 0.20, 0.20, 0.20, 0.20])

#retornos
retorno = carteira_cripto.pct_change()


#matriz de diagramas de dispersão
sns.pairplot(retorno[1:])

#mapa de calor das correlações
sns.heatmap(retorno.corr(), annot=True)

#retorno acumulado
returns_acm = (1 + retorno).cumprod()
#plota retornos acumulados
returns_acm.plot()
#calcula retorno carteira x pesos   
retorno_total = returns_acm * pesos
#calcula retoerno total da carteira
retorno_total["total"] = retorno_total.sum(axis=1)

# Modificação feita em 28/01/2022 para evitar o display da configuração gráfica
retorno_total['total'].plot();

#matriz covariancia
cov_matrix = retorno.cov()
cov_matrix

#voltilidade do portfólio
port_volatility = np.sqrt(np.dot(pesos.T, np.dot(cov_matrix, pesos)))

vol_ano = port_volatility*np.sqrt(252)

print(vol_ano)


#Otimização Max-Sharpe
from pypfopt.expected_returns import capm_return

#Estimadores de retorno

#CAPM
mu = capm_return(carteira_cripto, risk_free_rate=0.00157)

from pypfopt import risk_models

#matriz covariância
from pypfopt.risk_models import CovarianceShrinkage


#Modelos de Risco
#estimativa de matriz de covariância
S = CovarianceShrinkage(carteira_cripto).ledoit_wolf()

#Técnica de Otimização - Fronteira Eficiente
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import objective_functions
ef = EfficientFrontier(mu, S)
ef.add_objective(objective_functions.L2_reg, gamma=0.1)

#Máximo Sharpe_Ratio
weights = ef.max_sharpe(risk_free_rate=0.00157)

ef.portfolio_performance(verbose=True)

#calcula retorno carteira x pesos   
retorno_sharpe = returns_acm * weights
#calcula retoerno total da carteira
retorno_sharpe["total"] = retorno_sharpe.sum(axis=1)

#voltilidade do portfólio
port_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

vol_ano = port_volatility*np.sqrt(252)


# -*- coding: utf-8 -*-


#live 18-01-2020 - Criptomoedas

#bibliotecas

import pandas as pd
import numpy as np
import pandas_datareader as wb
import matplotlib.pyplot as plt
import seaborn as sns

#cesta de ativos

criptos = ['ETH-USD', 'XRP-USD', 'LTC-USD', 'XMR-USD', 'BTC-USD']


carteira_cripto = pd.DataFrame()

for i in criptos:
    carteira_cripto[i] = wb.DataReader(i, data_source='yahoo', start='2019-01-18')['Adj Close']
    

#atribuindo pesos
pesos = np.array([0.2,0.2,0.2,0.2,0.2])

#retornos 
retorno = carteira_cripto.pct_change()

#pairplot
sns.pairplot(retorno[1:])

#mapa de calor das correlações
sns.heatmap(retorno.corr(), annot=True)

#retorno_acumulado
retorno_acm = (1+retorno).cumprod()
retorno_acm.plot()

#retorno_carteira
retorno_total = retorno_acm*pesos

#retorno_carteira
retorno_total['total'] = retorno_total.sum(axis=1)

#matriz covariacia
cov_matrix = retorno.cov()
cov_matrix

#volatilidade diária portfolio
port_volatility = np.sqrt(np.dot(pesos.T,np.dot(cov_matrix, pesos)))
vol_ano = port_volatility*np.sqrt(365)

#Otimização de Portfólio

#1 - Retornos Esperados

from pypfopt.expected_returns import capm_return

retornos_esperados = capm_return(carteira_cripto, risk_free_rate=0.00157, frequency=365)

#2 - Modelo de Risco
from pypfopt.risk_models import CovarianceShrinkage

#estimativa de matriz de covariancia
m_cov = CovarianceShrinkage(carteira_cripto, frequency=365).ledoit_wolf()

#3 Otimização
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import objective_functions

ef = EfficientFrontier(retornos_esperados, m_cov)
ef.add_objective(objective_functions.L2_reg, gamma=0.1)

#max_sharpe_ratio
pesos_sharpe = ef.max_sharpe(risk_free_rate=0.00157)

#calcula retorno carteira x pesos   
retorno_sharpe = retorno_acm * pesos_sharpe
#calcula retoerno total da carteira
retorno_sharpe["total"] = retorno_sharpe.sum(axis=1)

#
ef.portfolio_performance(verbose=True)


