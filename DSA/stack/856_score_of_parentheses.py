"""
================================================================================
 PROBLEM: Score of Parentheses (LeetCode 856)
================================================================================
Given a BALANCED parentheses string `s`, return the SCORE of the string.
The score of a balanced parentheses string is defined recursively:
- `"()"` has score 1.
- `AB` has score `A + B`, where A and B are balanced parentheses strings.
- `(A)` has score `2 * A`, where A is a balanced parentheses string.

Example: s = "()"         -> 1
Example: s = "(())"       -> 2
Example: s = "()()"       -> 2
Example: s = "(()(()))"   -> 6   ( 2 * ( "()" + "(())" ) = 2 * (1 + 2) )

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Is the input GUARANTEED balanced? (Yes — only '(' and ')' and always valid, so
  I never need to handle an unmatched bracket or an empty stack on ')'.)
- Is "(A)" worth 2 * A even when A is a concatenation like "()()"? (Yes — the
  whole inside is doubled: "(()())" = 2 * (1 + 1) = 4, NOT 1 + 1 doubled
  piecewise differently. Nesting multiplies, concatenation adds.)
- What is the size limit? (n <= 50, so the score is at most about 2^24 — no
  overflow concerns in Python; in other languages a 32-bit int is enough.)
- Do I need the score of "" ? (Not required by the statement; treat it as 0 in
  helper functions so that "inside of ()" is naturally 0 / or handle "()" as
  the base case 1.)

"""

# ================================================================================
# 🔑🔑🔑  STRONG POINTS FOR "SCORE / VALUE OF A NESTED STRUCTURE" PROBLEMS  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   Keep a STACK of partial scores, one per open parenthesis level.   │
    │     '('  -> start a new level (push a placeholder)                  │
    │     ')'  -> close the level: its score is   max(2 * inner, 1)       │
    │             (inner == 0 means "()" which is worth exactly 1)        │
    │             and it is ADDED to the score of the enclosing level.    │
    │   Or, without any stack:  every "()" contributes 2^depth, where     │
    │   depth = number of parentheses enclosing it. Sum them all.         │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

This is the "evaluate a nested expression" cousin of Decode String (LC 394) and
Valid Parentheses (LC 20): the structure is nested like brackets, but each
closing bracket COMBINES the contents of its level into a number. Key ideas:

1. **The grammar gives exactly two combination rules:** concatenation ADDS
   (`AB = A + B`), enclosure DOUBLES (`(A) = 2A`), with `"()" = 1` as the base.

2. **A stack of per-level partial sums models it perfectly.** Each open
   parenthesis opens a level whose running sum starts at 0. When it closes:
   `value = max(2 * inner, 1)` (an empty inner level means "()", worth 1), and
   `value` is added to the enclosing level's running sum.

3. **Your solution's two branches are the same rule:** pushing `1` when the
   top is `'('` is the case `inner = 0 -> 1`; the `else` branch is
   `inner > 0 -> 2 * inner`. They can be merged into a single path that pops
   until `'('` and pushes `max(2 * inner, 1)`.

4. **Why the final `sum(stack)`:** several top-level primitives side by side
   (e.g. `"()(())"`) leave several values on the stack — concatenation adds.

5. **Depth view (O(1) space):** unfolding all the doublings, every "()" leaf is
   multiplied by 2 once for each enclosing pair, so it contributes `2^depth`.
   Detect a leaf as a `')'` whose previous character is `'('`.
   `"(()(()))"`: leaves at depth 1 and 2 contribute 2^1 + 2^2 = 6.

6. **Each value is pushed once and popped at most once -> O(n) time** even though
   there is a `while` inside the loop (amortized).
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea (follow the definition)
Split the string into its top-level balanced pieces (use a balance counter to
find where the first piece ends). For a piece that is exactly "()" the score is
1; otherwise it is `(A)` and the score is `2 * score(A)`. The score of the whole
string is the sum of the scores of its pieces. This is correct but slices
strings repeatedly -> O(n^2) in the worst case.

