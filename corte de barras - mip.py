
import sys
print(sys.executable)

#from __future__ import print_function
# !/usr/bin/python3.7
# -*- coding: utf-8 -*-
#from __future__ import print_function

import numpy as np
from prettytable import PrettyTable
from mip import Model, xsum, minimize, BINARY, INTEGER


'''
Dados PICCIN

d(i) 'demanda do item i'
/
30150000004 3
30150000005 2
30150000006 0
30150000008 3
30150000011 0
30150000014 0
30150000017 0
30150000036 44
30150000037 18
30150000038 16
30150000041 0
30150000046 0
30150000047 0
30150000050 0
30150000054 0
30150000055 0
/

le(i) 'comprimento desejado do item i'
/
30150000004 142
30150000005 1340
30150000006 2210
30150000008 514
30150000011 586
30150000014 1730
30150000017 2575
30150000036 800
30150000037 1420
30150000038 2535
30150000041 850
30150000046 1535
30150000047 150
30150000050 3445
30150000054 805
30150000055 690
/


desenho(i) 'código do desenho'
/
30150000004 PRL00660
30150000005 PRT00025
30150000006 PRT00026
30150000008 PRT00029
30150000011 PRT00035
30150000014 PRT00044
30150000017 PRT00054
30150000036 PRT00097
30150000037 PRT00098
30150000038 PRT00100
30150000041 PRT00106
30150000046 PRT00116
30150000047 PRT00118
30150000050 PRT00121
30150000054 PRT00129
30150000055 PRT00131


'''




#--------------------Problema de Corte de Barras----------------------------------#

#Modelo 02 - Dissetação Alexander Abuarara - Ufscar

#--------------Declaração dos parâmetros--------------------------#

#comprimento da barra j
b = []

for j in range(20):
    b.append(6000)


#comprimento do item i
l =[142,1340,2210,514,586,1730,2575,800,1420,2535,850,1535,150,3445,805,690]

#demanda dos itens i
d =[3,2,0,3,0,0,0,44,18,16,0,0,0,0,0,0]

#número máximo de barras j
M = max(b) - min(l)
print("O valor de M é: ", M)

#comprimento mínimo do item i para ser considerado como retalho
N = min(l)

print("O valor de N é: ", N)

#retalho
R = int(max(b)/min(l))

print("O valor de R é: ", R)

#--------------Fim da Declaração dos parâmetros--------------------------#


#Declaração dos conjuntos
J = len(b) #barras em estoque
I = len(d) #tipo dos itens



# Criacao do modelo
model = Model("Abuamara e Morabito")

# Criacao das variaveis
X = [[model.add_var(var_type=INTEGER) for j in range(J)]for i in range(I)] #Variável x(i,j) qtd de itens i produzidos na barra t t
T = [model.add_var() for j in range(J)] #Variável que define a perda por objeto j,isto é,uma sobra δj talque δj<N estocados no período t
U = [model.add_var(var_type=BINARY) for j in range(J)] #Variável que indica se a sobra no objeto j é maior ou igual a N,i.e,uj=1
Z = [model.add_var(var_type=BINARY) for j in range(J)] #Variável que indica se o objeto j está sendo utiliza do no plano de corte,i.e,zj=1
W = [model.add_var(var_type=BINARY) for j in range(J)] #Variável que indica se a sobra em j é menor do que o valor N,i.e,wj=1



# Funcao objetivo

#função objetivo min z = min FO = F1.(∑j,tj) + F2.(∑j,bj.zj/B) - ok

obj1= xsum(T[j] for j in range(J))
obj2= xsum(Z[j] for j in range(J))
obj = (obj1 + obj2)/N
model.objective = minimize(obj)


# Restrições 1= sum(j, X_ij) = d_i - ok

for i in range(I):
    expr = xsum(X[i][j] for j in range(J))
    model+= (expr >= d[i])

#Restrições 02 => N.u_j ≤ b_j.z_j− ∑i,(li.xij)  ∀j   - ok

for j in range(J):
    expr = N*U[j] - b[j]*Z[j] + xsum(l[i]*X[i][j] for i in range(I))
    model += (expr <=0.0)

#Restrições 03 => b_j.z_j−  ∑i, (li.xij) ≤ t_j+ M.u_j ∀j -ok

for j in range(J):
    expr = b[j]*Z[j]  - xsum(l[i]*X[i][j] for i in range(I)) - T[j] - M*U[j]
    model += (expr <=0.0)


#Restrições 05 =>  ∑j, (u_j) ≤ R - ok

for i in range(I):
    expr = xsum(U[j]for j in range(J))
    model += (expr<= R)


#Restrição 06 => sobra(barra) =e= b(barra) - sum(i, x(i,barra)*(le(i)+2));

for j in range(J):
    expr = T[j] + xsum(X[i][j]*l[i] for i in range(I))
    model += (expr == b[j])


model.max_gap = 0.05
status = model.optimize(max_seconds=300)

'''
if status == OptimizationStatus.OPTIMAL:
    print('optimal solution cost {} found'.format(model.objective_value))
elif status == OptimizationStatus.FEASIBLE:
    print('sol.cost {} found, best possible: {}'.format(model.objective_value, model.objective_bound))
elif status == OptimizationStatus.NO_SOLUTION_FOUND:
    print('no feasible solution found, lower bound is: {}'.format(model.objective_bound))
if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
    print('solution:')
    for v in model.vars:
       if abs(v.x) > 1e-6: # only printing non-zeros
          print('{} : {}'.format(v.name, v.x))

'''

# Resolvendo modelo
model.optimize()


print("\n")
print("\n")
print("---------Exemplo de Corte de Barras - Dissetação Alexander Abuarara - Ufscar ----------------")

print("\n")


print("\n")

print("O valor da função objetivo é:  {}".format(model.objective_value))
print("\n")


# Salvando solucao de X
sol_X_i_t = []
for i in range(I):
    for j in range(J):
	    sol_X_i_t.append(X[i][j].x)

#Obtem o valor de X:
sol_X_i_t = np.full((I, J), 0.0)
for i in range(I):
	for j in range(J):
		sol_X_i_t[i][j] = X[i][j].x

print("Os valores de X(i,j) são: ")


for i in range(len(d)):
    print (i+1, end="\t")
print()
for i in range(len(d)):
    print(i+1, end="\t")
    for j in range(len(b)):
        print(sol_X_i_t[i][j], end="\t")
    print()
print()