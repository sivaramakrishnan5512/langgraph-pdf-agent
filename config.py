"""
Application configuration and constants
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==================== Directory Configuration ====================
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
SRC_DIR = PROJECT_ROOT / "src"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# ==================== API Configuration ====================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))

# Validation
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables")

# ==================== PDF Processing Configuration ====================
PDF_CHUNK_SIZE = 1000
PDF_CHUNK_OVERLAP = 200
MAX_PDF_SIZE_MB = 50  # Maximum allowed PDF size in MB

# ==================== Vector Store Configuration ====================
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
RETRIEVAL_K = 4  # Number of documents to retrieve

# ==================== Workflow Configuration ====================
MAX_RETRIES = 2
TIMEOUT_SECONDS = 60

# ==================== Logging Configuration ====================
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = LOGS_DIR / "app.log"

# ==================== UI Configuration ====================
STREAMLIT_PAGE_TITLE = "PDF Story QA Assistant"
STREAMLIT_PAGE_ICON = "📖"
STREAMLIT_LAYOUT = "wide"

# ==================== Constants ====================
WORKFLOW_STATES = {
    "idle": "Waiting for input",
    "processing": "Processing request",
    "completed": "Request completed successfully",
    "error": "Error occurred"
}

WORKFLOW_STEPS = [
    "process_pdf",
    "summarize_story",
    "retrieve_context",
    "generate_answer"
]
