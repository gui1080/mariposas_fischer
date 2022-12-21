from recupera_arquivos import recupera_lista_arquivos, recupera_lista_imagens
from arquivos_locais import MOSTRAR_PRINTS, FISCHER_BD
import sqlite3
import os
import time 
import pandas as pd

# -----------------------------------------------

def main():

    # declarando queries
    #-------------------------------------------------------

    cria_tabela_main = '''CREATE TABLE IF NOT EXISTS main (
        id_especie INTEGER PRIMARY KEY AUTOINCREMENT, 
        nome_especie VARCHAR(255), 
        descricao TEXT, 
        imagem_principal VARCHAR(255),  
        imagem_sec VARCHAR(255))'''

    cria_tabela_coleta = '''CREATE TABLE IF NOT EXISTS coleta (
        id_coleta INTEGER PRIMARY KEY AUTOINCREMENT,
        id_especie_referencia INTEGER, 
        inst_bar_code VARCHAR(255),
        genus VARCHAR(255),
        species VARCHAR(255),
        author VARCHAR(255),
        sex VARCHAR(1),
        number_of_spec INTEGER,
        museum_coll VARCHAR(255),
        country VARCHAR(255),
        province VARCHAR(255),
        locality VARCHAR(255),
        date VARCHAR(155),
        collector VARCHAR(255),
        type VARCHAR(255),
        accession VARCHAR(255),
        lat VARCHAR(5),
        lat1 VARCHAR(5),
        lat2 VARCHAR(5),
        lat_hem VARCHAR(5),
        long VARCHAR(5),
        long1 VARCHAR(5),
        long2 VARCHAR(5),
        long_hem VARCHAR(5))'''

    insert_teste1 = '''INSERT INTO main VALUES (NULL, 'Acharia sp. 3', 'descrição aqui', 'sla1', 'sla2')'''

    insert_teste2 = '''INSERT INTO coleta (id_coleta, id_especie_referencia, inst_bar_code) VALUES (NULL, '1', 'USNM 00167178')'''


    # acesso de BD
    #-------------------------------------------------------

    print("Iniciando BD!")
    try:
        conn = sqlite3.connect(os.path.dirname(__file__) + FISCHER_BD)
        c = conn.cursor()

        print("Cria tabela principal")
        c.execute(cria_tabela_main)
        conn.commit()
        time.sleep(1)

        print("Cria tabela de coleta")
        c.execute(cria_tabela_coleta)
        conn.commit()
        time.sleep(1)

        print("Faz insert1")
        c.execute(insert_teste1)
        conn.commit()
        time.sleep(1)

        print("Faz insert2")
        c.execute(insert_teste2)
        conn.commit()
        time.sleep(1)

    except:
        print("Erro!")
        
    finally:
        print("Finalizando acesso!")
        conn.close()

    # Dados de coleta (Imagens!)
    # -----------------------------------------------

    imagens_para_import = recupera_lista_imagens()
    # [identificador, nome, string de arquivo, caminho_absoluto, caminho_relativo, familia_nome, sub_familia_nome]

    # exporta para dataframe

    # salva no BD

    # Dados de coleta (.xlsx)
    # -----------------------------------------------

    arquivos_para_import = recupera_lista_arquivos()

    for arquivo in arquivos_para_import:

        if ".DS_Store" not in arquivo:

            if MOSTRAR_PRINTS == 1:
                print("Extraindo dados de " + str(arquivo))
            
            dados_excel = pd.read_excel(arquivo,
                                        engine="openpyxl",
                                        header=0,
                                        index_col=False,
                                        keep_default_na=True
                                        )
            
            if MOSTRAR_PRINTS == 1:
                print(dados_excel.head())
                print("Mostrando colunas da planilha!")
                print("\n\n-----------")
                for col in dados_excel.columns:
                    print(col)
                print("-----------\n\n")

            # renomeia colunas

            # bota no BD



# -----------------------------------------------

if __name__ == '__main__':

    inicio = time.time()
    main()
    fim = time.time()

    duracao = (fim - inicio) / 60

    if MOSTRAR_PRINTS == 1:
        print("\n\nFim da execução")
        print("Duração: " + str(duracao))