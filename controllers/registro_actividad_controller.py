from PySide6.QtWidgets import QMessageBox
from db.database import SessionLocal
from db.modelos import Entrenamiento, Usuario

def guardar_actividad_controller(datos):
    try:
        fecha = datos["fecha"]
        disciplina = datos["disciplina"]
        duracion = datos["duracion"]
        distancia_km = float(datos["distancia_km"])
        notas = datos["notas"]
        nombre_usuario = datos["nombre_usuario"]
        ventana = datos["ventana"]

        if distancia_km < 0:
            QMessageBox.warning(ventana, "Dato inválido", "La distancia no puede ser negativa.")
            return

        with SessionLocal() as db:
            usuario = db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()
            if not usuario:
                QMessageBox.critical(ventana, "Error", "Usuario no encontrado.")
                return

            nuevo_entrenamiento = Entrenamiento(
                usuario_id=usuario.id,
                fecha=fecha,
                disciplina=disciplina,
                duracion=duracion,
                distancia_km=distancia_km,
                notas=notas
            )
            db.add(nuevo_entrenamiento)
            db.commit()

        QMessageBox.information(ventana, "Éxito", "Actividad registrada correctamente.")
        ventana.accept()

    except ValueError:
        QMessageBox.warning(ventana, "Error", "Por favor, introduce una distancia válida (número).")
