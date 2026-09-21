"""
================================================================================
 PROBLEM: First Bad Version (LeetCode 278)
================================================================================
Given: `n` versions, numbered 1 to n, released in order. Once a version is
"bad," EVERY version after it is also bad (a bug introduced in a bad
version persists forward). You're given an API `isBadVersion(version)`
that returns True/False. Find the FIRST bad version, using as few API
calls as possible.

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Is it guaranteed that at least one bad version exists (i.e. version n
  is always bad, or could ALL versions be good)? (LeetCode guarantees at
  least one bad version exists within [1, n])
- Is `isBadVersion` expensive to call (e.g. an actual API call over a
  network in a real system)? (Yes conceptually — "minimize calls" is
  explicitly part of the problem, which is why binary search matters,
  not just correctness)
- Are versions 1-indexed? (Yes — version numbering starts at 1, not 0)
"""

# ================================================================================
# 🔑🔑🔑  STRONG POINTS FOR "FIND FIRST X" PROBLEMS  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   "Once bad, always bad" = a MONOTONIC boolean sequence:            │
    │   good, good, good, ..., good, BAD, bad, bad, ..., bad              │
    │   Exactly ONE flip point — that flip point IS the answer.           │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

Memorize these as REFLEXES for "find the first version/position where a
condition becomes true (and stays true)" problems:

1. **"Once true, always true" is the signal.** Any time a condition has
   this monotonic property — good/bad, valid/invalid, small/big — you're
   looking at a binary-search-on-the-answer problem, whether or not
   there's a literal sorted array in sight.

2. **isBadVersion(mid) == True -> the answer is at mid or to the LEFT.**
   Shrink `r = mid` (NOT `mid - 1` — mid itself could BE the first bad
   version, so it must stay in the search range).

3. **isBadVersion(mid) == False -> the answer is strictly to the RIGHT.**
   Shrink `l = mid + 1` (mid is confirmed good, so it can be safely
   excluded — the first bad version is definitely past it).

4. **Converging pointers (`l < r`), not crossing pointers (`l <= r`).**
   Same template as findPeakElement / findMin: l and r walk toward each
   other and MEET exactly at the answer. Since they converge to the SAME
   value, `return l` and `return r` are interchangeable at the end — see
   the dedicated note below for why.

5. **This problem is "find the FIRST position after a boundary flips" —
   the mirror image of "find the LAST valid position before a boundary"
   (like mySqrt). Recognizing which side your answer sits on tells you
   the shrink direction instantly.**
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea
Just call `isBadVersion(1)`, then `isBadVersion(2)`, then `isBadVersion(3)`,
... in order, and return the first version number where it returns True.
Dead simple, always correct — but if there are a billion versions, and
the FIRST bad version happens to be version 999,999,999, you've just made
nearly a billion API calls to find it. That's the brute force approach.

### The key insight: "once bad, always bad" means you can binary search
Because the sequence of good/bad results is MONOTONIC — once you hit a
bad version, every version after it is guaranteed bad too — you don't
need to check every version one by one. If you check some middle version
and it's BAD, you know the first bad version is somewhere at or before
that point (never later). If it's GOOD, you know the first bad version
is somewhere strictly after that point (never at or before). Either way,
one single API call eliminates HALF the remaining candidates with total
certainty.

### Step-by-step trace: firstBadVersion(n=5), where version 4 is the
    first bad one
```
l=1, r=5

Step 1: mid = (1+5)//2 = 3  -> isBadVersion(3)? FALSE (version 3 is good)
        -> first bad version is strictly AFTER 3 -> l = mid+1 = 4

Step 2: l=4, r=5 -> mid = (4+5)//2 = 4  -> isBadVersion(4)? TRUE
        -> first bad version is AT or BEFORE 4 -> r = mid = 4

Step 3: l=4, r=4 -> l == r, loop ends!

Return 4 (either l or r, they're the same value).  Correct! ✅
```
Notice: only 2 API calls were needed to pinpoint the answer among 5
versions — and this gap grows enormously for large n (about 30 calls
instead of up to a billion, for n around 1 billion).

### Building strong intuition: "which side of the flip am I on?"
Picture the versions laid out left to right: a long run of GOOD versions,
then at some exact point, it flips to BAD and stays BAD forever after.
You're trying to find EXACTLY where that flip happens. Every time you
check a version, you're really asking "am I standing before the flip, or
at/after it?" A GOOD result means "the flip hasn't happened yet, keep
moving right." A BAD result means "I'm at or past the flip — the true
flip point is here or somewhere to my left, never further right than
where I'm standing right now."

