import os
from arquivos_locais import FONTE_DADOS, MOSTRAR_PRINTS, FONTE_DADOS_IMAGES
import re 

# --------------------------------------------------

def recupera_lista_arquivos():

    arquivos_para_import = []

    print("Iterando por arquivos para import")

    for diretorio, subpastas, arquivos in os.walk(os.path.dirname(__file__) + FONTE_DADOS):
        for arquivo in arquivos:
            print(os.path.join(diretorio, arquivo))
            arquivos_para_import.append(os.path.join(diretorio, arquivo))

    if MOSTRAR_PRINTS == 1:
        print("Lista de arquivos")
        print(arquivos_para_import)
    
    return arquivos_para_import

# --------------------------------------------------

def recupera_lista_imagens():

    arquivos_para_import = []

    print("Iterando por arquivos para import")

    for diretorio, subpastas, arquivos in os.walk(os.path.dirname(__file__) + FONTE_DADOS_IMAGES):
        for arquivo in arquivos:
            
            if ".DS_Store" not in str(os.path.join(diretorio, arquivo)):
                
                if MOSTRAR_PRINTS == 1:
                    print(os.path.join(diretorio, arquivo))
                
                # descricao da especie é tudo que vem depois de "fonte_dados_coleta_imagens"
                
                nome = re.search(r'^\w{1,} \w{1,}', arquivo)
                nome = str(nome.group(0))

                identificador = str(abs(hash(os.path.join(diretorio, arquivo))) % (10 ** 4)).zfill(4)

                descricao_especie =  os.path.dirname(os.path.join(diretorio, arquivo))

                caminho_absoluto = str(os.path.join(diretorio, arquivo))

                caminho_relativo = re.search(r'\/fonte_dados_coleta_imagens.{1,}', caminho_absoluto)
                caminho_relativo = str(caminho_relativo.group(0))

                if "Misc" not in descricao_especie:
                    
                    if MOSTRAR_PRINTS == 1:
                        print("Isso não vem da pasta 'misc'")
                    
                    # estrutura da string
                    # x/y/z/fonte_de_dados_coleta_imagens/familia/subfamilia
                    # extrair familia e subfamilia (pode ser que não tenha subfamilia)
                    
                    resultado_descricao_especie = re.sub(r'.{1,}\/fonte_dados_coleta_imagens', '', descricao_especie)
                    
                    resultado_descricao_especie = str(re.sub(r'\/', ' ', resultado_descricao_especie))
                    resultado_descricao_especie = re.sub(r'^ ', '', resultado_descricao_especie)
                    
                    familia = re.search(r'^\w{1,}', resultado_descricao_especie)
                    familia_nome = str(familia.group(0))

                    sub_familia_nome = str(re.sub(r'^\w{1,} ', '', resultado_descricao_especie))
                    
                    if MOSTRAR_PRINTS == 1:
                        print("\n\n")
                        print(familia_nome)
                        print(sub_familia_nome)

                else:

                    if MOSTRAR_PRINTS == 1:
                        print("Isso vem da pasta 'misc'")
                    # estrutura da string
                    # x/y/z/fonte_de_dados_coleta_imagens/misc/familia/subfamilia
                    # extrair familia e subfamilia (pode ser que não tenha subfamilia)

                    resultado_descricao_especie = re.sub(r'.{1,}\/fonte_dados_coleta_imagens/Misc', '', descricao_especie)
                    
                    resultado_descricao_especie = str(re.sub(r'\/', ' ', resultado_descricao_especie))
                    resultado_descricao_especie = re.sub(r'^ ', '', resultado_descricao_especie)
                    
                    familia = re.search(r'^\w{1,}', resultado_descricao_especie)
                    familia_nome = str(familia.group(0))

                    sub_familia_nome = str(re.sub(r'^\w{1,} ', '', resultado_descricao_especie))
                    
                    if MOSTRAR_PRINTS == 1:
                        print("\n\n")
                        print(familia_nome)
                        print(sub_familia_nome)

                arquivos_para_import.append([identificador, nome, str(arquivo), caminho_absoluto, caminho_relativo, familia_nome, sub_familia_nome])

    if MOSTRAR_PRINTS == 1:
        print("Lista de arquivos")
        print(arquivos_para_import)
    
    return arquivos_para_import

# --------------------------------------------------
