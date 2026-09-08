# 08/09/2026

# Node.js Interview Notes — Day 1: Runtime, Event Loop & Async Architecture

## 1. What is Node.js?

**Node.js is NOT a framework or a programming language.** It is a **JavaScript runtime environment** that lets you run JavaScript outside the browser (e.g., on a server).

- It's built on **Chrome's V8 engine**, which compiles JavaScript directly to machine code.
- Node itself is written primarily in **C++**, with V8 embedded inside it to execute JS.
- Node adds APIs that browsers don't have (like `fs` for file access, `http` for servers, `process`, etc.) since there's no browser environment involved.

**One-line answer for interviews:**
> "Node.js is a runtime built on Chrome's V8 engine that allows JavaScript to run outside the browser, primarily for building server-side applications."

---

## 2. Why is Node.js Highly Scalable?

Node.js applications scale well because of their **non-blocking, asynchronous I/O model**.

- Instead of waiting for an operation (like a database query or file read) to finish before moving to the next line, Node **hands off** the operation and keeps executing other code.
- When the operation completes, a **callback** (or Promise resolution) is queued to handle the result.
- This means a single Node process can handle **thousands of concurrent connections** without spawning a new thread per request (unlike traditional thread-per-request models in languages like Java or PHP).

**Key phrase interviewers want to hear:** *"non-blocking, event-driven architecture"*

---

## 3. Blocking (Synchronous) vs Non-Blocking (Asynchronous) Architecture

### Blocking (Synchronous)
- Each operation must **complete before the next one starts**.
- If one request is reading a large file, every other request has to **wait**.
- Example: traditional synchronous file read (`fs.readFileSync`) — the whole program pauses until the file is read.

### Non-Blocking (Asynchronous)
- An operation is **started**, and execution **moves on immediately** to the next line of code.
- When the operation finishes, a callback/Promise handles the result — **without freezing the rest of the program**.
- Example: `fs.readFile` (async version) — Node continues executing other code while the file loads in the background.

**Analogy for interviews:**
> "Blocking is like a chef who cooks one dish start to finish before starting the next. Non-blocking is like a chef who starts dish A, and while it's in the oven, starts prepping dish B — without standing and waiting."

---

## 4. JavaScript is Single-Threaded but Behaves Asynchronously

