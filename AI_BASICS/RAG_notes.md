# Retrieval-Augmented Generation (RAG)

## 1. What is RAG?

**RAG (Retrieval-Augmented Generation)** is a technique that gives LLMs access to external, up-to-date knowledge at the time of answering — instead of relying only on what they learned during training.

It solves three big problems with LLMs:

- They can't access information after their training cutoff date
- They can't access private or company-specific data
- They hallucinate when they don't truly "know" something

---

## 2. The Simple Analogy

Think of it as an exam:

- **Without RAG** → The LLM answers from memory only (closed-book). It might guess wrong.
- **With RAG** → The LLM gets to look up the answer in relevant pages first (open-book). Much more accurate.

---

## 3. How RAG Works

RAG works in three steps:

1. **Retrieve** — The system searches a database to find the most relevant pieces of information (called "chunks") related to your question.
2. **Augment** — Those relevant chunks are attached to your question as extra context before sending it to the LLM.
3. **Generate** — The LLM answers your question using both your question _and_ the retrieved context, so the answer is grounded in real data.

---

## 4. Key Components of RAG

### Embedding Model

Converts text into vectors (lists of numbers) so both your question and stored documents live in the same numerical "space" for comparison.

Popular models: OpenAI's `text-embedding-ada-002`, Sentence-BERT, Cohere Embed.

### Vector Database

A specialized database designed to store and quickly search embeddings by _similarity/meaning_ — not by exact keyword matching.

Popular options: **Pinecone**, **Weaviate**, **Qdrant**, **ChromaDB** (lightweight, good for local dev).

### Retriever

Finds the most relevant chunks from the vector database based on similarity to your query.

### LLM (Generator)

Takes the retrieved context and generates the final answer.

---

## 5. Embeddings Explained

An embedding is a way to turn text into a list of numbers (a vector) that captures its _meaning_.

Words or sentences that are similar in meaning will have vectors that are numerically close together.

```
"cat"  →  [0.2, 0.8, 0.1, ...]
"dog"  →  [0.3, 0.7, 0.2, ...]   ← close to "cat"
"car"  →  [0.9, 0.1, 0.5, ...]   ← far from "cat"
```

This means a query like "puppy" can still find results about "dog" — even though the exact word is different. This is called **semantic search**.

---

## 6. Vector Databases Explained

A vector database stores embeddings and lets you quickly find the most _similar_ ones to a given query.

| Normal Database (e.g. PostgreSQL)  | Vector Database (e.g. Pinecone)  |
| ---------------------------------- | -------------------------------- |
| Searches by exact match or filters | Searches by similarity / meaning |
| Stores structured rows / columns   | Stores vectors + metadata        |
| Great for lookups                  | Great for "find similar to this" |

### How a Vector DB Search Works

1. Your query is converted into a vector using an embedding model.
2. The database finds the _closest_ stored vectors (nearest neighbors).
3. It returns the original text chunks attached to those vectors.

---

## 7. The RAG Pipeline

### Phase 1: Indexing (done once or periodically)

```
Documents (PDFs, docs, etc.)
        ↓
Chunking (split into smaller pieces)
        ↓
Embedding Model (convert each chunk → vector)
        ↓
Vector Database (store vectors + original text)
```

### Phase 2: Query Time (every time a user asks something)

```
User Question
        ↓
Embedding Model (convert question → vector)
        ↓
Vector Database (find closest matching chunks)
        ↓
Combine question + retrieved chunks → send to LLM
        ↓
LLM generates answer grounded in the context
        ↓
Answer returned to user
```

---

## 8. RAG in Action — Code Example

A simple RAG setup using **ChromaDB** and **OpenAI**:

```python
import chromadb
from openai import OpenAI

client = OpenAI()
chroma = chromadb.Client()

# --- Phase 1: Indexing ---
collection = chroma.create_collection(name="company_docs")

# Pretend these are chunks from your documents
chunks = [
    "Employees get 20 days of paid leave per year.",
    "The office is open Monday to Friday, 9am to 6pm.",
    "Health insurance covers dental and vision."
]

# ChromaDB can auto-embed, or you can use your own model
collection.add(
    documents=chunks,
    ids=["chunk1", "chunk2", "chunk3"]
)

# --- Phase 2: Query Time ---
user_question = "How many leave days do I get?"

# Retrieve relevant chunks
results = collection.query(
    query_texts=[user_question],
    n_results=2  # get top 2 closest chunks
)

retrieved_context = "\n".join(results["documents"][0])

# Send to LLM with context
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": "Answer the user's question using only the provided context."
        },
        {
            "role": "user",
            "content": f"Context:\n{retrieved_context}\n\nQuestion: {user_question}"
        }
    ]
)

print(response.choices[0].message.content)
# Output: "You get 20 days of paid leave per year."
```

---

## 9. RAG vs Fine-Tuning

| RAG                               | Fine-Tuning                            |
| --------------------------------- | -------------------------------------- |
| Adds knowledge at query time      | Bakes knowledge into the model         |
| No retraining needed              | Requires retraining                    |
| Great for changing / private data | Better for teaching new style/behavior |
| Cheaper & faster to update        | More expensive & time-consuming        |

---

## 10. Common Pitfalls

- **Bad chunking** — Splitting documents poorly (e.g., cutting a sentence in half) makes the retrieved context useless.
- **Irrelevant retrieval** — If the vector DB returns unhelpful chunks, the LLM will still try to use them and may hallucinate.
- **Ignoring metadata** — Filtering by source, date, or category alongside vector search makes retrieval much more accurate.

---

## 11. Real-World Use Cases

### Basic

- Company internal chatbots
- FAQ systems
- Document search engines

### Advanced

- Customer support with live knowledge bases
- Legal or medical research assistants
- AI Agents that combine RAG with tool use

---

## 12. Summary

- RAG gives LLMs access to external knowledge without retraining
- It works by retrieving relevant chunks, augmenting the prompt, then generating an answer
- Embeddings and vector databases are the backbone of the retrieval step
- RAG is cheaper and more flexible than fine-tuning for most knowledge tasks

---

## 13. What to Learn Next

- **Chunking Strategies** — How to split documents smartly
- **Hybrid Search** — Combining vector search with keyword search
- **Metadata Filtering** — Narrowing retrieval with tags and filters
- **AI Agents** — LLMs that decide which tools to use and act autonomously
