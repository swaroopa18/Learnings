"""
================================================================================
 PROBLEM: Longest Valid Parentheses (LeetCode 32)
================================================================================
Given a string `s` containing only '(' and ')', return the LENGTH of the
longest valid (well-formed) parentheses SUBSTRING.

Example: s = "(()"      -> 2   ("()")
Example: s = ")()())"    -> 4   ("()()")
Example: s = ""          -> 0

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Substring or subsequence? (SUBSTRING — contiguous. "(()" has answer 2, and
  a subsequence reading would not change that, but "()(()" would differ:
  contiguous gives 2, subsequence gives 4. Contiguity is what creates the
  "walls" that make this problem tricky.)
- What counts as valid? (Every '(' is matched by a later ')' and every ')' by
  an earlier '(' inside the substring: running balance never goes below 0 and
  ends at exactly 0.)
- Can the string be empty / have no valid pair? (Yes -> answer 0.)
- Only '(' and ')' characters? (Yes — no other characters to skip.)
- How large can `n` be? (Up to 3 * 10^4 -> O(n^3) is hopeless, O(n^2) is
  borderline (~4.5 * 10^8 steps), the intended solution is O(n).)

"""

# ================================================================================
# 🔑🔑🔑  STRONG POINTS FOR "LONGEST VALID PARENTHESES" PROBLEMS  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   Keep a stack of INDICES whose top is always the LAST UNMATCHED    │
    │   position (the "wall") — seed it with -1.                          │
    │       '('  -> push i                                                │
    │       ')'  -> pop; if stack is empty, i is a new wall -> push i     │
    │               else valid length ending at i = i - stack[-1]         │
    │   Answer = max of those lengths.                                    │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

This is a cousin of Valid Parentheses (LC 20), but instead of a yes/no you need
a LENGTH, so you must remember WHERE things happen — hence indices, not chars.

1. **Valid = running balance never negative, ends at 0.** A counter is enough
   to VALIDATE one substring; you only need a stack when you want to locate
   boundaries.

2. **A valid substring can only end where a ')' closes something.** After
   popping the matching '(' the new stack top is the index just BEFORE the
   valid block starts, so `length = i - stack[-1]`.

3. **The -1 base index is the whole trick.** It acts as a virtual wall to the
   left of the string. Without it, a valid block starting at index 0 has no
   left neighbour to subtract from.

4. **An unmatched ')' is a permanent wall.** When a ')' arrives and the stack
   has nothing to pop (only the base wall left), nothing to its left can ever
   join a valid block that crosses it. Push i as the new wall.

5. **Unmatched '(' are walls too, just temporary.** Whatever '(' indices stay
   on the stack at the end are exactly the unmatched ones; the valid blocks
   are the gaps BETWEEN consecutive stack entries.

6. **Adjacent valid blocks merge automatically.** In "()()" the second ')' pops
   its '(' and the top is still the wall before the FIRST pair, so the length
   spans both pairs (4, not 2). This is why we subtract the WALL, not the
   matching '(' index.

7. **Why O(n^3) brute force is the natural first answer:** try every substring
   and validate each in O(n). Fix the start and stop early on a negative
   balance and it drops to O(n^2); the stack/counter tricks drop it to O(n).
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea
Look at EVERY substring `s[i..j]`. For each one ask "is it valid?" using the
classic Valid-Parentheses check (a stack, or just a counter that goes +1 for
'(' and -1 for ')'). Keep the longest valid length. Correct, but there are
O(n^2) substrings and each check costs O(n) -> O(n^3).

### Cheap upgrade: stop validating from scratch
If you fix the start `i` and extend `j` one char at a time, you can keep ONE
running balance instead of re-scanning. If the balance ever drops below 0 the
prefix can never recover, so `break`. If it hits 0, `s[i..j]` is valid. That is
O(n^2) with O(1) space — fine to mention, but still too slow in the worst case.

### The key insight: remember the last "wall"
When scanning left to right, the only thing that matters about the past is
"where did the current valid block START?" i.e. where is the last unmatched
character. A stack of indices tracks exactly that:
- '(' is a candidate wall for now: push its index.
- ')' tries to cancel the most recent '(' (pop). If the stack still has an
  entry afterwards, that entry is the last unmatched index, so everything
  between it and `i` is valid. If the stack is EMPTY, this ')' had nothing to
  match: it is a hard wall, push it.
