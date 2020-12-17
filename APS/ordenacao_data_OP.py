import sys                              #for maxInt
import random
from collections import defaultdict
import datetime                         #for Gantt (time formatting) #duration is in days
import plotly                           #for Gantt (full package)
import plotly as py              #for Gantt
import plotly.figure_factory as ff      #for Gantt
#plotly.tools.set_credentials_file(username='addejans', api_key='65E3LDJVN63Y0Fx0tGIQ')  #for Gantt -- DeJans pw:O********1*
#import chart_studio
#chart_studio.tools.set_credentials_file(username='tutrinhkt94', api_key='vSrhCEpX6ADg7esoVCbc')  #for Gantt -- T.Tran pw:OaklandU
import copy                             #for saving best objects
from leitura_op import ler_dados # for data reading
import pandas as pd
import numpy as np
import plotly.graph_objs as go# for Gantt
from plotly.offline import download_plotlyjs, init_notebook_mode,  plot #for Gantt

############################## INITIALIZATION --- START

    
pi = ler_dados(1) # lendo dados de processamento

datas = ler_dados(0) # lendo dados das datas das ops

grupo_maq = ler_dados(2) # lendo dados dos grupos de máquinas;

seq_process = ler_dados(3) # lendo dados dos tabela da seqûencia;


# print("\n")
# print("\n")

# print(pi)

# print("\n")
# print("\n")

# print(datas)

# print("\n")
# print("\n")

# print(grupo_maq)

# print("\n")
# print("\n")

#Ordenando as OPs por Operação
seq_process_ordenado = seq_process.sort_values(by=['Ord Prod', 'Oper']) 

# print(seq_process_ordenado)

# print("\n")
# print("\n")

########## Ordenando as OPs por data de entrega ######################

#Removendo Linhas duplicatas#

datas.drop_duplicates(inplace = True)

#"Ordenando as OPs por data de entrega#
datas['Término'] = pd.to_datetime(datas['Término'])

#Criando um novo dataframe para receber as datas de término ordenadas
OP_ordenadas_data = datas.sort_values(by=['Término'], ascending = 'False')

#print("OPs ordenadas por data de término")
#print(OP_ordenadas_data)

########## Fim da ordenação as OPs por data de entrega ##################


############## Criação do calendário de horizonte de planejamento ############

#importar configuraçoes de calendário do Brasil
# manipulação de calendários: https://peopledoc.github.io/workalendar/basic.html
# from datetime import date
# from workalendar.america import Brazil

# calendar = Brazil()
# print(calendar.holidays(2020))

#biblioteca e funções para os cálculos dos dias de trabalho
import datetime
from networkdays import networkdays

#dicionário para a inserção dos feriados específicos
HOLIDAYS  = { datetime.date(2020, 12, 25),}

#dias disponíveis para a programação
days = networkdays.Networkdays(datetime.date(2019, 3, 19), datetime.date(2019, 5, 20), holidays=HOLIDAYS)

#Estatísticas do horizonte de planejamento

print(f'''
Bussiness days: {len(days.networkdays())}
    {days.networkdays()[:2]}
    ...{days.networkdays()[-2:]}

Weekends:       {len(days.weekends())}
    {days.weekends()[:2]}
    ...{days.weekends()[-2:]}

Holidays:       {len(days.holidays())}
''')

############## Fim da Criação do calendário de horizonte de planejamento ############


################# Criação dos Conjuntos ###########################

#Conjunto de OPs a serem sequenciadas
N = OP_ordenadas_data['Ord Prod'].unique()
print("\n")
print("Conjuntos de OPs a serem sequenciadas")
print(N)
print("\n")

#Conjunto de máquinas disponíveis
M= pi.columns
print("Conjunto de máquinas disponíveis")
print(M)
print("\n")

#Conjunto auxliar para o cálculo do makespan
aux_M = M[1:]
print(aux_M)
print("\n")


#Conjunto de dias disponíveis no horizonte de programação
#print("Dias disponíveis para programação")
#print(len(days.networkdays()))
#print("\n")



#------------------- fim da leitura dos dados---------------------------------

#------------------- conversão dos dados---------------------------------


#print("\n")
#print("----------------Meta Heurística Algoritmo Genético-----------------")
#print("\n")

#print("Os dados são: \n", pi)
#print("\n")
#------------------- fim da conversão dos dados---------------------------------



#----------Declaração dos parametros de inicialização---------------------------


#--------------------Gerando a sequência aleatória--------------------

#print("--------------Parâmetros de entrada---------------------------")
print("\n")    

seq1 = []
 
seq2 = []

seq1= random.sample(list(N), int(len(N)))

print("A nova seq1 obtida é: ",seq1)

seq2= random.sample(list(N), int(len(N)))

print('#'*80)
print("\n")
print("A nova seq2 obtida é: ",seq2)    
print("\n")

#-----------------fim da geração de sequência aleatória-----------------

