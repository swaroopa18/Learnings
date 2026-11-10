# Hello Interview: System Design Delivery Framework

## The core idea

A system design interview is not about designing the most sophisticated
system. It is about delivering a clear, complete design within the
available time and explaining the reasoning behind your decisions.

A strong approach is to: 1. Understand the problem. 2. Identify the
important data. 3. Define the system's interface. 4. Sketch a working
architecture. 5. Find bottlenecks and improve the design.

We'll use **Twitter/X** as a running example.

------------------------------------------------------------------------

## 1. Requirements gathering (about 5 minutes)

Before drawing boxes or choosing technologies, clarify what the system
must do.

### Functional requirements: What should it do?

For a simplified Twitter design: - Users can create tweets. - Users can
follow other users. - Users can view a feed containing tweets from
people they follow.

Focus on the most important features. Trying to design every feature can
consume the interview and prevent you from completing the core design.

### Non-functional requirements: How well should it work?

Examples:

  Requirement       Meaning
  ----------------- -----------------------------------------------
  Scalability       Support a large and growing user base
  Availability      Keep the service accessible
  Latency           Return responses quickly
  Durability        Avoid losing persisted tweets
  Fault tolerance   Continue operating despite component failures
  Security          Protect accounts and user data

Quantify requirements when useful. For example, "feed requests should
have a p99 latency below 200 ms" is more actionable than "the feed
should be fast."

### Capacity estimation

Estimate traffic, storage, bandwidth, or read/write ratios when the
result could change your architecture.

For example, estimating the number of followers per user may help you
decide whether feed generation should happen when a tweet is created or
when a user requests their feed.

**Rule of thumb:** Do calculations that inform a design decision. Avoid
calculations that do not change what you would build.

------------------------------------------------------------------------

## 2. Identify core entities (about 2 minutes)

Entities are the main objects or nouns in the system.

For Twitter:

### User

-   `user_id`
-   `name`
-   `email`

### Tweet

-   `tweet_id`
-   `user_id`
-   `content`
-   `created_at`

### Follow

-   `follower_id`
-   `followee_id`
-   `created_at`

Entities help you reason about what information must be stored,
retrieved, and related.

At this stage, identify the important objects. Do not spend time
designing every database column or index before the requirements are
clear.

------------------------------------------------------------------------

## 3. Define APIs (about 5 minutes)

APIs describe how clients interact with the system. They turn the
requirements into concrete operations.

Example Twitter APIs:

  Operation                     Endpoint
  ----------------------------- ----------------------------
  Create a tweet                `POST /v1/tweets`
  Get a tweet                   `GET /v1/tweets/{tweetId}`
  Follow a user                 `POST /v1/follows`
  Get the current user's feed   `GET /v1/feed`

Example request:

``` http
POST /v1/tweets
Content-Type: application/json
Authorization: Bearer <token>
```

``` json
{
  "text": "Hello World!"
}
```

The backend might: 1. Authenticate the user. 2. Get the user's ID from
the authenticated context. 3. Validate the tweet. 4. Persist it. 5.
Return the created tweet.

### Choosing a protocol

-   **REST:** A sensible default for many client-facing APIs.
-   **GraphQL:** Useful when clients need flexible combinations of data.
-   **RPC/gRPC:** Often useful for efficient service-to-service
    communication.
-   **WebSockets or Server-Sent Events:** Useful when the product needs
    server-initiated real-time updates.

Choose based on requirements, not fashion.

------------------------------------------------------------------------

## 4. Describe the data flow (optional, about 5 minutes)

Data flow explains what happens to data from the moment it enters the
system until the intended result is produced.

This is especially useful for systems with multiple processing stages,
such as: - Payment processing - Video processing - Notification
systems - Web crawlers - Data pipelines

For example, a simplified crawler flow is:

1.  Read seed URLs.
2.  Fetch pages.
3.  Parse HTML.
4.  Extract links.
5.  Store page data and discovered URLs.
6.  Repeat for eligible URLs.

If the system's flow is straightforward, skip this step and use the time
elsewhere.

------------------------------------------------------------------------

## 5. Draw the high-level design (about 10--15 minutes)

Now connect components to support the requirements and APIs.

Start with the simplest architecture that works. Add complexity only
when you can explain what problem it solves.

### Example: Create a tweet

A basic request path:

``` text
Client
  |
  v
Load Balancer
  |
  v
Application Server
  |
  v
Tweet Database
```

The flow: 1. The client sends a create-tweet request. 2. The load
balancer routes it to an application server. 3. The server authenticates
and validates the request. 4. The server writes the tweet to the
database. 5. The server returns a response.

This is a valid starting point. It is not necessarily the final
architecture.

### Example: Get a feed

A simple first implementation could: 1. Find the accounts the current
user follows. 2. Fetch recent tweets from those accounts. 3. Sort the
tweets by creation time. 4. Return a page of results.

This may be sufficient at small scale, but it can become expensive for
users who follow many accounts. That weakness becomes a topic for a deep
dive.

### Avoid premature complexity

Do not add Redis, Kafka, multiple databases, microservices, sharding,
and replication simply to make the diagram look sophisticated.

Instead: 1. Build a basic end-to-end design. 2. Identify its
limitations. 3. Improve it based on concrete requirements.

------------------------------------------------------------------------

## 6. Deep dives (about 10 minutes)

Use deep dives to address bottlenecks and non-functional requirements.
Explain the problem first, then the proposed solution and its
trade-offs.

