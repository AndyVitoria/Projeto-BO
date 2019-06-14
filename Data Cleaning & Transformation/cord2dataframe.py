import pandas as pd
from datetime import datetime

RMGV = ['CARIACICA', 'FUNDAO', 'GUARAPARI', 'SERRA', 'VIANA', 'VILA VELHA', 'VITORIA']    

def load_bo(b01_dir, b02_dir, RMGV):

    b01 = pd.read_json(b01_dir)
    b01 = b01[b01.municipio.isin(RMGV)]
    b01 = b01.set_index('id')

    b02 = pd.read_json(b02_dir)
    b02 = b02[b02.municipio.isin(RMGV)]
    b02 = b02.set_index('id')

    df = pd.concat([b01, b02])
    del(b01)
    del(b02)
    return df


def split_datetime(df):
    data = df.data.values

    hora = []

    for i in range(data.size):
        if len(data[i]) > 0:
            temp = datetime.strptime(' '.join(data[i]), '%d/%m/%Y %H:%M')
            data[i] = temp.date()
            hora.append(temp.time())
        else:
            data[i] = ''
            hora.append('')
    df['hora'] = hora
    return df


def date_filter(df):
    df = df[df.data != '']
    start_date = datetime.strptime('31/12/2012', '%d/%m/%Y').date()
    final_date = datetime.strptime('01/01/2019', '%d/%m/%Y').date()
    df = df[(df.data > start_date) & (df.data < final_date)]
    return df


def check_bo_inside_es(x,y):
    es_geo = {'x':(-41.8, -39.0), 'y': (-21.0, -17.9)}
    return (es_geo['x'][0] <= x <= es_geo['x'][1]) and (es_geo['y'][0] <= y <= es_geo['y'][1])


def get_cord_inside_br(candidates):
    i = 0
    for addr in candidates:
        if check_bo_inside_es(addr.get('location').get('x'), addr.get('location').get('y')):
            break
        else:
            i += 1
    
    if i == len(candidates):
        i = 0
        
    addr = candidates[i]
    
    return addr


def google_to_arcgis(result):
    if len(result) == 0:
        return None
    i = 0
    
    for addr in result:
        if addr.get('geometry').get('location').get('lng') < 0 and addr.get('geometry').get('location').get('lat') < 0:
            break
        else:
            i += 1
    
    if i == len(result):
        i = 0
        
    addr = result[i]
    
    if 'bounds' in addr.get('geometry').keys():
        arcgis = {
            'address': addr.get('formatted_address'),
            'location': {
                'x': addr.get('geometry').get('location').get('lng'),
                'y': addr.get('geometry').get('location').get('lat')
            },
          'score': -1,
          'attributes': {
              'address': addr.get('address_components')[0].get('long_name')
          },
          'extent': {
              'xmin': addr.get('geometry').get('bounds').get('southwest').get('lng'),
              'ymin': addr.get('geometry').get('bounds').get('southwest').get('lat'),
              'xmax': addr.get('geometry').get('bounds').get('northeast').get('lng'),
              'ymax': addr.get('geometry').get('bounds').get('northeast').get('lat')
          }
        }
    else:
        arcgis = {'address': addr.get('formatted_address'),
          'location': {'x': addr.get('geometry').get('location').get('lng'), 'y': addr.get('geometry').get('location').get('lat')},
          'score': -1,
          'attributes': {'address': addr.get('address_components')[0].get('long_name')},
          'extent': {
              'xmin': addr.get('geometry').get('viewport').get('southwest').get('lng'),
              'ymin': addr.get('geometry').get('viewport').get('southwest').get('lat'),
              'xmax': addr.get('geometry').get('viewport').get('northeast').get('lng'),
              'ymax': addr.get('geometry').get('viewport').get('northeast').get('lat')
          }
        }
    return arcgis


