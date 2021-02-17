# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 19:49:35 2021

@author: USUARIO
"""

import pandas as pd
import numpy as np
import numpy_financial as npf
import matplotlib.pyplot as plt

#Valor Presente Valor Futuro
i = 0.05
periodos = 10
pagamento = 0
vp = -10000

valor_presente = npf.pv(i, periodos, pagamento, valor_futuro)
valor_presente

valor_futuro = npf.fv(i,periodos,pagamento,vp)
valor_futuro





#Case 1 - Empresa investir em uma nova planta
ativo = 100000000
passivo_oneroso = 40000000
patrimonio_liquido = 60000000
ki = 0.12
ke = 0.17

wacc = ((passivo_oneroso/ativo)*ki)+((patrimonio_liquido/ativo)*ke)

wacc

#VPL - Valor Presente Líquido

cf1 =np.array([-100,-50,30,30,30,30,50,60,70,80,80])

vpl = npf.npv(wacc,cf1)

vpl

#TIR - Taxa interna de retorno

tir = npf.irr(cf1)
tir

#MIRR - TIR Modificada

mirr = npf.mirr(cf1, wacc, 0.10)
mirr

if tir > wacc:
    print("Projeto agrega valor")
else:
    print("Projeto Destrói Valor")
    
    
#Qual a taxa?    
taxa = npf.rate(nper, pmt, pv, fv)

#Qual  Parcela
parcela = npf.pmt(rate, nper, pv)

#Valuation de Padaria

#premissas
lucro_operacional = 50000
despesas_capital = 5000
delta_ncg = 3000
reivestimento = (despesas_capital+delta_ncg)
i_crescimento = 0.02

periodo = np.array([0,1,2,3,4,5])


FCf = (lucro_operacional - reivestimento)
FCf

#Período Explíticito

vp_fcf = npf.pv(wacc,5, pmt=-FCf,when='begin')
vp_fcf

#Perpetuiddade
perpetuidade = (FCf*(1+i_crescimento)/(wacc-i_crescimento))

valor_negocio = vp_fcf + perpetuidade

valor_negocio

