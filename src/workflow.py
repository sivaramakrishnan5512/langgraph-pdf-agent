"""
LangGraph workflow definition for PDF QA application
Implements explicit state machine with conditional paths and multi-step workflow
"""

import logging
from typing import Literal
from langgraph.graph import StateGraph, END
from src.state import PDFQAState
from src.pdf_processor import PDFProcessor
from src.retriever import RAGRetriever
from src.llm_client import PDFQALLMClient

logger = logging.getLogger(__name__)


class PDFQAWorkflow:
    """LangGraph-based workflow for PDF question answering"""
    
    def __init__(self):
        """Initialize workflow components"""
        self.pdf_processor = PDFProcessor()
        self.retriever = RAGRetriever()
        self.llm_client = PDFQALLMClient()
        self.graph = None
        self.answer_graph = None
        self._build_graph()
        self._build_answer_graph()
    
    def _build_graph(self):
        """Build the LangGraph state machine"""
        workflow = StateGraph(PDFQAState)
        
        # Add nodes representing workflow steps
        workflow.add_node("process_pdf", self._process_pdf_node)
        workflow.add_node("summarize_story", self._summarize_story_node)
        workflow.add_node("retrieve_context", self._retrieve_context_node)
        workflow.add_node("generate_answer", self._generate_answer_node)
        workflow.add_node("error_handler", self._error_handler_node)
        
        # Set entry point
        workflow.set_entry_point("process_pdf")
        
        # Add conditional edges for routing logic
        workflow.add_conditional_edges(
            "process_pdf",
            self._process_pdf_router,
            {
                "summarize": "summarize_story",
                "error": "error_handler"
            }
        )
        
        workflow.add_conditional_edges(
            "summarize_story",
            self._summarize_router,
            {
                "retrieve": "retrieve_context",
                "end": END,
                "error": "error_handler"
            }
        )
        
        workflow.add_edge("retrieve_context", "generate_answer")
        
        workflow.add_conditional_edges(
            "generate_answer",
            self._generate_router,
            {
                "end": END,
                "error": "error_handler"
            }
        )
        
        workflow.add_edge("error_handler", END)
        
        self.graph = workflow.compile()
        logger.info("LangGraph workflow built successfully")
    
    def _build_answer_graph(self):
        """Build a separate graph for answering questions (skips PDF processing)"""
        workflow = StateGraph(PDFQAState)
        
        # Add only the nodes needed for Q&A
        workflow.add_node("retrieve_context", self._retrieve_context_node)
        workflow.add_node("generate_answer", self._generate_answer_node)
        workflow.add_node("error_handler", self._error_handler_node)
        
        # Set entry point to retrieval (not PDF processing)
        workflow.set_entry_point("retrieve_context")
        
        # Add edges
        workflow.add_edge("retrieve_context", "generate_answer")
        
        workflow.add_conditional_edges(
            "generate_answer",
            self._generate_router,
            {
                "end": END,
                "error": "error_handler"
            }
        )
        
        workflow.add_edge("error_handler", END)
        
        self.answer_graph = workflow.compile()
        logger.info("LangGraph answer workflow built successfully")
    
    # ==================== Node Functions ====================
    
    def _process_pdf_node(self, state: PDFQAState) -> PDFQAState:
        """Process PDF and extract text chunks"""
        logger.info(f"[Node] Processing PDF: {state.pdf_path}")
        state.workflow_status = "processing"
        state.metadata["current_step"] = "process_pdf"
        
        try:
            if not state.pdf_path:
                state.workflow_status = "error"
                state.error_message = "No PDF path provided"
                return state
            
            raw_content, chunks = self.pdf_processor.process_pdf(state.pdf_path)
            
            if not raw_content:
                state.workflow_status = "error"
                state.error_message = "Failed to load PDF"
                return state
            
            state.raw_content = raw_content
            state.document_chunks = chunks
            state.metadata["total_chunks"] = len(chunks)
            state.metadata["content_length"] = len(raw_content)
            
            logger.info(f"[Node] PDF processed: {len(chunks)} chunks extracted")
            return state
        except Exception as e:
            state.workflow_status = "error"
            state.error_message = f"Exception in PDF processing: {str(e)}"
            logger.error(f"[Node] Exception in process_pdf: {str(e)}", exc_info=True)
            return state
    
    def _summarize_story_node(self, state: PDFQAState) -> PDFQAState:
        """Generate story summary from PDF content"""
        logger.info("[Node] Generating story summary")
        state.workflow_status = "processing"
        state.metadata["current_step"] = "summarize_story"
        
        try:
            if not state.raw_content:
                state.workflow_status = "error"
                state.error_message = "No content to summarize"
                return state
            
            summary = self.llm_client.generate_story_summary(state.raw_content)
            
            if not summary:
                state.workflow_status = "error"
                state.error_message = "Failed to generate summary"
                return state
            
            state.story_summary = summary
            state.add_chat_message("assistant", f"Story Summary:\n{summary}")
            # Mark as completed only for PDF processing (will be overridden if query exists)
            state.workflow_status = "completed"
            logger.info("[Node] Story summary generated")
            return state
        except Exception as e:
            state.workflow_status = "error"
            state.error_message = f"Exception in story summarization: {str(e)}"
            logger.error(f"[Node] Exception in summarize_story: {str(e)}", exc_info=True)
            return state
    
    def _retrieve_context_node(self, state: PDFQAState) -> PDFQAState:
        """Retrieve relevant context for query"""
        logger.info(f"[Node] Retrieving context for query: {state.query}")
        state.workflow_status = "processing"
        state.metadata["current_step"] = "retrieve_context"
        
        try:
            if not state.query:
                state.workflow_status = "error"
                state.error_message = "No query provided"
                return state
            
            # Create vector store if not already done
            if not self.retriever.is_initialized():
                if not self.retriever.create_vector_store(state.document_chunks):
                    state.workflow_status = "error"
                    state.error_message = "Failed to create vector store"
                    return state
            
            # Retrieve context
            context = self.retriever.retrieve_relevant_context(state.query, k=4)
            
            if not context:
                logger.warning("[Node] No context retrieved, continuing with empty context")
            
            state.retrieved_context = context
            state.metadata["context_chunks_retrieved"] = len(context)
            logger.info(f"[Node] Retrieved {len(context)} context chunks")
            return state
        except Exception as e:
            state.workflow_status = "error"
            state.error_message = f"Exception in context retrieval: {str(e)}"
            logger.error(f"[Node] Exception in retrieve_context: {str(e)}", exc_info=True)
            return state
    
    def _generate_answer_node(self, state: PDFQAState) -> PDFQAState:
        """Generate answer based on query and context"""
        logger.info("[Node] Generating answer")
        state.workflow_status = "processing"
        state.metadata["current_step"] = "generate_answer"
        
        try:
            if not state.query:
                state.workflow_status = "error"
                state.error_message = "No query available"
                return state
            
            chat_history = state.get_chat_history_str()
            answer = self.llm_client.answer_question(
                question=state.query,
                context=state.retrieved_context,
                chat_history=chat_history
            )
            
            if not answer:
                state.workflow_status = "error"
                state.error_message = "Failed to generate answer"
                return state
            
            state.generated_response = answer
            state.add_chat_message("assistant", answer)
            state.workflow_status = "completed"
            logger.info("[Node] Answer generated successfully")
            return state
        except Exception as e:
            state.workflow_status = "error"
            state.error_message = f"Exception in answer generation: {str(e)}"
            logger.error(f"[Node] Exception in generate_answer: {str(e)}", exc_info=True)
            return state
    
    def _error_handler_node(self, state: PDFQAState) -> PDFQAState:
        """Handle errors in workflow"""
        logger.error(f"[Node] Error handler invoked: {state.error_message}")
        state.workflow_status = "error"
        return state
    
    # ==================== Router Functions ====================
    
    def _process_pdf_router(self, state: PDFQAState) -> Literal["summarize", "error"]:
        """Route after PDF processing"""
        if state.workflow_status == "error" or not state.document_chunks:
            return "error"
        return "summarize"
    
    def _summarize_router(self, state: PDFQAState) -> Literal["retrieve", "end", "error"]:
        """Route after summarization - only retrieve if query exists"""
        if state.workflow_status == "error":
            return "error"
        # If there's a query, proceed to retrieval; otherwise end
        if state.query:
            return "retrieve"
        return "end"
    
    def _generate_router(self, state: PDFQAState) -> Literal["end", "error"]:
        """Route after answer generation"""
        if state.workflow_status == "error":
            return "error"
        return "end"
    
    # ==================== Public API ====================
    
    def _dict_to_state(self, state_dict: dict) -> PDFQAState:
        """Convert dictionary returned by graph.invoke() to PDFQAState object"""
        if isinstance(state_dict, PDFQAState):
            return state_dict
        
        state = PDFQAState(
            pdf_path=state_dict.get("pdf_path"),
            document_chunks=state_dict.get("document_chunks", []),
            raw_content=state_dict.get("raw_content"),
            story_summary=state_dict.get("story_summary"),
            query=state_dict.get("query"),
            retrieved_context=state_dict.get("retrieved_context", []),
            chat_history=state_dict.get("chat_history", []),
            generated_response=state_dict.get("generated_response"),
            workflow_status=state_dict.get("workflow_status", "idle"),
            error_message=state_dict.get("error_message"),
            metadata=state_dict.get("metadata", {})
        )
        return state
    
    def process_pdf(self, pdf_path: str) -> PDFQAState:
        """Process a PDF file and initialize the state"""
        logger.info(f"Starting PDF processing workflow for: {pdf_path}")
        initial_state = PDFQAState(pdf_path=pdf_path)
        result = self.graph.invoke(initial_state)
        
        # Convert dict result back to PDFQAState
        state_result = self._dict_to_state(result)
        logger.info(f"PDF processing completed with status: {state_result.workflow_status}")
        return state_result
    
    def answer_question(self, state: PDFQAState, question: str) -> PDFQAState:
        """Answer a question about the PDF content"""
        logger.info(f"Processing question: {question}")
        state.query = question
        state.metadata["current_step"] = "retrieve_context"
        
        # Run the answer workflow (retrieve + generate) without reprocessing PDF
        result = self.answer_graph.invoke(state)
        
        # Convert dict result back to PDFQAState
        state_result = self._dict_to_state(result)
        logger.info(f"Question processing completed with status: {state_result.workflow_status}")
        return state_result
    
    def get_graph_visualization(self):
        """Get graph structure for visualization"""
        return self.graph
