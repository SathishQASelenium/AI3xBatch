import fs from 'node:fs'
import path from 'node:path'
// Import the inner module directly — pdf-parse's index.js runs a debug harness
// on import that looks for a test file and throws. The lib entry is clean.
import pdfParse from 'pdf-parse/lib/pdf-parse.js'

const SUPPORTED_EXT = ['.pdf', '.txt']

// Lists every supported document (*.pdf, *.txt) in the data directory.
export function listDocs(dataDir) {
  if (!fs.existsSync(dataDir)) return []
  return fs
    .readdirSync(dataDir)
    .filter((f) => SUPPORTED_EXT.includes(path.extname(f).toLowerCase()))
    .map((f) => ({ file: f, path: path.join(dataDir, f) }))
}

// Extracts raw text + page count from one PDF.
export async function extractPdf(filePath) {
  const buf = fs.readFileSync(filePath)
  const data = await pdfParse(buf)
  return {
    text: data.text || '',
    numPages: data.numpages || 0,
    info: data.info || {},
  }
}

// Extracts raw text from a plain-text file.
export function extractTxt(filePath) {
  const text = fs.readFileSync(filePath, 'utf-8')
  return { text, numPages: 1, info: {} }
}

// Dispatches to the right extractor based on file extension.
export async function extractDoc(filePath) {
  return path.extname(filePath).toLowerCase() === '.txt'
    ? extractTxt(filePath)
    : extractPdf(filePath)
}
