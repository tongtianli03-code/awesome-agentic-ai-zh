# Stage 6 — Memory · RAG · Context Engineering

> **Traditional Chinese** | [Simplified Chinese](./06-memory-rag.zh-Hans.md) | [English](./06-memory-rag.en.md)

⏱ **Estimated Time**: 2 weeks (approx. 10 hours)

> 💡 This stage is dense with terminology (**RAG / Vector Databases / Embedding / Chunking / Hybrid Search / Reranking⋯**) — if unfamiliar, first consult [`resources/glossary.md` §3](../resources/glossary.md#3-memory--retrieval--rag).

> 📋 **Chapter Structure**: Positioning → Entry Point → **RAG Core** (Basics + Advanced + DSPy + Eval) → **Bridge** → **Memory Core** (3 Patterns + Trio + Advanced) → Chunking → Reflexion / Reasoning → Practice → Projects
>
> 🔑 **Key Terms**: See [`resources/glossary.md` §3](../resources/glossary.md#3-memory--retrieval--rag) (memory / RAG / embedding / chunking / reranking)

## 🎯 What is Context Engineering? (Positioning First)

**Context Engineering = The engineering discipline of dynamically assembling prompts across multiple LLM calls**—the intermediate layer of the prompt → context → harness three-layer lineage. The full definition + the three-layer discipline table has been expanded in [Stage 2 §Advanced Prompt → Context → Harness](02-prompt-engineering.md#-advanced-prompt--context--harness-three-layer-engineering), and the top layer connects to [Stage 7 §Harness Engineering](07-multi-agent-production.md#-harness-engineering--the-engineering-discipline-of-production-agent-runtime--core-concept-of-this-stage).

> 📺 **Visual Learning**: [Hung-Yi Lee 2025 Lecture 2 — Context Engineering: The Key Technology Behind AI Agents](https://www.youtube.com/watch?v=lVdajtNpaGI) (NTU Introduction to Generative AI & Machine Learning 2025)

**This stage focuses on the first two of the 3 problem domains of context engineering**:

1.  **Retrieval** — Fetching relevant snippets from external knowledge bases (RAG / vector search / GraphRAG / hybrid search)
2.  **Memory Management** — How to layer, store, and forget short-term / long-term / episodic / semantic memory
3.  **Context Window Budget** — Handled in Stage 7 §Harness

### 4 Commonly Confused Concepts — Clarified in One Table

| Term | What it is (Abstract / Concrete) | Example Tools |
|---|---|---|
| **Memory** | An agent's **capability** to remember things across conversations / sessions (abstract concept) | LangChain ConversationBufferMemory / mem0 / Letta |
| **Embedding** | Converting text into an N-dimensional **vector** for calculable similarity (data transformation) | `sentence-transformers` producing 768-dim vectors / OpenAI ada-002 |
| **Vector DB** | The **storage layer** for storing + querying embeddings (infrastructure) | Chroma / Qdrant / Weaviate / pgvector |
| **RAG** | The **architectural pattern** of "retrieve relevant snippets → insert into prompt → generate" | LlamaIndex / LangChain RAG chain |

→ **Core Distinction**: Memory is a **capability**, Embedding is **data transformation**, Vector DB is **storage**, and RAG is an **architectural pattern**—these 4 are often confused but are actually concepts at 4 different layers.

### RAG vs Long Context vs Fine-tuning — When to Use What

LLMs know your private/domain data through 3 main approaches. **This stage teaches RAG**, but you should know when NOT to use it:

| Option | Suitable For | Not Suitable For | Cost |
|---|---|---|---|
| **RAG**<br>(External Retrieve) | Large / dynamic / private knowledge bases, requires citations for sources | Tasks requiring full-text reasoning, multi-hop reasoning across documents | Latency of an additional vector search per query |
| **Long Context**<br>(Directly in Prompt) | Medium-sized documents (< 200k tokens), one-off queries, cross-document reasoning | Large/frequently changing knowledge bases, need for citations | High input token usage per query (even with prompt caching) |
| **Fine-tuning**<br>(Modifying Model Weights) | Uniform style/format, specific domain language (medical, legal, code) | Knowledge that changes frequently, need for citations, reluctance to train models | Training costs + maintenance costs + model lock-in |

→ **How to Choose**: Start with RAG (lowest cost, easiest to change) → Consider Long Context if RAG is insufficient → Consider Fine-tuning only if both fail. **Proceed to Stage 7 to learn fine-tuning deployment**.

## 📌 Learning Objectives

- Build a basic RAG pipeline (chunk → embed → store → retrieve → generate)
- Identify scenarios where RAG is not suitable (and where it is)
- Differentiate between short-term, long-term, episodic, and semantic memory
- Understand vector embeddings and similarity search
- Know when to add advanced RAG techniques (GraphRAG / Contextual Retrieval / Hybrid Search)

## 🚪 Prerequisites

You should have already:
- Completed Stage 3 (ability to write tool use, call LLM APIs, understand ReAct loop)
- Be able to run Python `pip install` to install SDKs (will use `chromadb`, `sentence-transformers`, etc. later)
- Be comfortable with basic Python structures like lists, dicts, and generators.

If not, refer back to [Stage 3](03-tool-use-and-hello-agent.md) or [Stage 0 §Setup Guide](00-foundations.md#when-can-i-skip-this-stage).

## 📚 Required Reading

1.  [**LlamaIndex — RAG Concepts**](https://docs.llamaindex.ai/en/stable/getting_started/concepts/) — The clearest introduction.
2.  [**LangChain — RAG Tutorial**](https://python.langchain.com/docs/tutorials/rag/) — Hands-on implementation.
3.  [**Pinecone — Learning Center**](https://www.pinecone.io/learn/) — Vector DB fundamentals.
4.  [**Anthropic — Contextual Retrieval**](https://www.anthropic.com/news/contextual-retrieval) — Anthropic's approach to RAG with prompt caching.
5.  [**LangChain — Text Splitters**](https://docs.langchain.com/oss/python/integrations/splitters/index) — Introduction to chunking strategies.

> 🙏 **Special Recommendation for the Memory Chapter**: Refer to [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) — This stage covers the concepts and basic implementations of memory. For a **chapter-length in-depth guide**, consult the corresponding chapter in hello-agents, which provides the most comprehensive explanation of short-term vs. long-term memory differences, dynamic prompt assembly with context engineering, session persistence, and forgetting strategies. This stage serves as a roadmap, while that is a deep dive textbook.

## 🧭 Unit Guide (Progressive Flow)

This chapter proceeds by first teaching **RAG**, then **Memory**, as RAG is the most fundamental and commonly used tool for context engineering, while Memory enables agent capabilities across conversations/sessions. We'll start by getting the RAG pipeline running, then introduce Memory design, and finally revisit Chunking details.

**Recommended Reading Order**:

1.  **🌐 Basic RAG Pipeline** (Next Section) — Establish the mental model.
2.  **🚀 Advanced RAG Techniques** — GraphRAG / Contextual Retrieval / Hybrid Search, etc. for production upgrades.
3.  **🌉 From RAG to Memory** — Why RAG isn't enough and where Memory fills the gaps.
4.  **🧠 Memory Design** — Short-term vs. Long-term, 3 patterns, CoALA framework.
5.  **🧩 Chunking Details** — In-depth look at techniques used in both RAG and Memory.

As you read this chapter, consider: In which application scenarios is RAG unsuitable? Which scenarios are suitable for RAG but not well-served by basic RAG? This will lead you to advanced techniques like GraphRAG / Self-RAG / RAPTOR later on.

## 🌐 Basic RAG Pipeline

**RAG (Retrieval-Augmented Generation)** = The pattern of "retrieve relevant snippets → insert into prompt → generate". Think of it as building a library for your agent—you need to organize your books first, then you can quickly and accurately retrieve information when needed.

The most basic RAG is divided into two pipelines:

-   **Data Preprocessing (Ingest Once)**: ingest → chunk → embed → store (index). This step builds the searchable knowledge base.
-   **Retrieval & Generation (Per Query)**: retrieve → generate. This step finds relevant content when the user asks a question and feeds it to the LLM for generation.

![RAG Pipeline Overview](../resources/diagrams/rag-pipeline-overview.jpg)

The RAG Fusion and query rewrite techniques mentioned in the diagram fall under advanced retrieval techniques. When learning RAG for the first time, focus on understanding the main flow.

**Understanding the 5 Steps**:

| Step | What it does | Which Pipeline | Technical Details Found In |
|---|---|---|---|
| **1. Ingest** | Loads data (PDF / web / DB) | Preprocessing | LlamaIndex / LangChain respective loaders |
| **2. Chunk** | Splits documents into small pieces (500-2000 tokens / chunk) | Preprocessing | See §🧩 Chunking Details later (read RAG/Memory main sections first, technical details later) |
| **3. Embed** | Converts each chunk into an N-dimensional vector | Preprocessing | `sentence-transformers` / OpenAI ada-002 |
| **4. Store** | Stores vectors + metadata in a vector DB | Preprocessing | Chroma / Qdrant / pgvector |
| **5. Retrieve + Generate** | Embeds query → top-k semantic search → concatenates into prompt → LLM generates answer | Per Query | Universal LLM API |

These are the minimal structural elements. **The 3 most common pitfalls**:

-   **Chunk size too large / too small**: If too large, retrieved chunks might contain only one relevant sentence amidst much noise; if too small, context is lost (see §🧩 Chunking Details).
-   **Incorrect embedding model chosen**: Using an English model for Chinese documents halves retrieval accuracy.
-   **Top-k set too high / too low**: Too low might miss relevant chunks; too high introduces noise / burns tokens.

> 📚 **For more RAG pitfalls and solutions**: [NirDiamant/RAG_Techniques](https://github.com/NirDiamant/RAG_Techniques) ★ Large Production RAG Cookbook, includes 30+ techniques + Jupyter notebook examples.

After implementing the basic skeleton, complete Exercises 1-4 (Embeddings / Vector DB / Chunking / Full Pipeline) to gain practical experience, then move to the next section on §Advanced RAG Techniques.

## 🚀 Advanced RAG Techniques (Read After Basic RAG)

The following six subsections represent common production RAG enhancements from 2024-2026, grouped by the stage they are added to the pipeline:
-   **After Retrieve** — GraphRAG / Contextual Retrieval / Hybrid Search & Reranking
-   **Before Retrieve** (Query Rewriting) — Query Transformations
-   **During Retrieve** (Control Flow) — Self-improving RAG
-   **Index Structure** — RAPTOR
-   **2024-2026 Overview** — 17 other techniques worth knowing

**First, complete the basic RAG to establish a baseline version before diving into these**—otherwise, you'll be tuning parameters without a baseline, never knowing which change yielded improvement.

| Technique | Solves What Problem | Pipeline Stage | Cost |
|---|---|---|---|
| **GraphRAG** | Vanilla RAG cannot perform multi-hop / cross-document entity-relation reasoning | Before Retrieve (build graph) + During Retrieve (graph traversal) | High (requires KG construction, significant LLM token usage for entity extraction) |
| **Contextual Retrieval** | Chunks lose original document context, retrieval fetches incorrect snippets | After Chunk / Before Embed (add contextual header) | Medium (one-time ingest cost, 90% cheaper with prompt caching) |
| **Hybrid Search & Reranking** | Pure vector misses keyword matches, top-k has noise | During Retrieve (combine with BM25) + After Retrieve (cross-encoder reranking) | Low (mature tools integrate easily) |

### 🔗 GraphRAG — Knowledge Graph + RAG

**Mental Model**: Vanilla RAG cuts documents into chunks and relies on embedding similarity for retrieval—but it **doesn't know which entities are the same or their relationships**. GraphRAG constructs a knowledge graph by extracting (entity, relation, entity) triples from documents during ingestion. Retrieval then uses both vector similarity and graph traversal to find related entities and their connections.

**When to Use**:
- Tasks requiring **multi-hop reasoning** (A → B → C to answer).
- Cross-document entity referencing (company financial reports, research papers, legal cases).
- Questions like "How does X affect Y, and what is Y linked to Z?" — Vanilla RAG typically only retrieves content related to X.

**When Not to Use**:
- Documents without entity-relation links (standalone FAQs, independent product manuals).
- Small knowledge bases (< 1k chunks) — Vanilla RAG is sufficient.
- Tight budgets — KG construction can be 10-50x more token-intensive than regular RAG.

**Representative Frameworks**:
- [**HKUDS/LightRAG**](https://github.com/HKUDS/LightRAG) ★ **35.1k** MIT EMNLP 2025 — Currently the hottest community choice, lightweight, KG + vector hybrid, lower cost than Microsoft's version.
- [**Microsoft GraphRAG**](https://github.com/microsoft/graphrag) — Original reference implementation, Apache-2.0, includes community detection.
- [**gusye1234/nano-graphrag**](https://github.com/gusye1234/nano-graphrag) — Minimal implementation (< 1000 lines) for understanding core principles.

**Paper**: [**From Local to Global: A Graph RAG Approach to Query-Focused Summarization (Edge et al. 2024)**](https://arxiv.org/abs/2404.16130) — Original Microsoft GraphRAG paper explaining how community summarization addresses global queries.

### 🪶 Contextual Retrieval — Anthropic's Prompt Caching Solution

**Mental Model**: Vanilla chunks lose original document context—a chunk like "Q3 revenue grew 15%" doesn't tell you **which company** or **which year's** Q3. Anthropic's 2024 proposal: During ingestion, use an LLM to generate a 50-100 token **contextual header** for each chunk (e.g., "This chunk is from ACME Corp 2024 Q3 earnings, discussing the cloud segment...") and prepend it before embedding. Combined with **prompt caching**, this allows sending the entire document + each chunk only once, sharing the cache for subsequent chunks.

**When to Use**:
- Chunks are semantically distant from their original document's topic (financial reports, research papers, long narratives).
- You are willing to incur an initial ingest cost for improved retrieval accuracy.
- You are using Claude or plan to leverage prompt caching (other models can run this, but without cache benefits).

**When Not to Use**:
- Chunks are self-contained (FAQs, product descriptions, definitions).
- Knowledge base changes frequently (requires re-ingestion).
- Extremely tight budgets — ingest cost is higher than vanilla, even with caching discounts.

**Why it Saves 90% Cost**: Anthropic's report suggests prompt caching reduces costs to ~1/10 by treating the entire document as a cached prefix and only sending differences for each chunk. However, **this only saves on ingest, not retrieval**.

**Representative Implementations**:
- [**Anthropic — Contextual Retrieval Blog**](https://www.anthropic.com/news/contextual-retrieval) ⭐ — Official explanation + benchmark (failed retrieval rate dropped from 5.7% to 1.9%).
- [**Anthropic Cookbook**](https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide) — End-to-end Jupyter notebook with prompt templates.

**Paired Techniques**: The same Anthropic blog also recommends combining this with **Contextual BM25** (using contextual chunks with both vector + BM25) + **reranking**—leading into the next section on §Hybrid Search & Reranking.

### 🎯 Hybrid Search & Reranking — Two Essential Polishes for Production RAG

**Mental Model**:
-   **Hybrid Search** = Combines vector similarity (semantic match) with BM25/keyword search (literal match), using methods like [RRF (Reciprocal Rank Fusion)](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) to fuse scores. This addresses the dual blind spots of pure vector search: missing keyword matches due to different phrasing and weak semantic embedding for proper nouns, product IDs, technical terms, or rare words.
-   **Reranking** = First stage retrieves **top-50** chunks (prioritizing recall, broad fetch) → then a **cross-encoder reranker** re-scores and ranks the top **top-5** (prioritizing precision, fine-grained filtering). Cross-encoders (which process query + chunk together) are much more accurate than bi-encoders (query/chunk processed separately) but are too slow for initial retrieval, hence only used in the second stage.

**Why These Are "Must-Add Polishes"**: Production RAG evaluations almost universally show that adding hybrid search + rerankers improves recall@5 from around 70% to 85-90% with low marginal cost and mature tooling. **These offer the best cost/benefit**.

**When to Use**:
-   Production RAG (not demos/experiments).
-   Queries containing proper nouns, product IDs, technical terms, or rare words (pure vector search might miss these).
-   Budget allows for an additional 100-300ms latency per query.

**When to Defer**:
-   Experimental phase / MVP (get basic RAG working first).
-   Extremely tight budget / latency constraints (rerankers add an extra model call).

**Representative Tools**:
-   **Hybrid Search**: [Weaviate](https://github.com/weaviate/weaviate) (built-in BM25 + vector + RRF) / [Qdrant](https://github.com/qdrant/qdrant) (supports sparse + dense vectors) / pgvector + Postgres FTS.
-   **Rerankers**: [Cohere Rerank API](https://docs.cohere.com/docs/rerank-overview) (commercial, widely used) / [BGE Reranker](https://huggingface.co/BAAI/bge-reranker-large) (open-source, HuggingFace, good performance in Chinese) / [Jina Reranker](https://jina.ai/reranker).
-   **Framework Built-ins**: LlamaIndex's `SentenceTransformerRerank` / LangChain's `ContextualCompressionRetriever`.

**Paper / Introduction**:
-   [**Pinecone — Rerankers and Two-Stage Retrieval**](https://www.pinecone.com/learn/series/rag/rerankers/) — Best explanation of the reranker mental model.
-   [**Anthropic — Contextual Retrieval**](https://www.anthropic.com/news/contextual-retrieval) (listed above) — Demonstrates hybrid + reranker with benchmarks.

### 🔄 Query Transformations — HyDE / Multi-Query / RAG Fusion

**Mental Model**: Basic RAG embeds the user's query directly for retrieval—but the query's wording, style, or abstraction level often differs significantly from the document (e.g., user asks "What should I do for a stomach ache?", document describes "Differential diagnosis of upper abdominal pain"). Query transformations rewrite the query *before* retrieval, creating versions closer to how documents are phrased.

**3 Representative Techniques**:

| Technique | How it Rewrites | When to Use |
|---|---|---|
| **HyDE** (Hypothetical Document Embeddings) | First, let the LLM generate a "hypothetical answer" to the query; use the embedding of this answer for retrieval. | When query wording/style differs greatly from document phrasing. |
| **Multi-Query** | The LLM rewrites the query into N variations, each retrieved separately, then unioned and deduplicated. | When the query is too short, ambiguous, or has multiple meanings. |
| **RAG Fusion** | Combines Multi-Query with RRF to fuse results from N retrievals for more stable ranking. | Same as Multi-Query, aims for more stable rankings. |

**When Not to Use**: When the query is already long and structured (e.g., RAG over code, user pastes an error stack trace)—rewriting might introduce noise.

**Papers / Implementations**:
-   [**HyDE (Gao et al. 2022)**](https://arxiv.org/abs/2212.10496) — Original paper.
-   [**RAG Fusion (Raudaschl 2023)**](https://github.com/Raudaschl/rag-fusion) — Reference implementation for Multi-Query + RRF.
-   LangChain includes `MultiQueryRetriever` / LlamaIndex includes `HyDEQueryTransform` built-in.

### 🔁 Self-improving RAG — Self-RAG / CRAG / Adaptive RAG (2024 Focus)

**Mental Model**: All RAG techniques above assume a fixed pipeline: "query → retrieve → generate". Self-improving RAG transforms this into an **agentic loop** where the LLM decides whether to retrieve, evaluates retrieval quality, and adjusts the query if necessary. **This is a major focus of RAG research in 2024.**

| Technique | How it Self-Corrects | Paper |
|---|---|---|
| **Self-RAG** | Trains the LLM to output `[Retrieve]` tokens to decide retrieval, then outputs `[IsRel]/[IsSup]/[IsUse]` scores for each retrieved segment. | [Asai et al. ICLR 2024](https://arxiv.org/abs/2310.11511) |
| **CRAG** (Corrective RAG) | A retrieval evaluator scores results; high confidence uses them directly, low confidence falls back to web search, medium confidence triggers query rewriting. | [Yan et al. 2024](https://arxiv.org/abs/2401.15884) |
| **Adaptive RAG** | A classifier first determines query complexity, routing to strategies like "no retrieve / single-step / multi-step". | [Jeong et al. NAACL 2024](https://arxiv.org/abs/2403.14403) |

**Why This is a 2024 Focus**: A fixed pipeline is suboptimal for both simple queries (e.g., "What is the capital of Tokyo?" doesn't need retrieval) and complex ones (multi-hop, cross-document). Letting the LLM decide routing handles both extremes effectively.

**When to Use**: Production RAG with diverse query types (from factual to reasoning), willing to accept 1.5-3x latency for increased accuracy.
**When Not to Use**: Uniform query types / strict budget / extremely sensitive latency requirements.

**Implementations**: LangGraph provides official cookbooks for [Self-RAG](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_self_rag/) + [CRAG](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_crag/) + [Adaptive RAG](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_adaptive_rag/), which can be directly applied.

### 🌳 RAPTOR — Hierarchical Recursive Retrieval (ICLR 2024)

**Mental Model**: Basic chunking creates flat chunks—but the **main thesis of a long document isn't contained in any single chunk**. RAPTOR recursively clusters and summarizes chunks, building a **multi-layer tree**: bottom layer = original chunks, middle layers = summaries of related chunk groups, top layer = overall document summary. Retrieval can then search the entire tree or specific abstraction levels.

**Why it's Useful**:
-   Retrieves answers for **abstract queries** (e.g., "What is the main conclusion of this paper?"—the original chunks might not have this sentence, but the top-level summary does).
-   Retrieves **specific details** effectively (bottom chunks are preserved).
-   Unlike GraphRAG—RAPTOR uses a **tree** (hierarchical summarization), while GraphRAG uses a **graph** (entity-relation).

**When to Use**: Long documents (books, papers, reports) requiring queries at different levels of abstraction; coherent knowledge bases.
**When Not to Use**: Independent chunks (FAQs); frequently changing knowledge bases (rebuilding the tree is costly).

**Paper / Implementation**:
-   [**RAPTOR (Sarthi et al. ICLR 2024)**](https://arxiv.org/abs/2401.18059) ⭐ — Original paper.
-   [**parthsarthi03/raptor**](https://github.com/parthsarthi03/raptor) — Official reference implementation.
-   LlamaIndex has built-in `RAPTOR pack`.

### 🧬 DSPy — Programmatic Optimization Without Prompting (Path 3 Paradigm)

**Mental Model**: Traditional RAG/Agents involve manually writing prompts and chains. DSPy **eliminates prompt writing**—you define "signatures" (input/output types) and write programs (chain structures); DSPy then compiles the optimal prompts, few-shot examples, and retriever settings using LLMs. Proposed by Stanford NLP group in 2024 and championed by Karpathy, it's increasingly adopted in production.

**When to Use**:
-   Your RAG prompts have accumulated over 6 months and are hard to maintain; you want automatic optimization.
-   The same program needs to switch between different LLM providers (DSPy recompiles automatically).
-   Your agent system has multiple steps; you want to track metrics and traces.

**When Not to Use**:
-   You only have one prompt and don't need optimization.
-   You are new to LLMs and haven't explored prompting yet.

**Representative Repo**: [**stanfordnlp/dspy**](https://github.com/stanfordnlp/dspy) ★ **34.4k** MIT, official Stanford NLP group, actively maintained.

**How it Integrates with RAG**: DSPy is **compatible with all RAG techniques** discussed—you can use GraphRAG / Hybrid Search / Reranking as DSPy modules and compile them. It's an overarching typing system for RAG construction.

→ **Parallel to Path 1 / Path 2 Reasoning**: Path 1 is "manual prompt writing", Path 2 is "training reflection into model weights", **DSPy is Path 3 "programmatic search for optimal prompts"**. It's especially useful for advanced scenarios in Stage 7 §Multi-agent.

### 📊 Overview of Advanced RAG Techniques — 2025-2026 Main Themes ⭐

Advanced RAG research in 2024-2025 is converging on **3 main themes**:

1.  **🧠 Merging KG + Memory** — Moving from flat vector stores to "structured, evolving, associative" knowledge representations. Representatives: [**HippoRAG 2**](https://arxiv.org/abs/2502.14802) (Hippocampus-inspired, KG + PageRank, cross-document multi-hop), A-MEM, KAG.
2.  **🎬 Multimodal RAG** — Moving from text retrieval to native image / video / table retrieval. Representatives: [**ColPali**](https://arxiv.org/abs/2407.01449) (direct image embedding from PDF pages, bypassing OCR), TV-RAG, MegaRAG.
3.  **🤖 Agentic RAG** — Retrieval evolves from a fixed pipeline into a tool within an agent loop (agent decides how many times/how to retrieve). Representatives: A-RAG, Self-RAG (covered in §Self-improving RAG).

**2 Other Areas Worth Exploring**:
-   **🛡 RAG Security** — Corpus poisoning / prompt injection become critical in production considerations. Representatives: [RAGPart / RAGMask](https://arxiv.org/abs/2512.24268).
-   **🔧 Prompting is Dead** — Systems automatically search for optimal prompt + retriever combinations. Representatives: [**DSPy**](https://github.com/stanfordnlp/dspy) (Stanford's "programming not prompting" paradigm, see §DSPy subsection above).

**5 Representative Works for Deep Dive** (quick reference):

| Technique | One-Liner | Link |
|---|---|---|
| **HippoRAG 2** | KG + Personalized PageRank, cross-document multi-hop, hippocampus-inspired | [Gutiérrez et al. ICML 2025](https://arxiv.org/abs/2502.14802), [OSU-NLP-Group/HippoRAG](https://github.com/OSU-NLP-Group/HippoRAG) ⭐ |
| **ColPali** | Direct image embedding from PDFs, bypassing OCR, multimodal RAG entry point | [Faysse et al. 2024](https://arxiv.org/abs/2407.01449) |
| **A-RAG / SoK Agentic RAG** | Retrieval as a tool, agent decides retrieval frequency/method | [Ayanami0730/arag](https://github.com/Ayanami0730/arag), [SoK survey](https://arxiv.org/abs/2603.07379) ⭐ |
| **DSPy** | No prompt writing, program + signature for auto-optimization | [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy) ★ 34.4k |
| **LightRAG** | Lightweight alternative to MS GraphRAG, EMNLP 2025 | [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG) ★ 35.1k (already in §GraphRAG section) |

<details>
<summary>📚 Full Overview — 12 Other Advanced RAG Techniques Worth Knowing (Expand to View)</summary>

| Technique | One-Liner | Year / Paper |
|---|---|---|
| **Sentence-Window Retrieval** | Embed sentences, retrieve +/- N sentence window | Built into LlamaIndex |
| **Parent-Child / Small-to-Big** | Embed small chunks, retrieve parent chunks | LangChain `ParentDocumentRetriever` |
| **Multi-Vector Retrieval** | One chunk, multiple embeddings (summary / original / hypothetical question) | LangChain `MultiVectorRetriever` |
| **ColBERT / Post-Interaction Retrieval** | Token-level comparison instead of pooled embeddings | [Khattab & Zaharia 2020](https://arxiv.org/abs/2004.12832), [RAGatouille](https://github.com/AnswerDotAI/RAGatouille) |
| **LongRAG** | Large chunks (4k) + long-context reader, reduces retrieval frequency | [Jiang et al. 2024](https://arxiv.org/abs/2406.15319) |
| **MemoRAG** | Memory model compresses KB into latent memory, retrieval triggered by cues | [Qian et al. 2024](https://arxiv.org/abs/2409.05591) |
| **KAG** (Knowledge-Augmented Generation) | Strict schema KG + logical reasoning, finance / medical / legal domains | [Liang et al. 2024 (Ant Group)](https://arxiv.org/abs/2409.13731) |
| **MiA-RAG** (Mindscape-Aware) | First build high-level document summaries (mindscape) to guide retrieval and answers | [arXiv:2512.17220](https://arxiv.org/abs/2512.17220) ⭐ 2025-12 |
| **QuCo-RAG** (Quality-Controlled) | Uses pretraining statistics to determine if retrieval is needed; rare entity triggers search, reducing hallucination | [arXiv:2512.19134](https://arxiv.org/abs/2512.19134) ⭐ 2025-12 |
| **MegaRAG** | Multimodal KG, extracts entities + relations + visuals from long documents, builds hierarchical graphs | [arXiv:2512.20626](https://arxiv.org/abs/2512.20626) ⭐ 2025-12 |
| **TV-RAG** | Training-free time-aware RAG, aligning long videos with subtitles + visuals | [arXiv:2512.23483](https://arxiv.org/abs/2512.23483) ⭐ 2025-12 |
| **RAGPart / RAGMask** | Lightweight defense against RAG corpus poisoning attacks | [arXiv:2512.24268](https://arxiv.org/abs/2512.24268) ⭐ 2025-12 |

</details>

## 🌉 From RAG to Memory — Why RAG Isn't Enough

By now, you should be able to run basic RAG and understand several production levers. However, looking back at the 3 problem domains listed in §Context Engineering—you've only addressed **Retrieval**, and haven't touched **Memory Management**. Why are these treated separately?

RAG addresses "retrieve relevant snippets from **external knowledge bases**"—but agents also need to "remember things **themselves** across conversations / sessions". These are not the same problem:

| Dimension | RAG | Memory |
|---|---|---|
| Content Source | **External** (PDFs / documents / web / DB) | Agent's **own conversations / experiences** |
| Writing Time | Ingested once, retrieved repeatedly | Written every turn, potentially at every task |
| Content Nature | Primarily static facts, documentary knowledge | Dynamic: user preferences, past interactions, accumulated lessons |
| Can it Replace RAG? | — | No—you wouldn't treat every PDF as "memory" |
| Can it Be Replaced by RAG? | — | No—RAG won't "remember what the user said last time" |

**3 Scenarios Where RAG Is Insufficient** (Corresponding to Memory's Role):

1.  **Remembering User Preferences / Persona Across Sessions**—User told the agent "I'm vegan" last week; this week, the agent remembers not to recommend meat dishes. RAG knowledge bases don't update this automatically.
2.  **Accumulating Agent's Past Success/Failure Lessons** (Reflexion's domain)—An agent fails a task the first time, reflects on "why it failed," stores this, and retrieves it on similar future tasks to avoid repeating mistakes. RAG knowledge bases don't "remember its own failures."
3.  **Intermediate States in Long-Horizon Tasks**—An agent running a 100-step task needs to retain working memory without loss. RAG is not suitable for this type of "short-term + structured + high-frequency writing" state.

→ **Conclusion**: RAG and Memory are **complementary**, not mutually exclusive. Production agents typically need **both**: RAG for external knowledge, Memory for self-reflection and user interaction history. The next section, §Memory Design, will guide you in choosing the right memory pattern.

## 🧠 What is Memory + How to Design It

> 📺 **Visual Learning**: [Hung-Yi Lee 2025 Lecture 2 — Understanding AI Agent Principles in One Lecture (Includes Read/Write/Reflection Memory Modules)](https://www.youtube.com/watch?v=M2Yg1kwPpts) (NTU Machine Learning in the Era of Generative AI 2025)

### Short-term vs. Long-term Memory — Establishing a Mental Model First

| Aspect | Short-term Memory | Long-term Memory |
|---|---|---|
| **Chinese Term** | 短期記憶 | 長期記憶 |
| **Source** | Current conversation content | Information preserved across sessions or over a long period |
| **Duration** | Short, typically limited to the current session | Long, can span across sessions |
| **Technical Basis** | Context window / prompt | Memory store / user profile / vector database |
| **Suitable For** | Task details, recent conversation points | Stable preferences, long-term goals, background information |
| **Limited by Context Length?** | Yes, due to model's limited view of content | Less so, as it can be stored externally and a small relevant piece retrieved and placed back into context |
| **Real-world Analogy** | Phone verification code just received, the previous sentence in an ongoing conversation | Learned knowledge, library, knowledge base, books read |

Here, a "session" can be understood as a continuous interaction, such as a single chat conversation, a specific task, or a single agent execution.

### 3 Design Patterns (When to Use What) ⭐ Essential for Track B

**Not all agents require an external memory store. Choosing the wrong memory architecture can lead to 10x token usage for the same effect.**

This is the mental model to establish before starting exercises. The exercises (1-5) in the following section simulate "Pattern 3: Vector Store", but you might not need such complexity in production.

| Pattern | Suitable Scenarios | Implementation | Cost |
|---|---|---|---|
| **1. Naive Buffer**<br>(Stuff Everything in Context) | Short conversations, ≤ 10 turns, agent doesn't need to remember across sessions | Send the entire conversation history into the prompt every time | Linearly increasing; burns tokens quickly |
| **2. Summary + Recent**<br>(Summarize old parts + Keep last N turns) | Medium-to-long conversations, ~50 turns, want to compress history without losing too much | Every N turns, ask the LLM to summarize older history into one part; Prompt = `summary + last N turns` | Moderate; involves LLM summarization cost |
| **3. Vector Store + Retrieval**<br>(External Store + Semantic Search per turn) | Cross-session interactions, knowledge base scenarios, agent needs to "recall" distant information | Embed past messages → Store in Vector DB → Retrieve relevant snippets per query and include in prompt | High (vector computation + storage), but stable token usage |

**How to Choose**:

-   Conversational chatbots without cross-session needs → **Pattern 1**.
-   Agents with long conversations needing to recall today's discussion → **Pattern 2**.
-   Agents with cross-session needs + knowledge base (common scenario for this stage's exercises) → **Pattern 3**.
-   Large-scale production agents → Typically **a hybrid** of Pattern 2 for recent history and Pattern 3 for long-term memory.

> 💡 **Track B Focus**: When building multi-agent systems in Stage 7, each agent will likely have its "own memory" + "shared memory"—requiring a combination of **Patterns 2 + 3**. Understanding these 3 patterns thoroughly in this stage will prevent memory design bottlenecks in Stage 7.

### ⭐ 5 Mainstream Production Memory Layers (Choose by Use Case)

After understanding the 3 patterns, you don't need to build memory stores from scratch in production. Here are 5 active, Apache-2.0 / MIT licensed frameworks, each excelling in specific areas:

| Framework | Stars | License | Primary Use Case | Key Features |
|---|---|---|---|---|
| [**agentmemory**](https://github.com/rohitg00/agentmemory) | 7.7k★ | Apache-2.0 | **Coding agent cross-session memory** | MCP-universal (integrates with Claude Code, Cursor, Gemini CLI, Codex, Hermes, OpenClaw), 95.2% R@5, 92% token saving, 51 MCP tools + 12 auto hooks, benchmark-driven. |
| [**mem0**](https://github.com/mem0ai/mem0) | 55.6k★ | Apache-2.0 | **Chatbot / Personal Assistant user-level memory** | Auto fact extraction + forgetting + namespace, production-tested, largest community. |
| [**Letta**](https://github.com/letta-ai/letta) (formerly MemGPT) | 22.7k★ | Apache-2.0 | **Long-session agents** (monthly basis) | OS-style paging memory (working + archival layers), persona stability, original MemGPT paper origin. |
| [**Zep**](https://github.com/getzep/zep) | 4.6k★ | Apache-2.0 | **Temporal KG-based memory** | Builds conversation history into a temporal knowledge graph, enabling time-aware reasoning and audit trails. |
| [**LangMem**](https://github.com/langchain-ai/langmem) | 1.4k★ | MIT | **LangChain-native memory** | Official LangChain memory library, integrates directly with LangGraph, suitable for existing LangChain stacks. |

**How to Choose**:
-   Building coding agents → **agentmemory** (MCP-native, aligns perfectly with Stage 5 ecosystem).
-   Developing chatbots / personal assistants → **mem0** (most mature, largest community).
-   Creating long-running agents (weeks/months) → **Letta** (OS-paging excels here).
-   Requiring time-series data + audit trails → **Zep** (temporal KG).
-   Already committed to LangChain stack → **LangMem** (avoid framework hopping).

**Additional Official Docs**: [Anthropic Memory Tool](https://docs.claude.com/en/docs/agents-and-tools/tool-use/memory-tool) (Claude's official tool-based memory, file-based, direct API calls), [LangChain Memory Concepts](https://python.langchain.com/docs/concepts/memory/) (comparison of memory classes within the framework).

### Advanced: CoALA Framework — A 4-Layer Taxonomy for Agent Memory

[**Sumers et al. 2023 — Cognitive Architectures for Language Agents**](https://arxiv.org/abs/2309.02427) categorizes agent memory into 4 types, forming the most common mental model today:

| Type | Stores What | Corresponding Example |
|---|---|---|
| **Working Memory** | Current task context | LLM context window itself |
| **Episodic Memory** | Specific experiences from past tasks | Reflexion's self-reflection records, past trajectories |
| **Semantic Memory** | Abstract facts / knowledge | RAG knowledge base, user profiles, preferences |
| **Procedural Memory** | How to perform actions / skills | Tool definitions, [Skills (Stage 5.3)](05-claude-code-ecosystem.md#53--skillsclaude-code-的行為層-claude-code-生態最關鍵的一層) |

→ **Why it's Useful**: The 3 patterns discussed (buffer / summary / vector) primarily handle working + episodic memory. Production agents need to design for all 4 layers—CoALA serves as a checklist to identify which layers your agent might be missing.

### Advanced: Generative Agents — Triple Score Weighting (Classic Case Study)

The [**Park et al. 2023 — Generative Agents: Smallville**](https://arxiv.org/abs/2304.03442) simulation featured 25 NPCs, each with its own memory stream. Retrieval used a weighted combination of three scores:

-   **Importance**: LLM assigns a 1-10 importance score to each memory (eating = 2, breakup = 9).
-   **Recency**: Exponential decay based on time.
-   **Relevance**: Embedding similarity to the current query.

The final score = `α·importance + β·recency + γ·relevance`, ranked to retrieve top-k. **This is the conceptual framework for many production memory layers (mem0 / Letta) from 2024-2025.**

> 💻 **Official Code**: [joonspk-research/generative_agents](https://github.com/joonspk-research/generative_agents) ★ The paper's accompanying Smallville simulation code repository. Refer here for implementing memory streams and triple-score retrieval.

### 2024-2026 Latest Memory Works — 3 Main Themes

Memory research in 2024-2026 is focusing on **3 main themes**:

1.  **🧠 Structured, Evolving, Associative Memory** — Moving beyond flat vector stores to human-brain / Zettelkasten-inspired memory structures. Representatives: [**A-MEM**](https://arxiv.org/abs/2502.12110) (automatic linking between memories), [**HippoRAG 2**](https://arxiv.org/abs/2502.14802) (KG + PageRank, hippocampus-inspired).
2.  **📚 Explosive Growth in 2026 Surveys** — Five major surveys and cross-disciplinary syntheses in one year. Representatives: [**Memory in the Age of AI Agents**](https://arxiv.org/abs/2512.13564) (3D taxonomy + benchmarks), [**Memory for Autonomous LLM Agents**](https://arxiv.org/abs/2603.07670) (formalizing the write-manage-read loop).
3.  **🛡 Memory Security Emerges as a Subfield** — As agents run longer, memory becomes vulnerable to cross-session poisoning / unauthorized access attacks. Representatives: [**Memory Security Survey**](https://arxiv.org/abs/2604.16548) (covered in Stage 7 §Security).

**4 Representative Works for Deep Dive**:

| Work | One-Liner | Link |
|---|---|---|
| **Anthropic Memory Tool** | Claude's official tool-based memory, API calls, file-based | [Anthropic Docs](https://docs.claude.com/en/docs/agents-and-tools/tool-use/memory-tool) |
| **A-MEM** (Agentic Memory) | Zettelkasten-inspired, auto-links memories, evolving | [Xu et al. 2025](https://arxiv.org/abs/2502.12110) ⭐ |
| **HippoRAG 2** | KG + Personalized PageRank, cross-document multi-hop, ICML 2025 | [Gutiérrez et al. 2025](https://arxiv.org/abs/2502.14802), [OSU-NLP-Group/HippoRAG](https://github.com/OSU-NLP-Group/HippoRAG) ⭐ |
| **Memory in the Age of AI Agents** (Survey) | 3D taxonomy (temporal / substrate / control) + benchmark compilation | [Hu et al. 2025-12](https://arxiv.org/abs/2512.13564) ⭐ |

<details>
<summary>📚 Full Overview — 8 Other Memory Works Worth Knowing (Expand to View)</summary>

| Work | One-Liner | Year / Paper |
|---|---|---|
| **MemGPT → Letta GA** | OS-paging memory, working/archival layers, strong for long sessions | [Packer et al. 2023](https://arxiv.org/abs/2310.08560) → Letta GA |
| **MemoryBank** | Ebbinghaus forgetting curve, accessed memories strengthened, unused ones decay | [Zhong et al. 2023](https://arxiv.org/abs/2305.10250) |
| **MemoryLLM** | Self-updatable memory parameters embedded within the model weights, not context | [Wang et al. 2024](https://arxiv.org/abs/2402.04624) |
| **mem0** (See §3 Mainstream Memory Layers) | Production memory layer, auto fact extraction + forgetting | [mem0ai/mem0](https://github.com/mem0ai/mem0) |
| **Memory for Autonomous LLM Agents** (Survey) | Formalizes write-manage-read loop, covers 2022-2026 advancements | [arXiv:2603.07670](https://arxiv.org/abs/2603.07670) ⭐ 2026 |
| **From Storage to Experience** (Survey) | Evolutionary framework: Storage → Reflection → Experience stages | [arXiv:2605.06716](https://arxiv.org/abs/2605.06716) ⭐ 2026 |
| **ScrapMem** | Bio-inspired on-device memory, "Optical Forgetting" reduces resolution of old memories | [arXiv:2605.03804](https://arxiv.org/abs/2605.03804) ⭐ 2026-05 |
| **Memory Security Survey** | Risks of cross-session poisoning, unauthorized access, and organizational propagation in long-term memory | [arXiv:2604.16548](https://arxiv.org/abs/2604.16548) ⭐ 2026 |

</details>

## 🧩 Chunking Details (Technical Deep Dive)

Good chunking allows LLMs to generate more precise and complete answers within limited contexts. It's not just about splitting text evenly; it depends on the application scenario and document content. It determines the smallest semantic unit the retriever sees.

A good chunk should achieve two things: **sufficient completeness** for the model to understand context, and **focused content** to minimize retrieval noise. Chunks that are too small lose context, while chunks that are too large can dilute similarity search effectiveness.

**Common Strategies**:

-   **Fixed-Length**: Splits based on character or token count. Simple and stable, but can cut sentences, paragraphs, or tables awkwardly.
-   **Sliding Window**: Overlaps chunks to retain information at boundaries. Increases index size but reduces boundary information loss.
-   **Recursive**: Tries to preserve paragraphs first; if still too long, falls back to sentences, then words. Often a good baseline for RAG entry-level.
-   **Semantic Chunking**: Splits based on embedding similarity or semantic shifts, where similarity between consecutive chunks changes. Suitable for long documents but more complex and costly.
-   **Hybrid Strategies**: Combines different methods based on document structure and application needs. For example, a research paper might need to preserve chapter context, tables, formulas, and citation references.

![Chunking Strategy Flowchart](../resources/diagrams/chunking-strategies.jpg)

> 📚 **Classic Tutorial**: [Greg Kamradt — 5 Levels of Text Splitting](https://github.com/FullStackRetrieval-com/RetrievalTutorials) ★ Essential reading for chunking basics, covering everything from character-based to agentic chunking across five levels, including Jupyter notebooks.

For your first RAG implementation, avoid overly complex strategies. LangChain documentation recommends starting with `RecursiveCharacterTextSplitter` for most scenarios.

Run a baseline version first, then adjust chunking strategies based on retrieval results and failure cases.

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text = "This is a very long document content... (omitting a thousand words here)..."

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
)

chunks = splitter.split_text(text)
print(f"Split into {len(chunks)} chunks")
print(chunks[0])
```

**Intuitive Assessment of Chunking Quality**:

-   Answers missing information or are incomplete: Usually due to small chunks or insufficient overlap.
-   Answers contain correct information but also irrelevant details: Usually due to large chunks or too many retrieved items (high top-k).

**Advanced Considerations**:

-   Chunking is not a one-time setup; it requires iterative refinement based on real queries and failure cases.
-   Chunk size, overlap, top-k, and reranker interact; don't adjust one parameter in isolation.
-   Consider how you would chunk PDFs with images, meeting transcripts with timestamps, or structured data like tables.
-   Advanced chunking variations (Sentence-Window / Parent-Child / Multi-Vector) are covered in the §Overview of Advanced RAG Techniques table.

## 🪞 Advanced: Full Reflexion with Persistent Memory ⭐ Track B Elective

> **This section covers concepts and routing; it's not a practice exercise.** It expands on the basic Reflexion from [Stage 3 §Reflection](03-tool-use-and-hello-agent.md#-reflectionreflexion--self-refine-concept--routing) by explaining why some reflections require persistent memory—this version truly belongs in Stage 6.

**Difference Between Full Reflexion and Self-Refine**:

| Version | Retains within Session | Retains Across Sessions | Memory Pattern Required |
|---|---|---|---|
| **Self-Refine** (Madaan 2023) | Previous round's answer + critic feedback | ❌ Not retained | None required (Pattern 1 buffer is sufficient) |
| **Full Reflexion** (Shinn 2023) | Same as above | ✅ Stores "reflection summaries" from past trials into episodic memory, retrieved into prompts for future similar tasks | **Required** (Pattern 3 vector store or Pattern 2 summary) |

**Why This Version Requires Memory**: The core of Reflexion's verbal reinforcement learning is "agent accumulates lessons across trials"—the agent attempts a task, fails, reflects on "why it failed" and stores it, then retrieves past reflections when encountering similar tasks to avoid repeating mistakes. This requires **persistent episodic memory**, directly connecting to the 3 memory patterns discussed earlier in this stage.

**Typical Architecture** (Full Persistent Memory Version):

```
Actor → Critic → Actor    (Single-round loop, consistent with Stage 3 §Reflection)
       ↑──────────┘
            ↓
   Reflection summary
            ↓
   Episodic memory store
   (Vector / Summary pattern, see §Memory Design Patterns above)
            ↓
   Next task → Retrieve relevant past reflections
            → Prepend to Actor's prompt
            (Accumulates lessons across trials, avoids repeating mistakes)
```

→ **Difference from Stage 3 §Reflection**: Stage 3 focuses on an **in-context loop within a single session** (no external store). This section covers **persistent episodic memory storage + retrieval across trials** to learn from past experiences.

### 📚 Want to Implement / Dive Deeper

**Papers**:
-   [**Reflexion (Shinn et al. 2023)**](https://arxiv.org/abs/2303.11366) ⭐ — The **full version** paper. Algorithm 1 outlines how the memory buffer is used.
-   [**Self-Refine (Madaan et al. 2023)**](https://arxiv.org/abs/2303.17651) — Baseline comparison; version without episodic memory.

**Reference Implementations**:
-   [**noahshinn/reflexion**](https://github.com/noahshinn/reflexion) — Reference implementation by the paper's lead author (includes full episodic memory workflow).
-   [**LangChain — Reflexion**](https://langchain-ai.github.io/langgraph/tutorials/reflexion/reflexion/) — LangGraph version, directly integrable with the RAG pipeline exercise in this stage.
-   [**mem0**](https://github.com/mem0ai/mem0) (listed above) + [**Letta**](https://github.com/letta-ai/letta) (listed above) — Production memory layers that can directly serve as episodic stores for Reflexion.

> 💡 **Delineation with Stage 3 §Reflection**:
> -   To understand "how the reflection loop works and runs in a single turn" → Stage 3 §Reflection.
> -   To understand "how reflections accumulate across sessions and agents learn from past lessons" → This section.
> -   To see how reflection is used in production agents (Cursor / Claude Code) → [Stage 5 §5.6 Harness Internals](05-claude-code-ecosystem.md#56--claude-code-source-解剖reference-harness-implementation-track-b-必看).

## 🤔 Advanced Reasoning / Reflection — 2024-2026 Trends ⭐ Covers Both Tracks

Reflexion is **prompt-based reflection**—LLMs modify themselves during inference. 2024-2025 saw the emergence of a **second path**: **training reflection into the model weights** (OpenAI **o1** / DeepSeek **R1**). You should be aware of both approaches.

### Path 1: Prompt-Based Reflection / Reasoning (Traditional Approach)

| Technique | Core Idea | Paper |
|---|---|---|
| **Self-Consistency** | Sample N reasoning paths, take majority vote — **Simplest & Most Common** | [Wang et al. 2022](https://arxiv.org/abs/2203.11171) |
| **Tree of Thoughts (ToT)** | Reasoning becomes a tree, allowing branching and backtracking; suitable for puzzles / planning. | [Yao et al. 2023](https://arxiv.org/abs/2305.10601) |
| **Graph of Thoughts (GoT)** | Extends ToT beyond trees to arbitrary graph structures. | [Besta et al. 2023](https://arxiv.org/abs/2308.09687) |
| **Chain-of-Verification (CoVe)** | Generate an answer → Ask verification questions to itself → Correct the answer. | [Dhuliawala et al. 2023](https://arxiv.org/abs/2309.11495) |
| **CRITIC** | Tool-augmented self-critique (using search / calculator for verification). | [Gou et al. 2023](https://arxiv.org/abs/2305.11738) |
| **Self-Discover** | Agent first "discovers" the reasoning structure to use before executing. | [Zhou et al. ICML 2024](https://arxiv.org/abs/2402.03620) ⭐ 2024 |
| **Self-Refine / Reflexion** | Covered above / in Stage 3. | Stage 3 §Reflection, this stage §Reflexion |

### Path 2: Trained-in Reasoning / Reflection (Major Shift in 2024-2026)

> 📺 **Visual Learning**: [Hung-Yi Lee 2025 Lecture 7 — How Large Language Models Like DeepSeek-R1 Perform "Deep Thinking" (Reasoning)](https://www.youtube.com/watch?v=bJFtcwLSNxI) (NTU Machine Learning in the Era of Generative AI 2025)

OpenAI's **o1** (Sep 2024), followed by open-source efforts like DeepSeek's **R1** (Jan 2025), **DeepSeek-V4-Pro** (Apr 2026 preview, agent-focused open-source reasoning), Claude Opus 4.7 (Apr 2026), GPT-5.5 (Apr 2026), and Gemini 3.1 Pro (Feb 2026) represent the current frontier. These models have "step-by-step thinking + self-correction" **trained directly into their weights**, automatically unfolding long reasoning chains (thinking tokens) during inference. **This is the biggest paradigm shift in LLMs from 2024-2026**, with all frontier models adopting this approach. The table below lists **current (May 2026) frontiers**—historical predecessors (o1 / R1 / Sonnet 4.5 / Gemini 2.5) are omitted; refer to release dates for lineage.

| Model | Source / Release | Features | Link |
|---|---|---|---|
| **GPT-5.5** | OpenAI 2026-04 (Predecessors: o1 2024-09 → o3 → GPT-5 2025-08 → 5.4 2026-03) | Closed-source, unified reasoning + chat, Thinking budget API, enhanced agent capabilities | [OpenAI](https://openai.com/) |
| **Claude Opus 4.7** | Anthropic 2026 (Predecessors: Sonnet 4.5 / Opus 4.5) | Closed-source, controllable thinking budget (API parameter), **leading in SWE-bench / Terminal-bench** | [Anthropic extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) |
| **Gemini 3.1 Pro** | Google 2026-02 (Predecessors: Gemini 2.5 Thinking 2025, Gemini 3 2025-11) | Closed-source, viewable thinking traces, **GPQA Diamond 94.3%**, leading in price/speed/multimodality | [Gemini API](https://ai.google.dev/gemini-api/docs/thinking) |
| **DeepSeek-V4 / V4-Pro / V4-Flash** | DeepSeek 2026-04 preview (Predecessors: R1 2025-01 → V3.1) | Open-source **MIT license**, agent-focused training, integrated reasoning + tool use + knowledge processing. R series reasoning now mainline. | [HF DeepSeek-V4-Pro](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro), [R1 paper (method baseline)](https://arxiv.org/abs/2501.12948), [CNBC report](https://www.cnbc.com/2026/04/24/deepseek-v4-llm-preview-open-source-ai-competition-china.html) |
| **QwQ-32B / QvQ-72B** | Alibaba Qwen 2024-11 ~ 2026 | Open-source **Apache 2.0**, QwQ-32B remains a top choice for small-size reasoning, QvQ is the visual variant. | [QwQ blog](https://qwenlm.github.io/blog/qwq-32b-preview/) |

### How to Choose Between the Two Paths

| Your Situation | Recommendation |
|---|---|
| Using a general chat model base and want to add reasoning | Path 1 (Prompt-based) — ToT / Self-Consistency / CoVe |
| Budget/latency allows for strongest reasoning | Path 2 — Choose among **GPT-5.5 / Opus 4.7 / Gemini 3.1 Pro / V4-Pro** |
| Want to fine-tune your own reasoning model | Path 2 — Study the R1 paper (method baseline), start from R1-Distill / V4 open-source weights |
| On-device / Extremely tight budget | **QwQ-32B** (Apache 2.0) or R series distilled versions |
| Multi-agent debate / critic scenarios | Path 1 (CRITIC / debate) + [Stage 7 §Multi-agent](07-multi-agent-production.md) |

> 💡 **2025-2026 Trends**:
> - Reasoning models are integrating Reflexion's capabilities into their weights—however, **prompt-based reflection is not obsolete**. Agent loops (controlling reflection timing/content) and multi-agent debates remain essential.
> -   **Open-source is rapidly catching up to closed-source**. DeepSeek-V4-Pro (Apr 2026 preview, MIT license) integrates R1 reasoning into its mainline, trained with an agent-first approach, narrowing the gap with GPT-5.5 / Gemini 3.1 Pro.
> -   **Agent capabilities are becoming the primary selling point**. V4 / Opus 4.7 position agents-as-products (SWE-bench / Terminal-bench / tool use) as headline benchmarks, moving beyond just raw reasoning.
> -   **Both paths will coexist**; production agents will likely leverage both.

## 📏 RAG / Memory Eval — Running is Not Running Accurately

**Why This Section is Crucial**: The biggest pitfall in RAG/Memory systems is "they seem to run, but retrieval accuracy is poor." Without evaluation, you won't know if changing chunk size, embedding model, or adding a reranker actually helps—you'll only have subjective impressions like "the answer seems smoother." Production agents without evaluation are essentially untested.

**3 Core Metrics**:

| Metric | Measures What | Tools |
|---|---|---|
| **Retrieval Recall@K** | Whether the ground truth answer's chunk is within the top-K retrieved chunks. | ragas / TruLens / LangSmith |
| **Answer Faithfulness** | Whether the generated answer is grounded in the retrieved chunks (vs. model hallucination). | ragas / TruLens |
| **Answer Relevance** | How relevant the answer is to the query (avoids off-topic responses). | ragas / LLM-as-judge |

**Representative Frameworks**:

-   [**explodinggradients/ragas**](https://github.com/explodinggradients/ragas) ★ **13.9k** Apache-2.0 ⭐ — The standard tool for RAG evaluation, including 8+ metrics (faithfulness, answer relevance, context precision, context recall, etc.), supporting both reference-free and reference-based evaluation.
-   [**TruLens**](https://github.com/truera/trulens) — Integrates observability and evaluation, with good LangChain / LlamaIndex support.
-   [**LangSmith**](https://docs.langchain.com/langsmith) — LangChain's official evaluation + tracing platform (closed-source SaaS).

**How to Start**: After completing Exercise 4 (Full RAG Pipeline), integrate RAGAS evaluation to measure a baseline. Then, adjust chunking/embedding/top-k and observe how the metrics change. **Without this step, parameter tuning is just guesswork.**

→ Stage 7 §Evaluation builds upon this section, extending evaluation to multi-agent systems / full harnesses.

## 🛠 Hands-on Exercises (Illustrative Basics)

### Exercise 1: Embeddings
Embed 100 sentences, find nearest neighbors for a query. Understand the meaning of vector distances.

### Exercise 2: Vector DB
Store embeddings in Chroma, perform semantic queries. Compare the results against keyword search.

### Exercise 3: Chunking Comparison
Use three chunking methods on the same document: fixed length, paragraph-based, heading-aware. Compare top-k results for 5 real questions, noting which method retrieves the correct context more easily.

### Exercise 4: Full RAG Pipeline
Chunk a PDF → Embed → Retrieve top-k → Generate an answer. This is the basic skeleton for most RAG applications.

### Exercise 5: Long-term Memory
Enable an agent to remember things across multiple conversation turns. Use `mem0` or build your own with a vector store.

## 🛠 Recommended Tools for Common Memory / RAG Use Cases (Categorized by Purpose)

Unsure where to start with tool selection? Here are commonly used combinations in the industry post-2025—**choose based on your scenario ("Entry Point") and follow the links for deeper dives**:

| Scenario | Recommended Tools | Why |
|---|---|---|
| **First RAG Implementation** (Quickest Start) | [Chroma](https://github.com/chroma-core/chroma) + [LlamaIndex](https://github.com/run-llama/llama_index) | Local-first, zero-ops, beginner-friendly quickstart. Default for Stage 6 exercises. |
| **Enterprise-Grade RAG Framework** (Alternative to LangChain/LlamaIndex) | [Haystack (deepset)](https://github.com/deepset-ai/haystack) ★ 25.2k Apache-2.0 | Open-source by deepset, production-oriented orchestration, mature for enterprise NLP scenarios. |
| **Agent Long-Term Memory** (See §3 Mainstream Memory Layers) | [agentmemory](https://github.com/rohitg00/agentmemory) / [mem0](https://github.com/mem0ai/mem0) / [Letta](https://github.com/letta-ai/letta) / [Zep](https://github.com/getzep/zep) / [LangMem](https://github.com/langchain-ai/langmem) | Detailed above in §5 Mainstream Production Memory Layers. |
| **RAG / Memory Evaluation** (Must-Have) | [ragas](https://github.com/explodinggradients/ragas) ★ 13.9k | Standard RAG evaluation tool, 8+ metrics, reference-free + reference-based. |
| **Production-Scale RAG** (Millions of Docs) | [Qdrant](https://github.com/qdrant/qdrant) + LlamaIndex | Rust-based vector DB, faster than Chroma at scale. |
| **Existing Postgres Environment** | [pgvector](https://github.com/pgvector/pgvector) | Postgres extension, unified SQL + vector in one DB, simplest ops. |
| **Enterprise RAG + Web UI** | [RAGFlow](https://github.com/infiniflow/ragflow) | Robust document parsing (OCR/tables/layout), enterprise-grade, includes Web UI. |
| **Chinese RAG Template** | [Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat) | Widely used in Chinese community, local LLM integration (ChatGLM/Qwen/Llama), good Chinese defaults. ★ 38k+, Apache-2.0. ⚠️ Last update Nov 2025 (marginal). |
| **Advanced: Contextual Retrieval** | [Anthropic Cookbook](https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide) | Claude with prompt caching for contextual chunking (**See §Advanced RAG Techniques**). |
| **Advanced: Knowledge Graph Reasoning** | [LightRAG](https://github.com/HKUDS/LightRAG) / [Microsoft GraphRAG](https://github.com/microsoft/graphrag) | Knowledge graph + RAG, entity-relation reasoning (See §Advanced RAG Techniques). |
| **Tutorial Collection** | [ai-engineering-hub](https://github.com/patchy631/ai-engineering-hub) | RAG + agent tutorial collection, Jupyter notebook format. |

**Recommended Entry Sequence**:
1.  First essential installation: **Chroma + LlamaIndex** (for Stage 6 exercises).
2.  For agent memory needs: Add **mem0** (simplest memory layer).
3.  For production scaling: Switch to **Qdrant** or **pgvector**.
4.  For upgrading to advanced RAG: Explore techniques in the §Advanced RAG Techniques section.

## 🎯 Featured Projects (Templates / Specs / Example Collections)

Categorized for quick reference; **choose by use case ("Entry Point") and follow the links for deeper dives**.

| Category | Project | ⭐ | Who It's For | Why Recommended / Notes |
|---|---|---|---|---|
| **RAG Framework**<br>(Full Pipeline) | [LlamaIndex](https://github.com/run-llama/llama_index) | ⭐⭐⭐⭐⭐ | Applications focused on documents | Core RAG library, provides document loaders / chunking / retrieval / query engines. ★ 49k+ |
| | [infiniflow/ragflow](https://github.com/infiniflow/ragflow) | ⭐⭐⭐⭐⭐ | Teams shipping RAG to non-developers | Production-grade RAG engine, deep document understanding (layout/tables/OCR) + hybrid retrieval + agent loops + Web UI. ★ 79k+, Apache-2.0. |
| | [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG) | ⭐⭐⭐⭐ | Those exploring research-grade graph + long-context memory methods | Graph + vector hybrid retrieval + summarization-based memory, backed by EMNLP 2025 paper. ★ 34k+, MIT. Research-oriented codebase. |
| **Vector DB**<br>(Local-First) | [Chroma](https://github.com/chroma-core/chroma) | ⭐⭐⭐⭐⭐ | Exercises 2 / 4, easiest vector DB to start with | Open-source embedding database, runs locally, in-memory/SQLite backend, zero ops. ★ 27k+, Apache-2.0. **Install**: `pip install chromadb` |
| **Vector DB**<br>(Production Scale) | [Qdrant](https://github.com/qdrant/qdrant) | ⭐⭐⭐⭐⭐ | When Chroma can't keep up, need production scale | Rust-based vector DB, offers cloud and self-hosted options. ★ 31k+ |
| **Vector DB**<br>(Hybrid) | [Weaviate](https://github.com/weaviate/weaviate) | ⭐⭐⭐⭐ | Production deployment + schema constraints | Built-in modules (text2vec/generative/classification), schema-driven, native BM25 + vector hybrid. ★ 16k+ |
| **Vector DB**<br>(Existing Postgres) | [pgvector](https://github.com/pgvector/pgvector) | ⭐⭐⭐⭐ | Teams already using Postgres | Postgres extension, unified SQL + vector in one DB, simplest ops. ★ 21k+ |
| **Memory Framework**<br>(Auto Fact Extraction) | [mem0ai/mem0](https://github.com/mem0ai/mem0) | ⭐⭐⭐⭐⭐ | Personal assistants / chatbots needing user-level memory | Self-refining memory layer, cross-session fact storage. ★ 54k+ |
| **Memory Framework**<br>(OS-Paging) | [Letta (formerly MemGPT)](https://github.com/letta-ai/letta) | ⭐⭐⭐⭐ | Agents running for extended periods (months) | Hierarchical memory (working/archival), OS-paging concept. ★ 22k+ |
| **Memory (In-Framework)** | [LangChain — Memory](https://python.langchain.com/docs/concepts/memory/) | ⭐⭐⭐ | Already using LangChain | 4 abstract memory types (buffer/summary/vectorstore-backed/entity). |
| **Advanced RAG Techniques** | [Anthropic — Contextual Retrieval Cookbook](https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide) | ⭐⭐⭐⭐⭐ | After basic RAG, want to upgrade | Claude with prompt caching for contextual chunking (full end-to-end examples). |
| **Chinese RAG Template** | [chatchat-space/Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat) | ⭐⭐⭐⭐ | Chinese knowledge bases / RAG applications | Widely used in Chinese community, local LLM support (ChatGLM/Qwen/Llama/Ollama), good Chinese defaults. ★ 38k+, Apache-2.0. ⚠️ Last update Nov 2025 (marginal). |
| **Tutorial Collection** | [ai-engineering-hub](https://github.com/patchy631/ai-engineering-hub) | ⭐⭐⭐⭐ | Interested in seeing "how the same concept is implemented in different contexts" | Thematic LLM / RAG / agent tutorial collection, Jupyter notebooks, useful across many stages. ★ 34k+, MIT. |
| **Production AI Assistant**<br>(Learn to Ship RAG) | [onyx](https://github.com/onyx-dot-app/onyx) (formerly Danswer) | ⭐⭐⭐⭐⭐ | Want to see "how RAG-driven AI assistants are productionized" | Open-source enterprise AI assistant, cross-LLM support, full ingest/retrieval/chat/admin. ★ 29.4k, active maintenance. |
| **RAG Cookbook**<br>(30+ Techniques) | [NirDiamant/RAG_Techniques](https://github.com/NirDiamant/RAG_Techniques) | ⭐⭐⭐⭐⭐ | After basic RAG, want to explore various implementations | Large RAG techniques cookbook, includes Self-RAG / HyDE / Multi-Query / Adaptive and 30+ Jupyter notebook examples. |
| **DSPy**<br>(Programming not Prompting) | [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy) | ⭐⭐⭐⭐⭐ | Used LLMs for a while, want to auto-optimize prompts + chains | Stanford NLP group, ★ 34.4k MIT, Path 3 paradigm (See §DSPy in §Advanced RAG Techniques) |
| **RAG / Memory Eval**<br>(Must-Have) | [explodinggradients/ragas](https://github.com/explodinggradients/ragas) | ⭐⭐⭐⭐⭐ | After completing Exercise 4 (Full RAG Pipeline), want to measure retrieval accuracy | Standard RAG evaluation tool, 8+ metrics, reference-free + reference-based. ★ 13.9k Apache-2.0 |

## ✅ Self-Check Before Entering Stage 7

Can you:
- [ ] Write a 50-line RAG pipeline (load → chunk → embed → store → query → answer)?
- [ ] Explain why naive chunking fails on long documents?
- [ ] Design different chunking strategies for API docs, PDFs, and tables?
- [ ] Choose between Chroma, Qdrant, and pgvector based on scale?
- [ ] Differentiate between "giving an agent memory" and "using RAG"?
- [ ] Explain where RAG and Memory complement each other (refer to the table in §From RAG to Memory)?

If yes → Proceed to [Stage 7 — Multi-Agent · Advanced Applications](07-multi-agent-production.md).
