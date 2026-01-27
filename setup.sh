#!/bin/bash

# DataPlotQA Setup Script
# This script sets up the DataPlotQA environment

set -e  # Exit on error

echo "=========================================="
echo "DataPlotQA Setup Script"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Check if version is 3.9 or higher
required_version="3.9"
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)"; then
    echo "Error: Python 3.9 or higher is required"
    exit 1
fi
echo "✓ Python version OK"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --break-system-packages
echo "✓ Dependencies installed"
echo ""

# Create data directory
echo "Creating data directory..."
mkdir -p data
echo "✓ Data directory created"
echo ""

# Check for API key
echo "Checking for ANTHROPIC_API_KEY..."
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  Warning: ANTHROPIC_API_KEY environment variable not set"
    echo ""
    echo "To set it, run:"
    echo "  export ANTHROPIC_API_KEY='your-api-key-here'"
    echo ""
    echo "Or create a .env file:"
    echo "  cp .env.example .env"
    echo "  # Edit .env and add your key"
    echo ""
else
    echo "✓ API key found"
    echo ""
fi

# Run tests
echo "Running basic tests..."
python3 tests/test_dataplotqa.py
echo ""

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Ensure ANTHROPIC_API_KEY is set (see above)"
echo "2. Run the application:"
echo "   streamlit run app/main.py"
echo ""
echo "For more information, see:"
echo "  - README.md"
echo "  - USER_GUIDE.md"
echo ""
