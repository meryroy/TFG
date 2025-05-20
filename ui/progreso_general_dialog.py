from PySide6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QSizePolicy, QPushButton, QFileDialog, QMessageBox
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime, timedelta
from db.database import SessionLocal
from db.modelos import Usuario, PlanEntrenamiento, Entrenamiento

class ProgresoGeneralDialog(QDialog):
    def __init__(self, nombre_usuario):
        super().__init__()
        self.setWindowTitle("Progreso General por Disciplina")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout(self)

        self.combo_disciplina = QComboBox()
        self.combo_disciplina.addItems(["Correr", "Ciclismo", "Natacion"])
        self.combo_disciplina.currentIndexChanged.connect(self.actualizar_grafico)
        self.layout.addWidget(self.combo_disciplina)

        # Botón para guardar imagen
        self.boton_guardar = QPushButton("Guardar gráfico como imagen")
        self.boton_guardar.clicked.connect(self.guardar_imagen)
        self.layout.addWidget(self.boton_guardar)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.canvas)

        self.db = SessionLocal()
        self.usuario = self.db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()

        if not self.usuario:
            raise Exception("Usuario no encontrado")

        semanas_plan = self.db.query(PlanEntrenamiento.semana).filter(
            PlanEntrenamiento.usuario_id == self.usuario.id
        ).distinct().order_by(PlanEntrenamiento.semana).all()

        self.lista_semanas = sorted(set(s[0] for s in semanas_plan))
        self.duracion = max(self.lista_semanas) if self.lista_semanas else 12

        self.actualizar_grafico()

    def actualizar_grafico(self):
        disciplina = self.combo_disciplina.currentText().lower()
        usuario_id = self.usuario.id

        fecha_ultima_semana = datetime(2025, 6, 9).date()
        fecha_inicio_plan = fecha_ultima_semana - timedelta(weeks=self.duracion - 1)

        planes = self.db.query(PlanEntrenamiento).filter(
            PlanEntrenamiento.usuario_id == usuario_id,
            PlanEntrenamiento.disciplina == disciplina
        ).all()

        plan_por_semana = {}
        for p in planes:
            plan_por_semana[p.semana] = plan_por_semana.get(p.semana, 0) + (p.distancia_km or 0)

        entrenamientos = self.db.query(Entrenamiento).filter(
            Entrenamiento.usuario_id == usuario_id,
            Entrenamiento.disciplina == disciplina
        ).all()

        real_por_semana = {}
        for e in entrenamientos:
            if e.fecha:
                if e.fecha < fecha_inicio_plan:
                    continue
                delta = (e.fecha - fecha_inicio_plan).days
                semana = (delta // 7) + 1
                if 1 <= semana <= self.duracion:
                    real_por_semana[semana] = real_por_semana.get(semana, 0) + (e.distancia_km or 0)

        semanas = list(range(1, self.duracion + 1))
        plan_km = [plan_por_semana.get(s, 0) for s in semanas]
        real_km = [real_por_semana.get(s, 0) for s in semanas]

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(semanas, plan_km, label="Planificado", marker='o')
        ax.plot(semanas, real_km, label="Realizado", marker='x')
        ax.set_xlabel("Semana del plan")
        ax.set_ylabel("Kilómetros")
        ax.set_title(f"Progreso general en {disciplina.capitalize()}")
        ax.legend()
        ax.grid(True)

        self.canvas.draw()

    def guardar_imagen(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar gráfico como imagen",
            "",
            "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;All Files (*)"
        )
        if filename:
            try:
                self.figure.savefig(filename)
                QMessageBox.information(self, "Guardado", f"Imagen guardada correctamente en:\n{filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo guardar la imagen:\n{e}")

    def closeEvent(self, event):
        self.db.close()
        event.accept()
