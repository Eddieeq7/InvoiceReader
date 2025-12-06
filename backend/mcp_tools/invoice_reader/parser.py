"""
Invoice Parser Module

This module parses extracted OCR text into structured invoice data.
It uses regex pattern matching and text processing to identify and extract
key invoice fields such as invoice number, dates, vendor, line items,
and totals.

MCP Flow:
- Called by handler.py's extract() method after OCR
- Receives raw text from OCR module
- Applies parsing logic to structure the data
- Returns structured dictionary with invoice fields
"""

import re
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)


def parse_invoice(text: str) -> Dict[str, Any]:
    """
    Parse extracted OCR text into structured invoice data.
    
    This function analyzes the raw text from OCR and extracts structured
    invoice information including metadata, line items, and financial totals.
    It uses regex pattern matching to identify key fields.
    
    Args:
        text: Raw text content extracted from PDF via OCR
        
    Returns:
        Dictionary containing structured invoice data with extracted fields.
        Missing fields will have empty strings or 0.0 values.
        
    Raises:
        ValueError: If the text is empty or invalid
    """
    if not text or len(text.strip()) < 10:
        logger.warning("Text is too short or empty for parsing")
        raise ValueError("Insufficient text content for parsing")
    
    logger.info(f"Parsing invoice text ({len(text)} characters)")
    
    # Extract individual fields
    invoice_number = _extract_invoice_number(text)
    date = _extract_date(text)
    due_date = _extract_due_date(text)
    vendor = _extract_vendor(text)
    items = _extract_line_items(text)
    subtotal = _extract_subtotal(text)
    tax = _extract_tax(text)
    total = _extract_total(text)
    currency = _extract_currency(text)
    
    # Calculate confidence score
    confidence = _calculate_confidence(
        invoice_number, date, vendor, items, total
    )
    
    result = {
        "invoice_number": invoice_number,
        "date": date,
        "due_date": due_date,
        "vendor": vendor,
        "items": items,
        "subtotal": subtotal,
        "tax": tax,
        "total": total,
        "currency": currency,
        "metadata": {
            "confidence": confidence,
            "text_length": len(text),
            "items_found": len(items)
        }
    }
    
    logger.info(f"Parsing complete: {len(items)} items found, confidence: {confidence:.2f}")
    return result


