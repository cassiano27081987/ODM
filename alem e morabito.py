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
print("#---------------------Além e Morabito-------------------------------#\n")
print("\n")

#-----------------Além e Morabito----------------#

#Declaração dos conjuntos
I = 3
J = 6
P = 10
T = 8

#--------------Declaração dos parâmetros--------------------------#

#número suficientemente grande
Q = 100

#não sei
epsolon = 1

#v(j)'tempo necessáio para produzir o padrão de corte j'

v=[]

for j in range(J):
    v.append(18.6)


# I_max(i,t)'estoque máximo do item i no período t'

I_max = [[120,120,120,120,120,120,120,120,120],
        [250,250,250,250,250,250,250,250,250],
        [150,150,150,150,150,150,150,150,150]]



#h(i,t)'custo de estocagem da  fonte i no período j'

h =[[0,2,2,2,2,2,2,2],
    [0,2,2,2,2,2,2,2],
    [0,2,2,2,2,2,2,2]]

# c(i,t) 'custo de produção'

c = [[12,17,19,10,10,12,19,7],
     [6,15,16,11,17,11,13,7],
    [10,15,8,16,10,12,14,18]]



#d(i,t) 'demanda do item i no periodo t'

d =  [[121,192,104,138,95,56,54,75],
      [171,182,190,73,54,12,106,61],
      [146,198,118,100,199,191,116,189]]


#d = np.random.randint(30,70,size=(I,T))  


#r(p,i) 'qtd de peças p para compor o produto i'

r = [[6,0,0],
    [4,6,0],
    [2,0,7],
    [2,0,0],
    [5,4,0],
    [5,0,0],
    [1,0,5],
    [2,0,0],
    [0,2,6],
    [0,2,0]]



#delta(p,t)'custo de escolha do padrão'
delta = np.zeros((P,T))
custo = 6.5


for p in range (P):
    for t in range(T):
        delta[p][t] = custo


#sigma_1(j) 'tempo de preparação da máquina 1'

sigma_1 = []

for j in range(J):
    sigma_1.append(900)

#b(p) 'tempo de furação da peça p'

b = []
#valor original = 2.5
for p in range(P):
    b.append(3)


#sigma_2(p) 'tempo de preparação da máquina 2'

sigma_2 = []

for p in range(P):
    sigma_2.append(600)


#C_R1(t) 'capacidade regular da máquina 1'

c_r1 = 31680

#C_R2(t) 'capacidade regular da máquina 2'

c_r2 = 31680

#C_E(t) 'capacidade extra das máquinas'

c_e = 15840

#gama_d(i,t)'número de parametros que vão para o pior caso'

gama_d = 1

#o(t) Custo de horas extras no período t.

o = []

aux = np.max(c)

for t in range(T):
    o.append(2*aux)


#w(j,t) Custo de prepração do processo j no período t.

w = np.zeros((J,T))
custo_setup = 100


for j in range (J):
    for t in range(T):
        w[j][t] = custo_setup


# custo unitário de carregar atraso do item P no período t

hnegative =[[0,36,36,36,36,36,36,36],
            [0,36,36,36,36,36,36,36],
            [0,36,36,36,36,36,36,36]]

#Padrões de corte dos itens p no padrão j (j = 6; p=10)

a = [[3,0,0,0,0,0],
    [0,0,0,0,16,0],
    [0,0,0,0,0,6],
    [0,0,0,24,0,0],
    [0,8,0,0,0,0],
    [0,4,20,0,0,0],
    [0,0,0,0,0,5],
    [3,0,0,0,0,2],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0]]


#--------------Fim da Declaração dos parâmetros--------------------------#




# Criacao do modelo
model = Model("Alem e Morabito")

# Criacao das variaveis
X = [[model.add_var(var_type = INTEGER) for t in range(T)]for i in range(I)]
Y = [[model.add_var(var_type = INTEGER) for t in range(T)]for j in range(J)]
Ipositive = [[model.add_var() for t in range(T)]for i in range(I)]
Inegative = [[model.add_var() for t in range(T)]for i in range(I)]
Lambda_d = [[model.add_var() for t in range(T)]for i in range(I)]
Mi_d = [[model.add_var() for t in range(T)]for i in range(I)]
H_S = [[model.add_var() for t in range(T)]for i in range(I)]
O = [model.add_var() for t in range(T)]

Z = [[model.add_var(var_type = BINARY) for t in range(T)]for j in range(J)]

# Funcao objetivo

obj1 = xsum(c[i][t]*X[i][t] for i in range(I)for t in range(T)) #primeiro termo da fo
obj2 = xsum(h[i][t]*Ipositive[i][t]for i in range(I)for t in range (T)) #segundo termo da fo
obj3 = xsum(hnegative[i][t]*Inegative[i][t]for i in range(I)for t in range (T)) #terceiro termo da fo
obj4 = xsum(w[j][t]*Y[j][t]for j in range(J)for t in range (T)) #quarto termo da fo
obj5 = xsum(O[t]*o[t] for t in range (T))


obj = obj1 + obj2 + obj3 + obj4 + obj5
model.objective = minimize(obj)


