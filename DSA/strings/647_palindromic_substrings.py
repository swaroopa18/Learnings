"""
================================================================================
 PROBLEM: Palindromic Substrings (LeetCode 647)
================================================================================
Given: a string `s`.
Task: return the total COUNT of substrings of `s` that are palindromes
(substrings at different positions count separately, even if their text
is identical — e.g. "aaa" has 6 palindromic substrings: "a","a","a",
"aa","aa","aaa").

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Do identical-text substrings at different positions count separately?
  (Yes — "aaa" gives 6, not fewer, since position matters)
- Is a single character always a palindrome? (Yes — every length-1
  substring counts)
- Empty string input? (Answer is trivially 0)
- Case-sensitive / any character restrictions? (Typically plain
  comparison, no normalization needed unless stated)
"""

# ================================================================================
# MY APPROACH #1 — Brute Force (check every substring)
# ================================================================================
"""
### Idea
Enumerate every possible substring by its (start, end) index pair, and for
each one, check with a two-pointer `isPalindrome` helper whether it reads
the same forwards and backwards.

### Complexity
- TC: O(n^3) — O(n^2) substrings total, and each `isPalindrome` check can
  take up to O(n) time in the worst case (e.g. a string of all identical
  characters, where every substring passes the full two-pointer scan)
- SC: O(1) extra (ignoring recursion/call overhead of the helper)

### Pros
- Directly matches the problem statement — very easy to verify correct.
- No insight about palindrome structure required to write it.

### Cons
- Cubic — checks every substring from scratch with no reuse of the fact
  that a palindrome check on a LARGER substring already implies
  information about its inner substring.

### Bottleneck
Checking whether `s[i..j]` is a palindrome via a full two-pointer scan
throws away the fact that a palindrome must "grow outward" from some
center — if we instead started FROM the center and expanded outward, each
character comparison would only ever need to happen once per valid
expansion. Ask: "can I avoid re-scanning the whole substring by growing
outward from candidate centers instead?" -> Yes: expand-around-center
(the main approach below).
"""


def count_substrings_brute(s: str) -> int:
    total = 0

    def is_palindrome(l, r):
        while l <= r:
            if s[l] != s[r]:
                return False
            l += 1
            r -= 1
        return True

    for i in range(len(s)):
        for j in range(i, len(s)):
            if is_palindrome(i, j):
                total += 1
    return total


# ================================================================================
# MY APPROACH #2 — Expand Around Center
# ================================================================================
"""
### Idea
Every palindrome has a CENTER — either a single character (odd-length
palindrome, like "aba") or a gap between two characters (even-length
palindrome, like "abba"). There are exactly `2n - 1` possible centers for
a string of length n: n single-character centers, and n-1 between-character
gaps. For each center, expand outward with two pointers (l, r) as long as
`s[l] == s[r]`, counting one valid palindrome per successful expansion
step.

### Why does it work?
Instead of checking "is this substring a palindrome?" from the outside in
(which risks redoing comparisons for substrings we've already partially
validated), we grow palindromes from the inside out. Each expansion step
naturally builds on the fact that everything closer to the center was
ALREADY confirmed symmetric in a previous step — no redundant re-checking
of inner characters.

### Complexity
- TC: O(n^2) — there are O(n) centers, and each center's expansion can run
  up to O(n) steps in the worst case (e.g. all-identical-character string)
- SC: O(1) extra — just a few pointer variables per center

### Pros
- Much better than brute force — drops one full factor of n by never
  re-verifying already-confirmed inner symmetry.
- Simple to implement, no auxiliary data structures needed.

### DSA Buddy Point 🧠
"Palindrome counting/finding problems -> think 'expand around center'
first. 2n-1 centers (n odd, n-1 even), grow outward while characters
match — this is the standard O(n^2) baseline for palindrome substring
problems."

### What can be improved?
For counting specifically, O(n^2) is about as good as it gets without
Manacher's Algorithm — a specialized O(n) technique that avoids
re-expanding by reusing symmetry information from previously computed
palindromes. It's a legitimate further optimization but has enough
implementation complexity that it's rarely expected outside of very
palindrome-specific interview tracks (see below).
"""


def count_substrings(s: str) -> int:
    total = 0

    for i in range(len(s)):
        l, r = i, i
        while l >= 0 and r < len(s) and s[l] == s[r]:
            total += 1
            l -= 1
            r += 1

    for i in range(len(s)):
        l, r = i, i + 1
        while l >= 0 and r < len(s) and s[l] == s[r]:
            total += 1
            l -= 1
            r += 1
    return total


