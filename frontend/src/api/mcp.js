/**
 * MCP API Client
 * 
 * This module provides functions to interact with the Invoice Reader MCP server.
 * It handles file uploads and invoice extraction via JSON-RPC.
 */

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8001";

/**
 * Upload an invoice PDF file to the server
 * 
 * @param {File} file - The PDF file to upload
 * @returns {Promise<string>} The server-side file path (file_url)
 * @throws {Error} If upload fails
 */
export async function uploadInvoice(file) {
  if (!file) {
    throw new Error("No file provided");
  }

  if (!file.name.toLowerCase().endsWith('.pdf')) {
    throw new Error("Only PDF files are supported");
  }

  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: "Upload failed" }));
    throw new Error(error.error || `Upload failed with status ${response.status}`);
  }

  const data = await response.json();
  return data.file_url; // Server-side path
}

/**
 * Extract invoice data from a PDF using the MCP tool
 * 
 * @param {string} fileUrl - The server-side file path
 * @returns {Promise<Object>} The extracted invoice data
 * @throws {Error} If extraction fails
 */
export async function extractInvoice(fileUrl) {
  const payload = {
    jsonrpc: "2.0",
    method: "tools/call",
    params: {
      name: "extract_invoice",
      arguments: {
        file_url: fileUrl,
      },
    },
    id: Date.now(),
  };

  const response = await fetch(`${API_BASE}/mcp`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`MCP request failed with status ${response.status}`);
  }

  const data = await response.json();

  // Check for JSON-RPC errors
  if (data.error) {
    throw new Error(data.error.message || "MCP tool error");
  }

  // Extract the result from MCP response format
  const text = data?.result?.content?.[0]?.text;
  if (!text) {
    throw new Error("Invalid MCP response format");
  }

  // Parse the JSON string containing invoice data
  try {
    return JSON.parse(text);
  } catch (e) {
    throw new Error("Failed to parse invoice data");
  }
}

/**
 * Process an invoice file: upload and extract in one call
 * 
 * @param {File} file - The PDF file to process
 * @returns {Promise<Object>} The extracted invoice data
 * @throws {Error} If processing fails
 */
export async function processInvoice(file) {
  const fileUrl = await uploadInvoice(file);
  return await extractInvoice(fileUrl);
}

/**
 * List available MCP tools
 * 
 * @returns {Promise<Array>} List of available tools
 */
export async function listTools() {
  const payload = {
    jsonrpc: "2.0",
    method: "tools/list",
    params: {},
    id: Date.now(),
  };

  const response = await fetch(`${API_BASE}/mcp`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`Failed to list tools: ${response.status}`);
  }

  const data = await response.json();
  return data.result?.tools || [];
}

/**
 * Check server health
 * 
 * @returns {Promise<Object>} Server health status
 */
export async function checkHealth() {
  const response = await fetch(`${API_BASE}/health`);
  
  if (!response.ok) {
    throw new Error("Server health check failed");
  }

  return await response.json();
}

