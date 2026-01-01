from typing import List, Dict, Any, Optional
import asyncio
import httpx

async def query_model( model_endpoint:str, messages: List[Dict[str, str]], timeout: float = 200.0) -> Optional[Dict[str, Any]]:
    """
    Query a council model via REST API
    """
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                model_endpoint,
                json={"messages": messages}
            )
            response.raise_for_status()
            return response.json()

    except Exception as e:
        print(f"Error querying model {model_endpoint}: {repr(e)}")
        return None


async def query_models_parallel(models: List[str], messages: List[Dict[str, str]]) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Query multiple council models in parallel
    """
    tasks = [query_model(model, messages) for model in models]
    
    responses = await asyncio.gather(*tasks)

    return {model: response for model, response in zip(models, responses)}
