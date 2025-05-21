from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QLabel, QMessageBox,
    QTableWidget, QTableWidgetItem, QSizePolicy, QScrollArea, QWidget
)
from controllers.usuario_controller import UsuarioController
from utils.ui_helpers import cargar_css
from ui.registrar_actividad_dialog import RegistroActividadDialog
from ui.consultar_actividades_dialog import ConsultarActividadesDialog
from ui.progreso_semanal_dialog import ProgresoSemanalDialog
from ui.progreso_general_dialog import ProgresoGeneralDialog


class AreaUsuario(QDialog):
    def __init__(self, nombre_usuario):
        super().__init__()
        self.nombre_usuario = nombre_usuario

        self.setWindowTitle("Área de Usuario")
        self.setMinimumSize(600, 500)
        self.resize(900, 600)

        cargar_css(self)

        # Scrollable layout
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        self.layout = QVBoxLayout(container)

        self.bienvenida_label = QLabel(f"¡Bienvenido, {self.nombre_usuario}!")
        self.bienvenida_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.layout.addWidget(self.bienvenida_label)

        # Botones
        self.consultar_plan_button = QPushButton("Consultar plan de entrenamientos")
        self.consultar_plan_button.clicked.connect(self.consultar_plan)
        self.layout.addWidget(self.consultar_plan_button)

        self.registrar_actividad_button = QPushButton("Registrar actividad")
        self.registrar_actividad_button.clicked.connect(self.registrar_actividad)
        self.layout.addWidget(self.registrar_actividad_button)

        self.consultar_actividades_button = QPushButton("Consultar actividades y plan")
        self.consultar_actividades_button.clicked.connect(self.consultar_actividades)
        self.layout.addWidget(self.consultar_actividades_button)

        self.boton_progreso_semanal = QPushButton("Comprobar progreso por semanas")
        self.boton_progreso_semanal.clicked.connect(self.comprobar_progreso_semanal)
        self.layout.addWidget(self.boton_progreso_semanal)

        self.boton_progreso_general = QPushButton("Comprobar progreso general")
        self.boton_progreso_general.clicked.connect(self.comprobar_progreso_general)
        self.layout.addWidget(self.boton_progreso_general)

        # Tabla
        self.table_widget = QTableWidget()
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.table_widget)

        # Cerrar sesión
        self.cerrar_sesion_button = QPushButton("Cerrar sesión")
        self.cerrar_sesion_button.clicked.connect(self.cerrar_sesion)
        self.layout.addWidget(self.cerrar_sesion_button)

        scroll_area.setWidget(container)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)

    def consultar_plan(self):
        usuario = UsuarioController.obtener_usuario_por_nombre(self.nombre_usuario)
        if not usuario:
            QMessageBox.warning(self, "Error", "No se ha encontrado el usuario.")
            return

        planes = UsuarioController.obtener_planes_entrenamiento(usuario.id)
        if not planes:
            QMessageBox.warning(self, "Error", "No se ha encontrado el plan de entrenamiento.")
            return

        self.table_widget.clearContents()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(
            ["Semana", "Día", "Disciplina", "Descripción", "Distancia (km)"]
        )
        self.table_widget.setRowCount(len(planes))

        for i, plan in enumerate(planes):
            self.table_widget.setItem(i, 0, QTableWidgetItem(str(plan.semana)))
            self.table_widget.setItem(i, 1, QTableWidgetItem(plan.dia))
            self.table_widget.setItem(i, 2, QTableWidgetItem(plan.disciplina))
            self.table_widget.setItem(i, 3, QTableWidgetItem(plan.descripcion))
            self.table_widget.setItem(i, 4, QTableWidgetItem(str(plan.distancia_km)))

    def registrar_actividad(self):
        dialogo = RegistroActividadDialog(self.nombre_usuario)
        dialogo.exec()

    def consultar_actividades(self):
        usuario = UsuarioController.obtener_usuario_por_nombre(self.nombre_usuario)
        if usuario:
            dialog = ConsultarActividadesDialog(usuario.id)
            dialog.exec()
        else:
            QMessageBox.warning(self, "Error", "No se encontró el usuario para consultar actividades.")

    def comprobar_progreso_semanal(self):
        usuario = UsuarioController.obtener_usuario_por_nombre(self.nombre_usuario)
        if usuario:
            dialog = ProgresoSemanalDialog(usuario.id)
            dialog.exec()
        else:
            QMessageBox.warning(self, "Error", "No se encontró el usuario.")

    def comprobar_progreso_general(self):
        dialog = ProgresoGeneralDialog(self.nombre_usuario)
        dialog.exec()

    def cerrar_sesion(self):
        from ui.inicio import PantallaInicio
        self.close()
        self.inicio = PantallaInicio()
        self.inicio.show()
