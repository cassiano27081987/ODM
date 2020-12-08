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
from criar_no import param_seq
from leitura_op import ler_dados

inicio = timeit.default_timer()


#-------------------declaração dos parametros---------------------------------

pi = []# matriz que receberá os tempos de processamento



#-------------------fim da declaração dos parametros---------------------------

#-------------------leitura dos dados---------------------------------

arquivo= open('/home/cassiano/Área de Trabalho/ODM/Otimização Python/APS/table_process.txt','r')

linha = arquivo.readline()
#print("A linha é: ",linha)
#print("\n")
while linha != "":
    elementos = linha.split()
    for n in range(len(elementos)):
        elementos[n] = float(elementos[n])
        aux = elementos
    pi.append(aux)
    linha = arquivo.readline()

arquivo.close()

   

print ("\n Os dados são: \n")
print(pi)



jobs = len(pi) #número de tarefas representada pelas linhas de pi
maq = len(pi[0]) #número de máquinas representada pelas colunas de pi

#------------------- fim da leitura dos dados---------------------------------




# teste = param_seq()
# #print(teste.get_joblist())

# #teste = param_seq()
# #print(teste.get_nodelist())


# ############################## INITIALIZATION --- START


# pi2 = ler_dados(1) # lendo dados de processamento

# datas = ler_dados(0) # lendo dados das datas das ops

# grupo_maq = ler_dados(2) # lendo dados dos grupos de máquinas;

# seq_process = ler_dados(3) # lendo dados dos tabela da seqûencia;


# print("\n")
# print("\n")
# print("Os dados são:")
# print(pi2)

# print("\n")
# print("\n")
# print("As datas são:")
# print(datas)

# print("\n")
# print("\n")
# print("Os grupos de máquinas são:")
# print(grupo_maq)

# print("\n")
# print("\n")
# print("A sequência de processamento é: ")
# print(seq_process.sort_values(by=['Ord Prod', 'Oper'])) #ordenando por job

# ############################# Criação dos conjuntos #################################

# conjuntos = param_seq()
# numJobs = conjuntos.get_numJobs()

# numMachines = conjuntos.get_numMachines()

# numNodes =  conjuntos.get_numNodes()


print("\n Os dados são: \n")
print(pi)
print("\n")



#------------------- fim da leitura dos dados---------------------------------

#------------------- conversão dos dados---------------------------------


print("\n")
print("----------------Meta Heurística Algoritmo Genético-----------------")
print("\n")

print("Os dados são: \n", pi)
print("\n")
#------------------- fim da conversão dos dados---------------------------------

#-------------------declaração dos conjuntos---------------------------------
M =  len(pi[0]) #número de jobs
N =  len(pi) #número de maquinas

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

while aa < 1001:
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

print("\n")
print("\n")

print("", end="\t")
for i in range(aux3):
    print (i+1, end="\t")
print()
for i in range(jobs):
    print(i+1, end="\t")
    for j in range(jobs):
        print(completionTimes[i][j], end="\t")
    print()
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
    



from locale import setlocale, LC_ALL
from calendar import mdays

setlocale(LC_ALL, '')
setlocale(LC_ALL, 'pt_BR.utf-8')



############################## GANTT --- START
def makeGanttChart(bestSoFarAnt):
    #quit()  #to not use more than 30 API calls per hour or 50 per day
    df = []
    colors = {}
    ordem_producao = teste.get_ordens_producao()
    for job in JOBSLIST: #I believe this could stay as JOBSLIST since we pass in only the node.num into the bestSoFarNODESLIST
        for node in job.Nodes:
            if node.duration> 0 and node.duration != 0:
                print("\n")
                print("node.num é: ",node.num)
                print("job.num é: ",job.num)
                print("\n")
                s = str(datetime.datetime.strptime('2020-12-02 07:15:00', "%Y-%m-%d %H:%M:%S"))
                d = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=bestSoFarNODESLIST[node.num].startTime)+ \
                    datetime.timedelta(hours=bestSoFarNODESLIST[node.num].duration)
                if s!= 0 and d != 0:
                    df.append(dict(Task=str(node.machine), Start=str(s), Finish=str(d), Resource=str(job.num), OP=str(ordem_producao[node.num])))
                    print("O tempo de início é: ",s)
                    print("O tempo de término é: ",d)
                    print("\n")
        #random_color = np.random.randint(0,256,size=(3)).tolist()
        #random_color = np.array(random_color)  
        #print("random_color é: ", random_color)  
        #colors.update({str(node.machine) : 'rgb'+str(random_color).replace('[','(').replace(']',')')})
        #print(colors)

    
    
    fig = ff.create_gantt(df, title = "ADAVANCED PLANNING SCHEDLING - ODM ",group_tasks=True, showgrid_x =True)
    
    
    plot(fig)




# Criando e escrevendo em arquivos de texto (modo 'w').
arquivo = open('/home/cassiano/Área de Trabalho/ODM/Otimização Python/APS/genetico-4000.txt','w')
arquivo.write("Teste 4000")
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