import bcrypt
from db.database import SessionLocal
from db.modelos import Usuario

class AuthController:
    @staticmethod
    def validar_usuario(nombre_usuario: str, contraseña: str) -> bool:
        with SessionLocal() as db:
            user = db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()
            if user and bcrypt.checkpw(contraseña.encode('utf-8'), user.contrasena):
                return True
            return False
