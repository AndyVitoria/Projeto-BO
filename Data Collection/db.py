import json
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


class Categoria(Base):
    __tablename__ = 'categoria'

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(10), nullable=False)
    descricao = Column(String(250), nullable=False)


class Municipio(Base):
    __tablename__ = 'municipio'
    id = Column(Integer, primary_key=True, autoincrement=True)
    municipio = Column(String(250), nullable=False)


class Bairro(Base):
    __tablename__ = 'bairro'
    id = Column(Integer, primary_key=True, autoincrement=True)
    bairro = Column(String(250), nullable=False)
    municipio_id = Column(Integer, ForeignKey('municipio.id'))
    municipio = relationship(Municipio)


class Logradouro(Base):
    __tablename__ = 'logradouro'
    id = Column(Integer, primary_key=True, autoincrement=True)
    logradouro = Column(String(250), nullable=True)
    bairro_id = Column(Integer, ForeignKey('bairro.id'))
    bairro = relationship(Bairro)


class Endereco(Base):
    __tablename__ = 'endereco'
    id = Column(Integer, primary_key=True, autoincrement=True)
    referencia = Column(String(250), nullable=True)
    complemento = Column(String(250), nullable=True)
    logradouro_id = Column(Integer, ForeignKey('logradouro.id'))
    logradouro = relationship(Logradouro)


class TipoLocal(Base):
    __tablename__ = 'tipo_local'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo_local = Column(String(250), nullable=False)


class Boletim(Base):
    __tablename__ = 'boletim'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    categoria_id = Column(Integer, ForeignKey('categoria.id'))
    categoria = relationship(Categoria)
    endereco_id = Column(Integer, ForeignKey('endereco.id'))
    endereco = relationship(Endereco)
    tipo_local_id = Column(Integer, ForeignKey('tipo_local.id'))
    tipo_local = relationship(TipoLocal)
    data_registro = Column(Date, nullable=False)
    hora_registro = Column(Time, nullable=False)
    data_ocorrencia = Column(Date, nullable=True)
    hora_ocorrencia = Column(Time, nullable=True)


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    item = Column(String(250), nullable=False)
    status = Column(String(250), nullable=True)
    quantidade = Column(Integer, nullable=False)
    boletim_id = Column(Integer, ForeignKey('boletim.id'))
    boletim = relationship(Boletim)




# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
# engine = create_engine('sqlite:///sqlalchemy_example.db')
engine = create_engine('postgresql://postgres:DarkAngel1995#@localhost')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
Base.metadata.bind = engine

from sqlalchemy.orm import sessionmaker
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()


def main():
    #print(session.query(Endereco).filter_by(complemento='').first())
    return


if __name__ == '__main__':

    main()