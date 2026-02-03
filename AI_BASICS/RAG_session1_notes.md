# 📘 RAG (Retrieval Augmented Generation) — Session Notes

---

## Table of Contents

1. [What is an LLM?](#1-what-is-an-llm)
2. [Limitations of LLMs](#2-limitations-of-llms)
3. [The Smart Intern Analogy](#3-the-smart-intern-analogy)
4. [What is RAG?](#4-what-is-rag)
5. [The Chef Analogy](#5-the-chef-analogy)
6. [RAG Pipeline — Data Preparation](#6-rag-pipeline--data-preparation)
7. [RAG Pipeline — Retrieval & Generation](#7-rag-pipeline--retrieval--generation)
8. [RAG Paradigms](#8-rag-paradigms)
9. [RAG Architecture (In-Depth)](#9-rag-architecture-in-depth)
10. [Demo Walkthrough](#10-demo-walkthrough)
11. [How to Improve RAG](#11-how-to-improve-rag)
12. [Challenges in RAG](#12-challenges-in-rag)
13. [Key Takeaways](#13-key-takeaways)
14. [References](#14-references)

---

## 1. What is an LLM?

A **Large Language Model (LLM)** is a deep learning model based on the **Transformer architecture**, trained on vast amounts of data (billions of parameters). Its core ability is **next-token prediction** — given some text, it predicts what comes next.

> **Example:** You type _"The capital of India is"_ → the LLM completes it with _"New Delhi."_

Other related terms you may hear:

- **SLM** — Small Language Model
- **MLM** — Medium Language Model

**Primary use cases:** sentence completion, question answering, translation, summarisation, analysis.

---

## 2. Limitations of LLMs

| Limitation                    | Explanation                                                                                                      |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| **Hallucination**             | The model can confidently generate wrong or fabricated answers, especially for topics outside its training data. |
| **Outdated Knowledge**        | Training data has a cutoff date; the model doesn't know anything after that.                                     |
| **No Access to Private Data** | LLMs can't access your company's internal or proprietary documents unless you provide them.                      |
| **Overconfidence**            | LLMs always sound confident — even when they are completely wrong.                                               |

---

## 3. The Smart Intern Analogy

This is a handy mental model for understanding why LLMs fall short on their own:

```
┌─────────────────────────────────────────────────┐
│              THE SMART INTERN                    │
│                                                 │
│  ✅ Speaks extremely well                       │
│  ✅ Has broad general knowledge                 │
│  ❌ Has NO access to company internal files     │
│  ❌ Will GUESS answers with 100% confidence     │
│                                                 │
│  Asked: "What is the leave policy?"             │
│  Intern: "Typically companies give 15 days…"   │
│          (sounds confident — but may be WRONG) │
│                                                 │
│  💡 Confidence ≠ Correctness                   │
└─────────────────────────────────────────────────┘
```

This is exactly how an LLM behaves — **confident but potentially incorrect** when it doesn't have the right context.

---

## 4. What is RAG?

**RAG = Retrieval Augmented Generation**

Instead of making the LLM guess, you **give it the data to look up** before generating an answer.

### High-Level RAG Flow

```
                        ┌──────────────┐
  User asks a           │              │
  question ──────────►  │   Knowledge  │
                        │     Base     │
                        │  (Docs/DB)   │
                        └──────┬───────┘
                               │
                    Relevant chunks retrieved
                               │
                               ▼
                        ┌──────────────┐
   Question ──────────► │     LLM      │ ──────► Answer
                        │  (Generator) │          to User
                        └──────────────┘
```

**In plain words:**

1. The user's question goes to a **knowledge base**.
2. Relevant information (chunks) is **retrieved**.
3. The retrieved context + the original question are sent to the **LLM**.
4. The LLM generates an answer **grounded in actual data**.

---

## 5. The Chef Analogy

A great way to remember how each piece of RAG works:

```
┌────────────────────────────────────────────────────────┐
│                   🍳 THE CHEF ANALOGY                  │
│                                                        │
│  📖 Recipe Book          →  Knowledge Base             │
│  🔍 Finding the recipe   →  Vector Retrieval           │
│  📝 The recipe steps     →  Retrieved Chunk            │
│  👨‍🍳 Cooking               →  LLM Generation           │
│  🍽️  Dish quality          →  Answer Accuracy           │
│                                                        │
│  The chef doesn't cook from memory — he LOOKS IT UP   │
│  in the book first. That's exactly what RAG does.      │
└────────────────────────────────────────────────────────┘
```

---

## 6. RAG Pipeline — Data Preparation

Data preparation is the **foundation** of a good RAG system. If the data isn't prepared well, retrieval will suffer.

### Full Data Preparation Flow

![alt text](rag_architecture.png)

### 6a. Chunking

Chunking splits your data into smaller, relevant pieces. Two key parameters:

- **Chunk Size** — how many characters/tokens in one chunk (e.g., 500–2000 characters)
- **Overlap** — how many characters are shared between consecutive chunks

```
  Chunk 1: [=============================]
  Chunk 2:                    [=============================]
                              ^^^^^^^^
                              Overlap (e.g., 50–200 chars)
```

**Why overlap matters:** If Chunk 2 refers back to something in Chunk 1 (e.g., a pronoun like "he" referring to a name in Chunk 1), the overlap ensures that connection isn't lost during retrieval.

**Chunking strategies:**

1. **Fixed-size chunking** — split every N characters (simplest)
2. **Delimiter-based chunking** — split on paragraphs, sentences, or punctuation
3. **Semantic/intelligent chunking** — use a model to decide where meaningful boundaries are

### 6b. Embedding

Embedding converts text chunks into **vectors** — numerical coordinates in a high-dimensional space.

```
  "India"    →  [0.12, 0.45, 0.78, …]   ● India
  "Delhi"    →  [0.14, 0.47, 0.80, …]     ● Delhi   (close to India)
  "Paris"    →  [0.91, 0.22, 0.11, …]
                                            ● Paris   (far from India)

  Similar meanings = closer vectors in space
```

Embeddings also include **positional encoding** — so the model knows the _order_ of words in a sentence.

### 6c. Why a Vector Database?

A regular SQL/NoSQL database stores data for _humans_ to query. A **vector database** stores data in a way that makes **similarity search** fast and efficient for machines.

---

## 7. RAG Pipeline — Retrieval & Generation

Once data is stored, here's what happens at **query time**:

```
  User Query
      │
      ▼
  Embed the Query  ──────────────────┐
  (convert to vector)                │
                                     ▼
                            ┌─────────────────┐
                            │  VECTOR DB      │
                            │  Similarity     │
                            │  Search (Top-K) │
                            └────────┬────────┘
                                     │
                         Retrieved Chunks
                                     │
                                     ▼
                            ┌─────────────────┐
  Original Query ──────►    │      LLM        │  ──►  Final Answer
                            │   (Generation)  │
                            └─────────────────┘
```

**Key terms:**

- **Top-K** — how many of the most similar chunks to retrieve (e.g., K=2, K=5, K=7)
- **Cosine Similarity** — the standard method to measure how close two vectors are

---

## 8. RAG Paradigms

There are several patterns/approaches for building RAG systems:

```
┌─────────────────────────────────────────────────────────────┐
│                     RAG PARADIGMS                            │
│                                                             │
│  ① NAIVE / STANDARD RAG                                     │
│     Query → Retrieve → Generate                             │
│     Simple, fast, good for basic FAQ / narrow use cases     │
│                                                             │
│  ② ADVANCED RAG                                             │
│     Adds layers BEFORE and AFTER retrieval:                 │
│     • Query Rewriting / Expansion (before)                  │
│     • Filtering                                             │
│     • Re-ranking                                            │
│     • Fusion (combine results from multiple sources)        │
│     Better accuracy, handles vague queries                  │
│                                                             │
│  ③ MODULAR RAG                                              │
│     Plug-and-play — only activate modules when needed       │
│     • Router-based: directs queries to right model/DB       │
│     • Graph RAG: builds knowledge graphs for relationships  │
│     • Agentic RAG: the RAG can take actions autonomously    │
└─────────────────────────────────────────────────────────────┘
```

### Advanced RAG — Detailed Flow

```
  User Query
      │
      ▼
  ┌─────────────────┐
  │ Query Expansion  │  ← Use another model to rewrite/expand
  │  / Rewriting     │     the query with better keywords
  └────────┬────────┘
           ▼
  ┌─────────────────┐
  │   Retrieval      │  ← Fetch more relevant chunks
  └────────┬────────┘
           ▼
  ┌─────────────────┐
  │   Filtering      │  ← Remove irrelevant results
  └────────┬────────┘
           ▼
  ┌─────────────────┐
  │   Re-ranking     │  ← Reorder by relevance using a model
  └────────┬────────┘
           ▼
  ┌─────────────────┐
  │  LLM Generation  │  ← Generate grounded answer
  └─────────────────┘
```

### Graph RAG

When documents have lots of **relationships**, a graph structure is better than plain vector search.

```
  Documents ──► Extract Entities & Relations ──► Graph DB (e.g., Neo4j)
                                                      │
                                                      ▼
                                              Query retrieves
                                              not just facts,
                                              but RELATIONSHIPS too
```

> ⚠️ Trade-off: Graph generation adds cost and complexity.

### Agentic RAG

RAG that can **take actions** — not just answer questions, but execute tools, run code, or make decisions on its own.

---

## 9. RAG Architecture (In-Depth)

```
  ┌─────────────────────────────────────────────────────────────┐
  │                   COMPLETE RAG ARCHITECTURE                  │
  │                                                             │
  │  [Documents]                                                │
  │       │                                                     │
  │       ▼                                                     │
  │  [Embedding Model]  ──►  [Vector Database]                  │
  │                               │                             │
  │                    ┌──────────┤                             │
  │                    │          │                             │
  │             Sparse │    Dense │  ← Hybrid Retrieval         │
  │           (keyword)│ (vector) │                             │
  │                    └────┬─────┘                             │
  │                         ▼                                   │
  │                   [Re-Ranker]   ← Optional                  │
  │                         │                                   │
  │                         ▼                                   │
  │              [Retrieved Context]                             │
  │                    +                                        │
  │              [User Query/Prompt]                             │
  │                         │                                   │
  │                         ▼                                   │
  │                  [LLM / Generator]                           │
  │                         │                                   │
  │                         ▼                                   │
  │               [Formatted Response]  ──►  User               │
  └─────────────────────────────────────────────────────────────┘
```

### Retrieval Types

| Type       | Method                  | Example                |
| ---------- | ----------------------- | ---------------------- |
| **Sparse** | Keyword matching        | Elasticsearch, BM25    |
| **Dense**  | Vector similarity       | Embedding-based search |
| **Hybrid** | Combines Sparse + Dense | Best of both worlds    |

> 💡 **Hybrid retrieval** is currently the most popular approach because neither keyword search nor vector search alone is perfect.

---

## 10. Demo Walkthrough

### Tools & Stack Used

| Component           | Tool / Library                           | Purpose                         |
| ------------------- | ---------------------------------------- | ------------------------------- |
| Framework           | **LangChain**                            | Building the LLM app pipeline   |
| Expression Language | **LCEL** (LangChain Expression Language) | Chaining steps with pipe syntax |
| Embedding Model     | **all-MiniLM** (Hugging Face)            | Converting text to vectors      |
| LLM                 | **Gemma 2 (2B params)** via Ollama       | Generating answers              |
| Vector DB           | **Qdrant**                               | Storing & searching vectors     |
| Orchestration       | **LangGraph**                            | Managing multi-step workflows   |

### Demo Structure

```
  ┌────────────────────────────────────────────────┐
  │           DEMO FLOW                            │
  │                                                │
  │  1. Raw text data (fictional restaurant info)  │
  │         │                                      │
  │         ▼                                      │
  │  2. Chunking (size=500, overlap=50)            │
  │         │                                      │
  │         ▼                                      │
  │  3. Embed → Store in Qdrant                    │
  │         │                                      │
  │         ▼                                      │
  │  4a. NAIVE RAG  →  Direct query → LLM         │
  │  4b. ADVANCED RAG → Enhance query →            │
  │       Retrieve more → Refine if uncertain →    │
  │       Generate better answer                   │
  └────────────────────────────────────────────────┘
```

### Key Observations from Demo

- **Without RAG:** The LLM said _"I don't have access to real-time information"_ and gave generic advice.
- **With Naive RAG (K=2):** Answered simple questions correctly but struggled with complex, multi-part queries.
- **With Advanced RAG (K=7 + query enhancement + refinement loop):** Provided more detailed, accurate answers. Also broke down complex questions automatically.

### LangGraph State Machine Concept

```
  ┌──────────┐    ┌───────────┐    ┌────────────┐
  │ Enhance  │───►│ Retrieve  │───►│  Generate  │
  │  Query   │    │  Docs     │    │  Answer    │
  └──────────┘    └───────────┘    └─────┬──────┘
                                         │
                          Uncertain?     │  Confident?
                             ▼           │      ▼
                        ┌─────────┐      │    [END]
                        │ Refine  │      │
                        │  Query  │      │
                        └────┬────┘      │
                             │           │
                             ▼           │
                        (loop back)      │
                                         │
```

Each node holds its own **state** (current query, retrieved docs, answer, refinement flag). The graph decides which node to visit next based on the state.

---

## 11. How to Improve RAG

```
  ┌────────────────────────────────────────────────────┐
  │              IMPROVEMENT STRATEGIES                 │
  │                                                    │
  │  1. HYBRID SEARCH                                  │
  │     Combine keyword (BM25) + vector search         │
  │     → Reduces missed results                       │
  │                                                    │
  │  2. BETTER CHUNKING                                │
  │     Use semantic or hybrid chunking instead of     │
  │     fixed-size                                     │
  │                                                    │
  │  3. RE-RANKING                                     │
  │     After retrieval, use a model to reorder        │
  │     chunks by true relevance                       │
  │                                                    │
  │  4. QUERY DECOMPOSITION                            │
  │     Break complex queries into sub-queries,        │
  │     answer each, then fuse results                 │
  │     Example: "Compare React vs Android"            │
  │       → Query 1: "Tell me about React"             │
  │       → Query 2: "Tell me about Android"           │
  │       → Fuse & compare                             │
  │                                                    │
  │  5. CONVERSATION MEMORY                            │
  │     • Short-term: current session context          │
  │     • Long-term: user persona across sessions      │
  └────────────────────────────────────────────────────┘
```

---

## 12. Challenges in RAG

### 12a. Low-Quality Retrieval

- Use **hybrid retrieval** (sparse + dense)
- Add a **re-ranking layer**
- Continuously **monitor precision** and iterate

### 12b. Context Window Limitation

```
  Retrieved Chunks: [C1] [C2] [C3] [C4] [C5] [C6] [C7] …
                    |___________________________________|
                              Context Window
                           (has a MAX limit!)

  If exceeded → information gets lost or ignored

  Solutions:
    • Filter out less relevant chunks
    • Summarise chunks before passing to LLM
    • Use document compression
```

### 12c. Latency & Cost

- **Cache** frequently asked queries and their embeddings
- Use **smaller models** for intermediate steps (e.g., query rewriting) and larger ones only for final generation
- Choose **optimised vector stores** for your data source

### 12d. Security & Governance

- Prevent sensitive data from leaking to external models
- Enforce **access control** and **multi-tenancy** in your vector DB
- Maintain proper **audit logs**

### 12e. Evaluation (The Hardest Part)

- Prepare a **sample set** of documents + expected Q&A pairs
- Use **human-in-the-loop scoring** for quality checks
- Use tools like **TruLens** or **RAGAS** for automated factuality checks
- Collect **user feedback** (thumbs up/down) to improve over time

---

## 13. Key Takeaways

| #   | Takeaway                                               | Why It Matters                                                       |
| --- | ------------------------------------------------------ | -------------------------------------------------------------------- |
| 1   | **RAG is a system design pattern**                     | It's flexible — you can plug/swap components as needed               |
| 2   | **Models don't have to be huge**                       | RAG accuracy depends more on **retrieval quality** than model size   |
| 3   | **Open-source models are production-viable**           | With good retrieval + ingestion, smaller open models work well       |
| 4   | **Start simple, iterate often**                        | Begin with naive RAG, then add modules one by one                    |
| 5   | **LLM alone = guessing; LLM + RAG = grounded answers** | RAG is what makes LLMs actually useful for specific, real-world data |

---

## 14. References

- **CRAG (Corrective RAG)** — Adds a post-generation relevance check using a model before returning the answer. Prevents vague or hallucinated responses from reaching the user.
- **LightRAG** (by Meta) — A lighter alternative to Graph RAG that achieves comparable accuracy with less overhead.
- **GraphRAG** (by Microsoft) — Uses knowledge graphs to capture and retrieve entity relationships from documents.

---

_Notes compiled from the RAG introductory session. For deeper dives into any section (e.g., vector databases, LangGraph, or advanced retrieval), a separate session is recommended._
