from pdf2txt import Diretorio, Windows, Linux
import Arquivo
from Acentos import remover_acentos
import json
from urllib.request import urlopen

def endereco(ocorencia):
    end = ocorencia.get('local')
    if end != '':
        end += ',+'
    end += ocorencia.get('bairro') + ',+' + ocorencia.get('municipio')
    end = end.replace(' ', '+')
    return end

def url_json(end):
    try:
        url = 'http://maps.google.com/maps/api/geocode/json?address=' + remover_acentos(end) + '&sensor=false'
        print(url)
        json_web = urlopen(url)
        json_byte = json_web.read()
        json_str = json_byte.decode()
        result = json.loads(json_str)
        print(end + '\tStatus: ', result.__getitem__('status'))
    except:
        result = None
    return result


def status(lista_enderecos, boletim_json):
    print('Total de endereços:', len(lista_enderecos))
    status_dict = {}
    for key in lista_enderecos:
        status_key = lista_enderecos[key].__getitem__('status')
        if status_key in status_dict:
            status_dict[status_key] += 1
        else:
            status_dict[status_key] = 1
    for status_key in status_dict:
        print('\t' + status_key + ':', status_dict[status_key])

    print('Total de Boletins: ', len(boletim_json))


def main():
    entrada = 'BOLETIM/'
    saida = 'MAPEADOS/'
    boletim_dir = 'B/B01/boletim.json'
    boletim_json = Arquivo.json(entrada + boletim_dir)
    lst = list()
    lista_enderecos = Arquivo.json('enderecos_coordenadas.json')
    status(lista_enderecos, boletim_json)
    count = 10

    print('Iniciando o processo de conversão ...')
    for ocorencia in boletim_json:
        end = endereco(ocorencia)
        end_status = lista_enderecos.__getitem__(end)
        if end is None or end_status.__getitem__('status') == 'OVER_QUERY_LIMIT':
            result = url_json(end)
            if result is not None:

                if result.__getitem__('status') == 'OVER_QUERY_LIMIT':
                    count -= 1
                    if count < 1:
                        break
                else:
                    count = 10

                lista_enderecos.__setitem__(end, result)

        else:
            result = lista_enderecos.get(end)
        if result is not None:
            ocorencia.__setitem__('geocode', result)
            lst.append(ocorencia)

    Arquivo.escrever_json(saida + boletim_dir, lst)
    Arquivo.escrever_json('enderecos_coordenadas.json', lista_enderecos)

    return


if __name__ == '__main__':
    main()





















































