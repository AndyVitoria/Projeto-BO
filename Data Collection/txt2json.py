from unicodedata import normalize
import Arquivo
import pdf2txt
import json
import re
import threading


# Verifica se existe uma lista de municipios do estado do Espírito Santo restringindo a conversão
try:
    MUNICIPIO = Arquivo.abrir('lista_municipios.txt')
except:
    MUNICIPIO = list()

# Numero de Threads a serem utilizados
THREAD_NUM = 12

THREAD_CONTROL = [True] * THREAD_NUM


class Conversor(threading.Thread):
    def __init__(self, entrada, saida, pasta, lote, ID):
        threading.Thread.__init__(self)
        self.pasta = pasta
        self.lote = lote
        self.dir = pdf2txt.Diretorio('')
        self.dir.dir = self.dir.concatena(dir1=entrada, dir2=pasta)
        self.entrada = entrada
        self.saida = saida
        self.ID = ID

    def run(self):
        # Lista os arquivos dentro do diretorio
        self.dir.listar(self.lote)

        try:
            buffer = list()
            buffer.append('[')
            arquivos = Arquivo.abrir(self.entrada + '/' + self.pasta + '/' + self.lote)[:-1]
            print("Conversão de CSV no diretorio " + self.pasta)
            print("Adicionando ao buffer")
            count = 0
            tot = len(arquivos)
            for arq in arquivos:
                count += 1
                if tot % count == 0:
                    print("%s -> %.1f%%" % (super().name, 100*count/tot))
                try:
                    csv = Arquivo.abrir(self.entrada + '/' + self.pasta + '/' + arq)

                    boletim = Boletim(csv, id_boletim=int(arq[:-4]))
                    if boletim.valido:
                        buffer.append(boletim.json() + ',')

                except ValueError:
                    # Em caso de erro gera um arquivo de log com o nome dos arquivos e o erro gerado.
                    print(ValueError)
                    print("Nao foi possivel converter o arquivo " + self.pasta + '/' + arq)
                    Arquivo.escrever('Log_Erro.txt',
                                     ['Erro ao converter o diretorio ' + self.pasta + '/' + arq, "-- " + ValueError.__str__()])

            buffer[-1] = buffer[-1][:-1]
            buffer.append(']')
            print('Salvando lote: ' + self.pasta)
            Arquivo.sobrescrever(self.saida + '/' + self.pasta + '/' + self.pasta + '.json', buffer)
            THREAD_CONTROL[self.ID] = True
        except ValueError:
            print(ValueError)
            print("Nao foi possivel converter o diretorio " + self.pasta)
            Arquivo.escrever('Log_Erro.txt', ['Erro ao converter o diretorio ' + self.pasta, "-- " + ValueError.__str__()])
        return 0


def get_next(i, boletim):
    i+= 1
    while i < len(boletim) and boletim[i] == '':
        i += 1

    if i < len(boletim):
        return i, boletim[i]
    else:
        return i, ''


def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII','ignore').decode('ASCII')


