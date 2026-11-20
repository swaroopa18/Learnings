"""
================================================================================
 PROBLEM: Decode Ways (LeetCode 91)
================================================================================
Given: a string `s` of digits.
Task: return the number of ways to decode it, where
  'A' -> "1", 'B' -> "2", ... 'Z' -> "26".
A valid code is "1".."26" (no leading zeros: "06" is NOT valid, "0" alone is
NOT valid). Return 0 if there is no valid decoding.

Examples:
  "12"  -> 2   ("AB" = 1|2, "L" = 12)
  "226" -> 3   ("BZ" = 2|26, "VF" = 22|6, "BBF" = 2|2|6)
  "06"  -> 0   (leading zero -> impossible)
  "10"  -> 1   ("J" only; 1|0 is invalid)

Follow-up: can you do it in O(1) extra space?

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Can `s` be empty? (LeetCode: length >= 1; for robustness return 0)
- Can `s` contain non-digit characters? (No -> only '0'-'9')
- Is a leading zero ever valid? (No: "0" and "06" are invalid, "10"/"20" are)
- How large can the answer get? (Guaranteed to fit in a 32-bit int; in other
  languages ask about overflow / modulo)
- How long can `s` be? (<= 100 -> O(n) is easy, but pure recursion is
  exponential, so it's worth discussing)
"""

from typing import List
from functools import lru_cache

# ================================================================================
# MY APPROACH #1 — Brute-force recursion (try 1 digit, try 2 digits)
# ================================================================================
"""
### Idea
Define `go(i)` = number of ways to decode the suffix s[i:].
  - If i == n          -> 1 (a complete decoding was formed)
  - If s[i] == '0'     -> 0 (nothing can start with 0)
  - Otherwise: take 1 digit -> go(i + 1)
               take 2 digits if s[i:i+2] is in 10..26 -> + go(i + 2)

### Complexity
- TC: O(2^n) worst case — every position can branch into two calls, and the
  same suffix is recomputed many times (it grows like Fibonacci)
- SC: O(n) — recursion depth is at most n

### Pros
- Directly mirrors the definition; the easiest way to see the recurrence.

### Cons
- Exponential time: "1111111111111111111111111" times out.
- Overlapping subproblems: go(i) is recomputed over and over.

### Bottleneck
Repeated work. go(i) depends only on i, so there are only n+1 distinct
subproblems -> cache them (approach #2) or build bottom-up (approach #3).
"""


class SolutionBruteForce:
    def numDecodings(self, s: str) -> int:
        n = len(s)

        def go(i):
            if i == n:
                return 1
            if s[i] == "0":
                return 0

            ways = go(i + 1)
            if i + 1 < n and 10 <= int(s[i : i + 2]) <= 26:
                ways += go(i + 2)
            return ways

        return go(0) if s else 0


# ================================================================================
# MY APPROACH #2 — Top-down DP (recursion + memoization)
# ================================================================================
"""
### Idea
Same recurrence as #1, but cache `go(i)` so each suffix is solved once.

### Complexity
- TC: O(n) — n+1 states, O(1) work per state
- SC: O(n) — memo table + recursion stack

### Pros
- Minimal change from brute force; easy to derive in an interview.

### Cons
- Recursion depth n (fine for n <= 100, risky for very long strings).
- Function-call overhead; the O(n) table is not actually needed (see #4).

### Bottleneck
go(i) only ever needs go(i+1) and go(i+2) -> a full table (and the call
stack) is wasteful. Go bottom-up.
"""


class SolutionMemo:
    def numDecodings(self, s: str) -> int:
        n = len(s)

        @lru_cache(maxsize=None)
        def go(i):
            if i == n:
                return 1
            if s[i] == "0":
                return 0

            ways = go(i + 1)
            if i + 1 < n and 10 <= int(s[i : i + 2]) <= 26:
                ways += go(i + 2)
            return ways

        return go(0) if s else 0