### The "aha" moment to remember 🎯
This is functionally the EXACT SAME algorithm shape as `findPeakElement`'s
simplified version and `findMin`'s converging-pointer approach — a
monotonic boolean condition, `while l < r`, shrink toward whichever side
is guaranteed to contain the answer, and trust that convergence alone
(no extra final check needed) lands you exactly on it. Different problem
surface, identical underlying template.
"""

# ================================================================================
# ALTERNATIVE APPROACH — Brute Force (linear scan)
# ================================================================================
"""
### Thought Process 🧠
Call `isBadVersion` for every version starting from 1, in order, and
return the first one that comes back True.

### Idea
`for version in range(1, n+1): if isBadVersion(version): return version`

### Complexity
- TC: O(n) — worst case, the first bad version is the very last one, or
  there's exactly one bad version at the end
- SC: O(1)
- API calls: up to n calls — this is the metric the problem actually
  cares about minimizing, since `isBadVersion` conceptually represents an
  expensive real-world check (e.g. a network call, a test suite run)

### Pros
- Trivial to write, obviously correct.

### Cons
- Makes far too many API calls for large n — the problem explicitly asks
  you to minimize this, not just "get the right answer eventually."

### Bottleneck
Checking versions one at a time completely ignores the "once bad, always
bad" monotonic guarantee — a single check at any point tells you
DEFINITIVELY which whole half of the remaining range to discard, but
linear scanning throws that guarantee away and checks everything anyway.
Ask: "can one check eliminate half the remaining candidates with total
certainty?" -> Yes: binary search (the main approach below).
"""


def first_bad_version_brute(n: int, isBadVersion) -> int:
    for version in range(1, n + 1):
        if isBadVersion(version):
            return version
    return -1


# ================================================================================
# MY APPROACH — Binary Search (converging pointers)
# ================================================================================
"""
### Idea
Classic converging-pointer binary search over the version range [1, n].
If `isBadVersion(mid)` is True, the first bad version is at `mid` or
earlier, so shrink `r = mid` (keep mid in range — it might BE the
answer). If False, the first bad version is strictly after `mid`, so
shrink `l = mid + 1` (mid is confirmed good, safely excluded). Loop while
`l < r`; when they converge, that shared value is the answer.

### Complexity
- TC: O(log n) — search range halves every API call
- SC: O(1)
- API calls: O(log n) — for n around 1 billion, this is roughly 30 calls
  instead of up to a billion — the entire point of the exercise

### Pros
- Optimal number of API calls — directly addresses what the problem is
  actually asking you to minimize.
- Minimal, clean converging-pointer template — no special edge-case
  branches needed.

### DSA Buddy Point 🧠
"'Once true, always true' (monotonic boolean) -> binary search for the
flip point. isBadVersion(mid)==True shrinks r=mid (keep mid, it might be
the answer); False shrinks l=mid+1 (mid is safely excluded)."

### Why `return l` and `return r` are BOTH correct here ⚠️
Same reasoning as findPeakElement's simplified version: because the loop
condition is `while l < r`, the loop can only keep running while `l` and
`r` differ — the instant they become equal, the loop exits. So `l` and
`r` hold the EXACT SAME value when the loop ends; `return l` and
`return r` are two names for the identical number, not two competing
answers. This is the "converging pointers" template (contrast with
mySqrt/searchInsert's `while l <= r`, where `l` and `r` CROSS and end up
genuinely different, making the l-vs-r choice actually matter there).

