import os
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QSizePolicy, QPushButton, QFileDialog, QMessageBox
from sqlalchemy.orm import Session
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from db.database import SessionLocal
from db.modelos import Usuario, PlanEntrenamiento, Entrenamiento
from datetime import datetime, timedelta


class ProgresoSemanalDialog(QDialog):
    def __init__(self, usuario_id):
        super().__init__()
        self.setWindowTitle("Progreso Semanal")
        self.setMinimumSize(800, 600)
        self.resize(900, 650)

        ruta_css = os.path.join(os.path.dirname(__file__), '..', 'css', 'style.css')
        try:
            with open(ruta_css, 'r') as file:
                self.setStyleSheet(file.read())
        except Exception as e:
            print(f"No se pudo cargar el CSS: {e}")

        self.usuario_id = usuario_id
        self.db: Session = SessionLocal()

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

        self.usuario = self.db.query(Usuario).filter_by(id=self.usuario_id).first()
        self.cargar_semanas()

    def cargar_semanas(self):
        semanas = (
            self.db.query(PlanEntrenamiento.semana)
            .filter_by(usuario_id=self.usuario_id)
            .distinct()
            .order_by(PlanEntrenamiento.semana)
            .all()
        )
        self.semanas_disponibles = [s[0] for s in semanas]
        self.semana_selector.clear()
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

        dias = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
        esperada = [0] * 7
        realizada = [0] * 7

        # Obtener plan de entrenamiento de esa semana
        plan = self.db.query(PlanEntrenamiento).filter_by(
            usuario_id=self.usuario_id,
            semana=semana_actual
        ).all()

        for p in plan:
            if p.dia.lower() in dias:
                dia_index = dias.index(p.dia.lower())
                esperada[dia_index] += p.distancia_km or 0

        # Cálculo de semana real
        fecha_ultima_semana = datetime(2025, 6, 9).date()  # lunes
        fecha_inicio_plan = fecha_ultima_semana - timedelta(weeks=max(self.semanas_disponibles) - 1)
        fecha_inicio_semana_actual = fecha_inicio_plan + timedelta(weeks=semana_actual - 1)
        fecha_fin_semana_actual = fecha_inicio_semana_actual + timedelta(days=6)

        # Obtener entrenamientos registrados en esa semana real
        entrenamientos = self.db.query(Entrenamiento).filter(
            Entrenamiento.usuario_id == self.usuario_id,
            Entrenamiento.fecha >= fecha_inicio_semana_actual,
            Entrenamiento.fecha <= fecha_fin_semana_actual
        ).all()

        # Mapeo días
        dias_en = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        dias_es = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
        mapa_dias = dict(zip(dias_en, dias_es))

        for e in entrenamientos:
            if e.fecha:
                dia_nombre_en = e.fecha.strftime("%A").lower()
                dia_nombre_es = mapa_dias.get(dia_nombre_en, None)

                if dia_nombre_es in dias:
                    dia_index = dias.index(dia_nombre_es)
                    realizada[dia_index] += e.distancia_km or 0

        # Dibujar gráfico
        self.ax.clear()
        x = range(len(dias))
        self.ax.bar(x, esperada, width=0.4, label='Planificado', align='center')
        self.ax.bar([i + 0.4 for i in x], realizada, width=0.4, label='Realizado', align='center')
        self.ax.set_xticks([i + 0.2 for i in x])
        self.ax.set_xticklabels(dias, rotation=45)
        self.ax.set_ylabel("Km")
        self.ax.set_title(f"Semana {semana_actual} ({fecha_inicio_semana_actual.strftime('%d/%m')} - {fecha_fin_semana_actual.strftime('%d/%m')})")
        self.ax.legend()
        self.canvas.draw()

    def guardar_imagen(self):
        # Abrir diálogo para seleccionar ruta y nombre de archivo
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar gráfico como imagen",
            "",
            "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;All Files (*)"
        )

        if filename:
            try:
                self.canvas.figure.savefig(filename)
                QMessageBox.information(self, "Guardado", f"Imagen guardada correctamente en:\n{filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo guardar la imagen:\n{e}")
