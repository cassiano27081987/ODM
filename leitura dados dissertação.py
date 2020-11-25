import sys
print(sys.executable)

#from __future__ import print_function
# !/usr/bin/python3.7
# -*- coding: utf-8 -*-
#from __future__ import print_function

import numpy as np
from prettytable import PrettyTable
from mip import Model, xsum, minimize, BINARY


#-----------------Problema de Dimensionamento de Lotes Estático----------------#

#Modelo SSDSC


#--------------Declaração dos parâmetros--------------------------#
'''
T = 10
S = 15
P = 5

dados = []

cc= [T,S,P]  # empty array to receive the times of the jobs in each machine

# split() method returns a list of strings after breaking the given string by the specified separator.
# separator : The is a delimiter. The string splits at this specified separator. If is not provided then any white space is a separator.


file = open("/home/cassiano/Documentos/Dissertação - Cassiano/Supplier Selection/Instâncias/5P-10T-15S/cc(t,s,p)-1.txt","r")
file.seek(0, 0)
for t in range(T):
    if t >0:
        linha = []  # cria as linhas vazias da matriz
        content = file.readline()  # reading the next line from the file
        line = content.split()  # split the content
        for p in range(P):
            if p>0:
                linha.append(int(line[p]))  # adds integers to the lines
        dados.append(linha)  # accreates lines filled to the matrix

file.close()

cc = dados

print("\n Os dados são: \n")
print(cc)
print("\n")

'''

T = 10
S = 15
P = 5


N = (T * S)+3  # number of jobs
M = 5  # number of machines

times = []

T = [M, N]  # empty array to receive the times of the jobs in each machine

# split() method returns a list of strings after breaking the given string by the specified separator.
# separator : The is a delimiter. The string splits at this specified separator. If is not provided then any white space is a separator.


file = open("/home/cassiano/Documentos/Dissertação - Cassiano/Supplier Selection/Instâncias/5P-10T-15S/cc(t,s,p)-1.txt","r")
file.seek(0, 0)
for i in range(N):
    if i>0:
        linha = []  # cria as linhas vazias da matriz
        content = file.readline()  # reading the next line from the file
        line = content.split()  # split the content
        for j in range(M):
            if j > 0:
                linha.append(line) # adds integers to the lines
        times.append(linha)  # accreates lines filled to the matrix

file.close()

T = times

print("\n Os dados são: \n")
print(T)
print("\n")


# Criando e escrevendo em arquivos de texto (modo 'w').
arquivo = open('/home/cassiano/Área de Trabalho/Teste.txt','w')
arquivo.write("Leitura de dados da dissertação.txt\n")
arquivo.write(str(T))
arquivo.write("\n")