class Boletim(object):
    def __init__(self, boletim, id_boletim=None):
        self.valido = True
        self.registrado = list()
        self.data = list()
        self.codigo = ''
        self.descricao = ''
        self.tipo_de_local = ''
        self.local = ''
        self.complemento = ''
        self.bairro = ''
        self.municipio = ''
        self.referencia = ''
        self.item = dict()
        self.erro = ''
        check = True
        try:
            if id_boletim is None:
                self.id = int(boletim[2])
            else:
                self.id = id_boletim
            for linha in boletim:
                if len(linha) > 7:
                    self.valido = linha[:8] != 'INVÁLIDO'
                    if not self.valido:
                        self.erro = ' - INVÁLIDO'
                        return
        except Exception as e:
            self.valido = False
            self.erro = ' - ' + str(e)
            return
        i = 0
        while check:
            i, linha = get_next(i, boletim)
            if linha != '':
                cmp = linha.lower()

                if 'registrado em' in cmp:
                    info = linha.split(' ')
                    for elem in info:
                        if '/' in elem or ':' in elem:
                            self.registrado.append(elem)

                elif 'tipo de local' == cmp:
                    i, linha = get_next(i, boletim)
                    if self.valida_string_upper(linha):
                        self.tipo_de_local = linha

                elif 'evento' == cmp:
                    i, linha = get_next(i, boletim)
                    data = linha.split(' ')
                    if len(data) == 2 and '/' in data[0]:
                        self.data = data
                    else:
                        i -= 1

                elif 'incidente inicial' in cmp:
                    
                    i, linha = get_next(i, boletim)
                    if ' ' in linha:
                        self.codigo = linha.split(' ')[0]
                        self.descricao = linha[len(self.codigo):]

                    else:
                        self.codigo = linha
                        i, linha = get_next(i, boletim)
                        self.descricao = linha

                elif 'local (' in cmp:
                    
                    i, linha = get_next(i, boletim)
                    if linha != 'Bairro':
                        end = linha.split(',')[0].split('-')[0]
                        if len(end) != len(linha):
                            local = linha[:len(end)]
                            self.complemento = linha[len(end):]
                        else:
                            local = linha

                        if not (len(local) == 1 or'XXXX' in local[:5] or 'ZZZ' in local[:5] or 'UUU' in local[:6] or 'VVV' in local[:7] or ('00' == local[:2] and '1' != local[-1])):
                            self.local = self.remove_caracteres_especiais(local)
                        if len(self.local) >= 1 and self.local[0] == ' ':
                            self.local = self.local[1:]

                    else:
                        i -= 1
                elif 'bairro' == cmp:
                    
                    i, linha = get_next(i, boletim)
                    if linha == 'Municipio':
                        i -= 1
                    else:
                        self.bairro = linha
                        if self.municipio == '':
                            i, linha = get_next(i, boletim)
                            if linha != 'CEP' and self.valida_string_upper(linha):
                                self.municipio = linha
                            else:
                                i -= 1

                elif 'municipio' == remover_acentos(cmp):

                    i, linha = get_next(i, boletim)
                    if self.valida_string_upper(linha):
                        if self.municipio == '' or not self.municipio in MUNICIPIO:
                            self.municipio = linha

                    if not self.valida_string(self.bairro):
                        municipio = self.municipio
                        lst = municipio.split(' ')
                        bairro = lst[0]
                        count = len(bairro) + 1
                        del(lst[0])
                        while len(lst) != 0 and not municipio[count:] in MUNICIPIO:
                            bairro += ' ' + lst[0]
                            count += len(lst[0]) + 1
                            del (lst[0])
                        if len(lst) != 0:
                            self.bairro = bairro
                            self.municipio = municipio[count:]
                elif 'ponto de ref' in cmp:
                    
                    i, linha = get_next(i, boletim)
                    if self.valida_string_upper(linha):
                        self.referencia = linha
                    else:
                        i -= 1
                elif 'objetos relacionados' == cmp:
                    i, linha = get_next(i, boletim)

                    while 'Tipo' != linha[:4]:
                        i, linha = get_next(i, boletim)
                    lst_item = list(filter(None, boletim[i:-2]))
                    key_word = ['Item', 'Tipo de Objeto', 'Tipo de Ação', 'Quantidade']
                    for word in key_word:
                        try:
                            lst_item.remove(word)
                        except:
                            pass
                    try:
                        count = 1
                        temp = list()
                        for item in lst_item:
                            if item.isdigit():
                                temp.append(item)
                                self.item[count] = temp
                                temp = list()
                                count += 1
                            else:
                                temp.append(item)
                    except ValueError:
                        print(ValueError)
                        print(self.id)
            else:
                check = False
        try:
            bairro = self.valida_string_upper(self.bairro)
            municipio = self.valida_string_upper(self.municipio)
            if not (bairro and municipio):
                self.valido = False
                self.erro = ' - Endrereco'

        except:
            self.valido = False
            self.erro = ' - Desconhecido'

    def valida_string_upper(self, valor):
        try:
            verificador = re.match('[A-Z ]+', remover_acentos(valor))
            return not (verificador is None or verificador.end() != len(valor))
        except:
            return False

    def remove_caracteres_especiais(self, string):
        return str().join(re.split('[^a-z A-Z0-9]+', remover_acentos(string)))


    def check(self):
        if self.municipio not in MUNICIPIO:
            print(self.id)
            print(self.municipio)

    def valida_string(self, valor):
        try:
            verificador = re.match('[a-z A-Z]+', remover_acentos(valor))
            return not (verificador is None or verificador.end() != len(valor))
        except:
            return False

    def valida_string_num(self, valor):
        try:
            verificador = re.match('[a-z A-Z0-9]+', remover_acentos(valor))
            return not (verificador is None or verificador.end() != len(valor))
        except:
            return False

    def json(self):
        dic = self.__dict__
        del(dic['valido'])
        del(dic['erro'])
        return json.dumps(dic)

    def salvar(self, arq):
        if self.valido:
            Arquivo.sobrescrever(arq, [self.json()])
        else:
            Arquivo.escrever('ErroLog.txt', [str(self.id) + self.erro])


def listar(lote, csv_dir, boletim_pasta):
    temp = pdf2txt.Diretorio('')
    temp.dir = temp.concatena(csv_dir, boletim_pasta)
    temp.listar(lote)


def converte(entrada, saida, lote, pasta):
    id = 0
    num_threads = len(THREAD_CONTROL)
    while not THREAD_CONTROL[id]:
        id = (id + 1) % num_threads

    THREAD_CONTROL[id] = False
    Conversor(entrada, saida, pasta, lote, id).start()


def txt2json(csv_dir, json_dir, lote):
    csv = pdf2txt.Diretorio(csv_dir)
    csv.listar(lote)

    boletim_root = Arquivo.abrir(csv_dir + '/' + lote)[:-1]

    JSON = pdf2txt.Diretorio(json_dir)

    for boletim_pasta in boletim_root:
        JSON.criar(boletim_pasta)

        converte(csv_dir, json_dir, lote, boletim_pasta)

    while False in THREAD_CONTROL:
        pass


def main():
    txt2json(lote='lote.txt', csv_dir='TXT', json_dir='JSON')
    return 0


if __name__ == '__main__':
    main()