# Node.js Interview Notes — Day 2: Fundamentals, Core Modules & Node Lifecycle

## 1. How Does the Web Work? (Request Lifecycle)

A simplified journey of a request from browser to response:

1. **Client** types a URL / makes a request (e.g., `www.example.com`).
2. **DNS lookup** — the domain name is resolved to an **IP address** (DNS = Domain Name System, essentially the internet's phonebook).
3. Request travels to the **server** at that IP address, usually over HTTP/HTTPS.
4. The server processes the request — this often means talking to a **database** to fetch or store data.
5. Server sends a **response** back (HTML, JSON, etc.) to the client, which renders/uses it.

**Interview soundbite:**
> "When you hit enter on a URL, the browser first resolves the domain to an IP via DNS, sends an HTTP request to the server at that IP, the server does its processing — often querying a database — and sends back a response."

---

## 2. HTTP vs HTTPS

| | HTTP | HTTPS |
|---|---|---|
| Full form | HyperText Transfer Protocol | HTTP **Secure** |
| Encryption | None — data sent in plain text | Uses **TLS/SSL** to encrypt data |
| Port | 80 | 443 |
| Security | Vulnerable to interception (man-in-the-middle) | Data is encrypted in transit |
| Certificate | Not required | Requires an **SSL/TLS certificate** |

**Interview soundbite:**
> "HTTPS is HTTP layered with TLS encryption, so data exchanged between client and server can't be read or tampered with in transit. It also verifies the server's identity via a certificate."

---

## 3. Core Node.js Modules

Node ships with built-in modules so you don't need external packages for basic tasks:

- **`http` / `https`** — create servers, make requests, handle HTTP(S) communication
- **`fs`** (File System) — read/write/delete files, both sync and async versions (e.g., `fs.readFile` vs `fs.readFileSync`)
- **`path`** — safely handle and manipulate file paths across operating systems (e.g., `path.join`, `path.resolve`) — avoids issues with `/` vs `\` between Linux/Windows
- **`os`** — get information about the operating system (CPU, memory, platform, home directory, etc.)

These are all available without installing anything via `npm` — just `require('fs')`, `require('path')`, etc.

---

## 4. Creating a Simple Server with `http.createServer`

```js
const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello World');
});

server.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

**What's happening:**
- `http.createServer()` takes a **callback function** that runs every time a request hits the server.
- The callback receives `req` (request object — has method, URL, headers, body) and `res` (response object — used to send data back).
- `server.listen(port)` starts the server listening for incoming connections on that port.
- This callback is essentially an **event listener** — it stays registered and fires every time a new request event occurs.

---

## 5. Node.js Application Lifecycle

When you run `node app.js`:

1. **Node starts** and reads/parses your file.
2. **Registration phase** — Node parses the code top to bottom:
   - Functions and variables get registered/defined
   - Any modules you `require` get loaded
   - Any event listeners you set up (like the callback in `http.createServer`) get **registered** with the event loop
3. **Execution of top-level (synchronous) code** happens immediately.
4. **Event loop kicks in** — once the initial script finishes running synchronously, Node doesn't exit. Instead, it checks: *"Are there any pending events/callbacks/listeners still registered?"*
5. **Node keeps running as long as there's at least one active event listener** — e.g., an HTTP server listening for requests. This is why `node app.js` for a server **doesn't exit immediately** — the `http.createServer` callback keeps the event loop "alive," waiting for incoming request events.
6. If there's nothing left registered (no timers, no open servers, no pending callbacks), the event loop has nothing to do, and the **Node process exits naturally**.

**Interview soundbite:**
> "Node parses the file, executes synchronous code top-to-bottom, and registers any callbacks or listeners. Then the event loop takes over — as long as something is still registered, like a server listening for requests, the process stays alive. Once nothing is left to listen for, Node exits."

---

## 6. Event Loop (Recap + Lifecycle Connection)

- The event loop is the mechanism that lets Node handle async operations despite being single-threaded.
- It continuously checks the call stack — when empty, it pulls the next callback from the queue and executes it.
- **This is directly tied to the Node lifecycle**: the reason a running server doesn't exit is that the event loop keeps finding registered listeners (like the request handler) to potentially execute.

---

## 7. Streams and Buffers

### Buffers
- A **Buffer** is a temporary space in memory used to hold raw binary data while it's being read/written (before it's fully processed).
- Example: when reading a file or receiving network data, chunks arrive as **binary data** — a Buffer holds this raw data before it's converted to a usable format (e.g., a string).
- Buffers exist because JavaScript historically had no good way to handle raw binary data — Node's `Buffer` class fills that gap.

### Streams
- A **Stream** is a way of handling data **piece by piece (in chunks)** instead of loading it all into memory at once.
- Useful for large files/data — e.g., reading a 2GB video file. Loading it all at once would consume huge memory; streaming it lets you process it chunk-by-chunk.
- **Types of streams:**
  - **Readable** — data you can read from (e.g., `fs.createReadStream`)
  - **Writable** — data you can write to (e.g., `fs.createWriteStream`)
  - **Duplex** — both readable and writable (e.g., a TCP socket)
  - **Transform** — a duplex stream that modifies data as it passes through (e.g., compression with `zlib`)