### The key insight: combine on the way OUT
Process left to right. Whenever a ')' closes a level, you know everything inside
that level, so you can compute its value immediately and hand it to the level
around it. A stack of partial results is exactly "the levels currently open".

### Step-by-step trace (your stack): "(()(()))"
Stack holds '(' markers and integer scores.
```
'(' -> push                                   stack=[ ( ]
'(' -> push                                   stack=[ (, ( ]
')' -> top is '(' : "()" -> pop, push 1        stack=[ (, 1 ]
'(' -> push                                   stack=[ (, 1, ( ]
'(' -> push                                   stack=[ (, 1, (, ( ]
')' -> top is '(' : "()" -> pop, push 1        stack=[ (, 1, (, 1 ]
')' -> top is 1: sum ints until '(' = 1,
       pop '(' , push 2*1 = 2                  stack=[ (, 1, 2 ]
')' -> top is 2: sum ints until '(' = 2 + 1 = 3,
       pop '(' , push 2*3 = 6                  stack=[ 6 ]
sum(stack) = 6 ✅
```

### Same input, "stack of per-level scores": start with stack=[0]
```
'(' -> push 0                                  [0, 0]
'(' -> push 0                                  [0, 0, 0]
')' -> v=pop()=0, w=pop()=0, push w+max(2v,1)=1   [0, 1]
'(' -> push 0                                  [0, 1, 0]
'(' -> push 0                                  [0, 1, 0, 0]
')' -> v=0, w=0 -> push 0+1 = 1                [0, 1, 1]
')' -> v=1, w=1 -> push 1 + max(2,1) = 3        [0, 3]
')' -> v=3, w=0 -> push 0 + max(6,1) = 6        [6]
answer = 6 ✅
```

### Depth trace (O(1) space): "(()(()))"
```
'(' depth=1
'(' depth=2
')' depth=1, previous char was '(' -> leaf at depth 1: ans += 2^1 = 2
'(' depth=2
'(' depth=3
')' depth=2, previous char was '(' -> leaf at depth 2: ans += 2^2 = 4   (ans=6)
')' depth=1, previous char was ')' -> not a leaf
')' depth=0, previous char was ')' -> not a leaf
answer = 6 ✅
```

### The "aha" moment to remember 🎯
"Concatenation adds, enclosure doubles, '()' is 1. Either keep per-level partial
sums on a stack, or notice that each '()' is worth 2^(its nesting depth)."
"""

# ================================================================================
# ALTERNATIVE APPROACH 1 — Brute Force: Recursive Split by Balanced Primitives
# ================================================================================
"""
### Thought Process 🧠
Directly implement the definition. Find the end of the FIRST balanced piece by
scanning with a balance counter (+1 for '(', -1 for ')', stop at 0). If that
piece is "()" its score is 1; otherwise it is `(A)` and its score is
`2 * score(A)` where A is the piece with its outer parentheses removed. Add the
score of the remaining suffix (the rest of the concatenation).

### Complexity
- TC: O(n^2) worst case — each recursive call scans and slices strings, e.g.
  "((((...))))" or "()()()..." re-scans / re-slices O(n) per level or per piece
- SC: O(n) recursion depth plus O(n) per slice copy (up to O(n^2) total
  allocation in the worst case)

### Pros
- A literal transcription of the problem statement; trivially correct.
- Perfect oracle for validating the optimized versions.

### Cons
- Quadratic time and heavy string copying.
- Deep nesting means deep recursion (fine for n <= 50, a problem in general).

### Bottleneck
Every call re-scans characters that a previous call already scanned to find its
boundary. Ask: "can I compute each level's score while scanning ONCE, and hand
it to the enclosing level on the way out?" -> Yes: a stack (or an index-based
recursive descent).
"""


def score_brute(s: str) -> int:
    if not s:
        return 0
    balance = 0
    end = 0
    for i, ch in enumerate(s):
        balance += 1 if ch == "(" else -1
        if balance == 0:
            end = i
            break
    first, rest = s[: end + 1], s[end + 1 :]
    first_score = 1 if first == "()" else 2 * score_brute(first[1:-1])
    return first_score + score_brute(rest)


# ================================================================================
# MY APPROACH — Stack of '(' Markers and Integer Scores (optimal time)
# ================================================================================
"""
### Idea
Push every '('. On ')':
- if the top is '(' the pair is "()" -> pop it and push the score 1;
- otherwise the top is an integer: pop and add up all integers until the
  matching '(' (these are the scores of the pieces concatenated inside this
  level), pop the '(' and push `2 * total`.
