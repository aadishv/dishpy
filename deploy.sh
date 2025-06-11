#!/bin/bash
set -e

echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info

echo "🔨 Building package..."
uv run python -m build

echo "✅ Checking package..."
uv run twine check dist/*

echo "🚀 Choose deployment target:"
echo "1) TestPyPI (testing)"
echo "2) PyPI (production)"
read -p "Enter choice (1 or 2): " choice

case $choice in
    1)
        echo "📦 Uploading to TestPyPI..."
        uv run twine upload --repository testpypi dist/*
        echo "✨ Test with: pip install --index-url https://test.pypi.org/simple/ dishpy"
        ;;
    2)
        echo "📦 Uploading to PyPI..."
        uv run twine upload dist/*
        echo "✨ Package available at: https://pypi.org/project/dishpy/"
        echo "🎉 Users can now install with: pip install dishpy"
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo "✅ Deployment complete!"