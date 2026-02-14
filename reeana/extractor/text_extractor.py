from io import BytesIO
import PyPDF2
import docx

class TextExtractor:
    """Extract text from resume files"""
    
    @staticmethod
    def extract_from_pdf(file_bytes: bytes) -> str:
        """Extract text from PDF"""
        pdf_file = BytesIO(file_bytes)
        reader = PyPDF2.PdfReader(pdf_file)
        
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    
    @staticmethod
    def extract_from_docx(file_bytes: bytes) -> str:
        """Extract text from DOCX"""
        doc_file = BytesIO(file_bytes)
        doc = docx.Document(doc_file)
        
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        
        return text.strip()
    
    @staticmethod
    def extract_from_txt(file_bytes: bytes) -> str:
        """Extract text from TXT"""
        return file_bytes.decode('utf-8')