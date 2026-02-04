# RAG Types: Complete Beginner's Guide

## Table of Contents
1. [What is RAG?](#what-is-rag)
2. [Basic Concepts Explained](#basic-concepts-explained)
3. [RAG Types in Detail](#rag-types-in-detail)
4. [Choosing the Right Type](#choosing-the-right-type)

---

## What is RAG?

### The Problem RAG Solves

Imagine you're talking to ChatGPT and ask: "What did my company announce in yesterday's board meeting?"

ChatGPT would say: "I don't know - I wasn't trained on your company's private data."

**RAG (Retrieval-Augmented Generation) solves this problem.**

### How RAG Works (Simple Explanation)

Think of RAG like an open-book exam:

1. **You ask a question** → "What are the side effects of aspirin?"
2. **The system looks through relevant books/documents** → Finds medical articles about aspirin
3. **It reads the relevant pages** → Extracts information about side effects
4. **It answers your question** using what it just read

**Without RAG**: AI can only answer from memory (what it learned during training)
**With RAG**: AI can answer by looking up current information in your documents

---

## Basic Concepts Explained

Before we dive into RAG types, let's understand the building blocks:

### 1. Embeddings (Vector Representations)

**What is it?**
Converting text into numbers that capture meaning.

**Simple Analogy:**
Imagine you want to organize books in a library. Instead of just alphabetically, you create a "meaning score":
- Books about "dogs" and "cats" get similar scores (both about pets)
- Books about "cars" get different scores

**Technical Example:**
```
Text: "The cat sat on the mat"
Embedding: [0.23, -0.45, 0.67, 0.12, -0.89, ...]
           (a list of numbers)

Text: "The dog sat on the rug"
Embedding: [0.25, -0.43, 0.65, 0.14, -0.87, ...]
           (similar numbers because similar meaning!)
```

**Why Important for RAG?**
We convert both documents and questions into embeddings, then find documents with similar embeddings to the question.

---

### 2. Vector Database

**What is it?**
A special database that stores embeddings and can quickly find similar ones.

**Simple Analogy:**
Like a librarian who can instantly find all books "similar" to the one you're holding.

**How it Works:**
```
Step 1: Store documents as embeddings
Document 1: "Dogs are loyal pets" → [0.8, 0.2, 0.5]
Document 2: "Cats are independent" → [0.7, 0.3, 0.4]
Document 3: "Cars need fuel" → [-0.2, 0.9, -0.5]

Step 2: When you ask "Tell me about pets"
Query embedding: [0.75, 0.25, 0.45]

Step 3: Find most similar
Document 1: Very similar! ✓
Document 2: Very similar! ✓
Document 3: Not similar ✗
```

**Popular Vector Databases:**
- Pinecone
- Weaviate
- ChromaDB
- FAISS
- Qadrant

---

### 3. Chunking

**What is it?**
Breaking large documents into smaller pieces.

**Why Needed?**
- AI models have limited context windows (can't read entire books at once)
- Smaller chunks = more precise matching

**Example:**
```
Original Document (500 pages):
"Chapter 1: Introduction to Medicine
 Medicine has evolved over centuries...
 
 Chapter 2: Common Diseases
 Diabetes is a metabolic disorder...
 
 Chapter 3: Treatment Methods
 Antibiotics work by..."

Chunked Version:
Chunk 1: "Chapter 1: Introduction to Medicine. Medicine has evolved..."
Chunk 2: "Diabetes is a metabolic disorder affecting..."
Chunk 3: "Antibiotics work by killing bacteria..."
```

**Good Chunking Strategy:**
- Size: 200-500 words per chunk
- Overlap: 10-20% overlap between chunks (so context isn't lost)
- Respect boundaries: Don't split sentences or paragraphs awkwardly

---

### 4. Re-ranking

**What is it?**
Taking initial search results and reordering them by actual relevance.

**Simple Analogy:**
You search Google for "apple" and get:
1. Apple fruit recipes
2. Apple company stock
3. Apple iPhone reviews

A re-ranker looks at your full question: "How to grow apples in my garden?" and reorders:
1. Apple fruit recipes ← Most relevant!
2. Apple gardening guide
3. Apple company stock ← Not relevant

**How it Works:**
```
Initial Search (Vector Database):
Query: "Best treatment for headaches"

Top 5 Results:
1. "Headache causes and symptoms" (similarity: 0.82)
2. "Migraine treatment options" (similarity: 0.80)
3. "Headache prevention tips" (similarity: 0.79)
4. "Aspirin usage guide" (similarity: 0.77)
5. "Brain anatomy" (similarity: 0.75)

Re-ranking Step:
A smarter model reads the full query + each document and scores:

1. "Migraine treatment options" (relevance: 0.95) ← Moved up!
2. "Aspirin usage guide" (relevance: 0.88) ← Moved up!
3. "Headache prevention tips" (relevance: 0.82)
4. "Headache causes and symptoms" (relevance: 0.75)
5. "Brain anatomy" (relevance: 0.30) ← Pushed down
```

**Re-ranking Models:**
- Cross-encoders (very accurate but slower)
- Cohere Re-rank API
- LLM-based re-ranking

---

### 5. Hybrid Search

**What is it?**
Combining two types of search for better results:
1. **Semantic Search** (meaning-based, using embeddings)
2. **Keyword Search** (exact word matching, like old-school search)

**Why Both?**
Each has strengths:
- Semantic: Understands "car" ≈ "automobile"
- Keyword: Finds exact product codes, names, technical terms

**Example:**
```
Query: "What's the warranty on MacBook Pro M2 model number MNW83LL/A?"

Semantic Search finds:
- "Apple laptop warranty information"
- "MacBook Pro support policies"
- "M2 chip specifications"

Keyword Search finds:
- Documents containing exact text "MNW83LL/A"
- Documents with "MacBook Pro M2"

Combined: You get both conceptual matches AND exact technical matches!
```

**How Results are Combined (Fusion):**
```
Semantic Results:         Keyword Results:
1. Doc A (score 0.9)     1. Doc C (score 0.95)
2. Doc B (score 0.8)     2. Doc A (score 0.85)
3. Doc C (score 0.7)     3. Doc D (score 0.60)

Fusion (combining scores):
1. Doc A (combined: 0.875) ← Appeared in both!
2. Doc C (combined: 0.825) ← Appeared in both!
3. Doc B (combined: 0.800)
4. Doc D (combined: 0.600)
```

---

### 6. Query Transformation

**What is it?**
Rewriting or expanding the user's question to get better search results.

**Types of Transformations:**

#### A. Query Rewriting
Making the question clearer:
```
Original: "iphone battery bad"
Rewritten: "iPhone battery draining quickly troubleshooting"
```

#### B. Query Expansion
Adding related terms:
```
Original: "python loops"
Expanded: "python loops, for loop, while loop, iteration, iterate"
```

#### C. Query Decomposition
Breaking complex questions into simpler ones:
```
Original: "Compare iPhone 15 and Samsung S24 camera quality and battery life"

Decomposed:
1. "iPhone 15 camera specifications"
2. "Samsung S24 camera specifications"
3. "iPhone 15 battery life"
4. "Samsung S24 battery life"
```

#### D. HyDE (Hypothetical Document Embeddings)
Generate a hypothetical perfect answer, then search for documents similar to it:
```
Query: "How do I fix error 404?"

HyDE generates hypothetical answer:
"Error 404 occurs when a page is not found. To fix it, check the URL, 
verify the file exists, check server configuration..."

Then searches for documents similar to this hypothetical answer!
```

---

### 7. Fusion Strategies

**What is it?**
Methods to combine results from multiple searches.

**Common Strategies:**

#### A. Reciprocal Rank Fusion (RRF)
```
Source 1 ranks:          Source 2 ranks:
1. Doc A                 1. Doc C
2. Doc B                 2. Doc A
3. Doc C                 3. Doc D

RRF Score Calculation:
Doc A: 1/(1+1) + 1/(1+2) = 1/2 + 1/3 = 0.833
Doc B: 1/(1+2) + 0 = 0.333
Doc C: 1/(1+3) + 1/(1+1) = 0.25 + 0.5 = 0.750
Doc D: 0 + 1/(1+3) = 0.250

Final Ranking:
1. Doc A (0.833)
2. Doc C (0.750)
3. Doc B (0.333)
4. Doc D (0.250)
```

#### B. Weighted Fusion
Give more importance to certain sources:
```
Semantic results (weight: 0.7) + Keyword results (weight: 0.3)
```

---

### 8. Context Compression

**What is it?**
Removing unnecessary information before sending to the AI.

**Why Needed?**
- AI models charge by token
- Shorter context = faster responses
- Focus on relevant parts only

**Example:**
```
Retrieved Document (500 words):
"The history of aspirin dates back to ancient times when willow bark 
was used for pain relief. In 1897, Felix Hoffmann synthesized aspirin 
at Bayer. Today, aspirin is one of the most widely used medications.

Side effects include:
- Stomach upset
- Nausea  
- Bleeding risk
- Allergic reactions in some people

Dosage typically ranges from 75mg to 325mg depending on use case..."

After Compression (keeping only relevant parts for query "side effects"):
"Side effects include: stomach upset, nausea, bleeding risk, 
allergic reactions in some people."
```

---

### 9. Self-Reflection / Self-Critique

**What is it?**
The AI evaluating its own answer and deciding if it needs more information.

**Example Flow:**
```
Question: "Is it safe to take aspirin with ibuprofen?"

First retrieval → Gets: "Aspirin is a pain reliever"

AI reflects: "This doesn't answer the interaction question. 
I need more specific information about drug interactions."

Second retrieval → Gets: "NSAIDs like ibuprofen and aspirin 
increase bleeding risk when combined"

AI reflects: "Now I have the answer!"

Final answer: "Taking aspirin with ibuprofen is generally not 
recommended as both are NSAIDs and increase bleeding risk..."
```

---

### 10. Iterative Retrieval

**What is it?**
Retrieving information multiple times, using each result to inform the next search.

**Example:**
```
Question: "What's the impact of climate change on polar bears?"

Round 1: Search "climate change polar bears"
Result: "Arctic ice is melting"

Round 2: Search "Arctic ice melting effects wildlife" (based on Round 1)
Result: "Ice loss reduces hunting grounds for seals"

Round 3: Search "polar bear seal hunting behavior" (based on Round 2)
Result: "Polar bears primarily hunt seals on sea ice"

Final Answer combines all rounds:
"Climate change causes Arctic ice to melt, reducing hunting grounds 
for seals, which are polar bears' primary food source hunted on sea ice..."
```

---

## RAG Types in Detail

Now that we understand the basics, let's explore each RAG type:

---

## 1. Naive RAG

### What It Is
The simplest possible RAG system. Just the bare minimum to work.

### Architecture
```
User Question
    ↓
Convert to Embedding
    ↓
Search Vector Database
    ↓
Get Top 3-5 Most Similar Chunks
    ↓
Put Chunks + Question into AI
    ↓
Get Answer
```

### Step-by-Step Example

**Scenario:** You have a company knowledge base and ask: "What's our vacation policy?"

```
Step 1: Index Phase (done once when setting up)
─────────────────────────────────────────────
Document: "Employee Handbook"

Split into chunks:
Chunk 1: "Vacation Policy: Full-time employees receive 15 days 
         of paid vacation per year..."
Chunk 2: "Sick Leave: Employees get 10 days of sick leave..."
Chunk 3: "Remote Work: Employees can work remotely 2 days per week..."

Convert each chunk to embedding and store:
Chunk 1 → [0.23, -0.45, 0.67, ...] → Vector DB
Chunk 2 → [0.11, -0.33, 0.52, ...] → Vector DB
Chunk 3 → [0.44, -0.12, 0.23, ...] → Vector DB

Step 2: Query Phase (when user asks a question)
─────────────────────────────────────────────
User asks: "What's our vacation policy?"

Convert question to embedding:
"What's our vacation policy?" → [0.24, -0.44, 0.68, ...]

Search vector database for most similar:
Similarity to Chunk 1: 0.95 (very similar!) ✓
Similarity to Chunk 2: 0.62
Similarity to Chunk 3: 0.45

Retrieve top match (Chunk 1)

Step 3: Generate Answer
─────────────────────────────────────────────
Send to AI:
Context: "Vacation Policy: Full-time employees receive 15 days 
         of paid vacation per year..."
Question: "What's our vacation policy?"

AI responds: "According to the employee handbook, full-time 
             employees receive 15 days of paid vacation per year."
```

### Pros & Cons

**Pros:**
- ✅ Very simple to implement (can build in a weekend)
- ✅ Fast responses
- ✅ Low cost
- ✅ Good for prototyping

**Cons:**
- ❌ Often retrieves irrelevant chunks
- ❌ Misses important context that's in different chunks
- ❌ No handling of complex questions
- ❌ Can't do multi-hop reasoning
- ❌ Poor handling of ambiguous queries

### When to Use
- Quick prototypes
- Simple FAQ systems
- Testing if RAG works for your use case
- Very small document sets (< 100 documents)

---

## 2. Standard RAG

### What It Is
A production-ready RAG system with improvements in every stage: better chunking, hybrid search, re-ranking, and post-processing.

### Architecture
```
User Question
    ↓
Pre-Processing (clean, normalize)
    ↓
    ├─→ Dense Search (embeddings)
    └─→ Sparse Search (keywords)
    ↓
Hybrid Fusion (combine results)
    ↓
Re-ranking (order by true relevance)
    ↓
Context Compression (remove fluff)
    ↓
Send to AI with optimized context
    ↓
Generate Answer
```

### Step-by-Step Example

**Scenario:** Medical information system. Question: "What are treatment options for type 2 diabetes?"

```
Step 1: Pre-Processing
─────────────────────────────────────────────
Raw Query: "treatment options type 2 diabetes???"

Clean:
- Remove extra punctuation
- Normalize: "treatment options for type 2 diabetes"
- Expand: Add synonyms → "treatment, therapy, management, 
  type 2 diabetes, T2D, diabetes mellitus type 2"

Step 2: Hybrid Search
─────────────────────────────────────────────
A. Dense Search (Semantic/Embeddings):
   Query embedding: [0.45, -0.23, 0.78, ...]
   
   Top 5 results:
   1. "Managing Type 2 Diabetes Through Diet" (score: 0.89)
   2. "Metformin: First-Line Treatment" (score: 0.86)
   3. "Insulin Therapy for Diabetes" (score: 0.84)
   4. "Diabetes Complications Prevention" (score: 0.81)
   5. "Exercise and Blood Sugar Control" (score: 0.79)

B. Keyword Search (BM25):
   Searching for exact terms: "type 2 diabetes" + "treatment"
   
   Top 5 results:
   1. "Type 2 Diabetes Treatment Guidelines 2024" (score: 0.92)
   2. "Metformin: First-Line Treatment" (score: 0.88)
   3. "GLP-1 Agonists for Type 2 Diabetes" (score: 0.85)
   4. "SGLT2 Inhibitors in Diabetes Management" (score: 0.82)
   5. "Insulin Therapy for Diabetes" (score: 0.80)

Step 3: Fusion (Combine Results)
─────────────────────────────────────────────
Using Reciprocal Rank Fusion:

Unique documents and their combined scores:
1. "Type 2 Diabetes Treatment Guidelines 2024" (0.91)
2. "Metformin: First-Line Treatment" (0.90) ← In both!
3. "GLP-1 Agonists for Type 2 Diabetes" (0.84)
4. "Managing Type 2 Diabetes Through Diet" (0.83)
5. "SGLT2 Inhibitors in Diabetes Management" (0.81)
6. "Insulin Therapy for Diabetes" (0.80) ← In both!
7. "Diabetes Complications Prevention" (0.76)
8. "Exercise and Blood Sugar Control" (0.74)

Step 4: Re-ranking
─────────────────────────────────────────────
Use a cross-encoder model to read the full query + each document

Cross-encoder scores (0-1, higher = more relevant):
1. "Type 2 Diabetes Treatment Guidelines 2024" (0.96)
2. "Metformin: First-Line Treatment" (0.94)
3. "GLP-1 Agonists for Type 2 Diabetes" (0.91)
4. "SGLT2 Inhibitors in Diabetes Management" (0.89)
5. "Insulin Therapy for Diabetes" (0.87)
6. "Managing Type 2 Diabetes Through Diet" (0.72) ← Pushed down
7. "Exercise and Blood Sugar Control" (0.68) ← Pushed down
8. "Diabetes Complications Prevention" (0.51) ← Pushed down

Keep top 5 for generation

Step 5: Context Compression
─────────────────────────────────────────────
Original Document 1 (1000 words):
"Type 2 Diabetes Treatment Guidelines 2024

Introduction:
Type 2 diabetes has become increasingly prevalent worldwide...
[Historical context about diabetes - 300 words]

Treatment Options:
1. Lifestyle Modifications
   - Diet: Low carbohydrate, Mediterranean diet
   - Exercise: 150 minutes per week
   
2. First-Line Medication
   - Metformin 500-2000mg daily
   
3. Second-Line Options
   - GLP-1 agonists (semaglutide, liraglutide)
   - SGLT2 inhibitors (empagliflozin)
   - DPP-4 inhibitors
   
[More details on each - 500 words]

Monitoring and Follow-up:
[Another 200 words]"

After Compression (keeping only treatment-relevant parts):
"Treatment Options for Type 2 Diabetes:
1. Lifestyle: Low-carb diet, Mediterranean diet, 150 min exercise/week
2. First-line: Metformin 500-2000mg daily
3. Second-line: GLP-1 agonists (semaglutide), SGLT2 inhibitors 
   (empagliflozin), DPP-4 inhibitors"

Step 6: Generate Answer
─────────────────────────────────────────────
Optimized context (compressed from 5 docs) + Question → AI

AI generates comprehensive answer:
"Treatment options for type 2 diabetes include:

1. Lifestyle Modifications: Start with diet (low-carb or Mediterranean) 
   and exercise (150 minutes weekly)

2. First-Line Medication: Metformin (500-2000mg daily) is the 
   recommended initial medication

3. Second-Line Medications if needed:
   - GLP-1 agonists (semaglutide, liraglutide)
   - SGLT2 inhibitors (empagliflozin)
   - DPP-4 inhibitors

Treatment should be personalized based on individual needs..."
```

### Pros & Cons

**Pros:**
- ✅ Much better accuracy than Naive RAG
- ✅ Handles diverse question types
- ✅ Production-ready
- ✅ Good balance of cost and performance
- ✅ Catches both semantic and exact matches

**Cons:**
- ❌ More complex to set up
- ❌ Higher latency (multiple processing steps)
- ❌ Requires tuning for optimal performance
- ❌ Still struggles with very complex multi-step questions

### When to Use
- Production applications
- Customer support systems
- Documentation search
- Knowledge bases
- Most real-world RAG applications

---

## 3. Advanced RAG

### What It Is
Sophisticated RAG with query transformation, iterative retrieval, and self-correction capabilities.

### Architecture
```
User Question
    ↓
Query Analysis & Understanding
    ↓
    ├─→ Generate Multiple Query Variations
    ├─→ Decompose into Sub-Questions
    └─→ Generate Hypothetical Answer (HyDE)
    ↓
Parallel Retrieval (all variations)
    ↓
Initial Answer Generation
    ↓
Self-Reflection: "Do I have enough info?"
    ↓
    ├─→ Yes → Final Answer
    └─→ No → Additional Retrieval → Loop back
```

### Step-by-Step Example

**Scenario:** Research assistant. Question: "Compare the environmental impact of electric cars vs hydrogen fuel cell cars in 2024"

```
Step 1: Query Analysis
─────────────────────────────────────────────
AI analyzes the question:
- Type: Comparative analysis
- Complexity: High (requires multiple data points)
- Entities: Electric cars, Hydrogen fuel cell cars, Environmental impact
- Time constraint: 2024 (needs recent data)

Step 2: Query Decomposition
─────────────────────────────────────────────
Break into sub-questions:
1. "What is the environmental impact of electric cars in 2024?"
2. "What is the environmental impact of hydrogen fuel cell cars in 2024?"
3. "What are the carbon emissions from electric car production?"
4. "What are the carbon emissions from hydrogen fuel cell production?"
5. "How is electricity generated for EVs?"
6. "How is hydrogen produced for fuel cells?"

Step 3: Multi-Query Generation
─────────────────────────────────────────────
Generate query variations for better coverage:

For Sub-Q1:
- "electric vehicle environmental footprint 2024"
- "EV carbon emissions lifecycle analysis"
- "battery production environmental impact"
- "electric car sustainability metrics"

For Sub-Q2:
- "hydrogen fuel cell vehicle emissions 2024"
- "FCEV environmental assessment"
- "hydrogen production methods environmental cost"

Step 4: HyDE (Hypothetical Document Embeddings)
─────────────────────────────────────────────
Generate a hypothetical "perfect answer":

"Electric vehicles in 2024 have a total lifecycle carbon footprint 
of approximately X tons CO2, with Y% from battery production and Z% 
from electricity generation. Hydrogen fuel cell vehicles have a 
footprint of A tons CO2, with B% from hydrogen production via 
steam methane reforming. When powered by renewable electricity, 
EVs produce C% less emissions, while green hydrogen FCEVs produce D%..."

Convert this hypothetical answer to embedding and search for similar docs

Step 5: Parallel Retrieval (Round 1)
─────────────────────────────────────────────
Execute all queries simultaneously:

Sub-Q1 results:
- Doc A: "2024 EV Lifecycle Analysis" (relevance: 0.94)
- Doc B: "Battery Production CO2 Study" (relevance: 0.89)

Sub-Q2 results:
- Doc C: "Hydrogen Fuel Cell Assessment 2024" (relevance: 0.91)
- Doc D: "Hydrogen Production Methods" (relevance: 0.87)

HyDE results:
- Doc E: "Comparative Study: EVs vs FCEVs" (relevance: 0.96)
- Doc F: "Green Energy Vehicles Impact" (relevance: 0.88)

Total: 15 unique documents retrieved

Step 6: Initial Answer Generation
─────────────────────────────────────────────
AI generates draft answer using retrieved docs:

"Electric vehicles in 2024 have shown significant environmental 
benefits, with lifecycle emissions of approximately 50 tons CO2 
equivalent. Battery production accounts for 30% of this impact..."

Step 7: Self-Reflection
─────────────────────────────────────────────
AI evaluates its own answer:

Checklist:
✓ Do I have EV emissions data? YES
✓ Do I have FCEV emissions data? YES  
✗ Do I have charging infrastructure impact? NO ← Gap identified!
✗ Do I have hydrogen infrastructure impact? NO ← Gap identified!
✓ Do I have production process details? YES
✗ Do I have regional differences? NO ← Gap identified!

Decision: Need more information

Step 8: Adaptive Re-Retrieval (Round 2)
─────────────────────────────────────────────
Based on gaps, generate new queries:
- "electric vehicle charging infrastructure environmental impact"
- "hydrogen refueling station construction emissions"
- "EV vs FCEV regional differences Europe Asia USA"

Retrieve additional documents:
- Doc G: "EV Charging Infrastructure Study" (relevance: 0.89)
- Doc H: "Hydrogen Infrastructure Requirements" (relevance: 0.86)
- Doc I: "Regional Analysis Clean Vehicles" (relevance: 0.92)

Step 9: Final Answer Generation
─────────────────────────────────────────────
Combine all rounds of retrieval (18 total docs):

"Comprehensive comparison of electric cars vs hydrogen fuel cell cars:

Environmental Impact - Electric Vehicles (2024):
- Lifecycle emissions: ~50 tons CO2eq
- Battery production: 15 tons CO2eq (30% of total)
- Electricity use (average grid): 35 tons CO2eq
- Infrastructure: 0.5 tons CO2eq per charging station
- Regional variation: 30-70 tons depending on grid mix

Environmental Impact - Hydrogen Fuel Cell Vehicles (2024):
- Lifecycle emissions: ~55-80 tons CO2eq (depending on H2 source)
- Fuel cell production: 10 tons CO2eq
- Hydrogen production:
  * Grey hydrogen (natural gas): 60 tons CO2eq
  * Green hydrogen (renewable): 5 tons CO2eq
- Infrastructure: 2 tons CO2eq per refueling station

Key Findings:
1. With average electricity grids, EVs emit 10-30% less than FCEVs
2. With renewable energy, both can achieve <20 tons CO2eq
3. Infrastructure impact is minimal for both (<2% of total)
4. Regional grid composition is the biggest variable for EVs
5. Hydrogen production method is critical for FCEVs

Conclusion: In 2024, EVs generally have lower environmental impact, 
especially in regions with cleaner grids. However, FCEVs with green 
hydrogen can achieve similar or better results..."
```

### Pros & Cons

**Pros:**
- ✅ Handles complex, multi-faceted questions
- ✅ Multi-hop reasoning capability
- ✅ Self-correcting (finds and fills gaps)
- ✅ Very high accuracy
- ✅ Can handle ambiguous queries

**Cons:**
- ❌ High latency (multiple retrieval rounds)
- ❌ Expensive (many LLM calls for decomposition, HyDE, reflection)
- ❌ Complex to implement and debug
- ❌ Requires careful prompt engineering
- ❌ Can over-retrieve (too much information)

### When to Use
- Research and analysis tasks
- Complex comparative questions
- Academic or scientific queries
- Legal research
- When accuracy is more important than speed

---

## 4. Modular RAG

### What It Is
A flexible, component-based RAG architecture where you can swap different modules (retrievers, re-rankers, generators) based on query type or requirements.

### Architecture
```
User Question
    ↓
Query Router (decides which modules to use)
    ↓
┌─────────────────┬─────────────────┬─────────────────┐
│   Route A       │    Route B      │    Route C      │
│  (Factual)      │   (Code)        │  (Creative)     │
├─────────────────┼─────────────────┼─────────────────┤
│ - Vector DB     │ - Code Search   │ - Web Search    │
│ - BM25          │ - GitHub        │ - Vector DB     │
│ - SQL DB        │                 │                 │
├─────────────────┼─────────────────┼─────────────────┤
│ - Cross-Encoder │ - Code BERT     │ - Simple Rank   │
│   Re-ranker     │   Re-ranker     │                 │
├─────────────────┼─────────────────┼─────────────────┤
│ - GPT-4         │ - Claude (Code) │ - GPT-4 Turbo   │
└─────────────────┴─────────────────┴─────────────────┘
```

### Key Concept: Mix & Match

Instead of one fixed pipeline, you have a toolbox:

**Retriever Modules:**
- Vector database (semantic search)
- BM25 (keyword search)
- SQL database (structured data)
- Web search API
- Graph database
- Elasticsearch
- Custom APIs

**Re-ranker Modules:**
- Cross-encoder models
- Cohere Re-rank
- LLM-based re-ranking
- Custom scoring functions

**Generator Modules:**
- GPT-4 (general purpose)
- Claude (analysis)
- GPT-3.5 (fast, cheap)
- Fine-tuned models (domain-specific)
- Local models (privacy)

### Step-by-Step Example

**Scenario:** Enterprise knowledge system handling different query types

```
Example 1: Factual Query
─────────────────────────────────────────────
Query: "What's our company's Q3 revenue?"

Step 1: Query Router Analysis
Type: Factual, structured data
Complexity: Low
Data source: Likely in databases

Step 2: Module Selection
Retrievers: 
- ✓ SQL Database (financial data)
- ✓ Vector DB (search financial reports)
- ✗ Web Search (not needed)
- ✗ Code Search (not relevant)

Re-ranker:
- ✓ Simple scoring (fast, sufficient for simple query)
- ✗ Cross-encoder (overkill)

Generator:
- ✓ GPT-3.5 Turbo (fast, cheap, good enough)
- ✗ GPT-4 (expensive, unnecessary)

Step 3: Execution
SQL query: SELECT revenue FROM financials WHERE quarter='Q3-2024'
Result: $45.2M

Vector DB: Search "Q3 revenue 2024"
Result: Financial report PDF

Step 4: Generate Answer
"The company's Q3 2024 revenue was $45.2 million, representing 
a 12% increase from Q2."

Cost: $0.002, Latency: 1.2s

─────────────────────────────────────────────

Example 2: Code Documentation Query
─────────────────────────────────────────────
Query: "How do I use the authenticate() function in our Python API?"

Step 1: Query Router Analysis
Type: Code documentation
Complexity: Medium
Data source: Code repositories, documentation

Step 2: Module Selection
Retrievers:
- ✗ SQL Database (not relevant)
- ✓ Code Search (GitHub, internal repos)
- ✓ Vector DB (documentation)
- ✗ Web Search (internal code only)

Re-ranker:
- ✓ CodeBERT (specialized for code)
- ✗ General cross-encoder

Generator:
- ✓ Claude Opus (excellent at code explanation)
- ✗ GPT-3.5 (less good with code)

Step 3: Execution
Code Search: Find authenticate() function definition
Vector DB: Find API documentation mentioning authenticate()

Step 4: Generate Answer with code examples
"The authenticate() function is used to..."
[Includes code examples, parameters, return values]

Cost: $0.015, Latency: 2.8s

─────────────────────────────────────────────

Example 3: Research Query
─────────────────────────────────────────────
Query: "What are the latest developments in quantum computing and 
how do they compare to our competitors' approaches?"

Step 1: Query Router Analysis
Type: Research, comparative analysis
Complexity: High
Data source: Web + internal documents

Step 2: Module Selection
Retrievers:
- ✓ Web Search (latest developments)
- ✓ Vector DB (internal research docs)
- ✓ News API (recent news)
- ✗ SQL Database (not applicable)

Re-ranker:
- ✓ Cross-encoder (need high accuracy)
- ✗ Simple scoring (insufficient)

Generator:
- ✓ GPT-4 (need advanced reasoning)
- ✗ GPT-3.5 (too simple for this)

Step 3: Execution
Web Search: "quantum computing developments 2024"
News API: Recent quantum computing news
Vector DB: Internal quantum research documents

Cross-encoder re-ranks all 30 results → Top 10

Step 4: Generate Answer
Comprehensive analysis comparing external developments 
with internal approaches

Cost: $0.25, Latency: 8.5s
```

### Configuration Example

Here's how you might configure this in code:

```python
# Define routing rules
routing_config = {
    "factual_queries": {
        "retrievers": [
            {"type": "sql", "weight": 0.6},
            {"type": "vector_db", "weight": 0.4}
        ],
        "reranker": "simple_score",
        "generator": "gpt-3.5-turbo",
        "max_cost": 0.01
    },
    
    "code_queries": {
        "retrievers": [
            {"type": "code_search", "weight": 0.7},
            {"type": "vector_db", "weight": 0.3}
        ],
        "reranker": "codebert",
        "generator": "claude-opus",
        "max_cost": 0.05
    },
    
    "research_queries": {
        "retrievers": [
            {"type": "web_search", "weight": 0.4},
            {"type": "vector_db", "weight": 0.3},
            {"type": "news_api", "weight": 0.3}
        ],
        "reranker": "cross_encoder",
        "generator": "gpt-4",
        "max_cost": 0.50,
        "enable_iteration": True
    },
    
    "simple_faq": {
        "retrievers": [
            {"type": "vector_db", "weight": 1.0}
        ],
        "reranker": None,
        "generator": "gpt-3.5-turbo",
        "max_cost": 0.005,
        "cache_results": True
    }
}

# Query router uses classifier or rules to pick config
def route_query(query):
    if is_factual_query(query):
        return routing_config["factual_queries"]
    elif is_code_query(query):
        return routing_config["code_queries"]
    elif is_research_query(query):
        return routing_config["research_queries"]
    else:
        return routing_config["simple_faq"]
```

### Pros & Cons

**Pros:**
- ✅ Highly customizable for different use cases
- ✅ Optimized cost/performance per query type
- ✅ Easy to upgrade individual components
- ✅ Can A/B test different configurations
- ✅ Flexible and adaptable
- ✅ Can balance speed, cost, and accuracy

**Cons:**
- ❌ Requires significant upfront design
- ❌ Complex to maintain (many moving parts)
- ❌ Need good query classification
- ❌ More integration work
- ❌ Monitoring is more complex
- ❌ Debugging can be challenging

### When to Use
- Enterprise systems with diverse query types
- When you need to optimize for different metrics (cost, speed, accuracy)
- Multi-domain applications (e.g., customer support + technical docs + sales)
- When you want to easily experiment with different approaches
- Systems that need to scale to different use cases

---

## 5. Graph RAG

### What It Is
Instead of storing documents as flat chunks, Graph RAG extracts entities (people, places, things, concepts) and their relationships, storing them in a knowledge graph. Retrieval happens by traversing these relationships.

### Core Concept: Knowledge Graphs

**Traditional (Chunk-based):**
```
Chunk 1: "Apple acquired Beats in 2014 for $3 billion"
Chunk 2: "Tim Cook is the CEO of Apple"
Chunk 3: "Beats was founded by Dr. Dre and Jimmy Iovine"
```

**Graph Representation:**
```
     [Tim Cook] ──CEO_of──> [Apple] ──acquired──> [Beats]
                                                      ↑
                                                      |
                                            founded_by
                                                      |
                                         [Dr. Dre] [Jimmy Iovine]
                                                  ↓
                                            [acquisition_year: 2014]
                                            [price: $3B]
```

### Why Graphs Are Powerful

**Question:** "Who leads the company that acquired the company founded by Dr. Dre?"

**Chunk-based RAG:** Might retrieve:
- Chunk about Dr. Dre founding Beats ✓
- Chunk about Tim Cook at Apple ✓
- Chunk about Apple's other acquisitions ✗ (not helpful)
→ Needs AI to connect the dots

**Graph RAG:** Can traverse:
```
Dr. Dre → founded → Beats → acquired_by → Apple → CEO → Tim Cook
```
→ Direct path to answer!

### Architecture
```
Documents
    ↓
Entity & Relationship Extraction
    ↓
Knowledge Graph Construction
    ↓
    [Nodes: Entities]
    [Edges: Relationships]
    ↓
User Question
    ↓
Identify Relevant Entities
    ↓
Graph Traversal (find paths)
    ↓
Retrieve Connected Context
    ↓
Generate Answer
```

### Step-by-Step Example

**Scenario:** Medical knowledge base. Question: "What medications should I avoid if I'm taking warfarin for atrial fibrillation?"

```
Step 1: Build Knowledge Graph (done once)
─────────────────────────────────────────────
From medical documents, extract entities and relationships:

Documents:
Doc 1: "Warfarin is an anticoagulant used to treat atrial fibrillation 
        and prevent blood clots."
Doc 2: "Warfarin interacts with aspirin, increasing bleeding risk."
Doc 3: "NSAIDs like ibuprofen should be used cautiously with 
        anticoagulants."
Doc 4: "Atrial fibrillation increases stroke risk."

Extracted Graph:
┌──────────────────────────────────────────────────────┐
│  [Warfarin]                                          │
│      ├── type_of → [Anticoagulant]                  │
│      ├── treats → [Atrial Fibrillation]             │
│      ├── prevents → [Blood Clots]                   │
│      ├── interacts_with → [Aspirin]                 │
│      │       └── effect → [Increased Bleeding Risk] │
│      └── interacts_with → [NSAIDs]                  │
│              ├── includes → [Ibuprofen]             │
│              └── warning → [Use Cautiously]         │
│                                                      │
│  [Atrial Fibrillation]                              │
│      ├── treated_by → [Warfarin]                    │
│      └── increases_risk_of → [Stroke]               │
│                                                      │
│  [Aspirin]                                           │
│      ├── type_of → [Antiplatelet]                   │
│      └── interacts_with → [Warfarin]                │
│                                                      │
│  [NSAIDs]                                            │
│      ├── examples → [Ibuprofen, Naproxen]           │
│      ├── type_of → [Pain Reliever]                  │
│      └── contraindicated_with → [Anticoagulants]    │
└──────────────────────────────────────────────────────┘

Step 2: Process User Query
─────────────────────────────────────────────
Query: "What medications should I avoid if I'm taking warfarin 
        for atrial fibrillation?"

Extract entities from query:
- [Warfarin] ← Main entity
- [Atrial Fibrillation] ← Condition
- Looking for: Medications to avoid

Step 3: Graph Traversal Strategy
─────────────────────────────────────────────
Starting from [Warfarin], find:
1. Direct [interacts_with] relationships
2. [contraindicated_with] relationships
3. [warning] relationships

Traversal Path 1:
[Warfarin] → interacts_with → [Aspirin]
           → leads_to → [Increased Bleeding Risk]

Traversal Path 2:
[Warfarin] → interacts_with → [NSAIDs]
           → includes → [Ibuprofen]
           → includes → [Naproxen]
           → warning → [Use Cautiously]

Traversal Path 3:
[Warfarin] → type_of → [Anticoagulant]
           → contraindicated_with → [NSAIDs]

Step 4: Retrieve Context
─────────────────────────────────────────────
For each path, retrieve the original document chunks:

Path 1 documents:
- "Warfarin interacts with aspirin, increasing bleeding risk. 
   Concurrent use should be avoided unless specifically prescribed."

Path 2 documents:
- "NSAIDs like ibuprofen and naproxen should be used cautiously 
   with anticoagulants as they also affect platelet function."
- "The combination of warfarin and NSAIDs significantly increases 
   gastrointestinal bleeding risk."

Path 3 documents:
- "Anticoagulants are contraindicated with antiplatelet agents 
   and NSAIDs due to additive bleeding risk."

Step 5: Context-Aware Generation
─────────────────────────────────────────────
Send to AI:
- Graph paths (shows relationships)
- Retrieved document context
- User's specific situation (atrial fibrillation)

Generated Answer:
"Since you're taking warfarin for atrial fibrillation, you should 
avoid or use with caution:

1. Aspirin and antiplatelet drugs
   - Risk: Significantly increases bleeding risk
   - Action: Avoid unless specifically prescribed by your doctor

2. NSAIDs (Non-steroidal anti-inflammatory drugs)
   - Examples: Ibuprofen (Advil), Naproxen (Aleve)
   - Risk: Increases gastrointestinal bleeding risk
   - Action: Use cautiously and only under medical supervision
   - Alternative: Acetaminophen (Tylenol) is generally safer

3. Other anticoagulants
   - Risk: Excessive anticoagulation
   - Action: Never combine without explicit medical guidance

Always consult your healthcare provider before taking any new 
medications while on warfarin."
```

### Multi-Hop Reasoning Example

**Question:** "What's the connection between the CEO of the company that makes iPhone and the acquisition of Beats?"

```
Graph Traversal:
[iPhone] → manufactured_by → [Apple]
         → CEO → [Tim Cook]
         → approved_acquisition → [Beats Acquisition]
                                → price → [$3 billion]
                                → year → [2014]

Answer: "Tim Cook, CEO of Apple (the company that makes iPhone), 
approved the acquisition of Beats for $3 billion in 2014."
```

### Pros & Cons

**Pros:**
- ✅ Captures complex relationships between entities
- ✅ Excellent for multi-hop reasoning
- ✅ Explainable (can show the path taken)
- ✅ Rich contextual understanding
- ✅ Great for domains with many interconnections
- ✅ Can answer "how are X and Y related?" questions
- ✅ Reduces hallucination (paths must exist in graph)

**Cons:**
- ❌ Complex to build and maintain graphs
- ❌ Entity extraction is challenging (needs NER models)
- ❌ Relationship extraction is even harder
- ❌ Expensive to construct initially
- ❌ Requires domain expertise to design graph schema
- ❌ Can miss information not in graph form
- ❌ Graph updates are complex

### When to Use
- Medical knowledge bases (drugs, diseases, symptoms, treatments)
- Legal research (cases, statutes, precedents, relationships)
- Financial analysis (companies, executives, transactions)
- Scientific research (papers, citations, authors, institutions)
- Enterprise knowledge (organizations, people, projects, dependencies)
- Any domain where relationships are as important as facts

### Technologies
- **Graph Databases:** Neo4j, Amazon Neptune, ArangoDB
- **Entity Extraction:** spaCy, Stanford NER, fine-tuned BERT models
- **Knowledge Graph Libraries:** NetworkX, PyKEEN, DGL

---

## 6. Agentic RAG

### What It Is
The most advanced RAG approach where an AI agent autonomously plans, executes, and adapts its retrieval strategy. The agent can use multiple tools, make decisions, self-reflect, and iteratively improve its approach.

### Core Concept: AI as an Autonomous Agent

Instead of a fixed pipeline, the AI acts like a human researcher:
1. **Understands** the task
2. **Plans** how to approach it
3. **Uses tools** to gather information
4. **Evaluates** what it finds
5. **Adjusts** its strategy
6. **Verifies** the final answer

### Architecture
```
Complex User Question
    ↓
┌─────────────────────────────────────┐
│  AGENT REASONING LOOP               │
│                                     │
│  ┌──────────────────────┐          │
│  │ 1. PLANNING          │          │
│  │ - Break down task    │          │
│  │ - Identify needs     │          │
│  └──────────────────────┘          │
│           ↓                         │
│  ┌──────────────────────┐          │
│  │ 2. TOOL SELECTION    │          │
│  │ - Web search?        │          │
│  │ - Database query?    │          │
│  │ - Calculator?        │          │
│  │ - Code execution?    │          │
│  └──────────────────────┘          │
│           ↓                         │
│  ┌──────────────────────┐          │
│  │ 3. EXECUTION         │          │
│  │ - Use selected tools │          │
│  │ - Gather data        │          │
│  └──────────────────────┘          │
│           ↓                         │
│  ┌──────────────────────┐          │
│  │ 4. OBSERVATION       │          │
│  │ - Analyze results    │          │
│  │ - Identify gaps      │          │
│  └──────────────────────┘          │
│           ↓                         │
│  ┌──────────────────────┐          │
│  │ 5. REFLECTION        │          │
│  │ - Is answer complete?│          │
│  │ - Any contradictions?│          │
│  │ - Need more info?    │          │
│  └──────────────────────┘          │
│           ↓                         │
│  ┌──────────────────────┐          │
│  │ 6. DECISION          │          │
│  │ → Continue loop      │          │
│  │ → OR Final answer    │          │
│  └──────────────────────┘          │
│                                     │
└─────────────────────────────────────┘
```

### Step-by-Step Example

**Scenario:** Investment research assistant. Question: "Should I invest in Tesla stock right now? Consider current market conditions, company performance, and expert opinions."

```
═══════════════════════════════════════════════════════════════
AGENT THINKING LOG (Internal Reasoning)
═══════════════════════════════════════════════════════════════

┌─ CYCLE 1 ─────────────────────────────────────────────────┐

Thought: "This is a complex investment question. I need to gather:
         1. Current Tesla stock price and trends
         2. Recent company performance (earnings, deliveries)
         3. Market conditions (overall stock market, EV sector)
         4. Expert analyst opinions
         5. Recent news that might affect stock
         
         Let me start with current stock data."

Action: search_web("Tesla stock price today")

Observation: 
"Tesla (TSLA) trading at $242.50, down 2.3% today. 
 52-week range: $138.80 - $299.29
 P/E ratio: 76.5"

Thought: "Good, I have current price. But I need context. 
         Is this decline part of a trend? Let me check 
         recent performance."

└───────────────────────────────────────────────────────────┘

┌─ CYCLE 2 ─────────────────────────────────────────────────┐

Action: search_web("Tesla Q4 2024 earnings results")

Observation:
"Tesla Q4 2024: 
 - Revenue: $25.2B (up 3% YoY)
 - Net income: $1.9B (down 23% YoY)
 - Vehicle deliveries: 484,507 (up 2.3% YoY)
 - Margins compressed due to price cuts"

Thought: "Revenue up but profits down significantly. 
         This is concerning. I need to understand why 
         margins are compressed and what analysts think."

└───────────────────────────────────────────────────────────┘

┌─ CYCLE 3 ─────────────────────────────────────────────────┐

Action: search_web("Tesla analyst ratings 2024")

Observation:
"Average analyst rating: Hold
 17 analysts: 6 Buy, 8 Hold, 3 Sell
 Average price target: $255 (5% upside from current)
 
 Concerns:
 - Competition from Chinese EVs intensifying
 - Price cuts hurting margins
 - Macro headwinds (higher interest rates)"

Thought: "Mixed sentiment with slight lean toward hold. 
         The competition and margin issues are consistent 
         with the earnings data. Let me check market 
         conditions and EV sector trends."

└───────────────────────────────────────────────────────────┘

┌─ CYCLE 4 ─────────────────────────────────────────────────┐

Action: search_web("electric vehicle market trends 2024")

Observation:
"EV Market 2024:
 - Global EV sales growth slowing to 15% (from 35% in 2023)
 - Chinese EVs gaining market share globally
 - BYD overtook Tesla as world's largest EV maker
 - Government incentives being reduced in some markets"

Thought: "The sector is showing signs of maturation and 
         slowing growth. Competition is intensifying. 
         But I should also check broader market conditions."

└───────────────────────────────────────────────────────────┘

┌─ CYCLE 5 ─────────────────────────────────────────────────┐

Action: search_web("stock market outlook 2024 interest rates")

Observation:
"Market Conditions:
 - S&P 500 near all-time highs
 - Fed expected to hold rates at 5.25-5.50%
 - High interest rates affecting growth stocks
 - Investors rotating to value stocks"

Thought: "High interest rates are a headwind for growth 
         stocks like Tesla. This explains some of the 
         pressure. Let me also check recent Tesla-specific 
         news that might affect the stock."

└───────────────────────────────────────────────────────────┘

┌─ CYCLE 6 ─────────────────────────────────────────────────┐

Action: search_web("Tesla news today recent developments")

Observation:
"Recent Tesla News:
 - Cybertruck production ramping up slowly
 - FSD (Full Self-Driving) beta expanding
 - Mexico Gigafactory plans on hold
 - Elon Musk focused on xAI, raising concerns about 
   divided attention"

Thought: "Some positive (Cybertruck, FSD) but also 
         concerning signals (Mexico delay, CEO focus 
         issues). I now have enough information to 
         evaluate the investment thesis."

└───────────────────────────────────────────────────────────┘

┌─ SELF-REFLECTION ────────────────────────────────────────┐

Checklist:
✓ Current stock price and valuation
✓ Recent financial performance
✓ Analyst opinions and ratings
✓ Industry trends and competition
✓ Macro market conditions
✓ Company-specific recent news

Do I have enough information? YES

Are there any contradictions to resolve? 
- Analysts are mixed (some bullish, some bearish)
- Company growing revenue but shrinking profits
- Strong brand but intensifying competition

Can I provide a balanced recommendation? YES

└───────────────────────────────────────────────────────────┘

┌─ FINAL SYNTHESIS ────────────────────────────────────────┐

Action: generate_final_answer()

Generated Answer:

"Based on comprehensive analysis, here's my assessment of 
investing in Tesla stock right now:

CURRENT SITUATION:
- Stock Price: $242.50 (down 2.3% today)
- Valuation: P/E of 76.5 (expensive compared to traditional 
  automakers)
- Recent Performance: Revenue growing slowly (+3%), but 
  profits declining (-23%)

POSITIVE FACTORS:
• Strong brand and market position
• Cybertruck production ramping up
• Full Self-Driving technology advancing
• Long-term EV adoption tailwinds

NEGATIVE FACTORS:
• Intensifying competition (especially from Chinese EVs)
• Margin compression from price cuts
• Slowing EV market growth (15% vs 35% last year)
• High interest rates hurting growth stocks
• CEO divided attention concerns
• Analyst consensus: HOLD (not strong buy)

RECOMMENDATION:
❌ NOT a strong buy at current levels for these reasons:

1. Valuation Risk: P/E of 76.5 is high given slowing growth
2. Margin Pressure: Profit decline of 23% is concerning
3. Competition: BYD and Chinese EVs gaining market share
4. Macro Headwinds: High rates unfavorable for growth stocks
5. Limited Upside: Analyst target of $255 (only 5% higher)

ALTERNATIVE APPROACHES:
• Wait for Better Entry: Consider waiting for pullback to 
  $200-220 range
• Dollar-Cost Average: If bullish long-term, invest smaller 
  amounts over time
• Sector Alternative: Consider diversified EV ETF instead
• Risk Management: If you buy, position size should be <5% 
  of portfolio

BOTTOM LINE: 
While Tesla remains a leader in EVs, current conditions 
(high valuation, margin pressure, intensifying competition) 
suggest it's not an optimal entry point. Patient investors 
might find better risk/reward at lower prices.

This is not financial advice. Consult with a financial 
advisor before making investment decisions."

└───────────────────────────────────────────────────────────┘
```

### Agent Tools Available

Modern agentic RAG systems can use various tools:

```
INFORMATION GATHERING:
• web_search(query) - Search the internet
• fetch_webpage(url) - Read full articles
• query_database(sql) - Get structured data
• vector_search(query) - Search knowledge base
• news_api(topic) - Get latest news

COMPUTATION:
• calculator(expression) - Do math
• python_execute(code) - Run calculations/analysis
• data_analysis(csv_data) - Analyze datasets

VERIFICATION:
• fact_check(claim) - Verify claims
• source_credibility(url) - Check source reliability
• cross_reference(fact) - Check against multiple sources

SPECIALIZED:
• financial_data(ticker) - Get stock data
• weather_api(location) - Get weather
• translate(text, language) - Translate text
• image_analysis(image) - Analyze images
```

### Real Agent Frameworks

Popular frameworks for building agentic RAG:

**1. LangGraph (by LangChain)**
```python
from langgraph.graph import StateGraph

# Define agent state
class AgentState(TypedDict):
    question: str
    plan: str
    retrieved_docs: List[str]
    answer: str
    needs_more_info: bool

# Define agent nodes
def plan_step(state):
    # Agent plans approach
    return {"plan": create_plan(state["question"])}

def retrieve_step(state):
    # Agent retrieves information
    return {"retrieved_docs": search(state["question"])}

def reflect_step(state):
    # Agent evaluates if it has enough info
    return {"needs_more_info": evaluate(state)}

# Build graph
workflow = StateGraph(AgentState)
workflow.add_node("plan", plan_step)
workflow.add_node("retrieve", retrieve_step)
workflow.add_node("reflect", reflect_step)

# Add conditional logic
workflow.add_conditional_edges(
    "reflect",
    lambda s: "retrieve" if s["needs_more_info"] else "end"
)
```

**2. AutoGPT Pattern**
```python
while not task_complete:
    # Think
    thought = agent.think(current_state)
    
    # Decide action
    action = agent.decide_action(thought)
    
    # Execute
    result = agent.execute(action)
    
    # Reflect
    should_continue = agent.reflect(result)
    
    if not should_continue:
        break
```

### Pros & Cons

**Pros:**
- ✅ Handles extremely complex, multi-step tasks
- ✅ Self-correcting and adaptive
- ✅ Can use multiple tools and data sources
- ✅ Human-like reasoning and problem-solving
- ✅ Handles ambiguity well
- ✅ Can discover unexpected connections
- ✅ Explainable (shows reasoning process)

**Cons:**
- ❌ Very high latency (many iterations)
- ❌ Expensive (numerous LLM calls, often 20-50+)
- ❌ Can be unpredictable (different paths each time)
- ❌ Difficult to debug and test
- ❌ Might over-complicate simple questions
- ❌ Risk of infinite loops if not designed carefully
- ❌ Requires careful prompt engineering and safety rails

### When to Use
- Complex research and analysis tasks
- Investment research and due diligence
- Competitive intelligence
- Scientific literature review
- Legal case research
- Strategic planning support
- When accuracy and thoroughness matter more than speed
- Tasks requiring multi-step reasoning with verification

### When NOT to Use
- Simple FAQ questions
- Time-sensitive queries needing instant answers
- High-volume, routine queries
- When cost is a major constraint
- Production systems where consistency is critical

---

## Choosing the Right Type

### Decision Framework

```
┌─────────────────────────────────────────────────────────┐
│  START: What kind of application are you building?      │
└─────────────────────────────────────────────────────────┘
                        ↓
        ┌───────────────┴───────────────┐
        │                               │
    Is it just                      Is it a
    a prototype/                    production
    proof of concept?               application?
        │                               │
        YES                             YES
        ↓                               ↓
    Use NAIVE RAG              What's your priority?
    - Fast setup                       ↓
    - Test feasibility        ┌────────┴────────┐
    - Low investment          │                 │
                        Speed & Cost      Accuracy & Quality
                              │                 │
                              ↓                 ↓
                        STANDARD RAG      ADVANCED RAG
                        - Hybrid search   - Query decomposition
                        - Re-ranking      - Iterative retrieval
                        - Good balance    - Higher accuracy
                              
                                    
        Is your application                    Do you have
        serving different                      knowledge that's
        types of queries?                      highly interconnected?
                ↓                                      ↓
               YES                                    YES
                ↓                                      ↓
        MODULAR RAG                              GRAPH RAG
        - Route by query type                    - Entity relationships
        - Optimize per use case                  - Multi-hop reasoning
        - Mix and match components               - Medical, legal, etc.
        
        
        Do you need autonomous
        research and complex
        multi-step reasoning?
                ↓
               YES
                ↓
        AGENTIC RAG
        - Self-planning
        - Tool usage
        - Iterative refinement
        - Maximum capability
```

### Quick Comparison Table

| Feature | Naive | Standard | Advanced | Modular | Graph | Agentic |
|---------|-------|----------|----------|---------|-------|---------|
| **Setup Time** | 1 day | 1 week | 2-4 weeks | 3-6 weeks | 4-8 weeks | 6-12 weeks |
| **Latency** | <1s | 1-3s | 3-10s | 1-5s | 2-6s | 5-30s |
| **Cost per Query** | $0.001 | $0.01 | $0.05 | $0.01-0.10 | $0.02 | $0.10-1.00 |
| **Accuracy** | 60-70% | 75-85% | 85-92% | 80-90% | 88-95% | 90-98% |
| **Complexity** | ⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Maintenance** | Easy | Medium | Hard | Medium | Hard | Very Hard |

### Practical Recommendations

**Start Here for Most Projects:**
→ **Standard RAG**
- Covers 80% of use cases
- Good balance of cost/performance
- Production-ready
- Easy to understand and debug

**Upgrade to Advanced RAG when:**
- Users ask complex, multi-part questions
- Need high accuracy (>85%)
- Can tolerate higher latency
- Have budget for more LLM calls

**Consider Modular RAG when:**
- Serving multiple distinct use cases
- Need to optimize different metrics for different queries
- Want flexibility to experiment
- Have engineering resources for integration

**Choose Graph RAG when:**
- Domain has rich relationships (medical, legal, scientific)
- Questions involve "how are X and Y related?"
- Multi-hop reasoning is common
- Have data that naturally forms a graph

**Deploy Agentic RAG when:**
- Tasks require genuine research
- Need autonomous problem-solving
- Accuracy is paramount (even at high cost)
- Can tolerate unpredictability
- Users are willing to wait for quality

### Migration Path

```
Phase 1: Prototype (Week 1)
└─→ Naive RAG - Validate the concept

Phase 2: MVP (Weeks 2-4)
└─→ Standard RAG - Launch to early users

Phase 3: Optimization (Months 2-3)
└─→ Add Advanced RAG for complex queries
    (Keep Standard RAG for simple ones)

Phase 4: Scale (Months 4-6)
└─→ Modular RAG - Route different query types
    Different pipelines for different needs

Phase 5: Specialization (6+ months)
└─→ Add Graph RAG for specific domains
    Add Agentic RAG for research tasks
```

---

## Appendix: Glossary

### A-E
- **Agentic**: System where AI acts autonomously, making decisions about what actions to take
- **BM25**: Traditional keyword-based search algorithm (stands for "Best Matching 25")
- **Chunking**: Splitting documents into smaller pieces
- **Context Window**: Maximum amount of text an AI model can process at once
- **Cross-Encoder**: Neural model that scores query-document pairs for relevance
- **Dense Retrieval**: Search using semantic embeddings
- **Embedding**: Numerical representation of text that captures meaning
- **Entity**: A thing (person, place, object, concept) in text

### F-M
- **Fusion**: Combining results from multiple search methods
- **Graph Database**: Database that stores data as nodes and relationships
- **HyDE**: Hypothetical Document Embeddings - generating fake answer to search with
- **Iterative Retrieval**: Retrieving information multiple times in sequence
- **Knowledge Graph**: Network of entities and their relationships
- **LLM**: Large Language Model (like GPT, Claude)
- **Multi-hop Reasoning**: Connecting multiple pieces of information in sequence

### N-Z
- **NER**: Named Entity Recognition - identifying entities in text
- **Query Decomposition**: Breaking complex questions into simpler sub-questions
- **Query Expansion**: Adding related terms to a search query
- **RAG**: Retrieval-Augmented Generation
- **Re-ranking**: Reordering search results by relevance
- **Self-Reflection**: AI evaluating its own output
- **Semantic Search**: Search based on meaning rather than keywords
- **Sparse Retrieval**: Traditional keyword-based search
- **Vector Database**: Database optimized for storing and searching embeddings

---

## Final Tips for Beginners

1. **Start Simple**: Begin with Naive or Standard RAG. Don't jump to complexity.

2. **Measure Everything**: Track metrics like:
   - Retrieval accuracy (are you finding the right documents?)
   - Answer quality (is the final answer good?)
   - Latency (how long does it take?)
   - Cost (how much per query?)

3. **Iterate Based on Failures**: When RAG fails, understand why:
   - Bad retrieval? → Improve chunking, indexing, search
   - Good retrieval but bad answer? → Improve prompts, context
   - Slow? → Optimize pipeline, reduce unnecessary steps

4. **Use Tools**: Don't build everything from scratch:
   - LangChain/LlamaIndex for RAG pipelines
   - Pinecone/Weaviate for vector databases
   - Cohere for re-ranking
   - OpenAI/Anthropic for LLMs

5. **Test with Real Users**: Your assumptions about what works will often be wrong. Get real user feedback early.

6. **Document Your Choices**: Write down why you chose certain chunk sizes, search methods, etc. You'll forget otherwise.

7. **Monitor in Production**: RAG systems can degrade over time as documents change. Set up monitoring.

---

**This guide should give you a solid foundation in RAG systems. Start simple, learn from failures, and gradually add complexity only when needed!**