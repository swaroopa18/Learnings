"""
================================================================================
 PROBLEM: Sqrt(x) (LeetCode 69)
================================================================================
Given: a non-negative integer `x`.
Task: return the integer square root of x — i.e. floor(sqrt(x)), the
largest integer `r` such that `r * r <= x`. (Decimal digits are truncated;
you may NOT use built-in power/sqrt operators as the "intended" solution,
though Python's math.isqrt exists as a real-world shortcut.)

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Is x guaranteed non-negative? (Yes per constraints — negative sqrt is
  undefined for this problem)
- Should the result be floored, not rounded? (Yes — sqrt(8) = 2, not 3,
  even though 2.828 rounds to 3)
- Are built-in functions like `math.sqrt` or `x ** 0.5` allowed? (Often
  explicitly disallowed in the problem statement, since floating-point
  sqrt can have precision errors near perfect squares — the point of the
  exercise is usually to implement it manually)
"""

# ================================================================================
# MY APPROACH — Binary Search on the Answer
# ================================================================================
"""
### Idea
The function `f(mid) = mid * mid` is monotonically increasing for
non-negative mid, which means "is mid*mid <= x?" is a classic monotonic
predicate — exactly what binary search needs. Search the range [0, x] for
the largest `mid` such that `mid * mid <= x`.

### Why does it work?
Binary search requires a search space where you can always discard HALF
the remaining candidates based on a single comparison. Because squaring
is monotonic for non-negative numbers, comparing `mid*mid` to `x` tells
us definitively whether the true answer lies in the lower half or upper
half of the current range — no information is lost by discarding the
other half.

### Complexity
- TC: O(log x) — the search range halves every iteration
- SC: O(1) — a few pointer variables

### Pros
- Much faster than any linear scan for large x.
- Standard "binary search on the answer" pattern — very transferable to
  other "find the largest/smallest value satisfying a monotonic
  condition" problems.

### DSA Buddy Point 🧠
"Whenever you're searching for 'the largest/smallest X such that
f(X) <= target' and f is monotonic, that's binary search on the answer —
not necessarily binary search over a sorted ARRAY, but over the space of
POSSIBLE ANSWERS itself."

### Edge Case ⚠️
When the loop ends (`l > r`), `r` holds the correct floor(sqrt(x))
because `r` is decremented only when `mid*mid > x` — so `r` always ends
up as the largest value proven to satisfy `mid*mid <= x`. Returning `r`
(not `l`) is the key detail — a common off-by-one trap in binary-search-
on-the-answer problems is returning the wrong boundary variable.

### What can be improved?
Nothing algorithmically for a general-purpose exact-integer-arithmetic
solution — O(log x) is optimal for binary search over this range. Newton's
Method (below) also achieves fast convergence and is worth knowing as an
alternative numerical technique, though its worst-case guarantees differ
from binary search's clean O(log x) bound.
"""


def my_sqrt(x: int) -> int:
    l, r = 0, x

    while l <= r:
        mid = (l + r) // 2
        product = mid * mid

        if product == x:
            return mid
        if product > x:
            r = mid - 1
        else:
            l = mid + 1
    return r


# ================================================================================
# ALTERNATIVE APPROACH — Linear Search
# ================================================================================
"""
### Thought Process 🧠
The most direct idea: just try 0, 1, 2, 3, ... squaring each one, until
the square exceeds x. The last value that didn't exceed x is the answer.

### Idea
Increment `i` while `i*i <= x`, then return `i - 1` once the loop
overshoots.

### Complexity
- TC: O(sqrt(x)) — we count up to roughly sqrt(x) before overshooting
- SC: O(1)

### Pros
- Extremely simple, no binary search bookkeeping to get wrong.
- Fine for small x.

### Cons
- For large x (e.g. x near 2^31), sqrt(x) is still ~46,340 iterations —
  vastly more than binary search's ~31 iterations (log2 of 2^31). The gap
  widens dramatically as x grows.

### Bottleneck
Checking every integer one at a time wastes the fact that "is i*i <= x"
is a MONOTONIC condition — once we know i*i > x, we also know every
larger i also fails, so we could have skipped huge chunks of the search
space. Ask: "can I eliminate half the remaining candidates with a single
check, instead of just one?" -> Yes: binary search (the main approach).
"""


def my_sqrt_linear(x: int) -> int:
    i = 0
    while i * i <= x:
        i += 1
    return i - 1


