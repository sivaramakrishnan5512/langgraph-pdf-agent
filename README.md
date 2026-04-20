# 📖 PDF Story QA Application with LangGraph

A sophisticated multi-featured LangGraph application that reads PDFs, extracts stories, and answers questions about them using a graph-centric workflow architecture.

## 🎯 Features

### Core Functionality
- **PDF Processing**: Extracts and chunks text from PDF documents
- **Story Summarization**: Automatically generates summaries using Groq LLM
- **Question Answering**: Answers questions about the story with context retrieval
- **Chat History**: Maintains full conversation context across sessions
- **Web UI**: Interactive Streamlit interface for easy interaction

### LangGraph Concepts Implemented
- **Explicit State Machine**: Multi-step workflow with defined states and transitions
- **Fully Traceable**: Complete execution tracking and metadata logging
- **Multi-step Workflow**: Complex processing pipeline (PDF → Chunks → Summary → QA)
- **Conditional Paths**: Router functions for dynamic workflow branching
- **Graph-Centric Model**: Node-based architecture with clear dependencies

## 📁 Project Structure

```
langchain-pdf/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── state.py                 # PDFQAState definition
│   ├── pdf_processor.py         # PDF loading and chunking
│   ├── retriever.py             # FAISS vector store & retrieval
│   ├── llm_client.py            # Groq LLM client
│   └── workflow.py              # LangGraph workflow definition
├── app.py                       # Streamlit web UI
├── .env                         # Environment variables (API keys)
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── data/                        # Data storage directory
├── logs/                        # Application logs
└── myenvAI/                     # Virtual environment
```

## 🔧 Technical Stack

- **Framework**: LangGraph for workflow orchestration
- **LLM**: Groq API with llama-3.1-8b-instant model
- **Embeddings**: HuggingFace sentence-transformers
- **Vector Store**: FAISS for similarity search
- **PDF Processing**: PyPDF
- **Web UI**: Streamlit
- **Language**: Python 3.10+

## 🚀 Quick Start

### 1. Clone and Navigate
```bash
cd c:\D-drive\AI\langchain-pdf
```

### 2. Activate Virtual Environment
```bash
# Windows
myenvAI\Scripts\activate.bat

# Linux/Mac
source myenvAI/bin/activate
```

### 3. Install Dependencies (if not already done)
```bash
pip install -r requirements.txt
```

### 4. Verify Environment Variables
Check `.env` file contains:
```
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama-3.1-8b-instant
```

### 5. Run the Application
```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

## 📊 Workflow Architecture

### State Machine Flow
```
START
  ↓
[process_pdf] → Extract text and create chunks
  ↓
[summarize_story] → Generate story summary using LLM
  ↓
[retrieve_context] → Find relevant chunks using FAISS
  ↓
[generate_answer] → Answer question using LLM + context
  ↓
END
```

### Conditional Routing
- **PDF Processing**: Routes to summarization or error handling
- **Summarization**: Routes to retrieval or error handling
- **Answer Generation**: Routes to end or error handling
- **Error Handler**: Catches and logs errors, ensures graceful termination

## 🔄 How It Works

### 1. PDF Upload & Processing
- User uploads PDF file
- PDFProcessor extracts text using PyPDF
- Text is split into overlapping chunks (1000 tokens, 200 overlap)
- Chunks are stored in application state

### 2. Story Summarization
- LLM generates comprehensive story summary
- Summary added to chat history
- Vector embeddings created for all chunks using HuggingFace model

### 3. Question Answering
- User asks a question
- FAISS retrieves top 4 most similar chunks
- LLM generates answer using retrieved context + chat history
- Response added to chat history

### 4. Chat History Management
- All messages (system, user, assistant) stored in state
- Context maintained across multiple questions
- Users can clear history or reset application

## 📝 Usage Examples

### Example 1: Loading and Summarizing
1. Upload a PDF file
2. Application automatically:
   - Extracts text
   - Creates 50-100 chunks (depending on file size)
   - Generates a 2-3 paragraph summary
   - Creates vector embeddings

### Example 2: Asking Questions
```
User: "Who is the main character?"
Assistant: [Retrieves relevant chunks, generates answer]

User: "What happens in the climax?"
Assistant: [Uses chat history + new context to answer]

