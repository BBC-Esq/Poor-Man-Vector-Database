from PySide6.QtCore import QRect, QPoint, QThread, Signal
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QLabel, QTextEdit, QFileDialog, 
                               QRadioButton, QButtonGroup)
from PySide6.QtGui import QFont
from PySide6.QtWebEngineWidgets import QWebEngineView
import markdown
import json
import subprocess
from pypdf import PdfReader
from docx import Document
from nltk.tokenize import sent_tokenize

class TextUtilities:
    def __init__(self):
        pass

    def pdf_to_text(self, pdf_file_path):
        reader = PdfReader(pdf_file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() if page.extract_text() else ''
        return text

    def docx_to_text(self, docx_file_path):
        doc = Document(docx_file_path)
        return ' '.join([paragraph.text for paragraph in doc.paragraphs])

    def txt_to_text(self, txt_file_path):
        with open(txt_file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text

    def clean_text(self, text):
        text = text.encode('utf-8', 'ignore').decode('utf-8')
        text = text.replace('\n', ' ')
        sentences = sent_tokenize(text)
        cleaned_text = ' '.join(sentences)
        return cleaned_text

def process_file(file_path):
    utilities = TextUtilities()
    text = ""
    if file_path.lower().endswith('.pdf'):
        text = utilities.pdf_to_text(file_path)
    elif file_path.lower().endswith('.docx'):
        text = utilities.docx_to_text(file_path)
    elif file_path.lower().endswith(('.txt', '.py', '.html', '.md')):
        text = utilities.txt_to_text(file_path)

    text = utilities.clean_text(text)
    return text

def get_completion(prompt, temperature=0.0, max_tokens=-1, prefix="[INST]", suffix="[/INST]"):
    formatted_prompt = f"{prefix}{prompt}{suffix}"

    data = {
        "messages": [{"role": "user", "content": formatted_prompt}],
        "stop": ["### Instruction:"],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False
    }

    curl_command = [
        'curl',
        'http://localhost:1234/v1/chat/completions',
        '-H', 'Content-Type: application/json',
        '-d', json.dumps(data)
    ]

    process = subprocess.Popen(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        response = json.loads(stdout)
        return response['choices'][0]['message']['content']
    else:
        raise Exception(f"Curl command failed with error: {stderr}")

class LLMWorker(QThread):
    finished = Signal(str)

    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt

    def run(self):
        try:
            response = get_completion(self.prompt)
            self.finished.emit(response)
        except Exception as e:
            self.finished.emit(f"Error: {str(e)}")

class DocQA_GUI(QWidget):
    def __init__(self):
        super(DocQA_GUI, self).__init__()

        self.load_stylesheet("style.css")

        screen_geom = QApplication.screens()[0].availableGeometry()
        start_x = (screen_geom.width() - 800) // 2
        start_y = (screen_geom.height() - 600) // 2
        self.setGeometry(QRect(QPoint(start_x, start_y), QPoint(start_x + 800, start_y + 600)))

        self.setWindowTitle("Poor Man's Vector Database - www.chintellalaw.com")

        self.last_dir = None
        self.cleaned_text = None
        self.llm_response = None

        layout = QVBoxLayout()

        self.web_view = QWebEngineView()
        self.text_view = QTextEdit()
        self.text_view.setReadOnly(True)
        layout.addWidget(self.web_view, 2)
        layout.addWidget(self.text_view, 2)
        self.text_view.hide()

        radio_layout = QHBoxLayout()
        self.radio_html = QRadioButton("HTML View")
        self.radio_html.setChecked(True)
        self.radio_html.toggled.connect(self.update_display)
        self.radio_text = QRadioButton("Text View")
        self.radio_text.toggled.connect(self.update_display)
        self.radio_markdown = QRadioButton("Markdown View")
        self.radio_markdown.toggled.connect(self.update_display)
        radio_layout.addWidget(self.radio_html)
        radio_layout.addWidget(self.radio_text)
        radio_layout.addWidget(self.radio_markdown)

        self.text_input = QTextEdit()
        font_input = QFont()
        font_input.setPointSize(13)
        self.text_input.setFont(font_input)
        layout.addWidget(self.text_input, 1)

        self.file_path_label = QLabel()
        layout.addWidget(self.file_path_label)

        bottom_layout = QHBoxLayout()
        btn_choose_document = QPushButton("Choose Document")
        btn_choose_document.clicked.connect(self.choose_document)
        self.btn_send_prompt = QPushButton("Send Prompt to LLM")
        self.btn_send_prompt.clicked.connect(self.send_prompt_to_llm)
        btn_clear = QPushButton("Clear Prompt")
        btn_clear.clicked.connect(self.clear_prompt)
        bottom_layout.addWidget(btn_choose_document)
        bottom_layout.addWidget(self.btn_send_prompt)
        bottom_layout.addWidget(btn_clear)

        layout.addLayout(radio_layout)
        layout.addLayout(bottom_layout)

        self.setLayout(layout)

    def load_stylesheet(self, path):
        with open(path, "r") as f:
            self.setStyleSheet(f.read())

    def choose_document(self):
        file_types = "Documents (*.pdf *.docx *.txt *.py *.html *.md);;All Files (*)"
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose Document", self.last_dir, file_types)
        if file_path:
            self.last_dir = '/'.join(file_path.split('/')[:-1])
            self.file_path_label.setText(file_path)
            self.cleaned_text = process_file(file_path)

    def clear_prompt(self):
        self.text_input.clear()

    def send_prompt_to_llm(self):
        if self.cleaned_text:
            user_prompt = self.text_input.toPlainText().strip()
            full_text = user_prompt + " " + self.cleaned_text
            self.btn_send_prompt.setEnabled(False)
            self.btn_send_prompt.setText("Processing...")
            self.worker = LLMWorker(full_text)
            self.worker.finished.connect(self.handle_llm_response)
            self.worker.start()

    def handle_llm_response(self, response):
        self.llm_response = response
        self.update_display()
        self.btn_send_prompt.setEnabled(True)
        self.btn_send_prompt.setText("Send Prompt to LLM")

    def update_display(self):
        if self.llm_response:
            if self.radio_html.isChecked():
                html_response = markdown.markdown(self.llm_response)
                html_with_style = f"<style>body {{ background-color: #2e333b; color: white; }}</style>{html_response}"
                self.web_view.setHtml(html_with_style)
                self.web_view.show()
                self.text_view.hide()
            elif self.radio_text.isChecked():
                self.text_view.setStyleSheet("background-color: #2e333b; color: white;")
                self.text_view.setText(self.llm_response)
                self.text_view.show()
                self.web_view.hide()
            elif self.radio_markdown.isChecked():
                html_response = markdown.markdown(self.llm_response)
                with open('github-markdown-dark.css', 'r') as css_file:
                    css_content = css_file.read()
                styled_html = f'''
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                    {css_content}
                    .markdown-body {{
                        box-sizing: border-box;
                        min-width: 200px;
                        margin: 0 auto;
                        padding: 45px;
                    }}
                </style>
                <article class="markdown-body">{html_response}</article>
                '''
                self.web_view.setHtml(styled_html)
                self.web_view.show()
                self.text_view.hide()