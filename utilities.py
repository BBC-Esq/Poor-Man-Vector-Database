import re
import fitz  # PyMuPDF
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
        # Remove non-utf-8 encodable characters
        text = text.encode('utf-8', 'ignore').decode('utf-8')
        
        # Remove newlines
        text = text.replace('\n', ' ')
        
        # Tokenize the text into sentences
        sentences = sent_tokenize(text)
        
        # Join the sentences into a single string with proper spacing
        cleaned_text = ' '.join(sentences)
        
        return cleaned_text

# Main function
def process_file(file_path):
    utilities = TextUtilities()
    text = ""
    if file_path.lower().endswith('.pdf'):
        text = utilities.pdf_to_text(file_path)
    elif file_path.lower().endswith('.docx'):
        text = utilities.docx_to_text(file_path)
    elif file_path.lower().endswith('.txt'):
        text = utilities.txt_to_text(file_path)

    # Cleaning the text
    text = utilities.clean_text(text)

    return text
