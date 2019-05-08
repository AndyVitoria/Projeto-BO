import Arquivo
from Acentos import remover_acentos
import json
from urllib.request import urlopen

def main():
    boletins = Arquivo.json('MAPEADOS/A/boletim.json')
    json_marker = dict()
    for boletim in boletins:
        if boletim.get('geocode').get('status') == 'OK':
            marker = dict()
            marker['codigo'] = boletim.get('codigo')
            data_hora = boletim.get('data')
            marker['data'] = ''
            marker['hora'] = ''
            print(data_hora)
            if len(data_hora) != 0:
                marker['data'] = data_hora[0]
                marker['hora'] = data_hora[1]
            registro = boletim.get('registrado')
            marker['data_registro'] = registro[0]
            marker['hora_registro'] = registro[1]
            geocode = boletim.get('geocode').get('results')

            for key in geocode[0]:
                elem = geocode[0][key]
                if key == "address_components":
                    for dados in elem:
                        if dados.get('types')[0] == 'route':
                            marker['rua'] = dados.get('short_name')
                        elif 'sublocality' in dados.get('types'):
                            marker['bairro'] = dados.get('long_name')
                        elif 'administrative_area_level_2' in dados.get('types'):
                            marker['municipio'] = dados.get('long_name')
                        elif 'administrative_area_level_1' in dados.get('types'):
                            marker['estado'] = dados.get('short_name')
                        elif 'country' in dados.get('types'):
                            marker['pais'] = dados.get('short_name')
                elif key == "formatted_address":
                    marker['endereco'] = elem
                elif key == "geometry":
                    local = elem.get("location")
                    marker['lat'] = local.get('lat')
                    marker['lng'] = local.get('lng')
        json_marker[boletim.get('id')] = marker
    Arquivo.escrever_json('MARCADOR/A.json', {"boletim": json_marker}, encoding="utf8")
    return


if __name__ == '__main__':
    main()

