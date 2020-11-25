

class Leitura_Dados:

    #def __init__(self, nome):
       #self.nome = nome



    def ler_matriz(self,arquivo):

        self.arquivo = arquivo    
        arquivo = open(arquivo,'r')
        conteudo = []

        linha = arquivo.readline()
        #print("A linha é: ",linha)
        #print("\n")
        while linha != "":
            elementos = linha.split()
            for n in range(len(elementos)):
                elementos[n] = (elementos[n])
                aux = elementos
            conteudo.append(aux)
            linha = arquivo.readline()
             
        arquivo.close()

        return conteudo