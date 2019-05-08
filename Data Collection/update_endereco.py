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
        json_web = urlopen(url)
        json_byte = json_web.read()
        json_str = json_byte.decode()
        result = json.loads(json_str)
    except:
        result = None
    return result


def main():
    end = Arquivo.json('enderecos_coordenadas.json')
    OQL = 0
    OK = 0
    ZR = 0
    CV = 0
    TOT = len(end)
    i = 0
    for key in end:
        i += 1
        print("%.2f%%" %(float(i/TOT) * 100))
        if end[key].get('status') == 'OVER_QUERY_LIMIT':
            CV += 1
            end[key] = url_json(key)
            if end[key].get('status') == 'OVER_QUERY_LIMIT':
                OQL += 1
            elif end[key].get('status') == 'OK':
                OK += 1
            else:
                ZR += 1
        elif end[key].get('status') == 'OK':
            OK += 1
        else:
            ZR += 1
    print("Total ", TOT, "Convertidos ", CV, '\nOK: ', OK, 'Zero Results: ', ZR, 'QOV: ', OQL)
    Arquivo.escrever_json('enderecos_coordenadas.json', end)


if __name__ == '__main__':
    main()