User: "How does it end?"
Assistant: [Maintains conversation context]
```

## 🎮 Web UI Features

### Main Interface
- **File Uploader**: Drag-and-drop or click to upload PDF
- **Story Summary**: Expandable section showing AI-generated summary
- **Question Input**: Text field for asking questions
- **Chat History**: Full conversation displayed with user/assistant labels
- **Metadata Display**: Shows processing statistics and workflow status

### Control Buttons
- **🔍 Ask Question**: Submit question for processing
- **🔄 Reset Application**: Clear all data and start fresh
- **🗑️ Clear History**: Remove chat history but keep PDF

### Expandable Sections
- **How to use**: Instructions and tips
- **Story Summary**: Full story summary from LLM
- **Processing Metadata**: Statistics about chunks, tokens, workflow status

## 📊 State Management

### PDFQAState Structure
```python
@dataclass
class PDFQAState:
    pdf_path: str              # Path to uploaded PDF
    document_chunks: List[str] # Text chunks from PDF
    raw_content: str           # Full extracted text
    story_summary: str         # LLM-generated summary
    
    query: str                 # Current user question
    retrieved_context: List    # FAISS retrieval results
    chat_history: List[Dict]   # Full conversation
    
    generated_response: str    # Answer to current question
    workflow_status: str       # idle, processing, completed, error
    error_message: str         # Error details if any
    metadata: Dict             # Execution metadata
```

## 🔍 Traceability

The application tracks the entire execution:

1. **Logging**: Each step logs its execution
2. **Metadata**: Stores chunk counts, content lengths, retrieval stats
3. **State History**: Full state maintained for inspection
4. **Error Tracking**: Errors captured with messages and logged

Example metadata captured:
```python
{
    "current_step": "generate_answer",
    "total_chunks": 47,
    "content_length": 15234,
    "context_chunks_retrieved": 4,
    "execution_time": 2.34  # seconds
}
```

## 🛠️ Customization

### Modify Chunk Size
Edit `pdf_processor.py`:
```python
self.chunk_size = 1000  # Change this
self.chunk_overlap = 200  # And this
```

### Change Retrieval Count
Edit `retriever.py`:
```python
self.retriever = self.vector_store.as_retriever(
    search_kwargs={"k": 4}  # Change from 4 to desired number
)
```

### Adjust Temperature (Creativity)
Edit `app.py` when initializing PDFQAWorkflow:
```python
PDFQALLMClient(temperature=0.5)  # Lower = more deterministic
```

### Use Different Model
Edit `.env`:
```
MODEL_NAME=llama-2-70b-chat  # Use different Groq model
```

## 📋 Requirements

See `requirements.txt` for complete list:
- langchain >= 1.2.0
- langchain-core >= 1.2.7
- langchain-community >= 0.3.0
- langchain-groq >= 0.2.0
- langchain-huggingface >= 1.2.0
- langgraph >= 0.2.0
- streamlit >= 1.41.0
- pypdf >= 4.2.0
- faiss-cpu >= 1.13.0
- python-dotenv >= 1.0.0

## 🐛 Troubleshooting

### Issue: "GROQ_API_KEY not found"
**Solution**: Make sure `.env` file exists in project root with valid API key

### Issue: "Failed to create vector store"
**Solution**: Check that HuggingFace embeddings are loaded and document chunks exist

### Issue: Streamlit not found
**Solution**: Activate virtual environment and ensure dependencies are installed:
```bash
myenvAI\Scripts\activate.bat
pip install -r requirements.txt
```

### Issue: "No context retrieved"
**Solution**: This is normal for very specific questions. The LLM will attempt to answer anyway.

## 📚 LangGraph Concepts Explained

### Explicit State Machine
- Defined states: idle, processing, completed, error
- Clear transitions between states
- Each node represents a processing step
- Conditional edges for branching logic

### Fully Traceable
- Every step logged with timestamp
- Metadata captured at each node
- Complete state history maintained
- Error messages with context

### Multi-step Workflow
1. PDF Processing (extract and chunk)
2. Summarization (LLM generates summary)
3. Retrieval (FAISS finds relevant chunks)
4. Generation (LLM answers question)

### Conditional Paths
- Router functions determine next node
- Branching based on success/failure
- Error handling path available at each step
- Alternative flows for edge cases

### Graph-Centric Model
- Nodes represent actions
- Edges represent flow transitions
- Conditional edges route based on state
- END node terminates execution

## 📈 Performance

Typical execution times:
- **PDF Loading**: 1-5 seconds (depends on file size)
- **Summarization**: 2-5 seconds (API call + LLM)
- **Question Processing**: 2-4 seconds (retrieval + generation)
- **First Load**: ~10 seconds (includes embeddings initialization)
- **Subsequent Queries**: ~3-5 seconds

## 🔐 Security

- API keys stored in `.env` (not in code)
- No sensitive data logged
- Temporary files cleaned up after use
- Vector store created in memory

## 📖 Additional Resources

- [LangGraph Documentation](https://python.langchain.com/langgraph/)
- [Groq API Docs](https://console.groq.com/docs/text-chat)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/)

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

Created as a demonstration of LangGraph concepts and modern LLM application architecture.

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest improvements
- Submit pull requests
- Add new features

---

**Happy PDF analyzing! 📖✨**
