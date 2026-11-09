# Observer Pattern --- Complete Notes (Patterns.dev)

Source: https://www.patterns.dev/vanilla/observer-pattern/

These notes explain the Observer Pattern and the related examples
covered in the Patterns.dev article.

------------------------------------------------------------------------

## 1. Introduction: Why the Observer Pattern?

Imagine a stock dashboard displaying Apple's stock price. When a new
price arrives, several parts of the application may need to update:

-   A chart redraws.
-   A watchlist row flashes green or red.
-   A portfolio total is recalculated.
-   An audit log records the new price.

One approach is for the WebSocket handler to call every function
directly. However, then the WebSocket code must know about the chart,
watchlist, portfolio, and audit log. This creates **tight coupling**.

The Observer Pattern provides another approach: the part receiving the
update announces that something changed, and interested parts subscribe
to that announcement.

Two main concepts:

-   **Subject:** Maintains a list of observers and notifies them.
-   **Observers:** Functions or objects interested in receiving
    notifications.

The Subject does not need to know what each observer does.

**Central idea:** one-to-many communication without tightly coupling the
Subject to its observers.

------------------------------------------------------------------------

## 2. The core implementation

A Subject needs three capabilities:

1.  Store observers.
2.  Allow observers to subscribe and unsubscribe.
3.  Notify all registered observers.

``` js
class Subject {
  #observers = new Set();

  subscribe(observer) {
    this.#observers.add(observer);

    return () => this.#observers.delete(observer);
  }

  notify(payload) {
    for (const observer of this.#observers) {
      observer(payload);
    }
  }
}
```

### 2.1 `#observers = new Set()`

``` js
#observers = new Set();
```

-   `observers` stores the functions that want to receive updates.
-   A `Set` stores unique values, so the same function cannot be
    registered twice.
-   `#` declares a private class field. Code outside the class cannot
    access it directly.

For example:

``` js
const subject = new Subject();

// Not allowed: private fields cannot be accessed outside the class.
subject.#observers;
```

A `Set` is useful because it prevents duplicate registrations and
supports removal of a particular observer.

### 2.2 `subscribe(observer)`

``` js
subscribe(observer) {
  this.#observers.add(observer);

  return () => this.#observers.delete(observer);
}
```

This method registers an observer.

``` js
const ticker = new Subject();

function updateChart(data) {
  console.log("Updating chart:", data);
}

const unsubscribe = ticker.subscribe(updateChart);
```

What happens?

1.  `updateChart` is passed to `subscribe()`.
2.  The function is added to the Subject's Set.
3.  `subscribe()` returns a cleanup function.
4.  That returned function is stored in `unsubscribe`.

Calling `unsubscribe()` removes the observer:

``` js
unsubscribe();
```

The returned cleanup function closes over the Subject and removes the
observer from its private Set.

### 2.3 `notify(payload)`

``` js
notify(payload) {
  for (const observer of this.#observers) {
    observer(payload);
  }
}
```

This loops through every registered observer and calls it with the same
payload.

``` js
ticker.notify({
  symbol: "AAPL",
  price: 200
});
```

If three observers are registered, all three receive the object.

The caller only needs to call `notify()`. It does not need to call each
observer individually.

### Remember the methods

  Method                          Responsibility
  ------------------------------- ---------------------------------
  `subscribe()`                   Register an observer
  `notify()`                      Notify all registered observers
  Returned unsubscribe function   Remove one observer

In this implementation, `unsubscribe` is not a Subject method. It is a
function returned by `subscribe()`.

------------------------------------------------------------------------

## 3. Stock ticker example

The article applies the Subject to a stock-price stream.

``` js
const ticker = new Subject();
```

The `ticker` Subject will notify interested parts of the application
whenever a stock-price update arrives.

### 3.1 Chart observer

``` js
const chartQueue = [];
let pending = false;

const drawChart = (tick) => {
  chartQueue.push(tick);

  if (pending) return;

  pending = true;

  requestAnimationFrame(() => {
    renderChart(chartQueue);
    chartQueue.length = 0;
    pending = false;
  });
};
```

What each part does:

-   `chartQueue` temporarily stores incoming stock-price updates.
-   `pending` tracks whether a chart-render operation has already been
    scheduled.
