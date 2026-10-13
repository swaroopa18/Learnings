"""
================================================================================
 PROBLEM: Factorial of a Number (Classic Recursion / Memoization)
================================================================================
Given a non-negative integer `n`, return `n!` (n factorial), defined as:

    n! = n * (n-1) * (n-2) * ... * 2 * 1,      with 0! = 1 and 1! = 1

Example: factorial(5) = 5 * 4 * 3 * 2 * 1 = 120

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Can `n` be 0? (Yes — 0! = 1 by definition. This is the #1 base-case bug:
  a base case of only `n == 1` makes factorial(0) recurse forever / blow the
  stack.)
- Can `n` be negative? (Factorial is undefined for negatives — clarify whether
  to raise an error or assume the input is always >= 0.)
- How large can `n` get? (Decides the approach: Python ints never overflow, but
  recursion depth is ~1000 by default, so a big `n` needs an iterative solution
  or a raised recursion limit. In Java/C++ the result overflows long past 20!.)
- Will the function be called many times? (If yes, memoization / caching
  across calls pays off. If it is called once, plain iteration is enough.)

"""

# ================================================================================
# 🔑🔑🔑  STRONG POINTS FOR "RECURSION / MEMOIZATION" PROBLEMS  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   RECURSION = BASE CASE + RECURSIVE CASE (smaller subproblem).      │
    │   factorial(n) = n * factorial(n - 1), stop at the base case.       │
    │   MEMOIZATION = remember answers already computed so repeated       │
    │   calls become O(1) lookups instead of re-doing the whole chain.    │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

Factorial is the "hello world" of recursion. It teaches the exact template
reused in Fibonacci, Climbing Stairs, Power(x, n), and every DP problem.
Key ideas:

1. **Every recursion needs a correct BASE CASE.** The base case is where the
   chain stops. For factorial it is `n <= 1 -> 1` (covers BOTH 0! and 1!).
   Using only `n == 1` silently breaks for n = 0.

2. **The recursive case must move toward the base case.** `n - 1` shrinks the
   problem each step, so we always reach the base case (for n >= 0).

3. **Each call waits on the next => the CALL STACK grows to depth n.**
   Space is O(n) for recursion, and Python's default limit (~1000 frames)
   raises RecursionError for large n.

4. **Memoization only helps across MULTIPLE calls here.** A single
   factorial(n) has no overlapping subproblems (each value is needed exactly
   once), so the memo does not speed up one call — it speeds up the NEXT ones
   (factorial(10) after factorial(8) needs just 2 new multiplications).

5. **A class-level / global memo is SHARED state.** It persists across all
   instances and calls — great for caching, but a classic source of bugs
   if the cached values can ever be wrong or mutated.
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea
5! is just 5 * 4!, and 4! is just 4 * 3!, and so on, until we hit 1! = 1.
So: "factorial of n = n times factorial of (n - 1)". A function that calls
ITSELF on a smaller input is recursion.

### The key insight: trust the smaller problem
You do not need to know HOW factorial(n-1) works — just trust it returns the
right answer, then multiply by n. The base case is the one answer you know
directly, which makes the whole chain collapse into a real number.

### Step-by-step trace: factorial(4)
```
factorial(4)
 └─ 4 * factorial(3)
          └─ 3 * factorial(2)
                   └─ 2 * factorial(1)
                            └─ returns 1          <- base case
                   returns 2 * 1   = 2
          returns 3 * 2   = 6
 returns 4 * 6   = 24 ✅
```

### Memoized trace (cache survives between calls)
```
call factorial(4): memo = {1:1, 2:2}
   4 not in memo -> need factorial(3)
   3 not in memo -> need factorial(2)
   2 IS in memo  -> return 2           (no further recursion!)
   memo[3] = 3 * 2 = 6
   memo[4] = 4 * 6 = 24                memo = {1:1, 2:2, 3:6, 4:24}
call factorial(5): 5 not in memo -> needs factorial(4) -> cache HIT (24)
   memo[5] = 5 * 24 = 120              only ONE new multiplication ✅
```

### The "aha" moment to remember 🎯
"Recursion = base case + shrink the problem. Memoization = store results so
you never compute the same thing twice." Same two ideas power Fibonacci,
Climbing Stairs and all of Dynamic Programming.
"""

# ================================================================================
# ALTERNATIVE APPROACH 1 — Plain Recursion (your first version)
# ================================================================================
"""
### Thought Process 🧠
Directly translate the math definition: n! = n * (n-1)!, with base case 1.
Each call multiplies `n` by the result of the call for `n - 1`.

