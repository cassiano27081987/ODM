###### capacitated lot sizing problem ####
#### Solver: CPLEX ####

import sys
print(sys.executable)

#from __future__ import print_function
# !/usr/bin/python3.7
# -*- coding: utf-8 -*-
#from __future__ import print_function

import numpy as np
from prettytable import PrettyTable
import cplex


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
M = len(dit[0])
N = len(dit)

T = len(dit[0])
I = len(dit)




# DECISION VARIABLES

model = cplex.Cplex()  # Creates the object 'model' to Cplex

model.variables.add(names=["X_{0}_{1}".format(i, t)  # X_it: units of items i produced at period t
                           for i in range(N)
                           for t in range(T)],
                    types=['I'] * N * T)

model.variables.add(names=["I_{0}_{1}".format(i, t)  # I_it: units of items i holding at period t
                           for i in range(N)
                           for t in range(T)],
                    types=['C'] * N * T)

model.variables.add(names=["Y_{0}_{1}".format(i, t)  # Y_it = 1, if occurs production of item i at period t, 0 c.c
                           for i in range(N)
                           for t in range(T)],
                    types=['B'] * N * T)

#### CONSTRAINTS ####

# Constraint 1: It = It-1 + Xit - dit, 1 <= i <= N; 1 <= t <= T
for i in range(N):
    for t in range(T):
        if t < 1:
            _vars = ["X_{0}_{1}".format(i, t)] + ["I_{0}_{1}".format(i, t)]
            _coef = [1] + [-1]
            model.linear_constraints.add(
                lin_expr=[cplex.SparsePair(ind=_vars, val=_coef)],
                rhs=[dit[i][t]],
                senses="E")
        else:
            _vars = ["X_{0}_{1}".format(i, t)] + ["I_{0}_{1}".format(i, t - 1)] + ["I_{0}_{1}".format(i, t)]
            _coef = [1] + [1] + [-1]
            model.linear_constraints.add(
                lin_expr=[cplex.SparsePair(ind=_vars, val=_coef)],
                rhs=[dit[i][t]],
                senses="E")

# Constraint 2: sum_i (a_it * X_it <= Cap_t * Y_it), 1 <= t <= T
for t in range(T):
    _vars = ["X_{0}_{1}".format(i, t) for i in range(N)]
    _coef = [ri[i] for i in range(N)]
    model.linear_constraints.add(lin_expr=[cplex.SparsePair(ind=_vars, val=_coef)],
                                 rhs=[rt[t]], senses="L")


# Objective Function
_vars = ["X_{0}_{1}".format(i, t) for i in range(N) for t in range(T)] + \
        ["I_{0}_{1}".format(i, t) for i in range(N) for t in range(T)]

_coef = [cit[i][t] for i in range(N) for t in range(T)] + \
        [hit[i][t] for i in range(N) for t in range(T)]

model.objective.set_linear(zip(_vars, _coef))
model.objective.set_sense(model.objective.sense.minimize)

model.solve()

print("Objective value: ", model.solution.get_objective_value(), "\n")  # print the Objective value

print("Xit")
for i in range(N):
    print("item: ", i)
    for t in range(T):
        print(model.solution.get_values("X_{0}_{1}".format(i, t)))

print("\nIit")
for i in range(N):
    print("item: ", i)
    for t in range(T):
        print(model.solution.get_values("I_{0}_{1}".format(i, t)))



for t in range(T):
    print("t =: ", t)
    soma = 0
    for i in range(N):
        soma = soma + a_i[i] * model.solution.get_values("X_{0}_{1}".format(i, t))
    print(soma)
