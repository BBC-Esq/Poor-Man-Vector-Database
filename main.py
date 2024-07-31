from PySide6.QtWidgets import QApplication
from gui import DocQA_GUI

if __name__ == "__main__":
    app = QApplication([])
    app.setStyle('Fusion')
    window = DocQA_GUI()
    window.show()
    app.exec()