### Complexity
- TC: O(n) — one multiplication per level, n levels
- SC: O(n) — call stack holds n frames at the deepest point

### Pros
- Shortest, most readable code; mirrors the mathematical definition 1:1.
- No extra data structures.

### Cons
- BUG for n = 0: base case is only `n == 1`, so factorial(0) calls
  factorial(-1), factorial(-2), ... until RecursionError.
- O(n) stack space; Python fails around n ~ 1000 (RecursionError).
- Recomputes everything from scratch on every call — no reuse.

### Bottleneck
No caching between calls and stack depth grows with n. Ask: "have I computed
this before?" -> memoization. "Do I need the stack at all?" -> iteration.
"""


class SolutionRecursive:
    def factorial(self, n: int) -> int:
        if n == 1:
            return 1
        return n * self.factorial(n - 1)


# ================================================================================
# ALTERNATIVE APPROACH 2 — Iterative Loop (no recursion)
# ================================================================================
"""
### Thought Process 🧠
Multiply 2 * 3 * ... * n in a simple loop, keeping a running product. This is
exactly what the recursion computes, but without the call stack.

### Complexity
- TC: O(n) — n - 1 multiplications
- SC: O(1) — a single running `result` variable

### Pros
- O(1) space, no RecursionError, safe for large n.
- Handles n = 0 and n = 1 naturally (the loop body never runs -> returns 1).
- Fastest in practice (no function-call overhead).

### Cons
- Does not reuse work between calls (every call recomputes from scratch)
  unless you add a cache on top.
- Teaches less about recursion/DP, so interviewers may still ask for the
  recursive version.

### DSA Buddy Point 🧠
"Any tail-style recursion can be turned into a loop. If recursion depth is the
risk, convert to iteration — same complexity, O(1) space."
"""


def factorial_iterative(n: int) -> int:
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


# ================================================================================
# MY APPROACH — Memoized Recursion (cache shared across calls)
# ================================================================================
"""
### Idea
Keep a dictionary `memo` mapping n -> n!. Before recursing, check if the answer
is already cached and return it immediately. Otherwise compute it from
factorial(n - 1), STORE it, and return it. Seeding the cache with
{1: 1, 2: 2} gives the recursion known answers to stop at.

### Complexity
- TC: O(n) for the FIRST call that fills the cache up to n;
      O(1) for any later call with n already cached
      (amortized: only the "new" part beyond the largest cached n costs work)
- SC: O(n) — memo dictionary + recursion stack of depth up to n

### Pros
- Repeated / increasing calls are extremely cheap (cache hits).
- Keeps the clean recursive structure while adding reuse.
- Seeded base cases {1:1, 2:2} stop the recursion early.

### Cons
- A single isolated call is NOT faster than plain recursion (no overlapping
  subproblems) — it just adds dictionary overhead and O(n) extra memory.
- `memo` is a CLASS-LEVEL mutable dict: shared by every instance, never
  cleared, and grows forever (memory leak for huge / many distinct n).
- Still O(n) recursion depth -> RecursionError for large n on a COLD cache.
- BUG for n = 0 (and negatives): 0 is not in the memo, so it recurses into
  factorial(-1), factorial(-2), ... forever.

### DSA Buddy Point 🧠
"Memoization pays off when subproblems OVERLAP or when the same function is
called many times. For one-shot factorial the win is only across calls."

### What can be improved?
Complexity-wise nothing — O(n) is optimal for computing n! from scratch.
Two small fixes: (1) seed the memo with `{0: 1, 1: 1}` (or add a base case
`if n <= 1: return 1`) so n = 0 works; (2) a class-level `memo = {...}` is
shared state — fine for this exercise, but use `self.memo` set in `__init__`
(or `functools.lru_cache`) if you want per-instance caches. The fixed version
is the one below.
"""


class Solution:
    memo = {0: 1, 1: 1}  # 0! = 1 and 1! = 1 (fixes the n = 0 bug)

    def factorial(self, n: int) -> int:
        if n in self.memo:
            return self.memo[n]
        self.memo[n] = n * self.factorial(n - 1)
        return self.memo[n]


# ================================================================================
# ALTERNATIVE APPROACH 3 — functools.lru_cache (Pythonic memoization)
# ================================================================================
"""
### Thought Process 🧠
Let the standard library handle the cache. Decorate the plain recursive
function with `@lru_cache(maxsize=None)`; Python stores results keyed by `n`
automatically. (In real code, `math.factorial(n)` is the one-liner answer.)

