"""
================================================================================
 PROBLEM: Make The String Great (LeetCode 1544)
================================================================================
Given a string `s` of lower and upper case English letters. A string is
GOOD if it does NOT contain two ADJACENT characters `s[i]` and `s[i + 1]`
such that:
- `s[i]` is a lower-case letter and `s[i + 1]` is the SAME letter in
  upper case, OR
- `s[i]` is an upper-case letter and `s[i + 1]` is the SAME letter in
  lower case.

To make the string good, you may repeatedly choose two adjacent characters
that make the string bad and REMOVE them. Return the string after making it
good. The answer is guaranteed to be unique under the given constraints.
An empty string is also good.

Example: s = "leEeetcode" -> "leetcode"   (remove "eE")
Example: s = "abBAcC"     -> ""           (cascade: "bB", then "aA", then "cC")

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- What makes a pair "bad"? (Two ADJACENT characters that are the SAME letter
  in OPPOSITE cases, in either order: "aA" or "Aa". "aa", "AA" and "aB" are
  all fine. Same letter + same case is NOT a bad pair.)
- After removing a bad pair, can NEW bad pairs form from the characters that
  become adjacent? (Yes — "abBA" -> remove "bB" -> "aA" is now bad -> remove
  -> "". This cascading is the whole reason a stack is the right tool.)
- Does the order in which I remove pairs change the final answer? (No — the
  result is unique, so a left-to-right simulation is valid.)
- Can the result be empty? (Yes — return `""`.)
- What alphabet is allowed? (ONLY English letters, both cases — this makes
  the ASCII "differ by 32" shortcut safe; with other characters it would not
  be.)

"""

# ================================================================================
# 🔑🔑🔑  STRONG POINTS FOR "CANCEL ADJACENT PAIRS" STACK PROBLEMS  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   Removing an adjacent pair can make NEW neighbours touch ->        │
    │   cascading cancellation -> use a STACK of survivors.               │
    │   For each char: if it CANCELS the stack top, pop the top;          │
    │   otherwise push it. The stack at the end IS the answer.            │
    │   "Cancels" here = same letter, OPPOSITE case                       │
    │   <=> stack[-1] == char.swapcase().                                 │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

This is the same skeleton as Remove All Adjacent Duplicates (LC 1047),
Backspace String Compare (LC 844), Valid Parentheses (LC 20) and Asteroid
Collision (LC 735): the stack holds survivors, and only the TOP can interact
with the next character. The only thing that changes is the DEFINITION of
"cancels". Key ideas:

1. **Only the stack TOP can cancel with the incoming character.** Anything
   deeper is already separated from it by the top; if the top doesn't cancel,
   nothing below can.

2. **Cascades are free.** After a pop, the NEW top is automatically the
   neighbour of the next incoming character, so chains like "abBA" collapse
   without any extra loop or rescan. A single `if` (not `while`) is enough
   because each incoming character cancels AT MOST ONE stack element — the
   cancelled partner is gone and the character itself is consumed.

3. **The cancel condition has two parts: same letter AND different case.**
   - same letter:      `stack[-1].lower() == char.lower()`
   - different case:   one is lower, the other is upper
   Your three-part condition expresses this literally. The compact
   equivalent is `stack[-1] == char.swapcase()` — if swapping the case of
   `char` gives exactly the top, they are the same letter in opposite cases.

4. **Same letter, same case does NOT cancel.** `"aa"` must stay. That is why
   `lower() == lower()` alone is wrong — you MUST also require the cases to
   differ (or use `swapcase`, or the `!=` check).

5. **ASCII trick (letters only):** an upper/lower pair differ by exactly 32 in
   code point, i.e. `abs(ord(a) - ord(b)) == 32` (equivalently
   `ord(a) ^ ord(b) == 32`). Valid here only because the input contains
   just English letters.
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea
Scan the string for any adjacent pair like "aA" or "Bb". If you find one,
delete both characters and start scanning from the beginning again. Repeat
until no bad pair is left. Correct, but restarting the scan after every
removal is slow (O(n^2)).

### The key insight: only the latest survivor matters
Build the answer left to right in a stack. When a new character arrives, the
only thing it can possibly cancel is the character currently on TOP (its
left neighbour in the string built so far). If they cancel, pop the top —
and the new top becomes the next neighbour automatically, so cascades happen
for free. If they don't cancel, push the new character.

