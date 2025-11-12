#!/bin/bash

# Deployment script for Azure App Service
# This script handles Python dependency installation and app startup

echo "Starting Python App Deployment..."

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -m textblob.download_corpora
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('punkt')"

echo "Dependencies installed successfully!"
echo "Starting Flask app..."

# Run the app with gunicorn (for production)
gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 4 --timeout 120 app:app