### Complexity
- TC: O(n) first call, O(1) for cached calls
- SC: O(n) — cache + recursion stack

### Pros
- Zero manual cache bookkeeping — hard to get wrong.
- Same recursive structure as the plain version, plus reuse.

### Cons
- Still O(n) recursion depth (RecursionError for large n).
- `maxsize=None` means the cache is unbounded.
- Hides the mechanism — interviewers usually want you to write the dict
  version once to show you understand it.

### DSA Buddy Point 🧠
"@lru_cache == automatic memo dict. Know the manual version first, then use
the decorator in production."
"""

from functools import lru_cache


@lru_cache(maxsize=None)
def factorial_lru(n: int) -> int:
    if n <= 1:
        return 1
    return n * factorial_lru(n - 1)


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
FACTORIAL (n!)
│
├── Plain Recursion
│   └── n * factorial(n - 1), base case -> O(n) time, O(n) stack
│
├── Bottleneck
│   └── No reuse between calls + stack depth grows with n
│       (and base case `n == 1` breaks for n = 0)
│
├── Key Insight
│   └── Base case + shrink the problem; cache results so repeated work
│       becomes an O(1) lookup
│
├── Iterative Loop
│   └── running product 2..n -> O(n) time, O(1) space, no recursion limit
│
├── My Approach — Memoized Recursion (cache across calls)
│   └── memo = {0:1, 1:1}; check memo -> else compute, store, return
│       -> O(n) first call, O(1) cached; O(n) space
│
└── lru_cache / math.factorial
    └── Library does the caching (or the whole job) -> same complexity,
        least code
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Every recursive function needs a base case that is REACHED. For factorial
  use `n <= 1` (or seed the memo with 0 and 1) so n = 0 does not recurse
  forever."
- "Recursion depth = n, so space is O(n) and Python raises RecursionError
  around n ~ 1000. If n can be large, use the iterative version."
- "Memoization helps ACROSS calls, not within a single factorial(n) call —
  there are no overlapping subproblems in a straight chain."
- "A class-level `memo = {...}` is shared by all instances and never cleared.
  Convenient, but be aware it is global-like mutable state."
- "Python ints never overflow, so factorial(n) is always exact — but the
  numbers get huge (100! has 158 digits). In Java/C++ the result overflows a
  64-bit long past 20!."
- "Same two ideas — base case + smaller subproblem, plus caching — are the
  foundation of Fibonacci, Climbing Stairs and all Dynamic Programming."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                | Core Idea                                    | TC                         | SC   | Pros                                   | Cons                                                | When to Use                      |
|-------------------------|----------------------------------------------|----------------------------|------|----------------------------------------|-----------------------------------------------------|----------------------------------|
| Plain Recursion         | n * factorial(n-1), base case n == 1         | O(n)                       | O(n) | Simplest, mirrors the math definition  | n=0 bug, stack depth n, no reuse across calls       | Teaching / first solution        |
| Iterative Loop          | Running product 2..n                         | O(n)                       | O(1) | No stack limit, fastest, handles n=0   | No cross-call reuse, less "recursive" insight       | Large n / production, single call|
| Memoized Recursion      | Dict cache of n -> n!, seeded {0:1, 1:1}     | O(n) first, O(1) cached    | O(n) | Fast repeated calls, keeps recursion   | Shared mutable memo, stack depth n, extra memory    | Many calls (your code)           |
| lru_cache Recursion     | Decorator caches results automatically       | O(n) first, O(1) cached    | O(n) | Least code, no manual bookkeeping      | Unbounded cache, still O(n) recursion depth         | Pythonic memoization             |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Recursion (base case + smaller subproblem) with optional
  memoization — same family as Fibonacci (LC 509), Climbing Stairs (LC 70),
  Pow(x, n) (LC 50) and the top-down DP template.
- Go-to answer: "factorial(n) = n * factorial(n-1) with base case n <= 1.
  That is O(n) time and O(n) stack. For repeated calls I add a memo dict so
  cached results return in O(1). For very large n I switch to a loop to get
  O(1) space and avoid RecursionError."
- Good to call out: the n = 0 base case, recursion-depth limits in Python,
  and that memoization only helps across calls (no overlapping subproblems
  within one call).
- Common follow-up: "Can you avoid recursion?" -> iterative loop, O(1) space.
  "What about huge n / overflow?" -> Python big ints are exact; in Java use
  BigInteger and note long overflows past 20!. "Trailing zeros of n!?" ->
  count factors of 5: n//5 + n//25 + n//125 + ... (LC 172).
"""