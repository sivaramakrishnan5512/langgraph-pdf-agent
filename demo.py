"""
Example and demo script for the PDF QA Application
Shows how to use the LangGraph workflow programmatically
"""

import os
import sys
import logging
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.workflow import PDFQAWorkflow
from src.state import PDFQAState

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def example_basic_usage():
    """
    Example 1: Basic usage of the workflow
    Shows how to process a PDF and ask questions
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Usage")
    print("="*80)
    
    # Initialize workflow
    workflow = PDFQAWorkflow()
    logger.info("Workflow initialized")
    
    # Example PDF path (user would provide actual PDF)
    pdf_path = "sample.pdf"  # Replace with actual PDF path
    
    if not os.path.exists(pdf_path):
        print(f"⚠️  PDF file not found: {pdf_path}")
        print("Please provide an actual PDF file path")
        return None
    
    # Process PDF
    print(f"\n📄 Processing PDF: {pdf_path}")
    state = workflow.process_pdf(pdf_path)
    
    # Display results
    print(f"\n✅ Status: {state.workflow_status}")
    print(f"📊 Chunks created: {len(state.document_chunks)}")
    print(f"📝 Content length: {len(state.raw_content) if state.raw_content else 0}")
    
    if state.story_summary:
        print(f"\n📚 Story Summary:\n{state.story_summary[:200]}...")
    
    return state


def example_workflow_with_questions():
    """
    Example 2: Process PDF and ask multiple questions
    Demonstrates the full Q&A workflow
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: PDF Processing with Questions")
    print("="*80)
    
    workflow = PDFQAWorkflow()
    
    pdf_path = "sample.pdf"  # Replace with actual PDF
    
    if not os.path.exists(pdf_path):
        print(f"⚠️  PDF file not found: {pdf_path}")
        return None
    
    # Process PDF
    print(f"\n📄 Processing: {pdf_path}")
    state = workflow.process_pdf(pdf_path)
    
    if state.workflow_status != "completed":
        print(f"❌ Error: {state.error_message}")
        return None
    
    # Example questions
    questions = [
        "What is the main story about?",
        "Who are the main characters?",
        "What is the climax of the story?",
    ]
    
    # Ask questions
    for question in questions:
        print(f"\n❓ Question: {question}")
        state = workflow.answer_question(state, question)
        
        if state.workflow_status == "completed":
            print(f"✅ Answer: {state.generated_response}")
        else:
            print(f"❌ Error: {state.error_message}")
    
    return state


def example_state_inspection():
    """
    Example 3: Inspect and display the complete state
    Shows how to access state information for debugging/monitoring
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: State Inspection and Metadata")
    print("="*80)
    
    workflow = PDFQAWorkflow()
    pdf_path = "sample.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"⚠️  PDF file not found: {pdf_path}")
        return None
    
    state = workflow.process_pdf(pdf_path)
    
    # Display state information
    print("\n📊 State Information:")
    state_dict = state.to_dict()
    
    print(f"Workflow Status: {state_dict['workflow_status']}")
    print(f"Total Chunks: {len(state_dict['document_chunks'])}")
    print(f"Chat History Messages: {len(state_dict['chat_history'])}")
    
    print("\n📈 Metadata:")
    for key, value in state_dict['metadata'].items():
        print(f"  - {key}: {value}")
    
    # Display chat history structure
    if state_dict['chat_history']:
        print("\n💬 Chat History:")
        for i, msg in enumerate(state_dict['chat_history'], 1):
            role = msg['role'].upper()
            preview = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
            print(f"  {i}. {role}: {preview}")
    
    return state


def example_workflow_visualization():
    """
    Example 4: Understand the workflow graph structure
    Shows the LangGraph structure and node definitions
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: Workflow Graph Structure")
    print("="*80)
    
    workflow = PDFQAWorkflow()
    
    print("\n🔗 Workflow Steps:")
    print("  1. process_pdf: Extract text and create chunks")
    print("  2. summarize_story: Generate story summary using LLM")
    print("  3. retrieve_context: Find relevant chunks using FAISS")
    print("  4. generate_answer: Generate answer using LLM + context")
    print("  5. error_handler: Handle errors and log issues")
    
    print("\n📍 Router Functions:")
    print("  - process_pdf_router: Routes to summarize or error")
    print("  - summarize_router: Routes to retrieve or error")
    print("  - generate_router: Routes to end or error")
    
    print("\n🔄 Conditional Edges:")
    print("  - Success paths: PDF → Summary → Retrieve → Answer → END")
    print("  - Error paths: Any node → Error Handler → END")
    
    print("\n✅ State Variables Tracked:")
    state = PDFQAState()
    print(f"  - Document: {type(state.pdf_path).__name__}")
    print(f"  - Chunks: {type(state.document_chunks).__name__}")
    print(f"  - Query: {type(state.query).__name__}")
    print(f"  - Context: {type(state.retrieved_context).__name__}")
    print(f"  - History: {type(state.chat_history).__name__}")
    print(f"  - Status: {type(state.workflow_status).__name__}")
    print(f"  - Metadata: {type(state.metadata).__name__}")


def example_error_handling():
    """
    Example 5: Demonstrates error handling in the workflow
    Shows how the system handles various error conditions
    """
    print("\n" + "="*80)
    print("EXAMPLE 5: Error Handling")
    print("="*80)
    
    workflow = PDFQAWorkflow()
    
    # Test 1: Non-existent PDF
    print("\n🔴 Test 1: Non-existent PDF file")
    state = workflow.process_pdf("nonexistent.pdf")
    print(f"Status: {state.workflow_status}")
    print(f"Error: {state.error_message}")
    
    # Test 2: Empty query
    print("\n🔴 Test 2: Question without PDF processing")
    empty_state = PDFQAState()
    empty_state.query = "What is the story?"
    # This would fail in the retrieve_context node
    print("Would fail when trying to retrieve context without processed PDF")
    
    # Test 3: API key not set (if applicable)
    print("\n🔴 Test 3: Missing API credentials")
    print("Would fail during LLM initialization if GROQ_API_KEY is missing")


def print_instructions():
    """Print instructions for running examples"""
    print("\n" + "="*80)
    print("PDF QA Application - Demo Script")
    print("="*80)
    print("\nTo run the examples, you need a PDF file.")
    print("\nOptions:")
    print("1. Use the Streamlit UI: streamlit run app.py")
    print("2. Modify this script to use your PDF path")
    print("3. Run individual examples programmatically")
    print("\nExamples include:")
    print("  - Basic workflow usage")
    print("  - Multi-question Q&A")
    print("  - State inspection and metadata")
    print("  - Workflow graph visualization")
    print("  - Error handling demonstration")
    print("\n" + "="*80)


if __name__ == "__main__":
    print("\n" + "="*80)
    print("PDF QA Application - Demonstration & Examples")
    print("="*80)
    
    # Show workflow visualization (doesn't need a PDF)
    example_workflow_visualization()
    
    # Show error handling examples (doesn't need a PDF)
    example_error_handling()
    
    # Print instructions for other examples
    print_instructions()
    
    print("\n✅ Examples completed!")
    print("\nNext steps:")
    print("1. Prepare a PDF file")
    print("2. Update pdf_path in this script")
    print("3. Run: python demo.py")
    print("\nOr use the Streamlit UI:")
    print("  streamlit run app.py")