### Step-by-step trace: makeGood("abBAcC")
```
'a' : stack empty                                -> push      stack=[a]
'b' : top 'a' vs 'b' -> different letters        -> push      stack=[a, b]
'B' : top 'b' vs 'B' -> same letter, opposite
      case -> CANCEL                             -> pop b     stack=[a]
'A' : top 'a' vs 'A' -> same letter, opposite
      case -> CANCEL (cascade!)                  -> pop a     stack=[]
'c' : stack empty                                -> push      stack=[c]
'C' : top 'c' vs 'C' -> CANCEL                   -> pop c     stack=[]
result = "" ✅
```

### Second trace: makeGood("leEeetcode")  (same letter, same case must stay)
```
'l' -> push                                          stack=[l]
'e' -> top 'l' differs                  -> push      stack=[l, e]
'E' -> top 'e' vs 'E' -> CANCEL         -> pop e     stack=[l]
'e' -> top 'l' differs                  -> push      stack=[l, e]
'e' -> top 'e' vs 'e' -> same letter but SAME case,
       NOT a bad pair                   -> push      stack=[l, e, e]
't' 'c' 'o' 'd' 'e' -> no cancels       -> push all  stack=[l,e,e,t,c,o,d,e]
result = "leetcode" ✅
```

### The "aha" moment to remember 🎯
"Cancel-adjacent-pairs => stack of survivors; compare the incoming character
with the TOP only. Define 'cancels' precisely (here: same letter, opposite
case) — the stack skeleton is the same as every other adjacent-cancel
problem."
"""

# ================================================================================
# ALTERNATIVE APPROACH 1 — Brute Force (rescan and remove, repeat)
# ================================================================================
"""
### Thought Process 🧠
Repeatedly scan for the FIRST index `i` where `s[i]` and `s[i + 1]` are the
same letter in opposite cases. Delete both characters (string slicing) and
restart from the beginning. Stop when a full scan finds no bad pair.

### Complexity
- TC: O(n^2) — up to n/2 removals, each costing an O(n) scan plus an O(n)
  string rebuild (Python strings are immutable)
- SC: O(n) — a new string is built at every removal

### Pros
- Literal translation of the statement; easy to trust.
- Great oracle for testing the stack solution.

### Cons
- Quadratic in the worst case (e.g. "aaaa...AAAA" cascades through the whole
  string, one pair at a time, rescanning the long prefix each time).
- Repeated string allocation is slow in Python.

### Bottleneck
After a removal only the junction where two characters just became adjacent
can form a new bad pair, but brute force rescans everything. Ask: "can I
remember only the characters that might still be cancelled?" -> The stack's
top is exactly that junction.
"""


def make_good_brute(s: str) -> str:
    while True:
        for i in range(len(s) - 1):
            if s[i] != s[i + 1] and s[i].lower() == s[i + 1].lower():
                s = s[:i] + s[i + 2:]
                break
        else:
            return s


# ================================================================================
# MY APPROACH — Stack with Explicit "Same Letter, Opposite Case" Check (optimal)
# ================================================================================
"""
### Idea
Iterate through the characters, keeping a stack of survivors. For each
`char`, if the stack is non-empty AND the top is the same letter as `char`
(`lower()` equal) AND they have opposite cases (one lower, one upper), they
cancel: pop the top and do NOT push `char`. Otherwise push `char`. Join the
stack for the answer.

### Complexity
- TC: O(n) — each character is pushed at most once and popped at most once
  (note: `lower()`/`islower()`/`isupper()` on a single character are O(1))
- SC: O(n) — the stack, which is also the returned answer

### Pros
- Single pass, optimal time; the stack is the output (just `join`).
- Handles cascading cancellations ("abBA") automatically — no rescans.
- The condition spells out the problem statement word by word, so it is easy
  to read and justify: same letter + opposite case.
- Correctly leaves "aa" and "AA" alone (same case never cancels).

### Cons
- The condition is longer than necessary; there is redundancy (it checks
  lower-then-upper AND upper-then-lower plus the `lower()` equality).
- Several string-method calls per iteration — slightly slower than a single
  comparison.

