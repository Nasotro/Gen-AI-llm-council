"""3-stage LLM Council orchestration - Local version using Ollama."""

from typing import List, Dict, Any, Tuple
from langchain_ollama import ChatOllama
import asyncio
from config import CHAIRMAN_MODEL_NAME


# Define local models to use in the council
# These will be queried from a local Ollama instance
LOCAL_COUNCIL_MODELS = [
    "qwen3:1.7b",
    "gemma3:1b",
]

# Initialize models
try:
    llama_model = ChatOllama(model="llama3.2:1b")
    gemma_model = ChatOllama(model="gemma3:1b")
    chairman_model = ChatOllama(model=CHAIRMAN_MODEL_NAME)
    models = [llama_model, gemma_model]
except Exception as e:
    print(f"Warning: Failed to initialize Ollama models: {e}")
    models = []


async def query_local_model(model: ChatOllama, messages: List[Dict[str, str]]) -> str:
    """
    Query a local Ollama model synchronously (wrapped for async context).
    
    Args:
        model: ChatOllama model instance
        messages: List of message dicts with 'role' and 'content'
        
    Returns:
        Model response as string
    """
    try:
        # Run the model query in a thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: model.invoke(messages)
        )
        return result.content
    except Exception as e:
        print(f"Error querying local model: {repr(e)}")
        return f"Error: {str(e)}"


async def stage1_collect_responses_local(user_query: str) -> List[Dict[str, Any]]:
    """
    Stage 1: Collect individual responses from all local council models.

    Args:
        user_query: The user's question

    Returns:
        List of dicts with 'model' and 'response' keys
    """
    messages = [{"role": "user", "content": user_query}]

    # Query all models in parallel
    tasks = [query_local_model(model, messages) for model in models]
    responses = await asyncio.gather(*tasks)

    # Format results
    stage1_results = []
    model_names = ["llama3.2:1b", "gemma3:1b"]
    
    for model_name, response in zip(model_names, responses):
        if response:  # Only include successful responses
            stage1_results.append({
                "model": model_name,
                "response": response
            })

    return stage1_results


async def stage2_collect_rankings_local(
    user_query: str,
    stage1_results: List[Dict[str, Any]]
) -> Tuple[List[Dict[str, Any]], Dict[str, str]]:
    """
    Stage 2: Each model ranks the anonymized responses.

    Args:
        user_query: The original user query
        stage1_results: Results from Stage 1

    Returns:
        Tuple of (rankings list, label_to_model mapping)
    """
    # Create anonymized labels for responses (Response A, Response B, etc.)
    labels = [chr(65 + i) for i in range(len(stage1_results))]  # A, B, C, ...
    
    # Create label to model mapping
    label_to_model = {label: result["model"] for label, result in zip(labels, stage1_results)}

    # Build the ranking prompt
    responses_text = "\n".join(
        [f"Response {label}: {result['response']}" for label, result in zip(labels, stage1_results)]
    )
    
    ranking_prompt = f"""You are evaluating the following responses to the question: "{user_query}"

{responses_text}

Please rank these responses from best to worst based on:
1. Accuracy and correctness
2. Completeness and relevance
3. Clarity and usefulness

Provide your ranking as a comma-separated list of response labels (e.g., "A,B,C" or "B,A,C").
Only provide the ranking, nothing else."""

    ranking_messages = [{"role": "user", "content": ranking_prompt}]

    # Query all models for rankings in parallel
    tasks = [query_local_model(model, ranking_messages) for model in models]
    rankings = await asyncio.gather(*tasks)

    # Parse rankings
    stage2_results = []
    for model_name, ranking_str in zip(["llama3.2:1b", "gemma3:1b"], rankings):
        try:
            # Parse the ranking (should be comma-separated labels)
            ranking_list = [label.strip().upper() for label in ranking_str.split(",")]
            # Filter to only valid labels
            ranking_list = [label for label in ranking_list if label in labels]
            
            stage2_results.append({
                "model": model_name,
                "ranking": ranking_str,  # Store the raw text for display
                "parsed_ranking": ranking_list  # Store the parsed list separately
            })
        except Exception as e:
            print(f"Error parsing ranking from {model_name}: {e}")
            stage2_results.append({
                "model": model_name,
                "ranking": ranking_str,  # Store the raw text for display
                "parsed_ranking": labels  # Default to original order if parsing fails
            })

    return stage2_results, label_to_model


