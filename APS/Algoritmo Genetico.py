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
from collections import defaultdict
import datetime                         #for Gantt (time formatting) #duration is in days
import plotly                           #for Gantt (full package)
import plotly.figure_factory as ff      #for Gantt
import matplotlib as plt
import chart_studio.plotly as py  

inicio = timeit.default_timer()


#-------------------declaração dos parametros---------------------------------

pi = []# matriz que receberá os tempos de processamento

#-------------------fim da declaração dos parametros---------------------------

#-------------------leitura dos dados---------------------------------

arquivo = open('/home/cassiano/Área de Trabalho/Tópicos Avançados em Gerência da Produção/2020/Trabalho Final/Instâncias/N20M16-1.txt','r')

linha = arquivo.readline()
#print("A linha é: ",linha)
#print("\n")
while linha != "":
    elementos = linha.split()
    for n in range(len(elementos)):
        elementos[n] = int(elementos[n])
        aux = elementos
    pi.append(aux)
    linha = arquivo.readline()

arquivo.close()

jobs = len(pi) #número de máquina representada pelas colunas de pi
maq = len(pi[0]) #número de máquina representada pelas colunas de pi

print(jobs,maq)




#------------------- fim da leitura dos dados---------------------------------

#------------------- conversão dos dados---------------------------------


print("\n")
print("----------------Meta Heurística Algoritmo Genético-----------------")
print("\n")

print("Os dados são: \n", pi)
print("\n")
#------------------- fim da conversão dos dados---------------------------------

#-------------------declaração dos conjuntos---------------------------------
M=  len(pi[0]) #número de jobs
N=  len(pi) #número de maquinas

#-------------------fim da declaração dos conjuntos---------------------------


#----------Declaração dos parametros de inicialização---------------------------


#--------------------Gerando a sequência aleatória--------------------

print("--------------Parâmetros de entrada---------------------------")
print("\n")    

seq1 = []
 
seq2 = []

seq1= random.sample(range(0,N), N)

print("A nova seq1 obtida é: ",seq1)

seq2= random.sample(range(0,N), N)

print("A nova seq1 obtida é: ",seq2)    

#-----------------fim da geração de sequência aleatória-----------------

aa = 0
# if N>0 and N<10:
#   aa = 1000
# if N>=10 and N<20:
#   aa = 2000


while aa < 3000:
    aa = aa+1
    print("---Ciclo: ", aa)
    print("-----------------------------Crossover------------------------------")
    print("\n")
    
    # patent chromosomes: 
	
    print("Pais") 
    print("P1 :", seq1) 
    print("P2 :", seq2, "\n") 
    
    seq3 = []
    seq4 = []
    
    print("\n")
    #---------- fim Declaração dos parametros de inicialização-------------------
    
    
    #----------Função que realiza o cross-over---------------------------
    
    # realizando o crossover através da escolha de um ponto aleatório 
    
     # gerando um número aleatório  
    k = random.randint(0, N) 
    print("Ponto de crossover :", k) 
    
    # Interação entre os genes;
    for i in range(k, len(seq1)): 
	    aux1 = seq1[i]
	    seq3.append(aux1)
	    aux2 = seq2[i]
	    seq4.append(aux2)
	
     
    print("A seq3 antes do crossover é: ", seq3)
    print("A seq4 antes do crossover é: ", seq4)
    print("\n")
     
    #Gerando os novos filhos
    for i in range(len(seq1)):
	    if i not in seq3:
		    seq3.append(i)
	    if i not in seq4:
		    seq4.append(i)	    
    
    print("Filhos") 
    print("A seq3 após o crossover é: ", seq3)
    print("A seq4 após o crossover é: ", seq4)
	
    print("\n")
    
    print("------------------------Fim do Crossover-------------------------")
    print("\n")    
    
    #---------- Função que calcula o makespan---------------------------------
   
    def makespan(seq, pi):
        completionTimes = np.zeros((N,M))
        i = seq[0]
        completionTimes[i][0] = (pi[i][0])
        completionTimes[0][0] = (N*pi[i][0]) #restrição 4
        
        for m in range(1,M):
            i = seq[0]
            completionTimes[i][m] = completionTimes[i][m-1] + (pi[i][m])
            completionTimes[0][m] >= completionTimes[0][m-1] + (M*pi[i][m])#restrição 5
	    
        for i in range(1, len(seq)):
            atual = seq[i]
            anterior = seq[i-1]
            completionTimes[atual][0] >= completionTimes[anterior][1] #restrição 6
            completionTimes[atual][0] >= completionTimes[anterior][0] + (N*pi[atual][0])#restrição 7
        
            for m in range(1, M-1):
                completionTimes[atual][m] >= completionTimes[anterior][m+1] #restrição 8
            
            for m in range(1, M):
                completionTimes[atual][m] >= completionTimes[atual][m-1] + (M*pi[atual][m]) #restrição 9
                completionTimes[atual][m] = max(completionTimes[atual][m-1],completionTimes[anterior][m])  + pi[atual][m]
        global aux_completionTimes 
        aux_completionTimes = completionTimes
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