- Seed the stack with -1 so "start of string" is also a wall.

### Step-by-step trace (stack with -1 base): s = ")()())"
```
stack = [-1], best = 0
i=0 ')': pop -1 -> stack empty -> push 0 (new wall)        stack=[0]
i=1 '(': push 1                                           stack=[0,1]
i=2 ')': pop 1 -> top is 0 -> len = 2-0 = 2                stack=[0]   best=2
i=3 '(': push 3                                           stack=[0,3]
i=4 ')': pop 3 -> top is 0 -> len = 4-0 = 4                stack=[0]   best=4
i=5 ')': pop 0 -> stack empty -> push 5 (new wall)        stack=[5]
max length = 4 ✅
```
Notice at i=4 the length is 4, not 2: the wall is still index 0, so the block
"()()" counts as one run.

### Second trace (unmatched '(' stays as a wall): s = "(()"
```
stack = [-1], best = 0
i=0 '(': push 0                                           stack=[-1,0]
i=1 '(': push 1                                           stack=[-1,0,1]
i=2 ')': pop 1 -> top is 0 -> len = 2-0 = 2                stack=[-1,0] best=2
max length = 2 ✅   (index 0 is an unmatched '(' wall, left on the stack)
```

### The "aha" moment to remember 🎯
"A valid block is the gap between two walls. Walls are unmatched characters:
an unmatched ')' becomes a wall when the stack is empty, an unmatched '(' just
stays on the stack. Seed with -1 and the length is always `i - stack[-1]`."
"""

# ================================================================================
# MY APPROACH 1 — Brute Force: Every Substring + Stack Validation (O(n^3))
# ================================================================================
"""
### Idea
Enumerate every substring `s[i..j]`. Validate it with the classic stack:
push on '(', pop on ')', fail if a ')' finds an empty stack, and succeed only
if the stack is empty at the end. Track the longest valid length.

### Complexity
- TC: O(n^3) — O(n^2) substrings x O(n) validation each
- SC: O(n) — the validation stack (up to the substring length)

### Pros
- The most literal translation of the problem definition; very hard to get wrong.
- Reuses the well-known Valid Parentheses check (LC 20) unchanged.
- Perfect oracle for testing the faster solutions.

### Cons
- n up to 3 * 10^4 -> ~10^13 operations; guaranteed TLE.
- Re-validates overlapping substrings from scratch over and over.
- The stack stores characters, but only its SIZE ever matters — wasted memory.

### Bottleneck
Two sources of waste: (1) the validity check re-scans the substring even
though `s[i..j]` shares everything with `s[i..j-1]`; (2) the stack only needs to
know HOW MANY '(' are open, not which ones. Ask: "can a single integer replace
the stack?" -> Yes (next approach).

### DSA Buddy Point 🧠
"If a stack only ever stores identical items, replace it with a counter."

### What can be improved?
Correctness-wise your code is fine (`return True if len(stack) == 0 else False`
is just `return not stack`). To speed it up, swap the stack for a counter
(your second solution), then stop re-validating by extending `j` incrementally
(see Alternative 1), then go O(n) with the index stack.
"""


class SolutionBruteStack:
    def longestValidParentheses(self, s: str) -> int:
        def validParentheses(l, r):
            stack = []
            for i in range(l, r + 1):
                char = s[i]
                if char == "(":
                    stack.append(char)
                elif stack:
                    stack.pop()
                else:
                    return False
            return True if len(stack) == 0 else False

        max_val = 0
        for i in range(len(s)):
            for j in range(i, len(s)):
                if validParentheses(i, j):
                    max_val = max(max_val, j - i + 1)
        return max_val


# ================================================================================
# MY APPROACH 2 — Brute Force: Every Substring + Counter Validation (O(n^3), O(1))
# ================================================================================
"""
### Idea
Same enumeration of all substrings, but validate with a single integer
`count`: +1 for '(', -1 for ')'. If `count` ever goes negative the substring
is invalid (a ')' with nothing to match). It is valid iff `count == 0` at the
end.