### Problem A: Feed reads are slow

If every feed request queries all followed accounts and gathers their
tweets, the read path may become expensive.

One possible improvement is caching frequently accessed feed data.

``` text
Client
  |
  v
Feed Service
  |
  v
Redis Cache
  |
  +---- Cache hit: return cached feed
  |
  +---- Cache miss: fetch from persistent storage
```

Caching can reduce repeated database work and improve latency. It also
introduces challenges such as expiration, invalidation, and stale data.

### Problem B: A user has an enormous number of followers

Suppose a celebrity has tens of millions of followers. When they publish
a tweet, immediately writing that tweet into every follower's feed can
create a large burst of work.

This leads to two common approaches:

  -----------------------------------------------------------------------
  Approach                How it works            Trade-off
  ----------------------- ----------------------- -----------------------
  Fanout-on-write         Push a new tweet into   Fast reads, potentially
                          followers' feed stores  expensive writes
                          when it is created      

  Fanout-on-read          Fetch followed users'   Cheaper tweet writes,
                          tweets when a user      potentially expensive
                          opens their feed        reads
  -----------------------------------------------------------------------

A hybrid design can use fanout-on-write for ordinary accounts and
fanout-on-read for accounts with exceptionally large audiences.

### Problem C: The database becomes a bottleneck

Potential techniques include: - **Caching:** Reduce repeated reads from
the database. - **Read replicas:** Distribute read traffic across
database replicas. - **Sharding:** Partition data across multiple
database nodes. - **Asynchronous processing:** Move non-critical work
off the synchronous request path. - **Queueing:** Buffer work and
decouple producers from consumers.

Do not introduce a technology without explaining why it is needed.

For example:

> Feed updates should not delay the response to a create-tweet request.
> I would publish an event to a durable queue and let background workers
> update feed data asynchronously. This reduces coupling and keeps the
> user-facing write path shorter, at the cost of eventual consistency
> and additional operational complexity.

That explanation is stronger than simply saying, "Let's use Kafka."

------------------------------------------------------------------------

## 7. What interviewers evaluate

  -----------------------------------------------------------------------
  Area                                What to demonstrate
  ----------------------------------- -----------------------------------
  Problem understanding               Ask relevant clarifying questions

  Prioritization                      Identify the most important
                                      requirements

  Technical fundamentals              Choose appropriate storage and
                                      infrastructure

  Architecture                        Build a coherent end-to-end design

  Scalability                         Identify bottlenecks and explain
                                      solutions

  Communication                       Explain decisions and trade-offs
                                      clearly

  Collaboration                       Respond constructively to
                                      interviewer feedback
  -----------------------------------------------------------------------

Expectations vary with seniority. More senior candidates are generally
expected to identify risks and lead deeper architectural discussions
more independently.

Keep the conversation collaborative. Explain your reasoning, pause for
feedback, and invite the interviewer to explore important trade-offs
with you.

------------------------------------------------------------------------

## 8. The complete framework: interview checklist

Use this sequence for each system design problem:

### 1. Requirements

-   What are the most important user-facing features?
-   What are the key non-functional requirements?
-   What is explicitly out of scope?
-   Which estimates would influence the design?

### 2. Core entities

-   What are the main objects?
-   How are they related?
-   What data must be stored?

### 3. APIs

-   What operations must clients perform?
-   What are the key request and response fields?
-   Are synchronous APIs sufficient, or is real-time communication
    needed?

### 4. Data flow (when useful)

-   Where does data enter?
-   Which processing steps occur?
-   What is synchronous and what is asynchronous?
-   Where is the result stored or delivered?

### 5. High-level design

-   What are the main services and storage systems?
-   How does each API work end to end?
-   Can the basic design satisfy the core requirements?

### 6. Deep dives

-   What is the likely bottleneck?
-   What happens when traffic grows?
-   What happens when a component fails?
-   What consistency and latency trade-offs exist?
-   Which improvement best addresses the problem?

------------------------------------------------------------------------

## 9. Practical preparation advice

Do not merely memorize the architecture of Twitter, WhatsApp, Netflix,
or Uber. Practice applying the same reasoning process to unfamiliar
problems.

For every practice question, try to answer:

1.  What are the three most important functional requirements?
2.  What are the most important non-functional requirements?
3.  What are the core entities?
4.  What APIs are needed?
5.  What happens when a request enters the system?
6.  What are the likely bottlenecks?
7.  How would you address them, and what trade-offs would the solutions
    introduce?

A simple, complete architecture that you can explain and improve is
better than a sophisticated architecture that you never finish.

## 10. Quick self-test

1.  **You are asked to design WhatsApp. What should you do first?**\
    Clarify functional and non-functional requirements.

2.  **Why define APIs before the high-level architecture?**\
    APIs identify the operations the architecture must support.

3.  **When should you introduce caching?**\
    When a latency or workload requirement gives you a reason to reduce
    repeated access to slower storage.

4.  **What is the purpose of deep dives?**\
    To improve the initial design by addressing bottlenecks, scale,
    reliability, and other non-functional requirements.

------------------------------------------------------------------------

## Final takeaway

The delivery framework is a way to structure your thinking and manage
interview time:

**Requirements → Entities → APIs → Data flow (optional) → High-level
design → Deep dives**

Start simple, complete the end-to-end design, identify its limitations,
and improve it with clear reasoning. The goal is not to name the most
technologies; it is to demonstrate sound engineering judgment.
