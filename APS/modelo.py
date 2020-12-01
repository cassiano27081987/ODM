
import sys
print(sys.executable)

#from __future__ import print_function
# !/usr/bin/python3.7
# -*- coding: utf-8 -*-
#from __future__ import print_function



from leitura_op import ler_dados
import numpy as np
import pandas as pd
from mip import Model, xsum, minimize, BINARY


#ler_dados: função que quando = 1 retorna a tabela dos processamento e quando = 0 retorna os dados das datas

pi = ler_dados(1)

datas = ler_dados(0)

print("\n")
print("\n")

print(pi)

#Percorrendo a tabela de tempos na seguinte ordem (tempo da operação no recurso, número  da operação, recurso)
#for i in pi.columns:
    #print(pi[i].values)
    # for j in pi[i]:
    #     print(j)

print("\n")
print("\n")

print(datas)

print("\n")
print("\n")

