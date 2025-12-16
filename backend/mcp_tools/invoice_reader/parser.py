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
    """Extract invoice number using enhanced common patterns."""
    patterns = [
        r'invoice\s*#\s*:?\s*([A-Z]{2,4}-\d{4}-\d{3,4})',  # Format: INV-2025-001
        r'invoice\s*number\s*:?\s*([A-Z0-9-]+)',
        r'invoice\s*#\s*:?\s*([A-Z0-9-]+)',
        r'inv(?:oice)?\s*#?\s*:?\s*([A-Z0-9-]+)',
        r'invoice\s*id\s*:?\s*([A-Z0-9-]+)',
        r'#\s*:?\s*([A-Z]{2,}-\d{4}-\d{3,})',  # Catches #: INV-2025-001
        r'#\s*([A-Z0-9-]{5,})',  # Generic # with at least 5 chars
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            invoice_num = match.group(1).strip()
            # Validate it's not just a date or something else
            if len(invoice_num) >= 3 and not invoice_num.replace('-', '').replace('/', '').isdigit():
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
    """Extract due date using enhanced common patterns including written months."""
    patterns = [
        # Written month formats: "February 25, 2025" or "Feb 25, 2025"
        r'due\s*:?\s*([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})',
        r'due\s+date\s*:?\s*([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})',
        r'payment\s+due\s*:?\s*([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})',
        # Numeric formats
        r'due\s+date\s*:?\s*(\d{4}-\d{1,2}-\d{1,2})',  # YYYY-MM-DD
        r'due\s+date\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',  # MM/DD/YYYY
        r'due\s*:?\s*(\d{4}-\d{1,2}-\d{1,2})',
        r'due\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'payment\s+due\s*:?\s*(\d{4}-\d{1,2}-\d{1,2})',
        r'payment\s+due\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'pay\s+by\s*:?\s*(\d{4}-\d{1,2}-\d{1,2})',
        r'pay\s+by\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
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
    """Extract vendor/company name from invoice using enhanced logic."""
    lines = text.split('\n')[:20]  # Look at more lines
    
    # Look for explicit vendor patterns first
    vendor_patterns = [
        r'(?:from|seller|vendor)\s*:?\s*([A-Z][A-Za-z\s&.,\'-]+(?:LLC|Inc|Ltd|Corp|Corporation|Co|Company|LLP|LP)?)',
        r'(?:bill\s+from|billed\s+by)\s*:?\s*([A-Z][A-Za-z\s&.,\'-]+)',
    ]
    
    for pattern in vendor_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            vendor = match.group(1).strip()
            # Clean up - remove any invoice number that might have been captured
            vendor = re.sub(r'\s+Invoice\s+#.*$', '', vendor, flags=re.IGNORECASE)
            logger.debug(f"Found vendor via pattern: {vendor}")
            return vendor
    
    # Fallback: Look for company name in first significant lines
    # Skip page markers, invoice headers, and look for company indicators
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Skip empty lines, page markers, and short lines
        if not line or len(line) < 5 or line.startswith('---'):
            continue
            
        # Skip lines that are clearly headers
        if re.search(r'^(invoice|page|date|bill\s+to|ship\s+to|from|to)', line, re.IGNORECASE):
            continue
            
        # Skip lines that are mostly numbers or symbols
        if re.search(r'^[\d\s\-:/#]+$', line):
            continue
        
        # Look for lines with company indicators (LLC, Inc, etc.)
        company_match = re.search(r'([A-Z][A-Za-z\s&.,\'-]*?\s+(?:LLC|Inc|Ltd|Corp|Corporation|Co\.|Company|LLP|LP))', line, re.IGNORECASE)
        if company_match:
            vendor = company_match.group(1).strip()
            # Clean up - stop at "Invoice" keyword if present
            if 'Invoice' in vendor or 'invoice' in vendor:
                vendor = vendor.split('Invoice')[0].strip()
                vendor = vendor.split('invoice')[0].strip()
            logger.debug(f"Found vendor with company indicator: {vendor}")
            return vendor
        
        # If we're in the first few lines and find a capitalized name, that's likely the vendor
        if i < 5 and re.match(r'^[A-Z][A-Za-z\s&.,\'-]+', line) and len(line) > 8:
            # Extract just the company name part, stop at invoice-related keywords
            vendor = line
            # Stop at "Invoice" keyword
            if 'Invoice' in vendor or 'invoice' in vendor:
                vendor = vendor.split('Invoice')[0].strip()
                vendor = vendor.split('invoice')[0].strip()
            # Make sure it's not an address or common header
            if not re.search(r'(?:street|avenue|road|drive|suite|floor|city|state|zip)', vendor, re.IGNORECASE):
                logger.debug(f"Found vendor as first company line: {vendor}")
                return vendor
    
    logger.debug("No vendor found")
    return ""


def _extract_line_items(text: str) -> List[Dict[str, Any]]:
    """Extract line items with enhanced pattern matching for various invoice formats."""
    items = []
    lines = text.split('\n')
    
    # Enhanced patterns for different invoice formats
    patterns = [
        # Format: "Description  Quantity lbs/units  Price  Total"
        # Example: "Bananas 10.0 lbs $0.60 $6.00"
        r'([A-Za-z][\w\s\-/()]*?)\s+(\d+\.?\d*)\s+(?:lbs?|units?|hrs?|pcs?)\s+\$([\d,]+\.?\d*)\s+\$([\d,]+\.?\d*)',
        
        # Format: "Description with Phase numbers"
        # Example: "Software Development - Phase 1 40.0 hrs $150.00 $6000.00"
        r'([A-Za-z][\w\s\-/()]+?)\s+(\d+\.?\d*)\s+(?:hrs?|units?|pcs?)\s+\$?([\d,]+\.?\d*)\s+\$([\d,]+\.?\d*)',
        
        # Format: "Description Quantity Rate Amount" (no unit specified)
        # Example: "UI/UX Design Services 20.0 $125.00 $2500.00"
        r'([A-Za-z][\w\s\-/()]+?)\s+(\d+\.?\d*)\s+\$?([\d,]+\.?\d*)\s+\$([\d,]+\.?\d*)',
        
        # Format: "Single-word item Quantity Price Total"
        # Example: "Bananas 10.0 $0.60 $6.00"
        r'([A-Za-z]+)\s+(\d+\.?\d*)\s+\$([\d,]+\.?\d*)\s+\$([\d,]+\.?\d*)',
        
        # Format with "x": "10 x Apples @ $2.50 = $25.00"
        r'(\d+\.?\d*)\s+x\s+([A-Za-z\s\-]+?)\s+[@$]\s*\$?([\d,]+\.?\d*)\s+[=]?\s*\$([\d,]+\.?\d*)',
        
        # Format with hrs first: "40.0 hrs Design Services $125.00 $2500.00"
        r'(\d+\.?\d*)\s*hrs?\s+([A-Za-z][\w\s\-/]+?)\s+\$([\d,]+\.?\d*)\s+\$([\d,]+\.?\d*)',
    ]
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines, headers, and separator lines
        if not line or len(line) < 5:
            continue
        if re.search(r'^(description|item|quantity|qty|rate|price|amount|total|---)', line, re.IGNORECASE):
            continue
        if line.count('-') > 10 or line.count('=') > 5:  # Separator lines
            continue
        
        # Try each pattern
        for i, pattern in enumerate(patterns):
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                try:
                    # Different patterns have groups in different orders
                    if i == 4 or i == 5:  # x format or hrs with qty first (quantity comes first)
                        quantity = float(match.group(1).replace(',', ''))
                        description = match.group(2).strip()
                        unit_price = float(match.group(3).replace(',', '').replace('$', ''))
                        total = float(match.group(4).replace(',', '').replace('$', ''))
                    else:  # Description first format (all other patterns)
                        description = match.group(1).strip()
                        quantity = float(match.group(2).replace(',', ''))
                        unit_price = float(match.group(3).replace(',', '').replace('$', ''))
                        total = float(match.group(4).replace(',', '').replace('$', ''))
                    
                    # Validate it's an actual item (not a subtotal/total line)
                    if re.search(r'(?:sub)?total|tax|due|balance|amount\s+due|grand', description, re.IGNORECASE):
                        continue
                    
                    # Validate reasonable values
                    if quantity > 0 and unit_price >= 0 and total >= 0:
                        items.append({
                            "description": description,
                            "quantity": quantity,
                            "unit_price": unit_price,
                            "total": total
                        })
                        logger.debug(f"Found item (pattern {i}): {description} x{quantity} @ ${unit_price} = ${total}")
                        break  # Found a match, move to next line
                        
                except (ValueError, IndexError, AttributeError) as e:
                    logger.debug(f"Failed to parse line item with pattern {i}: {e}")
                    continue
    
    logger.debug(f"Found {len(items)} line items")
    return items


def _extract_subtotal(text: str) -> float:
    """Extract subtotal amount with support for formatted numbers."""
    patterns = [
        r'subtotal\s*:?\s*\$?([\d,]+\.?\d*)',
        r'sub-total\s*:?\s*\$?([\d,]+\.?\d*)',
        r'sub\s+total\s*:?\s*\$?([\d,]+\.?\d*)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                # Remove commas and convert to float
                subtotal_str = match.group(1).replace(',', '')
                subtotal = float(subtotal_str)
                logger.debug(f"Found subtotal: ${subtotal:,.2f}")
                return subtotal
            except ValueError:
                continue
    
    logger.debug("No subtotal found")
    return 0.0


def _extract_tax(text: str) -> float:
    """Extract tax amount with support for formatted numbers and percentages."""
    patterns = [
        r'tax\s*(?:\([\d.]+%\))?\s*:?\s*\$?([\d,]+\.?\d*)',
        r'sales\s+tax\s*:?\s*\$?([\d,]+\.?\d*)',
        r'vat\s*:?\s*\$?([\d,]+\.?\d*)',
        r'gst\s*:?\s*\$?([\d,]+\.?\d*)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                # Remove commas and convert to float
                tax_str = match.group(1).replace(',', '')
                tax = float(tax_str)
                logger.debug(f"Found tax: ${tax:,.2f}")
                return tax
            except ValueError:
                continue
    
    logger.debug("No tax found")
    return 0.0


def _extract_total(text: str) -> float:
    """Extract total amount with support for formatted numbers, avoiding subtotal."""
    patterns = [
        # Use negative lookbehind to avoid matching "subtotal"
        r'(?<!sub)(?<!Sub)total\s*:?\s*\$?([\d,]+\.?\d*)',  # "TOTAL: $10,850.00" but not "Subtotal"
        r'total\s+due\s*:?\s*\$?([\d,]+\.?\d*)',
        r'amount\s+due\s*:?\s*\$?([\d,]+\.?\d*)',
        r'grand\s+total\s*:?\s*\$?([\d,]+\.?\d*)',
        r'balance\s+due\s*:?\s*\$?([\d,]+\.?\d*)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                # Remove commas and convert to float
                total_str = match.group(1).replace(',', '')
                total = float(total_str)
                # Validate it's a reasonable total (not too small)
                if total > 0:
                    logger.debug(f"Found total: ${total:,.2f}")
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
