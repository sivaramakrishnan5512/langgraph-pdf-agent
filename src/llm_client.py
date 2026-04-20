"""
LLM module for interacting with Groq API
"""

import logging
import os
from typing import Optional
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

logger = logging.getLogger(__name__)


class PDFQALLMClient:
    """Client for LLM interactions using Groq"""
    
    def __init__(self, model_name: str = "llama-3.1-8b-instant", temperature: float = 0.7):
        """
        Initialize Groq LLM client
        
        Args:
            model_name: Model to use
            temperature: Temperature for generation
        """
        try:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY not found in environment variables")
            
            self.llm = ChatGroq(
                temperature=temperature,
                model_name=model_name,
                api_key=api_key
            )
            logger.info(f"Initialized Groq LLM with model: {model_name}")
        except Exception as e:
            logger.error(f"Error initializing LLM: {str(e)}")
            self.llm = None
    
    def generate_story_summary(self, content: str) -> Optional[str]:
        """
        Generate a summary of the story from PDF content
        
        Args:
            content: Raw PDF content
            
        Returns:
            Story summary or None
        """
        try:
            if not self.llm:
                logger.error("LLM not initialized")
                return None
            
            # Limit content to prevent token overflow
            limited_content = content[:5000] if len(content) > 5000 else content
            
            system_message = SystemMessage(
                content="You are a helpful assistant that reads and summarizes stories from PDF documents. "
                       "Provide a concise but comprehensive summary of the story, highlighting the main plot, "
                       "characters, and key events."
            )
            
            user_message = HumanMessage(
                content=f"Please summarize the following story in 2-3 paragraphs:\n\n{limited_content}"
            )
            
            response = self.llm.invoke([system_message, user_message])
            summary = response.content
            logger.info("Generated story summary")
            return summary
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return None
    
    def answer_question(self, question: str, context: str, chat_history: str = "") -> Optional[str]:
        """
        Answer a question based on provided context
        
        Args:
            question: User question
            context: Retrieved context from documents
            chat_history: Previous conversation history
            
        Returns:
            Answer to the question or None
        """
        try:
            if not self.llm:
                logger.error("LLM not initialized")
                return None
            
            system_message = SystemMessage(
                content="You are a knowledgeable assistant that answers questions about a story "
                       "from a PDF document. Use the provided context and chat history to provide accurate, "
                       "helpful answers. If the answer is not in the provided context, say 'I don't have "
                       "information about that in the story.' Keep answers concise but informative."
            )
            
            context_str = "\n".join([f"- {chunk}" for chunk in context[:3]])  # Use top 3 chunks
            
            user_message = HumanMessage(
                content=f"Context from the story:\n{context_str}\n\n"
                       f"Chat History:\n{chat_history}\n\n"
                       f"Question: {question}"
            )
            
            response = self.llm.invoke([system_message, user_message])
            answer = response.content
            logger.info("Generated answer to question")
            return answer
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            return None
    
    def is_initialized(self) -> bool:
        """Check if LLM is ready"""
        return self.llm is not None
