from db.database import SessionLocal
from db.modelos import Usuario, PlanEntrenamiento

class UsuarioController:
    @staticmethod
    def obtener_usuario_por_nombre(nombre_usuario):
        with SessionLocal() as db:
            return db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()

    @staticmethod
    def obtener_planes_entrenamiento(usuario_id):
        orden_dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        with SessionLocal() as db:
            planes = db.query(PlanEntrenamiento).filter(PlanEntrenamiento.usuario_id == usuario_id).all()
            if planes:
                # Ordenar planes según semana y día
                planes.sort(key=lambda p: (p.semana, orden_dias.index(p.dia)))
            return planes