-   `chartQueue.push(tick)` adds the new update to the queue.
-   `if (pending) return` avoids scheduling another render if one is
    already pending.
-   `requestAnimationFrame()` schedules work before the browser's next
    repaint.
-   `renderChart(chartQueue)` renders using the collected updates.
-   `chartQueue.length = 0` clears the queue.
-   `pending = false` allows another render to be scheduled.

**Main idea:** the chart batches rapid updates rather than redrawing
immediately for every individual tick.

### 3.2 Watchlist observer

``` js
const flashRow = ({ symbol, price, previous }) => {
  if (symbol !== "AAPL") return;

  document
    .querySelector('[data-symbol="AAPL"]')
    ?.classList.toggle("up", price > previous);
};
```

Explanation:

-   `({ symbol, price, previous })` uses object destructuring to extract
    properties from the incoming object.
-   `if (symbol !== "AAPL") return` means this observer only cares about
    Apple's stock.
-   `document.querySelector(...)` finds the HTML element for Apple's
    watchlist row.
-   `?.` is optional chaining. If the element does not exist, the code
    does not try to access its `classList`.
-   `classList.toggle("up", price > previous)` adds the `up` class if
    the new price is higher than the previous price; otherwise, it
    removes the class.

### 3.3 Logging observer

``` js
const logTick = (tick) => {
  console.debug("[tick]", tick);
};
```

This observer records each incoming stock-price update in the browser
console.

Each observer has a separate responsibility:

-   `drawChart`: visualizes price updates.
-   `flashRow`: updates the watchlist row.
-   `logTick`: logs the update.

### 3.4 Register the observers

``` js
const unsubChart = ticker.subscribe(drawChart);
const unsubRow = ticker.subscribe(flashRow);
const unsubLog = ticker.subscribe(logTick);
```

All three observers are registered with the same Subject.

Each call returns its own unsubscribe function. This lets the
application remove one observer without removing the others.

### 3.5 Receive updates from a WebSocket

``` js
socket.addEventListener("message", (event) => {
  const tick = JSON.parse(event.data);

  ticker.notify(tick);
});
```

The flow is:

1.  The WebSocket receives a message.
2.  `JSON.parse()` converts the JSON string into a JavaScript object.
3.  `ticker.notify(tick)` broadcasts the object.
4.  Every registered observer receives the update.

The WebSocket handler only needs to notify the Subject. It does not need
to know about the chart, watchlist, or logger.

This separation is called **decoupling**.

------------------------------------------------------------------------

## 4. Browser-native alternative: EventTarget

Browsers provide a built-in event system called `EventTarget`.

You may have used it with DOM elements:

``` js
button.addEventListener("click", handler);
```

It can also be used with custom objects.

``` js
class Ticker extends EventTarget {
  push(tick) {
    this.dispatchEvent(
      new CustomEvent("tick", {
        detail: tick
      })
    );
  }
}
```

### 4.1 `extends EventTarget`

``` js
class Ticker extends EventTarget
```

The `Ticker` class inherits from `EventTarget`, so instances get methods
such as:

-   `addEventListener()`
-   `removeEventListener()`
-   `dispatchEvent()`

### 4.2 Dispatch a custom event

``` js
push(tick) {
  this.dispatchEvent(
    new CustomEvent("tick", {
      detail: tick
    })
  );
}
```

This creates and dispatches a custom event named `"tick"`.

The `detail` property carries the stock-price data.

``` js
ticker.push({
  symbol: "AAPL",
  price: 200
});
```

### 4.3 Listen for the event

``` js
const ticker = new Ticker();

ticker.addEventListener("tick", (event) => {
  drawChart(event.detail);
});

ticker.addEventListener("tick", (event) => {
  flashRow(event.detail);
});
```

-   `"tick"` is the event name.
-   `event` is the event object.
-   `event.detail` contains the data passed to `CustomEvent`.

Both listeners receive the event.

### Custom Subject vs EventTarget

  -----------------------------------------------------------------------
  Custom Subject                      EventTarget
  ----------------------------------- -----------------------------------
  We maintain our own Set.            The browser maintains listeners.

  We write `subscribe()`.             We use `addEventListener()`.

  We write `notify()`.                We use `dispatchEvent()`.

  We implement cleanup.               We can use built-in listener
                                      cleanup options.
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 5. AbortSignal integration

