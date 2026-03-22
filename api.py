from fastapi import FastAPI, UploadFile, File, Header, HTTPException
import cv2
import numpy as np
import os
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Aluno, EventoAcesso, Dispositivo

app = FastAPI(title="API Hub Universitário - v2.0 (OpenCV + SQL)")

# Carrega o detector de rostos padrão do OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

@app.post("/access/verify")
async def verificar_acesso(
    file: UploadFile = File(...), 
    x_api_key: str = Header(None, alias="X-API-Key-Device"),
    x_device_mac: str = Header(None, alias="X-Device-MAC")
):
    db = get_db()
    dispositivo = db.query(Dispositivo).filter(Dispositivo.api_key == x_api_key).first()
    
    if not dispositivo:
        raise HTTPException(status_code=401, detail="Catraca não autorizada!")

    try:
        conteudo = await file.read()
        nparr = np.frombuffer(conteudo, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detecta rostos na imagem
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) == 0:
            novo_evento = EventoAcesso(id_dispositivo=dispositivo.id_dispositivo, resultado="DESCONHECIDO", codigo_motivo="ROSTO_NAO_DETECTADO")
            db.add(novo_evento)
            db.commit()
            return {"status": "bloqueado", "motivo": "Nenhum rosto detectado"}

        # Como é um teste para a ExpoTech, vamos simular que o primeiro aluno do banco foi reconhecido
        aluno = db.query(Aluno).filter(Aluno.status_acesso == "ATIVO").first()
        
        if aluno:
            novo_evento = EventoAcesso(id_aluno=aluno.id_aluno, id_dispositivo=dispositivo.id_dispositivo, resultado="LIBERADO", codigo_motivo="OK")
            db.add(novo_evento)
            db.commit()
            return {"status": "liberado", "nome": aluno.nome_completo, "matricula": aluno.matricula}
        else:
            return {"status": "bloqueado", "motivo": "Acesso negado"}

    except Exception as e:
        db.rollback()
        return {"status": "erro", "mensagem": str(e)}
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
