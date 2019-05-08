import Arquivo
import json
import requests


def auth(client_id='Z9dXSGAyLhQ884F8', client_secret='33c36d02693249b0a8865bf48ae1a1d1'):
    url = "https://www.arcgis.com/sharing/rest/oauth2/token"
    payload = "client_id=" + client_id + "&client_secret=" + client_secret + "&grant_type=client_credentials"
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'accept': "application/json",
        'cache-control': "no-cache",
        'postman-token': "11df29d1-17d3-c58c-565f-2ca4092ddf5f"
    }
    response = requests.request("POST", url, data=payload, headers=headers)


def endereco(ocorencia):
    end = ocorencia.get('local')
    if end != '':
        end += ',+'
    end += ocorencia.get('bairro') + ',+' + ocorencia.get('municipio')
    end = end.replace(' ', '+')
    return end


def url_json(end):
    try:
        url = 'https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates'
        params = {'f': 'json', 'outFields': 'address', 'singleLine': end}

        json_response = requests.get(url=url, params=params)
        if json_response.status_code == 200:
            json_str = json_response.text
            result = json.loads(json_str)
            if len(result['candidates']) > 0:
                result['status'] = 'OK'
            else:
                result['status'] = 'ZERO_RESULTS'
            result['source'] = 'ArcGIS'
            print(end + '\tStatus: ', result.get('status'), end=' ')
        else:
            result = None
        print('RESPONSE: ', json_response.status_code)
    except:
        result = None
    return result


def status(lista_enderecos, boletim_json):
    print('Total de endereços:', len(lista_enderecos))
    status_dict = {}
    for key in lista_enderecos:
        status_key = lista_enderecos[key].get('status')
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
    boletim_dir = 'B/B03/boletim.json'
    boletim_json = Arquivo.json(entrada + boletim_dir)
    lst = list()
    lista_enderecos = Arquivo.json('enderecos_coordenadas.json')
    status(lista_enderecos, boletim_json)
    count = 10

    print('Iniciando o processo de conversão ...')
    for ocorencia in boletim_json:
        end = endereco(ocorencia)
        end_status = lista_enderecos.get(end)
        if end is None or end_status is None or end_status.get('status') == 'OVER_QUERY_LIMIT':
            result = url_json(end)
            if result is not None:

                if result.get('status') == 'OVER_QUERY_LIMIT':
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





















