If a component registers many event listeners, it needs to remove them
when it is no longer needed.

Calling `removeEventListener()` separately for every listener can become
repetitive.

`AbortController` provides a convenient way to clean up multiple
listeners together.

``` js
const controller = new AbortController();
const { signal } = controller;

ticker.addEventListener("tick", drawChart, { signal });
ticker.addEventListener("tick", flashRow, { signal });
ticker.addEventListener("tick", logTick, { signal });
```

### 5.1 Create an AbortController

``` js
const controller = new AbortController();
```

This creates a controller that can cancel operations associated with its
signal.

### 5.2 Get its signal

``` js
const { signal } = controller;
```

The signal is passed to APIs that support cancellation.

### 5.3 Associate listeners with the signal

``` js
ticker.addEventListener("tick", drawChart, { signal });
```

This registers the listener and associates it with the signal.

The same signal can be used for multiple listeners.

### 5.4 Remove all associated listeners

``` js
controller.abort();
```

Calling `abort()` removes all event listeners registered with that
signal.

Instead of:

``` js
ticker.removeEventListener("tick", drawChart);
ticker.removeEventListener("tick", flashRow);
ticker.removeEventListener("tick", logTick);
```

You can use:

``` js
controller.abort();
```

This is especially useful when a dashboard component is destroyed or
unmounted. Its listeners can be cleaned up together.

------------------------------------------------------------------------

## 6. Observer Pattern vs Pub/Sub

Observer and Publish/Subscribe (Pub/Sub) are related patterns, but they
have different communication structures.

### 6.1 Observer Pattern

-   A Subject maintains its observers.
-   Observers register directly with that Subject.
-   The Subject notifies its observers.

Example:

``` js
ticker.notify({
  symbol: "AAPL",
  price: 200
});
```

All observers registered with `ticker` receive the notification.

### 6.2 Pub/Sub Pattern

Pub/Sub usually uses an intermediary such as an Event Bus or Message
Broker.

The publisher does not directly communicate with subscribers.

The flow is:

1.  Publisher publishes a message.
2.  Event Bus receives it.
3.  Event Bus routes it based on the topic.
4.  Subscribers listening to that topic receive it.

Example:

``` js
bus.publish("ticks/AAPL", {
  price: 200
});
```

A subscriber can listen to a specific topic:

``` js
bus.subscribe("ticks/AAPL", handler);
```

Another subscriber might listen to:

``` js
bus.subscribe("ticks/GOOGL", handler);
```

Each subscriber receives messages for its chosen topic.

### 6.3 Main differences

  -----------------------------------------------------------------------
  Concept                 Observer                Pub/Sub
  ----------------------- ----------------------- -----------------------
  Communication           Direct                  Through a broker

  Connection              Subject and observer    Publisher and
                                                  subscriber

  Routing                 Subject notifies its    Topics or channels
                          observers               

  Typical usage           Object-state            Communication across
                          notifications           modules
  -----------------------------------------------------------------------

A simple way to remember:

-   **Observer:** "I'm watching this particular object."
-   **Pub/Sub:** "I'm interested in messages published under this
    topic."

### 6.4 EventBus implementation using EventTarget

``` js
class EventBus {
  #target = new EventTarget();

  publish(topic, data) {
    this.#target.dispatchEvent(
      new CustomEvent(topic, { detail: data })
    );
  }

  subscribe(topic, handler, { signal } = {}) {
    const listener = (event) => handler(event.detail);

    this.#target.addEventListener(topic, listener, { signal });

    return () =>
      this.#target.removeEventListener(topic, listener);
  }
}
```

Explanation:

**`#target = new EventTarget()`**

Creates a private EventTarget instance. It acts as the internal event
broker.

**`publish(topic, data)`**

Creates and dispatches a custom event whose name is the topic.

``` js
bus.publish("user:login", {
  name: "John"
});
```

**`subscribe(topic, handler, { signal } = {})`**

Registers a listener for a particular topic.

``` js
bus.subscribe("user:login", (data) => {
  console.log(data.name);
});
```

