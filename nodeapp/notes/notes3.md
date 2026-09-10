# Node.js Interview Notes — Day 3: Express.js & Middleware

## 1. What is Express.js?

**Express.js** is a **minimal, unopinionated web framework** for Node.js, built on top of Node's core `http` module.

- It doesn't replace Node's `http` module — it **wraps and extends** it, giving you a much simpler, more structured API for building web servers and APIs.
- Without Express, you'd handle routing, request parsing, and response formatting manually using raw `http.createServer`. Express abstracts all of that into clean, reusable patterns.
- Core things Express gives you out of the box:
  - Simplified **routing** (`app.get()`, `app.post()`, etc.)
  - A **middleware system** (see below — this is the heart of Express)
  - Easier request/response handling (`req.params`, `req.query`, `req.body`, `res.json()`, etc.)
  - Integration point for templating engines, static file serving, error handling, etc.

**Interview soundbite:**
> "Express is a lightweight, unopinionated framework built on top of Node's http module. It doesn't add new capabilities Node doesn't have — it makes the ones Node already has (routing, request handling, middleware) dramatically easier to work with."

---

## 2. Express is All About Middleware

- The **core architectural idea** behind Express is: **everything is middleware.**
- A middleware function is just a function that has access to the **request**, the **response**, and a function to pass control to the **next** middleware in line — `(req, res, next)`.
- Even Express's routing (`app.get`, `app.post`) is really just middleware scoped to a specific method + path.
- Middleware functions are executed **in the order they're defined**, forming a **chain** — each one can:
  - Modify `req` or `res`
  - End the request-response cycle (e.g., `res.send()`, `res.json()`)
  - Pass control to the next middleware via `next()`
  - Or pass an error to Express's error-handling middleware via `next(err)`

**Interview soundbite:**
> "Express's entire architecture is built around middleware — a chain of functions that each get access to the request and response, and choose to either handle it, modify it, or pass it along to the next function in the chain."

---

## 3. How Middleware Works

```js
const express = require('express');
const app = express();

// A simple middleware
app.use((req, res, next) => {
  console.log(`${req.method} ${req.url}`);
  next(); // pass control to the next middleware/route handler
});

app.get('/users', (req, res) => {
  res.json({ users: [] });
});

app.listen(3000);
```

