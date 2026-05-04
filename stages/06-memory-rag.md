# Stage 6 — Memory · RAG · Advanced

⏱ **Time estimate**: 2 weeks (~10 hours)

Agents that don't remember past interactions are not useful. RAG (Retrieval-Augmented Generation) is the standard approach. This stage covers both.

## 📌 Learning Goals

- Distinguish short-term, long-term, episodic, semantic memory
- Understand vector embeddings and similarity search
- Build a basic RAG pipeline (chunk → embed → store → retrieve → generate)
- Recognize when RAG is the wrong answer (and when it's the right one)

## 📚 Required Reading

1. [**LlamaIndex — RAG concepts**](https://docs.llamaindex.ai/en/stable/getting_started/concepts/) — clearest intro
2. [**LangChain — RAG tutorial**](https://python.langchain.com/docs/tutorials/rag/) — hands-on
3. [**Pinecone — Learning Center**](https://www.pinecone.io/learn/) — vector DB fundamentals
4. [**Anthropic — Contextual Retrieval**](https://www.anthropic.com/news/contextual-retrieval) — Anthropic's RAG technique with prompt caching

## 🛠 Hello-X

- **Hello Embeddings** — embed 100 sentences, find nearest neighbors of one query
- **Hello Vector DB** — store embeddings in Chroma, query semantically
- **Hello RAG** — full pipeline: chunk a PDF → embed → retrieve top-k → generate answer
- **Hello Memory** — give an agent conversational memory across multiple turns

## 🎯 Curated Projects

### [LlamaIndex](https://github.com/run-llama/llama_index)

| Stars | ★ 49k+ |
|---|---|
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: The RAG-focused framework. Document loaders, chunking strategies, retrieval patterns, query engines.

**Best for**: Document-heavy applications. RAG is its core.

---

### [Chroma](https://github.com/chroma-core/chroma)

| Stars | ★ 27k+ |
|---|---|
| License | Apache-2.0 |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Open-source embedding database. Run locally, no infrastructure setup.

**Best for**: Hello-2 and Hello-3 above. Easiest vector DB to start with.

**Run it**:
```python
import chromadb
client = chromadb.Client()
collection = client.create_collection("hello")
collection.add(documents=["doc 1", "doc 2"], ids=["1", "2"])
results = collection.query(query_texts=["query"], n_results=1)
```

---

### [Qdrant](https://github.com/qdrant/qdrant)

| Stars | ★ 31k+ |
|---|---|
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: Production-grade vector DB written in Rust. Faster than Chroma at scale.

**Best for**: When Chroma can't keep up. Has cloud + self-hosted modes.

---

### [Weaviate](https://github.com/weaviate/weaviate)

| Stars | ★ 16k+ |
|---|---|
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: Vector DB with built-in modules (text2vec, generative, classification). Schema-driven.

**Best for**: Production deployments needing schema constraints.

---

### [pgvector](https://github.com/pgvector/pgvector)

| Stars | ★ 21k+ |
|---|---|
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: Vector similarity search inside PostgreSQL. SQL + vector in one DB.

**Best for**: Teams already on PostgreSQL who don't want a separate vector store.

---

### [LangChain — Memory](https://python.langchain.com/docs/concepts/memory/)

**What it teaches**: Agent memory patterns (buffer, summary, vectorstore-backed).

**Best for**: When your agent needs to remember across sessions.

---

### [mem0ai/mem0](https://github.com/mem0ai/mem0)

| Stars | ★ 54k+ |
|---|---|
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: Self-improving memory layer for AI agents. Stores facts about users across sessions.

**Best for**: Personal assistant / chatbot apps that need user-level memory.

---

### [Letta (formerly MemGPT)](https://github.com/letta-ai/letta)

| Stars | ★ 22k+ |
|---|---|
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: Long-context agent with hierarchical memory. Inspired by OS memory management.

**Best for**: Agents that need very long-running context (months, not minutes).

---

### [Anthropic — Contextual Retrieval cookbook](https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide)

**What it teaches**: Anthropic's contextual retrieval technique with prompt caching, end-to-end example.

**Best for**: After basic RAG, upgrade to contextual retrieval for better recall on long documents.

**Notes**: Anthropic renamed `anthropic-cookbook` → `claude-cookbooks` in 2025. The hosted notebook above is the canonical reference; raw GitHub paths may shift.

---

## ✅ Self-Check Before Stage 7

Can you:
- [ ] Build a 50-line RAG pipeline (load → chunk → embed → store → query → answer)
- [ ] Explain why naive chunking fails on long documents
- [ ] Pick between Chroma, Qdrant, pgvector for a given scale
- [ ] Distinguish "give the agent memory" from "use RAG"

If yes → proceed to [Stage 7 — Multi-Agent · Production](07-multi-agent-production.md).
