from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel, QSizePolicy, QDialog
)
from ui.area_usuario import AreaUsuario
from ui.inicio_sesion import LoginForm
from ui.formulario import Formulario
import os
from utils.ui_helpers import cargar_css


class PantallaInicio(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión Entrenamiento - Triatlón Madrid")
        self.setMinimumSize(350, 250)
        self.resize(500, 300)


        cargar_css(self)

        layout = QVBoxLayout()

        self.label_bienvenida = QLabel("Bienvenido al Gestor de Entrenamiento")
        self.label_bienvenida.setWordWrap(True)
        self.label_bienvenida.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(self.label_bienvenida)

        self.boton_crear = QPushButton("Crear plan de entrenamiento")
        self.boton_crear.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.boton_crear.clicked.connect(self.crear_plan)
        layout.addWidget(self.boton_crear)

        self.boton_existente = QPushButton("Ya tengo plan de entrenamiento")
        self.boton_existente.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.boton_existente.clicked.connect(self.acceder_area_usuario)
        layout.addWidget(self.boton_existente)

        self.setLayout(layout)

    def crear_plan(self):
        self.formulario = Formulario()
        self.formulario.show()
        self.close()

    def acceder_area_usuario(self):
        login_form = LoginForm()
        if login_form.exec() == QDialog.Accepted:
            nombre_usuario = login_form.nombre_usuario
            self.area = AreaUsuario(nombre_usuario)
            self.area.show()
            self.close()
