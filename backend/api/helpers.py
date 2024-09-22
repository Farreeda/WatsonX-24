import fitz  # PyMuPDF
import os

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
abs_file_path = os.path.join(script_dir, 'prompt.txt')


def read_file():
    with open(abs_file_path, 'r') as f:
        file_prompt = f.read()
        return file_prompt

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text.
    """
    text = ""
    try:
        # Open the PDF file
        pdf_document = fitz.open(pdf_path)

        # Iterate through each page
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()

        # Close the PDF document
        pdf_document.close()

    except Exception as e:
        print(f"An error occurred: {e}")

    return text

def append_prompt(input: str):
    file_prompt = read_file()
    new_propmt = f"{file_prompt}\n[Question] {input}"
    return new_propmt

def update_file(input: str, output:str):
    with open(abs_file_path, 'a') as f:
        f.write(f'\n Q: {input}\n A: {output}\n')
