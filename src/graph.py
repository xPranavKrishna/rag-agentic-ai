from typing import List, TypedDict

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langgraph.graph import END, START, StateGraph

from src.config import (
    EMBEDDING_MODEL,
    LLM_MODEL,
    MIN_RELEVANCE_SCORE,
    PINECONE_INDEX_NAME,
    TOP_K,
    check_keys,
)


class AgentState(TypedDict):
    question: str
    context: List[str]
    answer: str
    score: float


def build_rag_graph():
    check_keys()

    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    vector_store = PineconeVectorStore(
        index_name=PINECONE_INDEX_NAME,
        embedding=embeddings,
    )
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0)

    def retrieve_node(state: AgentState):
        results = vector_store.similarity_search_with_score(
            state["question"],
            k=TOP_K,
        )

        context = []
        scores = []

        for document, score in results:
            page = document.metadata.get("page_number", "unknown")
            text = document.page_content.strip()
            context.append(f"[Page {page}] {text}")
            scores.append(float(score))

        average_score = sum(scores) / len(scores) if scores else 0.0
        return {
            "context": context,
            "score": round(average_score, 2),
        }

    def generate_node(state: AgentState):
        if not state["context"] or state["score"] < MIN_RELEVANCE_SCORE:
            return {
                "answer": "I cannot answer that based on the provided Agentic AI eBook.",
            }

        context_text = "\n\n".join(state["context"])

        prompt = f"""You are a document-based question answering assistant.

Answer the user's question ONLY using the context from the Agentic AI eBook below.
Do not use outside knowledge.
If the answer is not present in the context, say exactly:
I cannot answer that based on the provided Agentic AI eBook.
Keep the answer clear and reasonably short.

Context:
{context_text}

Question:
{state['question']}
"""

        response = llm.invoke(prompt)
        return {"answer": response.content.strip()}

    workflow = StateGraph(AgentState)
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("generate", generate_node)
    workflow.add_edge(START, "retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)

    return workflow.compile()


if __name__ == "__main__":
    graph = build_rag_graph()
    result = graph.invoke(
        {
            "question": "What is Agentic AI?",
            "context": [],
            "answer": "",
            "score": 0.0,
        }
    )
    print(result["answer"])
