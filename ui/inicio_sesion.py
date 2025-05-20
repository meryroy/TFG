import os
import bcrypt

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton,
    QMessageBox, QLabel, QSizePolicy
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.database import SessionLocal
from db.modelos import Usuario


class LoginForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de sesión")
        self.setMinimumSize(300, 200)
        self.resize(400, 250)

        # Cargar hoja de estilos
        ruta_css = os.path.join(os.path.dirname(__file__), '..', 'css', 'style.css')
        try:
            with open(ruta_css, 'r') as file:
                self.setStyleSheet(file.read())
        except Exception as e:
            print(f"No se pudo cargar el CSS: {e}")

        self.engine = create_engine('sqlite:///data/entrenamiento.db')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

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

        user = self.session.query(Usuario).filter(Usuario.nombre_usuario == usuario).first()

        if user and bcrypt.checkpw(contraseña.encode('utf-8'), user.contrasena):
            QMessageBox.information(self, "Éxito", "Inicio de sesión exitoso")
            self.nombre_usuario = user.nombre_usuario
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Nombre de usuario o contraseña incorrectos")