### DSA Buddy Point 🧠
"Adjacent-pair cancellation with cascades => stack. Spend your thinking time
on defining 'cancels' precisely; the rest is boilerplate."

### What can be improved?
Complexity-wise nothing — O(n) time is optimal. Your code is correct as
written: it requires the same letter (`lower()` equal) and opposite cases, so
"aa"/"AA" are kept and "aA"/"Aa" are cancelled. Optional simplification:
because letters are only English letters, "same letter and not the same
character" is already "same letter, opposite case", so the whole condition
reduces to `stack and stack[-1] == char.swapcase()` (or
`stack[-1] != char and stack[-1].lower() == char.lower()`). Shorter, fewer
method calls, same behaviour.
"""


class Solution:
    def makeGood(self, s: str) -> str:
        stack = []

        for char in s:
            if (
                stack
                and stack[-1].lower() == char.lower()
                and (
                    (stack[-1].islower() and char.isupper())
                    or (char.islower() and stack[-1].isupper())
                )
            ):
                stack.pop()
            else:
                stack.append(char)
        return "".join(stack)


# ================================================================================
# ALTERNATIVE APPROACH 2 — Stack with `swapcase` Shortcut (cleanest)
# ================================================================================
"""
### Thought Process 🧠
Two characters are a bad pair exactly when one is the OTHER's case-swap:
`'a'.swapcase() == 'A'` and `'A'.swapcase() == 'a'`. So the whole condition is
`stack and stack[-1] == char.swapcase()`. Everything else is the same stack
loop.

### Complexity
- TC: O(n)
- SC: O(n)

### Pros
- One short, obviously-correct condition; trivial to read and to write under
  pressure.
- Same-case pairs ("aa") are automatically safe because `'a'.swapcase()` is
  `'A'`, not `'a'`.

