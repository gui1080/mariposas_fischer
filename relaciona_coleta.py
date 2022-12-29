from arquivos_locais import MOSTRAR_PRINTS, FISCHER_BD
import sqlite3
import os
import pandas as pd
import time 

def relaciona_coleta(dados_Coleta, dados_Main, referencia_main):

    # "genus" nos dados de coleta, bater
    # "species" em coleta com "nome" na tabela main

    # é uma relacao de 1 entrada na main para varias na coleta

    print("Iniciando relacionamento de coleta!")

    num_coleta = 0
    num_relacionamentos = 0

    for index_coleta, row_coleta in dados_Coleta.iterrows():
        
        genus_coleta = str(row_coleta["genus"]).lower()
        especie_coleta = str(row_coleta["species"]).lower()

        for index_main, row_main in dados_Main.iterrows():

            nome = str(row_main["nome"]).lower()

            if (genus_coleta in nome) or (genus_coleta == nome):
                
                if especie_coleta in nome:
                    
                    num_relacionamentos = num_relacionamentos + 1
                    #print("bateu")
                    # tem que add "referencia_main" nos dados da coleta
                    referencia_main_atual = str(referencia_main[num_coleta])

                    if referencia_main_atual == "0000":
                        referencia_main[num_coleta] = str(row_main["identificador"]) 
                    else:
                        referencia_main[num_coleta] = referencia_main_atual + ", " + str(row_main["identificador"]) 
                


        num_coleta = num_coleta + 1

    print("Relações feitas -> "+ str(num_relacionamentos))

    print("Coleta relacionada!")

    return referencia_main

def relaciona_imagens(df_imagens, dados_Main, referencia_main_imagens):

    contador_imagens = 0

    for index_imagem, row_imagem in df_imagens.iterrows():

        #id_imagem = row_imagem["identificador"]
        nome_imagem = str(row_imagem["nome"]).lower() 
        subfamilia = str(row_imagem["sub_familia_nome"]).lower() 

        for index_main, row_main in dados_Main.iterrows():

            nome_referencia = str(row_main["nome"]).lower()
            id_referencia = str(row_main["identificador"]).lower()

            if nome_imagem in nome_referencia or nome_referencia in nome_imagem:

                referencia_main_imagens[contador_imagens] = id_referencia
            
            elif nome_referencia in subfamilia or subfamilia in nome_referencia:

                referencia_main_imagens[contador_imagens] = id_referencia


        contador_imagens = contador_imagens + 1

    return referencia_main_imagens