# Restrições 1 => X(i,t) + I(i,t-1) − I(i,t) = d(i,t) i = t = 1,....,T; s=1, ...., S; p=1,....,P

for t in range(T):
    for i in range(I):
        
        if t<1:
            expr = X[i][t] -Ipositive[i][t] + Inegative[i][t]
            model += (expr == d[i][t])
        else:
            expr = X[i][t] -Ipositive[i][t] + Inegative[i][t] +Ipositive[i][t-1] - Inegative[i][t-1]
            model += (expr == d[i][t])

'''
# Restrições 2 => sum(j, a(p.j)*Y(j,t)) >= sum(i, r(p,i)*X(i,t)) p=1,...,P; t=1,...,T

for p in range(P):
    for t in range(T):
        expr = xsum(a[p][j]*Y[j][t]for j in range(J)) - xsum(r[p][i]*X[i][t]for i in range(I))
        model += (expr >= 0.0)
'''
# Restrições 3 =>sum(j, v(j)*Y(j,t)) + sum(j, sigma_1(j)*Z(j,t))<= Cap_1(t) + O(t)  t = l, ..., T

for t in range(T):
    expr = xsum(v[j]*Y[j][t] for j in range(J)) + xsum(sigma_1[j]*Z[j][t] for j in range(J)) - O[t]
    model += (expr<= c_r1)


# Restrições 4 =>sum(p, b(p)*a(p)(j)*Y(j,t)) + sum(p, sigma_2(p)*delta(p,t)*Z(j,t))<= Cap_2(t) + O(t)  t = l, ..., T

for t in range(T):
    expr = xsum(b[p]*a[p][j]*Y[j][t] for p in range(P) for j in range(J)) + xsum(sigma_2[p]*delta[p][t]*Z[j][t] for p in range(P)for j in range(J))  - O[t]
    model += (expr <= c_r2)

#Restrições 5 =>Y(j,t)<=Q*Z(j,t); j=1,...,J; t=1,...,T

for j in range(J):
    for t in range(T):
        expr = Y[j][t] - Q*Z[j][t]
        model += (expr <=0.0)


for i in range(I):
    for t in range(T):
        expr = X[i][t]
        model +=(expr >=0.0)

for i in range(I):
    for t in range(T):
        expr = Ipositive[i][t]
        model +=(expr >=0.0)

for i in range(I):
    for t in range(T):
        expr = Ipositive[i][t]
        model +=(expr <=I_max[i][t])


for i in range(I):
    for t in range(T):
        expr = Inegative[i][t]
        model +=(expr >=0.0)

for t in range(T):
    expr = O[t]
    model +=(expr>=0)

for t in range(T):
    expr = O[t]
    model +=(expr<=c_e)



#Parametros de resolução
model.max_gap = 0.05
status = model.optimize(max_seconds=300)

# Resolvendo modelo
model.optimize()


#-------------------------Imprimindo o resultado--------------------------------#

print("\n")
print("\n")
print("---------Alem e Morabito ----------------")

print("\n")


print("\n")

print("O valor da função objetivo é:  {}".format(model.objective_value))
print("\n")


# Salvando solucao de X
sol_X_i_t = []
for i in range(I):
    for t in range(T):
	    sol_X_i_t.append(X[i][t].x)

#Obtem o valor de X:
sol_X_i_t = np.full((I, T), 0.0)
for i in range(I):
	for t in range(T):
		sol_X_i_t[i][t] = X[i][t].x
        
print("Os valores de X(i,t) são: ")

for i in range(I):
    print (i+1, end="\t")
print()
for t in range(T):
    print(t+1, end="\t")
    for t in range(T):
        print(sol_X_i_t[i][t], end="\t")
    print()
print()
 

# Salvando solucao de Ipositive
sol_Ipositive_i_t = []
for i in range(I):
    for t in range(T):
	    sol_Ipositive_i_t.append(Ipositive[i][t].x)

#Obtem o valor de X:
sol_Ipositive_i_t = np.full((I, T), 0.0)
for i in range(I):
	for t in range(T):
		sol_Ipositive_i_t[i][t] = Ipositive[i][t].x

print("Os valores de Ipositive(i,t) são: ")

for i in range(I):
    print (i+1, end="\t")
print()
for t in range(T):
    print(t+1, end="\t")
    for t in range(T):
        print(sol_Ipositive_i_t[i][t], end="\t")
    print()
print()
 

# Salvando solucao de Inegative
sol_Inegative_i_t = []
for i in range(I):
    for t in range(T):
	    sol_Inegative_i_t.append(Inegative[i][t].x)

#Obtem o valor de X:
sol_Inegative_i_t = np.full((I, T), 0.0)
for i in range(I):
	for t in range(T):
		sol_Inegative_i_t[i][t] = Inegative[i][t].x

print("Os valores de Inegative(i,t) são: ")

for i in range(I):
    print (i+1, end="\t")
print()
for t in range(T):
    print(t+1, end="\t")
    for t in range(T):
        print(sol_Inegative_i_t[i][t], end="\t")
    print()
print()


 