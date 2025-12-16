"""
OCR Module for Invoice Reader

This module handles optical character recognition (OCR) to extract text
from PDF invoice files. It uses a multi-stage approach:
1. First attempts to extract text directly from PDF (for text-based PDFs)
2. Falls back to image-based OCR using Tesseract (for scanned PDFs)
3. Uses enhanced OCR configuration for better accuracy

MCP Flow:
- Called by handler.py's extract() method
- Processes the PDF file at the given URL/path
- Returns raw text content for parsing
"""

import os
import io
import logging
import tempfile
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_text(file_url: str) -> str:
    """
    Extract text content from a PDF invoice file using enhanced multi-stage OCR.
    
    This function uses an intelligent multi-stage approach:
    1. First tries to extract text directly from PDF using pdfplumber (fastest)
    2. If minimal text found, falls back to image-based OCR with Tesseract (most accurate)
    3. Uses enhanced extraction settings for better accuracy
    
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
    
    logger.info(f"Starting enhanced text extraction from: {file_url}")
    
    # Stage 1: Try direct text extraction from PDF (fast method)
    logger.info("Stage 1: Attempting direct PDF text extraction...")
    text = _extract_text_from_pdf(file_url)
    
    # Check if we got meaningful content
    if text and len(text.strip()) > 100:  # Threshold for meaningful content
        logger.info(f"✓ Direct extraction successful: {len(text)} characters")
        return text
    else:
        if text:
            logger.warning(f"Direct extraction yielded only {len(text.strip())} characters (below threshold)")
        else:
            logger.warning("Direct extraction failed or returned empty")
    
    # Stage 2: Fallback to image-based OCR (more accurate for scanned docs)
    logger.info("Stage 2: Falling back to image-based OCR (this may take longer)...")
    text = _extract_text_from_images(file_url)
    
    if text and len(text.strip()) > 50:
        logger.info(f"✓ OCR extraction successful: {len(text)} characters")
        return text
    else:
        logger.error("OCR extraction failed to extract meaningful text")
        if text:
            logger.warning(f"OCR returned only {len(text.strip())} characters")
        return text  # Return whatever we got, even if minimal
    
    return text


def _extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text directly from PDF using pdfplumber with enhanced extraction.
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
                    # Try multiple extraction methods for better results
                    page_text = page.extract_text()
                    
                    # If direct extraction fails, try extracting from layout
                    if not page_text or len(page_text.strip()) < 10:
                        # Try with layout preservation
                        page_text = page.extract_text(layout=True)
                    
                    # Also try to extract tables separately
                    tables = page.extract_tables()
                    table_text = ""
                    if tables:
                        for table in tables:
                            for row in table:
                                if row:
                                    # Join row cells with spaces
                                    row_text = " ".join([str(cell) if cell else "" for cell in row])
                                    if row_text.strip():
                                        table_text += row_text + "\n"
                    
                    # Combine regular text and table text
                    combined_text = ""
                    if page_text and page_text.strip():
                        combined_text += page_text
                    if table_text and table_text.strip():
                        combined_text += "\n" + table_text
                    
                    if combined_text.strip():
                        text_content.append(f"--- Page {page_num} ---\n{combined_text}")
                        logger.debug(f"Extracted {len(combined_text)} characters from page {page_num}")
                    else:
                        logger.warning(f"No text extracted from page {page_num}")
                        
                except Exception as e:
                    logger.warning(f"Could not extract text from page {page_num}: {e}")
                    continue
        
        result = "\n\n".join(text_content)
        if result and len(result.strip()) > 50:  # Threshold for meaningful content
            logger.info(f"Direct PDF extraction successful: {len(result)} characters")
            return result
        else:
            logger.warning("Direct PDF extraction yielded minimal text")
            return ""
        
    except ImportError:
        logger.warning("pdfplumber not installed, skipping direct text extraction")
        return ""
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        return ""


def _extract_text_from_images(file_path: str) -> str:
    """
    Extract text from PDF using image-based OCR with enhanced configuration.
    Converts PDF pages to images, then uses Tesseract OCR with optimized settings.
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        Extracted text or empty string if OCR fails
    """
    try:
        from pdf2image import convert_from_path
        import pytesseract
        from PIL import Image
        
        logger.info("Converting PDF to images for OCR...")
        
        # Use temporary directory for better cleanup
        with tempfile.TemporaryDirectory() as temp_dir:
            # Convert PDF to images with enhanced settings
            images = convert_from_path(
                file_path,
                dpi=300,  # Higher DPI for better quality
                output_folder=temp_dir,
                fmt='png',
                thread_count=4,  # Parallel processing
                grayscale=False  # Keep color for better detection
            )
            
            num_pages = len(images)
            logger.info(f"Converted {num_pages} pages to images")
            
            if num_pages == 0:
                logger.warning("PDF contained no pages for OCR")
                return ""
            
            text_content = []
            for page_num, image in enumerate(images, start=1):
                try:
                    # Enhanced OCR configuration for better accuracy
                    custom_config = r'--oem 3 --psm 6'  # LSTM + Assume uniform block of text
                    
                    # Perform OCR with English language
                    page_text = pytesseract.image_to_string(
                        image,
                        lang='eng',
                        config=custom_config
                    )
                    
                    if page_text and page_text.strip():
                        text_content.append(f"--- Page {page_num} (OCR) ---\n{page_text.strip()}")
                        logger.debug(f"OCR extracted {len(page_text)} characters from page {page_num}")
                    else:
                        logger.warning(f"No text detected via OCR on page {page_num}")
                        text_content.append(f"--- Page {page_num} (OCR) ---\n[No text detected]\n")
                        
                except pytesseract.TesseractError as ocr_err:
                    logger.error(f"Tesseract OCR failed for page {page_num}: {str(ocr_err)}")
                    text_content.append(f"--- Page {page_num} (OCR) ---\n[OCR Error: {str(ocr_err)}]\n")
                except Exception as e:
                    logger.warning(f"OCR failed for page {page_num}: {e}")
                    continue
            
            result = "\n\n".join(text_content)
            if result and len(result.strip()) > 50:
                logger.info(f"Image-based OCR successful: {len(result)} characters extracted")
                return result
            else:
                logger.warning("OCR completed but extracted minimal text")
                return result
        
    except ImportError as e:
        logger.error(f"Required OCR libraries not installed: {e}")
        logger.error("Install with: pip install pdf2image pytesseract pillow")
        logger.error("Also ensure Tesseract is installed: brew install tesseract (macOS)")
        return ""
    except Exception as e:
        logger.error(f"Error during image-based OCR: {e}")
        logger.error(f"Details: {type(e).__name__}: {str(e)}")
        return ""

