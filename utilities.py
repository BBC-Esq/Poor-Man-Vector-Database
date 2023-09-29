import re
import fitz
from docx import Document
from nltk.tokenize import sent_tokenize

class TextUtilities:

    def __init__(self):
        pass

    def pdf_to_text(self, pdf_file_path):
        with fitz.open(pdf_file_path) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
        return text

    def docx_to_text(self, docx_file_path):
        doc = Document(docx_file_path)
        return ' '.join([paragraph.text for paragraph in doc.paragraphs])

    def txt_to_text(self, txt_file_path):
        with open(txt_file_path, encoding='utf-8') as f:
            text = f.read()
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
    elif file_path.lower().endswith('.txt'):
        text = utilities.txt_to_text(file_path)

    text = utilities.clean_text(text)

    return text
