from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox, QSpinBox,
    QVBoxLayout, QPushButton, QMessageBox, QLabel
)
from db.database import SessionLocal
from db.modelos import Usuario
from utils.generador_plan import generar_plan
from datetime import datetime

class Formulario(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Formulario de Registro de Usuario")
        self.setGeometry(100, 100, 400, 400)

        self.layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        # Datos del usuario
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

        # Nivel general (bajo, medio, alto) para todas las disciplinas
        self.nivel_input = QComboBox()
        self.nivel_input.addItems(["Bajo", "Medio", "Alto"])
        self.form_layout.addRow("Nivel general de habilidad:", self.nivel_input)

        self.frecuencia_input = QSpinBox()
        self.frecuencia_input.setRange(3, 7)
        self.form_layout.addRow("Frecuencia semanal:", self.frecuencia_input)

        # Duración del plan
        self.duracion_plan_input = QComboBox()
        self.duracion_plan_input.addItems(["24 semanas", "12 semanas", "8 semanas", "6 semanas"])
        self.form_layout.addRow("Duración del plan:", self.duracion_plan_input)

        self.crear_plan_button = QPushButton("Crear Plan")
        self.crear_plan_button.clicked.connect(self.crear_plan)

        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(self.crear_plan_button)
        self.setLayout(self.layout)

    def crear_plan(self):
        db = SessionLocal()

        nombre = self.nombre_input.text().strip()
        apellido = self.apellido_input.text().strip()
        nombre_usuario = self.nombre_usuario_input.text().strip()
        contraseña = self.contraseña_input.text()
        genero = self.genero_input.currentText().lower()
        categoria = self.categoria_input.currentText().lower().replace(" ", "_")
        nivel = self.nivel_input.currentText().lower()  # Nivel general
        frecuencia = self.frecuencia_input.value()

        # Duración seleccionada del plan
        duracion_plan = self.duracion_plan_input.currentText().split()[0]
        duracion_plan = int(duracion_plan)

        # Creamos el usuario en la base de datos
        if db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first():
            self.mostrar_error("Ese nombre de usuario ya está registrado. Elige otro.")
            return

        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            nombre_usuario=nombre_usuario,
            contrasena=contraseña,
            genero=genero,
            categoria=categoria,
            nivel=nivel,  # Solo nivel general
            frecuencia_semanal=frecuencia,

        )

        db.add(nuevo_usuario)
        db.commit()

        # Llamamos a la función generar_plan para generar el plan de entrenamiento con la duración seleccionada
        generar_plan(nuevo_usuario.id, duracion_plan)

        db.close()

        self.mostrar_exito(f"¡Usuario {nombre_usuario} registrado correctamente y plan creado!")

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
        msg.exec()
