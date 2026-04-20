"""
Streamlit Web UI for PDF QA Application with Chat History
Provides user interface for PDF upload, question asking, and conversation management
"""

import os
import logging
import tempfile
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
from src.workflow import PDFQAWorkflow
from src.state import PDFQAState

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== Page Configuration ====================
st.set_page_config(
    page_title="PDF Story QA Assistant",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== Sidebar Configuration ====================
st.sidebar.title("📖 PDF Story QA Assistant")
st.sidebar.markdown("---")

# Add instructions
with st.sidebar.expander("ℹ️ How to use", expanded=False):
    st.markdown("""
    1. **Upload PDF**: Use the file uploader to select your PDF file
    2. **View Summary**: The story summary will be generated automatically
    3. **Ask Questions**: Type your questions about the story
    4. **Chat History**: All conversations are maintained in the session
    5. **Clear History**: Use the button below to reset the conversation
    """)

st.sidebar.markdown("---")

# ==================== Session State Management ====================
def initialize_session_state():
    """Initialize session state variables"""
    if "workflow" not in st.session_state:
        st.session_state.workflow = PDFQAWorkflow()
        logger.info("Initialized PDFQAWorkflow")
    
    if "current_state" not in st.session_state:
        st.session_state.current_state = None
    
    if "pdf_processed" not in st.session_state:
        st.session_state.pdf_processed = False
    
    if "uploaded_file_name" not in st.session_state:
        st.session_state.uploaded_file_name = None


def clear_conversation_history():
    """Clear the chat history and reset state"""
    if st.session_state.current_state:
        st.session_state.current_state.chat_history = []
        logger.info("Cleared conversation history")
    st.success("Conversation history cleared!")


def reset_application():
    """Reset entire application"""
    st.session_state.pdf_processed = False
    st.session_state.uploaded_file_name = None
    st.session_state.current_state = None
    logger.info("Application reset")
    st.success("Application reset! Upload a new PDF to continue.")


# Initialize session state
initialize_session_state()

# ==================== Main UI ====================

st.markdown("# 📖 PDF Story QA Assistant")
st.markdown("*Powered by LangGraph and Groq AI*")

# ==================== File Upload Section ====================
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("📤 Upload Your PDF")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type="pdf",
        help="Upload the PDF containing the story you want to analyze"
    )

with col2:
    st.subheader("🎛️ Controls")
    if st.button("🔄 Reset Application", use_container_width=True):
        reset_application()
    
    if st.button("🗑️ Clear History", use_container_width=True):
        clear_conversation_history()

# ==================== PDF Processing ====================
if uploaded_file is not None:
    # Check if a new file was uploaded
    if uploaded_file.name != st.session_state.uploaded_file_name:
        st.session_state.uploaded_file_name = uploaded_file.name
        st.session_state.pdf_processed = False
        st.session_state.current_state = None
    
    # Process PDF if not already processed
    if not st.session_state.pdf_processed:
        with st.spinner("📄 Processing PDF..."):
            # Save uploaded file to temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())
                temp_pdf_path = tmp_file.name
            
            try:
                # Process PDF using LangGraph workflow
                state = st.session_state.workflow.process_pdf(temp_pdf_path)
                st.session_state.current_state = state
                st.session_state.pdf_processed = True
                
                if state.workflow_status == "completed":
                    st.success(f"✅ PDF loaded successfully! ({len(state.document_chunks)} chunks)")
                    logger.info(f"PDF processed: {len(state.document_chunks)} chunks")
                else:
                    error_msg = state.error_message if state.error_message else "Unknown error occurred"
                    st.error(f"❌ Error processing PDF: {error_msg}")
                    logger.error(f"PDF processing failed: {error_msg}")
                    with st.expander("📋 Debug Information"):
                        st.write(f"**Status**: {state.workflow_status}")
                        st.write(f"**Chunks**: {len(state.document_chunks)}")
                        st.write(f"**Content Length**: {len(state.raw_content) if state.raw_content else 0}")
                        if state.metadata:
                            st.write(f"**Metadata**: {state.metadata}")
            
            except Exception as e:
                st.error(f"❌ Exception during PDF processing: {str(e)}")
                logger.error(f"Exception during PDF processing: {str(e)}", exc_info=True)
            
            finally:
                # Clean up temporary file
                if os.path.exists(temp_pdf_path):
                    os.remove(temp_pdf_path)
    
    # Display Story Summary
    if st.session_state.pdf_processed and st.session_state.current_state:
        state = st.session_state.current_state
        
        with st.expander("📚 Story Summary", expanded=True):
            if state.story_summary:
                st.markdown(state.story_summary)
            else:
                st.info("Summary will be displayed here once processing is complete.")
        
        # ==================== Question & Answer Section ====================
        st.subheader("❓ Ask Questions About the Story")
        
        # Question input
        user_question = st.text_input(
            "Type your question here:",
            placeholder="e.g., What is the main character's name? What happened at the end?",
            key="question_input"
        )
        
        # Submit button
        col1, col2 = st.columns([3, 1])
        
        with col2:
            submit_button = st.button("🔍 Ask Question", use_container_width=True)
        
        if submit_button and user_question:
            with st.spinner("⏳ Processing question..."):
                try:
                    # Process question through LangGraph workflow
                    updated_state = st.session_state.workflow.answer_question(state, user_question)
                    st.session_state.current_state = updated_state
                    
                    if updated_state.workflow_status == "completed":
                        logger.info("Question processed successfully")
                    else:
                        st.error(f"Error processing question: {updated_state.error_message}")
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    logger.error(f"Error processing question: {str(e)}")
        
        # ==================== Chat History Section ====================
        st.subheader("💬 Conversation History")
        
        if state.chat_history:
            # Display chat history
            chat_container = st.container()
            
            for message in state.chat_history:
                role = message["role"].lower()
                content = message["content"]
                
                if role == "user":
                    st.chat_message("user").write(content)
                else:
                    st.chat_message("assistant").write(content)
        else:
            st.info("No conversation yet. Ask a question to start!")
        
        # ==================== Metadata Section ====================
        with st.expander("📊 Processing Metadata", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Status", state.workflow_status.upper())
            
            with col2:
                st.metric("Total Chunks", len(state.document_chunks))
            
            with col3:
                st.metric("Chat Messages", len(state.chat_history))
            
            # Display metadata
            if state.metadata:
                st.markdown("**Workflow Metadata:**")
                for key, value in state.metadata.items():
                    st.write(f"- {key}: {value}")

else:
    # No file uploaded yet
    st.info("👈 Upload a PDF file to get started!")
    
    # Display some example instructions
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🚀 Features
        - **PDF Processing**: Extracts text from any PDF
        - **Story Analysis**: Automatically summarizes the story
        - **Smart Q&A**: Answers questions about the content
        - **Chat History**: Maintains conversation context
        - **Traceability**: Full workflow tracking
        """)
    
    with col2:
        st.markdown("""
        ### 🔧 Technical Stack
        - **LangGraph**: State machine & workflow
        - **Groq API**: Fast LLM inference
        - **FAISS**: Vector similarity search
        - **HuggingFace**: Embeddings
        - **Streamlit**: Web interface
        """)

# ==================== Footer ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <small>Built with LangGraph, Groq, and Streamlit | PDF QA Application v1.0</small>
</div>
""", unsafe_allow_html=True)
