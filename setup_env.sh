#!/bin/bash

# Setup script for environment variables
echo "Setting up environment variables for the Dalmar Task project..."

# Create .env file in backend directory
cat > backend/.env << EOF
# Azure OpenAI Configuration
# Replace with your actual API key
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_OPENAI_API_VERSION=2024-04-01-preview
AZURE_OPENAI_MODEL_NAME=gpt-4o-mini
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
EOF

echo "✅ Environment file template created at backend/.env"
echo "⚠️  Remember: Replace 'your_azure_openai_api_key_here' with your actual API key"
echo "⚠️  The .env file is now in .gitignore and will not be committed to version control"
echo ""
echo "You can now push your changes to GitHub without exposing the API key!"
