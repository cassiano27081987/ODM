#Meta Heurística Algoritmo Genético

import sys
print(sys.executable)
# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
#import cplex
import numpy
import numpy as np
from prettytable import PrettyTable
import random
import copy 
import time
import timeit
from leitura_op import ler_dados
import numpy as np
import pandas as pd
from mip import Model, xsum, minimize, BINARY


#ler_dados: função que quando = 1 retorna a tabela dos processamento;
#                      quando = 0 retorna os dados das datas das ops;
#                      quando = 2 retorna os dados dos grupos de máquinas;
#                      quando = 3 retorna os dados dos tabela da seqûencia;
#


pi = ler_dados(1) # lendo dados de processamento

datas = ler_dados(0) # lendo dados das datas das ops

grupo_maq = ler_dados(2) # lendo dados dos grupos de máquinas;

seq_process = ler_dados(3) # lendo dados dos tabela da seqûencia;


print("\n")
print("\n")

print(pi)

print("\n")
print("\n")

print(datas)

print("\n")
print("\n")

print(grupo_maq)

print("\n")
print("\n")

print(seq_process)

print("\n")
print("\n")


inicio = timeit.default_timer()



#------------------- fim da leitura dos dados---------------------------------



print("\n")
print("----------------Meta Heurística Algoritmo Genético-----------------")
print("\n")


#------------------- fim da conversão dos dados---------------------------------

#-------------------declaração dos conjuntos---------------------------------


#Criando o vetor de máquinas


#for m in grupo_maq['Grp Maq'].values:
# 
M = grupo_maq['Grp Maq'].values[:-1]

print(" O vetor de máquinas é:")
print(M)
print("\n")

#Criando o vetor de ordens 

N = datas['Ord Prod'].values

print(" O vetor de ordens é:")
print(N)
print("\n")


#-------------------fim da declaração dos conjuntos---------------------------


#----------Declaração dos parametros de inicialização---------------------------


#--------------------Gerando a sequência aleatória--------------------

print("--------------Parâmetros de entrada---------------------------")
print("\n")    

seq1 = []
 
seq2 = []

seq1= np.random.choice(N, len(N))

print("A nova seq1 obtida é: ",seq1)

seq2= np.random.choice(N, len(N))

print("A nova seq1 obtida é: ",seq2)    

#-----------------fim da geração de sequência aleatória-----------------




aa = 0

