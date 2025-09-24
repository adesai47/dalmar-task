# Backend Setup

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

```bash
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_OPENAI_API_VERSION=2024-04-01-preview
AZURE_OPENAI_MODEL_NAME=gpt-4o-mini
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
```

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables in a `.env` file

4. Run the application:
```bash
python run.py
```

## Security Note

Never commit your `.env` file to version control. The `.env` file should be added to `.gitignore` to prevent accidentally exposing sensitive information like API keys.
