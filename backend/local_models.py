from typing import List, Dict, Any, Optional
import asyncio
from langchain_ollama import ChatOllama

async def query_model( model:str, messages: List[Dict[str, str]], timeout: float = 120.0) -> Optional[Dict[str, Any]]:
    try:
        llm = ChatOllama(
            model=model
        )
        result = llm.invoke(messages)

        return {
            'content': result.content,
            'reasoning_details': None
        }
    
    except Exception as e:
        print(f"Error querying model {model}: {e}")
        return None


async def query_models_parallel(models: List[str], messages: List[Dict[str, str]]) -> Dict[str, Optional[Dict[str, Any]]]:
    # Create tasks for all models
    tasks = [query_model(model, messages) for model in models]

    # Wait for all to complete
    responses = await asyncio.gather(*tasks)

    # Map models to their responses
    return {model: response for model, response in zip(models, responses)}
