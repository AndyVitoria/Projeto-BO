import threading
import PyPDF2
import textract
import os

CONTROL = [True, True, True]  # Variavel de controle de criação de threads


# ========================{Threads}========================#
def PreparaConversao(Pilha):
    i = 0
    MAX = len(CONTROL)
    while i < MAX and CONTROL[i] == False:
        i += 1

    CONTROL[i] = False
    Conversor(Pilha[-1], i).start()
    del (Pilha[-1])
    return


def converteCSV(Dir):
    os.system("java -jar tabula_0.9.0.jar " + Dir + " -r -o CSV" + Dir[3:-3] + 'csv')
    return


class Conversor(threading.Thread):
    def __init__(self, pasta, ID):
        threading.Thread.__init__(self)
        self.pasta = pasta
        self.ID = ID

    def run(self):
        # Lista os arquivos dentro do diretorio
        os.system("dir PDF\\%s /b /o:n >PDF\\%s\\lote.txt" % (self.pasta, self.pasta))
        try:
            arquivos = abrir('PDF\\' + self.pasta + '\\lote.txt')[:-1]
            print("Conversão de PDF no diretorio " + self.pasta)

            for arq in arquivos:
                print(self.pasta + '\\' + arq)
                converteCSV('PDF\\' + self.pasta + '\\' + arq)
            CONTROL[self.ID] = True
        except:
            print("Nao foi possivel converter o diretorio " + self.pasta)
            arq = open('Log_Erro.txt', 'wt')
            arq.write('Erro ao converter o diretorio ' + self.pasta)
            arq.close()
        return 0


# =========================================================#


def listaDir():
    os.system("dir PDF\\ /b /o:n >PDF\\lote.txt")
    pastas = abrir('PDF\\lote.txt')
    for i in range(0, len(pastas), 1):
        if not '.' in pastas[i]:
            print(pastas[i])
            os.system("dir PDF\\" + pastas[i] + "\ /b /o:n > PDF\\" + pastas[i] + "\lote.txt")
    return


def abrir(arquivo):
    arq = open(arquivo, 'rt')
    lst = []
    linha = arq.readline().strip('\n')

    while linha != "":
        lst.append(linha)
        linha = arq.readline().strip('\n')
    arq.close()
    return lst


def abrirPDF(Dir):
    arq = open(Dir, 'rb')
    pdf = PyPDF2.PdfFileReader(arq)
    page = pdf.getPage(0)
    text = page.extractText()
    arq.close()
    return text


def deleta(Dir):
    os.remove(Dir)
    print("REMOVIDO: " + Dir)
    return


def FiltraPDF(Dir):
    text = abrirPDF(Dir)
    lim = [int(len(text) * 0.3), int(len(text) * 0.7)]
    # if (not "INVÁLIDO" in text[:8]) and (
    #             'B01' in text[lim[0]:lim[1]] or 'B02' in text[lim[0]:lim[1]] or 'B10' in text[lim[0]:lim[1]]):
    if (not "INVÁLIDO" in text[:8]):
        return
    else:
        deleta(Dir)
        return


def calcula():
    ret = 0
    diretorios = abrir('PDF/lote.txt')[:-1]
    for i in range(0, len(diretorios), 1):
        arquivos = abrir('PDF/' + diretorios[i] + '/' + 'lote.txt')[:-1]
        ret += len(arquivos)
    return ret


def criaPastas(Direc):
    for elem in Direc:
        os.system("md CSV\\" + elem)
    return


def main():
    # Variaveis #
    tot = 0
    cont = 0
    arquivos = []
    diretorios = []
    PilhaPronto = []  # Pilha de diretorios de pdf's prontos para conversao
    Index = 0

    end = 0
    # ===========#

    listaDir()
    tot = calcula()
    diretorios = abrir('PDF/lote.txt')[:-1]
    '''criaPastas(diretorios)

    for i in range(0, len(diretorios), 1):
        arquivos = abrir('PDF/' + diretorios[i] + '/' + 'lote.txt')[:-1]  # Lista com arquivos do diretorio i
        for j in range(0, len(arquivos), 1):
            cont += 1
            print("[%d%%] [%d Arquivos de %d]" % (cont / tot * 100, cont, tot))
            FiltraPDF('PDF/' + diretorios[i] + '/' + arquivos[j])
        PilhaPronto.append(diretorios[i])
        if True in CONTROL:
            print('antes: %d' % len(PilhaPronto))
            PreparaConversao(PilhaPronto)
            print('depois: %d' % len(PilhaPronto))
    '''
    PilhaPronto = diretorios
    # Conversão dos pdf's restantes
    end = len(PilhaPronto)
    while end > 0:
        if True in CONTROL:
            print("Convertendo Pasta: " + PilhaPronto[-1])
            PreparaConversao(PilhaPronto)
            end -= 1
    return 0


if __name__ == '__main__':
    main()
