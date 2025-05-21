
from PySide6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QSizePolicy, QPushButton, QFileDialog, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from controllers.graficos_controller import obtener_usuario_y_semanas, obtener_datos_progreso_general
from utils.ui_helpers import cargar_css
from utils.imagen_utils import guardar_figura_como_imagen


class ProgresoGeneralDialog(QDialog):
    def __init__(self, nombre_usuario):
        super().__init__()
        self.setWindowTitle("Progreso General por Disciplina")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout(self)

        cargar_css(self)

        self.combo_disciplina = QComboBox()
        self.combo_disciplina.addItems(["Correr", "Ciclismo", "Natacion"])
        self.combo_disciplina.currentIndexChanged.connect(self.actualizar_grafico)
        self.layout.addWidget(self.combo_disciplina)

        self.boton_guardar = QPushButton("Guardar gráfico como imagen")
        self.boton_guardar.clicked.connect(self.guardar_imagen)
        self.layout.addWidget(self.boton_guardar)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.canvas)

        # Obtener usuario y semanas con el controlador
        resultado = obtener_usuario_y_semanas(nombre_usuario)
        self.usuario = resultado['usuario']
        self.lista_semanas = resultado['semanas']

        if not self.usuario:
            raise Exception("Usuario no encontrado")

        self.duracion = max(self.lista_semanas) if self.lista_semanas else 12

        self.actualizar_grafico()

    def actualizar_grafico(self):
        disciplina = self.combo_disciplina.currentText().lower()
        usuario_id = self.usuario.id

        datos = obtener_datos_progreso_general(usuario_id, disciplina, self.duracion)

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(datos['semanas'], datos['plan_km'], label="Planificado", marker='o')
        ax.plot(datos['semanas'], datos['real_km'], label="Realizado", marker='x')
        ax.set_xlabel("Semana del plan")
        ax.set_ylabel("Kilómetros")
        ax.set_title(f"Progreso general en {disciplina.capitalize()}")
        ax.legend()
        ax.grid(True)

        self.canvas.draw()

    def guardar_imagen(self):
        guardar_figura_como_imagen(self, self.canvas.figure)


    def closeEvent(self, event):
        event.accept()
