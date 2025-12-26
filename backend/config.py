"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv

load_dotenv()

# Mistral API key
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Council members - list of Mistral model identifiers
COUNCIL_MODELS = [
    "mistral-tiny",
    "mistral-small", 
    "mistral-medium",
    "mistral-large-2512",
]

# Chairman model - synthesizes final response
CHAIRMAN_MODEL = "mistral-large-2512"

# Mistral API endpoint
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# Data directory for conversation storage
DATA_DIR = "data/conversations"
