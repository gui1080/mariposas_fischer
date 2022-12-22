from recupera_arquivos import recupera_lista_arquivos, recupera_lista_imagens
from arquivos_locais import MOSTRAR_PRINTS, FISCHER_BD
import sqlite3
import os
import time 
import pandas as pd
import random

from relaciona_coleta import relaciona_coleta

# -----------------------------------------------

def main():

    # declarando queries
    #-------------------------------------------------------

    #[identificador, nome, string_arquivo, caminho_absoluto, caminho_relativo, familia_nome, sub_familia_nome]

    cria_tabela_main = '''CREATE TABLE IF NOT EXISTS main (
        identificador INTEGER PRIMARY KEY AUTOINCREMENT, 
        nome VARCHAR(255), 
        string_arquivo VARCHAR(255),
        caminho_absoluto VARCHAR(255),
        caminho_relativo VARCHAR(255),
        familia_nome VARCHAR(255),  
        sub_familia_nome VARCHAR(255))'''

    cria_tabela_coleta = '''CREATE TABLE IF NOT EXISTS coleta (
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
        long_hem VARCHAR(5),
        id_coleta INTEGER PRIMARY KEY AUTOINCREMENT,)'''

    insert_teste1 = '''INSERT INTO main VALUES (NULL, 'Acharia sp. 3', 'descrição aqui', 'sla1', 'sla2')'''

    insert_teste2 = '''INSERT INTO coleta (id_coleta, inst_bar_code) VALUES (NULL, 'USNM 00167178')'''


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
    df_imagens = pd.DataFrame(imagens_para_import, columns = ["id", "nome", "string_arquivo", "caminho_absoluto", "caminho_relativo", "familia_nome", "sub_familia_nome"])

    # salva no BD
    try:
        conn = sqlite3.connect(os.path.dirname(__file__) + FISCHER_BD)
        c = conn.cursor()

        df_imagens.to_sql('main', conn, if_exists='replace', index=False)

        conn.commit()
        time.sleep(1)
    
    except:
        print("Erro!")
        quit()

    finally:
        conn.close()

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
            
            dados_excel["Inst. Bar Code"] = dados_excel["Inst. Bar Code"].astype(str)

            if MOSTRAR_PRINTS == 1:
                print(dados_excel.head())
                print("Mostrando colunas da planilha!")
                print("\n\n-----------")
                for col in dados_excel.columns:
                    print(col)
                print("-----------\n\n")

            ids_coleta = []

            for row, index in dados_excel.iterrows():
                
                ids_coleta.append("NULL")

            dados_excel["id_coleta"] = ids_coleta

            # renomeia colunas
            dados_excel.rename(
                            {'Inst. Bar Code':'inst_bar_code',
                            'Genus':'genus',
                            'Species':'species',
                            'Author':'author',
                            'Sex':'sex',
                            'number of spec':'number_of_spec',
                            'Museum/Coll':'museum_coll',
                            'Country':'country',
                            'Province':'province',
                            'Locality':'locality',
                            'date':'date',
                            'collector':'collector',
                            'type #':'type',
                            'accession #':'accession',
                            'Lat. o':'lat',
                            'Lat. 1':'lat1',
                            'Lat. 2':'lat2',
                            'Lat. Hem.':'lat_hem',
                            'Long. o':'long',
                            'Long. 1':'long1',
                            'Long. 2':'long2',
                            'Long. Hem.':'long_hem',
                            'id_coleta':'id_coleta'}, axis='columns', inplace=True)

            if MOSTRAR_PRINTS == 1:
                print(dados_excel.head())
                print("Mostrando colunas da planilha!")
                print("\n\n-----------")
                for col in dados_excel.columns:
                    print(col)
                print("-----------\n\n")

            # bota no BD
            try:

                conn = sqlite3.connect(os.path.dirname(__file__) + FISCHER_BD)
                c = conn.cursor()

                dados_excel.to_sql('coleta', conn, if_exists='append', index=False)

                conn.commit()
                time.sleep(1)
            
            except:
                print("Erro botando coleta no BD!")
                quit()

            finally:
                conn.close()




# -----------------------------------------------

if __name__ == '__main__':

    inicio = time.time()
    main()
    relaciona_coleta()
    fim = time.time()

    duracao = (fim - inicio) / 60

    if MOSTRAR_PRINTS == 1:
        print("\n\nFim da execução")
        print("Duração: " + str(duracao))