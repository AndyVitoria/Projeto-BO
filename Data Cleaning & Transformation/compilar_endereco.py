import pdf2txt
import Arquivo
import json

def main():
    lote = 'lote.txt'
    json_dir = 'JSON'
    JSON = pdf2txt.Diretorio(json_dir)
    JSON.listar(lote)
    pastas = Arquivo.abrir(json_dir + '/' + lote)[:-1]
    enderecos = list()
    for pasta in pastas:
        print("Abrindo " + pasta)
        arquivo = json_dir + '/' + pasta + '/' + pasta + '.json'
        arq = open(arquivo, 'rt', encoding='cp1252')
        boletins = json.load(arq)
        for boletim in boletins:
            end = boletim.get('local')
            if end != '':
                end += ', '
            end += boletim.get('bairro') + ', ' + boletim.get('municipio')
            if not end in enderecos:
                enderecos.append(end)
    enderecos.sort()
    print("Salvando")
    Arquivo.sobrescrever('enderecos.txt', enderecos)
    return


if __name__ == '__main__':
    main()