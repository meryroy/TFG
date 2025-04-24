from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QLabel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.database import SessionLocal
from db.modelos import Usuario
from ui.area_usuario import AreaUsuario


class LoginForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de sesión")


        self.engine = create_engine('sqlite:///data/entrenamientos.db')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        layout = QVBoxLayout()

        self.label_usuario = QLabel("Nombre de usuario:")
        self.input_usuario = QLineEdit()
        layout.addWidget(self.label_usuario)
        layout.addWidget(self.input_usuario)

        self.label_contraseña = QLabel("Contraseña:")
        self.input_contraseña = QLineEdit()
        self.input_contraseña.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.label_contraseña)
        layout.addWidget(self.input_contraseña)

        self.boton_iniciar = QPushButton("Iniciar sesión")
        self.boton_iniciar.clicked.connect(self.validar_login)
        layout.addWidget(self.boton_iniciar)

        self.setLayout(layout)

    def validar_login(self):
        # Obtener el nombre de usuario y la contraseña del formulario
        usuario = self.input_usuario.text()
        contraseña = self.input_contraseña.text()

        # Buscar el usuario en la base de datos
        user = self.session.query(Usuario).filter(Usuario.nombre_usuario == usuario).first()

        # Verificar si se encontró el usuario y si la contraseña es correcta
        if user and user.contrasena == contraseña:  # Asegúrate de tener la contraseña cifrada correctamente
            QMessageBox.information(self, "Éxito", "Inicio de sesión exitoso")
            self.nombre_usuario = user.nombre_usuario
            self.accept()  # Aceptar el login y cerrar el formulario
        else:
            QMessageBox.warning(self, "Error", "Nombre de usuario o contraseña incorrectos")
    def show_area_usuario(self):
        # Este método lo utilizas para mostrar el área de usuario después del login
        self.area_usuario = AreaUsuario()
        self.area_usuario.exec()
