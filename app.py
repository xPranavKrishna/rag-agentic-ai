from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.graph import build_rag_graph

app = FastAPI(title="Agentic AI RAG Chatbot")
graph = None


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def home():
    return {"message": "Agentic AI RAG API is running"}


@app.post("/chat")
def chat(request: QueryRequest):
    global graph

    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        if graph is None:
            graph = build_rag_graph()

        result = graph.invoke(
            {
                "question": request.query,
                "context": [],
                "answer": "",
                "score": 0.0,
            }
        )

        return {
            "query": request.query,
            "final_answer": result["answer"],
            "retrieved_context_chunks": result["context"],
            "confidence_score": result["score"],
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
