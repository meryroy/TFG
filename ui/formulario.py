import os

from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox, QSpinBox,
    QVBoxLayout, QPushButton, QMessageBox, QSizePolicy
)

from controllers.registro_controller import RegistroController
from utils.ui_helpers import cargar_css


class Formulario(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Formulario de Registro de Usuario")
        self.setMinimumSize(400, 400)

        # Cargar CSS usando la utilidad
        cargar_css(self)

        self.main_layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()

        self.nombre_input = QLineEdit()
        self.form_layout.addRow("Nombre:", self.nombre_input)

        self.apellido_input = QLineEdit()
        self.form_layout.addRow("Apellido:", self.apellido_input)

        self.nombre_usuario_input = QLineEdit()
        self.nombre_usuario_input.setPlaceholderText("Nombre de usuario único")
        self.form_layout.addRow("Nombre de usuario:", self.nombre_usuario_input)

        self.contraseña_input = QLineEdit()
        self.contraseña_input.setEchoMode(QLineEdit.Password)
        self.form_layout.addRow("Contraseña:", self.contraseña_input)

        self.genero_input = QComboBox()
        self.genero_input.addItems(["Masculino", "Femenino", "Otro"])
        self.form_layout.addRow("Género:", self.genero_input)

        self.categoria_input = QComboBox()
        self.categoria_input.addItems(["Super Sprint", "Sprint", "Estándar"])
        self.form_layout.addRow("Categoría:", self.categoria_input)

        self.nivel_input = QComboBox()
        self.nivel_input.addItems(["Bajo", "Medio", "Alto"])
        self.form_layout.addRow("Nivel general de habilidad:", self.nivel_input)

        self.frecuencia_input = QSpinBox()
        self.frecuencia_input.setRange(3, 7)
        self.form_layout.addRow("Frecuencia semanal:", self.frecuencia_input)

        self.duracion_plan_input = QComboBox()
        self.duracion_plan_input.addItems(["24 semanas", "12 semanas", "8 semanas", "6 semanas"])
        self.form_layout.addRow("Duración del plan:", self.duracion_plan_input)

        self.crear_plan_button = QPushButton("Crear Plan")
        self.crear_plan_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.crear_plan_button.clicked.connect(self.crear_plan)

        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.crear_plan_button)

    def crear_plan(self):
        datos = {
            "nombre": self.nombre_input.text().strip(),
            "apellido": self.apellido_input.text().strip(),
            "nombre_usuario": self.nombre_usuario_input.text().strip(),
            "contraseña": self.contraseña_input.text(),
            "genero": self.genero_input.currentText().lower(),
            "categoria": self.categoria_input.currentText().lower().replace(" ", "_"),
            "nivel": self.nivel_input.currentText().lower(),
            "frecuencia": self.frecuencia_input.value(),
            "duracion_plan": int(self.duracion_plan_input.currentText().split()[0])
        }

        resultado = RegistroController.registrar_usuario(datos)

        if resultado == "usuario_existente":
            self.mostrar_error("Ese nombre de usuario ya está registrado. Elige otro.")
        elif resultado == "registro_exitoso":
            self.mostrar_exito(f"¡Usuario {datos['nombre_usuario']} registrado correctamente y plan creado!")
        else:
            self.mostrar_error("Ha ocurrido un error inesperado.")

    def mostrar_error(self, mensaje):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setText(mensaje)
        msg.exec()

    def mostrar_exito(self, mensaje):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Éxito")
        msg.setText(mensaje)
        msg.setStandardButtons(QMessageBox.Ok)

        if msg.exec() == QMessageBox.Ok:
            self.close()
            self.abrir_inicio()

    def abrir_inicio(self):
        from ui.inicio import PantallaInicio
        self.ventana_inicio = PantallaInicio()
        self.ventana_inicio.show()
