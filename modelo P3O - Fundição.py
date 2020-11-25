import sys
print(sys.executable)

#from __future__ import print_function
# !/usr/bin/python3.7
# -*- coding: utf-8 -*-
#from __future__ import print_function

import numpy as np
from random import randrange, uniform
from prettytable import PrettyTable
from mip import Model, xsum, minimize, BINARY, INTEGER


print("\n")
print("#---------------------Modelo P3O------------------------------#\n")
print("\n")



#RAIRO-Oper. Res. 53 (2019) 1551–1561
#https://doi.org/10.1051/ro/2019084


#-----------------P3O------------------------------------------------------#


#--------------Declaração dos conjuntos--------------------------#

K = 2 #tipos de ligas
I = 10 #ordens de produção
J = 10 #tipo de itens
T = 5 # número de períodos
ETA =T*8 #número de subperíodos {1,...,Lt}




#--------------Declaração dos parâmetros--------------------------#
'''
#Numero de subperíodos no horzionte t, ou seja, quantas vezes o forno é carregado no período t

NS = np.zeros((T))

#Primeiro subperído no horizonte t (F1 = 1)
F = []
for t in range (0,1):
    F[t] = 1 + xsum(NS[t] for t in range (T))

#Último subperíodo no horizonte t
L = []

for t in range(T-1,T):
    L[t] = xsum(NS[t] for t in range (T))
'''
#penalidade de atrasar uma ordem de produção i, no período t

#bo = np.zeros((I,T))

bo = np.random.randint(-10,10, size = (I,T))

#penalidade de entregas extras da ordem de produção i, no período t

#pe = np.zeros((I,T))

pe = np.random.randint(-10,10, size = (I,T))


#benefício de entregar o item j, da ordem de produção i antecipadamente no período t (antes da data de entrega)

#r = np.zeros((J,I,T))

r = np.random.randint(6,10, size = (J,I,T))

#benefício em carregar estoque do item j para o subperíodo final do horizonte de planejamento (período T)

h = np.random.randint(6,10, size = (J))

#paramêtro adicional = 1 se a data de entrega da ordem de produção i está no período t, 0 caso contrário

d = np.random.randint(10,60, size=(I,T))

# peso bruto do item j

#p = np.zeros((J))

p = np.random.randint(1,30, size = (J))

# capacidade de processamnto do forno (kg)

cap = 0.6

# número máximo de entregas extras da ordem i

me = np.ones((I))

#quantidade de itens j na demanda da ordem i

#a = np.zeros((J,I))

a = np.random.randint(10,60, size = (J,I))

#--------------Fim da Declaração dos parâmetros--------------------------#




# Criacao do modelo
model = Model("P3O")

# Criacao das variaveis
BO = [[model.add_var(var_type = BINARY) for t in range(T)]for i in range(I)] # asume 1 se o item j é entregue no período t, 0 caso contrário
E = [[model.add_var(var_type = BINARY) for t in range(T)]for j in range(J)]# asume 1 se há entregas extras do item j, no período t, 0 caso contrário
Tal= [[[model.add_var() for t in range(T)]for i in range(I)]for j in range(J)] # variável adicional que indica a quantidade do item j na ordem i, entregue no período t, em uma entrega extra
Estoque= [[model.add_var() for t in range(T)]for j in range(J)] #Quantidade de itens j estocados no período t
XO = [[model.add_var(var_type = BINARY) for t in range(T)]for i in range(I)] # asume 1 se a op é finalizada no período t, 0 caso contrário
X = [[model.add_var(var_type = BINARY) for eta in range(ETA)]for j in range(J)]# quantidade do item j produzido no subperíodo de t
Y = [model.add_var(var_type = BINARY) for eta in range(ETA)] # asume 1 se o forno é utilizado para a produção da liga k no subperíodo de t, 0 caso contrário
W = [[[model.add_var() for t in range(T)]for i in range(I)]for j in range(J)] # quantidade total de itens j da ordem de produção i, entregues no período t


# Funcao objetivo

