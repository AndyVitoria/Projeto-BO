import textract
import Arquivo
import os
import platform
import threading

CONTROL = [True, True, True, True, True, True, True, True, True, True, True, True]


class ArquivoPDF(object):
    def __init__(self, nome):
        self.content = ''
        self.nome = nome

    def abrir(self, nome: str):
        self.content = textract.process(nome).decode('utf-8')

    def valido(self):
        return 'INVÁLIDO' not in self.content[:int(len(self.content) * 0.25)]

    def salvar(self, nome):
        return Arquivo.sobrescrever(nome, [self.content])


class Conversor(threading.Thread):
    def __init__(self, entrada, saida, pasta, lote, ID):
        threading.Thread.__init__(self)
        self.pasta = pasta
        self.lote = lote
        self.dir = Diretorio('')
        self.dir.dir = self.dir.concatena(dir1=entrada, dir2=pasta)
        self.entrada = entrada
        self.saida = saida
        self.ID = ID

    def run(self):
        # Lista os arquivos dentro do diretorio
        self.dir.listar(self.lote)

        try:
            invalidos = list()
            buffer = list()
            arquivos = Arquivo.abrir(self.entrada + '/' + self.pasta + '/' + self.lote)[:-1]
            print("Conversão de PDF no diretorio " + self.pasta)
            print("Adicionando ao buffer")
            for arq in arquivos:
                pdf = ArquivoPDF(arq)
                pdf.abrir(self.entrada + '/' + self.pasta + '/' + arq)

                if pdf.valido():
                    buffer.append(pdf)
                else:
                    invalidos.append(pdf)

                if len(buffer) >= 700 or arq == arquivos[-1]:
                    print('Salvando buffer')
                    for elem in buffer:
                        elem.salvar(self.saida + '/' + self.pasta + '/' + elem.nome[:-3] + 'txt')
                    buffer = list()
                    if arq != arquivos[-1]:
                        print("Adicionando ao buffer")
            for elem in invalidos:
                print('Invalido: ' + self.entrada + '/' + self.pasta + '/' + elem.nome)
            CONTROL[self.ID] = True
        except ValueError:
            print(ValueError)
            print("Nao foi possivel converter o diretorio " + self.pasta)
            Arquivo.escrever('Log_Erro.txt', ['Erro ao converter o diretorio ' + self.pasta, "-- " + ValueError.__str__()])
        return 0


class Windows(object):
    def listar(self, dir, arq):
        self.deletar(dir, arq)
        os.system("dir " + dir + "\\ /b /o:n >" + dir + "\\" + arq)

    def deletar(self, dir, arq):
        os.system("del " + dir + "\\" + arq)

    def criar(self, dir):
        os.system("md " + dir)

    def concatena(self, dir1, dir2):
        return dir1 + '\\' + dir2


class Linux(object):
    def listar(self, dir, arq):
        self.deletar(dir, arq)
        os.system('ls ' + dir + '/ >> ' + dir + "/" + arq)

    def deletar(self, dir, arq):
        os.system('rm ' + dir + "/" + arq)

    def criar(self, dir):
        os.system("mkdir " + dir)

    def concatena(self, dir1, dir2):
        return dir1 + '/' + dir2


class Diretorio(object):
    def __init__(self, dir):
        self.dir = dir
        so = platform.system()
        if so == "Windows":
            self.so = Windows()
        elif so == "Linux":
            self.so = Linux()
        else:
            self.so = None

    def listar(self, arq):
        if self.so is not None:
            self.so.listar(self.dir, arq)

    def criar(self, dir):
        if self.so is not None:
            self.so.criar(self.so.concatena(self.dir, dir))

    def concatena(self, dir1, dir2):
        return self.so.concatena(dir1, dir2)


def converte(entrada, saida, lote, pasta):
    id = 0
    num_threads = len(CONTROL)
    while not CONTROL[id]:
        id = (id + 1) % num_threads

    CONTROL[id] = False
    Conversor(entrada, saida, pasta, lote, id).start()


def pdf2txt(lote_dir, pdf_dir, csv_dir):
    lote = lote_dir
    pdf = Diretorio(pdf_dir)
    csv = Diretorio(csv_dir)

    pdf.listar(lote)

    pastas = Arquivo.abrir(pdf.dir + '/' + lote)[:-1]

    for pasta in pastas:
        csv.criar(pasta)

    for pasta in pastas:
        entrada = pdf.dir
        saida = csv.dir
        converte(entrada, saida, lote, pasta)
    while False in CONTROL:
        pass


def main():
    pdf2txt(lote_dir='lote.txt', pdf_dir='PDF', csv_dir='CSV')
    return


if __name__ == '__main__':
    main()
