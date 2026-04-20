"""
Setup script for PDF QA Application
Helps users set up and verify the environment
"""

import os
import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent


def print_header(title):
    """Print formatted header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)


def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ Python 3.10+ required")
        return False
    print("✅ Python version OK")
    return True


def check_virtual_env():
    """Check if virtual environment is activated"""
    print_header("Checking Virtual Environment")
    
    venv_path = PROJECT_ROOT / "myenvAI"
    
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment is activated")
        return True
    else:
        if venv_path.exists():
            print("⚠️  Virtual environment exists but not activated")
            print(f"\nActivate it with:")
            print(f"  Windows: myenvAI\\Scripts\\activate.bat")
            print(f"  Linux/Mac: source myenvAI/bin/activate")
        else:
            print("❌ Virtual environment not found")
            print(f"\nCreate it with:")
            print(f"  python -m venv myenvAI")
        return False


def check_requirements():
    """Check if required packages are installed"""
    print_header("Checking Required Packages")
    
    required_packages = [
        'langchain',
        'langchain_core',
        'langchain_community',
        'langchain_groq',
        'langchain_huggingface',
        'langgraph',
        'streamlit',
        'pypdf',
        'faiss',
        'dotenv',
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED")
            all_installed = False
    
    if not all_installed:
        print("\n⚠️  Some packages are missing. Install with:")
        print(f"  pip install -r requirements.txt")
    
    return all_installed


def check_env_file():
    """Check if .env file exists and has required keys"""
    print_header("Checking Environment Configuration")
    
    env_file = PROJECT_ROOT / ".env"
    
    if not env_file.exists():
        print("❌ .env file not found")
        print("\nCreate .env file with:")
        print("  GROQ_API_KEY=your_api_key_here")
        print("  MODEL_NAME=llama-3.1-8b-instant")
        return False
    
    print("✅ .env file found")
    
    # Check for required keys
    with open(env_file) as f:
        content = f.read()
    
    required_keys = ['GROQ_API_KEY']
    all_present = True
    
    for key in required_keys:
        if key in content:
            print(f"✅ {key} present")
        else:
            print(f"❌ {key} missing")
            all_present = False
    
    return all_present


def check_project_structure():
    """Check if required directories and files exist"""
    print_header("Checking Project Structure")
    
    required_items = {
        'src': {'type': 'dir'},
        'src/__init__.py': {'type': 'file'},
        'src/state.py': {'type': 'file'},
        'src/pdf_processor.py': {'type': 'file'},
        'src/retriever.py': {'type': 'file'},
        'src/llm_client.py': {'type': 'file'},
        'src/workflow.py': {'type': 'file'},
        'app.py': {'type': 'file'},
        'config.py': {'type': 'file'},
        'requirements.txt': {'type': 'file'},
        'README.md': {'type': 'file'},
        'data': {'type': 'dir'},
        'logs': {'type': 'dir'},
    }
    
    all_present = True
    for item, props in required_items.items():
        path = PROJECT_ROOT / item
        item_type = props['type']
        
        if item_type == 'dir':
            exists = path.is_dir()
        else:
            exists = path.is_file()
        
        status = "✅" if exists else "❌"
        print(f"{status} {item}")
        
        if not exists:
            all_present = False
    
    return all_present


def test_imports():
    """Test if key modules can be imported"""
    print_header("Testing Module Imports")
    
    test_modules = {
        'langchain': 'LangChain',
        'langgraph': 'LangGraph',
        'streamlit': 'Streamlit',
        'pypdf': 'PyPDF',
        'faiss': 'FAISS',
    }
    
    all_ok = True
    for module, name in test_modules.items():
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError as e:
            print(f"❌ {name}: {str(e)}")
            all_ok = False
    
    return all_ok


def install_dependencies():
    """Install dependencies from requirements.txt"""
    print_header("Installing Dependencies")
    
    req_file = PROJECT_ROOT / "requirements.txt"
    
    if not req_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    print("Running: pip install -r requirements.txt")
    print("This may take a few minutes...")
    
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", str(req_file)],
        cwd=PROJECT_ROOT
    )
    
    return result.returncode == 0


def print_next_steps():
    """Print next steps for the user"""
    print_header("Next Steps")
    
    print("\n1. Ensure virtual environment is activated:")
    print("   Windows: myenvAI\\Scripts\\activate.bat")
    print("   Linux/Mac: source myenvAI/bin/activate")
    
    print("\n2. Verify all checks pass")
    
    print("\n3. Run the application:")
    print("   streamlit run app.py")
    
    print("\n4. Open your browser to:")
    print("   http://localhost:8501")
    
    print("\n5. Upload a PDF file to get started!")


def run_setup():
    """Run all setup checks"""
    print_header("PDF QA Application - Setup Checker")
    
    checks = [
        ("Python Version", check_python_version),
        ("Virtual Environment", check_virtual_env),
        ("Environment File", check_env_file),
        ("Project Structure", check_project_structure),
    ]
    
    results = {}
    
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results[check_name] = False
    
    # Check requirements if venv is active
    if results.get("Virtual Environment", False):
        results["Installed Packages"] = check_requirements()
        results["Module Imports"] = test_imports()
    
    # Summary
    print_header("Setup Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\n✅ Passed: {passed}/{total}")
    
    for check_name, result in results.items():
        status = "✅" if result else "❌"
        print(f"  {status} {check_name}")
    
    # Next steps
    print_next_steps()
    
    return all(results.values())


if __name__ == "__main__":
    success = run_setup()
    
    print("\n" + "="*80)
    if success:
        print("✅ Setup check completed successfully!")
        print("You're ready to run the application")
    else:
        print("⚠️  Some checks failed. Please address the issues above")
    print("="*80 + "\n")
    
    sys.exit(0 if success else 1)
