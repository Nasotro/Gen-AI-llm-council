"""Configuration for the LLM Council."""


# Council members with mapping to their endpoint
COUNCIL_MODELS = [
    "http://172.20.10.2:8002/api/query",
    "http://172.20.10.3:8003/api/query",
]

COUNCIL_MODEL_NAMES = {
    "http://172.20.10.2:8002/api/query": "llama3.2:1b",
    "http://172.20.10.3:8003/api/query": "gemma3:1b",
}

# Chairman model - synthesizes final response
CHAIRMAN_ENDPOINT = "http://localhost:8004/api/query"

CHAIRMAN_MODEL_NAME = "gemma3:1b"

# Data directory for conversation storage
DATA_DIR = "data/conversations"
