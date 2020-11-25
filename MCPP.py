
import sys
print(sys.executable)

#from __future__ import print_function
# !/usr/bin/python3.7
# -*- coding: utf-8 -*-
#from __future__ import print_function

import numpy as np
from prettytable import PrettyTable
import cplex


#------Problema de Dimensionamento de Lotes com Preservação da Preparação------#

#Exemplo Arenales pág 276

#--------------Declaração dos parâmetros--------------------------#

#demanda do item i no período t, i = 1, ..., n, t = 1, ..., T
dit = [[1,10,3,10],
       [2,4,0,5],
       [2,4,0,5]
       ]

#capacidade de produção (hora) de uma máquina (facilidade) no período t
ct = [280, 320, 280, 400]

#custo de estocar uma unidade do item i no período t 
hit = [[0,150,100,70],
       [0,150,100,70],
       [0,150,100,70]
       ]

#tempo para produzir uma unidade do item i,
bi = [20,10,20]

#tempo de preparação de máquina para processar o item i
spi = [40,40,40]

#custo de preparação do item i no período t
sit = [[350,100,90,90],
       [350,100,90,90],
       [350,100,90,90]
       ]

#número de recursos disponíveis
k = 1

#conjunto de índices que utilizam o recurso k
rk = [1,2,3]

#quantidade de itens i necessários para produzir um item j
rij = [[1,2,3],
       [1,2,3],
       [1,2,3]
       ]
       

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

model.variables.add(names=["Y_{0}_{1}".format(i,t) #Variável Y(i,t) = 1 se o item é produzido no período t. O caso contrário
                           for i in range(n)
                           for t in range(m)],
                    types=['B']*n*m)


model.variables.add(names=["AUX_{0}_{1}".format(i,t) #Variável auxiliar que armazena a necessidade dos filhos  do item i
                            for i in range(n)
                            for t in range(m)],
                    types=['C']*n*m)



#for i in range(n):
#    model.variables.set_upper_bounds("I_{0}_{1}".format(i, 0), 0.0) # estoque inicial não permitido

#Definimos as restrições do modelo

#model.linear_constraints.add adiciona restrições (lin_expr = [], rhs = []. senses = '')
#senses = Equal 'E', 'G' Greater than, 'L' less than, 'R' ranged constraints
#lin_expr = [] é uma lista de lista que guarda os valores de sparsepair (lista de índice e respectivos valores do indice que estão também em lista)
#cpex.sparsePair(índice ind = colocar aqui os índices, value val - Respectivos valores dos índices)
#rhs = valor depois do sinal (igual, maior ou igual, menor ou igua etc)

#função objetivo min z = sum(i,t (Y(i,t)*si(i))) + sum(i,t (I(i,t)*h(i)))

_vars = ["Y_{0}_{1}".format(i, t) for i in range(n) for t in range(m)] + \
        ["I_{0}_{1}".format(i, t) for i in range(n) for t in range(m)]

_coef = [sit[i][t] for i in range(n) for t in range(m)] + \
        [hit[i][t] for i in range(n) for t in range(m)]

model.objective.set_linear(zip(_vars, _coef))
model.objective.set_sense(model.objective.sense.minimize)      


  

# Restrições 1 => X(i,t) + I(i,t-1) − I(i,t) - sum(j, r(i,j)*X(j,t)) = d(i,t) i = 1, ..., n, t = l, ..., T

#calculo da necessidade de todos os itens filhos

'''
for j in range(len(rij)):
    for i in range(n):
        for t in range(m):
            _vars = ["AUX_{0}_{1}".format(i,t),"X_{0}_{1}".format(j, t)]
            _coef = [1] +[-rij[i][j]]
            model.linear_constraints.add(
                lin_expr=[cplex.SparsePair(ind = _vars, val = _coef)],
                rhs=[0.0],
                senses="E")
'''


for i in range(n):
    for t in range(1,m):
        _vars = ["X_{0}_{1}".format(i, t),"I_{0}_{1}".format(i, t-1),
                 "I_{0}_{1}".format(i, t)]
        _coef = [1] + [1] + [-6] 
        model.linear_constraints.add(
            lin_expr=[cplex.SparsePair(ind = _vars, val = _coef)],
            rhs=[dit[i][t]],
            senses="E")


# Restrições 2 =>sum(i, X(i,t)*r(i)) ≤ R(t) t = l, ..., T

for k in range(k):
    for t in range(m):
        _vars = ["Y_{0}_{1}".format(i, t),"X_{0}_{1}".format(i, t) ]
        _coef = [spi[i]*len(_vars)] +[bi[i]*len(_vars)]
        model.linear_constraints.add(
            lin_expr=[cplex.SparsePair(ind = _vars, val = _coef)],
            rhs=[ct[t]],
            senses="L")


# Restrições 3 =>X(i,t)<= M(i,t)*Y(i,t)

#Parametro adicional para limitar a capacidade
print("\n")

demanda_acumulada = list(map(sum,dit)) 
#demanda_acumulada.insert(3,24)
demanda_acumulada.insert(0,0)


print("A demanda acumulada é: ", demanda_acumulada)

print("\n")


for i in range(n):
    for j in range(m):
        _vars = ["X_{0}_{1}".format(i, t),"Y_{0}_{1}".format(i, t) ]
        _coef = [1] + [-demanda_acumulada[j]]
        model.linear_constraints.add(
            lin_expr=[cplex.SparsePair(ind = _vars, val = _coef)],
            rhs=[0.0],
            senses="L")



# Restrições 5=>X(i,t) , I(i,t) ≥ 0 i = 1, ..., n, t = l, ..., T

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
print("\t \t \t Problema de Dimensionamento de Lotes com Preservação da Preparação-- Arenales, pág 231")
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
        int(model.solution.get_values("X_{0}_{1}".format(i,j))) for j in range(m)for i in range(n)
    ]
]
producao = np.array(producao)
print(producao.reshape(len(dit),len(dit[0]))) #exibir o valor da sequencia ótima na tela
print("\n")


#Obtem o valor de I:
print("Os valores de I(i,t) são:  ")

estoque = np.zeros((n,m))

estoque= [
    [
       int(model.solution.get_values("I_{0}_{1}".format(i,j))) for j in range(m)for i in range(n)
    ]
]
estoque = np.array(estoque)
print(estoque.reshape(len(dit),len(dit[0]))) #exibir o valor da sequencia ótima na tela

print("\n")

#Obtem o valor de Y:
print("Os valores de Y(i,t) são:  ")

setup = np.zeros((n,m))

#truque para trabalhar com variáveis binárias
'''
setup = [
    [
        sum(j * int(model.solution.get_values("Y_{0}_{1}".format(i,j))) for j in range(n))
        for i in range(n)
    ]
]
'''
setup= [
    [
       int(model.solution.get_values("Y_{0}_{1}".format(i,j))) for j in range(m)
       for i in range(n)
    ]
]


setup= np.array(setup)
print(setup.reshape(len(dit),len(dit[0]))) #exibir o valor da sequencia ótima na tela



print("\n")
print("Valor da Função Objetivo: ", model.solution.get_objective_value(), "\n") #exibir o valor da FO na tela