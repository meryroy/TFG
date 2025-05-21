
import os
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QSizePolicy, QPushButton, QFileDialog, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from controllers.graficos_controller import cargar_semanas, obtener_datos_progreso_semanal
from utils.ui_helpers import cargar_css
from utils.imagen_utils import guardar_figura_como_imagen


class ProgresoSemanalDialog(QDialog):
    def __init__(self, usuario_id):
        super().__init__()
        self.setWindowTitle("Progreso Semanal")
        self.setMinimumSize(800, 600)
        self.resize(900, 650)


        cargar_css(self)

        self.usuario_id = usuario_id

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

        self.label = QLabel("Selecciona una semana:")
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.layout.addWidget(self.label)

        self.semana_selector = QComboBox()
        self.semana_selector.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.semana_selector.currentIndexChanged.connect(self.mostrar_grafico)
        self.layout.addWidget(self.semana_selector)

        self.boton_guardar = QPushButton("Guardar gráfico como imagen")
        self.boton_guardar.clicked.connect(self.guardar_imagen)
        self.layout.addWidget(self.boton_guardar)

        self.canvas = FigureCanvas(Figure(figsize=(8, 5)))
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.canvas)
        self.ax = self.canvas.figure.add_subplot(111)

        # Cargar semanas con el controlador
        self.semanas_disponibles = cargar_semanas(self.usuario_id)
        for semana in self.semanas_disponibles:
            self.semana_selector.addItem(f"Semana {semana}", semana)

        if self.semanas_disponibles:
            self.semana_selector.setCurrentIndex(0)
            self.mostrar_grafico()

    def mostrar_grafico(self):
        semana_index = self.semana_selector.currentIndex()
        if semana_index == -1:
            return

        semana_actual = self.semanas_disponibles[semana_index]

        datos = obtener_datos_progreso_semanal(self.usuario_id, self.semanas_disponibles, semana_actual)

        self.ax.clear()
        x = range(len(datos['dias']))
        self.ax.bar(x, datos['esperada'], width=0.4, label='Planificado', align='center')
        self.ax.bar([i + 0.4 for i in x], datos['realizada'], width=0.4, label='Realizado', align='center')
        self.ax.set_xticks([i + 0.2 for i in x])
        self.ax.set_xticklabels(datos['dias'], rotation=45)
        self.ax.set_ylabel("Km")
        self.ax.set_title(f"Semana {semana_actual} ({datos['fecha_inicio_semana_actual'].strftime('%d/%m')} - {datos['fecha_fin_semana_actual'].strftime('%d/%m')})")
        self.ax.legend()
        self.canvas.draw()

    def guardar_imagen(self):
        guardar_figura_como_imagen(self, self.canvas.figure)