### Complexity
- TC: O(n^3) — still O(n^2) substrings x O(n) validation
- SC: O(1) — only a counter

### Pros
- Drops the validation space from O(n) to O(1).
- Shows the key reduction: for ONE bracket type, a counter is equivalent to a
  stack.
- Early `return False` on a negative count prunes some work inside each check.

### Cons
- Same O(n^3) time as before; the improvement is only in space.
- Still re-scans every substring from its first character.
- Checks odd-length substrings too, which can never be valid.

### DSA Buddy Point 🧠
"With a single bracket type, validity = (balance never < 0) AND (final balance
== 0). No stack needed to VALIDATE — only to LOCATE boundaries."

### What can be improved?
Your code is correct. Three quick wins: (1) skip odd lengths (`(j - i + 1) % 2`),
(2) keep ONE running counter while `j` grows instead of re-validating, and
`break` as soon as it is negative — that is O(n^2) (Alternative 1),
(3) use the index stack to reach O(n).
"""


class SolutionBruteCounter:
    def longestValidParentheses(self, s: str) -> int:
        def validParentheses(l, r):
            count = 0
            for i in range(l, r + 1):
                char = s[i]
                if char == "(":
                    count += 1
                else:
                    count -= 1
                    if count < 0:
                        return False
            return count == 0

        max_val = 0
        for i in range(len(s)):
            for j in range(i, len(s)):
                if validParentheses(i, j):
                    max_val = max(max_val, j - i + 1)
        return max_val


# ================================================================================
# MY APPROACH 3 — Index Stack with -1 Base (O(n) time, O(n) space, canonical)
# ================================================================================
"""
### Idea
Keep a stack of indices where the TOP is always the last unmatched position.
Seed it with -1. For each index `i`:
- '(' -> push `i`.
- ')' -> pop. If the stack is now EMPTY, this ')' was unmatched: push `i` as
  the new base wall. Otherwise the current valid block runs from
  `stack[-1] + 1` to `i`, so its length is `i - stack[-1]`.
Return the maximum length seen.

### Complexity
- TC: O(n) — each index is pushed once and popped at most once
- SC: O(n) — worst case all '(' (e.g. "((((") fills the stack

### Pros
- One pass, one stack, easy to code once the -1 trick is understood.
- Handles merging of adjacent valid blocks for free ("()()" -> 4).
- The same wall-based idea generalizes to other "longest valid ..." problems.

### Cons
- The `if not stack: push i` branch plus the -1 seed is a classic off-by-one
  trap.
- Uses O(n) extra space; the two-pass counter solution gets O(1).
- Non-obvious: the stack stores walls, not "open brackets" as in LC 20.

### DSA Buddy Point 🧠
"Seed the stack with -1. On ')' pop; if empty push i (new wall), else the answer
candidate is i - stack[-1]. The stack top is always the last unmatched index."

### What can be improved?
Correct as written. Optional cleanup: the `else` after `if not stack` can stay
as is — it is already minimal. If the interviewer asks for O(1) space, switch to
the two-pass counter approach (Alternative 3).
"""


class Solution:
    def longestValidParentheses(self, s: str) -> int:
        stack = [-1]
        max_len = 0

        for i in range(len(s)):
            if s[i] == "(":
                stack.append(i)
            else:
                stack.pop()
                if not stack:
                    stack.append(i)
                else:
                    max_len = max(max_len, i - stack[-1])
        return max_len


# ================================================================================
# ALTERNATIVE APPROACH 1 — Fix Start, Extend End with a Running Balance (O(n^2))
# ================================================================================
"""
### Thought Process 🧠
For each start `i`, walk `j` forward keeping ONE running balance. If it goes
below 0, no extension can ever fix it -> `break`. If it equals 0, `s[i..j]` is
valid -> update the best length. No re-validation, no extra memory.

### Complexity
- TC: O(n^2) — n starts x up to n extensions, each O(1)
- SC: O(1)

### Pros
- Tiny change from your counter brute force that removes a whole factor of n.
- O(1) space and trivial to reason about.
- Early `break` makes typical inputs much faster than the worst case.

