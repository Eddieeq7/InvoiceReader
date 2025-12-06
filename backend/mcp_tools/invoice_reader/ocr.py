"""
OCR Module for Invoice Reader

This module handles optical character recognition (OCR) to extract text
from PDF invoice files. It uses a two-stage approach:
1. First attempts to extract text directly from PDF (for text-based PDFs)
2. Falls back to image-based OCR using Tesseract (for scanned PDFs)

MCP Flow:
- Called by handler.py's extract() method
- Processes the PDF file at the given URL/path
- Returns raw text content for parsing
"""

import os
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_text(file_url: str) -> str:
    """
    Extract text content from a PDF invoice file using OCR.
    
    This function uses a two-stage approach:
    1. First tries to extract text directly from PDF using pdfplumber
    2. If no text found, falls back to image-based OCR with pytesseract
    
    Args:
        file_url: URL or file path to the PDF invoice file
        
    Returns:
        Extracted text content from the PDF as a string.
        Multi-page documents will have pages separated by newlines.
        Returns empty string if extraction fails.
        
    Raises:
        FileNotFoundError: If the file cannot be found at the given path
        ValueError: If the file is not a valid PDF or cannot be processed
    """
    # Validate file exists
    if not os.path.exists(file_url):
        logger.error(f"File not found: {file_url}")
        raise FileNotFoundError(f"PDF file not found: {file_url}")
    
    if not file_url.lower().endswith('.pdf'):
        logger.error(f"File is not a PDF: {file_url}")
        raise ValueError(f"File must be a PDF: {file_url}")
    
    logger.info(f"Starting text extraction from: {file_url}")
    
    # Stage 1: Try direct text extraction from PDF
    text = _extract_text_from_pdf(file_url)
    
    # Stage 2: Fallback to image-based OCR if no text found
    if not text or len(text.strip()) < 10:
        logger.info("No extractable text found, falling back to image-based OCR")
        text = _extract_text_from_images(file_url)
    
    if text:
        logger.info(f"Successfully extracted {len(text)} characters")
    else:
        logger.warning("No text could be extracted from PDF")
    
    return text


def _extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text directly from PDF using pdfplumber.
    Works best for text-based PDFs (not scanned images).
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        Extracted text or empty string if extraction fails
    """
    try:
        import pdfplumber
        
        text_content = []
        with pdfplumber.open(file_path) as pdf:
            logger.info(f"PDF has {len(pdf.pages)} pages")
            
            for page_num, page in enumerate(pdf.pages, start=1):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(f"--- Page {page_num} ---\n{page_text}")
                        logger.debug(f"Extracted text from page {page_num}")
                except Exception as e:
                    logger.warning(f"Could not extract text from page {page_num}: {e}")
                    continue
        
        result = "\n\n".join(text_content)
        if result:
            logger.info(f"Direct PDF extraction successful: {len(result)} characters")
        return result
        
    except ImportError:
        logger.warning("pdfplumber not installed, skipping direct text extraction")
        return ""
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        return ""


def _extract_text_from_images(file_path: str) -> str:
    """
    Extract text from PDF using image-based OCR.
    Converts PDF pages to images, then uses Tesseract OCR.
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        Extracted text or empty string if OCR fails
    """
    try:
        from pdf2image import convert_from_path
        import pytesseract
        from PIL import Image
        
        logger.info("Converting PDF to images for OCR")
        
        # Convert PDF to images (one per page)
        images = convert_from_path(file_path)
        logger.info(f"Converted {len(images)} pages to images")
        
        text_content = []
        for page_num, image in enumerate(images, start=1):
            try:
                # Perform OCR on the image
                page_text = pytesseract.image_to_string(image)
                if page_text:
                    text_content.append(f"--- Page {page_num} ---\n{page_text}")
                    logger.debug(f"OCR completed for page {page_num}")
            except Exception as e:
                logger.warning(f"OCR failed for page {page_num}: {e}")
                continue
        
        result = "\n\n".join(text_content)
        if result:
            logger.info(f"Image-based OCR successful: {len(result)} characters")
        return result
        
    except ImportError as e:
        logger.error(f"Required OCR libraries not installed: {e}")
        logger.error("Install with: pip install pdf2image pytesseract pillow")
        logger.error("Also ensure Tesseract is installed: brew install tesseract (macOS)")
        return ""
    except Exception as e:
        logger.error(f"Error during image-based OCR: {e}")
        return ""

