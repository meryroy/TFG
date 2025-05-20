from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox,
    QPushButton, QDateEdit, QTimeEdit, QTextEdit, QMessageBox, QSizePolicy
)
from PySide6.QtCore import QDate, QTime
from db.database import SessionLocal
from db.modelos import Entrenamiento, Usuario
from datetime import date, time


class RegistroActividadDialog(QDialog):
    def __init__(self, nombre_usuario):
        super().__init__()
        self.setWindowTitle("Registrar Nueva Actividad")
        self.nombre_usuario = nombre_usuario
        self.setMinimumSize(400, 300)  # Esto puede cambiar en pantallas grandes/pequeñas

        # Cargar la hoja de estilo CSS
        try:
            with open('css/style.css', 'r') as file:
                stylesheet = file.read()
                self.setStyleSheet(stylesheet)
        except Exception as e:
            print(f"Error al cargar el CSS: {e}")
            QMessageBox.warning(self, "Error de Estilo", f"No se pudo cargar el archivo CSS.\n{e}")

        # Layouts
        main_layout = QVBoxLayout(self)  # ¡Importante! pasar `self`
        form_layout = QFormLayout()

        # Fecha
        self.fecha_input = QDateEdit()
        self.fecha_input.setDate(QDate.currentDate())
        self.fecha_input.setCalendarPopup(True)
        self.fecha_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        form_layout.addRow("Fecha:", self.fecha_input)

        # Disciplina
        self.disciplina_input = QComboBox()
        self.disciplina_input.addItems(["Ciclismo", "Correr", "Natación"])
        self.disciplina_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        form_layout.addRow("Disciplina:", self.disciplina_input)

        # Duración
        self.duracion_input = QTimeEdit()
        self.duracion_input.setDisplayFormat("HH:mm:ss")
        self.duracion_input.setTime(QTime(0, 30))  # valor por defecto
        self.duracion_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        form_layout.addRow("Duración (hh:mm:ss):", self.duracion_input)

        # Distancia
        self.distancia_input = QLineEdit()
        self.distancia_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        form_layout.addRow("Distancia (km):", self.distancia_input)

        # Notas
        self.notas_input = QTextEdit()
        self.notas_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        form_layout.addRow("Notas:", self.notas_input)

        # Botón de guardar
        self.guardar_button = QPushButton("Guardar")
        self.guardar_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.guardar_button.clicked.connect(self.guardar_actividad)

        # Añadir layouts
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.guardar_button)

    def guardar_actividad(self):
        # (sin cambios en esta parte, excepto disciplina normalizada)
        try:
            fecha: date = self.fecha_input.date().toPython()
            disciplina: str = self.disciplina_input.currentText().lower().strip()
            duracion: time = self.duracion_input.time().toPython()
            distancia_km: float = float(self.distancia_input.text())
            notas: str = self.notas_input.toPlainText()

            if distancia_km < 0:
                QMessageBox.warning(self, "Dato inválido", "La distancia no puede ser negativa.")
                return

            with SessionLocal() as db:
                usuario = db.query(Usuario).filter(Usuario.nombre_usuario == self.nombre_usuario).first()

                if not usuario:
                    QMessageBox.critical(self, "Error", "Usuario no encontrado.")
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

                print(f"[DEBUG] Guardado: {fecha}, {disciplina}, {distancia_km}")
                QMessageBox.information(self, "Éxito", "Actividad registrada correctamente.")
                self.accept()

        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor, introduce una distancia válida (número).")