async def stage3_synthesize_final_local(
    user_query: str,
    stage1_results: List[Dict[str, Any]],
    stage2_results: List[Dict[str, Any]]
) -> str:
    """
    Stage 3: Chairman synthesizes all responses and rankings into final answer.

    Args:
        user_query: The original user query
        stage1_results: Results from Stage 1
        stage2_results: Results from Stage 2

    Returns:
        Final synthesized response string
    """
    # Prepare context from previous stages
    council_responses_text = "\n".join([
        f"- {result['model']}: {result['response']}"
        for result in stage1_results
    ])

    rankings_text = "\n".join([
        f"- {result['model']}: {', '.join(result['ranking'])}"
        for result in stage2_results
    ])

    synthesis_prompt = f"""You are a chairman synthesizing the responses and feedback from a council of AI models.

Original question: "{user_query}"

Council responses:
{council_responses_text}

Model rankings of responses (best to worst):
{rankings_text}

Based on the council's responses and rankings, provide a comprehensive final answer that:
1. Incorporates the best insights from the responses
2. Considers the council's collective judgment
3. Provides a clear, well-reasoned answer
4. Explains the reasoning behind your synthesis

Provide the final answer:"""

    chairman_messages = [{"role": "user", "content": synthesis_prompt}]

    # Get final response from chairman model
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: chairman_model.invoke(chairman_messages)
        )
        return result.content
    except Exception as e:
        print(f"Error in chairman synthesis: {repr(e)}")
        return f"Error generating final synthesis: {str(e)}"


async def run_full_council_local(user_query: str) -> Tuple[
    List[Dict[str, Any]],
    List[Dict[str, Any]],
    str,
    Dict[str, Any]
]:
    """
    Run the complete 3-stage council process locally.

    Args:
        user_query: The user's question

    Returns:
        Tuple of (stage1_results, stage2_results, stage3_result, metadata)
    """
    # Stage 1: Collect responses
    stage1_results = await stage1_collect_responses_local(user_query)

    # Stage 2: Collect rankings
    stage2_results, label_to_model = await stage2_collect_rankings_local(user_query, stage1_results)

    # Calculate aggregate rankings
    aggregate_rankings = calculate_aggregate_rankings(stage2_results, label_to_model)

    # Stage 3: Synthesize final answer
    stage3_result = await stage3_synthesize_final_local(user_query, stage1_results, stage2_results)

    # Prepare metadata
    metadata = {
        "label_to_model": label_to_model,
        "aggregate_rankings": aggregate_rankings,
        "council_size": len(stage1_results),
        "mode": "local"
    }

    return stage1_results, stage2_results, stage3_result, metadata


async def generate_conversation_title_local(user_message: str) -> str:
    """
    Generate a title for the conversation using local model.

    Args:
        user_message: The user's initial message

    Returns:
        Generated title string
    """
    title_prompt = f"""Given the following user message, generate a short, concise title (5-10 words max) for this conversation.

User message: "{user_message}"

Respond with only the title, nothing else."""

    messages = [{"role": "user", "content": title_prompt}]

    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: models[0].invoke(messages)
        )
        title = result.content.strip()
        # Clean up the title if it has extra quotes or formatting
        title = title.strip('"\'')
        return title if title else "New Conversation"
    except Exception as e:
        print(f"Error generating title: {repr(e)}")
        return "New Conversation"


def calculate_aggregate_rankings(
    stage2_results: List[Dict[str, Any]],
    label_to_model: Dict[str, str]
) -> Dict[str, Any]:
    """
    Calculate aggregate rankings from all council members.

    Args:
        stage2_results: Rankings from Stage 2
        label_to_model: Mapping of response labels to model names

    Returns:
        Dictionary with aggregated ranking scores
    """
    # Count points: 1st place = n points, 2nd place = n-1 points, etc.
    rankings_scores = {label: 0 for label in label_to_model.keys()}
    
    for result in stage2_results:
        ranking = result.get("ranking", [])
        points = len(ranking)
        for label in ranking:
            if label in rankings_scores:
                rankings_scores[label] += points
            points -= 1

    # Sort by score (descending)
    sorted_rankings = sorted(
        rankings_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return {
        "rankings": [
            {
                "label": label,
                "model": label_to_model.get(label, "Unknown"),
                "score": score
            }
            for label, score in sorted_rankings
        ],
        "total_voters": len(stage2_results)
    }
