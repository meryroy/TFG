from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QCalendarWidget, QTextEdit, QMessageBox,
    QSizePolicy, QScrollArea, QWidget
)
from PySide6.QtCore import QDate
from db.database import SessionLocal
from db.modelos import PlanEntrenamiento, Entrenamiento
from datetime import datetime, timedelta

class ConsultarActividadesDialog(QDialog):
    def __init__(self, usuario_id):
        super().__init__()
        self.usuario_id = usuario_id
        self.setWindowTitle("Consultar Actividades y Plan")
        self.setMinimumSize(500, 400)
        self.resize(700, 500)

        # Cargar hoja de estilo
        try:
            with open('css/style.css', 'r') as file:
                self.setStyleSheet(file.read())
        except Exception as e:
            print(f"Error al cargar el CSS: {e}")
            QMessageBox.warning(self, "Error de Estilo", f"No se pudo cargar el archivo CSS.\n{e}")

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        layout = QVBoxLayout(container)

        self.calendario = QCalendarWidget()
        self.calendario.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.calendario.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.calendario.selectionChanged.connect(self.mostrar_info_seleccionada)
        layout.addWidget(self.calendario)

        self.texto_info = QTextEdit()
        self.texto_info.setReadOnly(True)
        self.texto_info.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.texto_info)

        scroll.setWidget(container)

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)

        # Cargar datos
        self.planes = []
        self.plan_por_fecha = {}
        self.cargar_planes()

    def cargar_planes(self):
        db = SessionLocal()
        try:
            self.planes = db.query(PlanEntrenamiento).filter(
                PlanEntrenamiento.usuario_id == self.usuario_id
            ).all()

            if not self.planes:
                self.texto_info.setText("No hay plan de entrenamiento generado para este usuario.")
                return

            duracion_plan = max(plan.semana for plan in self.planes)
            fecha_ultima_semana = datetime(2025, 6, 9).date()
            fecha_inicio_plan = fecha_ultima_semana - timedelta(weeks=duracion_plan - 1)
            dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

            self.plan_por_fecha = {}
            for plan in self.planes:
                if plan.dia not in dias_semana:
                    continue
                dia_index = dias_semana.index(plan.dia)
                fecha_mapeada = fecha_inicio_plan + timedelta(weeks=plan.semana - 1, days=dia_index)
                self.plan_por_fecha[fecha_mapeada] = plan

            # Rango del calendario
            self.calendario.setMinimumDate(QDate(fecha_inicio_plan.year, fecha_inicio_plan.month, fecha_inicio_plan.day))
            self.calendario.setMaximumDate(QDate(fecha_ultima_semana.year, fecha_ultima_semana.month, fecha_ultima_semana.day + 6))
            self.calendario.setSelectedDate(QDate(fecha_inicio_plan.year, fecha_inicio_plan.month, fecha_inicio_plan.day))

            self.mostrar_info_seleccionada()

        finally:
            db.close()

    def mostrar_info_seleccionada(self):
        fecha_qdate = self.calendario.selectedDate()
        fecha = datetime(fecha_qdate.year(), fecha_qdate.month(), fecha_qdate.day()).date()

        db = SessionLocal()
        try:
            actividades = db.query(Entrenamiento).filter(
                Entrenamiento.usuario_id == self.usuario_id,
                Entrenamiento.fecha == fecha
            ).all()
        finally:
            db.close()

        info = []

        if fecha in self.plan_por_fecha:
            p = self.plan_por_fecha[fecha]
            info.append(f"Plan: {p.disciplina} - {p.descripcion} - {p.distancia_km} km")

        for act in actividades:
            duracion_str = act.duracion.strftime("%H:%M:%S") if act.duracion else "N/A"
            texto = f"Actividad: {act.disciplina} - {act.distancia_km} km - Duración: {duracion_str}"
            if act.notas:
                texto += f" - Notas: {act.notas}"
            info.append(texto)

        if not info:
            info.append(f"No hay plan ni actividad para el {fecha.strftime('%A %d %B %Y')}.")

        self.texto_info.setText("\n".join(info))
