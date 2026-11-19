## Why does my useEffect run twice in dev?

"In React 18+, useEffect runs twice in development because of React.StrictMode.

In development only, React intentionally performs a mount 
→
→ unmount 
→
→ remount cycle. It does this to stress-test our components and verify that we’ve implemented proper cleanup functions for things like timers, subscriptions, event listeners, and API calls.

- This helps catch memory leaks and race conditions before going to production, where it only runs once."

- Don't use hacky fixes: "A common mistake is using a useRef(false) flag to force it to run once in development. That defeats the purpose of StrictMode and hides bugs. The correct solution is always writing proper cleanup code (e.g., using AbortController for fetches or removeEventListener)."
- Production behavior: "It is purely a development-time tool—React completely strips this double-invocation behavior in production builds."

