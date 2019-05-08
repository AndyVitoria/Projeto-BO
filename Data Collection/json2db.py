from pdf2txt import Diretorio
from datetime import datetime
import Arquivo
import json
from db import Categoria, Municipio, Bairro, Logradouro, Endereco, TipoLocal, Boletim, Item
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def save_bo(bo, session):

    categoria = session.query(Categoria).filter_by(codigo=bo['codigo']).first()
    if categoria is None:
        categoria = Categoria(codigo=bo['codigo'], descricao=bo['descricao'])
        save(session, categoria)

    municipio = session.query(Municipio).filter_by(municipio=bo['municipio']).first()
    if municipio is None:
        municipio = Municipio(municipio=bo['municipio'])
        save(session, municipio)

    bairro = session.query(Bairro).filter_by(bairro=bo['bairro']).first()
    if bairro is None:
        bairro = Bairro(bairro=bo['bairro'], municipio=municipio)
        save(session, bairro)

    logradouro = session.query(Logradouro).filter_by(logradouro=bo['local']).first()
    if logradouro is None:
        logradouro = Logradouro(logradouro=bo['local'], bairro=bairro)
        save(session, logradouro)

    endereco = session.query(Endereco).filter_by(complemento=bo['complemento'], referencia=bo['referencia']).first()
    if endereco is None:
        endereco = Endereco(complemento=bo['complemento'], referencia=bo['referencia'], logradouro=logradouro)
        save(session, endereco)

    tipo_local = session.query(TipoLocal).filter_by(tipo_local=bo['tipo_de_local']).first()
    if tipo_local is None:
        tipo_local = TipoLocal(tipo_local=bo['tipo_de_local'])
        save(session, tipo_local)

    boletim = session.query(Boletim).filter_by(id=bo['id']).first()
    if boletim is None:
        if len(bo['data']) == 2:
                bo['data'][0] = datetime.strptime(bo['data'][0], "%d/%m/%Y").date()
                bo['data'][1] = datetime.strptime(bo['data'][1], "%H:%M").time()
        else:
            while len(bo['data']) < 2:
                bo['data'].append(None)

        bo['registrado'][0] = datetime.strptime(bo['registrado'][0], "%d/%m/%Y").date()
        bo['registrado'][1] = datetime.strptime(bo['registrado'][1], "%H:%M").time()

        boletim = Boletim(id=bo['id'], data_ocorrencia=bo['data'][0], hora_ocorrencia=bo['data'][1], data_registro=bo['registrado'][0], hora_registro=bo['registrado'][1], categoria=categoria, tipo_local=tipo_local, endereco=endereco)
        save(session,boletim)

    for item_key in bo['item']:
        item = bo['item'][item_key]
        if len(item) == 2:
            bo_item = session.query(Item).filter_by(boletim=boletim, item=item[0], quantidade=item[1]).first()
            if bo_item is None:
                bo_item = Item(boletim=boletim, item=item[0], quantidade=item[1])
                save(session, bo_item)
        elif len(item) ==3:
            bo_item = session.query(Item).filter_by(boletim=boletim, item=item[0], status=item[1], quantidade=item[2]).first()
            if bo_item is None:
                bo_item = Item(boletim=boletim, item=item[0], status=item[1], quantidade=item[2])
                save(session, bo_item)


def save(session, obj):
    session.add(obj)
    session.commit()
    return


def start():
    Base = declarative_base()
    # Create an engine that stores data in the local directory's
    # sqlalchemy_example.db file.
    # engine = create_engine('sqlite:///sqlalchemy_example.db')
    engine = create_engine('postgresql://postgres:DarkAngel1995#@localhost')

    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine

    DBSession = sessionmaker()
    DBSession.bind = engine
    session = DBSession()
    return session


def main():
    session = start()
    json_dir = 'JSON/'
    lote_list = Arquivo.abrir(json_dir + 'lote.txt')[:-1]

    for lote in lote_list:
        arq = open(json_dir + lote + '/' + lote + '.json', 'rt')
        bo_list = json.load(arq)
        for bo in bo_list:
            save_bo(bo, session)
    return

if __name__ == '__main__':
    main()