aa = 0
# if N>0 and N<10:
#   aa = 1000
# if N>=10 and N<20:
#   aa = 2000


while aa < 5:
  aa = aa+1
  print("---Ciclo: ", aa)
  print("-----------------------------Crossover------------------------------")
  print("\n")
  
  #patent chromosomes: 
  
  print("Pais") 
  print('#'*80)
  print("P1 :", seq1) 
  print("\n")
  print("P2 :", seq2, "\n") 
  
  seq3 = []
  seq4 = []
  
  print("\n")
  #---------- fim Declaração dos parametros de inicialização-------------------
  
  
  #----------Função que realiza o cross-over---------------------------
  
  # realizando o crossover através da escolha de um ponto aleatório 
  
  # gerando um número aleatório  
  k = random.sample(list(N),1)
  print("Ponto de crossover :", k) 
  
  ponto_crossover = 0
  
  
  for posicao in range(len(N)):
      if N[posicao] == k:
          ponto_crossover = posicao
  
  print('#'*80)
  print("Posição do ponto de crossover",ponto_crossover)
  
  # Interação entre os genes;
  for i in range(ponto_crossover, len(N)): 
    aux1 = seq1[i]
    seq3.append(aux1)
    aux2 = seq2[i]
    seq4.append(aux2)
  
    
  #print("A seq3 antes do crossover é: ", seq3)
  #print("\n")
    
  #print("A seq4 antes do crossover é: ", seq4)
  #print("\n")
    
  #Gerando os novos filhos
  for i in seq1:
    if i not in seq3:
      seq3.append(i)
    if i not in seq4:
      seq4.append(i)	    
  
  #print('#'*80)
  #print("Filhos") 
  #print("A seq3 após o crossover é: ", seq3)
  #print("\n")
    
  #print("A seq4 após o crossover é: ", seq4)
  
  #print("\n")
  
  #print("------------------------Fim do Crossover-------------------------")
  #print("\n")    
  
  #---------- Função que calcula o makespan---------------------------------
  
  # print('#'*80)
  # print('#'*80)
  # print(pi)
  
  def makespan(seq, pi):
      
      completionTimes = pd.DataFrame(np.zeros((pi.shape[0],pi.shape[1])),columns = pi.columns)
      completionTimes.index = pi.index
      i = seq[0]
      #print(completionTimes.shape)
      for m in M[1:]:
        for aux in aux_M:
            completionTimes.loc[i,m] = completionTimes.loc[i,aux] + pi.loc[i,m]
          
      for i in range(len(seq)):
          atual = seq[i]
          print("\n")
          print("Atual é: ",  atual)
          anterior = seq[i-1]
          print("Anterior é: ",  anterior)
          print("\n")
          print("\n")
          completionTimes.loc[atual,0] >= completionTimes.loc[anterior,1] #restrição 6
          completionTimes.loc[atual,0] >= completionTimes.loc[anterior,0] + pi.loc[atual,0]#restrição 7
      
          for m in M:
              completionTimes.loc[atual,m] >= completionTimes.loc[anterior,(m[0], m[1]+1)] #restrição 8
          
          for m in M:
              completionTimes.loc[atual,m] >= completionTimes.iloc[atual,(m[0], m[1]-1)] + pi.loc[atual,m] #restrição 9
              completionTimes.loc[atual,m] = max(completionTimesiloc[atual,(m[0], m[1]-1)],completionTimes.iloc[anterior,m])  + pi.loc[atual,m]
      global aux_completionTimes 
      aux_completionTimes = completionTimes
      return completionTimes.max
  
  #---------- fim Função que calcula o makespan---------------------------------
  
  #--------------------Gerando as mutações de seq3---------------------------
  
  # print("------------------------Mutações--------------------------------")
  # print("\n")     
  
  # print("------------------------Mutação da seq3 --------------------------")
  # print("\n")     
  
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
  # print("A seq3 atual é: ", melhor_seq3)
  # #--------------------Fim da geração as mutações de seq3-------------------  
  
  # print("------------------fim da Mutação da seq3 --------------------------")
  # print("\n")     
  
  
  
  # #--------------------Gerando as mutações de seq4--------------------------
  
  # print("------------------------Mutação da seq4 --------------------------")
  # print("\n") 
  
  
  
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
  # print("A seq4 atual é: ", melhor_seq4)    
  
  # #--------------------Fim da geração as mutações de seq4 -------------------    
  
  # print("------------------Fim da Mutação da seq4 --------------------------")
  # print("\n")    
  
  # print("------------------------ Fim da Mutações---------------------------")
  # print("\n")
  
  
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
  
  
  # Ordena pelo maior valor de Makespan e salva em um novo DataFrame
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
  
  #------------------ Fim da fase de seleção---------------------------------#
  
  
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

###############################################################
# Construção da matriz de início

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

###############################################################
# Construção da matriz de término


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