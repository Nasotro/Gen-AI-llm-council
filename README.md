# LLM Council - Local Deployement

### Team
- **Group Members**:
    - Aymeric MARTIN
    - Noémie MAZEPA
    - Lorrain MORLET
- **TD Group**: CDOF3

--- 

### Project Overview


### System Architecture
```

```

### LLM Models Used
- Council Member 1: Qwen2.5 (1.5B)
- Council Member 2: Ministral-3 (3B)
- Chairman: Ministral-3 (3B)

### Setup and Installation
#### Prerequisites

### Ollama Setup
On each machine, install Ollama and pull the required models:
````
ollama pull qwen2.5:1.5b
ollama pull ministral:3b
````
--- 
### Running the Project

#### Start the LLM Servers
1. Chairman Machine

Terminal 1 (Backend):
```bash
uv run python -m backend.main
```

Terminal 2 (Chairman Server):
```bash
uv run python -m backend.chairman_server
```

Terminal 3 (Frontend):
```bash
cd frontend
npm run dev
```
Then open http://localhost:5173 in your browser.

2. Council Member 1 Machine
Terminal 1 (Council Member 1 Server):
```bash
uv run python -m backend.council_server_1
```
3. Council Member 2 Machine
Terminal 1 (Council Member 2 Server):
```bash
uv run python -m backend.council_server_2
```


---
## Technologies Used

- **Backend:** FastAPI (Python 3.10+), async httpx, Ollama
- **Frontend:** React + Vite, react-markdown for rendering
- **Storage:** JSON files in `data/conversations/`
- **Package Management:** uv for Python, npm for JavaScript

---
### Improvements Over the Original Project


---
### Generative AI Usage Statement