After the scan, the stack holds the scores of the top-level pieces; their sum
is the answer.

### Complexity
- TC: O(n) — each pushed integer is popped at most once (amortized); the
  inner `while` never re-visits an element
- SC: O(n) — the stack (up to n / 2 entries for fully nested input)

### Pros
- Mirrors the definition: "()" -> 1, concatenation -> add (the inner sum loop),
  enclosure -> double.
- Handles top-level concatenation naturally via the final `sum(stack)`.
- Single pass, optimal time, easy to explain.

### Cons
- The stack mixes TYPES ('(' strings and integers), so the code needs the
  `stack[-1] != "("` comparison against a string while popping integers.
- Two branches implement what is really one rule (`max(2 * inner, 1)`): pushing
  1 for "()" is the case `inner = 0`. The duplication invites copy-paste bugs.
- O(n) extra space, whereas the depth formula needs O(1).
- `stack and stack[-1] == "("` — the `stack and` check is unnecessary for a
  balanced input (the stack is never empty at a ')').

### DSA Buddy Point 🧠
"Nested structure with a numeric combine rule: push markers, and when a closing
token arrives, fold everything above the marker into one number and push it
back — the same shape as Decode String."

### What can be improved?
Correctness is fine (verified against brute force below). Optional: merge the
two branches — pop integers until '(' (an empty fold gives 0), pop '(', then
push `max(2 * count, 1)`. Or use the stack-of-ints version (next), or the O(1)
depth formula.
"""


class Solution:
    def scoreOfParentheses(self, s: str) -> int:
        stack = []

        for char in s:
            if char == "(":
                stack.append(char)
            elif stack and stack[-1] == "(":
                stack.pop()
                stack.append(1)
            else:
                count = 0
                while stack and stack[-1] != "(":
                    count += stack.pop()
                stack.pop()
                stack.append(count * 2)
        return sum(stack)


# ================================================================================
# ALTERNATIVE APPROACH 2 — Stack of Per-Level Integer Scores (cleanest stack)
# ================================================================================
"""
### Thought Process 🧠
Keep a stack of integers, one per currently open level, starting with a single
`0` for the top level. On '(' push a fresh `0`. On ')': pop the finished
level's score `v`, pop the enclosing level's running score `w`, and push
`w + max(2 * v, 1)` — `max(2 * v, 1)` handles both `"()" (v = 0 -> 1)` and
`(A) (v > 0 -> 2v)`. The answer is the single value left on the stack.

### Complexity
- TC: O(n) — constant work per character
- SC: O(n) — stack depth equals the maximum nesting depth + 1

### Pros
- Homogeneous int stack, ONE rule for closing a level, no inner `while` loop.
- No separate "()" case and no final `sum` (everything folds into the level
  below).
- Space is O(max depth), which can be much smaller than O(n) for flat strings
  like "()()()...".

### Cons
- The initial `0` for the outer level and the `max(2v, 1)` trick need a moment
  to understand.
- Still O(depth) extra space (the next approach is O(1)).

### DSA Buddy Point 🧠
"One running total per open level: close a level -> convert it into a value and
add it to its parent."
"""


def score_level_stack(s: str) -> int:
    stack = [0]
    for ch in s:
        if ch == "(":
            stack.append(0)
        else:
            v = stack.pop()
            w = stack.pop()
            stack.append(w + max(2 * v, 1))
    return stack[0]


# ================================================================================
# ALTERNATIVE APPROACH 3 — Depth Counting: Each "()" Contributes 2^depth (O(1) space)
# ================================================================================
"""
### Thought Process 🧠
Unfold the rules: each enclosing pair doubles everything inside, and
concatenation adds, so the final score is the sum, over every innermost "()",
of `2^(number of pairs enclosing it)`. Scan once while tracking `depth`
(number of currently open parentheses). On ')', decrement `depth`; if the
character just before was '(' this ')' closes a leaf "()" at the current
`depth`, so add `1 << depth`.

