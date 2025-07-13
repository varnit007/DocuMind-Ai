from PyPDF2 import PdfReader
import io

def load_document(file):
    content = ""
    if file.name.endswith(".pdf"):
        pdf_reader = PdfReader(file)
        for page in pdf_reader.pages:
            content += page.extract_text()
    elif file.name.endswith(".txt"):
        stringio = io.StringIO(file.getvalue().decode("utf-8"))
        content = stringio.read()
    else:
        content = "Unsupported file format."
    return content
