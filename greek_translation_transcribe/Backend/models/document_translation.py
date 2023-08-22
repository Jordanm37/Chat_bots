from PyPDF2 import PdfReader
from docx import Document

class DocumentTranslation(Translation):
    '''Class to translate pdf documents into English from Greek'''
    # Inherits from the Translation class
    def __init__(self, source_language, target_language):
        super().__init__(source_language, target_language)

    def translate_document(self, file):
        '''Function to translate a given document from Greek to English and extract key words'''
        
        logger.info("Starting document translation...")
        
        document_type = os.path.splitext(file.name)[1][1:]
        logger.info(f"Document type: {document_type}")
        
        text = self.open_pdf(file.name) if 'pdf' in document_type else self.open_word(file.name)
        logger.info(f"Document text: {text}")
        
        translation, key_words = super().translate(text)
        
        return translation, key_words
        
    def open_pdf(self, pdf_path):
        '''Opens a pdf file and extracts the text'''
        
        pdf = PdfReader(pdf_path)
        text = ""
        for page in range(len(pdf.pages)):
            text += pdf.pages[page].extract_text()
        
        return text
           
    def open_word(self, word_path):
        '''Opens a word file and extracts the text'''
        
        document = Document(word_path)
        text = ""
        for para in document.paragraphs:
            text += para.text
        
        return text
    
    # def chunk_text(self, text):
    #     '''Chunks the text into smaller pieces'''
    #     pass
    
       