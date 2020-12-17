

import pandas as pd
import numpy as np

def ler_dados(escolha):




    #pd.set_option("display.max_rows", None, "display.max_columns", None)


    '''
    print (df.iloc[0])
    print (df.iloc[0][2])
    print (df.loc[0, 'fm-codigo'])
    print (df.loc['fm-codigo'])
    '''


    #################################################################################################
    #Lendo os dados da Tabela Acompanhamento da Ordem de Produção

    df_ordem = pd.read_excel(r'/home/cassiano/Área de Trabalho/ODM/APS/teste job shop.ods',sheet_name='Dados OP')[['Ord Prod','Item','Descrição','Un','Início','Término','Qtde Ordem','Estado da Ordem','Oper','Descrição','Qtde Prod','Tmp Máq','Grp Maq','Descrição GM']]

    print(df_ordem)



    #################################################################################################
    #Lendo os dados da Tabela Grupo de Máquinas
    df_gm = pd.read_excel(r'/home/cassiano/Área de Trabalho/ODM/APS/teste job shop.ods',sheet_name='Grupos de máquina', header=2)[['Grupo Maq','Descrição','Nº processadores','Carga Disponível (h/d)']]

    df_gm.columns = ['Grp Maq','Descrição','Nº processadores','Carga Disponível (h/d)']
    #foi necessário alterar o nome da primeira coluna para realizar o merge (próximo passo)

    df_gm.dropna(how='any') #retirando os valores nulos

    #print(df_gm)


    #################################################################################################
    #Inserindo a Coluna Carga Disponível (h/d)

    df_completo = pd.merge(df_ordem,df_gm, on='Grp Maq')

    df_completo.drop('Descrição_y',  inplace=True, axis=1) #removendo colunas duplicadas do merge
    df_completo.drop('Grp Maq',  inplace=False, axis=1)#removendo colunas duplicadas do merge

    print(df_completo)
   

    #################################################################################################
    #Criando a matriz do roteiro

    colunas_selecionadas = ['Grp Maq']

    df_roteiro = df_gm.filter(items = colunas_selecionadas)

    df_roteiro.pivot(columns = 'Grp Maq')


    #print(df_roteiro)
    

    table_processamento = pd.pivot_table(df_completo, values =['Tmp Máq'], index=['Ord Prod'], columns = ['Grp Maq'],aggfunc=np.sum,fill_value=0)

    print(table_processamento)

    

    ##################################################################################
    #Criação da tabela de data de entrega


    colunas_selecionadas1 = ['Ord Prod','Início','Término']

    df_data_op = df_completo[colunas_selecionadas1]

    df_data_op.drop_duplicates()

    print(df_data_op)

    


    ##################################################################################
    #Criação a tabela de sequencia

    #table_sequencia= pd.pivot_table(df_completo, values=['Tmp Máq'], columns=['Oper','Grp Maq'],index=['Ord Prod'],fill_value=0)


    colunas_selecionadas2 = ['Ord Prod','Oper','Grp Maq','Tmp Máq']


    df_sequencia= df_ordem[colunas_selecionadas2]

    #print("Tabela da sequencia")
    print(df_sequencia)
    #return table_sequencia

    if escolha ==0:
        return df_data_op

    if escolha ==1:
        return table_processamento

    if escolha ==2:
        return df_gm

    if escolha==3:
        return df_sequencia

    if escolha==4:
        return df_completo


aux = ler_dados(3)

print("\n")
print("\n")

print(aux)  