# ================================================================================
# MY APPROACH #3 — Bottom-up DP array (my submitted solution)
# ================================================================================
"""
### Idea
dp[i] = number of ways to decode the PREFIX s[0..i] (inclusive).
For each position i there are two independent ways the last code can end:
  1. s[i] alone is a valid code (1..9)           -> add dp[i-1]
  2. s[i-1:i+1] together is a valid code (10..26) -> add dp[i-2]
Base cases are handled separately:
  - dp[0] = 1 if s[0] is valid, else the answer is 0
  - dp[1] = (s[1] valid ? dp[0] : 0) + (s[0:2] in 10..26 ? 1 : 0)

### Why does it work?
Every decoding of s[0..i] ends with either a 1-digit code or a 2-digit code.
These two cases are disjoint and exhaustive, so the counts simply add up.
A '0' can never be a 1-digit code, so it only counts as the second half of
"10" or "20" — which the two-digit check covers automatically.

### Complexity
- TC: O(n) — one pass, O(1) work per index
- SC: O(n) — the dp array

### Pros
- No recursion, no stack-overflow risk; easy to trace by hand.
- Handles leading zeros / "00" / "30" naturally through the two checks.

### Cons
- Base cases dp[0], dp[1] are special-cased -> more code, more bugs
  (the "+= 1" for the first pair is a hidden "dp[-1] = 1" assumption).
- O(n) space even though only the last two values are used.
- `isValid` uses int() conversions on every call (fine, but slightly slow);
  `s[i] != '0'` is cheaper and clearer.

### What can be improved?
- Use dp of size n+1 with dp[0] = 1 for the empty prefix -> removes the
  special base cases for index 1.
- Keep only two variables -> O(1) space (approach #4).
"""


class SolutionDP:
    def numDecodings(self, s: str) -> int:
        def isValid(char):
            return 1 <= int(char) <= 26

        if not s or not isValid(s[0]):
            return 0

        if len(s) == 1:
            return 1

        dp = [0] * len(s)
        dp[0] = 1

        if isValid(s[1]):
            dp[1] += dp[0]

        if 10 <= int(s[0:2]) <= 26:
            dp[1] += 1

        for i in range(2, len(s)):
            if isValid(s[i]):
                dp[i] += dp[i - 1]
            if 10 <= int(s[i - 1 : i + 1]) <= 26:
                dp[i] += dp[i - 2]
        return dp[-1]


# ================================================================================
# MY APPROACH #4 — Bottom-up DP with O(1) space (optimal)
# ================================================================================
"""
### Idea
dp[i] only depends on dp[i-1] and dp[i-2], so keep two rolling variables:
  prev2 = dp[i-2], prev1 = dp[i-1]
Treat the empty prefix as having exactly 1 decoding (prev2 = 1 initially),
which removes the special base case for the second character.
For each i from 1..n-1:
  cur = 0
  if s[i] != '0'                  : cur += prev1   (1-digit code)
  if 10 <= int(s[i-1:i+1]) <= 26  : cur += prev2   (2-digit code)
  shift: prev2, prev1 = prev1, cur
Early exit: if s[0] == '0' -> 0.

### Why does it work?
Exactly the same recurrence as #3; we just discard dp values that can never
be read again.

### Complexity
- TC: O(n) — single pass
- SC: O(1) — two integers

### Pros
- Optimal time and space; short; no recursion.
- Empty-prefix trick (dp = 1) gives clean base cases.

### Cons
- Slightly harder to explain than the array version (rolling variables).
- If `cur` becomes 0 at some index while later digits look fine, the answer
  correctly becomes 0 only because prev1/prev2 propagate it — easy to
  mis-trace by hand.

### What can be improved?
Nothing asymptotically. For a follow-up with modulo (LC 639, '*' wildcard)
the same rolling idea works with extra case analysis.
"""