# ================================================================================
# ALTERNATIVE APPROACH — Dynamic Programming (2D table)
# ================================================================================
"""
### Thought Process 🧠
A different angle on the same O(n^2) result: instead of expanding
outward from centers, build a table bottom-up where `dp[i][j]` answers
"is s[i..j] a palindrome?" using the fact that s[i..j] is a palindrome
exactly when `s[i] == s[j]` AND the INNER substring `s[i+1..j-1]` is
also a palindrome (or is trivially short, length 0 or 1).

### Idea
Fill `dp[i][j]` for all i <= j, processing `i` from n-1 down to 0 (so
`dp[i+1][...]` is always already computed when we need it) and `j` from
i upward. `dp[i][j] = True` when `s[i] == s[j]` and
(`j - i < 2` OR `dp[i+1][j-1]`). Every True entry is one palindromic
substring — sum them all up.

### Why does it work?
This is the classic "palindrome = matching outer characters + palindromic
inner substring" recurrence. Building the table in the right order
(i decreasing, j increasing from i) guarantees `dp[i+1][j-1]` — a smaller
subproblem strictly "inside" the current one — is always ready before
it's needed.

### Complexity
- TC: O(n^2) — fill an n x n table, O(1) work per cell
- SC: O(n^2) — the full DP table

### Pros
- Same time complexity as expand-around-center, with a very clean and
  formal recurrence — some find the correctness argument easier to state
  precisely this way (useful if asked to prove correctness rigorously).
- If OTHER subproblems in a larger question also need "is s[i..j] a
  palindrome?" answered many times, this table serves double duty as a
  reusable lookup structure — expand-around-center doesn't give you that.

### Cons
- O(n^2) SPACE, strictly worse than expand-around-center's O(1) extra
  space, for the exact same O(n^2) time — a straight downgrade if all you
  need is the count.

### DSA Buddy Point 🧠
"Same O(n^2) time as expand-around-center, but trades O(1) space for
O(n^2) space in exchange for a reusable 'is s[i..j] palindrome?' lookup
table — only worth it if you need that table for something else."
"""


def count_substrings_dp(s: str) -> int:
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    total = 0
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i < 2 or dp[i + 1][j - 1]):
                dp[i][j] = True
                total += 1
    return total


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
PALINDROMIC SUBSTRINGS (count all)
│
├── Brute Force
│   └── Check every (i,j) substring with a full two-pointer scan -> O(n^3)
│
├── Bottleneck
│   └── Re-verifies inner-character symmetry that a smarter approach
│       could reuse from smaller, already-confirmed palindromes
│
├── Key Observation
│   └── Every palindrome has a CENTER (single char OR a gap between two
│       chars) — 2n-1 possible centers total
│
├── Path A — Expand Around Center
│   └── For each of the 2n-1 centers, grow outward while symmetric
│       └── O(n^2) time, O(1) space  <-- optimal for this problem, your code
│
└── Path B — DP Table (dp[i][j] = is s[i..j] a palindrome?)
    └── dp[i][j] = s[i]==s[j] AND (short OR dp[i+1][j-1])
        └── O(n^2) time, O(n^2) space  <-- same time, more space, reusable table

(Beyond both: Manacher's Algorithm reaches true O(n) time, but with
 significant implementation complexity — rarely expected unless the
 interview is specifically palindrome-focused.)
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Palindrome problems -> think 'expand around center' as your default
  O(n^2) approach: 2n-1 centers (n odd-length, n-1 even-length)."
- "Expand-around-center avoids re-checking inner symmetry by growing
  outward — each comparison happens once per valid expansion step."
- "DP table (dp[i][j] = s[i]==s[j] AND dp[i+1][j-1]) is the same time
  complexity but trades O(1) space for a reusable O(n^2) lookup table —
  only worth it if you need repeated palindrome-range queries elsewhere."
- "Manacher's Algorithm exists for true O(n) — know that it exists and
  what problem it solves, but implementing it from memory is a stretch
  goal, not a baseline expectation."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                  | Core Idea                                              | TC     | SC     | Pros                                  | Cons                                        | When to Use                          |
|------------------------------|---------------------------------------------------------------|--------|--------|---------------------------------------------|--------------------------------------------------|-------------------------------------------|
| Brute Force                   | Check every substring with a full palindrome scan                | O(n^3) | O(1)   | Trivial to write/verify                      | Cubic — redoes inner symmetry checks repeatedly    | Baseline / correctness check only        |
| Expand Around Center          | Grow outward from each of 2n-1 centers                            | O(n^2) | O(1)   | Optimal space, simple to implement            | None significant for this problem                | Default optimal choice (your code)       |
| DP Table (dp[i][j])           | Bottom-up: palindrome = matching ends + palindromic inside         | O(n^2) | O(n^2) | Reusable lookup table, clean formal recurrence | Strictly more space for the same time              | When you need repeated range-palindrome queries |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Expand Around Center (the standard default for palindrome
  counting/finding problems; same family as "Longest Palindromic
  Substring," which uses the identical center-expansion idea but tracks
  the longest span instead of a running count).
- Go-to answer: "Every palindrome has a center — either a character or a
  gap between two characters, giving 2n-1 candidate centers. Expand
  outward from each while characters match, counting one palindrome per
  successful step. O(n^2) time, O(1) space."
- Good to mention brute force first (O(n^3)) to set the baseline, then
  pivot with "palindromes grow from a center, so let's check from the
  inside out instead of scanning every substring from the outside in."
- Common follow-up: "Can you do better than O(n^2)?" -> Yes, Manacher's
  Algorithm achieves O(n), but it's a specialized technique — worth
  naming and describing the high-level idea (reusing symmetry from
  previously computed palindromes to avoid redundant expansions) even if
  not implementing it live.
"""