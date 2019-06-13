from pdf2txt import pdf2txt
from txt2json import txt2json
from json2cat import json2cat
from end2cord import end2cord

def main():
    # Definição das informações dos diretórios

    # Nome do arquivo contendo o nome dos lotes (subpastas) de cada etapa
    lote = 'lote.txt'
    # Nome do diretório dos boletins armazenados em PDF
    pdf_dir = 'PDF'
    # Nome do diretório dos boletins convertidos em TXT
    csv_dir = 'TXT'
    # Nome do diretório dos lotes compilados em JSON
    json_dir = 'JSON'
    # Nome do diretório das Categorias dos boletins
    cat_dir = 'BOLETIM'
    # Nome do diretório dos boletins mapeados geograficamente
    geo_dir = 'MAPEADOS'

    # Caminho da categoria que será mapeada geograficamente
    boletim_cat = 'B/B01/boletim.json'

    print("\n\nCONVERTENDO OS BOLETINS DE PDF PARA TXT")
    pdf2txt(lote=lote, pdf_dir=pdf_dir, csv_dir=csv_dir)

    print("\n\nCOMPILANDO OS BOLETINS EM TXT EM JSON")
    txt2json(lote=lote, csv_dir=csv_dir, json_dir=json_dir)

    print("\n\nSEGMENTANDO OS BOLETINS POR CATEGORIA")
    json2cat(lote=lote, json_dir=json_dir, cat_dir=cat_dir)

    print("\n\nMAPEANDO GEOGRAFICAMENTE OS BOLETINS DA CATEGORIA SELECIONADA")
    end2cord(boletim_dir=boletim_cat, entrada=cat_dir, saida=geo_dir)

    return


if __name__ == '__main__':
    main()