def _extract_invoice_number(text: str) -> str:
    """Extract invoice number using common patterns."""
    patterns = [
        r'invoice\s*number\s*:?\s*([A-Z0-9-]+)',
        r'invoice\s*#?\s*:?\s*([A-Z0-9-]+)',
        r'inv\s*#?\s*:?\s*([A-Z0-9-]+)',
        r'#\s*([A-Z0-9-]{3,})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            invoice_num = match.group(1).strip()
            logger.debug(f"Found invoice number: {invoice_num}")
            return invoice_num
    
    logger.debug("No invoice number found")
    return ""


def _extract_date(text: str) -> str:
    """Extract invoice date using common date patterns."""
    patterns = [
        r'(?:invoice\s+)?date\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(?:invoice\s+)?date\s*:?\s*(\d{4}[/-]\d{1,2}[/-]\d{1,2})',
        r'(?:invoice\s+)?date\s*:?\s*([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})',
        r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            date_str = match.group(1).strip()
            logger.debug(f"Found date: {date_str}")
            return date_str
    
    logger.debug("No date found")
    return ""


def _extract_due_date(text: str) -> str:
    """Extract due date using common patterns."""
    patterns = [
        r'due\s+date\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'due\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'payment\s+due\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            due_date_str = match.group(1).strip()
            logger.debug(f"Found due date: {due_date_str}")
            return due_date_str
    
    logger.debug("No due date found")
    return ""


def _extract_vendor(text: str) -> str:
    """Extract vendor name from top of invoice."""
    # Try to find vendor in first few lines
    lines = text.split('\n')[:10]
    
    # Look for company indicators
    for line in lines:
        line = line.strip()
        if len(line) > 3 and not re.search(r'^\d', line):
            # Skip common headers
            if re.search(r'invoice|page|date|bill|ship', line, re.IGNORECASE):
                continue
            # First substantial line is often the vendor
            if len(line) > 5 and not line.startswith('-'):
                logger.debug(f"Found vendor: {line}")
                return line
    
    logger.debug("No vendor found")
    return ""


def _extract_line_items(text: str) -> List[Dict[str, Any]]:
    """Extract line items with descriptions, quantities, and prices."""
    items = []
    
    # Split text into lines
    lines = text.split('\n')
    
    # Pattern for tabular format: "Item Quantity Price Total"
    # Example: "Bananas 10 $0.60 $6.00"
    table_pattern = r'([A-Za-z\s]+?)\s+(\d+\.?\d*)\s+\$(\d+\.?\d*)\s+\$(\d+\.?\d*)'
    
    # Pattern with "x" separator: "10 x Apples @ $2.50 = $25.00"
    x_pattern = r'(\d+\.?\d*)\s+x\s+([A-Za-z\s]+?)\s+[@$]\s*\$?(\d+\.?\d*)\s+[=]?\s*\$(\d+\.?\d*)'
    
    for line in lines:
        line = line.strip()
        
        # Skip header lines and empty lines
        if not line or re.search(r'quantity|unit\s+price|description|item|total', line, re.IGNORECASE):
            continue
        
        # Try table format first
        match = re.search(table_pattern, line)
        if match:
            try:
                description = match.group(1).strip()
                quantity = float(match.group(2))
                unit_price = float(match.group(3))
                total = float(match.group(4))
                
                # Validate it's an actual item (not a total line)
                if not re.search(r'subtotal|tax|total|due', description, re.IGNORECASE):
                    items.append({
                        "description": description,
                        "quantity": quantity,
                        "unit_price": unit_price,
                        "total": total
                    })
                    logger.debug(f"Found item: {description} x{quantity} @ ${unit_price}")
            except (ValueError, IndexError) as e:
                logger.debug(f"Failed to parse line item: {e}")
                continue
        else:
            # Try "x" format
            match = re.search(x_pattern, line)
            if match:
                try:
                    quantity = float(match.group(1))
                    description = match.group(2).strip()
                    unit_price = float(match.group(3))
                    total = float(match.group(4))
                    
                    items.append({
                        "description": description,
                        "quantity": quantity,
                        "unit_price": unit_price,
                        "total": total
                    })
                    logger.debug(f"Found item: {description} x{quantity} @ ${unit_price}")
                except (ValueError, IndexError) as e:
                    logger.debug(f"Failed to parse line item: {e}")
                    continue
    
    logger.debug(f"Found {len(items)} line items")
    return items


def _extract_subtotal(text: str) -> float:
    """Extract subtotal amount."""
    patterns = [
        r'subtotal\s*:?\s*\$?(\d+\.?\d*)',
        r'sub-total\s*:?\s*\$?(\d+\.?\d*)',
        r'sub\s+total\s*:?\s*\$?(\d+\.?\d*)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                subtotal = float(match.group(1))
                logger.debug(f"Found subtotal: ${subtotal}")
                return subtotal
            except ValueError:
                continue
    
    logger.debug("No subtotal found")
    return 0.0


def _extract_tax(text: str) -> float:
    """Extract tax amount."""
    patterns = [
        r'tax\s*(?:\([\d.]+%\))?\s*:?\s*\$?(\d+\.?\d*)',
        r'sales\s+tax\s*:?\s*\$?(\d+\.?\d*)',
        r'vat\s*:?\s*\$?(\d+\.?\d*)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                tax = float(match.group(1))
                logger.debug(f"Found tax: ${tax}")
                return tax
            except ValueError:
                continue
    
    logger.debug("No tax found")
    return 0.0


def _extract_total(text: str) -> float:
    """Extract total amount."""
    patterns = [
        r'total\s+(?:amount\s+)?due\s*:?\s*\$?(\d+\.?\d*)',
        r'grand\s+total\s*:?\s*\$?(\d+\.?\d*)',
        r'total\s*:?\s*\$?(\d+\.?\d*)',
        r'amount\s+due\s*:?\s*\$?(\d+\.?\d*)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                total = float(match.group(1))
                logger.debug(f"Found total: ${total}")
                return total
            except ValueError:
                continue
    
    logger.debug("No total found")
    return 0.0


def _extract_currency(text: str) -> str:
    """Extract currency code or symbol."""
    # Look for currency codes
    currency_match = re.search(r'\b(USD|EUR|GBP|CAD|AUD)\b', text)
    if currency_match:
        return currency_match.group(1)
    
    # Default to USD if $ symbol is present
    if '$' in text:
        return "USD"
    
    return "USD"  # Default


def _calculate_confidence(
    invoice_number: str,
    date: str,
    vendor: str,
    items: List[Dict],
    total: float
) -> float:
    """Calculate confidence score based on extracted fields."""
    score = 0.0
    
    if invoice_number:
        score += 0.2
    if date:
        score += 0.2
    if vendor:
        score += 0.2
    if items:
        score += 0.2
    if total > 0:
        score += 0.2
    
    return score
