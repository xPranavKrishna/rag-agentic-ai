# Agentic AI RAG Chatbot

A simple RAG chatbot built for the AI Engineer interview assignment.

The project uses:

- Python
- LangGraph
- LangChain
- OpenAI embeddings + chat model
- Pinecone vector database
- FastAPI
- PyPDF

The chatbot is designed to answer questions only from the provided **Agentic AI** eBook. If the retrieved content is not relevant enough, it refuses to answer instead of using outside knowledge.

## Project structure

```text
rag-agentic-ai/
├── data/
│   └── Ebook-Agentic-AI.pdf       # keep the PDF locally
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── ingestion.py
│   └── graph.py
├── app.py
├── tests_sample_queries.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 1. Requirements

- Python 3.10+
- OpenAI API key
- Pinecone API key

## 2. Create the project environment

Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 3. Add the PDF

Put the provided file here:

```text
data/Ebook-Agentic-AI.pdf
```

The PDF is intentionally ignored by Git because this repository is public.

## 4. Add API keys

Copy `.env.example` to `.env` and add your keys:

```env
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=agentic-ai-index
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1
LLM_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
```

Do not commit `.env`.

## 5. Run ingestion

This loads the PDF, splits it into chunks of 1000 characters with 200 characters overlap, creates embeddings, and stores them in Pinecone.

```bash
python -m src.ingestion
```

You should see something similar to:

```text
Loading PDF...
Loaded 60 pages
Created ... chunks
Created Pinecone index: agentic-ai-index
Ingestion completed successfully.
```

If the Pinecone index already exists, the script uses it.

## 6. Start the API

```bash
uvicorn app:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

FastAPI provides a simple Swagger UI where `/chat` can be tested.

## 7. Example request

POST `/chat`

```json
{
  "query": "What is Agentic AI?"
}
```

Example response shape:

```json
{
  "query": "What is Agentic AI?",
  "final_answer": "Agentic AI refers to systems capable of autonomous decision-making and action in pursuit of specific objectives.",
  "retrieved_context_chunks": [
    "[Page 12] Agentic AI refers to systems capable of autonomous decision-making..."
  ],
  "confidence_score": 0.82
}
```

The exact answer and score will depend on the retrieved chunks.

## 8. Test the sample questions

Keep the API running and open another terminal:

```bash
python tests_sample_queries.py
```

The test includes an out-of-scope question:

```text
Who won the 2022 FIFA World Cup?
```

The expected behavior is a refusal because the answer is not part of the eBook.

## How the graph works

```text
User Question
     |
     v
  Retrieve
     |
     v
 Relevance Check
     |
     v
  Generate
     |
     v
   Answer
```

The LangGraph state contains:

- `question`
- `context`
- `answer`
- `score`

The retrieve node searches Pinecone for the top 4 chunks. The average similarity score is used as a simple confidence/relevance score. If it is below the threshold, the chatbot refuses to answer.

The generate node receives only the retrieved document chunks. The prompt also explicitly tells the model not to use outside knowledge.

## Notes

This is intentionally kept small and readable. It is a normal Python implementation rather than a large framework or low-code workflow.

## Quick API test with PowerShell

After starting FastAPI, you can also test it with:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/chat -Method Post -ContentType "application/json" -Body '{"query":"What is Agentic AI?"}'
```

## GitHub submission

See `GITHUB_SETUP.md` for the exact Windows setup and Git commands to create the public repository and push the project.
