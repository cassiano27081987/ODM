
import sys
print(sys.executable)

#from __future__ import print_function
# !/usr/bin/python3.7
# -*- coding: utf-8 -*-
#from __future__ import print_function

import numpy as np
from prettytable import PrettyTable
import cplex


#--------------------Problema de Corte de Barras----------------------------------#

#Modelo 02 - Dissetação Alexander Abuarara - Ufscar

#--------------Declaração dos parâmetros--------------------------#

#comprimento da barra j
bj = [10.280, 10.220, 10.160, 10.180, 10.100]

#comprimento do item i
li =[239,188, 134]

#demanda dos itens i
di =[140, 55,25]

#número máximo de barras j
M = max(bj) - min(li)

#comprimento mínimo do item i para ser considerado como retalho
N = min(li)

#retalho
R = int(max(bj)/min(li))

#--------------Fim da Declaração dos parâmetros--------------------------#

#Declaração dos conjuntos
m = len(bj) #barras em estoque
n = len(di) #tipo dos itens

print("o valor de n é: ", n)
print("o valor de m é: ", m)

print("\n")

#Criamos o objeto Cplex
model = cplex.Cplex()
                    
                    
#Declaração de variáveis:
#nome_do_modelo.variables.add(names =, lower bound - lb = [], types - continuous 'C' , Binary 'B',  integer 'I').
#Ex: Definir nome da variável (Índice) _varname = ["C_"+str(i)+"_"+str(j)]
#Adicionar ao modelo: model.variables.add(names = _varname, lb = [0], types = ['C'])

#Definimos das variáveis do modelo
model.variables.add(names=["X_{0}_{1}".format(i,j) #Variável x(i,j) qtd de itens i produzidos na barra t t
                            for i in range(n)
                            for j in range(m)],
                    types=['I']*n*m)

model.variables.add(names=["T_{0}".format(j) #Variável que define a perda por objeto j,isto é,uma sobra δj talque δj<N estocados no período t
                            for j in range(m)],
                    types=['C']*m)

model.variables.add(names=["U_{0}".format(j) #Variável que indica se a sobra no objeto j é maior ou igual a N,i.e,uj=1
                            for j in range(m)],
                    types=['B']*m)

model.variables.add(names=["Z_{0}".format(j) #Variável que indica se o objeto j está sendo utiliza do no plano de corte,i.e,zj=1
                            for j in range(m)],
                    types=['B']*m)

model.variables.add(names=["W_{0}".format(j) #Variável que indica se a sobra em j é menor do que o valor N,i.e,wj=1
                            for j in range(m)],
                    types=['B']*m)


model.variables.add(names=["FO1_{0}".format(j) #Variável que armazena o valor do primeiro termo da função objetivo
                            for j in range(m)],
                    types=['C']*m)

model.variables.add(names=["FO2_{0}".format(j) #Variável que armazena o valor do primeiro termo da função objetivo
                            for j in range(m)],
                    types=['C']*m)

#Definimos as restrições do modelo

#model.linear_constraints.add adiciona restrições (lin_expr = [], rhs = []. senses = '')
#senses = Equal 'E', 'G' Greater than, 'L' less than, 'R' ranged constraints
#lin_expr = [] é uma lista de lista que guarda os valores de sparsepair (lista de índice e respectivos valores do indice que estão também em lista)
#cpex.sparsePair(índice ind = colocar aqui os índices, value val - Respectivos valores dos índices)
#rhs = valor depois do sinal (igual, maior ou igual, menor ou igua etc)

#função objetivo min z = min FO = F1.n(∑j,tj) + F2.n(∑j,bj.zj/B)

#valor do primeiro termo da FO
for j in range(m):
    _vars = ["T_{0}".format(j),"FO1_{0}".format(j) ]
    _coef = [1.0*len(_vars)]  + [-1.0]
    model.linear_constraints.add(
    lin_expr=[cplex.SparsePair(ind = _vars, val = _coef)],
    rhs=[0.0],
    senses="E")    
    
#valor do segundo termo da FO
for j in range(m):
    _vars = ["Z_{0}".format(j),"FO2_{0}".format(j) ]
    _coef = [bj[j]]  + [-1.0]
    model.linear_constraints.add(
    lin_expr=[cplex.SparsePair(ind = _vars, val = _coef)],
    rhs=[0.0],
    senses="E")  


for j in range(m):
    _vars = ["FO1_{0}".format(j),"FO2_{0}".format(j)]
    _coef = [1.0*len(_vars)]  + [1.0*len(_vars)]
    model.objective.set_linear(zip(_vars, _coef))
    model.objective.set_sense(model.objective.sense.minimize) 

# Restrições 1= sum(j, X_ij) = d_i

for i in range(n):
    _vars = ["X_{0}_{1}".format(i,j) for j in range(m)]
    _coef = [1.0]*len(_vars)
    model.linear_constraints.add(
    lin_expr=[cplex.SparsePair(ind = _vars, val = _coef)],
    rhs=[di[i]],
    senses="E")

#Restrições 02 => N.u_j ≤ b_j.z_j−m.∑i,(li.xij)  ∀j  
for j in range(m):
    _vars =["U_{0}".format(j),"Z_{0}".format(j),"X_{0}_{1}".format(i,j)]
    _coef = [1*0*N] + [-1.0*bj[j]]+[li[i]*len(_vars)]
    model.linear_constraints.add(lin_expr = 
    [cplex.SparsePair(ind = _vars, val = _coef)],
    rhs = [0.0],
    senses="L")
    

#Restrições 03 => b_j.z_j− m. ∑i, (li.xij) ≤ t_j+ M.u_j ∀j

for j in range(m):
    _vars =["Z_{0}".format(j),"X_{0}_{1}".format(i,j),"T_{0}".format(j),"U_{0}".format(j)]
    _coef = [bj[j]]+[-li[i]*len(_vars)] + [-1.0] + [-M]
    model.linear_constraints.add(lin_expr = 
    [cplex.SparsePair(ind = _vars, val = _coef)],
    rhs = [0.0],
    senses="L")
    
    
#Restrições 04 =>  ∑j, (u_j) ≤ 1

for j in range(m):
    _vars =["U_{0}".format(j)]
    _coef = [1.0*len(_vars)] 
    model.linear_constraints.add(lin_expr = 
    [cplex.SparsePair(ind = _vars, val = _coef)],
    rhs = [1.0],
    senses="L")
    
  
#Restrições 05 =>  ∑j, (u_j) ≤ R

for i in range(n):
    _vars =["U_{0}".format(j)]
    _coef = [1.0*len(_vars)] 
    model.linear_constraints.add(lin_expr = 
    [cplex.SparsePair(ind = _vars, val = _coef)],
    rhs = [R],
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
print("\t \t \t Problema de Corte de Barras")
print("\n")


'''
#Obtendo o status e valor de resolução:

print(str(model.solution.get_status()))
print(str(round(model.solution.get_objective_value(),0)))

'''
#Obtem o valor de X:
print("Os valores de X(j) são:  ")

producao = np.zeros((n,m))
producao = [
    [
        int(model.solution.get_values("X_{0}_{1}".format(i,j))) 
        for i in range(n) for j in range(m)
    ]
]
producao = np.array(producao)
print(producao.reshape(len(di),len(bj)))#exibir o valor da sequencia ótima na tela
print("\n")


print("Valor da Função Objetivo: ", model.solution.get_objective_value(), "\n") #exibir o valor da FO na tela
