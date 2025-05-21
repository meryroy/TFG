from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox,
    QPushButton, QDateEdit, QTimeEdit, QTextEdit, QMessageBox, QSizePolicy
)
from PySide6.QtCore import QDate, QTime
from controllers.registro_actividad_controller import guardar_actividad_controller
from utils.ui_helpers import cargar_css

class RegistroActividadDialog(QDialog):
    def __init__(self, nombre_usuario):
        super().__init__()
        self.setWindowTitle("Registrar Nueva Actividad")
        self.nombre_usuario = nombre_usuario
        self.setMinimumSize(400, 300)
        # Cargar CSS usando la utilidad
        cargar_css(self)
        main_layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.fecha_input = QDateEdit()
        self.fecha_input.setDate(QDate.currentDate())
        self.fecha_input.setCalendarPopup(True)
        self.fecha_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        form_layout.addRow("Fecha:", self.fecha_input)

        self.disciplina_input = QComboBox()
        self.disciplina_input.addItems(["Ciclismo", "Correr", "Natación"])
        self.disciplina_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        form_layout.addRow("Disciplina:", self.disciplina_input)

        self.duracion_input = QTimeEdit()
        self.duracion_input.setDisplayFormat("HH:mm:ss")
        self.duracion_input.setTime(QTime(0, 30))
        self.duracion_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        form_layout.addRow("Duración (hh:mm:ss):", self.duracion_input)

        self.distancia_input = QLineEdit()
        self.distancia_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        form_layout.addRow("Distancia (km):", self.distancia_input)

        self.notas_input = QTextEdit()
        self.notas_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        form_layout.addRow("Notas:", self.notas_input)

        self.guardar_button = QPushButton("Guardar")
        self.guardar_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.guardar_button.clicked.connect(self.guardar_actividad)

        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.guardar_button)

    def guardar_actividad(self):
        datos = {
            "fecha": self.fecha_input.date().toPython(),
            "disciplina": self.disciplina_input.currentText().lower().strip(),
            "duracion": self.duracion_input.time().toPython(),
            "distancia_km": self.distancia_input.text(),
            "notas": self.notas_input.toPlainText(),
            "nombre_usuario": self.nombre_usuario,
            "ventana": self,
        }

        guardar_actividad_controller(datos)
