
import sys
print(sys.executable)

#from __future__ import print_function
# !/usr/bin/python3.7
# -*- coding: utf-8 -*-
#from __future__ import print_function

import numpy as np
from prettytable import PrettyTable
import cplex


#--------------------Problema da Designação----------------------------------#

#Exemplo Arenales, pág 243

#--------------Declaração dos parâmetros--------------------------#

#custo de processamento da tarefa j pelo processador i
cij = [[15,61,3,94,86,68,69,51],[21,28,76,48,54,85,69,72],[21,21,46,43,21,3,84,44]]

#tempo de processamento da tarefa j pelo processador i
aij = [[31,69,14,87,51,65,35,44],[23,20,71,86,91,57,30,74],[20,55,39,60,83,67,35,32]]

#recurso disponível
bi = [100,100,100]

#--------------Fim da Declaração dos parâmetros--------------------------#

#Declaração dos conjuntos
n = len(aij)
m = len(aij[0])

#Criamos o objeto Cplex
model = cplex.Cplex()
                    
                    
#Declaração de variáveis:
#nome_do_modelo.variables.add(names =, lower bound - lb = [], types - continuous 'C' , Binary 'B',  integer 'I').
#Ex: Definir nome da variável (Índice) _varname = ["C_"+str(i)+"_"+str(j)]
#Adicionar ao modelo: model.variables.add(names = _varname, lb = [0], types = ['C'])

#Definimos das variáveis do modelo
model.variables.add(names=["X_{0}_{1}".format(i,j) #Variável X(j) #binária
                            for i in range(n)
                            for j in range(m)],
                    types=['B']*n*m)


#Definimos as restrições do modelo

#model.linear_constraints.add adiciona restrições (lin_expr = [], rhs = []. senses = '')
#senses = Equal 'E', 'G' Greater than, 'L' less than, 'R' ranged constraints
#lin_expr = [] é uma lista de lista que guarda os valores de sparsepair (lista de índice e respectivos valores do indice que estão também em lista)
#cpex.sparsePair(índice ind = colocar aqui os índices, value val - Respectivos valores dos índices)
#rhs = valor depois do sinal (igual, maior ou igual, menor ou igua etc)

#função objetivo min z = sum(j (X(i,j)*(c(i,j))

_vars = ["X_{0}_{1}".format(i,j) for i in range(n) for j in range(m)]
_coef = [cij[i][j]for i in range(n) for j in range(m)]
model.objective.set_linear(zip(_vars, _coef))
model.objective.set_sense(model.objective.sense.minimize)        


# Restrições 1= sum(i, x(i,j)=1

for j in range(m):
    _vars = ["X_{0}_{1}".format(i,j) for i in range(n)]
    _coef = [1.0]*len(_vars)
    model.linear_constraints.add(
        lin_expr=[cplex.SparsePair(ind = _vars, val = _coef)],
        rhs=[1.0],
        senses="E")   



# Restrições 1= sum(j, x(i,j)*a(i,jj)) <= b(i)

for i in range(n):
    _vars = ["X_{0}_{1}".format(i,j) for j in range(m)]
    _coef = [aij[i][j] for j in range(m)]
    model.linear_constraints.add(
        lin_expr=[cplex.SparsePair(ind = _vars, val = _coef)],
        rhs=[bi[i]],
        senses="L")   
   

    
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
print("\t \t \t Problema de Atribuição - Arenales, pág 243")
print("\n")


'''
#Obtendo o status e valor de resolução:

print(str(model.solution.get_status()))
print(str(round(model.solution.get_objective_value(),0)))

'''
#Obtem o valor de X:
print("Os valores de X(i,t) são:  ")

producao = np.zeros((n,m))
producao = [
    [
        int(model.solution.get_values("X_{0}_{1}".format(i,j))) 
        for i in range(n)for j in range(m)
    ]
]
producao = np.array(producao)
print(producao.reshape(len(cij),len(cij[0]))) #exibir o valor da sequencia ótima na tela
print("\n")


print("Valor da Função Objetivo: ", model.solution.get_objective_value(), "\n") #exibir o valor da FO na tela

