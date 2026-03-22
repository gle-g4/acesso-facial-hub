from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, LargeBinary, Boolean, CheckConstraint
from sqlalchemy.orm import relationship, declarative_base
import datetime

Base = declarative_base()

class Aluno(Base):
    __tablename__ = "alunos"
    id_aluno = Column(Integer, primary_key=True, autoincrement=True)
    matricula = Column(String, unique=True, nullable=False)
    nome_completo = Column(String, nullable=False)
    curso = Column(String, nullable=False)
    tipo_vinculo = Column(String, nullable=False)
    turno = Column(String, nullable=False)
    status_acesso = Column(String, nullable=False, default="ATIVO")
    vetor_128d = Column(LargeBinary, nullable=True)
    criado_em = Column(DateTime, default=datetime.datetime.utcnow)
    acessos = relationship("EventoAcesso", back_populates="aluno")
    overrides = relationship("OverrideAcesso", back_populates="aluno")

class Dispositivo(Base):
    __tablename__ = "dispositivos"
    id_dispositivo = Column(Integer, primary_key=True, autoincrement=True)
    api_key = Column(String, unique=True, nullable=False)
    localizacao = Column(String, nullable=False)
    bloco = Column(String, nullable=False)
    mac_address = Column(String, unique=True)
    ativo = Column(Integer, default=1)
    ultimo_heartbeat = Column(DateTime)
    cadastrado_em = Column(DateTime, default=datetime.datetime.utcnow)
    acessos = relationship("EventoAcesso", back_populates="dispositivo")

class RegraBlocoVinculo(Base):
    __tablename__ = "regras_bloco_vinculo"
    id_regra = Column(Integer, primary_key=True, autoincrement=True)
    tipo_vinculo = Column(String, nullable=False)
    bloco = Column(String, nullable=False)
    permitido = Column(Boolean, default=True)

class OverrideAcesso(Base):
    __tablename__ = "overrides_acesso"
    id_override = Column(Integer, primary_key=True, autoincrement=True)
    id_aluno = Column(Integer, ForeignKey("alunos.id_aluno"), nullable=False)
    bloco = Column(String, nullable=False)
    tipo_override = Column(String, nullable=False)
    motivo = Column(String)
    criado_em = Column(DateTime, default=datetime.datetime.utcnow)
    aluno = relationship("Aluno", back_populates="overrides")

class EventoAcesso(Base):
    __tablename__ = "eventos_acesso"
    id_evento = Column(Integer, primary_key=True, autoincrement=True)
    id_aluno = Column(Integer, ForeignKey("alunos.id_aluno"), nullable=True)
    id_dispositivo = Column(Integer, ForeignKey("dispositivos.id_dispositivo"), nullable=False)
    resultado = Column(String, nullable=False)
    codigo_motivo = Column(String, nullable=False)
    distancia_faiss = Column(Float)
    ocorrido_em = Column(DateTime, default=datetime.datetime.utcnow)
    aluno = relationship("Aluno", back_populates="aluno")
    dispositivo = relationship("Dispositivo", back_populates="acessos")
