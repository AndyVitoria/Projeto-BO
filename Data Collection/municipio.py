import Arquivo
from Acentos import remover_acentos

lst = Arquivo.abrir('municipios.txt')
muni = list()
for elem in lst:
    muni.append(remover_acentos(elem.split('\t')[1]).upper())
muni.sort()
for elem in muni:
    print(elem)

Arquivo.sobrescrever('lista_municipios.txt', muni)