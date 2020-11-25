import sys
print(sys.executable)

#from __future__ import print_function
# !/usr/bin/python3.7
# -*- coding: utf-8 -*-
#from __future__ import print_function

import numpy as np
from prettytable import PrettyTable
from mip import Model, xsum, minimize, BINARY


#-----------------Problema de Dimensionamento de Lotes Estático----------------#

#Exemplo Arenales MSPP, pág 209


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
rij = [[3,6,9],
       [3,6,9],
       [3,6,9]
       ]
       

#--------------Fim da Declaração dos parâmetros--------------------------#


#Declaração dos conjuntos
m = len(dit[0])
n = len(dit)

t = len(dit[0])
i = len(dit)
print(i,t,n,m)


# Criacao do modelo
model = Model("MSPP")

# Criacao das variaveis
Xit = [[model.add_var() for t in range(m)]for i in range(n)]
Iit = [[model.add_var() for t in range(m)]for i in range(n)]
Yit = [[model.add_var(var_type=BINARY) for t in range(m)]for i in range(n)]


# Funcao objetivo

obj1 = xsum(sit[i][t]*Yit[i][t] for i in range(n)for t in range(m)) #primeiro termo da fo
obj2 = xsum(hit[i][t]*Iit[i][t] for i in range(n)for t in range(m))#segundo termo da fo
obj = obj1 + obj2
model.objective = minimize(obj)


# Restrições 1 => X(i,t) + I(i,t-1) − I(i,t) = d(i,t) i = 1, ..., n, t = l, ..., T

for i in range(n):
    for t in range(m):
        
        if t<1:
            expr = Xit[i][t]  - Iit[i][t]
            model += (expr == dit[i][t])
        else:
            expr = Xit[i][t] + Iit[i][t-1] - Iit[i][t] 
            model += (expr == dit[i][t])

# Restrições 2 =>sum(i, X(i,t)*r(i)) ≤ R(t) t = l, ..., T

for t in range(m):
    expr = xsum(bi[i] * Xit[i][t]  for i in range(n)) 
    model += (expr <= ct[t])

# Restrições 3 =>X(i,t)<= M(i,t)*Y(i,t)

#Parametro adicional para limitar a capacidade
print("\n")

demanda_acumulada = list(map(sum,dit)) 
demanda_acumulada.insert(3,24)

print("A demanda acumulada é: ", demanda_acumulada)
print("\n")

for i in range (n):
    for t in range(m):
        expr = Xit[i][t] + (-1*(Yit[i][t] * demanda_acumulada[t]))
        model += (expr <= 0)

# Restrições 4 =>X(i,t) , I(i,t) ≥ 0 i = 1, ..., n, t = l, ..., T

for i in range(n):
    for t in range(1,m):
        expr = Xit[i][t] 
        model += (expr >= 0.0)

for i in range(n):
    for t in range(m):
        expr = Iit[i][t] 
        model += (expr >= 0.0)



# Resolvendo modelo
model.optimize()
print("\n")
print("\n")
print("--------------Exemplo de Dimensionamento de Lotes MSPP------------------------")

print("\n")

print("O valor da função objetivo é:  {}".format(model.objective_value))
print("\n")

# Salvando solucao de X
sol_X_i_t = []
for i in range(n):
    for j in range(m):
	    sol_X_i_t.append(Xit[i][t].x)

#Obtem o valor de X:
sol_X_i_t = np.full((n, m), 0.0)
for i in range(n):
	for t in range(m):
		sol_X_i_t[i][t] = Xit[i][t].x

print("Os valores de X(i,t) são: ")
print(sol_X_i_t)
print("\n")

#Salvando solucao de Y:
sol_Y_i_t = []
for i in range(n):
    for j in range(m):
	    sol_Y_i_t.append(Yit[i][t].x)

#Obtem o valor de Y:
sol_Y_i_t = np.full((n, m), 0.0)
for i in range(n):
	for t in range(m):
		sol_Y_i_t[i][t] = Yit[i][t].x

print("Os valores de Y(i,t) são: ")
print(sol_Y_i_t)
print("\n")