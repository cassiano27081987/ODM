import sys
print(sys.executable)

#from __future__ import print_function
# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
#from __future__ import print_function

import numpy as np
from prettytable import PrettyTable
from mip import Model, xsum, minimize, BINARY, INTEGER

#-----------------Problema de Roteamento de Veículos----------------#

#Exemplo Arenales PVRP, pág 197


#--------------Declaração dos parâmetros--------------------------#

#Coordendas
x = [ 50 16 23 40 9 97 78 20 71 64 50 ]
y = [ 50 32 1 65 77 71 24 26 98 55 50 ]

#demanda dos clientes
d = [ 11 35 2 9 3 18 8 10 11 ]

#janelas de tempo
a = [ 0 45 11 25 20 15 50 10 40 10 0 ]
b = [ 0 70 145 40 100 80 190 110 190 45 400]

#Capacidade dos veículos
Q = 60

D = 1000

#--------------Fim da Declaração dos parâmetros--------------------------#


#Declaração dos conjuntos
J = len(d) #
I = len(d) #
k = len(Q) #



# Criacao do modelo
model = Model("PVRP")

# Criacao das variaveis
X = [[model.add_var(var_type=BINARY) for j in range(J)]for i in range(I)] #Variável 1 se o veículo k percorre o arco ( i , j ), ∀ k ∈ K , ∀ ( i , j ) ∈ E; 0 c.c.


# Funcao objetivo

obj = xsum(c[i][j]*X[i][j] for i in range(I)for j in range(J)) #primeiro termo da fo
model.objective = minimize(obj)

for i in range(I):
    expr = xsum(X[i][j] for j in range(J))
    model += (expr = 1.0)

for k in range(K):
    expr = xsum(X[i][j] for j in range(J))
    model += (expr <= Q/ xsum(d))

for k in range(K):
    expr = xsum(X[i][j]*t[i][j]for i in range(I)for j in range(J))
    model += (expr <= D)

for k in range(K):
    for i = 0:
         expr = xsum(X[i][j] for j in range(J))
        model += (expr==1.0)

for k in range(K):
    expr = xsum(X[i][j] for i in range(I)) - xsum(X[i][j] for j in range(J))
    model += (expr ==0.0)

for k in range(K):
    for j = J+1:
        expr = xsum(X[i][j] for i in range(I))
        model += (expr ==1.0)

 