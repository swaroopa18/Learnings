"""
================================================================================
 PROBLEM: Pow(x, n) (LeetCode 50)
================================================================================
Implement `pow(x, n)`, which calculates `x` raised to the power `n` (i.e. x^n).
`x` is a float, `n` is a 32-bit signed integer (it can be negative or zero).

Example 1: x = 2.0,  n = 10  -> 1024.0
Example 2: x = 2.1,  n = 3   -> 9.261
Example 3: x = 2.0,  n = -2  -> 0.25      (2^-2 = 1 / 2^2)

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Can `n` be negative? (Yes — x^-n = 1 / x^n. Handle the sign ONCE, up front,
  so the rest of the logic only deals with n >= 0.)
- Can `n` be 0? (Yes — anything^0 = 1, including x = 0 by the usual convention
  here. This is the BASE CASE of the recursion.)
- How large can |n| be? (Up to 2^31. A loop doing n multiplications is
  ~2 billion steps -> too slow. This is exactly what forces O(log n).)
- Can `x` be 0 with a negative `n`? (That is 1/0 -> undefined. LeetCode
  guarantees it will not happen; in an interview, state this assumption or
  raise an error.)
- Is floating-point precision a concern? (Answers within ~1e-5 are accepted;
  fewer multiplications also means less accumulated rounding error.)

"""

# ================================================================================
# 🔑🔑🔑  STRONG POINTS FOR "FAST EXPONENTIATION" PROBLEMS  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   x^n = (x^(n/2))^2        when n is EVEN   -> HALVE the problem.   │
    │   x^n = x * x^(n-1)        when n is ODD    -> make it even first.  │
    │   Halving every step => only O(log n) multiplications, not O(n).    │
    │   NEGATIVE n?  x^-n = 1 / x^n  -> flip the sign once at the top.    │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

This is "binary exponentiation" (exponentiation by squaring) — the same
divide-and-conquer idea used in modular exponentiation, matrix power (fast
Fibonacci) and many number-theory problems. Key ideas:

1. **Halve the exponent, square the result.** For even n, compute x^(n/2)
   ONCE and multiply it by itself. The classic mistake is writing
   `myPow(x, n//2) * myPow(x, n//2)` — that calls the function TWICE and
   throws away the speedup (back to O(n)). Store it in a variable first.

2. **An odd exponent costs one extra multiplication, then it is even.**
   x^n = x * x^(n-1), and n-1 is even, so the next step halves it. So at
   most every OTHER step is a "peel off one x" step => depth <= 2 * log2(n).

3. **Handle negative n up front with `1 / myPow(x, -n)`.** After that the
   recursion only ever sees n >= 0. (In Python `-n` is safe even for
   n = -2^31; in Java/C++ negating INT_MIN overflows — use a long.)

4. **Base case is n == 0 -> 1.** Every chain n -> n/2 or n -> n-1 eventually
   lands on 0, so the recursion always terminates.

5. **Complexity is logarithmic in n, not n.** n = 2^31 needs only ~31 halvings
   (about 62 calls worst case), versus 2 billion multiplications by brute force.
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea
2^10 = 2 * 2 * 2 * 2 * 2 * 2 * 2 * 2 * 2 * 2  -> ten multiplications.
Fine for 10, hopeless for 2,000,000,000.

### The key insight: reuse the half
2^10 = 2^5 * 2^5. If I know 2^5, ONE multiplication gives 2^10.
And 2^5 = 2 * 2^4, 2^4 = 2^2 * 2^2, 2^2 = 2^1 * 2^1 ...
Each step cuts the exponent roughly in half, so the number of steps is
about log2(n) instead of n.

### Step-by-step trace: myPow(2, 10)
```
myPow(2, 10)  even -> r = myPow(2, 5);  return r * r
 └─ myPow(2, 5)  odd  -> return 2 * myPow(2, 4)
     └─ myPow(2, 4)  even -> r = myPow(2, 2);  return r * r
         └─ myPow(2, 2)  even -> r = myPow(2, 1);  return r * r
             └─ myPow(2, 1)  odd  -> return 2 * myPow(2, 0)
                 └─ myPow(2, 0) -> 1                    <- base case
             myPow(2, 1) = 2 * 1  = 2
         myPow(2, 2) = 2 * 2  = 4
     myPow(2, 4) = 4 * 4  = 16
 myPow(2, 5) = 2 * 16 = 32
myPow(2, 10) = 32 * 32 = 1024 ✅
```
Only 6 multiplications instead of 10 (the gap explodes for big n).

### Negative exponent trace: myPow(2, -2)
```
n < 0 -> 1 / myPow(2, 2) = 1 / 4 = 0.25 ✅
```

### The "aha" moment to remember 🎯
"Power with a huge exponent => HALVE the exponent and SQUARE the result.
Odd => peel one x off to make it even. Negative => take the reciprocal once."
"""

# ================================================================================
# ALTERNATIVE APPROACH 1 — Brute Force (multiply x, n times)
# ================================================================================
"""
### Thought Process 🧠
Multiply `x` into a running result |n| times. If n is negative, take the
reciprocal at the end.

