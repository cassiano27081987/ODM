import sys
print(sys.executable)

#from __future__ import print_function
# !/usr/bin/python3.7
# -*- coding: utf-8 -*-
#from __future__ import print_function

import numpy as np
from random import randrange, uniform
from prettytable import PrettyTable
from mip import Model, xsum, minimize, BINARY


print("\n")
print("#---------------------Modelo SSDSC-------------------------------#\n")
print("\n")

#-----------------Modelo SSDSC----------------#

#Declaração dos conjuntos
T = 10
S = 15
P = 5

#--------------Declaração dos parâmetros--------------------------#


# Custo unitário de compra do produto p no fornecedor s e período t;
cc =[]

print("\n")
print("Custo unitário de compra do produto p no fornecedor s e período t: \n")
#função que gera os números aleatórios segundo a distribuição uniforme (numpy.random.randint(low value,hight value,size=(M,N))

cc = np.random.randint(3,7,size=(T,S,P))      

print(cc)
print("\n")


#Custo unitário de transporte de um produto, vindo do fornecedor s no período t;
ct = []

print("\n")
print("Custo unitário de transporte de um produto, vindo do fornecedor s no período t: \n")
#função que gera os números aleatórios segundo a distribuição uniforme (numpy.random.randint(low value,hight value,size=(M,N))

ct =  random_matrix = np.random.randint(500,2500,size=(T,S))


print(ct)
print("\n")


#Capacidade do fornecedor s para fornecer o produto p no período t;
c = []

print("\n")
print("Capacidade do fornecedor s para fornecer o produto p no período t \n")
#função que gera os números aleatórios segundo a distribuição uniforme (numpy.random.randint(low value,hight value,size=(M,N))


c= np.random.randint(500,2500,size=(T,S,P))

print(c)
print("\n")

#Um truque para trabalhar com variáveis binárias

alocacao = [
    [
        sum(j * int(model.solution.get_values("X_{0}_{1}".format(i,j))) for j in range(n))
        for i in range(n)
    ]
]
#função que gera os números aleatórios segundo a distribuição uniforme (numpy.random.randint(low value,hight value,size=(M,N))

d = random_matrix = np.random.randint(1000,5000,size=(T,P))


print(d)
print("\n")


#Custo unitário operacional do fornecedor s para o produto p no período t;
q = []

print("\n")
print("Custo unitário operacional do fornecedor s para o produto p no período t: \n")
#função que gera os números aleatórios segundo a distribuição uniforme (numpy.random.randint(low value,hight value,size=(M,N))

q = random_matrix = np.random.randint(3,10,size=(T,S,P))


print(q)
print("\n")


#Custo unitário de atraso do fornecedor s para o produto p no período t;
l = []

print("\n")
print("Custo unitário de atraso do fornecedor s para o produto p no período t: \n")
#função que gera os números aleatórios segundo a distribuição uniforme (numpy.random.randint(low value,hight value,size=(M,N))

l = random_matrix = np.random.randint(3,10,size=(T,S,P))

print("\n")
print(l)
print("\n")


#Tempo estimado de atraso de entrega do fornecedor s para o produto p no período t;
dl = []

print("\n")
print("Tempo estimado de atraso de entrega do fornecedor s para o produto p no período t: \n")
#função que gera os números aleatórios segundo a distribuição uniforme (numpy.random.randint(low value,hight value,size=(M,N))

dl = random_matrix = np.random.randint(0,4,size=(T,S,P))
     
print("\n")
print(dl)
print("\n")


#custo unitário de manter em estoque o produto p no período t;
hpositive = []

print("\n")
print("custo unitário de manter em estoque o produto p no período t: \n")
#função que gera os números aleatórios segundo a distribuição uniforme (numpy.random.randint(low value,hight value,size=(M,N))

hpositive = random_matrix = np.random.randint(3.3,7.7,size=(T,P))

print(hpositive)
print("\n")



#custo unitário para atrasar a entrega do produto p no período t;
hnegative = 3*hpositive


#disponibilidade
w = [[3000 for p in range (P)] for t in range(T)]



#big M
M = 500

#Nível de serviço exigido pela organização
teta = 0.95

