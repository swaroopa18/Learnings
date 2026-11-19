# React Performance & Hooks – Revision Notes

## 1. Code Splitting vs Lazy Loading

- **Code Splitting:** Divides a large JS bundle into smaller chunks.
- **Lazy Loading:** Loads chunks/components only when needed.
- Dynamic `import()` creates code-splitting points.
- `React.lazy()` + `Suspense` implements lazy loading for React components.

### Code-splitting strategies
1. Route-based – Load pages when navigating.
2. Component-based – Load heavy components when needed.
3. Event-based – Load modules after user actions.

**Remember:** Code splitting creates smaller chunks; lazy loading controls when they load.

## 2. React.memo vs useMemo vs useCallback

| API | Purpose |
|---|---|
| React.memo | Memoizes a component |
| useMemo | Memoizes a calculated value |
| useCallback | Memoizes a function reference |

- `React.memo` skips rendering when props are unchanged (shallow comparison).
- `useMemo` avoids unnecessary recalculations.
- `useCallback` preserves function references.

**Important:** New object/function references can cause memoized children to render again.

## 3. useState – Important Concepts

- State updates are scheduled, not immediately reflected in the current render.
- State is a snapshot of the current render.
- React batches multiple state updates.
- Multiple `setCount(count + 1)` calls use the same captured value.
- Use functional updates for sequential state changes:

```jsx
setCount(prev => prev + 1);
```

- `useState` replaces objects; it doesn't automatically merge them.
- Use spread syntax to preserve existing properties.
- React can skip updates when the new state is identical (`Object.is`).

## 4. useEffect – Important Concepts

| Dependency | Behavior |
|---|---|
| No dependency array | After every committed render |
| `[]` | After mount |
| `[count]` | Mount + when count changes |

- Cleanup runs before the next effect setup when dependencies change.
- Cleanup also runs on unmount.
- Effects don't execute during server rendering.
- Effects should return cleanup functions, not Promises.
- Missing dependencies can cause stale closures.
- React Strict Mode performs an extra effect setup/cleanup cycle in development.

### Stale closure example

```jsx
useEffect(() => {
  const id = setInterval(() => {
    setCount(prev => prev + 1);
  }, 1000);

  return () => clearInterval(id);
}, []);
```

Use functional updates to avoid depending on a stale count value.

## 5. List Virtualization

- Renders only visible list items instead of mounting thousands of DOM elements.
- Reduces DOM nodes and rendering overhead.
- Also called Windowing.

Popular libraries:
- `react-window` – Lightweight list virtualization.
- `@tanstack/react-virtual` – Flexible, headless virtualization.

**Important terms:**
- Viewport – Visible portion of the list.
- Overscan – Extra items rendered outside the viewport.
- Virtualization does not reduce the actual data array.
- Pagination and virtualization are different.

## 6. Moving State Down

- Keep state close to the component that needs it.
- Prevents unrelated parent and sibling components from re-rendering due to that state update.

```jsx
function App() {
  return (
    <>
      <Header />
      <Counter />
      <Footer />
    </>
  );
}
```

Keep counter state inside `Counter`, not `App`.

## 7. Lifting Content Up

- Pass expensive JSX from a parent through `children` or props.
- When the stateful wrapper re-renders, unchanged child elements can retain their identity.
- React can skip rendering that unchanged child subtree.
- Does not necessarily require `React.memo`.

```jsx
function App() {
  return (
    <Parent>
      <SlowComponent />
    </Parent>
  );
}

function Parent({ children }) {
  const [count, setCount] = useState(0);

  return (
    <>
      <button onClick={() => setCount(count + 1)}>
        {count}
      </button>
      {children}
    </>
  );
}
```

**Key:** `App` doesn't re-render when Parent's own state changes, so the children element reference remains stable.

## 8. Parent vs Child Re-rendering

| Scenario | Behavior |
|---|---|
| Parent state changes | Parent re-renders; children may re-render |
| Child state changes | Child re-renders; parent doesn't |
| Parent passes changed props | Child receives new props |
| Parent passes unchanged props to React.memo child | Child can skip rendering |
| Child consumes changed context | Child can re-render independently |

### Important distinction

- `React.memo` – Controls unnecessary child renders caused by parent renders when props are unchanged.
- Moving state down – Limits which components are affected by a state update.
- Lifting content up – Preserves child element identity across wrapper state updates.

---

## Quick Interview Revision

- Code Splitting → Smaller JS chunks.
- Lazy Loading → Load when needed.
- React.memo → Component memoization.
- useMemo → Value memoization.
- useCallback → Function reference memoization.
- useState → State management.
- useEffect → Side effects and synchronization.
- List Virtualization → Fewer mounted DOM nodes.
- Moving State Down → Reduce affected component renders.
- Lifting Content Up → Preserve unchanged child elements.


**With&#x20;**`useEffect`**:**

- Filtering runs synchronously.
- React cannot interrupt the JavaScript filtering operation.
- New user input waits until the main thread is free.

**With&#x20;**`useTransition`**:**

- React can interrupt non-urgent rendering when an urgent update arrives.
- It prioritizes user input.
- It restarts rendering with the latest state.

**Remember:** `useTransition` interrupts React rendering, NOT synchronous JavaScript execution.