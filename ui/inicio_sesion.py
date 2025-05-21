import os
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton,
    QMessageBox, QLabel, QSizePolicy
)
from controllers.auth_controller import AuthController
from utils.ui_helpers import cargar_css

class LoginForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de sesión")
        self.setMinimumSize(300, 200)
        self.resize(400, 250)

        # Cargar CSS usando la utilidad
        cargar_css(self)

        layout = QVBoxLayout()

        self.label_usuario = QLabel("Nombre de usuario:")
        self.label_usuario.setWordWrap(True)
        layout.addWidget(self.label_usuario)

        self.input_usuario = QLineEdit()
        self.input_usuario.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.input_usuario)

        self.label_contraseña = QLabel("Contraseña:")
        self.label_contraseña.setWordWrap(True)
        layout.addWidget(self.label_contraseña)

        self.input_contraseña = QLineEdit()
        self.input_contraseña.setEchoMode(QLineEdit.Password)
        self.input_contraseña.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.input_contraseña)

        self.boton_iniciar = QPushButton("Iniciar sesión")
        self.boton_iniciar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.boton_iniciar.clicked.connect(self.validar_login)
        layout.addWidget(self.boton_iniciar)

        self.setLayout(layout)

    def validar_login(self):
        usuario = self.input_usuario.text()
        contraseña = self.input_contraseña.text()

        if AuthController.validar_usuario(usuario, contraseña):
            QMessageBox.information(self, "Éxito", "Inicio de sesión exitoso")
            self.nombre_usuario = usuario
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Nombre de usuario o contraseña incorrectos")