class SolutionOptimal:
    def numDecodings(self, s: str) -> int:
        if not s or s[0] == "0":
            return 0

        prev2, prev1 = 1, 1  # dp[i-2], dp[i-1]

        for i in range(1, len(s)):
            cur = 0
            if s[i] != "0":
                cur += prev1
            if 10 <= int(s[i - 1 : i + 1]) <= 26:
                cur += prev2
            prev2, prev1 = prev1, cur

        return prev1


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
DECODE WAYS
│
├── Definition
│   └── Count splits of s into codes "1".."26" (no leading zeros)
│
├── Recurrence (the heart of the problem)
│   └── ways(i) = [s[i] != '0'] * ways(i+1)
│               + [10 <= s[i:i+2] <= 26] * ways(i+2)
│       └── same shape as Climbing Stairs / Fibonacci with conditions
│
├── Brute force recursion
│   └── O(2^n) time — overlapping subproblems
│
├── Top-down memoization
│   └── O(n) time, O(n) space (cache + stack)
│
├── Bottom-up DP array
│   ├── dp[i] = dp[i-1] (if 1-digit ok) + dp[i-2] (if 2-digit ok)
│   └── O(n) time, O(n) space
│
├── Space-optimized DP
│   └── two rolling variables, empty prefix = 1
│       └── O(n) time, O(1) space
│
└── Edge cases
    ├── leading '0'          -> 0
    ├── "00", "30", "40"...  -> 0 (0 cannot stand alone, 30+ is not a code)
    ├── "10", "20"           -> 1 (0 only valid glued to 1 or 2)
    └── "27".."99"           -> only the 1-digit split is allowed
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Decode Ways = Climbing Stairs with conditions: you can take a 1-step
  (digit 1-9) and/or a 2-step (10-26); count the paths to the end."
- "A '0' can never stand alone. It is only usable as the second digit of
  '10' or '20'. Everything else involving 0 kills the decoding."
- "Check the 2-digit window with the NUMERIC value 10..26, not just <= 26:
  '06' converts to 6 but is NOT a valid code. Using >= 10 excludes it."
- "The 1-digit check and the 2-digit check are independent — BOTH can fire
  at the same index (e.g. '12' -> 1|2 and 12). Don't use elif."
- "Empty prefix = 1 way. This single convention removes special base cases."
- "dp[i] depends only on dp[i-1], dp[i-2] -> roll two variables for O(1)."
- "Test list: '12', '226', '06', '0', '10', '100', '27', '2101', '1201234'."
- "Same family: LC 70 (Climbing Stairs), LC 639 (Decode Ways II with '*'),
  LC 198 (House Robber), LC 509 (Fibonacci), LC 1155 (Dice Rolls)."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                | Core Idea                                         | TC     | SC (extra) | Pros                              | Cons                                         | When to Use                         |
|-------------------------|---------------------------------------------------|--------|------------|-----------------------------------|----------------------------------------------|-------------------------------------|
| Brute-force recursion   | go(i) = go(i+1) + go(i+2) with validity checks    | O(2^n) | O(n)       | Mirrors the definition            | Exponential; recomputes subproblems          | Only to derive the recurrence       |
| Top-down memo           | Same recurrence + cache                           | O(n)   | O(n)       | Tiny change from brute force      | Recursion depth n; call overhead             | Quick correct answer in interview   |
| Bottom-up DP array      | dp[i] = dp[i-1] + dp[i-2] under conditions        | O(n)   | O(n)       | No recursion; easy to trace       | Special base cases; O(n) space               | Clear, safe default                 |
| Rolling variables (O(1))| Keep only prev2, prev1; empty prefix = 1          | O(n)   | O(1)       | Optimal time and space            | Slightly trickier to explain                 | Final / follow-up answer            |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: 1-D DP / counting paths (Fibonacci-style with validity conditions).
- Go-to answer: "Let dp[i] be the number of ways to decode the first i
  characters. The last code is either one digit (valid if it's not '0') or
  two digits (valid if it's 10..26), so dp[i] = dp[i-1] (if the last char is
  non-zero) + dp[i-2] (if the last two chars form 10..26). With dp[0] = 1 for
  the empty string, this is O(n) time. Since only the last two values are
  needed, I keep two variables and get O(1) space."
- Good to mention: why '0' is special, why '06' fails the two-digit check,
  and the brute-force -> memo -> bottom-up -> O(1) progression.
- Common follow-ups:
  * "Can you reduce the space?" -> rolling variables.
  * "What if the string has '*' wildcards?" -> LC 639 (more cases, mod 1e9+7).
  * "Return all the decodings, not just the count?" -> backtracking
    (LC 93-style), exponential output size.
  * "What if the alphabet were larger than 26?" -> generalize the 2-digit
    check to k-digit windows (up to len(str(max_code))).
"""


if __name__ == "__main__":
    tests = ["12", "226", "06", "0", "10", "100", "27", "2101", "1201234", "11106"]
    for cls in (SolutionBruteForce, SolutionMemo, SolutionDP, SolutionOptimal):
        print(cls.__name__, [cls().numDecodings(t) for t in tests])