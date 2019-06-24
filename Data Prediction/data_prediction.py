import pandas as pd
import numpy as np
from datetime import date, timedelta
from m4competition import m4_predict


def data_preparation(df, start_date, end_date):
    # Verifica se os ados cobre todos os dias do periodo selecionado
    range_date = (end_date - start_date).days + 1
    if df.data.size == range_date:
        return df.label.values

    # Caso não cubra, preenche os dados faltando com 0
    data = list()
    #temp_date = start_date
    for i in range(range_date):
        temp_date = start_date + timedelta(days=i)
        temp = df[df.data == temp_date.__str__()].label.values

        if temp.size == 0:
            data.append(0)
        else:
            data.append(temp[0])
        #print(temp, temp_date)

    return np.array(data)


def load_train_test_validation(df_dir, df_base_name):
    df_test = pd.read_csv(df_dir + df_base_name + '_test_daily.csv')
    df_validation = pd.read_csv(df_dir + df_base_name + '_validation_daily.csv')
    df_train = pd.read_csv(df_dir + df_base_name + '_train_daily.csv')
    return df_train, df_test, df_validation


def main():
    # Variáveis do M4
    fh = 15  # forecasting horizon
    freq = 3  # data frequency
    in_size = 30  # number of points used as input for each forecast

    # Variáveis  da predição
    day_freq = 7
    num_prediction = 5

    # Lista de técnicas utilizadas
    prediction_tec_name = ['RNN_BENCH']

    # Variáveis do diretório dos dataframes
    df_base_name = 'dataframe_03'
    df_dir = '../Data Cleaning & Transformation/DATAFRAME/DF_01/'

    # Datas de filtragem dos dados
    start_validation_date = date(2018, 1, 1)
    end_validation_date = date(2018, 12, 31)
    start_train_date = date(2013, 1, 1)
    end_train_date = date(2017, 12, 31)


    print("\n\nCAREGANDO DADOS")
    df_train, df_test, df_validation = load_train_test_validation(df_dir, df_base_name)

    df_train = pd.concat([df_train, df_test])

    RMGV = df_train.municipio.unique()

    data_validation = list()
    data_all = list()

    print("\n\nPREPROCESSANDO OS DADOS")
    for m in RMGV:
        data_all.append(data_preparation(df_train[df_train.municipio == m], start_train_date, end_train_date))
        data_validation.append(data_preparation(df_validation[df_validation.municipio == m], start_validation_date, end_validation_date))

    data_all_clean = data_all.copy()

    print("\n\nCONSTRUINDO DATAFRAME COM OS RESULTADOS")
    prediction_dataframe_values = list()

    for pred_name in prediction_tec_name:
        print("\n\nTREINANDO O MODELO:", pred_name)
        data_all = data_all_clean

        for n in range(num_prediction):
            print("\n\nTREINANDO O MODELO E PREVENDO OS DADOS PARA O DIA:", n+1)
            data_all = np.array(data_all)
            data_prediction, smape_list, mase_list = m4_predict(data_all, in_size, freq, fh)

            for i in range(len(data_prediction)):
                for j in range(data_prediction[i].size):
                    prediction_date = (start_validation_date + timedelta(weeks=n, days=-1)).__str__()
                    prediction_day = (start_validation_date + timedelta(weeks=n, days=j)).__str__()
                    prediction_dataframe_values.append([prediction_day, int(data_prediction[i][j]), data_validation[i][(n*day_freq)+j], RMGV[i], prediction_date, pred_name])

            data_all = list(data_all)
            for i in range(len(data_all)):
                data_all[i] = np.append(data_all[i], data_validation[i][n*day_freq: (n+1)*day_freq])

    df_prediction = pd.DataFrame(prediction_dataframe_values, columns=['dia', 'value', 'real', 'municipio', 'prediction_date', 'method'])
    df_prediction = df_prediction.set_index('prediction_date')

    print("\n\nSALVANDO RESULTADOS")
    df_prediction.to_csv(df_dir + df_base_name + '_prediction_weekly.csv')


if __name__ == '__main__':
    main()
