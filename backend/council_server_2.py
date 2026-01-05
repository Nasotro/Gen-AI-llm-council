from fastapi import FastAPI
from pydantic import BaseModel
from langchain_ollama import ChatOllama
import uvicorn
from .config import COUNCIL_MODEL_NAMES

model_name = COUNCIL_MODEL_NAMES.get("http://localhost:8003/api/query")
print(model_name)

app = FastAPI()
llm = ChatOllama(model=model_name)

class QueryRequest(BaseModel):
    messages: list


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "model": model_name,
        "type": "Council Member 2"
    }


@app.post("/api/query")
def query(request: QueryRequest):
    try:
        result = llm.invoke(request.messages)

        return {
            'content': result.content,
            'reasoning_details': None
        }
    
    except Exception as e:
        print(f"Error querying model {llm}: {e}")
        return None

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