def geocode_filter(df):
    # Building the Geocode Structure
    geocode = {
        'address': list(),
        'x': list(),
        'y': list(),
        'xmin': list(), 
        'ymin': list(),
        'xmax': list(),
        'ymax': list()
    }

    for row in df.geocode.values:
        # Verify if the source is Google Maps, ArcGIS or the address could not be Geolocated
        if row.get('source') == 'Google Maps' and row.get('results') is not None:
            candidate = google_to_arcgis(row.get('results'))
        elif row.get('source') == 'ArcGIS':
            candidate = get_cord_inside_br(row.get('candidates'))
        else:
            candidate = {'address': '', 'location': {'x': '', 'y': ''}, 'extent': {'xmin': '', 'ymin': '', 'xmax': '', 'ymax': ''}}
        
        # Add the result in the Geocode Structure
        geocode['address'].append(candidate.get('address'))
        geocode['x'].append(candidate.get('location').get('x'))
        geocode['y'].append(candidate.get('location').get('y'))
        geocode['xmin'].append(candidate.get('extent').get('xmin'))
        geocode['xmax'].append(candidate.get('extent').get('xmax'))
        geocode['ymin'].append(candidate.get('extent').get('ymin'))
        geocode['ymax'].append(candidate.get('extent').get('ymax'))

    # Add the Geocode Structure inside the DataFrame
    df['address'] = geocode['address']
    df['x'] = geocode['x']
    df['y'] = geocode['y']
    df['xmin'] = geocode['xmin']
    df['xmax'] = geocode['xmax']
    df['ymin'] = geocode['ymin']
    df['ymax'] = geocode['ymax']

    return df


def drop_columns(df):
    df.pop('item')
    df.pop('referencia')
    df.pop('tipo_de_local')
    df.pop('registrado')
    df.pop('geocode')
    df.pop('descricao')
    df.pop('complemento')
    df.pop('local')
    df.pop('codigo')
    df.pop('address')
    df.pop('x')
    df.pop('y')
    df.pop('xmin')
    df.pop('xmax')
    df.pop('ymin')
    df.pop('ymax')
    df.pop('bairro')
    df.pop('hora')


def reorganize_dataframe(df):
    df= df.sort_values(by=['data'])
    label = [1] * df.data.size
    df['label'] = label
    df.data = pd.to_datetime(df.data)
    df = df.groupby(['data', 'municipio']).count()
    return df


def reorganize_dataframe_index(df):
    df['municipio'] = df.index.get_level_values('municipio')
    df = df.reset_index(level=1, drop=True)
    df = df.sort_index()
    return df


def split_train_test_validation(df, dataframe_name):
    df_validation = df[df.index.year == 2018]
    df_test =  df[df.index.year == 2017]
    df_train =  df[df.index.year < 2017]

    df_train.to_csv(dataframe_name + '_train' + '_daily.csv')
    df_test.to_csv(dataframe_name + '_test' + '_daily.csv')
    df_validation.to_csv(dataframe_name + '_validation' + '_daily.csv')


def cord2dataframe(b01_dir, b02_dir, dataframe_name):
    print("Carregando dados")
    # Load the data
    df = load_bo(b01_dir,b02_dir, RMGV)
    
    print("Aplicando filtros")
    # Filter based on the data datetime
    df = split_datetime(df) 
    df = date_filter(df)

    # Filter based on the data geocode
    df = geocode_filter(df)

    print("Gerando DataFame para o Power BI")
    # Save the DataFrame that will be used in Power BI
    df.to_csv(dataframe_name + '_pbi.csv')

    print("Gerando DataFrame para Redes Neurais")
    # Start to build the DataFrame that will be used in the prediction model
    drop_columns(df)

    df = reorganize_dataframe(df)

    # Checkpoint with the data splited daily
    df.to_csv(dataframe_name + '_daily.csv')

    df = reorganize_dataframe_index(df)
    print("Salvando dados de Treino, Teste e Validação")
    # Split the data into Train, Test and Validation
    split_train_test_validation(df, dataframe_name)


def main():
    cord2dataframe(b01_dir='MAPEADOS/B/B01/boletim.json', b02_dir='MAPEADOS/B/B02/boletim.json', dataframe_name = 'DATAFRAME/DF_01/dataframe_01')