sigma = 0.90

#--------------Fim da Declaração dos parâmetros--------------------------#




# Criacao do modelo
model = Model("SSDSC")

# Criacao das variaveis
X = [[[model.add_var() for p in range(P)]for s in range(S)]for t in range(T)]
Y = [[model.add_var() for s in range(S)]for t in range(T)]
Ipositive = [[model.add_var() for p in range(P)]for t in range(T)]
Inegative = [[model.add_var() for p in range(P)]for t in range(T)]

# Funcao objetivo

obj1 = xsum(cc[t][s][p]*X[t][s][p] for p in range(P)for s in range(S)for t in range (T)) #primeiro termo da fo
obj2 = xsum(ct[t][s]*Y[t][s]for s in range(S)for t in range (T)) #segundo termo da fo
obj3 = (1-teta) * xsum(q[t][s][p]*X[t][s][p] for p in range(P)for s in range(S)for t in range (T)) #tereceiro termo da fo
obj4 =  xsum(l[t][s][p]*dl[t][s][p]*X[t][s][p] for p in range(P)for s in range(S)for t in range (T)) #quarto termo da fo
obj5 = xsum(hpositive[t][p]*Ipositive[t][p]for p in range(P)for t in range (T)) #quinto termo da fo
obj6 = xsum(hnegative[t][p]*Inegative[t][p]for p in range(P)for t in range (T)) #sexto termo da fo

obj = obj1 + obj2 + obj3 + obj4 + obj5 + obj6
model.objective = minimize(obj)


# Restrições 1 => X(i,t) + I(i,t-1) − I(i,t) = d(i,t) i = t = 1,....,T; s=1, ...., S; p=1,....,P

for t in range(T):
    for p in range(P):
        
        if t<1:
            expr = xsum(X[t][s][p] for s in range(S)) -Ipositive[t][p] + Inegative[t][p]
            model += (expr == d[t][p])
        else:
            expr = xsum(X[t][s][p] for s in range(S)) -Ipositive[t][p] +Ipositive[t-1][p]+ Inegative[t][p] - Inegative[t-1][p]
            model += (expr == d[t][p])


# Restrições 2 =>X(t,s,p) <= Cap(t,s,p) t = 1,....,T; s=1, ...., S; p=1,....,P

for p in range(P):
    for t in range(T):
            for s in range(S):
                    expr = X[t][s][p]
                    model += (expr <= c[t][s][p])


# Restrições 3 =>sum(p, X(t,s,p) ≤ M* Y(t,s) t = l, ..., T; s=1,...,S

for s in range(S):
    for t in range(T):
        expr = xsum(X[t][s][p] for p in range(p)) - (M* Y[t][s])
        model += (expr<= 0)



# Restrições 4 =>Ipositive(t,p) <= w(t,p) t = 1,....,T;  p=1,....,P

for p in range(P):
    for t in range(T):
        expr = Ipositive[t][p]
        model += (expr<= w[t][p])



# Restrições 5 =>Inegative(t,p) <= sigma* d(t,p) t = 1,....,T;  p=1,....,P

for p in range(P):
    for t in range(T):
        expr = Inegative[t][p]
        model += (expr <= sigma*d[t][p])


# Restrições 6 =>X(t,s,p) ≥ 0 t = 1,....,T; s=1, ...., S; p=1,....,P

for p in range(P):
    for s in range(S):
        for t in range(T):
            expr = X[t][s][p]
            model += (expr >= 0.0)


# Restrições 7 =>Ipositive(t,p) >= 0 t = 1,....,T;  p=1,....,P

for p in range(P):
    for t in range(T):
        expr = Ipositive[t][p]
        model += (expr >= 0.0)


# Restrições 8 =>Inegative(t,p) >= 0 t = 1,....,T;  p=1,....,P

for p in range(P):
    for t in range(T):
        expr = Inegative[t][p]
        model += (expr >= 0.0)


# Resolvendo modelo
model.optimize()
print("\n")
print("\n")
print("--------------Modelo SSDSC-----------------------")

print("\n")

print("O valor da função objetivo é:  {}".format(model.objective_value))
print("\n")


