
import sys
print(sys.executable)

#from __future__ import print_function
# !/usr/bin/python3.7
# -*- coding: utf-8 -*-
#from __future__ import print_function

import numpy as np
from prettytable import PrettyTable
import cplex


#--------------------Problema da Mochila----------------------------------#

#Exemplo Arenales, pág 237

#--------------Declaração dos parâmetros--------------------------#

#capital para investimento
b = 100

#custo do projeto j
aj = [47,40,17,27,34,23,5,44]

#retorno esperado do projeto j
pj = [41,33,14,25,32,32,9,19]

#--------------Fim da Declaração dos parâmetros--------------------------#

#Declaração dos conjuntos
n = len(aj)


#Criamos o objeto Cplex
model = cplex.Cplex()
                    
                    
#Declaração de variáveis:
#nome_do_modelo.variables.add(names =, lower bound - lb = [], types - continuous 'C' , Binary 'B',  integer 'I').
#Ex: Definir nome da variável (Índice) _varname = ["C_"+str(i)+"_"+str(j)]
#Adicionar ao modelo: model.variables.add(names = _varname, lb = [0], types = ['C'])

#Definimos das variáveis do modelo
model.variables.add(names=["X_{0}".format(j) #Variável X(j) #binária
                            for j in range(n)
                            ],
                    types=['B']*n)


#Definimos as restrições do modelo

#model.linear_constraints.add adiciona restrições (lin_expr = [], rhs = []. senses = '')
#senses = Equal 'E', 'G' Greater than, 'L' less than, 'R' ranged constraints
#lin_expr = [] é uma lista de lista que guarda os valores de sparsepair (lista de índice e respectivos valores do indice que estão também em lista)
#cpex.sparsePair(índice ind = colocar aqui os índices, value val - Respectivos valores dos índices)
#rhs = valor depois do sinal (igual, maior ou igual, menor ou igua etc)

#função objetivo max z = sum(j (X(j)*(p(j))


_vars = ["X_{0}".format(j) for j in range(n)]
_coef = [pj[j]for j in range(n)]
model.objective.set_linear(zip(_vars, _coef))
model.objective.set_sense(model.objective.sense.maximize)        


# Restrições 1= sum(j, x(j)*a(j)) <= b(j)


_vars = ["X_{0}".format(j) for j in range(n)]
_coef = [aj[j]for j in range(n)]
model.linear_constraints.add(
    lin_expr=[cplex.SparsePair(ind = _vars, val = _coef)],
    rhs=[b],
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
print("\t \t \t Problema da Mochila - Arenales, pág 237")
print("\n")


'''
#Obtendo o status e valor de resolução:

print(str(model.solution.get_status()))
print(str(round(model.solution.get_objective_value(),0)))

'''
aux = []
#Obtem o valor de x:
print("Os valores de X(j) são:  ")
print(model.solution.get_values())
print("\n")


print("Valor da Função Objetivo: ", model.solution.get_objective_value(), "\n") #exibir o valor da FO na tela

