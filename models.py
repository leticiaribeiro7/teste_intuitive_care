# model pro sql alchemy

from sqlalchemy import Column, String, Integer, Numeric, Date, ForeignKey, CHAR
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Operadora(Base):
    __tablename__ = 'operadoras'
    
    registro_ans = Column(String(20), primary_key=True)
    cnpj = Column(String(14), nullable=False)
    razao_social = Column(String(255), nullable=False)
    nome_fantasia = Column(String(255))
    modalidade = Column(String(100))
    logradouro = Column(String(255))
    numero = Column(String(50))
    complemento = Column(String(255))
    bairro = Column(String(100))
    cidade = Column(String(100))
    uf = Column(CHAR(2))
    cep = Column(String(20))
    ddd = Column(String(10))
    telefone = Column(String(20))
    fax = Column(String(20))
    email = Column(String(255))
    representante = Column(String(255))
    cargo_representante = Column(String(255))
    regiao_comercializacao = Column(Integer)
    data_registro_ans = Column(Date)

class DespesaConsolidada(Base):
    __tablename__ = 'despesas_consolidadas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cnpj = Column(String(14), nullable=False)
    ano = Column(Integer, nullable=False)
    trimestre = Column(Integer, nullable=False)
    valor_despesas = Column(Numeric(18, 2), nullable=False)

class DespesaAgregada(Base):
    __tablename__ = 'despesas_agregadas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    razao_social = Column(String(255), nullable=False)
    registro_ans = Column(String(20), nullable=False)
    modalidade = Column(String(100), nullable=False)
    uf = Column(CHAR(2), nullable=False)
    total_despesas = Column(Numeric(18, 2), nullable=False)
    media_trimestral = Column(Numeric(18, 2), nullable=False)
    desvio_padrao = Column(Numeric(18, 2), nullable=False)