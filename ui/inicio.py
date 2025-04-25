from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox, QDialog
from ui.area_usuario import AreaUsuario
from ui.inicio_sesion import LoginForm
from ui.formulario import Formulario
import os

class PantallaInicio(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión Entrenamiento - Triatlón Madrid")
        self.setGeometry(100, 100, 400, 200)

        # Cargar hoja de estilos
        ruta_css = os.path.join(os.path.dirname(__file__), '..', 'css', 'style.css')
        try:
            with open(ruta_css, 'r') as file:
                self.setStyleSheet(file.read())
        except Exception as e:
            print(f"No se pudo cargar el CSS: {e}")

        layout = QVBoxLayout()

        self.label_bienvenida = QLabel("Bienvenido al Gestor de Entrenamiento")
        layout.addWidget(self.label_bienvenida)

        self.boton_crear = QPushButton("Crear plan de entrenamiento")
        self.boton_crear.clicked.connect(self.crear_plan)
        layout.addWidget(self.boton_crear)

        self.boton_existente = QPushButton("Ya tengo plan de entrenamiento")
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