### What can be improved?
Nothing — O(log n) API calls is optimal. You cannot reliably distinguish
between n+1 possible "first bad version" outcomes (any of the n versions,
or the edge case of none being bad if the problem allowed it) in fewer
than roughly log2(n) calls, since each call only yields one bit of
information (bad or not bad).
"""


def first_bad_version(n: int, isBadVersion) -> int:
    l, r = 1, n

    while l < r:
        mid = (l + r) // 2
        if isBadVersion(mid):
            r = mid
        else:
            l = mid + 1
    return r


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
FIRST BAD VERSION
│
├── Brute Force
│   └── Call isBadVersion(1), (2), (3)... in order -> O(n) calls
│
├── Bottleneck
│   └── Ignores "once bad, always bad" — that guarantee lets ONE call
│       eliminate half the remaining range with certainty
│
├── Key Observation
│   └── good, good, ..., good, BAD, bad, ..., bad — exactly ONE flip
│       point, a monotonic boolean sequence
│
└── Optimization — Converging-Pointer Binary Search
    ├── isBadVersion(mid) == True  -> answer at mid or left -> r = mid
    ├── isBadVersion(mid) == False -> answer strictly right  -> l = mid+1
    ├── Loop while l < r (pointers CONVERGE, don't cross)
    └── l == r at the end -> that's the first bad version
        └── O(log n) API calls  <-- optimal, your code
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "'Once true, always true' (monotonic condition) -> binary search for
  the flip point, even with no literal array — isBadVersion is just a
  black-box monotonic predicate."
- "True result -> shrink r=mid (keep mid, might be the answer). False
  result -> shrink l=mid+1 (mid safely excluded, answer is strictly
  further right)."
- "Converging pointers (`l < r`) mean l and r are IDENTICAL when the loop
  ends — return either one, it doesn't matter which."
- "The metric being optimized here is API CALLS, not just time
  complexity in the abstract — a good reminder that Big-O often stands in
  for a real-world cost (network calls, expensive computations, etc.)."
- "This is the exact same template as findPeakElement's simplified
  version and findMin's converging-pointer approach — recognizing the
  shared shape across different problem surfaces is what makes binary
  search feel 'easy' once you've internalized the pattern."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach            | Core Idea                                      | TC       | API Calls | SC   | Pros                          | Cons                                    | When to Use                       |
|--------------------------|-------------------------------------------------------|----------|-----------|------|--------------------------------------|--------------------------------------------|-----------------------------------------|
| Brute Force               | Check versions 1,2,3,... in order                        | O(n)     | O(n)      | O(1) | Trivial, always correct                | Wastes enormous numbers of API calls for large n | Baseline / correctness check only       |
| Binary Search (converging) | isBadVersion(mid) shrinks r or l toward the flip point    | O(log n) | O(log n)  | O(1) | Optimal API call count, minimal code    | None significant                            | Default optimal choice (your code)      |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Binary Search on a Monotonic Predicate (no array required —
  isBadVersion is a black-box function, but "once bad always bad" is
  exactly the monotonic guarantee binary search needs).
- Go-to answer: "Since bad versions form a monotonic run (once bad,
  always bad), binary search [1, n]: if isBadVersion(mid) is True, the
  answer is at mid or earlier (r = mid); if False, it's strictly later
  (l = mid + 1). Converging pointers land exactly on the first bad
  version in O(log n) calls."
- Good to explicitly frame this as "minimizing an expensive external
  call," not just "minimizing time complexity" — shows you understand
  WHY the problem cares about O(log n) specifically.
- Common follow-up: "What if isBadVersion could be flaky/non-deterministic
  (sometimes wrong)?" -> Binary search breaks down under noisy signals;
  you'd need a different strategy (e.g. repeated sampling / majority vote
  at each step), a good sign of understanding the monotonicity assumption
  this solution fundamentally relies on.
"""

# ================================================================================
# STRONG UNDERSTANDING CHECK 💪
# ================================================================================
"""
If you can confidently answer these without looking back up, you've truly
internalized this problem (not just memorized the code):

1. Q: Why is `r = mid` and not `r = mid - 1` when isBadVersion(mid) is
      True?
   A: Because mid itself might BE the first bad version — excluding it
      with `mid - 1` risks throwing away the correct answer. mid is never
      disqualified by a True result, only confirmed as "bad or later" is
      ruled out to its right.

2. Q: Why is it safe to use `l = mid + 1` (excluding mid) when
      isBadVersion(mid) is False?
   A: A False result definitively PROVES mid is good, and since bad
      versions never "turn back" to good, mid can never be the answer —
      it's safe to fully exclude it from all future consideration.

3. Q: What does this problem have in common with findPeakElement's
      simplified version and findMin's converging-pointer approach, at a
      structural level?
   A: All three use `while l < r` with pointers that CONVERGE (never
      cross), rely on a monotonic guarantee to decide which half to keep,
      and trust the final converged value without needing a separate
      verification step — same template, different surface problem.

4. Q: If isBadVersion(1) returns True immediately, what happens, and is
      the code still correct?
   A: `r` immediately shrinks toward 1 and stays there (every subsequent
      isBadVersion check at higher mids won't even get reached since `r`
      is already pinned near 1) — the loop correctly converges to 1,
      meaning version 1 itself is the first bad version. No special-case
      handling needed; the general logic already covers this.

5. Q: If you had to explain this to someone who's never seen binary
      search before, in one sentence, what would you say?
   A: "I check a version in the middle of what's left — if it's bad, the
      very first bad version must be at or before that point, so I
      narrow my search leftward (but keep that version as a candidate);
      if it's good, the first bad version must be somewhere after it, so
      I narrow rightward — repeating until there's only one version left
      to check, which has to be the answer."
"""
