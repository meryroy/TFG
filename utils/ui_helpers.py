from PySide6.QtWidgets import QMessageBox

def cargar_css(widget, ruta_css='css/style.css'):
    try:
        with open(ruta_css, 'r') as file:
            widget.setStyleSheet(file.read())
    except Exception as e:
        print(f"Error al cargar el CSS: {e}")
        QMessageBox.warning(widget, "Error de Estilo", f"No se pudo cargar el archivo CSS.\n{e}")
