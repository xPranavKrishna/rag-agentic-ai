# Setup and GitHub Push Guide

This guide is for Windows and assumes Git is already installed.

## 1. Open the project

Open the `rag-agentic-ai` folder in VS Code.

Open the VS Code terminal:

```powershell
cd path\to\rag-agentic-ai
```

## 2. Create and activate the virtual environment

```powershell
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` at the start of the terminal line.

## 3. Install packages

```powershell
pip install -r requirements.txt
```

## 4. Create `.env`

Copy `.env.example` and rename the copy to `.env`.

Then add:

```env
OPENAI_API_KEY=your_key_here
PINECONE_API_KEY=your_key_here
PINECONE_INDEX_NAME=agentic-ai-index
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1
LLM_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
```

Never put real API keys in GitHub.

## 5. Run ingestion

The PDF is already included in the local project package.

```powershell
python -m src.ingestion
```

Wait until you see:

```text
Ingestion completed successfully.
```

## 6. Start FastAPI

```powershell
uvicorn app:app --reload
```

Open this in the browser:

```text
http://127.0.0.1:8000/docs
```

Use `POST /chat`, click **Try it out**, and enter:

```json
{
  "query": "What is Agentic AI according to the eBook?"
}
```

## 7. Run the test questions

Keep the API terminal running. Open another terminal and activate the environment again:

```powershell
venv\Scripts\activate
python tests_sample_queries.py
```

## 8. Create the GitHub repository

1. Go to GitHub.
2. Click **New repository**.
3. Repository name: `rag-agentic-ai`.
4. Set it to **Public**.
5. Do not add a README, `.gitignore`, or license because this project already has them.
6. Create the repository.

## 9. Push the project

In the project terminal:

```powershell
git init
git branch -M main
git add .
git status
git commit -m "build: add agentic AI RAG chatbot"
```

Check `git status` before committing. You should NOT see `.env`.

Then connect your GitHub repository. Replace the URL with your own repository URL:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/rag-agentic-ai.git
git push -u origin main
```

Refresh GitHub. Your code should now be visible.

## 10. Final check before submitting

Check these items on GitHub:

- `README.md` is visible.
- `app.py` is visible.
- `src/graph.py` is visible.
- `src/ingestion.py` is visible.
- `requirements.txt` is visible.
- `.env` is NOT visible.
- The repository is Public.

The PDF is ignored by `.gitignore`, so `git add .` will not upload it.

## Useful Git commands

After making changes:

```powershell
git status
git add .
git commit -m "fix: improve RAG response handling"
git push
```

To check the remote repository:

```powershell
git remote -v
```

To see commit history:

```powershell
git log --oneline
```