### Cons
- Still quadratic: a long string like "((((...(" never breaks early.
- ~4.5 * 10^8 steps at n = 3 * 10^4 -> risky/slow in Python.

### DSA Buddy Point 🧠
"Don't recompute a property from scratch for each endpoint — carry it
incrementally as the endpoint advances."
"""


def longest_valid_quadratic(s: str) -> int:
    n = len(s)
    best = 0
    for i in range(n):
        bal = 0
        for j in range(i, n):
            bal += 1 if s[j] == "(" else -1
            if bal < 0:
                break
            if bal == 0:
                best = max(best, j - i + 1)
    return best


# ================================================================================
# ALTERNATIVE APPROACH 2 — Dynamic Programming (dp[i] = longest valid ending at i)
# ================================================================================
"""
### Thought Process 🧠
Let `dp[i]` = length of the longest valid substring ENDING at index `i`
(a valid substring can only end with ')', so '(' gives 0).
For `s[i] == ')'`:
- Case `s[i-1] == '('`  ("...()"): `dp[i] = dp[i-2] + 2`.
- Case `s[i-1] == ')'`  ("...))"): the block ending at `i-1` has length
  `dp[i-1]`; the char just before it is `j = i - dp[i-1] - 1`. If `s[j] == '('`
  it matches our ')' -> `dp[i] = dp[i-1] + 2 + dp[j-1]` (the extra term glues
  on a valid block that sits immediately before `j`).
Answer = `max(dp)`.

### Complexity
- TC: O(n) — one pass, O(1) work per index
- SC: O(n) — the dp array

### Pros
- Clean recurrence; shows you can model it as optimal substructure.
- Gives the longest valid length for EVERY ending position, not just the max.

### Cons
- Index arithmetic (`i - dp[i-1] - 1`, `j - 1`) with bounds checks is
  error-prone.
- Same O(n) space as the stack, with more edge cases.

### DSA Buddy Point 🧠
"For substrings, define dp[i] as 'best ending exactly at i' and look back
`dp[i-1]` chars to find what could pair with the current character."
"""


def longest_valid_dp(s: str) -> int:
    n = len(s)
    dp = [0] * n
    best = 0
    for i in range(1, n):
        if s[i] == ")":
            if s[i - 1] == "(":
                dp[i] = (dp[i - 2] if i >= 2 else 0) + 2
            else:
                j = i - dp[i - 1] - 1
                if j >= 0 and s[j] == "(":
                    dp[i] = dp[i - 1] + 2 + (dp[j - 1] if j >= 1 else 0)
            best = max(best, dp[i])
    return best


# ================================================================================
# ALTERNATIVE APPROACH 3 — Two Passes with Counters (O(n) time, O(1) space)
# ================================================================================
"""
### Thought Process 🧠
Scan left to right counting `open_` and `close`. When they are equal the
substring since the last reset is valid -> candidate `2 * close`. If `close`
exceeds `open_` the prefix is broken -> reset both to 0.
This pass misses cases with extra '(' that never close, e.g. "(()" (open
stays ahead, so equality is never reached after the first '('). So do the
mirror pass right to left: reset when `open_ > close`.

### Complexity
- TC: O(n) — two linear scans
- SC: O(1) — a few integers

### Pros
- Best space complexity; no stack, no array.
- Very short code once the "why two passes" argument is clear.

### Cons
- Needs the argument for WHY two directions are required (an unmatched '('
  blocks the left-to-right equality check; an unmatched ')' blocks the
  right-to-left one).
- Less obviously correct than the stack; harder to extend to other variants.

### DSA Buddy Point 🧠
"One pass only 'sees' unmatched ')' as walls. Scan from the other side to make
unmatched '(' visible. Each direction handles the walls the other cannot."
"""


def longest_valid_two_pass(s: str) -> int:
    best = 0
    open_ = close = 0
    for ch in s:
        if ch == "(":
            open_ += 1
        else:
            close += 1
        if open_ == close:
            best = max(best, 2 * close)
        elif close > open_:
            open_ = close = 0

    open_ = close = 0
    for ch in reversed(s):
        if ch == ")":
            close += 1
        else:
            open_ += 1
        if open_ == close:
            best = max(best, 2 * open_)
        elif open_ > close:
            open_ = close = 0
    return best


# ================================================================================
# ALTERNATIVE APPROACH 4 — Mark Matched Pairs, Then Longest Run of Marks
# ================================================================================
"""
### Thought Process 🧠
Use a normal LC 20 stack of '(' indices. When a ')' matches the top '(', mark
BOTH indices as matched in a boolean array. Afterwards, the answer is the
longest run of consecutive True values — adjacent matched pairs and nested
pairs form contiguous marked runs automatically.