obj1 = xsum(bo[i][t]*BO[i][t] for i in range(I) for t in range(T)) #primeiro termo da função objetivo
obj2 = xsum(pe[i][t]*E[i][t]for i in range(I)for t in range(T)) #segundo termo da função objetivo
obj3 = xsum(r[j][i][t]* Tal[j][i][t] for j in range(J) for i in range (I) for t in range (T)) # terceiro termo da função objetivo
obj4 = xsum(h[j]*Estoque[j][T-1] for j in range (J)) #quarto termo da função objetivo


obj = obj1 + obj2 + obj3 + obj4 
model.objective = minimize(obj)



#primeira restrição: XO(i,t) + BO(i,t) = d(i,t) + BO(i,t-1), i=1,....,I; t=1,....,T

for i in range(I):
    for t in range(T):
        if t < 1:
            expr = XO[i][t] + BO[i][t]
            model += (expr == d[i][t])
        else:
            expr = XO[i][t] + BO[i][t] + BO[i][t-1]
            model += (expr == d[i][t])

#segunda restrição: I(j, t-1) + sum(tal, X[j][tal]) = I(j,t) + sum(i, W(j,i,t)), j=1,....,N; t=1,....,T

for j in range(J):
    for t in range(T):
        if t<1:
            expr = xsum(X[j][eta] for eta in range(ETA)) - Estoque[j][t] + xsum(W[j][i][t] for i in range(I))
            model += (expr == 0.0)
        else:
            expr = Estoque[j][t-1] + xsum(X[j][eta] for eta in range(ETA)) - Estoque[j][t] + xsum(W[j][i][t] for i in range(I))    
            model += (expr == 0.0)

#terceira restrição: sum(k, Y(eta)) <=1, η ∈ L
'''
for eta in range(ETA):
    expr = xsum(Y[ETA] for k in range(K))
    model += (expr <= 1.0)
'''
#quarta restrição: sum(j, p(j)*X(j, eta)) <= cap* Y(eta); η ∈ L ; k=1,....,K

for eta in range(ETA):
    for k in range(K):
        expr = xsum(p[j]*X[j][eta] for j in range(J)) - cap* Y[eta]
        model += (expr <= 0.0)

#quinta restrição: sum(eta, X(j,eta)) <= sum(i, a(j,i)); j=1,.....,J
aux = []
for i in range(I):
    aux.append(a[j][i]+ a[j][i-1])
for j in range(J):
    expr = xsum(X[j][eta] for eta in range(ETA)) 
    model += (expr <= aux[i])

#sexta restrição:

for j in range(J):
    for i in range(I):
        for t in range(T):
            expr = W[j][i][t] - a[j][i] *(XO[i][t]+ E[i][t])
            model += (expr <= 0.0)

#sétima restrição

for j in range(J):
    for i in range(I):
        expr = xsum(W[j][i][t] for t in range(T))
        model += (expr <= a[j][i]) 

#oitava restrição

for i in range(I):
    for t in range(T):
        expr = XO[i][t] + E[i][t]
        model += (expr<= 1.0)

#nona restrição
aux2 = []
for i in range(I):
    for j in range(J):
        expr = xsum(W[j][i][t] for t in range(T))   - a[j][i] *(XO[i][t]) 
        model += (expr>= 0.0)



#décima restrição

for i in range(I):
    expr = xsum(E[i][t]for t in range(T))
    model += (expr<=me[i])

#décima primeira restrição - primeira parte

for j in range(J):
    for i in range(I):
        for t in range(T):
            expr = Tal[j][i][t] - W[j][i][t]
            model +=(expr <= 0.0)

#décima primeira restrição - segunda parte

for j in range(J):
    for i in range(I):
        for t in range(T):
            expr = Tal[j][i][t] + (a[j][i] * XO[i][t])
            model +=(expr <= a[j][i])


#Parametros de resolução
model.max_gap = 0.05
status = model.optimize(max_seconds=300)

# Resolvendo modelo
model.optimize()


print("O valor da função objetivo é:  {}".format(model.objective_value))
print("\n")

