"""Configuration for the LLM Council."""


# Council members - list of Mistral model identifiers
COUNCIL_MODELS = [
    "llama3.2:1b",
    "qwen2.5:0.5b",
    #"llama3.2:3b", 
    #"mistral:7b",
    "gemma3:1b"
]

# Chairman model - synthesizes final response
CHAIRMAN_MODEL = "gemma3:1b"

# Data directory for conversation storage
DATA_DIR = "data/conversations"
