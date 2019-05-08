#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json as json_lib

def abrir(dir):
    arq = open(dir, 'rt', encoding='utf8')
    linha = arq.readline()
    lst = []
    while linha != '':
        lst.append(linha.strip('\n'))
        linha = arq.readline()
    arq.close()
    return lst


def json(dir, encoding='cp1252'):
    arq = open(dir, 'rt', encoding=encoding)
    JSON = json_lib.load(arq)
    arq.close()
    return JSON


def escrever_json(dir, lst, encoding='cp1252'):
    arq = open(dir, 'wt', encoding=encoding)
    JSON = json_lib.dumps(lst)
    arq.write(JSON)
    arq.close()
    return


def escrever(dir, lst):
    arq = open(dir, 'a', encoding='utf8')
    for elem in lst:
        arq.write(elem + '\n')
    arq.close()
    return

def sobrescrever(dir, lst):
    arq = open(dir, 'w', encoding='utf8')
    for elem in lst:
        arq.writelines(elem + '\n')
    arq.close()
    return