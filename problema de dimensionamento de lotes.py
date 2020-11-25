
import sys
print(sys.executable)

#from __future__ import print_function
# !/usr/bin/python3.7
# -*- coding: utf-8 -*-
#from __future__ import print_function

import numpy as np
from prettytable import PrettyTable
import cplex


#-----------------Problema de Dimensionamento de Lotes Estático----------------#

#Exemplo Arenales, pág 31

#--------------Declaração dos parâmetros--------------------------#

#demanda do item i no período t, i = 1, ..., n, t = 1, ..., T
dit = [[100, 90, 120],
       [40, 40, 40]]


#custo de produzir uma unidade do item i no período t
cit = [[20,20,30],
       [20,20,30]]

#custo de estocar uma unidade do item i no período t
hit = [[2.0, 3.0, 0.0],
       [2.5, 3.5, 0.0]]


#disponibilidade de recursos (renováveis) no período t
rt = [40, 40, 40]

#quantidade de recursos necessários para a produção de uma unidade do item i
ri = [15, 20]


#--------------Fim da Declaração dos parâmetros--------------------------#

#Declaração dos conjuntos
m = (len(dit[0]))
n = (len(dit))

#Criamos o objeto Cplex
model = cplex.Cplex()
                    
                    
#Declaração de variáveis:
#nome_do_modelo.variables.add(names =, lower bound - lb = [], types - continuous 'C' , Binary 'B',  integer 'I').
#Ex: Definir nome da variável (Índice) _varname = ["C_"+str(i)+"_"+str(j)]
#Adicionar ao modelo: model.variables.add(names = _varname, lb = [0], types = ['C'])

#Definimos das variáveis do modelo
model.variables.add(names=["X_{0}_{1}".format(i,t) #Variável x(i,t) qtd de produtos i produzidos no período t
                            for i in range(n)
                            for t in range(m)],
                    types=['C']*n*m)

model.variables.add(names=["I_{0}_{1}".format(i,t) #Variável I(i,t) qtd de produtos i que devem ser estocados no período t
                            for i in range(n)
                            for t in range(m)],
                    types=['C']*n*m)



#fixa o estoque inicial
'''
model.variables.set_upper_bounds("I_{0}_{1}".format(0, 0), 0.0)
model.variables.set_upper_bounds("I_{0}_{1}".format(1, 0), 0.0)
model.variables.set_lower_bounds("I_{0}_{1}".format(0, 2), 0.0)
model.variables.set_lower_bounds("I_{0}_{1}".format(1, 2), 0.0)


#fixa o estoque final
model.variables.set_upper_bounds("I_{0}_{1}".format(0, 2), 0.0)
model.variables.set_upper_bounds("I_{0}_{1}".format(1, 2), 0.0)
model.variables.set_lower_bounds("I_{0}_{1}".format(0, 2), 0.0)
model.variables.set_lower_bounds("I_{0}_{1}".format(1, 2), 0.0)
'''

#Definimos as restrições do modelo

#model.linear_constraints.add adiciona restrições (lin_expr = [], rhs = []. senses = '')
#senses = Equal 'E', 'G' Greater than, 'L' less than, 'R' ranged constraints
#lin_expr = [] é uma lista de lista que guarda os valores de sparsepair (lista de índice e respectivos valores do indice que estão também em lista)
#cpex.sparsePair(índice ind = colocar aqui os índices, value val - Respectivos valores dos índices)
#rhs = valor depois do sinal (igual, maior ou igual, menor ou igua etc)

#função objetivo min z = sum(i,t (X(i,t)*c(i,t))) + sum(i,t (I(i,t)*h(i,t)))


_vars = ["X_{0}_{1}".format(i, t) for i in range(n) for t in range(m)] + \
        ["I_{0}_{1}".format(i, t) for i in range(n) for t in range(m)]

_coef = [cit[i][t] for i in range(n) for t in range(m)] + \
        [hit[i][t] for i in range(n) for t in range(m)]

model.objective.set_linear(zip(_vars, _coef))
model.objective.set_sense(model.objective.sense.minimize)      


# Restrições 1 => X(i,t) + I(i,t-1) − I(i,t) = d(i,t) i = 1, ..., n, t = l, ..., T

for i in range(n):
    for t in range(m):
        if t < 1:
            _vars = ["X_{0}_{1}".format(i, t)] + ["I_{0}_{1}".format(i, t)]
            _coef = [1] + [-1]
            model.linear_constraints.add(
                lin_expr=[cplex.SparsePair(ind=_vars, val=_coef)],
                rhs=[dit[i][t]],
                senses="E")
        else:
            _vars = ["X_{0}_{1}".format(i, t)] + ["I_{0}_{1}".format(i, t - 1)] + ["I_{0}_{1}".format(i, t)]
            _coef = [1] + [1] + [-1]
            model.linear_constraints.add(
                lin_expr=[cplex.SparsePair(ind=_vars, val=_coef)],
                rhs=[dit[i][t]],
                senses="E")

# Restrições 2 =>sum(i, X(i,t)*r(i)) ≤ R(t) t = l, ..., T

for t in range(m):
    _vars = ["X_{0}_{1}".format(i, t) for i in range(n)]
    _coef = [ri[i] for i in range(n)]
    model.linear_constraints.add(
        lin_expr=[cplex.SparsePair(ind = _vars, val = _coef)],
        rhs=[rt[t]] ,
        senses="L")

# Restrições 3 =>X(i,t) , I(i,t) ≥ 0 i = 1, ..., n, t = l, ..., T

for i in range(n):
    for t in range(m):
        _vars = ["X_{0}_{1}".format(i, t)]
        _coef = [1] 
        model.linear_constraints.add(
            lin_expr=[cplex.SparsePair(ind = _vars, val = _coef)],
            rhs=[0.0],
            senses="G")

for i in range(n):
    for t in range(m):
        _vars = ["I_{0}_{1}".format(i, t)]
        _coef = [1] 
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
print("\t \t \t Problema de Dimensionamento de Lotes Estático- Arenales, pág 31")
print("\n")

'''
#Obtendo o status e valor de resolução:

print(str(model.solution.get_status()))
print(str(round(model.solution.get_objective_value())))
'''

#Obtem o valor de X:
print("Os valores de X(i,t) são:  ")

producao = np.zeros((n,m))
producao = [
    [
        int(model.solution.get_values("X_{0}_{1}".format(i,j))) for i in range(n)for j in range(m)
    ]
]
producao = np.array(producao)
print(producao.reshape(len(ri),len(rt))) #exibir o valor da sequencia ótima na tela
print("\n")


#Obtem o valor de I:
print("Os valores de I(i,t) são:  ")

estoque = np.zeros((n,m))

estoque= [
    [
       int(model.solution.get_values("I_{0}_{1}".format(i,j))) for i in range(n)for j in range(m)
    ]
]
estoque = np.array(estoque)
print(estoque.reshape(len(ri),len(rt))) #exibir o valor da sequencia ótima na tela

print("\n")
print("Valor da Função Objetivo: ", model.solution.get_objective_value(), "\n") #exibir o valor da FO na tela