### Complexity
- TC: O(n) — one pass to mark, one pass to find the longest run
- SC: O(n) — the stack and the marker array

### Pros
- Very easy to explain: "match brackets, then measure the longest matched run".
- No -1 seed or wall bookkeeping to get wrong.

### Cons
- Two passes and two O(n) structures.
- Slightly more memory than the single index stack.

### DSA Buddy Point 🧠
"Turn a 'valid substring' question into 'longest run of marked positions' by
marking everything that gets matched."
"""


def longest_valid_marks(s: str) -> int:
    n = len(s)
    matched = [False] * n
    stack: list[int] = []
    for i, ch in enumerate(s):
        if ch == "(":
            stack.append(i)
        elif stack:
            matched[stack.pop()] = True
            matched[i] = True
    best = run = 0
    for flag in matched:
        run = run + 1 if flag else 0
        best = max(best, run)
    return best


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
LONGEST VALID PARENTHESES
│
├── Brute Force
│   └── Every substring + O(n) validity check -> O(n^3) time
│
├── Bottleneck
│   └── Re-validating overlapping substrings from scratch; a stack of chars is
│       overkill (a counter suffices to validate); what we really need is the
│       LOCATION of the last unmatched character
│
├── Key Insight
│   └── Valid blocks are the gaps between "walls" (unmatched chars).
│       Track the last wall with an index stack seeded by -1:
│       length = i - stack[-1]
│
├── My Approach 1 — Brute Force + Stack Validation
│   └── O(n^3) time, O(n) space
│
├── My Approach 2 — Brute Force + Counter Validation
│   └── O(n^3) time, O(1) space
│
├── My Approach 3 — Index Stack with -1 Base (OPTIMAL, canonical)
│   └── '(' push i; ')' pop, empty -> push i else len = i - top
│       -> O(n) time, O(n) space
│
├── Fix Start + Running Balance
│   └── break when balance < 0 -> O(n^2) time, O(1) space
│
├── Dynamic Programming
│   └── dp[i] = best valid ending at i; look back dp[i-1] chars
│       -> O(n) time, O(n) space
│
├── Two Passes with Counters (OPTIMAL space)
│   └── L->R reset on close > open; R->L reset on open > close
│       -> O(n) time, O(1) space
│
└── Mark Matched + Longest Run
    └── mark both indices on each match; longest True run
        -> O(n) time, O(n) space
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Validity for one bracket type = balance never negative AND final balance 0.
  A counter validates; an INDEX stack locates boundaries."
- "Seed the stack with -1: it is the virtual wall left of index 0, so a valid
  block starting at 0 still has `i - stack[-1]` = its full length."
- "On ')': pop first. If the stack is EMPTY, this ')' is unmatched -> push i as
  the new wall. Otherwise length = i - stack[-1]."
- "The stack top is always the LAST UNMATCHED index, so adjacent valid blocks
  like '()()' merge automatically (length 4, not 2)."
- "Subtract the WALL (new top after the pop), NOT the popped '(' index — the
  popped index would only measure the innermost pair."
- "Two-pass counters: left-to-right fails to see unmatched '(', right-to-left
  fails to see unmatched ')'. Doing both covers every case in O(1) space."
- "DP: for '))' look at j = i - dp[i-1] - 1; if s[j] == '(' then
  dp[i] = dp[i-1] + 2 + dp[j-1]."
- "Cousins: LC 20 (Valid Parentheses), LC 22 (Generate Parentheses), LC 301
  (Remove Invalid Parentheses), LC 921 (Min Add to Make Valid), LC 1249
  (Min Remove to Make Valid), LC 84 (Largest Rectangle — also a stack of
  indices with boundaries)."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                     | Core Idea                                              | TC        | SC    | Pros                                         | Cons                                              | When to Use                           |
|------------------------------|--------------------------------------------------------|-----------|-------|----------------------------------------------|---------------------------------------------------|---------------------------------------|
| Brute + Stack Validation     | Every substring, validate with a char stack            | O(n^3)    | O(n)  | Literal, trivially correct, great oracle     | TLE; re-validates from scratch                    | Baseline (your first code)            |
| Brute + Counter Validation   | Every substring, validate with a balance counter       | O(n^3)    | O(1)  | Shows stack -> counter reduction             | Still cubic                                       | Stepping stone (your second code)     |
| Fix Start + Running Balance  | Extend j, break when balance < 0                       | O(n^2)    | O(1)  | Tiny change, big win, no extra memory        | Still quadratic on inputs like "((((("            | "Can you do better than cubic?"       |
| Index Stack with -1 Base     | Stack top = last unmatched index; len = i - top        | O(n)      | O(n)  | Canonical interview answer, merges blocks    | -1 seed / empty-stack branch is off-by-one prone  | Best answer to write (your third code)|
| Dynamic Programming          | dp[i] = longest valid ending at i                      | O(n)      | O(n)  | Per-index answers, clear recurrence          | Fiddly index math and bounds checks               | "Can you model it as DP?"             |
| Two-Pass Counters            | Scan both directions, reset on imbalance               | O(n)      | O(1)  | Optimal space, very short                    | Needs the "why two passes" argument               | Follow-up: "O(1) extra space?"        |
| Mark Matched + Longest Run   | Mark matched indices, find longest True run            | O(n)      | O(n)  | Easiest to explain                           | Two passes, two structures                        | When you want the simplest reasoning  |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Stack of INDICES (not characters) used to find boundaries of a valid
  block. Cousins: LC 20 (Valid Parentheses), LC 84 (Largest Rectangle in
  Histogram — same "index stack, length = i - new_top - 1" shape), LC 301,
  LC 921, LC 1249.
- Go-to answer: "Brute force checks every substring in O(n^3). Instead, keep a
  stack of indices whose top is the last unmatched position, seeded with -1.
  On '(' push the index. On ')' pop; if the stack is empty, push the current
  index as a new wall, otherwise the valid length ending here is i - stack[-1].
  Track the max. O(n) time, O(n) space. If you want O(1) space, scan left to
  right and right to left with open/close counters, resetting on imbalance."
- Good to call out: why -1 is the seed, why we subtract the wall instead of the
  popped index, why adjacent blocks merge, and why the two-pass counter needs
  both directions.
- Common follow-ups:
  * "Can you do it in O(1) space?" -> Two-pass counters (Alternative 3).
  * "Return the substring itself, not just its length?" -> Store the best
    `(start, end)` = `(stack[-1] + 1, i)` whenever you update the max.
  * "What if there are other characters in the string?" -> Ignore them in the
    counter/stack logic but keep indices on the real string, or treat them as
    walls depending on the spec.
  * "Count how many longest valid substrings there are?" -> Track a count
    alongside the max length when updating in the stack solution.
"""


# ================================================================================
# SELF-CHECK: all approaches agree with the brute-force oracle
# ================================================================================
if __name__ == "__main__":
    import random

    impls = [
        SolutionBruteStack().longestValidParentheses,
        SolutionBruteCounter().longestValidParentheses,
        Solution().longestValidParentheses,
        longest_valid_quadratic,
        longest_valid_dp,
        longest_valid_two_pass,
        longest_valid_marks,
    ]

    fixed = {"": 0, "(()": 2, ")()())": 4, "()(()": 2, "()()": 4, "))((": 0, "(()())": 6}
    for text, expected in fixed.items():
        for f in impls:
            assert f(text) == expected, (f, text)

    random.seed(0)
    for _ in range(2000):
        text = "".join(random.choice("()") for _ in range(random.randint(0, 14)))
        oracle = SolutionBruteCounter().longestValidParentheses(text)
        for f in impls:
            assert f(text) == oracle, (f, text, oracle)
    print("All approaches agree with the brute-force oracle.")