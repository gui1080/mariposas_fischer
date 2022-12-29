from recupera_arquivos import recupera_lista_arquivos, recupera_lista_imagens
from arquivos_locais import MOSTRAR_PRINTS, FISCHER_BD
import sqlite3
import os
import time 
import pandas as pd
import random

from relaciona_coleta import relaciona_coleta, relaciona_imagens

# -----------------------------------------------

def main():

    # declarando queries
    #-------------------------------------------------------

    cria_tabela_main = '''CREATE TABLE IF NOT EXISTS main (
        identificador INTEGER PRIMARY KEY, 
        nome VARCHAR(255)'''

    cria_tabela_imagens = '''CREATE TABLE IF NOT EXISTS imagens (
        identificador INTEGER PRIMARY KEY, 
        nome VARCHAR(255), 
        string_arquivo VARCHAR(255),
        caminho_absoluto VARCHAR(255),
        caminho_relativo VARCHAR(255),
        familia_nome VARCHAR(255),  
        sub_familia_nome VARCHAR(255), 
        identificador_referencia INTEGER)'''

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
        id_coleta INTEGER PRIMARY KEY,
        referencia_main INTEGER)'''

    insert_teste1 = '''INSERT INTO imagens VALUES (NULL, 'Acharia sp. 3', 'descrição aqui', 'sla1', 'sla2')'''

    insert_teste2 = '''INSERT INTO coleta (id_coleta, inst_bar_code) VALUES (NULL, 'USNM 00167178')'''


    # acesso de BD
    #-------------------------------------------------------

    print("Iniciando BD!")
    try:
        conn = sqlite3.connect(os.path.dirname(__file__) + FISCHER_BD)
        c = conn.cursor()

        print("Cria tabela principal")
        c.execute(cria_tabela_imagens)
        conn.commit()
        time.sleep(1)
        
        print("Cria tabela main")
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
    df_imagens = pd.DataFrame(imagens_para_import, columns = ["identificador", "nome", "string_arquivo", "caminho_absoluto", "caminho_relativo", "familia_nome", "sub_familia_nome"])

    # -----------------------------------------------

    identificador_main = []
    nome_main = []

    for index_imagens, row_imagens in df_imagens.iterrows():
        
        nome_imagem = str(row_imagens["nome"])
        nome_main.append(nome_imagem)
    
    nome_main = list(set(nome_main))
    
    for nome in nome_main:
        identificador_main.append(str(random.randint(111111,999999)))

    df_main = pd.DataFrame({'nome': nome_main, 'identificador': identificador_main})
    
    print(df_main)
    

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
                            'Long. Hem.':'long_hem'}, axis='columns', inplace=True)
            
            ids_coleta = []
            referencia_main = []

            for row, index in dados_excel.iterrows():
                
                ids_coleta.append(str(random.randint(111111,999999)))
                referencia_main.append("0000")

            referencia_main = relaciona_coleta(dados_excel, df_main, referencia_main)
            
            dados_excel["id_coleta"] = ids_coleta
            dados_excel["referencia_main"] = referencia_main

            if MOSTRAR_PRINTS == 1:
                print(dados_excel.head())
                print("Mostrando colunas da planilha!")
                print("\n\n-----------")
                for col in dados_excel.columns:
                    print(col)
                print("-----------\n\n")

            # salvar dados_Coleta de volta no BD
            try:

                conn = sqlite3.connect(os.path.dirname(__file__) + FISCHER_BD)
                c = conn.cursor()

                dados_excel.to_sql('coleta', conn, if_exists='replace', index=False)

                conn.commit()
                time.sleep(1)
                    
            except:
                print("Erro botando coleta no BD!")
                quit()

            finally:
                conn.close()

    # -----------------------------------------------
    # Relaciona imagens com tabela main

    referencia_main_imagens = []

    for row, index in df_imagens.iterrows():
        referencia_main_imagens.append("0000")

    referencia_main_imagens = relaciona_imagens(df_imagens, df_main, referencia_main_imagens)
    
    # append list as column
    df_imagens["identificador_referencia"] = referencia_main_imagens

    # -----------------------------------------------

    # salva no BD
    try:
        conn = sqlite3.connect(os.path.dirname(__file__) + FISCHER_BD)
        c = conn.cursor()

        df_imagens.to_sql('imagens', conn, if_exists='replace', index=False)

        conn.commit()
        time.sleep(1)


        df_main.to_sql('main', conn, if_exists='replace', index=False)

        conn.commit()
        time.sleep(1)
    
    except:
        print("Erro!")
        quit()

    finally:
        conn.close()

# -----------------------------------------------

if __name__ == '__main__':

    inicio = time.time()
    main()
    fim = time.time()

    duracao = (fim - inicio) / 60

    if MOSTRAR_PRINTS == 1:
        print("\n\nFim da execução")
        print("Duração: " + str(duracao))