**How it flows:**
1. A request comes in.
2. Express runs it through the middleware **in the order they were registered** (`app.use`, then route-specific handlers).
3. Each middleware **must call `next()`** to pass control forward — otherwise, the request **hangs** (no response is ever sent, and it never reaches the next handler).
4. If a middleware calls `res.send()` / `res.json()` / `res.end()`, the cycle **ends there** — no further middleware runs (unless it's designed to still call `next()`, which is unusual).
5. **Middleware types:**
   - **Application-level** — `app.use(...)`, runs for every request (or a specific path if given)
   - **Router-level** — same idea, but scoped to an `express.Router()` instance
   - **Error-handling** — has **4 parameters**: `(err, req, res, next)` — Express recognizes it as an error handler specifically because of that 4th parameter
   - **Built-in** — e.g., `express.json()` (parses JSON bodies), `express.static()` (serves static files)
   - **Third-party** — e.g., `cors`, `morgan`, `helmet`

**Key gotcha to mention in interviews:**
> "If you forget to call `next()` in a middleware that isn't sending a response, the request will just hang forever — the client never gets a response and the connection times out."

---

## 4. Looking Behind Express.js

Under the hood, Express is doing a few key things on top of raw Node `http`:

- When you call `express()`, it returns an **app** — which is really a request handler function you could pass directly to `http.createServer()`. In fact:
```js
const express = require('express');
const app = express();
// app itself is technically usable as the callback to http.createServer(app)
```
- Express maintains an internal **middleware stack** — essentially an array of registered middleware/route handlers, each tagged with a method + path (or `*` for all).
- When a request comes in, Express walks through this stack **top to bottom**, checking if each entry's method/path matches the incoming request. If it matches, that middleware runs.
- The `next()` function is what tells Express's internal router: *"move to the next matching entry in the stack."*
- Express also enhances the raw `req`/`res` objects Node gives you — adding convenience methods/properties like `req.params`, `req.query`, `req.body` (after parsing middleware), `res.json()`, `res.status()`, etc. — but under the hood, it's still the same Node `http` request/response objects, just extended.

**Interview soundbite:**
> "Express is essentially a request handler function sitting on top of Node's raw http server. Internally it keeps a stack of middleware and route handlers, and for every incoming request, it walks through that stack looking for matches — calling next() is how you tell Express to keep moving down that stack."

---

## 5. Using Express Router

- `express.Router()` lets you create **modular, mountable route handlers** — essentially a mini Express app you can plug into your main app.
- Useful for organizing routes by feature/resource instead of dumping everything into one file.

**Example:**

```js
// userRoutes.js
const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
  res.json({ message: 'Get all users' });
});

router.get('/:id', (req, res) => {
  res.json({ message: `Get user ${req.params.id}` });
});

router.post('/', (req, res) => {
  res.json({ message: 'Create a user' });
});

module.exports = router;
```

```js
// app.js
const express = require('express');
const userRoutes = require('./userRoutes');

const app = express();
app.use(express.json());
app.use('/users', userRoutes); // mount the router at /users

app.listen(3000);
```

**What's happening:**
- `router.get('/:id', ...)` combined with `app.use('/users', userRoutes)` means a request to `/users/5` gets routed correctly — Express **concatenates** the mount path (`/users`) with the router's internal path (`/:id`).
- Routers can also have **their own middleware**, scoped only to routes registered on that router (e.g., an auth check just for `/users/*`).
- This keeps large applications organized: e.g., `userRoutes.js`, `productRoutes.js`, `authRoutes.js`, each mounted separately in `app.js`.

**Interview soundbite:**
> "express.Router() lets you break your routes into separate, self-contained modules that behave like mini Express apps. You mount them onto a path prefix in your main app, which keeps large codebases organized and lets you scope middleware — like authentication — to just a specific group of routes."

---

## Practice Questions & Answers

**Q1: What is Express.js, and how does it relate to Node's core `http` module?**
> A1: Express is a minimal, unopinionated web framework built on top of Node's http module. It doesn't replace http — it wraps it to provide simpler routing, middleware, and request/response handling.

**Q2: What is middleware in Express?**
> A2: A function with access to `req`, `res`, and `next`, that can inspect/modify the request or response, end the cycle by sending a response, or pass control to the next middleware by calling `next()`.

**Q3: What happens if you forget to call `next()` in a middleware?**
> A3: The request hangs — no response is ever sent to the client, and the connection will eventually time out.

**Q4: What distinguishes an error-handling middleware from a regular one?**
> A4: It has **four** parameters instead of three: `(err, req, res, next)`. Express identifies it as an error handler specifically by that signature.

**Q5: Name the different types of middleware in Express.**
> A5: Application-level, router-level, error-handling, built-in (e.g., `express.json()`, `express.static()`), and third-party (e.g., `cors`, `morgan`).

**Q6: How does Express process an incoming request internally?**
> A6: It walks through an internal stack of registered middleware/route handlers, in the order they were defined, checking method + path matches. `next()` tells it to move to the next matching entry in that stack.

**Q7: What is `express.Router()` used for?**
> A7: Creating modular, mountable groups of routes — like a mini Express app — that can be organized by feature/resource and mounted onto a path prefix in the main app, keeping large codebases clean and allowing scoped middleware.

**Q8: If you mount a router with `app.use('/users', userRoutes)` and the router has `router.get('/:id', ...)`, what URL triggers that handler?**
> A8: `/users/:id` — e.g., `/users/5`. Express concatenates the mount path with the router's internal path.

**Q9: Is `express()` itself just a plain object, or something else?**
> A9: It's a request handler function — technically usable directly as the callback passed to `http.createServer()`, since under the hood Express still runs on Node's raw http server.

---

## Quick Reference Table

| Concept | One-liner |
|---|---|
| Express.js | Minimal framework built on top of Node's `http` module |
| Middleware | `(req, res, next)` function — the core building block of Express |
| `next()` | Passes control to the next matching middleware in the stack |
| Error middleware | Identified by 4 params: `(err, req, res, next)` |
| Middleware types | Application, router-level, error-handling, built-in, third-party |
| Behind the scenes | Express = request handler + internal middleware stack, sitting on raw `http` |
| `express.Router()` | Modular, mountable mini-app for organizing routes by feature |