### Cons
- Relies on `swapcase` being a clean involution for the alphabet — true for
  English letters (the problem's constraint), but not for every Unicode
  character (e.g. some characters change length or have no case pair).
- Slightly "clever": some readers need a moment to see why it is equivalent
  to the longer explicit condition.

### DSA Buddy Point 🧠
"Look for a one-line algebraic definition of the cancel relation
(`swapcase`, `abs(diff) == 32`, `a + b == 0`, matching bracket pair)."
"""


def make_good_swapcase(s: str) -> str:
    stack = []
    for char in s:
        if stack and stack[-1] == char.swapcase():
            stack.pop()
        else:
            stack.append(char)
    return "".join(stack)


# ================================================================================
# ALTERNATIVE APPROACH 3 — In-Place Stack on a List with a `top` Pointer
# ================================================================================
"""
### Thought Process 🧠
Convert `s` to a list and use its own prefix as the stack: keep `top` as the
index of the current stack top (-1 if empty). For each character, if `top >= 0`
and `arr[top] == ch.swapcase()` then `top -= 1` (cancel); else `top += 1;
arr[top] = ch`. The write index `top + 1` never passes the read index, so
nothing unread is overwritten. Answer: `"".join(arr[:top + 1])`. A variant
swaps `swapcase` for the ASCII check `abs(ord(a) - ord(b)) == 32`.

### Complexity
- TC: O(n)
- SC: O(n) as written (the list copy of the string), but only O(1) EXTRA beyond
  that if the input were already a mutable char array (e.g. in C++/Java)

### Pros
- Shows the "stack lives in the array's prefix" space-saving trick; maps
  directly to C++/Java solutions that mutate a `string`/`char[]` in place.
- No `append`/`pop` overhead; the final join slices the prefix once.

### Cons
- Index arithmetic (`top + 1`, `top -= 1`) is easier to get off-by-one than
  `append`/`pop`.
- In Python strings are immutable, so you still pay O(n) to copy into a list
  — no real asymptotic benefit here.

### DSA Buddy Point 🧠
"A stack that never grows beyond the number of characters read can live INSIDE
the input buffer: `top` is the stack pointer."
"""


def make_good_inplace(s: str) -> str:
    arr = list(s)
    top = -1
    for ch in s:
        if top >= 0 and arr[top] == ch.swapcase():
            top -= 1
        else:
            top += 1
            arr[top] = ch
    return "".join(arr[: top + 1])


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
MAKE THE STRING GREAT
│
├── Brute Force
│   └── Rescan for an adjacent "aA"/"Aa" pair, delete it, restart -> O(n^2)
│
├── Bottleneck
│   └── A removal only creates a new neighbour at ONE junction, but brute
│       force rescans the whole string every time
│
├── Key Insight
│   └── Cancel adjacent pairs with cascades => STACK of survivors; compare the
│       incoming char with the TOP only (same letter, opposite case)
│
├── My Approach — Stack + explicit condition (optimal)
│   └── stack[-1].lower() == char.lower() and cases differ
│       -> pop; else push -> O(n) time, O(n) space
│
├── Stack with swapcase shortcut (cleanest)
│   └── stack[-1] == char.swapcase() -> same O(n), one-line condition
│       (ASCII variant: abs(ord(a) - ord(b)) == 32)
│
└── In-Place Stack (top pointer on a list)
    └── arr[top + 1] = ch / top -= 1 -> O(n) time, O(1) extra for mutable
        buffers
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Adjacent cancellation with cascades => STACK. Compare the incoming item
  with the top only; if they cancel, pop; else push."
- "Define 'cancels' precisely: SAME letter AND OPPOSITE case. 'aa' must stay,
  so `lower() == lower()` alone is wrong."
- "`stack[-1] == char.swapcase()` is the compact, exact equivalent of the
  long condition (for English letters)."
- "`if`, not `while`: an incoming character can cancel at most one top —
  after the pop, the character is consumed and not pushed."
- "Cascades come for free: after a pop the new top is automatically the next
  neighbour — no rescan needed."
- "ASCII shortcut: lower and upper forms of a letter differ by exactly 32 —
  valid only because the input is restricted to English letters."
- "O(n) total: each character is pushed once and popped at most once."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                         | Core Idea                                               | TC     | SC        | Pros                                              | Cons                                                    | When to Use                          |
|----------------------------------|---------------------------------------------------------|--------|-----------|---------------------------------------------------|---------------------------------------------------------|--------------------------------------|
| Brute Force                      | Rescan for "aA"/"Aa", delete, restart                   | O(n^2) | O(n)      | Literal translation, perfect oracle for tests     | Quadratic, repeated string rebuilds                     | Baseline / correctness check         |
| Stack + explicit condition       | Pop if same letter AND opposite case, else push         | O(n)   | O(n)      | Optimal, reads like the statement, cascades free  | Verbose condition, several method calls per char        | Default optimal choice (your code)   |
| Stack + swapcase shortcut        | Pop if stack[-1] == char.swapcase()                     | O(n)   | O(n)      | One-line condition, very hard to get wrong        | Relies on letters-only input / clean case mapping       | Cleanest version to write in practice|
| In-Place Stack (top pointer)     | Use the array prefix as the stack with an index         | O(n)   | O(1)*     | Space-trick showcase, maps to C++/Java in-place   | Off-by-one prone, no real gain in Python                | Follow-up: "reduce extra space?"     |

*O(1) extra only for a mutable char buffer; Python still copies into a list.

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Stack Simulation — adjacent-pair cancellation with cascades.
  Cousins: LC 1047 (Remove All Adjacent Duplicates), LC 1209 (Remove All
  Adjacent Duplicates II), LC 844 (Backspace String Compare), LC 735
  (Asteroid Collision), LC 20 (Valid Parentheses).
- Go-to answer: "Use a stack of survivors. For each character, if the stack
  top is the same letter in the opposite case (`stack[-1] ==
  char.swapcase()`), pop it; otherwise push the character. The stack is the
  answer. O(n) time, O(n) space."
- Good to call out: why only the top can cancel, why cascades need no extra
  loop, and that same-case pairs ("aa") must NOT cancel.
- Common follow-ups:
  * "Can you do it without extra space?" -> In-place `top` pointer on a
    mutable char buffer (Java/C++), or note Python strings are immutable.
  * "What if cancelling required k equal adjacent characters (LC 1209)?" ->
    Stack of (char, count); pop when count reaches k.
  * "What if the pair rule were different (e.g. digits summing to 10)?" ->
    Only the `cancels(a, b)` predicate changes; the stack skeleton stays.
  * "Does the removal order matter?" -> No: the final string is unique, so
    left-to-right greedy is valid.
"""