
import sys
print(sys.executable)

#from __future__ import print_function
# !/usr/bin/python3.7
# -*- coding: utf-8 -*-
#from __future__ import print_function

import numpy as np
from prettytable import PrettyTable
import cplex


#--------------------Problema de Transporte----------------------------------#

#Exemplo Arenales, pág 21

#--------------Declaração dos parâmetros--------------------------#

#matrix de custos de se transportar uma unidade do produto de cada centro de produção a cada mercado consumidor
cit = [[27.7, 59.8, 70.8],
       [10.4,52.0,34.1]]


#quantidade máxima disponível do produto em cada centro de produção
ai = [800, 1000]

#demandas
bj = [500, 400, 900]

#--------------Fim da Declaração dos parâmetros--------------------------#

#Declaração dos conjuntos
n = len(ai)
m = len(bj)


#Criamos o objeto Cplex
model = cplex.Cplex()
                    
                    
#Declaração de variáveis:
#nome_do_modelo.variables.add(names =, lower bound - lb = [], types - continuous 'C' , Binary 'B',  integer 'I').
#Ex: Definir nome da variável (Índice) _varname = ["C_"+str(i)+"_"+str(j)]
#Adicionar ao modelo: model.variables.add(names = _varname, lb = [0], types = ['C'])

#Definimos das variáveis do modelo
model.variables.add(names=["X_{0}_{1}".format(i,j) #Variável x(i,j) #inteira
                            for i in range(n)
                            for j in range(m)],
                    types=['C']*n*m)


#Definimos as restrições do modelo

#model.linear_constraints.add adiciona restrições (lin_expr = [], rhs = []. senses = '')
#senses = Equal 'E', 'G' Greater than, 'L' less than, 'R' ranged constraints
#lin_expr = [] é uma lista de lista que guarda os valores de sparsepair (lista de índice e respectivos valores do indice que estão também em lista)
#cpex.sparsePair(índice ind = colocar aqui os índices, value val - Respectivos valores dos índices)
#rhs = valor depois do sinal (igual, maior ou igual, menor ou igua etc)

#função objetivo min z = sum(i,t (X(i,t))) + sum(i,t (I(i,t))) 

for i in range (n):
    for t in range(m):
        _vars = ["X_{0}_{1}".format(i, t)]
        _coef = [cit[i][t]]
        model.objective.set_linear(zip(_vars, _coef))
        model.objective.set_sense(model.objective.sense.minimize)        



# Restrições 1 => sum(j, x(i,j)) <= a(i)

for i in range(n):
    _vars = ["X_{0}_{1}".format(i, j) for j in range(m)]
    _coef = [1.0] * len(_vars)
    model.linear_constraints.add(
    lin_expr=[cplex.SparsePair(ind = _vars, val = _coef)],
    rhs=[ai[i]],
    senses="L")


# Restrições 2= sum(i, x(i,j)) = b(j)

for j in range(m):
    _vars = ["X_{0}_{1}".format(i, j) for i in range(n)]
    _coef = [1.0]*len(_vars)
    model.linear_constraints.add(
    lin_expr=[cplex.SparsePair(ind = _vars, val = _coef)],
    rhs=[bj[j]],
    senses="E")   
   
for i in range (n):
    for j in range (m):
        _vars = ["X_{0}_{1}". format(i,j)]
        _coef = [1.0]
        model.linear_constraints.add(
        lin_expr=[cplex.SparsePair(ind =_vars, val = _coef)],
        rhs = [0.0],
        senses="G")

    
model.solve() #resolve o modelo


#Configurações do CPLEX:

model.parameters.timelimit.set(300)#Limite de tempo de execucao


model.parameters.mip.tolerances.mipgap.set(0.0)#Forca parada apenas com gap 0.0


model.parameters.mip.display.set(0)#Elimina a saida padrao do CPLEX

#Obtendo o tempo necessário para executar o modelo:
initiTime = model.get_time()
model.solve()
finalTime = model.get_time()

print("\n")
print("\n")
print("\t \t \t Problema de Transporte - Arenales, pág 21")
print("\n")


'''
#Obtendo o status e valor de resolução:

print(str(model.solution.get_status()))
print(str(round(model.solution.get_objective_value(),0)))

'''
aux = []
#Obtem o valor de x:
print("Os valores de X(i,j) são:  ")
print(model.solution.get_values())
print("\n")


print("Valor da Função Objetivo: ", model.solution.get_objective_value(), "\n") #exibir o valor da FO na tela