# ================================================================================
# ALTERNATIVE APPROACH — Newton's Method
# ================================================================================
"""
### Thought Process 🧠
A classic numerical-methods technique for finding roots: repeatedly refine
a guess using the update rule `guess = (guess + x/guess) / 2`, which
converges toward sqrt(x) extremely quickly (quadratic convergence — the
number of correct digits roughly DOUBLES each iteration).

### Idea
Start with an initial guess (x itself works, though smarter starting
points exist). Repeatedly apply the Newton update using integer division
until the guess squared no longer exceeds x. Because integer division
truncates, this converges to floor(sqrt(x)) exactly.

### Complexity
- TC: O(log x) in practice — Newton's method converges extremely fast
  (quadratically) for well-behaved functions like this one, typically
  needing only a handful of iterations even for very large x
- SC: O(1)

### Pros
- Extremely fast in practice — often fewer iterations than binary search
  for the same input, due to quadratic convergence.
- A genuinely different technique to have in your pocket — shows breadth
  beyond "binary search for everything."

### Cons
- The convergence proof and behavior are less immediately obvious than
  binary search's clean halving logic — harder to reason about
  correctness on the fly without prior familiarity with the method.
- Requires care with integer arithmetic to guarantee it lands exactly on
  the floor value rather than oscillating — the loop condition
  (`guess*guess > x`) must be gotten right to terminate correctly.

### DSA Buddy Point 🧠
"Newton's Method is calculus-flavored binary search — instead of halving
blindly, it uses the function's local slope to jump much closer to the
answer each step. Great to mention as 'another way to converge fast,' but
binary search is the safer default to write from memory under pressure."
"""


def my_sqrt_newton(x: int) -> int:
    if x == 0:
        return 0
    guess = x
    while guess * guess > x:
        guess = (guess + x // guess) // 2
    return guess


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
SQRT(X) — INTEGER SQUARE ROOT
│
├── Linear Search
│   └── Try 0,1,2,... until i*i > x -> O(sqrt(x))
│
├── Bottleneck
│   └── "i*i <= x" is MONOTONIC in i — checking one-at-a-time wastes that
│
├── Key Observation
│   └── Monotonic predicate over a range -> binary search on the ANSWER,
│       not just on sorted arrays
│
├── Path A — Binary Search on the Answer
│   └── Search [0, x] for largest mid with mid*mid <= x
│       └── O(log x) time, O(1) space  <-- standard optimal, your code
│
└── Path B — Newton's Method
    └── guess = (guess + x/guess) / 2, repeat until guess*guess <= x
        └── O(log x) time (quadratic convergence), O(1) space
            <-- different technique, same complexity class
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "'Largest/smallest value satisfying a monotonic condition' -> binary
  search on the ANSWER SPACE, even without a literal sorted array."
- "For mySqrt, the loop invariant is: when the loop ends, `r` (not `l`)
  holds the correct floor(sqrt(x)) — a classic off-by-one to double-check
  in every binary-search-on-the-answer problem."
- "Linear search is O(sqrt(x)) — looks small on paper, but for x near
  2^31 that's ~46,000 iterations vs. binary search's ~31. The gap is huge
  in practice, not just asymptotically."
- "Newton's Method converges quadratically — correct digits roughly
  double each step — making it a genuinely different, very fast
  alternative worth naming even if binary search is your default."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach              | Core Idea                                      | TC          | SC   | Pros                                   | Cons                                        | When to Use                          |
|--------------------------|-----------------------------------------------------|-------------|------|-----------------------------------------------|--------------------------------------------------|-------------------------------------------|
| Linear Search             | Increment i until i*i exceeds x                       | O(sqrt(x))  | O(1) | Trivial to write/verify                        | Far too slow for large x                          | Only for very small x / sanity checking   |
| Newton's Method           | Iteratively refine guess via (guess + x/guess)/2       | O(log x)*   | O(1) | Very fast in practice (quadratic convergence)   | Convergence/termination less obvious to reason about | Alternative to mention for breadth        |
| Binary Search on Answer   | Search [0,x] for largest mid with mid*mid <= x          | O(log x)    | O(1) | Clean halving logic, standard interview pattern | None significant                                  | Default optimal choice (your code)        |

  * Newton's method's O(log x) here is empirical/typical for this
    well-behaved function, not as tightly guaranteed in general as binary
    search's worst-case bound.

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Binary Search on the Answer Space (same family as "find peak
  element," "search in rotated sorted array," "koko eating bananas" —
  anywhere a monotonic yes/no predicate lets you halve the search space).
- Go-to answer: "Since mid*mid is monotonically increasing in mid, binary
  search [0, x] for the largest mid where mid*mid <= x. O(log x) time,
  O(1) space."
- Good to mention linear search first as the naive O(sqrt(x)) baseline,
  then pivot to "since squaring is monotonic, I can binary search instead
  of checking one at a time."
- Common follow-up: "How would you compute this without integer overflow
  concerns in a fixed-width-integer language?" -> Watch for `mid * mid`
  overflowing 32-bit integers for large x — use a wider integer type or
  compare via division (`mid <= x / mid`) instead of multiplication.
"""