### Complexity
- TC: O(|n|) — one multiplication per unit of the exponent
- SC: O(1) — a single running product

### Pros
- Trivially correct; perfect baseline for validating the fast solution.
- No recursion, no edge-case cleverness.

### Cons
- |n| can be ~2.1 billion -> far too slow (TLE) in practice.
- Many repeated multiplications also accumulate more floating-point error.

### Bottleneck
We recompute overlapping products: x^10 re-does everything inside x^5 twice.
Ask: "can I reuse x^(n/2) instead of rebuilding it?" -> binary exponentiation.
"""


def my_pow_brute(x: float, n: int) -> float:
    result = 1.0
    for _ in range(abs(n)):
        result *= x
    return 1 / result if n < 0 else result


# ================================================================================
# ALTERNATIVE APPROACH 2 — Iterative Binary Exponentiation (bit by bit)
# ================================================================================
"""
### Thought Process 🧠
Write n in binary. Every set bit contributes x^(2^k) to the answer. Walk the
bits of n from least significant to most significant while SQUARING `x` each
step (x, x^2, x^4, x^8, ...). Whenever the current bit is 1, multiply the
running result by the current x.

Example: n = 10 = 1010 (binary)
    x^10 = x^8 * x^2   (bits for 8 and 2 are set)

### Complexity
- TC: O(log n) — one loop iteration per bit of n (~31 for a 32-bit int)
- SC: O(1) — no recursion stack, just two variables

### Pros
- O(1) extra space — no recursion limit worries at all.
- Fastest in practice (no function-call overhead).
- Same loop is reused for modular exponentiation (just add `% mod`).

### Cons
- Less intuitive than the recursive "halve and square" explanation.
- Easy to slip on the details: forgetting to flip x to 1/x for negative n,
  or updating `x` and `n` in the wrong order.

### DSA Buddy Point 🧠
"Recursive halving and bit-by-bit squaring are the SAME algorithm. The
recursion walks the bits from the top; the loop walks them from the bottom."
"""


def my_pow_iterative(x: float, n: int) -> float:
    if n < 0:
        x = 1 / x
        n = -n
    result = 1.0
    while n:
        if n & 1:  # current lowest bit is 1 -> include this power of x
            result *= x
        x *= x  # x, x^2, x^4, x^8, ...
        n >>= 1  # move to the next bit
    return result


# ================================================================================
# MY APPROACH — Recursive Binary Exponentiation (optimal)
# ================================================================================
"""
### Idea
Handle a negative exponent once by returning `1 / myPow(x, -n)`. Base case is
`n == 0 -> 1`. For an EVEN n, compute the half power ONCE and square it. For
an ODD n, peel off one factor of x (`x * myPow(x, n - 1)`) so the exponent
becomes even and gets halved on the next call.

### Complexity
- TC: O(log n) — the exponent at least halves every two calls
- SC: O(log n) — recursion stack of depth up to ~2 * log2(n)

### Pros
- Optimal time; reads like the math definition.
- Computes the half power ONCE and stores it in `result` (the key step that
  keeps it logarithmic instead of linear).
- Handles negative n, n = 0 and n = 1 cleanly with no special loops.

### Cons
- O(log n) stack space (tiny — about 62 frames for 2^31 — but not O(1)).
- The odd branch `n - 1` costs an extra call per odd step; halving directly
  with `n // 2` for odd n (below) avoids that.
- Float edge cases: x = 0 with negative n gives ZeroDivisionError (excluded by
  the problem constraints); huge results may overflow to `inf`.

### DSA Buddy Point 🧠
"If you ever write f(n//2) * f(n//2), STOP — store f(n//2) in a variable and
square it. Calling it twice silently turns O(log n) into O(n)."

