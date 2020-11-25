#teste de leitura

from leitura_arquivos import Leitura_Dados
import numpy as np

p1 = []

aux = Leitura_Dados()

aux.ler_matriz('/home/cassiano/Área de Trabalho/Tópicos Avançados em Gerência da Produção/2020/Trabalho Final/Instâncias/N40M32-1.txt')
p1.append(aux)

print(values(p1))

'''
#p1 = np.array(p1)

I =  len(p1[0]) #número de linhas
J =  len(p1) #número de colunas



print("Os dados são: ")


for i in range (len(p1[0])):
    print()
    for j in range (len(p1)):
        print(p1[i][j])
    print()
'''