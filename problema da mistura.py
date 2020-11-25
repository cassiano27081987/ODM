
import sys
print(sys.executable)

#from __future__ import print_function
# !/usr/bin/python3.7
# -*- coding: utf-8 -*-
#from __future__ import print_function

import numpy as np
from prettytable import PrettyTable
import cplex


#--------------------Problema da Mistura----------------------------------#

#Exemplo Arenales, pág 18

#--------------Declaração dos parâmetros--------------------------#

#porcetagen do componente i no ingrediente j
aij = [[0.2,0.5,0.4],
       [0.6,0.4,0.4]]

#fração do componente i na mistura j
bi = [0.3, 0.5]

#o custo de uma unidade do ingrediente j
cj = [0.56, 0.81, 0.46]

#valor mínimo da mistura j
li = 100

#valor máximo da mistura j
ui = 200

#--------------Fim da Declaração dos parâmetros--------------------------#

#Declaração dos conjuntos
i = len(bi)
j = len(cj)

#Criamos o objeto Cplex
model = cplex.Cplex()
                    
                    
#Declaração de variáveis:
#nome_do_modelo.variables.add(names =, lower bound - lb = [], types - continuous 'C' , Binary 'B',  integer 'I').
#Ex: Definir nome da variável (Índice) _varname = ["C_"+str(i)+"_"+str(j)]
#Adicionar ao modelo: model.variables.add(names = _varname, lb = [0], types = ['C'])

#Definimos das variáveis do modelo
model.variables.add(names=["X_{0}".format(j) #Variável x(j) #contínua
                            for j in range(j)],
                    types=['C']*j)

#Definimos as restrições do modelo

#model.linear_constraints.add adiciona restrições (lin_expr = [], rhs = []. senses = '')
#senses = Equal 'E', 'G' Greater than, 'L' less than, 'R' ranged constraints
#lin_expr = [] é uma lista de lista que guarda os valores de sparsepair (lista de índice e respectivos valores do indice que estão também em lista)
#cpex.sparsePair(índice ind = colocar aqui os índices, value val - Respectivos valores dos índices)
#rhs = valor depois do sinal (igual, maior ou igual, menor ou igua etc)

#função objetivo min z = sum(j, (c(j)*x(j))) 
_vars = ["X_{0}".format(j) for j in range(j)]
_coef = [cj[j] for j in range(j)]
model.objective.set_linear(zip(_vars, _coef))
model.objective.set_sense(model.objective.sense.minimize)


# Restrições 1 = sum(j, x(j)) = 1

_vars = ["X_{0}".format(j) for j in range(j)]
_coef = [1.0] * len(_vars)
model.linear_constraints.add(
lin_expr=[cplex.SparsePair(ind = _vars, val = _coef)],
rhs=[1.0],
senses="E")

# Restrições 2
for i in range(i):
    _vars = ["X_{0}".format(j) for j in range(j)]
    _coef = [aij[i][j] for j in range(j)]
    model.linear_constraints.add(
    lin_expr=[cplex.SparsePair(ind = _vars, val = _coef)],
    rhs=[bi[i]],
    senses="G")    
    
'''    
for i in range(i):
    _vars = ["X_{0}".format(j) for j in range(j)]
    _coef = [1.0] * len(_vars)
    model.linear_constraints.add(
    lin_expr=[cplex.SparsePair(ind = _vars, val = _coef)],
    rhs=[li],
    senses="G")   
    
for i in range(i):
    _vars = ["X_{0}".format(j) for j in range(j)]
    _coef = [1.0] * len(_vars)
    model.linear_constraints.add(
    lin_expr=[cplex.SparsePair(ind = _vars, val = _coef)],
    rhs=[ui],
    senses="L")       
'''
_vars = ["X_{0}".format(j) for j in range(j)]
_coef = [1.0] * len(_vars)
model.linear_constraints.add(
lin_expr=[cplex.SparsePair(ind = _vars, val = _coef)],
rhs=[0.0],
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
print("\t \t \t Problema da Mistura - Arenales, pág 18")
print("\n")

'''
#Obtendo o status e valor de resolução:

print(str(model.solution.get_status()))
print(str(round(model.solution.get_objective_value(),0)))
'''

#Obtem o valor de X:
print("Os valores de X(j) são:  ")

producao = []


producao = [
    [
        model.solution.get_values("X_{0}".format(j))
        for j in range(j)
    ]
]

      

#float(producao) = np.array(producao)
print(producao) #exibir o valor da sequencia ótima na tela
print("\n")

print("Valor da Função Objetivo: ", model.solution.get_objective_value(), "\n") #exibir o valor da FO na tela