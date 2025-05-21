from db.database import SessionLocal
from db.modelos import Entrenamiento

def obtener_actividades_en_fecha(usuario_id, fecha):
    db = SessionLocal()
    try:
        return db.query(Entrenamiento).filter(
            Entrenamiento.usuario_id == usuario_id,
            Entrenamiento.fecha == fecha
        ).all()
    finally:
        db.close()
