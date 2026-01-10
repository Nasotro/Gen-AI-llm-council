from fastapi import FastAPI
from pydantic import BaseModel
from langchain_ollama import ChatOllama
import uvicorn
from chairman_model_name import CHAIRMAN_MODEL_NAME

print(CHAIRMAN_MODEL_NAME)

app = FastAPI()
llm = ChatOllama(model=CHAIRMAN_MODEL_NAME)

class QueryRequest(BaseModel):
    messages: list

@app.get("/")
def health_check():
    return {
        "status": "ok",
        "model": CHAIRMAN_MODEL_NAME,
        "type": "Chairman"
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
    uvicorn.run(app, host="0.0.0.0", port=8004)