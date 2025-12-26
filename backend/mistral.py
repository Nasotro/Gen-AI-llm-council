"""Mistral API client for making LLM requests."""

from mistralai import Mistral
from typing import List, Dict, Any, Optional
from .config import MISTRAL_API_KEY


async def query_model(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float = 120.0
) -> Optional[Dict[str, Any]]:
    """
    Query a single model via Mistral API.

    Args:
        model: Mistral model identifier (e.g., "mistral-large-latest")
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds

    Returns:
        Response dict with 'content' and optional 'reasoning_details', or None if failed
    """
    try:
        client = Mistral(api_key=MISTRAL_API_KEY)
        
        chat_response = client.chat.complete(
            model=model,
            messages=messages
        )
        
        message = chat_response.choices[0].message
        
        return {
            'content': message.content,
            'reasoning_details': getattr(message, 'reasoning_details', None)
        }

    except Exception as e:
        print(f"Error querying model {model}: {e}")
        return None


async def query_models_parallel(
    models: List[str],
    messages: List[Dict[str, str]]
) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Query multiple models in parallel.

    Args:
        models: List of Mistral model identifiers
        messages: List of message dicts to send to each model

    Returns:
        Dict mapping model identifier to response dict (or None if failed)
    """
    import asyncio

    # Create tasks for all models
    tasks = [query_model(model, messages) for model in models]

    # Wait for all to complete
    responses = await asyncio.gather(*tasks)

    # Map models to their responses
    return {model: response for model, response in zip(models, responses)}