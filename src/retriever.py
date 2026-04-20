"""
Retrieval module for similarity-based document retrieval using FAISS
"""

import logging
from typing import List, Optional
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

logger = logging.getLogger(__name__)


class RAGRetriever:
    """Handles vector store creation and similarity retrieval"""
    
    def __init__(self):
        try:
            # Initialize HuggingFace embeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
            logger.info("Initialized HuggingFace embeddings")
        except Exception as e:
            logger.error(f"Error initializing embeddings: {str(e)}")
            self.embeddings = None
        
        self.vector_store = None
        self.retriever = None
    
    def create_vector_store(self, chunks: List[str]) -> bool:
        """
        Create FAISS vector store from document chunks
        
        Args:
            chunks: List of text chunks
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.embeddings:
                logger.error("Embeddings not initialized")
                return False
            
            if not chunks:
                logger.error("No chunks provided")
                return False
            
            # Create FAISS vector store
            self.vector_store = FAISS.from_texts(
                texts=chunks,
                embedding=self.embeddings,
                metadatas=[{"chunk_index": i} for i in range(len(chunks))]
            )
            
            # Create retriever with 4 documents returned by default
            self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 4})
            
            logger.info(f"Created vector store with {len(chunks)} chunks")
            return True
        except Exception as e:
            logger.error(f"Error creating vector store: {str(e)}")
            return False
    
    def retrieve_relevant_context(self, query: str, k: int = 4) -> List[str]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: User query
            k: Number of documents to retrieve
            
        Returns:
            List of relevant document chunks
        """
        try:
            if not self.vector_store:
                logger.error("Vector store not initialized")
                return []
            
            # Retrieve documents
            docs = self.vector_store.similarity_search(query, k=k)
            
            # Extract text content
            results = [doc.page_content for doc in docs]
            logger.info(f"Retrieved {len(results)} documents for query")
            
            return results
        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            return []
    
    def is_initialized(self) -> bool:
        """Check if retriever is ready"""
        return self.vector_store is not None and self.retriever is not None
