
'''Model DFJ definition   DFJ = Dantzig, Fulkerson and Jhonson

Consider a complete graph G = (V,A) where V = {v1, v2,......vn} is the vertex 
set and A = {vi,vj}: vi,vj belongs to V, i!=j} Is the arc set. Let C = (c(i,j))
be the matrix of positive costs, distances or travel times associated with A. 
If we asssociates on a binary variable x(i,j) to every directed arv (vi,vj) where
equal to 1 if only the arc(vi,vj) is used in the solution.
The Miller, Tucker and Zemlin (MTZ) formulation, reduces the number of subtour
elimination constraints at the expense free variables u(i) = (i=2,....,n).

The Dantzig model is defined by:


min z = sum(i,j (c(i,j)*x(i,j))) (i!=j)


sa

sum (j, x(i,j)) =E= 1 (1<=i<=n, j!=i)
sum (i, x(i,j)) =E= 1 (1<=j<=n, i!=j)
sum ((i,j), x(i,j)) =L= |S|-1 (1<=i<=n,1<=j<=n, i!=j)

'''


import sys
print(sys.executable)
# !/usr/bin/python3.7
# -*- coding: utf-8 -*-
import cplex
import numpy as np
from prettytable import PrettyTable

'''
i =  17 #número de cidades
j =  17#número de cidades

cost = []



# split() method returns a list of strings after breaking the given string by the specified separator.
# separator : The is a delimiter. The string splits at this specified separator. If is not provided then any white space is a separator.


file = open("/home/cassiano/Área de Trabalho/Tópicos Avançados em Gerência da Produção/2020/br17.txt","r")
file.seek(0, 0)
for j in range(0,16):
    linha = []  # cria as linhas vazias da matriz
    content = file.readline()  # reading the next line from the file
    line = content.split()  # split the content
    for i in range(0,16):
        linha.append(int(line[i]))  # adds integers to the lines
    cost.append(linha)  # accreates lines filled to the matrix

file.close()

c = [i, j]  # empty array to receive the distances betwen the cities
c = cost

print("\n Os dados são: \n")
print(c)
                
print("\n")
'''

import sys
print(sys.executable)
# !/usr/bin/python3.7
# -*- coding: utf-8 -*-
import cplex
import numpy as np
from prettytable import PrettyTable

i =  17 #número de cidades
j =  17#número de cidades

cost = []

c = [i, j]  # empty array to receive the distances betwen the cities

n =  17 #número de nós

# split() method returns a list of strings after breaking the given string by the specified separator.
# separator : The is a delimiter. The string splits at this specified separator. If is not provided then any white space is a separator.


file = open("br17.txt","r")
file.seek(0, 0)
for j in range(n):
    linha = []  # cria as linhas vazias da matriz
    content = file.readline()  # reading the next line from the file
    line = content.split()  # split the content
    for i in range(n):
        linha.append(int(line[i]))  # adds integers to the lines
    cost.append(linha)  # accreates lines filled to the matrix

file.close()

c = cost

print("\n Os dados são: \n")
print(c)
                
print("\n")


#Criamos o objeto Cplex
model = cplex.Cplex()


#Definimos das variáveis do modelo
model.variables.add(names=["X_{0}_{1}".format(i, j) for i in range(n) for j in range(n)], types=['B']*n*n)


#Definimos as restrições do modelo

#função objetivo min z = sum(i,j (c(i,j)*x(i,j))) (i!=j)
_vars = ["X_{0}_{1}".format(i, j) for i in range(n)  for j in range(n)]
_coef = [c[i][j] for i in range(n) for j in range(n)]
model.objective.set_linear(zip(_vars, _coef))
model.objective.set_sense(model.objective.sense.minimize)



#primeira restrição sum (i, x(i,j)) =E= 1 (1<=i<=n, j!=i)

for j in range(n):
    _vars = ["X_{0}_{1}".format(i, j) for i in range(n) if i != j]
    _coef = [1.0] * len(_vars)
    model.linear_constraints.add(
    lin_expr=[cplex.SparsePair(ind = _vars, val = _coef)],
    rhs=[1.0],
    senses="E")

#segunda restrição sum (j, x(i,j)) =E= 1 (1<=j<=n, i!=j)

for i in range(n):
    _vars = ["X_{0}_{1}".format(i, j) for j in range(n) if i != j]
    _coef = [1.0] * len(_vars)
    model.linear_constraints.add(
    lin_expr=[cplex.SparsePair(ind = _vars, val = _coef)],
    rhs=[1.0],
    senses="E")


#Criação do Callback

class noSubtourCallBack(cplex.callbacks.LazyConstraintCallback):
    def getProxNo(self, i):
        ret = sum([j * int(0.5+self.get_values("X_{0}_{1}".format(i, j))) for j in range(self.n)])
        return(ret)

    def criaS(self):
        S = [0]
        i = self.getProxNo(0)
        while i != 0:
            S.append(i)
            i = self.getProxNo(S[-1])

        SN = [i for i in range(self.n) if i not in S]
        return S, SN

    def __call__(self):
        S, NS = self.criaS()
        if len(S) >= 2 and len(S) <= self.n-2:
            print("Eliminado subtour ", S)
            print("(NS = ",NS, ")")
            _var = ["X_{0}_{1}".format(i,j) for i in S for j in NS]
            _coef = [1] * len(_var)
            self.add(cplex.SparsePair(ind = _var, val = _coef), rhs=1.0, sense="G")

            _var = ["X_{0}_{1}".format(i,j) for i in S for j in S]
            _coef = [1.0] * len(_var)
            self.add(cplex.SparsePair(ind = _var, val = _coef), rhs=len(S)-1, sense="L")
            
#Ligando o Callback no modelo

tspCallBack = model.register_callback(noSubtourCallBack)
tspCallBack.n = n



model.solve() #resolve o modelo


#Configurações do CPLEX:

model.parameters.timelimit.set(300)#Limite de tempo de execucao


model.parameters.mip.tolerances.mipgap.set(0.0)#Forca parada apenas com gap 0.0


model.parameters.mip.display.set(0)#Elimina a saida padrao do CPLEX

#Obtendo o tempo necessário para executar o modelo:
initiTime = model.get_time()
model.solve()
finalTime = model.get_time()


#Obtendo o status e valor de resolução:

print(str(model.solution.get_status()))
print(str(round(model.solution.get_objective_value(),0)))

#Obtem o valor de x:
print("A sequencia ótima é:  ")
print(model.solution.get_values("X_{0}_{1}". format(i,j)))
print("\n")

print("Objective value: ", model.solution.get_objective_value(), "\n") #exibir o valor da FO na tela

#Um truque para trabalhar com variáveis binárias

alocacao = [
    [
        sum(j * int(model.solution.get_values("X_{0}_{1}".format(i,j))) for j in range(n))
        for i in range(n)
    ]
]

print("A sequencia ótima é: ", alocacao, "\n") #exibir o valor da sequencia ótima na tela


