from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, QFileDialog
from PySide6.QtGui import QScreen, QFont
import utilities
import chat

class DocQA_GUI(QWidget):
    def __init__(self):
        super(DocQA_GUI, self).__init__()

        # Center GUI
        screen_geom = QApplication.screens()[0].availableGeometry()
        start_x = (screen_geom.width() - 800) // 2
        start_y = (screen_geom.height() - 600) // 2
        self.setGeometry(QRect(QPoint(start_x, start_y), QPoint(start_x + 800, start_y + 600)))

        self.setWindowTitle("Poor Man's Vector Database - www.chintellalaw.com")
        self.setStyleSheet("QMainWindow{background-color: darkgray;}")

        self.last_dir = None
        self.cleaned_text = None

        layout = QVBoxLayout()

        # Display path and file name
        self.file_path_label = QLabel()
        layout.addWidget(self.file_path_label)

        # Query
        self.text_input = QTextEdit()
        font_input = QFont()
        font_input.setPointSize(13)
        self.text_input.setFont(font_input)
        self.text_input.setStyleSheet("background-color: #2e333b; color: white;")
        layout.addWidget(self.text_input, 1)

        # LLM Response
        self.read_only_text = QTextEdit()
        self.read_only_text.setReadOnly(True)
        font_output = QFont()
        font_output.setPointSize(13)
        self.read_only_text.setFont(font_output)
        self.read_only_text.setStyleSheet("background-color: #092327; color: white;")
        layout.addWidget(self.read_only_text, 2)

        # Buttons
        bottom_layout = QHBoxLayout()
        btn_choose_document = QPushButton("Choose Document")
        btn_choose_document.clicked.connect(self.choose_document)
        btn_send_prompt = QPushButton("Send Prompt to LLM")
        btn_send_prompt.clicked.connect(self.send_prompt_to_llm)
        btn_clear = QPushButton("Clear Prompt")
        btn_clear.clicked.connect(self.clear_prompt)

        bottom_layout.addWidget(btn_choose_document)
        bottom_layout.addWidget(btn_send_prompt)
        bottom_layout.addWidget(btn_clear)
        layout.addLayout(bottom_layout)

        self.setLayout(layout)

    def choose_document(self):
        file_types = "Documents (*.pdf *.docx *.txt *.doc *.py *.rtf);;All Files (*)"
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose Document", self.last_dir, file_types)
        if file_path:
            self.last_dir = '/'.join(file_path.split('/')[:-1])
            self.file_path_label.setText(file_path)
            self.cleaned_text = utilities.process_file(file_path)

    def clear_prompt(self):
        self.text_input.clear()

    def send_prompt_to_llm(self):
        if self.cleaned_text:
            user_prompt = self.text_input.toPlainText().strip()
            full_text = user_prompt + " " + self.cleaned_text
            response = chat.get_completion(full_text)
            self.read_only_text.setText(response)

if __name__ == "__main__":
    app = QApplication([])
    app.setStyle('Fusion')
    window = DocQA_GUI()
    window.show()
    app.exec()