- JavaScript (and Node.js) runs on a **single thread** — there's only **one call stack**, so only one operation executes at a time.
- Despite this, JS can handle async operations (timers, network calls, file I/O) **without blocking** thanks to:
  - The **Event Loop**
  - The **Callback Queue / Task Queue**
  - **Web APIs / Node APIs** (provided by the browser or by Node's C++ bindings, *not* by the JS engine itself)

**Important nuance:** V8 (the JS engine) itself is single-threaded, but Node.js under the hood uses a **thread pool (libuv)** for certain operations (like file system tasks). The single-threaded part is specifically about **JS execution** — not necessarily everything Node does internally.

---

## 5. How the Event Loop Works (Simplified)

1. **Call Stack** — where your synchronous code executes, function by function.
2. When an async operation (e.g., `setTimeout`, an HTTP request, a file read) is encountered, it's **handed off** to the Node/browser API to handle in the background.
3. Once that operation completes, its callback is placed into a **queue**:
   - **Microtask queue** — for Promises (`.then`, `async/await`) and `process.nextTick`. Higher priority.
   - **Macrotask queue (callback queue)** — for `setTimeout`, `setInterval`, I/O callbacks. Lower priority.
4. The **Event Loop** constantly checks: *"Is the call stack empty?"*
   - If yes, it takes the next callback from the queue (microtasks first, fully drained, then one macrotask) and pushes it onto the call stack to execute.
5. This cycle repeats — giving the illusion of concurrency on a single thread.

**Interview soundbite:**
> "The event loop is what allows Node.js to perform non-blocking I/O despite JavaScript being single-threaded — it offloads operations, and once the call stack is clear, it pulls completed callbacks back in to execute, prioritizing microtasks like Promises over macrotasks like setTimeout."

---

## 6. Why Node.js is Ideal for I/O-Intensive Applications

I/O-intensive = apps that spend most of their time **waiting** on external operations: database queries, API calls, file reads/writes, network requests.

- Since Node doesn't block while waiting on I/O, it can **juggle many I/O operations concurrently** on a single thread.
- Great fits: REST APIs, chat applications, streaming services, real-time apps (using WebSockets), microservices that mostly call other services/databases.

---

## 7. Why NOT to Use Node.js for CPU-Intensive Applications

- CPU-intensive tasks (image/video processing, heavy computations, complex encryption) **occupy the single thread** for a long time.
- Since JS execution is single-threaded, a long-running computation **blocks the event loop** — meaning **no other requests can be processed** until it finishes. This kills the scalability advantage.
- Example problem: if one user triggers a heavy computation, *every other user's request freezes* until it's done.
- **Workarounds** (good to mention in interviews): 
  - Worker Threads (`worker_threads` module) for parallelizing CPU work
  - Offloading heavy tasks to a separate service/queue (e.g., a background job processor)
  - Clustering (`cluster` module) to use multiple CPU cores across processes

---

## 8. Node.js Under the Hood

- Node.js is essentially a **C++ program** that embeds the **V8 engine** to execute JavaScript.
- Node adds:
  - **libuv** — a C library that provides the event loop and handles async I/O (including the thread pool for file system/DNS operations).
  - Core modules (`fs`, `http`, `path`, `events`, etc.) written partly in JS, partly in C++.
- This combination is why Node can offer JS-friendly syntax while still doing low-level, high-performance I/O operations.

---

## Practice Questions

Try answering these out loud before checking your notes — that's the real test.

1. Is Node.js a programming language or a framework? What is it, exactly?
2. What engine does Node.js use to execute JavaScript, and what language is Node itself written in?
3. Explain blocking vs non-blocking architecture with an example.
4. Why is Node.js considered single-threaded if it can handle thousands of concurrent connections?
5. Walk through what happens when you call `setTimeout(() => {}, 0)` in terms of the call stack, Web/Node APIs, and the event loop.
6. What's the difference between the microtask queue and the macrotask (callback) queue? Which one has priority?
7. Why is Node.js a good fit for I/O-intensive applications? Give two real-world examples.
8. Why should you avoid using Node.js for CPU-intensive tasks? What would happen if you ran a heavy synchronous computation in a Node server handling multiple users?
9. If Node.js JS execution is single-threaded, how does it handle things like file system operations without blocking? (Hint: mention libuv / thread pool.)
10. What are Worker Threads, and when would you use them?
11. What's the difference between `fs.readFileSync` and `fs.readFile`? Which one would you use in a production server and why?
12. What role does libuv play in Node.js?

---

## Quick Self-Check Answers (short form)

| # | Short Answer |
|---|---|
| 1 | Runtime environment, not a language or framework |
| 2 | V8 engine; Node itself is written in C++ |
| 3 | Blocking waits for each op to finish; non-blocking moves on and handles results via callbacks |
| 4 | Only one call stack for JS execution, but async ops are offloaded to Node/libuv APIs, not the JS thread |
| 5 | Callback is queued in the macrotask queue and only runs once the call stack is empty and microtasks are drained |
| 6 | Microtasks (Promises, `process.nextTick`) run before macrotasks (`setTimeout`, I/O callbacks); microtasks have priority |
| 7 | Non-blocking I/O lets it handle many concurrent waits efficiently — e.g., REST APIs, chat apps |
| 8 | It blocks the single thread, freezing all other requests — bad for scalability |
| 9 | Via libuv's thread pool, which handles certain I/O operations outside the main JS thread |
| 10 | A module to run JS in parallel threads for CPU-heavy work, avoiding blocking the main thread |
| 11 | `readFileSync` blocks execution; `readFile` is async and non-blocking — always prefer async in production |
| 12 | C library providing the event loop and async I/O (including the thread pool) for Node |