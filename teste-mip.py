'''
Uma indústria de refrigerantes produz dois tipos de bebidas, por meio de um
único tanque. Para processar 1000 litros da bebida 1 são necessárias 100 horas
do tanque, enquanto para 1000 litros da bebida 2, são necessárias 80 horas. A
disponibilidade do tanque para a fabricação destas bebidas nos próximos 3 meses
é de 240, 320 e 200 horas. O departamento de vendas fez uma previsão de
demanda para os próximos 3 meses. A demanda de cada bebida e os possı́veis
custos envolvidos são dados na tabela abaixo. Deseja-se determinar quanto
produzir e quanto estocar de cada bebida em cada perı́odo.

                            Bebida 1                Bebida 2
Perı́odo                 1       2       3       1       2       3
Demanda (L)             900     1800    1800    400     600     800
Custo prod (R$/L)       1.0    1.5      2.0     0.5     0.5     0.9
Custo estoc (R$/L)      0.5     0.25    0.0     0.25    0.25    0.0


Solução

x̄ 11 = 0
x̄ 12 = 0
x̄ 13 = 0

x̄ 21 = 0
x̄ 22 = 0
x̄ 23 = 0

I 11 = 0
I 12 = 0
I 13 = 0

I 21 = 0
I 22 = 0
I 23 = 0

FO  = 0

'''


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

#Exemplo Arenales, pág 31

#--------------Declaração dos parâmetros--------------------------#

#demanda do item i no período t, i = 1, ..., n, t = 1, ..., T
dit = [[900, 1800, 1800],
       [400, 600, 800]]


#custo de produzir uma unidade do item i no período t
cit = [[1.0,1.5,2.0],
       [0.5,0.5,0.9]]

#custo de estocar uma unidade do item i no período t
hit = [[0.5,0.25, 0.0],
       [0.25,0.25, 0.0]]


#disponibilidade de recursos (renováveis) no período t
rt = [240,320,200]

#quantidade de recursos necessários para a produção de uma unidade do item i
ri = [0.1,0.08]

#--------------Fim da Declaração dos parâmetros--------------------------#

#Declaração dos conjuntos
m = len(dit[0])
n = len(dit)

t = len(dit[0])
i = len(dit)
print(i,t,n,m)
# Criacao do modelo
model = Model("Dimensionamento de Lotes - Bebidas")

# Criacao das variaveis
X_i_t = [[model.add_var() for t in range(m)]for i in range(n)]
I_i_t = [[model.add_var() for t in range(m)]for i in range(n)]


# Funcao objetivo

obj1 = xsum(cit[i][t]*X_i_t[i][t] for i in range(n)for t in range(m)) #primeiro termo da fo
obj = obj1 + xsum(hit[i][t]*I_i_t[i][t] for i in range(n)for t in range(m))#segundo termo da fo
model.objective = minimize(obj)


#model.objective = minimize(xsum(cit[i][t]*X_i_t[i][t] + xsum(hit[i][t]*I_i_t[i][t] for i in range(n)for j in range(m))))


# Restrições 1 => X(i,t) + I(i,t-1) − I(i,t) = d(i,t) i = 1, ..., n, t = l, ..., T

for i in range(n):
    for t in range(m):
        if t<1:
            expr = X_i_t[i][t]  - I_i_t[i][t]
            model += (expr == dit[i][t])
        else:
            expr = X_i_t[i][t] + I_i_t[i][t-1] - I_i_t[i][t]
            model += (expr == dit[i][t])

# Restrições 2 =>sum(i, X(i,t)*r(i)) ≤ R(t) t = l, ..., T

for t in range(m):
    expr = xsum(ri[i] * X_i_t[i][t]  for i in range(n)) 
    model += (expr <= rt[t])

# Restrições 3 =>X(i,t) , I(i,t) ≥ 0 i = 1, ..., n, t = l, ..., T

for i in range(n):
    for t in range(1,m):
        expr = X_i_t[i][t] 
        model += (expr >= 0.0)

for i in range(n):
    for t in range(1,m):
        expr = I_i_t[i][t] 
        model += (expr >= 0.0)



# Resolvendo modelo
model.optimize()
print("\n")
print("\n")
print("--------------Exemplo de Dimensionamento de Lotes Capacitado------------------------")

print("\n")

print("O valor da função objetivo é:  {}".format(model.objective_value))
print("\n")

# Salvando solucao de X
sol_X_i_t = []
for i in range(n):
    for j in range(m):
	    sol_X_i_t.append(X_i_t[i][t].x)

#Obtem o valor de X:
sol_X_i_t = np.full((n, m), 0.0)
for i in range(n):
	for t in range(m):
		sol_X_i_t[i][t] = X_i_t[i][t].x

print("Os valores de X(i,t) são: ")
print(sol_X_i_t)
print("\n")

#Salvando solucao de Y:
sol_I_i_t = []
for i in range(n):
    for j in range(m):
	    sol_I_i_t.append(I_i_t[i][t].x)

#Obtem o valor de Y:
sol_I_i_t = np.full((n, m), 0.0)
for i in range(n):
	for t in range(m):
		sol_I_i_t[i][t] = I_i_t[i][t].x

print("Os valores de Y(i,t) são: ")
print(sol_I_i_t)
print("\n")