###################################################
#Calculando os parâmetros do Gantt

#aux1 = martriz das sequencias do jobs ótima
#incio_job = tempos de inicio dos jobs nas maquinas



seq_otima = []

for i in aux1:
    seq_otima.append(pi[i])



print("\n")

print(aux1)
print("\n")

print("Sequencia ótima")
print(seq_otima)

#Construção da matriz de início

inicio = np.zeros((N,M))


for i in range (N):
  for j in range(M):
    if i==0 and j==0:
      inicio[0][0]=0
    elif i>0 and j==0:
      inicio[i][j] =inicio[i-1][j+1]   
    elif i==N-1:
      inicio[i][j] = inicio[i][j-1]+ seq_otima[i][j-1]
    else:
      if  j<M-1:
        aux_comparacao = inicio[i][j-1] + seq_otima[i][j-1] 
        if aux_comparacao < inicio[i-1][j+1]:
          print(aux_comparacao)
          print("<")
          print(inicio[i-1][j+1])
          inicio[i][j] = inicio[i-1][j+1]
        else:  
          inicio[i][j] =inicio[i][j-1]+ seq_otima[i][j-1] 
      else:  
        if i==0:
          inicio[i][j] = inicio[i][j-1] + seq_otima[i][j-1]
        else:
          aux_comparacao = inicio[i][j-1] + seq_otima[i][j-1]
          if aux_comparacao > inicio[i][j]:
            inicio[i][j] = aux_comparacao
          else:
            inicio[i][j] =inicio[i][j-1]+ seq_otima[i][j-1]
        # if aux_comparacao > inicio[i][j]:
        #   print("Comparação última coluna")
        #   print(aux_comparacao)
        #   print(">")
        #   print(inicio[i][j])
        #   print(inicio[i][j-1])
        #   print(seq[i][j-1])
        #   inicio[i][j] =inicio[i][j-1]+ seq_otima[i][j-1]
     
       


print("\n")


print("Inicio das tarefas")   
print(inicio)


print("\n")

termino = np.zeros((N,M))

for i in range(N):
  for j in range(M):
    termino[i][j] = seq_otima[i][j] + inicio[i][j]

print("Término")
print(termino)


print("\n")


print("Inicio das tarefas")   
print(inicio)
   

print("\n")
print("Matrix das jobs")  
#print(seq)

print("\n")
print(seq_otima)


print("\n")

print("\n")
print("completionTimes")
print(aux_completionTimes)

#tempo_inicio = aux_completionTimes - seq_otima


print("\n")


import plotly.io as pio
pio.renderers
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import plotly.graph_objs as go# for Gantt
from plotly.offline import download_plotlyjs, init_notebook_mode,  plot #for Gantt

#########################################################################
#Impressao do Gantt

df = []
colors =[]
for i in range(N):
    for j in range(M):
        s = str(datetime.datetime.strptime('2020-12-09 07:00:00', "%Y-%m-%d %H:%M:%S") + datetime.timedelta(minutes=inicio[i][j] ))
        d = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")  + datetime.timedelta(minutes=seq_otima[i][j])
        df.append(dict(Task=str("maq "+str(j)), Start=str(s), Finish=str(d), Resource=str("job "+str(i))))
        print(f'Job {i} na Máquina {j}')
        print("O tempo de início é: ",s)
        print("O tempo de término é: ",d)
        print("\n")
        r = lambda: random.randint(0,255)
        colors.append('#%02X%02X%02X' % (r(),r(),r()))



fig = ff.create_gantt(df, colors = colors, index_col='Resource', title = "ADAVANCED PLANNING SCHEDLING - ODM ",show_colorbar=True, group_tasks=True,showgrid_x =True)
    

plot(fig)



plt.show()


# Criando e escrevendo em arquivos de texto (modo 'w').
arquivo = open('/home/cassiano/Área de Trabalho/ODM/Otimização Python/APS/genetico-3000-N20M16-1.txt','w')
arquivo.write("Teste 3000-N20M16-1")
arquivo.write("Melhor sequência: ")
arquivo.write(str(aux1))
arquivo.write("\n")
arquivo.write("Menor Makespan: ")
arquivo.write(str(aux3))
arquivo.write("\n")
arquivo.write('Tempo de execução do GA:')
arquivo.write(str(diferenca_tempo))
arquivo.close() 
    