The internal `listener` extracts `event.detail`, so the subscriber
receives the actual data rather than the complete event object.

The returned function removes that listener. The optional `signal` also
allows cleanup using an AbortController.

The key distinction is that this EventBus supports multiple event
topics, while the basic Subject broadcasts one type of update to all its
observers.

------------------------------------------------------------------------

## 7. Modern variants

The article introduces three modern approaches related to the Observer
Pattern:

1.  Async Iterators
2.  Reactive Signals
3.  RxJS

### 7.1 Async Iterators

An iterator lets us access a sequence of values one at a time.

An **async iterator** does something similar, but it can wait for
asynchronous data.

Example:

``` js
async function* watchTicks(socket, { signal }) {
  while (!signal.aborted) {
    const message = await new Promise((resolve, reject) => {
      socket.addEventListener("message", resolve, {
        once: true,
        signal
      });

      socket.addEventListener("error", reject, {
        once: true,
        signal
      });
    });

    yield JSON.parse(message.data);
  }
}
```

Important parts:

**`async function*`**

Defines an asynchronous generator function. It can produce multiple
values over time.

**`while (!signal.aborted)`**

Continues listening as long as the operation has not been cancelled.

**`await new Promise(...)`**

Waits until a WebSocket message arrives or an error occurs. The function
pauses without blocking the entire JavaScript application.

**`{ once: true, signal }`**

-   `once: true` removes the event listener after it fires.
-   `signal` allows cancellation using AbortController.

**`yield`**

``` js
yield JSON.parse(message.data);
```

Produces one stock-price update for the consumer. Unlike `return`,
`yield` pauses the generator so it can produce another value later.

#### Consume the async generator

``` js
const controller = new AbortController();

for await (const tick of watchTicks(socket, {
  signal: controller.signal
})) {
  drawChart(tick);
}
```

-   `for await...of` reads values from the asynchronous generator.
-   Each incoming stock tick is passed to `drawChart()`.
-   The loop continues until the operation is aborted.

Stop it with:

``` js
controller.abort();
```

**Why use Async Iterators?**

They let you handle event streams in a sequential, readable style
instead of manually managing callbacks.

### 7.2 Reactive Signals

Reactive signals are another modern approach related to Observer.

Libraries such as Preact, Solid, Angular, and Vue provide reactive
mechanisms that can automatically track dependencies.

Example using Preact Signals:

``` js
import {
  signal,
  computed,
  effect
} from "@preact/signals-core";

const price = signal(100);
const quantity = signal(2);

const total = computed(() =>
  price.value * quantity.value
);

effect(() =>
  console.log(`Total: $${total.value}`)
);
```

There are three important concepts.

#### 1. `signal()`

``` js
const price = signal(100);
const quantity = signal(2);
```

A signal stores a value that can change over time.

Initially:

-   Price = 100
-   Quantity = 2

#### 2. `computed()`

``` js
const total = computed(() =>
  price.value * quantity.value
);
```

Creates a derived value.

Initially:

``` text
100 × 2 = 200
```

The total automatically updates when its dependencies change.

#### 3. `effect()`

``` js
effect(() =>
  console.log(`Total: $${total.value}`)
);
```

Runs the function and tracks the reactive values it reads.

When the total changes, the effect runs again.

For example:

``` js
price.value = 110;
```

The total becomes:

``` text
110 × 2 = 220
```

The effect prints:

``` text
Total: $220
```

Then:

``` js
quantity.value = 3;
```

The total becomes:

``` text
110 × 3 = 330
```

The effect prints:

``` text
Total: $330
```

**How is this related to Observer?**

-   Signal: reactive source of data, similar to a Subject.
-   Effect: reacts to changes, similar to an Observer.
-   Changing the signal: updates the source.
-   Running the effect: notification and reaction.

The subscription and dependency tracking happen automatically behind the
scenes.

### 7.3 RxJS for stream composition

RxJS is a JavaScript library for working with streams of asynchronous
events.

Consider a search box. A user types:

``` text
J
Ja
Jav
Java
```

If the application sends an API request for every keystroke, it may make
unnecessary requests.

We can improve this by:

1.  Waiting until the user stops typing.
2.  Ignoring repeated search values.
3.  Switching to the latest search when a new one arrives.

Example:

``` js
import {
  fromEvent,
  switchMap,
  debounceTime,
  distinctUntilChanged,
  map
} from "rxjs";

const input = document.querySelector("#search");

fromEvent(input, "input").pipe(
  map((e) => e.target.value.trim()),

  debounceTime(250),

  distinctUntilChanged(),

  switchMap((q) =>
    q
      ? fetch(`/api/search?q=${encodeURIComponent(q)}`)
          .then((r) => r.json())
      : []
  )
).subscribe(renderResults);
```

#### 1. `fromEvent()`

``` js
fromEvent(input, "input")
```

Converts input events from the search box into an observable stream.

Every time the user types, a new event enters the stream.

#### 2. `pipe()`

``` js
.pipe(...)
```

Allows us to chain operations that transform or control the stream.

Think of it as a processing pipeline.

#### 3. `map()`

``` js
map((e) => e.target.value.trim())
```

Extracts the input value and removes whitespace from the beginning and
end.

Example:

``` text
" JavaScript " → "JavaScript"
```

#### 4. `debounceTime(250)`

Waits until 250 milliseconds have passed without another input event.

Instead of making four requests for `J`, `Ja`, `Jav`, and `Java`, it
waits until the user stops typing for 250 ms and then continues with the
latest value.

#### 5. `distinctUntilChanged()`

Prevents consecutive duplicate values from continuing through the
pipeline.

For example:

``` text
Java
Java
JavaScript
```

The second consecutive `Java` is ignored.

#### 6. `switchMap()`

Starts a new inner operation whenever a new search value arrives.

If a previous search is still in progress, `switchMap` unsubscribes from
the previous inner operation and switches to the latest one.

For example:

-   User searches for `Java`.
-   An API request starts.
-   Before it finishes, the user searches for `JavaScript`.
-   The previous operation is unsubscribed from the observable pipeline.
-   The latest search becomes active.

**Important technical detail:** Unsubscribing from a normal Promise does
not physically cancel the underlying HTTP request. RxJS can cancel the
previous subscription, but to abort the actual fetch request, use an
AbortController.

#### 7. `subscribe()`

``` js
.subscribe(renderResults);
```

Receives the final search results and passes them to `renderResults`.

**Why use RxJS?**

When event flows become complicated, manually combining, delaying,
filtering, and switching events becomes difficult. RxJS provides
operators to make this processing more declarative.

------------------------------------------------------------------------

## 8. Common pitfalls

The article discusses four mistakes developers should avoid.

### 8.1 Memory leaks from forgotten subscriptions

Imagine a component subscribes to a Subject:

``` js
ticker.subscribe(updateChart);
```

Later, the component is removed from the screen, but the Subject still
holds a reference to `updateChart`.

The function and objects it references may remain in memory because the
Subject still references them.

Solutions include:

**Use AbortSignal:**

``` js
const controller = new AbortController();

ticker.addEventListener("tick", updateChart, {
  signal: controller.signal
});

// When the component is removed:
controller.abort();
```

**Use an unsubscribe function:**

``` js
const unsubscribe = ticker.subscribe(updateChart);

// When finished:
unsubscribe();
```

**Use framework lifecycle cleanup:**

-   React: `useEffect` cleanup.
-   Vue: `onScopeDispose`.
-   Svelte: `onDestroy`.

Subscriptions should be cleaned up when they are no longer needed.

### 8.2 Notification order assumptions

Suppose:

``` js
ticker.subscribe(observerA);
ticker.subscribe(observerB);
ticker.subscribe(observerC);
```

Observers are generally called in subscription order.

However, if `observerB` depends on `observerA` completing its work
first, that creates a dependency between observers.

The Observer Pattern is not designed to coordinate such dependencies.

If one operation must happen after another, explicitly coordinate their
execution rather than relying on observer order.

### 8.3 Synchronous notification storms

Consider:

``` js
notify(payload) {
  for (const observer of this.#observers) {
    observer(payload);
  }
}
```

This calls observers synchronously.

If:

-   Observer A takes 200 ms.
-   Observer B takes 100 ms.
-   Observer C takes 50 ms.