### What can be improved?
Complexity-wise nothing — O(log n) time is optimal for this approach. One
optional tweak: for odd n you can skip the `n - 1` step and write
`half = myPow(x, n // 2); return half * half * x`. That uses ONE call per
halving (depth ~log2 n instead of ~2 * log2 n). Your version is already
correct as written; this is just a minor depth/readability optimisation.
"""


class Solution:
    def myPow(self, x: float, n: int) -> float:
        if n < 0:
            return 1 / self.myPow(x, -n)
        if n == 0:
            return 1
        if n % 2 == 0:
            result = self.myPow(x, n // 2)
            return result * result
        else:
            return x * self.myPow(x, n - 1)


# ================================================================================
# ALTERNATIVE APPROACH 3 — Recursive Halving with n // 2 for Odd n Too
# ================================================================================
"""
### Thought Process 🧠
Always split n into n // 2 (integer halving). Compute the half power once,
square it, and multiply by one extra x if n is odd:
    x^n = (x^(n//2))^2        if n is even
    x^n = (x^(n//2))^2 * x    if n is odd

### Complexity
- TC: O(log n) — exactly one halving per call
- SC: O(log n) — recursion depth ~log2(n) (about half of the version above)

### Pros
- One call per level -> shallower stack than the `n - 1` version.
- Both even and odd cases share the same recursive call (less code).

### Cons
- Still O(log n) stack space (use the iterative version for O(1)).
- Slightly less obvious than "even -> halve, odd -> peel one off".

### DSA Buddy Point 🧠
"Same algorithm, tighter recursion: split n into n//2 plus a remainder bit
and multiply by x only when that bit is 1."
"""


def my_pow_halving(x: float, n: int) -> float:
    if n < 0:
        return 1 / my_pow_halving(x, -n)
    if n == 0:
        return 1.0
    half = my_pow_halving(x, n // 2)
    return half * half * x if n % 2 else half * half


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
POW(x, n)
│
├── Brute Force
│   └── Multiply x, |n| times -> O(n) time, O(1) space (TLE for n ~ 2^31)
│
├── Bottleneck
│   └── Overlapping products: x^10 rebuilds x^5 twice. Exponent is HUGE, so
│       we need to cut the number of multiplications to ~log n
│
├── Key Insight
│   └── x^n = (x^(n/2))^2. Halve the exponent each step and reuse the half
│       (compute it ONCE). Odd n -> peel off one x. Negative n -> 1 / x^|n|
│
├── My Approach — Recursive Binary Exponentiation (BEST, clear)
│   └── n < 0 -> 1/pow(x,-n); n == 0 -> 1; even -> square the half;
│       odd -> x * pow(x, n-1)  -> O(log n) time, O(log n) stack
│
├── Recursive Halving (n // 2 for odd too)
│   └── half = pow(x, n//2); square it, times x if n odd
│       -> O(log n) time, ~half the stack depth of the version above
│
└── Iterative Bit-by-Bit
    └── square x each step, multiply into result when the bit is 1
        -> O(log n) time, O(1) space
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Big exponent => exponentiation by squaring: x^n = (x^(n/2))^2 for even n,
  x * x^(n-1) for odd n. That is O(log n) multiplications instead of O(n)."
- "Compute the half power ONCE and store it. Writing f(n//2) * f(n//2)
  calls the function twice and brings the complexity back to O(n)."
- "Handle negative exponents at the top: x^-n = 1 / x^n. After that the
  recursion only deals with n >= 0."
- "Base case is n == 0 -> 1. Every path (n -> n/2 or n -> n-1) reaches it."
- "Python ints never overflow, so -n is safe for n = -2^31. In Java/C++ cast
  to long first, because -INT_MIN overflows."
- "x = 0 with n < 0 is 1/0 -> undefined; call out the assumption in an
  interview."
- "Iterative version = same idea over the BITS of n: square x every step,
  multiply into the result when the bit is 1. Reused for modular power
  (add `% mod`) and matrix power (fast Fibonacci)."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                         | Core Idea                                     | TC       | SC       | Pros                                        | Cons                                                | When to Use                          |
|----------------------------------|-----------------------------------------------|----------|----------|---------------------------------------------|-----------------------------------------------------|--------------------------------------|
| Brute Force                      | Multiply x, |n| times                          | O(n)     | O(1)     | Trivial, great for validating               | TLE for n ~ 2^31, more float error                  | Baseline / correctness check         |
| Iterative Binary Exponentiation  | Square x each step, multiply in on set bits   | O(log n) | O(1)     | O(1) space, fastest, no recursion limit     | Less intuitive, bit/ordering details are easy to slip| Production code, avoid stack depth   |
| Recursive (even/odd, your code)  | Even: square the half. Odd: peel one x off    | O(log n) | O(log n) | Optimal time, mirrors the math, easy to read| ~2 * log n stack depth, extra `n - 1` call per odd  | Default interview answer (your code) |
| Recursive Halving (n // 2)       | half = pow(x, n//2); square; times x if odd   | O(log n) | O(log n) | One call per level, shallower stack         | Slightly less obvious odd handling                  | Tighter recursion variant            |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Divide & Conquer / Binary (Fast) Exponentiation — same family as
  Fibonacci via matrix power, modular exponentiation (Modular Pow / RSA),
  LC 372 (Super Pow), LC 1922 (Count Good Numbers).
- Go-to answer: "If n < 0, return 1 / myPow(x, -n). Base case n == 0 -> 1.
  For even n, compute half = myPow(x, n // 2) once and return half * half.
  For odd n, return x * myPow(x, n - 1). That is O(log n) time and O(log n)
  stack space; an iterative bit-by-bit version gets O(1) space."
- Good to call out: why n is halved (log n steps), why the half is computed
  ONCE (not twice), the negative-exponent handling, and the INT_MIN overflow
  trap in Java/C++.
- Common follow-up: "Can you do it without recursion?" -> iterative binary
  exponentiation, O(1) space. "Compute x^n mod m?" -> same loop, multiply and
  square under `% m`. "What about x^n for a 2x2 matrix / Fibonacci(n)?" ->
  replace float multiply with matrix multiply, still O(log n).
"""