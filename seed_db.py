from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Aluno, Dispositivo, EventoAcesso, RegraBlocoVinculo, OverrideAcesso
import datetime
import random

SQLALCHEMY_DATABASE_URL = "sqlite:///./acesso_facial.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    catraca_sede = Dispositivo(id_dispositivo=1, localizacao="Entrada Principal — Sede", bloco="SEDE", api_key="hub-device-01", mac_address="AA:BB:CC:DD:EE:01", ativo=1)
    catraca_bloco_a = Dispositivo(id_dispositivo=2, localizacao="Entrada Bloco A", bloco="BLOCO_AULAS", api_key="hub-device-02", mac_address="AA:BB:CC:DD:EE:02", ativo=1)
    db.add_all([catraca_sede, catraca_bloco_a])
    db.commit()

    regras = [
        RegraBlocoVinculo(tipo_vinculo="GRADUACAO", bloco="SEDE", permitido=True),
        RegraBlocoVinculo(tipo_vinculo="GRADUACAO", bloco="BLOCO_AULAS", permitido=True),
        RegraBlocoVinculo(tipo_vinculo="PROFESSOR", bloco="SEDE", permitido=True),
        RegraBlocoVinculo(tipo_vinculo="FUNCIONARIO", bloco="BLOCO_AULAS", permitido=False)
    ]
    db.add_all(regras)
    db.commit()

    for i in range(5):
        aluno = Aluno(nome_completo=f"Aluno Teste {i+1}", matricula=f"202400{i:04d}", curso="Engenharia", tipo_vinculo="GRADUACAO", turno="MANHA", status_acesso="ATIVO")
        db.add(aluno)
    
    db.commit()
    db.close()
    print("✅ Banco de Dados v2.0 FINAL criado com sucesso!")

if __name__ == "__main__":
    seed()
