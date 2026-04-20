"""
State definition for the PDF QA application using LangGraph
Implements explicit state machine for multi-step workflow
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from langchain_core.messages import BaseMessage


@dataclass
class PDFQAState:
    """
    State definition for PDF QA workflow.
    Maintains the full execution context and history.
    """
    # Document management
    pdf_path: Optional[str] = None
    document_chunks: List[str] = field(default_factory=list)
    raw_content: Optional[str] = None
    story_summary: Optional[str] = None
    
    # Chat and retrieval
    query: Optional[str] = None
    retrieved_context: List[str] = field(default_factory=list)
    chat_history: List[Dict[str, str]] = field(default_factory=list)
    
    # Generation
    generated_response: Optional[str] = None
    
    # Status and tracking
    workflow_status: str = "idle"  # idle, processing, completed, error
    error_message: Optional[str] = None
    
    # Metadata for traceability
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_chat_message(self, role: str, content: str):
        """Add a message to chat history"""
        self.chat_history.append({"role": role, "content": content})
    
    def get_chat_history_str(self) -> str:
        """Get chat history as formatted string"""
        history = ""
        for msg in self.chat_history:
            role = msg["role"].upper()
            content = msg["content"]
            history += f"\n{role}: {content}"
        return history
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary for serialization"""
        return {
            "pdf_path": self.pdf_path,
            "document_chunks": self.document_chunks,
            "raw_content": self.raw_content[:500] if self.raw_content else None,
            "story_summary": self.story_summary,
            "query": self.query,
            "retrieved_context": self.retrieved_context,
            "chat_history": self.chat_history,
            "generated_response": self.generated_response,
            "workflow_status": self.workflow_status,
            "error_message": self.error_message,
            "metadata": self.metadata,
        }
