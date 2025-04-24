from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QMessageBox, QTableWidget, QTableWidgetItem
from db.database import SessionLocal
from db.modelos import Usuario, PlanEntrenamiento

class AreaUsuario(QDialog):
    def __init__(self, nombre_usuario):
        super().__init__()
        self.nombre_usuario = nombre_usuario

        self.setWindowTitle("Área de Usuario")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()


        self.bienvenida_label = QLabel(f"¡Bienvenido, {self.nombre_usuario}!", self)
        self.layout.addWidget(self.bienvenida_label)

        # Botones para las opciones
        self.consultar_plan_button = QPushButton("Consultar plan de entrenamientos", self)
        self.consultar_plan_button.clicked.connect(self.consultar_plan)
        self.layout.addWidget(self.consultar_plan_button)

        self.registrar_actividad_button = QPushButton("Registrar actividad", self)
        self.registrar_actividad_button.clicked.connect(self.registrar_actividad)
        self.layout.addWidget(self.registrar_actividad_button)

        self.comprobar_progreso_button = QPushButton("Comprobar progreso", self)
        self.comprobar_progreso_button.clicked.connect(self.comprobar_progreso)
        self.layout.addWidget(self.comprobar_progreso_button)

        # Tabla para mostrar los datos del plan
        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        self.setLayout(self.layout)

    def consultar_plan(self):
        db = SessionLocal()
        usuario = db.query(Usuario).filter(Usuario.nombre_usuario == self.nombre_usuario).first()

        if usuario:
            # Obtener los planes del usuario
            planes = db.query(PlanEntrenamiento).filter(PlanEntrenamiento.usuario_id == usuario.id).order_by(PlanEntrenamiento.semana, PlanEntrenamiento.dia).all()

            if not planes:
                QMessageBox.warning(self, "Error", "No se ha encontrado el plan de entrenamiento.")
                return

            # Establecer las cabeceras de la tabla
            self.table_widget.setColumnCount(6)
            self.table_widget.setHorizontalHeaderLabels(["Semana", "Día", "Disciplina", "Descripción", "Duración (min)", "Distancia (km)"])

            # Llenar la tabla con los datos del plan
            self.table_widget.setRowCount(len(planes))

            for i, plan in enumerate(planes):
                self.table_widget.setItem(i, 0, QTableWidgetItem(str(plan.semana)))
                self.table_widget.setItem(i, 1, QTableWidgetItem(plan.dia))
                self.table_widget.setItem(i, 2, QTableWidgetItem(plan.disciplina))
                self.table_widget.setItem(i, 3, QTableWidgetItem(plan.descripcion))
                self.table_widget.setItem(i, 4, QTableWidgetItem(str(plan.duracion_min)))
                self.table_widget.setItem(i, 5, QTableWidgetItem(str(plan.distancia_km)))

        else:
            QMessageBox.warning(self, "Error", "No se ha encontrado el usuario.")

        db.close()

    def registrar_actividad(self):
        QMessageBox.information(self, "Registrar Actividad", "Aquí podrás registrar una nueva actividad.")

    def comprobar_progreso(self):
        QMessageBox.information(self, "Comprobar Progreso", "Aquí podrás ver tu progreso.")

    def cerrar_sesion(self):
        self.close()