Observer B cannot start until A finishes, and C cannot start until B
finishes.

This can cause performance problems, especially when updates arrive
frequently.

Possible techniques include:

-   Batching updates.
-   Using `queueMicrotask()`.
-   Using `setTimeout()`.

The goal is to avoid doing expensive work immediately for every
notification.

### 8.4 Re-entrant notifications

An observer may call `notify()` again on the same Subject.

``` js
const subject = new Subject();

subject.subscribe(() => {
  console.log("Observer called");

  subject.notify();
});

subject.notify();
```

What happens?

1.  `notify()` calls the observer.
2.  The observer calls `notify()` again.
3.  The observer gets called again.
4.  It calls `notify()` again.
5.  The process continues recursively.

This can eventually cause a stack overflow.

This is called a **re-entrant notification problem**.

A possible solution is to queue notifications instead of dispatching
them immediately.

------------------------------------------------------------------------

## 9. When NOT to use Observer

Design patterns should not be used everywhere. The article explains
three situations where Observer may not be the best choice.

### 9.1 When you only need a one-time result

Example:

``` js
const result = await fetch("/api/users");
```

You want the result of one asynchronous operation.

You do not need a Subject with multiple subscribers.

A Promise is a better solution.

Remember:

-   **Promise:** One eventual result.
-   **Observer:** Repeated notifications over time.

### 9.2 When Subject and Observer always live together

Imagine you have one object and exactly one function that needs its
data.

You could simply call:

``` js
cart.updateUI();
```

Creating a complete Subject and observer system would add unnecessary
complexity.

A direct method call is simpler.

### 9.3 When you need request/response communication

Example:

``` js
const result = calculateTotal(cart);
```

You call a function and expect an answer.

Observer is generally designed for notifying interested parties, not
returning a response to the caller.

For request/response communication, consider:

-   Regular function calls.
-   Promises.
-   Command buses, when appropriate.

------------------------------------------------------------------------

## 10. Complete overview

The article's concepts can be summarized as follows.

### Observer Pattern ecosystem

  -----------------------------------------------------------------------
  Concept                             Purpose
  ----------------------------------- -----------------------------------
  Basic Subject                       Stores observers and notifies them

  EventTarget                         Browser-native event notification

  Pub/Sub                             Event bus and topic-based
                                      communication

  Async Iterators                     Consume asynchronous events
                                      sequentially

  Reactive Signals                    Automatically track dependencies
                                      and react to changes

  RxJS                                Transform and compose event streams
  -----------------------------------------------------------------------

### Things to watch out for

-   Memory leaks from forgotten subscriptions.
-   Dependencies on notification order.
-   Synchronous performance problems.
-   Recursive or re-entrant notifications.

### When not to use it

  Situation                      Simpler alternative
  ------------------------------ -----------------------------------
  One-time asynchronous result   Promise
  Simple direct communication    Function or method call
  Request/response               Function, Promise, or command bus

------------------------------------------------------------------------

## 11. The main idea to remember

The Observer Pattern is about **one-to-many communication without tight
coupling**.

Instead of a Subject explicitly calling every feature that needs
updating, those features subscribe to the Subject. When a change occurs,
the Subject notifies them.

Remember this sequence:

**Subscribe → Change → Notify → React**

1.  **Subscribe:** Register your interest.
2.  **Change:** The Subject's data or state changes.
3.  **Notify:** The Subject informs its observers.
4.  **React:** Each observer handles the update independently.

### Recommended learning order

If you are learning this for the first time, study the concepts in this
order:

1.  Understand `Subject`, `subscribe()`, `notify()`, and unsubscribe.
2.  Follow the stock ticker example.
3.  Understand `EventTarget` and `AbortController`.
4.  Learn the difference between Observer and Pub/Sub.
5.  Explore Async Iterators, Signals, and RxJS.
6.  Understand the pitfalls and when not to use Observer.

You do not need to memorize every modern variant immediately. First
become comfortable with the basic Subject and Observer relationship.
Once that is clear, the other concepts become much easier.

------------------------------------------------------------------------

## Source

[Patterns.dev --- Observer
Pattern](https://www.patterns.dev/vanilla/observer-pattern/)
