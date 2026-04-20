# 🚀 Quick Start Guide

Welcome to the PDF Story QA Application! This guide will get you up and running in minutes.

## Prerequisites

- Python 3.10 or higher
- A Groq API key (already configured in `.env`)
- A PDF file you want to analyze

## 5-Minute Setup

### Step 1: Activate Virtual Environment

Open a terminal/PowerShell in the project directory and activate the virtual environment:

**Windows:**
```bash
myenvAI\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source myenvAI/bin/activate
```

### Step 2: Verify Setup (Optional)

Run the setup checker to verify everything is configured:

```bash
python setup.py
```

You should see "✅ Setup check completed successfully!"

### Step 3: Launch the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open automatically in your browser at `http://localhost:8501`

### Step 4: Upload and Analyze

1. **Upload PDF**: Drag and drop or click to upload your PDF file
2. **View Summary**: The story summary is generated automatically
3. **Ask Questions**: Type questions about the story
4. **Read Responses**: Get detailed answers based on the content
5. **Chat History**: All conversations are saved in the session

## Features

### 📄 PDF Processing
- Uploads PDF files securely
- Extracts and processes text automatically
- Creates searchable document chunks

### 📚 Story Analysis
- Generates automatic story summaries
- Extracts key plot points and characters
- Uses advanced AI (Groq LLM)

### 💬 Intelligent Q&A
- Answers questions about the story
- Uses context-aware retrieval (FAISS)
- Maintains conversation history

### 📊 Full Traceability
- Complete workflow tracking
- Processing metadata displayed
- Error handling and logging

## Usage Examples

### Example 1: Basic Story Summary
1. Upload `story.pdf`
2. Read the auto-generated summary
3. Understand the plot quickly

### Example 2: Character Questions
```
User: "Who is the main character?"
Assistant: [Provides detailed answer from the story]

User: "What are their personality traits?"
Assistant: [Extracts relevant information]
```

### Example 3: Plot Analysis
```
User: "What's the climax of the story?"
Assistant: [Identifies and explains the climax]

User: "How does the story end?"
Assistant: [Provides ending details]
```

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Clear chat | Press "Clear History" button |
| New PDF | Press "Reset Application" button |
| Submit question | Press Enter or click "Ask Question" |

## Troubleshooting

### Issue: "Streamlit command not found"
**Solution:** Make sure virtual environment is activated
```bash
myenvAI\Scripts\activate.bat  # Windows
source myenvAI/bin/activate    # Linux/Mac
```

### Issue: "GROQ_API_KEY not found"
**Solution:** Verify `.env` file exists and has the API key
```bash
cat .env  # Check the file
```

### Issue: "Failed to load PDF"
**Solution:** Make sure the PDF file is valid and not corrupted

### Issue: "No context retrieved"
**Solution:** This is normal. The system will still try to answer based on general knowledge.

## Project Structure

```
langchain-pdf/
├── src/
│   ├── state.py           # State management
│   ├── pdf_processor.py   # PDF handling
│   ├── retriever.py       # Vector search
│   ├── llm_client.py      # LLM interface
│   └── workflow.py        # LangGraph workflow
├── app.py                 # Streamlit UI
├── setup.py               # Setup checker
├── config.py              # Configuration
├── .env                   # API keys (secure)
├── requirements.txt       # Dependencies
└── README.md              # Full documentation
```

## What's Happening Behind the Scenes?

### The LangGraph Workflow

```
1. Upload PDF
   ↓
2. Extract text and create chunks (1000 tokens each)
   ↓
3. Generate story summary using Groq LLM
   ↓
4. Create vector embeddings (HuggingFace)
   ↓
5. User asks question
   ↓
6. Retrieve relevant chunks (FAISS)
   ↓
7. Generate answer using LLM + context
   ↓
8. Display answer and maintain history
```

### Key Technologies

- **LangGraph**: Workflow orchestration and state machine
- **Groq**: Fast LLM inference (llama-3.1-8b-instant)
- **FAISS**: Vector similarity search
- **HuggingFace**: Text embeddings
- **Streamlit**: Web interface

## Next Steps

### Try It Now
1. Find a PDF file (story, article, document)
2. Upload it to the application
3. Ask questions about the content
4. Explore the chat history

### Customize It
- Change chunk size in `src/pdf_processor.py`
- Adjust temperature in `app.py`
- Use different Groq models in `.env`
- Modify UI in `app.py`

### Extend It
- Add document type detection
- Implement multi-language support
- Create export functionality
- Build API endpoints
- Add user authentication

## Performance Tips

1. **First Load**: Larger PDFs take longer (1-2 minutes)
2. **Subsequent Queries**: 3-5 seconds per question
3. **Vector Store**: Created once per PDF, reused for all questions
4. **Memory**: Grows with chat history length

## Common Questions

**Q: Can I upload multiple PDFs?**
A: Yes, but you'll need to reset the application for each PDF.

**Q: How long can the chat history be?**
A: No limit, but very long histories may slow down responses.

**Q: Can I export the chat history?**
A: Not in the current version, but you can copy from the UI.

**Q: What PDF formats are supported?**
A: Currently PDF files (.pdf). Other formats require conversion first.

**Q: Is my data secure?**
A: Yes. All processing happens locally. PDFs are not stored.

## Need Help?

1. **Check README.md** for detailed documentation
2. **Run setup.py** to verify everything is working
3. **Check logs/** directory for error details
4. **Review demo.py** for code examples

## Resources

- [LangGraph Documentation](https://python.langchain.com/langgraph/)
- [Groq Console](https://console.groq.com/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [LangChain Docs](https://python.langchain.com/)

---

**Ready to analyze PDFs? Start with Step 1! 🚀**

**Questions?** Check README.md for comprehensive documentation.
