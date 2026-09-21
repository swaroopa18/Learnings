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
# 🔑🔑🔑  THE #1 RULE FOR BINARY-SEARCH BOUNDARIES  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   If your answer is the FIRST INVALID / first position AFTER       │
    │   the boundary  ──────────────────────────────────>  return `l`    │
    │                                                                     │
    │   If your answer is the LAST VALID / position BEFORE               │
    │   the boundary  ──────────────────────────────────>  return `r`    │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

THIS PROBLEM (mySqrt): we want the LARGEST value still satisfying
`mid*mid <= x` — that's the LAST VALID position before crossing into
"too big" territory -> return `r`.

Memorize this rule as a REFLEX, not a per-problem derivation. The moment
you know which side of the boundary your answer sits on, you know
instantly which variable to return — no need to re-trace the whole loop
every time to figure it out.
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea
Forget binary search for a second. If someone asked YOU "what's the
integer square root of 15?" by hand, you might just start guessing:
"Is it 1? 1*1=1, too small. Is it 2? 4, too small. Is it 3? 9, still too
small. Is it 4? 16 — too BIG! So the answer must be 3, since 3*3=9<=15
but 4*4=16>15." That's exactly what Linear Search does — try every number
starting from 0 until you overshoot, then step back by one.

### Why binary search instead of counting one by one?
Counting 1, 2, 3, 4... works, but imagine x = 1,000,000. You'd count all
the way up to 1000 before finding the answer! Here's the key trick: once
you know a number's square is TOO BIG, you also automatically know every
LARGER number's square is too big too (numbers only get bigger as you
square bigger things). So instead of checking numbers one at a time, you
can guess the MIDDLE of your search range, and immediately throw away
HALF the remaining possibilities based on just one check.

### A mental picture: "guess the number" but smarter
Think of the classic game "guess the number between 1 and 100" where
someone tells you "higher" or "lower" after each guess. If you played it
smart, you wouldn't guess 1, 2, 3, 4... one by one — you'd guess 50 first,
then 25 or 75 depending on the answer, and so on. This problem is exactly
that game, except instead of a person saying "higher/lower," the
comparison `mid*mid` vs `x` tells you which half to search next.

### Step-by-step trace: finding sqrt(15)
```
l=0, r=15   (searching the whole range [0, 15])

Step 1: mid = (0+15)//2 = 7    -> 7*7=49, way too big (49 > 15)
        so the answer must be SMALLER than 7 -> r = mid-1 = 6

Step 2: l=0, r=6  -> mid = (0+6)//2 = 3   -> 3*3=9, too small (9 <= 15)
        so the answer might be 3 OR bigger -> l = mid+1 = 4

Step 3: l=4, r=6  -> mid = (4+6)//2 = 5   -> 5*5=25, too big (25 > 15)
        so the answer must be SMALLER than 5 -> r = mid-1 = 4

Step 4: l=4, r=4  -> mid = (4+4)//2 = 4   -> 4*4=16, too big (16 > 15)
        so the answer must be SMALLER than 4 -> r = mid-1 = 3

Step 5: l=4, r=3  -> l > r, loop ends!

Return r = 3.  Check: 3*3=9 <= 15, and 4*4=16 > 15. Correct! ✅
```
Notice: we found the answer in just 4 comparisons, instead of counting
0,1,2,3 one by one (which would've taken 4 steps here too, but for x =
1,000,000 binary search takes ~20 steps while counting takes ~1000!).

### Why does `r` end up being the answer, not `l`?
Trace through carefully: `r` only ever moves when we've PROVEN
`mid*mid > x` (too big) — so every time `r` shrinks, it's because we just
ruled out `mid` and everything above it. `l` only ever moves when we've
PROVEN `mid*mid <= x` (still valid) — so `l` is always chasing "maybe
still too small." When the loop finally ends (`l` has crossed past `r`),
`r` is sitting on the last value that was CONFIRMED to satisfy
`mid*mid <= x`. That's exactly the definition of floor(sqrt(x)).

### Building strong intuition: the "shrinking fence" mental model
Picture two fence posts, `l` on the left and `r` on the right, standing on
a number line from 0 to x. Every single step, you look at the number
exactly in the middle of the two posts. If it's too big, you know the
TRUE answer is somewhere to the left, so you move the right post inward.
If it's still valid, the true answer might be here or further right, so
you move the left post inward. The two posts keep squeezing toward each
other. The moment they cross, the right post (`r`) is left standing
exactly on the correct answer — like a fence that shrank until it was
just barely touching the boundary between "valid" and "too big."

### The "aha" moment to remember 🎯
Binary search doesn't require a sorted ARRAY — it requires a sorted
YES/NO ANSWER as you move along a range. Here, "is mid*mid <= x?" flips
from YES to NO exactly once as mid increases (never flips back), and that
single flip point IS the answer. Any time you can phrase a problem as
"find where a yes/no answer flips, in a range where it only flips once,"
binary search applies — even if there's no array in sight.
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

# ================================================================================
# STRONG UNDERSTANDING CHECK 💪
# ================================================================================
"""
If you can confidently answer these without looking back up, you've truly
internalized this problem (not just memorized the code):

1. Q: Why can't we binary search this the same way if `x` could be
      negative?
   A: Because square roots of negative numbers aren't real numbers, so
      there's no valid answer to search FOR — the problem's monotonic
      predicate ("is mid*mid <= x?") doesn't even make sense to evaluate
      against a negative target in this context.

2. Q: What would break if we returned `l` instead of `r` at the end?
   A: `l` always ends up ONE PAST the correct answer — it's the first
      value PROVEN to be too big (or one past the search space if no
      value was ever too big). Returning `l` would overshoot the floor by
      exactly 1 in most cases. Try tracing x=15 with `l` instead of `r`
      to see it land on 4 (wrong) instead of 3 (correct).
      🔑 Rule check: our answer is the LAST VALID value before the
      boundary -> the rule says return `r`. This IS that rule in action.

3. Q: Why is `mid = (l + r) // 2` and not `mid = (l + r) / 2`?
   A: We're searching over INTEGERS (possible integer answers), so `mid`
      must itself be a valid integer candidate — floor division keeps it
      that way. Using true division would produce a float, which doesn't
      make sense as an "index" into the answer range.

4. Q: What's the deeper reason binary search works here, beyond "the
      function is increasing"?
   A: Binary search works on ANY predicate that is monotonic across the
      search range — meaning it's False for a while, then True forever
      after (or vice versa), with exactly ONE flip point. "mid*mid <= x"
      starts True (at mid=0) and becomes False forever once mid exceeds
      sqrt(x) — exactly one flip, which is what lets us safely discard
      half the range every step without ever discarding the true answer.

5. Q: If you had to explain this to someone who's never seen binary
      search before, in one sentence, what would you say?
   A: "Instead of checking every possible answer one by one, I keep
      guessing the middle of what's left and use whether I guessed too
      high or too low to throw away half of the remaining possibilities
      each time — like narrowing down a number in a guessing game."
"""


if __name__ == "__main__":
    tests = [0, 1, 2, 3, 4, 8, 9, 15, 16, 2147395599, 2147483647]
    for x in tests:
        a = my_sqrt(x)
        b = my_sqrt_linear(x)
        c = my_sqrt_newton(x)
        assert a == b == c, f"Mismatch on x={x}: {a}, {b}, {c}"
        print(f"x={x} -> {a}")