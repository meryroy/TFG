
import os
import sys
from PySide6.QtWidgets import QApplication
from ui.inicio import PantallaInicio


from db.database import Base, engine
import db.modelos

print("DB path:", os.path.exists("data/entrenamiento.db"))
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = PantallaInicio()
    ventana.show()
    sys.exit(app.exec())

