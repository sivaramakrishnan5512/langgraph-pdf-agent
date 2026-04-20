"""
PDF processing utilities for document extraction and chunking
"""

import logging
from typing import List, Optional
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)


class PDFProcessor:
    """Handles PDF loading and text extraction"""
    
    def __init__(self):
        self.chunk_size = 1000
        self.chunk_overlap = 200
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def load_pdf(self, pdf_path: str) -> Optional[str]:
        """
        Load and extract text from PDF file
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content or None if error
        """
        try:
            reader = PdfReader(pdf_path)
            text_content = ""
            
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                text_content += f"\n--- Page {page_num + 1} ---\n"
                text_content += text
            
            logger.info(f"Successfully loaded PDF from {pdf_path}")
            logger.info(f"Total pages: {len(reader.pages)}")
            logger.info(f"Content length: {len(text_content)} characters")
            
            return text_content
        except Exception as e:
            logger.error(f"Error loading PDF: {str(e)}")
            return None
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into chunks
        
        Args:
            text: Raw text content
            
        Returns:
            List of text chunks
        """
        try:
            chunks = self.splitter.split_text(text)
            logger.info(f"Split text into {len(chunks)} chunks")
            return chunks
        except Exception as e:
            logger.error(f"Error chunking text: {str(e)}")
            return []
    
    def process_pdf(self, pdf_path: str) -> tuple[Optional[str], List[str]]:
        """
        Complete PDF processing pipeline: load and chunk
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Tuple of (raw_content, chunks)
        """
        raw_content = self.load_pdf(pdf_path)
        if not raw_content:
            return None, []
        
        chunks = self.chunk_text(raw_content)
        return raw_content, chunks
