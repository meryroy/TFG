import traceback
from PySide6.QtWidgets import QFileDialog, QMessageBox

def guardar_figura_como_imagen(parent_widget, figura):
    filename, _ = QFileDialog.getSaveFileName(
        parent_widget,
        "Guardar gráfico como imagen",
        "",
        "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;All Files (*)"
    )
    if filename:
        try:
            figura.savefig(filename)
            QMessageBox.information(parent_widget, "Guardado", f"Imagen guardada correctamente en:\n{filename}")
        except Exception as e:
            error_msg = traceback.format_exc()
            QMessageBox.critical(parent_widget, "Error", f"No se pudo guardar la imagen:\n{e}\n\n{error_msg}")
