import fitz  # PyMuPDF
import os

from langchain.document_loaders import PyMuPDFLoader

def extract_text_from_pdf(pdf_path):
    # Initialize the PDF loader
    loader = PyMuPDFLoader(pdf_path)
    
    # Load the documents
    documents = loader.load()
    
    # Extract and return the text
    text = ""
    for doc in documents:
        text += doc.page_content + "\n"  # Adding a newline for readability
    
    return text

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
abs_file_path = os.path.join(script_dir, 'prompt.txt')


def read_file():
    with open(abs_file_path, 'r') as f:
        file_prompt = f.read()
        return file_prompt


def append_prompt(input: str):
    file_prompt = read_file()
    new_propmt = f"{file_prompt}\n[Question] {input}"
    return new_propmt

def update_file(input: str, output:str):
    with open(abs_file_path, 'a') as f:
        f.write(f'\n [Question]: {input}\n [Answer]: {output}\n')

def add_context_to_file(input:str):
    with open(abs_file_path, 'a') as f:
        f.write(f'\n\n[Document Data]\n {input} \n[End Of Document Data]\n\n')

def clear_file():
    with open(abs_file_path, 'w') as f:
        instructions ="Your job is the answer questions related to the query of the user in context of the text document below. If there is no right answer, your answer is \"I do not know\". Always make your answer short"
        f.write(instructions)