**Interview soundbite:**
> "Streams let Node process data incrementally rather than loading it all into memory — critical for handling large files or data efficiently. Buffers are the temporary in-memory holders for the raw chunks of binary data as they move through a stream."

---

## 8. Event-Driven Architecture

- Node.js is built around **events** — instead of a linear flow, code reacts to things happening (a request arriving, a file finishing reading, a timer completing).
- Core to this is the **`EventEmitter`** class (from the `events` module) — many built-in Node objects (like HTTP servers, streams) are `EventEmitter`s under the hood.
- Example pattern:
```js
const EventEmitter = require('events');
const emitter = new EventEmitter();

emitter.on('greet', (name) => console.log(`Hello, ${name}`));
emitter.emit('greet', 'Priya');
```
- This is the same underlying pattern as `http.createServer((req, res) => {...})` — you're registering a listener for a "request" event.

---

## 9. Single Thread, Event Loop & Blocking Code (Recap + Deeper Tie-In)

- JS execution in Node happens on a **single thread** — one call stack.
- The **event loop** allows async, non-blocking behavior on top of that single thread by offloading work and queuing callbacks.
- **Blocking code** (like a long `for` loop, or a synchronous heavy computation, or `fs.readFileSync` on a huge file) **occupies the single thread**, so the event loop can't process anything else — no other requests, no other timers — until that blocking operation finishes.
- This is why **understanding what's sync vs async matters so much in Node**: a single blocking call in a server can freeze the entire application for all connected users.

---

## Practice Questions & Answers

**Q1: Walk me through what happens when a browser requests a webpage, from URL to response.**
> A1: Browser resolves the domain to an IP via DNS lookup, sends an HTTP(S) request to the server at that IP, the server processes it (possibly querying a database), and sends a response back to the client.

**Q2: What's the difference between HTTP and HTTPS?**
> A2: HTTPS is HTTP secured with TLS/SSL encryption — data is encrypted in transit and the server's identity is verified via certificate. HTTP sends data in plain text over port 80; HTTPS uses port 443.

**Q3: Name four Node.js core modules and what they're used for.**
> A3: `http`/`https` for creating servers and handling requests, `fs` for file system operations, `path` for handling file paths cross-platform, `os` for OS-level system information.

**Q4: How would you create a basic HTTP server in Node without any frameworks?**
> A4: Using `http.createServer((req, res) => {...})` with a callback that handles incoming requests, then calling `.listen(port)` to start listening for connections.

**Q5: Why doesn't a Node.js server exit immediately after running `node app.js`?**
> A5: Because the event loop keeps the process alive as long as there are active listeners or pending callbacks — like the request listener registered via `http.createServer`. The process only exits once nothing is left registered.

**Q6: What's the difference between a Buffer and a Stream?**
> A6: A Buffer is a temporary in-memory holder for raw binary data. A Stream is a mechanism for processing data incrementally, in chunks, rather than loading everything into memory at once — Buffers are often what hold each chunk as it moves through a stream.

**Q7: What are the four types of streams in Node.js?**
> A7: Readable, Writable, Duplex (both), and Transform (modifies data as it passes through).

**Q8: What is event-driven architecture, and what class underlies it in Node?**
> A8: An architecture where code reacts to emitted events rather than running in a strict linear sequence. It's built on the `EventEmitter` class — many core Node objects (HTTP servers, streams) extend or use `EventEmitter` internally.

**Q9: What happens if you run a long, CPU-heavy synchronous loop inside a Node HTTP server handling multiple users?**
> A9: It blocks the single thread — the event loop can't process any other requests, timers, or callbacks until that loop finishes, freezing the server for every connected client.

**Q10: Describe the Node.js application lifecycle at a high level.**
> A10: Node parses the file top to bottom, executing synchronous code and registering functions, variables, and event listeners (e.g., an HTTP server's request handler). Once synchronous execution finishes, the event loop takes over, keeping the process alive as long as active listeners or pending callbacks exist, and exiting once none remain.

---

## Quick Reference Table

| Concept | One-liner |
|---|---|
| DNS | Resolves domain name → IP address |
| HTTP vs HTTPS | HTTPS = HTTP + TLS encryption, port 443 vs 80 |
| `http`/`https` | Build servers, handle HTTP(S) traffic |
| `fs` | File read/write operations |
| `path` | Cross-platform safe path handling |
| `os` | OS-level system info |
| Node lifecycle | Parse → register → execute sync code → event loop takes over → exits when nothing registered |
| Buffer | Temporary in-memory holder for raw binary data |
| Stream | Process data in chunks instead of all at once |
| EventEmitter | Core class behind Node's event-driven architecture |
| Blocking code | Freezes the single thread — no other requests processed until done |