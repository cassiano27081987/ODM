
import sys
print(sys.executable)

#from __future__ import print_function
# !/usr/bin/python3.7
# -*- coding: utf-8 -*-
#from __future__ import print_function

import numpy as np
from prettytable import PrettyTable
import cplex


#--------------------Problema de Localização de Facilidades----------------------------------#

#Exemplo Arenales, pág 247

#--------------Declaração dos parâmetros--------------------------#

#distancia da facilidade até a unidade de atendimento j
cj = [20,76,16,23,23,18]

#incidência das regiões que necessitam da facilidade j
#aij = 1 se i pertence a Si. O caso contrário
aij =[[1,1,0,0,1,0],
      [1,0,1,0,0,0],
      [0,1,0,1,0,0],
      [0,0,1,0,0,1],
      [0,1,1,0,0,1]]


#--------------Fim da Declaração dos parâmetros--------------------------#

#Declaração dos conjuntos
m = len(aij)
n = len(aij[0])

print("o valor de n é: ", n)
print("o valor de m é: ", m)

print("\n")

#Criamos o objeto Cplex
model = cplex.Cplex()
                    
                    
#Declaração de variáveis:
#nome_do_modelo.variables.add(names =, lower bound - lb = [], types - continuous 'C' , Binary 'B',  integer 'I').
#Ex: Definir nome da variável (Índice) _varname = ["C_"+str(i)+"_"+str(j)]
#Adicionar ao modelo: model.variables.add(names = _varname, lb = [0], types = ['C'])

#Definimos das variáveis do modelo
model.variables.add(names=["X_{0}".format(j) #Variável X(j) #binária
                            for j in range(n)],
                    types=['B']*n)


#Definimos as restrições do modelo

#model.linear_constraints.add adiciona restrições (lin_expr = [], rhs = []. senses = '')
#senses = Equal 'E', 'G' Greater than, 'L' less than, 'R' ranged constraints
#lin_expr = [] é uma lista de lista que guarda os valores de sparsepair (lista de índice e respectivos valores do indice que estão também em lista)
#cpex.sparsePair(índice ind = colocar aqui os índices, value val - Respectivos valores dos índices)
#rhs = valor depois do sinal (igual, maior ou igual, menor ou igua etc)

#função objetivo min z = sum(j (X(j)*(c(j))

_vars = ["X_{0}".format(j) for j in range(n)]
_coef = [cj[j] for j in range(n)]
model.objective.set_linear(zip(_vars, _coef))
model.objective.set_sense(model.objective.sense.minimize)        


# Restrições 1= sum(j, x(j)*a(j)) >= b(i)

for i in range(m):
    _vars = ["X_{0}".format(j) for j in range(n)]
    _coef = [aij[i][j]for j in range(n)]
    model.linear_constraints.add(
    lin_expr=[cplex.SparsePair(ind = _vars, val = _coef)],
    rhs=[1.0],
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
print("\t \t \t Problema de Localização de Facilidades - Arenales, pág 247")
print("\n")


'''
#Obtendo o status e valor de resolução:

print(str(model.solution.get_status()))
print(str(round(model.solution.get_objective_value(),0)))

'''
#Obtem o valor de X:
print("Os valores de X(j) são:  ")

localizacao_facilidades = np.zeros((n))
localizacao_facilidades = [
    [
        int(model.solution.get_values("X_{0}".format(j))) 
        for j in range(n)
    ]
]
localizacao_facilidades = np.array(localizacao_facilidades)
print(localizacao_facilidades.reshape(len(aij[0]))) #exibir o valor da sequencia ótima na tela
print("\n")


print("Valor da Função Objetivo: ", model.solution.get_objective_value(), "\n") #exibir o valor da FO na tela

