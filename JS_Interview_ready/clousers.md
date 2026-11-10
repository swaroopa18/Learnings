# JavaScript Closures – 10 Important Points

## 1. What is a Closure?
A closure is created when an inner function remembers and accesses variables from its outer function's scope, even after the outer function has finished executing.

```javascript
function outer() {
  let name = "John";

  function inner() {
    console.log(name);
  }

  return inner;
}

const result = outer();
result(); // John
```

**Remember:** A closure gives a function access to its outer lexical scope.

## 2. Closures Remember Their Lexical Environment

A function remembers the variables that were available in its lexical scope when it was created.

```javascript
function outer() {
  let count = 10;

  return function inner() {
    console.log(count);
  };
}

const fn = outer();
fn(); // 10
```

## 3. Closure Can Maintain Private Variables

Closures help create private variables that cannot be directly accessed from outside.

```javascript
function counter() {
  let count = 0;

  return function () {
    count++;
    return count;
  };
}

const increment = counter();

console.log(increment()); // 1
console.log(increment()); // 2
console.log(increment()); // 3
```

**Important:** `count` cannot be directly accessed from outside the counter function.

## 4. Closure Maintains State Between Function Calls

The inner function remembers the updated value of the outer variable.

```javascript
function createCounter() {
  let count = 0;

  return () => ++count;
}

const counter = createCounter();

counter(); // 1
counter(); // 2
counter(); // 3
```

The value is not reset because the closure maintains access to the same variable.

## 5. Closure with setTimeout (var vs let)

This is a very common interview question.

```javascript
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}

// Output:
// 3
// 3
// 3
```

**Why?**
- `var` is function-scoped.
- All callbacks share the same variable `i`.
- The loop finishes before callbacks execute.

Using `let`:

```javascript
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}

// Output:
// 0
// 1
// 2
```

`let` creates a separate binding for each loop iteration.

## 6. IIFE (Immediately Invoked Function Expression)

IIFE is a function that executes immediately after it is created.

It was commonly used to create private scope and solve closure problems.

```javascript
for (var i = 0; i < 3; i++) {
  (function (j) {
    setTimeout(() => console.log(j), 100);
  })(i);
}

// Output:
// 0
// 1
// 2
```

Each function invocation receives its own `j` value.

## 7. Closures Are Used in Memoization

Memoization stores previously calculated results to avoid repeated calculations.

```javascript
function memoize(fn) {
  const cache = new Map();

  return (...args) => {
    const key = JSON.stringify(args);

    if (cache.has(key)) {
      return cache.get(key);
    }

    const result = fn(...args);
    cache.set(key, result);

    return result;
  };
}
```

**Why closure?**

The returned function remembers the `cache` variable even after `memoize()` finishes executing.

## 8. Multiple Closures Have Separate Environments

Each function invocation gets its own lexical environment.

```javascript
function counter() {
  let count = 0;

  return function () {
    return ++count;
  };
}

const counter1 = counter();
const counter2 = counter();

console.log(counter1()); // 1
console.log(counter1()); // 2

console.log(counter2()); // 1
console.log(counter2()); // 2
```

**Why?** Each call to `counter()` creates a separate `count` variable.

## 9. Closures Can Cause Memory Issues

Closures can keep references to variables alive as long as the closure remains reachable.

```javascript
function outer() {
  const largeData = new Array(1000000).fill("data");

  return function inner() {
    console.log(largeData.length);
  };
}

const fn = outer();
```

Here, `largeData` remains reachable through `fn`.

**Remember:** Closures do not automatically cause memory leaks, but unnecessarily retaining references can increase memory usage.

## 10. Closure Uses Lexical Scope (Not Dynamic Scope)

JavaScript uses lexical scoping, meaning variable access is determined by where a function is defined, not where it is called.

```javascript
let name = "Global";

function outer() {
  let name = "Outer";

  return function inner() {
    console.log(name);
  };
}

const fn = outer();

function another() {
  let name = "Another";
  fn();
}

another(); // Outer
```

The output is `Outer` because `inner()` was defined inside `outer()`.

---

# Quick Interview Revision

| Concept | Important Point |
|---|---|
| Closure | Inner function remembers outer scope |
| Lexical scope | Scope depends on where function is defined |
| Private variables | Closures help hide internal state |
| State persistence | Variables survive outer function execution |
| setTimeout | Understand `var` vs `let` |
| IIFE | Immediately invoked function expression |
| Memoization | Cache results using closures |
| Separate closures | Each invocation has its own environment |
| Memory | Unnecessary references can retain memory |
| Scope chain | Inner functions can access outer scopes |

## Most Important Interview Definition

"A closure is a combination of a function and its lexical environment. It allows a function to access variables from its outer scope even after the outer function has completed execution."

**Interview tip:** Focus especially on points 1, 3, 5, 6, 7 and 10. These are particularly useful for JavaScript interviews.