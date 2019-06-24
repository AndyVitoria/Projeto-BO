# Passo a Passo de execução

## Estrutura de Pastas

O sistema é dividido em etapas, e os resultados de cada etapa são armazenados em sub-pastas. Para criar as pastas necessárias para execução do Projeto basta executar o arquivo **'build_folder'**:

Windows:
    
    > build_folder.bat
    
Linux:
    
    $ ./build_folder.sh

## Funções

### pdf2txt
Converte os boletins de ocorrência em PDF para TXT.
```python
    pdf2txt(lote='lote.txt', pdf_dir='PDF', csv_dir='TXT')
```
**lote**: Nome do arquivo contendo o nome dos lotes (subpastas) de cada etapa. Default: **'lote.txt'**

**pdf_dir**: Nome do diretório dos boletins armazenados em PDF. Default: **'PDF'**

**csv_dir**: Nome do diretório dos boletins convertidos em TXT. Default: **'TXT'**


### txt2json
Extrai os campos dos arquivos em TXT e compila-os em JSON, subdividindo por lote.
```python
    txt2json(lote='lote.txt', csv_dir='TXT', json_dir='JSON')
```
**lote**: Nome do arquivo contendo o nome dos lotes (subpastas) de cada etapa. Default: **'lote.txt'**

**csv_dir**: Nome do diretório dos boletins convertidos em TXT. Default: **'TXT'**

**json_dir**: Nome do diretório dos boletins armazenados e compilados em JSON. Default: **'JSON'**


### json2cat
Seguimenta e armazena os boletins de ocorrecia de todos os lotes do diretórios especificado por categoria.
```python
    json2cat(lote=lote, json_dir=json_dir, cat_dir=cat_dir)
```
**lote**: Nome do arquivo contendo o nome dos lotes (subpastas) de cada etapa. Default: **'lote.txt'**

**json_dir**: Nome do diretório dos boletins armazenados e compilados em JSON. Default: **'JSON'**

**cat_dir**: Nome do diretório dos boletins seguimentados por categoria. Default: **'BOLETIM'**


### end2cord
Converte os endereços dos boletins para coordenadas geográficas.
```python
    end2cord(boletim_dir=boletim_dir, entrada=cat_dir, saida=geo_dir)
```
**entrada**: Nome do diretório de categorias. Default: **'BOLETIM'**

**saida**: Nome do diretório de saida dos boletins geomapeados. Default: **'MAPEADOS'**

**boletim_dir**: Caminho das subspastas de categoria, contendo o nome do arquivo contendo os boletins compilados em JSON. Default: **None**

### cord2dataframe
Converte os boletins de ocorrência, especificamentes os de categoria B01 e B02, para o formato de DataFrame da biblioteca Pandas. Seguimentando em DataFrame para o Microsoft Power BI, e os DataFrames de Treino, Teste e Validação das Redes Neurais.
```python
    cord2dataframe(b01_dir='MAPEADOS/B/B01/boletim.json', b02_dir='MAPEADOS/B/B02/boletim.json', dataframe_name = 'DATAFRAME/DF_01/dataframe_01')
```

**b01_dir**: Caminho até o arquivo contendo os boletins de categoria B01. Default: **'MAPEADOS/B/B01/boletim.json'**

**b02_dir**: Caminho até o arquivo contendo os boletins de categoria B02. Default: **'MAPEADOS/B/B02/boletim.json'**

**dataframe_name**: Caminho contendo o nome base que será usando nos dataframes. Default: **'DATAFRAME/DF_01/dataframe_01'**

