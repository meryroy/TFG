import bcrypt
from datetime import datetime, timedelta
from db.database import SessionLocal
from db.modelos import Usuario
from controllers.plan_controller import generar_plan

class RegistroController:
    @staticmethod
    def registrar_usuario(datos: dict) -> str:
        with SessionLocal() as db:
            if db.query(Usuario).filter(Usuario.nombre_usuario == datos["nombre_usuario"]).first():
                return "usuario_existente"

            contraseña_hash = bcrypt.hashpw(datos["contraseña"].encode('utf-8'), bcrypt.gensalt())

            fecha_objetivo = datetime(2025, 6, 9).date()
            semanas_total = timedelta(weeks=datos["duracion_plan"] - 1)
            fecha_inicio_plan = fecha_objetivo - semanas_total

            nuevo_usuario = Usuario(
                nombre=datos["nombre"],
                apellido=datos["apellido"],
                nombre_usuario=datos["nombre_usuario"],
                contrasena=contraseña_hash,
                genero=datos["genero"],
                categoria=datos["categoria"],
                nivel=datos["nivel"],
                frecuencia_semanal=datos["frecuencia"],
                fecha_inicio_plan=fecha_inicio_plan,
                duracion_plan=datos["duracion_plan"]
            )

            db.add(nuevo_usuario)
            db.commit()
            db.refresh(nuevo_usuario)
            generar_plan(nuevo_usuario, datos["duracion_plan"], db)

            return "registro_exitoso"
