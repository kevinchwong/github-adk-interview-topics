#!/bin/bash

# Software Interview Topics Generator Setup Script
# GitHub Actions + Google ADK + MongoDB on Railway

set -e

echo "🚀 Setting up GitHub ADK Interview Topics Generator..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

# Check prerequisites
echo "🔍 Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required but not installed"
    exit 1
fi

python_version=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    print_error "Python 3.8+ is required, found $python_version"
    exit 1
fi

print_status "Python $python_version found"

# Check pip
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is required but not installed"
    exit 1
fi

# Check git
if ! command -v git &> /dev/null; then
    print_error "git is required but not installed"
    exit 1
fi

print_status "All prerequisites found"

# Create virtual environment
echo "🐍 Setting up Python virtual environment..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Created virtual environment"
else
    print_info "Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate
print_status "Activated virtual environment"

# Upgrade pip
pip install --upgrade pip
print_status "Upgraded pip"

# Install requirements
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt
print_status "Installed Python dependencies"

# Create .env from example if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    print_warning "Created .env file from example - please configure your settings"
else
    print_info ".env file already exists"
fi

# Create directories
mkdir -p logs
mkdir -p tmp
print_status "Created necessary directories"

# Test imports
echo "🧪 Testing Python imports..."
python3 -c "
import sys
sys.path.insert(0, 'src')

try:
    from agents.interview_agent import InterviewTopicsAgent
    from database.mongodb_client import MongoDBClient
    print('✅ All imports successful')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"

print_status "Python imports test passed"

# Display setup completion
echo ""
echo "🎉 Setup completed successfully!"
echo ""
print_info "Next steps:"
echo "  1. Configure your .env file with:"
echo "     - MONGODB_URI (from Railway MongoDB service)"
echo "     - GOOGLE_CLOUD_PROJECT (your GCP project ID)"
echo "     - GOOGLE_APPLICATION_CREDENTIALS (path to service account JSON)"
echo ""
echo "  2. Test the setup:"
echo "     source venv/bin/activate"
echo "     python src/main.py"
echo ""
echo "  3. Configure GitHub repository secrets:"
echo "     - MONGODB_URI"
echo "     - GOOGLE_CLOUD_PROJECT" 
echo "     - GOOGLE_APPLICATION_CREDENTIALS_JSON"
echo ""
echo "  4. Push to GitHub to trigger the workflow"
echo ""

# GitHub Actions workflow status
if [ -f ".github/workflows/generate-topics.yml" ]; then
    print_status "GitHub Actions workflow is configured"
    print_info "Workflow will run every Monday at 9:00 AM UTC"
    print_info "You can also trigger it manually from the Actions tab"
else
    print_warning "GitHub Actions workflow file not found"
fi

echo ""
print_info "For detailed instructions, see README.md"
echo "🚀 Happy interviewing!"