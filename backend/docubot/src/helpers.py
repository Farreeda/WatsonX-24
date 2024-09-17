import fitz  # PyMuPDF
import os

from transformers import BartTokenizer, BartForConditionalGeneration
import torch
import textwrap


import mimetypes
from datetime import datetime
from mutagen.mp3 import MP3
import mutagen


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


def summarize_large_text(text, max_chunk_size=1024, max_summary_length=1024):
    """
    Summarizes large text by breaking it into smaller chunks and summarizing each chunk using BART.

    Parameters:
    - text (str): The large text to summarize.
    - max_chunk_size (int): The maximum number of tokens per chunk.
    - max_summary_length (int): The maximum length of the summary.

    Returns:
    - str: The final summarized text.
    """

    # Initialize the BART tokenizer and model
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

    # Tokenize the large text
    tokens = tokenizer.encode(text, return_tensors='pt')

    # Split tokens into chunks
    chunk_size = max_chunk_size
    chunks = [tokens[0][i:i + chunk_size] for i in range(0, len(tokens[0]), chunk_size)]

    # Summarize each chunk
    summaries = []
    for chunk in chunks:
        # Decode chunk to string
        chunk_text = tokenizer.decode(chunk, skip_special_tokens=True)
        
        # Generate summary
        inputs = tokenizer.encode(chunk_text, return_tensors='pt', max_length=chunk_size, truncation=True)
        summary_ids = model.generate(inputs, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        
        summaries.append(summary)

    # Combine chunk summaries into one final summary
    final_summary = ' '.join(summaries)

    return final_summary


def get_file_metadata(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    # Basic metadata
    file_size = os.path.getsize(file_path)
    modification_time = os.path.getmtime(file_path)
    mime_type, _ = mimetypes.guess_type(file_path)
    
    metadata = {
        'File Path': file_path,
        'File Size (bytes)': file_size,
        'Last Modification Time': datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S'),
        'MIME Type': mime_type
    }
    
    # File-specific metadata
    if mime_type and mime_type.startswith('image'):
        try:
            with Image.open(file_path) as img:
                metadata.update({
                    'Image Width': img.width,
                    'Image Height': img.height,
                    'Image Format': img.format,
                    'Image Mode': img.mode
                })
        except Exception as e:
            metadata['Image Metadata Error'] = str(e)
    
    elif mime_type and mime_type.startswith('audio'):
        try:
            audio = MP3(file_path, ID3=ID3)
            metadata.update({
                'Audio Duration (seconds)': audio.info.length,
                'Audio Bitrate (kbps)': audio.info.bitrate // 1000
            })
            # Additional metadata can be added here
        except Exception as e:
            metadata['Audio Metadata Error'] = str(e)
    
    elif mime_type and mime_type.startswith('video'):
        # For videos, you might need a more specialized library like moviepy or ffprobe
        metadata['Video Metadata'] = 'Detailed video metadata extraction not implemented in this example.'
    
    # Add more elif blocks here for other types of files (e.g., PDFs, Word docs)
    
    return metadata


def build_tree(directory, prefix=''):
    result = ""
    try:
        # Get a list of the directory's entries
        entries = os.listdir(directory)
        
        # Sort entries to ensure a consistent order
        entries.sort()
        
        # Initialize the current index
        last_index = len(entries) - 1
        
        # Iterate over all entries
        for index, entry in enumerate(entries):
            path = os.path.join(directory, entry)
            
            # Check if the entry is a directory
            if os.path.isdir(path):
                # Append the directory entry
                is_last = index == last_index
                connector = '└── ' if is_last else '├── '
                result += f'{prefix}{connector}{entry}\n'
                
                # Recursively build the contents of the directory
                new_prefix = f'{prefix}    ' if is_last else f'{prefix}│   '
                result += build_tree(path, new_prefix)
            else:
                # Append the file entry
                is_last = index == last_index
                connector = '└── ' if is_last else '├── '
                result += f'{prefix}{connector}{entry}\n'
                
    except PermissionError:
        result += f'{prefix}Permission denied\n'

    return result

