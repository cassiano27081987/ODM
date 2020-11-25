import sys
print(sys.executable)

#from __future__ import print_function
# !/usr/bin/python3.7
# -*- coding: utf-8 -*-
#from __future__ import print_function

import numpy as np
from random import randrange, uniform
from prettytable import PrettyTable
from mip import Model, xsum, minimize, maximize, BINARY
import pulp as p
import pandas as pd
import numpy as np
from collections import OrderedDict


mao_de_obra = [7,3,6]

quantidade_mp = [4,4,5]

lucro = [4,2,3]

I = len(mao_de_obra)

recurso = 150

mp = 200


demanda = [5,10,5]


demanda_2 = [0.75,-0.25,-0.25]

# Criacao do modelo
model = Model("SSDSC")

# Criacao das variaveis
X = [model.add_var() for i in range(I)]


# Funcao objetivo

obj = xsum(lucro[i]*X[i] for i in range(I))#primeiro termo da fo

model.objective = maximize(obj)

#primeira restrição

expr = xsum(mao_de_obra[i]*X[i] for i in range(I))
model +=(expr<=recurso)


#segunda restrição

expr = xsum(quantidade_mp[i]*X[i] for i in range(I))
model +=(expr<=mp)

#terceira restrição

for i in range(I):
    expr = X[i]
    model += (expr>=0.0)


#quarta restrição

for i in range(I):
    expr = xsum(X[i] for i in range(I))
    model += (expr<=demanda[i])


#quarta restrição

for i in range(I):
    expr = xsum(X[i]*demanda_2[i] for i in range(I))
    model += (expr>=0.0)



# Resolvendo modelo
model.optimize()
print("\n")
print("\n")
print("--------------Modelo -----------------------")

print("\n")

print("O valor da função objetivo é:  {}".format(model.objective_value))
print("\n")

# Salvando solucao de X
sol_X_i = []
for i in range(I):
	sol_X_i.append(X[i].x)

#Obtem o valor de X:
sol_X_i = np.full((I), 0.0)
for i in range(I):
	sol_X_i[i] = X[i].x

print("Os valores de X(i) são: ")


for i in range(I):
    print (i+1, end="\t")
print()
for i in range(I):
    print(i+1, end="\t")
    print(sol_X_i[i], end="\t")
    print()
print()

'''
#Solucoes otimas das variaveis
for variable in model.variables():
  print((variable.name  + "  " + str(variable.varValue)))
'''

  #Exibindo a solução final
data = OrderedDict( {
    'Quantide de KG da loção I ' : [X[0]],
    'Quantide de KG da loção C ' : [X[1]],
    'Quantide de KG da loção P ' : [X[2]]
})

format_dict =  {
    'Quantidade 1': '{:.2%}',
    'Quantidade 2': '{:.2%}',
    'Quantidade 3': '{:.2%}'
    }
df = pd.DataFrame(data)
df.style.format(format_dict).hide_index()