# LLM Council - Local Deployement

### Team
- **Group Members**:
    - Aymeric MARTIN
    - Noémie MAZEPA
    - Lorrain MORLET
- **TD Group**: CDOF3

--- 

### Project Overview
This project is a local and distributed implementation of the LLM Council concept created by Andrej Karpathy (https://github.com/karpathy/llm-council). Instead of relying only on a single LLM, several LLMs are used to answer a query through a process made of three steps.

In the original implementation, the LLM models used for the council members and chairman were all models called via cloud-based APIs. 
The objective of this project is to refactor the LLM Council code so that everything runs locally. Each council member and the chairman are executed as independent services, on separate machines and communicate with the backend via REST APIs. This setup aims for a distributed architecture across multiple machines.

The three main stages are: 
- **First Opinions**: several LLMs answer the user query independently.

- **Review & Ranking**: each model reviews and ranks the anonymized answers.

- **Chairman Synthesis**: a dedicated Chairman LLM synthesizes all answers and rankings into a final answer.

The user has access to all of the intermediate outputs and can observe how the final answer is constructed.

---

### System Architecture
- All LLMs run locally using Ollama

- Each LLM runs as an independent server exposing REST API endpoints

- One machine hosts the main backend and the Chairman LLM

- Other machines host the council member LLMs

- All machines must be connected to the same network

- Communication between machines is done via HTTP requests on a fixed port

The backend coordinates the full council workflow and the frontend visualizes each stage of the process.

---

### LLM Models Used
- Council Member 1: Qwen2.5 (1.5B)
- Council Member 2: Ministral-3 (3B)
- Chairman: Ministral-3 (3B)

### Setup and Installation
#### Prerequisites
- Python 3.10+
- Node.js and npm
- Ollama installed on all machines
- All machines connected to the same network
- Firewall configured to allow communication on the required port (ex: 8002)

### Ollama Setup
On each machine, install Ollama and pull the required models:
````
ollama pull qwen2.5:1.5b
ollama pull ministral:3b
````
--- 
### Running the Project

#### Create and Activate a Virtual Environment

First, create a Python virtual environment named .venv.
For Windows:
````
python -m venv .venv
.venv\Scripts\Activate.ps1
````
#### Install Dependencies Using uv
Once the virtual environment is activated, install uv:
````
pip install uv
uv sync
````
This will install all required Python packages defined for the project.

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
npm install
npm run dev
```
Then open http://localhost:5173 in your browser.

2. Council Member 1 Machine
```bash
uv run python -m backend.council_server_1
```
3. Council Member 2 Machine
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
- Full local execution without cloud APIs
- Distributed architecture using REST APIs
- Separation of council members and chairman into independent services

- Enhanced frontend with:
    - Light/Dark mode
    
    - Model performance dashboard
    
    - Workflow visualization
    
    - Improved tab view for responses

---
### Generative AI Usage Statement
