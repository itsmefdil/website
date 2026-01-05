#!/bin/bash

# DevOps Jogja Website - Development Scripts
# Usage: ./dev.sh [command]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper function for colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if required tools are installed
check_requirements() {
    print_status "Checking requirements..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed"
        exit 1
    fi
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js is required but not installed"
        exit 1
    fi
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        print_error "npm is required but not installed"
        exit 1
    fi
    
    print_success "All requirements are met"
}

# Function to install dependencies
install_deps() {
    print_status "Installing dependencies..."
    
    # Install Python dependencies
    print_status "Installing Python dependencies..."
    uv sync --locked
    
    # Install Node.js dependencies
    print_status "Installing Node.js dependencies..."
    npm install
    
    print_success "Dependencies installed"
}

# Function to setup development environment
setup() {
    print_status "Setting up development environment..."
    
    check_requirements
    install_deps
    
    # Create required directories
    print_status "Creating required directories..."
    mkdir -p content/blog content/event
    mkdir -p static/organizer static/images static/images/gallery
    mkdir -p static/images/blog static/images/event
    
    print_success "Development environment setup complete"
}

# Function to build CSS
build_css() {
    print_status "Building Tailwind CSS..."
    if [ "$1" = "watch" ]; then
        npm run build-css
    else
        npm run build-css-prod
    fi
}

# Function to run Flask development server
dev_server() {
    print_status "Starting Flask development server..."
    print_warning "Server will run on http://localhost:3000"
    export FLASK_ENV=development
    export FLASK_DEBUG=1
    uv run python3 app.py
}

# Function to build static site
build_static() {
    print_status "Building static site..."
    
    # Build CSS first
    build_css
    
    # Build static site
    uv run python3 build.py $1
    
    print_success "Static site built successfully in 'dist' directory"
}

# Function to serve static site locally
serve_static() {
    print_status "Serving static site locally..."
    
    if [ ! -d "dist" ]; then
        print_warning "Static site not found. Building first..."
        build_static
    fi
    
    print_status "Starting local server on http://localhost:8888"
    print_warning "Press Ctrl+C to stop the server"
    
    cd dist && uv run python3 -m http.server 8888 --bind 0.0.0.0
}

# Function to clean build artifacts
clean() {
    print_status "Cleaning build artifacts..."
    
    # Remove dist directory
    if [ -d "dist" ]; then
        rm -rf dist
        print_status "Removed dist directory"   
    fi
    
    # Remove CSS build artifacts
    if [ -f "static/css/output.css" ]; then
        rm -f static/css/output.css
        print_status "Removed CSS build artifacts"
    fi
    
    # Remove Python cache
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    
    print_success "Cleanup complete"
}

# Function to run tests (placeholder for future)
test() {
    print_status "Running tests..."
    print_warning "No tests defined yet"
}

# Function to validate content
validate() {
    print_status "Validating content..."
    
    # Check if content directories exist
    if [ ! -d "content/blog" ] || [ ! -d "content/event" ]; then
        print_error "Content directories not found"
        exit 1
    fi
    
    # Validate markdown files
    python3 -c "
from utils.markdown_parser import MarkdownParser
from utils.yaml_loader import YAMLLoader
import glob

mp = MarkdownParser()
yl = YAMLLoader()

print('Validating blog posts...')
for file in glob.glob('content/blog/*.md'):
    post = mp.parse_file(file)
    if not post:
        print(f'ERROR: Failed to parse {file}')
        exit(1)
    print(f'✓ {file}')

print('Validating events...')
for file in glob.glob('content/event/*.md'):
    event = mp.parse_file(file)
    if not event:
        print(f'ERROR: Failed to parse {file}')
        exit(1)
    print(f'✓ {file}')

print('Validating YAML files...')
for file in ['content/about.yaml', 'content/organizer.yaml', 'content/sponsor.yaml']:
    data = yl.load_yaml(file)
    if not data:
        print(f'WARNING: Empty or invalid {file}')
    else:
        print(f'✓ {file}')

print('Content validation complete!')
"
    
    print_success "Content validation complete"
}

# Function to show help
show_help() {
    echo "DevOps Jogja Website - Development Scripts"
    echo ""
    echo "Usage: ./dev.sh [command]"
    echo ""
    echo "Commands:"
    echo "  setup              Setup development environment"
    echo "  dev                Start Flask development server"
    echo "  build [domain]     Build static site (optionally with custom domain)"
    echo "  serve              Serve static site locally"
    echo "  css [watch]        Build CSS (add 'watch' for watch mode)"
    echo "  clean              Clean build artifacts"
    echo "  validate           Validate content files"
    echo "  test               Run tests (placeholder)"
    echo "  help               Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./dev.sh setup                    # Setup environment"
    echo "  ./dev.sh dev                      # Start development server"
    echo "  ./dev.sh build                    # Build for GitHub Pages"
    echo "  ./dev.sh build devopsjogja.org    # Build with custom domain"
    echo "  ./dev.sh serve                    # Serve static site locally"
    echo "  ./dev.sh css watch                # Build CSS in watch mode"
}

# Main script logic
case "${1:-help}" in
    "setup")
        setup
        ;;
    "dev")
        dev_server
        ;;
    "build")
        build_static $2
        ;;
    "serve")
        serve_static
        ;;
    "css")
        build_css $2
        ;;
    "clean")
        clean
        ;;
    "validate")
        validate
        ;;
    "test")
        test
        ;;
    "help"|*)
        show_help
        ;;
esac
