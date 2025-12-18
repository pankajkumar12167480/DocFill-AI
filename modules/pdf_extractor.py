"""
PDF Text Extraction Module
Extracts text content from PDF photo reports using PyMuPDF.
"""

import fitz  # PyMuPDF
from typing import List, Union
from io import BytesIO


def extract_text_from_pdf(pdf_source: Union[str, bytes, BytesIO]) -> str:
    """
    Extract all text content from a PDF file.
    
    Args:
        pdf_source: Either a file path (str), bytes, or BytesIO object
        
    Returns:
        Extracted text from all pages, separated by page markers
    """
    try:
        # Handle different input types
        if isinstance(pdf_source, str):
            doc = fitz.open(pdf_source)
        elif isinstance(pdf_source, bytes):
            doc = fitz.open(stream=pdf_source, filetype="pdf")
        elif isinstance(pdf_source, BytesIO):
            doc = fitz.open(stream=pdf_source.read(), filetype="pdf")
        else:
            raise ValueError(f"Unsupported PDF source type: {type(pdf_source)}")
        
        extracted_text = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")
            
            if text.strip():
                extracted_text.append(f"--- Page {page_num + 1} ---\n{text}")
        
        doc.close()
        
        return "\n\n".join(extracted_text)
    
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")


def extract_text_from_multiple_pdfs(pdf_files: List[tuple]) -> str:
    """
    Extract text from multiple PDF files and combine them.
    
    Args:
        pdf_files: List of tuples (filename, file_content_bytes)
        
    Returns:
        Combined text from all PDFs with file separators
    """
    all_text = []
    
    for filename, content in pdf_files:
        try:
            text = extract_text_from_pdf(content)
            if text.strip():
                all_text.append(f"=== Document: {filename} ===\n\n{text}")
        except Exception as e:
            all_text.append(f"=== Document: {filename} ===\n\n[ERROR: Could not extract text - {str(e)}]")
    
    return "\n\n" + "=" * 50 + "\n\n".join(all_text)


if __name__ == "__main__":
    # Test with a sample PDF
    import sys
    if len(sys.argv) > 1:
        text = extract_text_from_pdf(sys.argv[1])
        print(text)