while aa < 1001:
    aa = aa+1
    print("---Ciclo: ", aa)
    print("-----------------------------Crossover------------------------------")
    print("\n")
    
    # patent chromosomes: 
	
    print("Pais") 
    print("P1 :", seq1, "\n") 
    print("P2 :", seq2, "\n") 
    
    seq3 = []
    seq4 = []
    
    print("\n")
    #---------- fim Declaração dos parametros de inicialização-------------------
    
    
    #----------Função que realiza o cross-over---------------------------
    
    # realizando o crossover através da escolha de um ponto aleatório 
    
     # gerando um número aleatório  
    k = np.random.choice(N, 1) 
    print("Ponto de crossover :", k) 
    
    # Interação entre os genes;
    for i in range(k, len(seq1)): 
	    aux1 = seq1[i]
	    seq3.append(aux1)
	    aux2 = seq2[i]
	    seq4.append(aux2)
	
     
    print("A seq3 antes do crossover é: ", seq3)
    print("\n")
    print("A seq4 antes do crossover é: ", seq4)
    print("\n")
     
    #Gerando os novos filhos
    for i in range(len(seq1)):
	    if i not in seq3:
		    seq3.append(i)
	    if i not in seq4:
		    seq4.append(i)	    
    
    print("Filhos") 
    print("\n")
    print("A seq3 após o crossover é: ", seq3)
    print("\n")
    print("A seq4 após o crossover é: ", seq4)
	
    print("\n")
    
    print("------------------------Fim do Crossover-------------------------")
    print("\n")    
    
    #---------- Função que calcula o makespan---------------------------------
    
    def makespan(seq, pi):
	    completionTimes = np.zeros((N,M))
	    i = seq[0]
	    completionTimes[i][0] = (pi[i][0])
	    completionTimes[0][0] = (1*maq*pi[i][0]) #restrição 4
	    for m in range(1,M):
		    i = seq[0]
		    completionTimes[i][m] = completionTimes[i][m-1] + (pi[i][m])
		    completionTimes[0][m] >= completionTimes[0][m-1] + (1*maq*pi[i][m])#restrição 5
	    
	    for i in range(1, len(seq)):
		    atual = seq[i]
		    anterior = seq[i-1]
		    completionTimes[atual][0] >= completionTimes[anterior][1] #restrição 6
		    completionTimes[atual][0] >= completionTimes[anterior][0] + (1*jobs*pi[atual][0])#restrição 7
		    
		    for m in range(1, M-1):
			    completionTimes[atual][m] >= completionTimes[anterior][m+1] #restrição 8
		    
		    for m in range(1, M):
			    completionTimes[atual][m] >= completionTimes[atual][m-1] + (1*jobs*pi[atual][m]) #restrição 9
			    completionTimes[atual][m] = max(completionTimes[atual][m-1],completionTimes[anterior][m])  + pi[atual][m]
	    return np.max(completionTimes)
    #---------- fim Função que calcula o makespan---------------------------------
    
    #--------------------Gerando as mutações de seq3---------------------------
    
    print("------------------------Mutações--------------------------------")
    print("\n")     
   
    print("------------------------Mutação da seq3 --------------------------")
    print("\n")     
    
    pos = len(seq3)-1 
    
    solucao = 'float'
    
    melhor_solucao = 100000000000000
    melhor_seq3 = []
    
    while pos > 0:
	    seq3[pos], seq3[pos-1] = seq3[pos-1], seq3[pos]
	    print('Permutação %d ' %(pos), end="\t")
	    print(seq3)
	    solucao = makespan(seq3, pi)
	    print("O makespan da sequência é: ",solucao)
	    print("\n")
	    if solucao < melhor_solucao:
		    melhor_solucao = copy.deepcopy(solucao)
		    melhor_seq3 = copy.deepcopy(seq3)
		    print("A solução atual é: ", melhor_solucao)
			
	    pos -= 1
    print("A seq3 atual é: ", melhor_seq3)
    #--------------------Fim da geração as mutações de seq3-------------------  
    
    print("------------------fim da Mutação da seq3 --------------------------")
    print("\n")     
    
    
    
    #--------------------Gerando as mutações de seq4--------------------------
    
    print("------------------------Mutação da seq4 --------------------------")
    print("\n") 



    pos = len(seq4)-1 
    
    solucao = 'float'
    
    melhor_solucao = 100000000000000
    melhor_seq4 = []
    
    while pos > 0:
	    seq4[pos], seq4[pos-1] = seq4[pos-1], seq4[pos]
	    print('Permutação %d ' %(pos), end="\t")
	    print(seq4)
	    solucao = makespan(seq4, pi)
	    print("O makespan da sequência é: ",solucao)
	    print("\n")
	    if solucao < melhor_solucao:
		    melhor_solucao = copy.deepcopy(solucao)
		    melhor_seq4 = copy.deepcopy(seq4)
		    print("A solução atual é: ", melhor_solucao)
			
	    pos -= 1
    print("A seq4 atual é: ", melhor_seq4)    
    
    #--------------------Fim da geração as mutações de seq4 -------------------    
    
    print("------------------Fim da Mutação da seq4 --------------------------")
    print("\n")    
    
    print("------------------------ Fim da Mutações---------------------------")
    print("\n")
    
    
    solucao1 = []
    
    solucao1 = makespan(seq1,pi)
    
    solucao2 = []
    
    solucao2 = makespan(seq2,pi)
    
    solucao3 = []
    
    solucao3=makespan(melhor_seq3,pi)
    
    solucao4 = []
    
    solucao4 =makespan(melhor_seq4,pi)
    
    #------------------ Início da fase de seleção---------------------------------#
    
    print("-----------------------------Seleção------------------------------\n")
    
    import pandas as pd
    
    selecao = pd.DataFrame({'Sequência': [seq1, seq2, melhor_seq3,melhor_seq4], 'Makespan': [solucao1, solucao2, solucao3, solucao4]})# criando a tabela com as sequências e seus respectivos makespans
    
    
    # Ordena pelo maior valor de Makesopan e salva em um novo DataFrame
    selecao_ordenado = selecao.sort_values(by='Makespan')
    
    print("As soluções ordenadas são: ")
    print(selecao_ordenado)
    print("\n")
    
    aux1 = selecao_ordenado.iloc[0,0] #pegando a primeira melhor sequência
    seq1 = copy.deepcopy(aux1)#copiando os valores para a seq1
    print("A melhor sequência deste ciclo foi: \n", seq1)
    aux3 = selecao_ordenado.iloc[0,1] #pegando o makespan da melhor sequência
    print("A menor Makespan deste ciclo foi: ", aux3)
    
    aux2 = selecao_ordenado.iloc[1,0] #pegando a primeira melhor sequência
    seq2 = copy.deepcopy(aux2)#copiando os valores para a seq1
    print("A segunda melhor sequência deste ciclo foi: \n", seq2)
    aux4 = selecao_ordenado.iloc[1,1] #pegando o makespan da melhor sequência
    print("O menor Makespan deste ciclo foi: ", aux4    )
    print("\n")
    

fim = timeit.default_timer()
diferenca_tempo = 0.00
print('Tempo de execução do GA')
diferenca_tempo =  fim - inicio
print(diferenca_tempo)
print()
 
'''
# Criando e escrevendo em arquivos de texto (modo 'w').
arquivo = open('/home/cassiano/Área de Trabalho/Tópicos Avançados em Gerência da Produção/2020/Trabalho Final/Resultados/Resultados Algoritmo Genético/N5M4-1(new1).txt','w')
arquivo.write("Instância N5M4-1(new1).txt\n")
arquivo.write("Melhor sequência: ")
arquivo.write(str(aux1))
arquivo.write("\n")
arquivo.write("Menor Makespan: ")
arquivo.write(str(aux3))
arquivo.write("\n")
arquivo.write('Tempo de execução do GA:')
arquivo.write(str(diferenca_tempo))
arquivo.close() 
    
'''
