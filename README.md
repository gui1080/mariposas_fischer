## Banco de dados do Fischer

Resumindo: pegou-se tudo que o Fischer tinha catalogado por meio de imagens e arquivo de coleta, e se botou num Banco de Dados SQLite. A estrutura de pasta de imagens representa uma estrutura que descreve família/genero de uma dada espécie, e o arquivo ".xlsx" são as coletas do foco dos estudos, as "Acharias". 

## Fonte de dados

Esses dados são privados e pertencem ao Guilherme Fischer, mas a estrutura dos dados é descrita a baixo.

```

.
└── fonte_dados_coleta_imagens/
    ├── Choreutidae/
    │   └── ...
    ├── Hepialidae/
    │   └── ...
    ├── Misc/
    │   └── ...
    ├── Noctuidae/
    │   └── ...
    ├── Tineoidea/
    │   └── ...
    └── Zygaenoidea/
        ├── Limacodidae/
        │   └── Acharia/
        │       └── ...
        └── ...

.
└── fonte_dados_coleta/
    ├── acharia.xlsx

```

#### O arquivo da coleta apresenta a seguinte estrutura

```
    Inst. Bar Code
    Genus
    Species
    Author
    Sex
    number of spec
    Museum/Coll
    Country
    Province
    Locality
    date
    collector
    type #
    accession #
    Lat. <span style="font-family: Arial;font-size: 13px;">o</span>
    Lat. '
    Lat. "
    Lat. Hem.
    Long. <span style="font-family: Arial;font-size: 13px;">o</span>
    Long. '
    Long. "
    Long. Hem.
```

## Execução do script

Instalar dependências:

> pip3 install -r requirements.txt 

Rodar:

> python3 main.py

Repositório: https://github.com/gui1080/mariposas_fischer

Autor: Guilherme Braga

```
/*
 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * Guilherme Braga Pinto wrote this file, and also other Python scripts in this repository.  As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return.   Poul-Henning Kamp
 * ----------------------------------------------------------------------------
 */
 ```