### Complexity
- TC: O(n)
- SC: O(1) — two integers (`depth`, `ans`) and the previous character

### Pros
- Optimal time and space; no stack and no recursion.
- Gives a neat closed form: score = sum of 2^depth over all "()" leaves.

### Cons
- Needs the unfolding insight; harder to derive from scratch than the stack.
- Easy to be off by one on `depth`: decrement BEFORE computing `1 << depth`
  (the leaf's depth excludes itself).
- `1 << depth` fits easily here (n <= 50) but could overflow fixed-width ints in
  other languages for larger inputs.

### DSA Buddy Point 🧠
"When nesting multiplies and concatenation adds, expand the multiplications:
each leaf is worth the product of the multipliers above it (2 per level)."
"""


def score_depth(s: str) -> int:
    depth = 0
    ans = 0
    prev = ""
    for ch in s:
        if ch == "(":
            depth += 1
        else:
            depth -= 1
            if prev == "(":
                ans += 1 << depth
        prev = ch
    return ans


# ================================================================================
# ALTERNATIVE APPROACH 4 — Recursive Descent with a Shared Index (O(n))
# ================================================================================
"""
### Thought Process 🧠
Parse the grammar directly. `parse()` reads consecutive balanced pieces at the
current level until it meets a ')' (or the end), summing their scores: for each
'(' it advances; if the next character is ')' the piece is "()" worth 1;
otherwise it recurses to score the inside, doubles it, and skips the matching
')'. A shared index `i` ensures every character is read exactly once.

### Complexity
- TC: O(n) — each character is consumed once (no slicing)
- SC: O(depth) — recursion depth equals the maximum nesting depth

### Pros
- Mirrors the grammar (`S -> (S) S | ε`) exactly; very readable and extendable
  (e.g., different multipliers or other bracket types).
- Fixes the brute-force version's quadratic slicing by using indices.

### Cons
- Recursion depth equals nesting depth (fine for n <= 50, risky for 10^5 in
  Python without raising the recursion limit).
- A shared mutable index (`nonlocal i`) is slightly awkward.

### DSA Buddy Point 🧠
"A recursive-descent parser is the call-stack version of the explicit stack:
each recursive call is one open level."
"""


def score_recursive(s: str) -> int:
    i = 0

    def parse() -> int:
        nonlocal i
        total = 0
        while i < len(s) and s[i] == "(":
            i += 1  # consume '('
            if s[i] == ")":
                total += 1  # "()" leaf
            else:
                total += 2 * parse()  # (A) -> 2 * A
            i += 1  # consume ')'
        return total

    return parse()


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
SCORE OF PARENTHESES
│
├── Brute Force
│   └── Split into balanced pieces by a counter; "()" = 1, (A) = 2*score(A),
│       sum the pieces -> O(n^2) (string slicing / re-scanning)
│
├── Bottleneck
│   └── Boundaries of each piece are rediscovered by re-scanning; slices copy
│       strings
│
├── Key Insight
│   └── Concatenation ADDS, enclosure DOUBLES, "()" = 1. Fold each level into
│       a number when its ')' arrives and hand it to the enclosing level
│
├── My Approach — Stack of '(' markers and ints (OPTIMAL time)
│   └── "()" -> push 1; else sum ints to '(' and push 2*sum; answer = sum(stack)
│       -> O(n) time, O(n) space (mixed types, two branches)
│
├── Stack of per-level int scores
│   └── v=pop, w=pop, push w + max(2v, 1) -> O(n) time, O(depth) space
│
├── Depth counting (OPTIMAL space)
│   └── each "()" adds 2^depth -> O(n) time, O(1) space
│
└── Recursive descent (index-based)
    └── parse(): "()" -> 1, "(A)" -> 2*parse(); sum the pieces
        -> O(n) time, O(depth) recursion
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Rules: '()' = 1, AB = A + B, (A) = 2A. Concatenation adds, enclosure
  doubles."
- "Closing a level: value = max(2 * inner, 1) — the max handles the empty
  inner case '()' = 1 in the same formula."
- "Stack of per-level sums: push 0 on '(', on ')' do `v = pop(); w = pop();
  push(w + max(2v, 1))`."
- "Depth formula: answer = sum of 2^depth over every '()' leaf, where depth is
  the number of enclosing pairs (decrement depth BEFORE shifting)."
- "Leaf detection: a ')' whose previous character is '(' ."
- "Top-level concatenation ('()()') is why your stack solution ends with
  `sum(stack)`."
- "O(n) time even with an inner `while`: every pushed value is popped at most
  once."
- "Cousins: LC 394 (Decode String), LC 20 (Valid Parentheses), LC 921 (Min Add
  to Make Valid), LC 1249, LC 1021 (Remove Outermost Parentheses), LC 726
  (Number of Atoms)."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                       | Core Idea                                                     | TC     | SC        | Pros                                                 | Cons                                                        | When to Use                              |
|--------------------------------|---------------------------------------------------------------|--------|-----------|------------------------------------------------------|-------------------------------------------------------------|------------------------------------------|
| Brute Force (recursive split)  | Split into balanced pieces; "()"=1, (A)=2*score(A); sum       | O(n^2) | O(n)      | Literal definition, great oracle                     | Quadratic, string slicing, deep recursion                   | Baseline / correctness check             |
| Stack of markers and ints      | push '('; "()"->1; else sum ints to '(' and push 2*sum        | O(n)   | O(n)      | Mirrors the definition, final sum handles concatenation | Mixed types, two near-duplicate branches                  | Default answer (your code)               |
| Stack of per-level int scores  | push 0 on '('; on ')' push w + max(2v, 1)                     | O(n)   | O(depth)  | One rule, int-only, no inner loop                    | `max(2v, 1)` trick and initial 0 need explaining            | Cleanest stack version                   |
| Depth counting (2^depth)       | each "()" leaf contributes 2^depth                            | O(n)   | O(1)      | Optimal time and space, no stack                     | Needs the unfolding insight; depth off-by-one risk          | Follow-up: "O(1) space?"                 |
| Recursive descent (index)      | parse() sums pieces; recurse on '(' ... ')' ; 2 * inner       | O(n)   | O(depth)  | Mirrors the grammar, extendable                      | Recursion depth, shared mutable index                       | Grammar-style / parser discussions       |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Stack for nested structure with a numeric fold (per-level partial
  results). Relatives: LC 394 (Decode String), LC 20 (Valid Parentheses), LC 921
  (Min Add to Make Valid), LC 726 (Number of Atoms), LC 1021 (Remove Outermost
  Parentheses), LC 224 (Basic Calculator).
- Go-to answer: "Use a stack of partial scores, one per open level. On '(' push
  0. On ')' pop the finished level's score v and the enclosing level's running
  score w, and push w + max(2*v, 1) — 1 if the level was empty (the pair '()'),
  else double it. The answer is the one value left. O(n) time, O(depth) space.
  Alternatively every '()' contributes 2^depth, giving an O(1)-space scan."
- Good to call out: concatenation adds vs. enclosure doubles, why `max(2*v, 1)`
  merges the two cases, and the 2^depth insight for O(1) space.
- Common follow-ups:
  * "Can you do it in O(1) space?" -> Track `depth` and add `1 << depth` for each
    "()" leaf.
  * "What if '()' were worth some other base value, or the multiplier were k?"
    -> Base value b and multiplier k: leaf contributes `b * k^depth`.
  * "What if the input might be unbalanced?" -> Validate first (LC 20 / LC 921
    style) or guard each pop against an empty stack.
  * "Return the score modulo 10^9+7 for huge inputs?" -> Keep the stack/depth
    approach and apply `pow(2, depth, MOD)`.
"""