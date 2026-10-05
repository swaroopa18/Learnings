"""
================================================================================
 PROBLEM: Backspace String Compare (LeetCode 844)
================================================================================
Given two strings `s` and `t`, return `True` if they are EQUAL when both are
typed into empty text editors. The character `'#'` means a BACKSPACE.

Note that after backspacing an EMPTY text, the text will continue empty
(backspace on nothing does nothing).

Example: s = "ab#c", t = "ad#c" -> both become "ac" -> True.
Example: s = "a#c",  t = "b"    -> "c" vs "b"        -> False.

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- What does `'#'` do on an EMPTY editor? (Nothing — the text stays empty.
  This is the edge case that forces the `if stack:` guard before `pop()`.)
- Can several `'#'` appear in a row? (Yes — each one erases one more
  character to the left, so "ab##" -> "" and "a##b" -> "b".)
- Is `'#'` ever a real character to compare? (No — it is ALWAYS a backspace,
  so it never appears in the final text.)
- What characters/lengths are allowed? (Lowercase letters and '#', lengths up
  to 200 — so O(n^2) would pass, but the interview follow-up asks for O(n)
  time and O(1) extra space.)
- Do I compare the final TEXTS, or the keystrokes? (Final texts after all
  backspaces are applied.)

"""

# ================================================================================
# 🔑🔑🔑  STRONG POINTS FOR "UNDO / BACKSPACE" STRING PROBLEMS  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   Typing text with backspaces IS a stack:                           │
    │     letter     -> push                                              │
    │     backspace  -> pop (only if the stack is non-empty)              │
    │   The stack at the end IS the final text.                           │
    │   O(1)-SPACE follow-up: a backspace erases characters to its LEFT,  │
    │   so scan BOTH strings from the END with a SKIP COUNTER — then      │
    │   you meet every '#' BEFORE the letters it deletes.                 │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

This is the simplest "simulate with a stack" problem — a warm-up for Asteroid
Collision, Remove All Adjacent Duplicates, Decode String and Valid
Parentheses. Key ideas:

1. **Backspace = pop, letter = push.** The stack always equals the text
   currently in the editor, so after processing the string it is the final
   answer — no cleanup required.

2. **Guard the pop: `if stack:`.** Backspacing an empty editor must do
   nothing; calling `pop()` on an empty list would raise an `IndexError`.

3. **Compare the FINAL strings, not the inputs.** `s` and `t` can have
   different lengths and different keystrokes yet produce the same text
   ("a#c" vs "b#c" -> both "c"; "xy##z#w" vs "w#w" -> both "w").

4. **Helper function for both strings** — build the same stack logic once
   (`filtered`) and apply it to `s` and `t`; keeps the code symmetric and
   removes copy-paste bugs.

5. **O(1)-space trick: scan from the RIGHT.** Going left-to-right you can't
   know whether a letter will be erased until you see later `'#'`s (hence the
   stack). Going right-to-left, every `'#'` is seen before the letters it
   erases, so a simple counter `skip` tells you "ignore the next `skip`
   letters" — no stack needed.
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea
Literally simulate the editor: whenever you see `'#'`, delete it AND the
character just before it (if any). Repeat until no `'#'` remains, then compare.
Works, but each deletion rebuilds the string -> O(n^2).

### The key insight: an editor is a stack
The text behind the cursor behaves exactly like a stack: typing pushes a
letter onto the end, backspace pops the most recent letter. One left-to-right
pass builds the final text in O(n).

### Step-by-step trace: s = "xy##z#w", t = "w#w"
```
filtered("xy##z#w"):
  'x' -> push                          stack=[x]
  'y' -> push                          stack=[x, y]
  '#' -> pop y                         stack=[x]
  '#' -> pop x                         stack=[]
  'z' -> push                          stack=[z]
  '#' -> pop z                         stack=[]
  'w' -> push                          stack=[w]
  result = "w"

filtered("w#w"):
  'w' -> push                          stack=[w]
  '#' -> pop w                         stack=[]
  'w' -> push                          stack=[w]
  result = "w"

"w" == "w"  -> True ✅
```

### Edge-case trace: backspace on empty text — s = "#a", t = "a"
```
filtered("#a"):
  '#' -> stack empty, nothing to pop   stack=[]      (the guard matters!)
  'a' -> push                          stack=[a]
  result = "a"          filtered("a") = "a"  -> True ✅
```

### The "aha" moment to remember 🎯
"Undo/backspace/delete-previous operations => STACK. Letter pushes, '#'
pops (guarded by non-empty). For O(1) space: scan from the end and count how
many characters still need to be skipped."
"""

# ================================================================================
# ALTERNATIVE APPROACH 1 — Brute Force (repeatedly delete "char#" pairs)
# ================================================================================
"""
### Thought Process 🧠
Repeatedly find the FIRST `'#'` in the string. If it is at index 0, just
remove it (nothing to erase). Otherwise remove it together with the single
character right before it. Continue until no `'#'` is left; compare the two
results.

### Complexity
- TC: O(n^2) — up to n/2 removals, each doing an O(n) search and an O(n)
  string rebuild (Python strings are immutable)
- SC: O(n) — a new string is created at every removal

### Pros
- Mirrors the statement exactly; trivial to trust and verify.
- Good oracle to test faster solutions against.

### Cons
- Quadratic time and repeated string re-allocation.
- Finding the first `'#'` again and again re-scans the same prefix.

### Bottleneck
After a deletion only the character just before the cursor can be affected by
the next backspace, yet we restart from the beginning. Ask: "can I keep only
the part of the text that might still be erased?" -> That is the stack.
"""


def _apply_backspaces_brute(text: str) -> str:
    while "#" in text:
        i = text.index("#")
        if i == 0:
            text = text[1:]
        else:
            text = text[: i - 1] + text[i + 1:]
    return text


def backspace_compare_brute(s: str, t: str) -> bool:
    return _apply_backspaces_brute(s) == _apply_backspaces_brute(t)


# ================================================================================
# MY APPROACH — Build the Final Text with a Stack, Then Compare (optimal time)
# ================================================================================
"""
### Idea
Write one helper `filtered(st)` that walks the string once: push every letter,
and on `'#'` pop the top IF the stack is non-empty. Return the stack joined
into a string. Then `s` and `t` are equal as typed iff `filtered(s) ==
filtered(t)`.

### Complexity
- TC: O(n + m) — each string is scanned once; every character is pushed at
  most once and popped at most once. (`"".join` and the final comparison are
  also linear.)
- SC: O(n + m) — the two stacks / resulting strings

### Pros
- Simplest correct solution; very hard to get wrong.
- A single helper is reused for both strings -> symmetric, no duplication.
- Clearly shows the "backspace = pop" insight interviewers look for.
- The `if stack:` guard handles backspace-on-empty correctly, and consecutive
  `'#'`s (even more `'#'`s than letters) just work.

### Cons
- Uses O(n + m) extra space; the standard follow-up asks for O(1) extra space
  (see the two-pointer approach below).
- Builds both complete final strings even if the very first characters already
  differ (no early exit).

### DSA Buddy Point 🧠
"Whenever an operation removes the MOST RECENT item (undo, backspace, remove
last duplicate, cancel adjacent pair), a stack is the natural model."

### What can be improved?
Complexity-wise nothing in time — O(n + m) is optimal since every character
must be read. Your code is correct as written: letters are pushed, `'#'`
pops only when the stack is non-empty, and the final texts are compared.
Two optional polish points: (1) you can skip the `"".join(...)` and compare
the stack lists directly (`filtered_list(s) == filtered_list(t)`), saving a
small allocation; (2) if the follow-up asks for O(1) space, switch to the
right-to-left skip-counter approach below.
"""


class Solution:
    def backspaceCompare(self, s: str, t: str) -> bool:
        def filtered(st):
            stack = []
            for char in st:
                if char == "#":
                    if stack:
                        stack.pop()
                else:
                    stack.append(char)
            return "".join(stack)

        return filtered(s) == filtered(t)


# ================================================================================
# ALTERNATIVE APPROACH 2 — Two Pointers from the End with Skip Counters (O(1) space)
# ================================================================================
"""
### Thought Process 🧠
A backspace deletes characters to its LEFT, so process both strings from the
RIGHT. Keep a pointer in each string. For each pointer, "settle" it onto the
next character that actually survives: walk left, and for every `'#'`
increment a `skip` counter; for every letter, if `skip > 0` consume one skip
(that letter is erased), otherwise stop — this letter is visible. Compare the
two visible letters; if they differ (or exactly one string ran out), return
`False`. Move both pointers left and repeat.

### Complexity
- TC: O(n + m) — each pointer moves left across its string once
- SC: O(1) — only a few integer variables (no stack, no new strings)

### Pros
- The answer to the classic follow-up "can you do it in O(1) extra space?".
- Early exit: returns `False` at the FIRST mismatching visible character
  without ever building full strings.

### Cons
- Much trickier to write correctly than the stack: skip-counter handling and
  the three "one string ended / both ended / mismatch" cases are easy to
  get wrong.
- Easy to forget that both pointers must be re-settled each iteration, or to
  treat a letter before a pending `'#'` as visible.
- More code and harder to explain under interview pressure.

### DSA Buddy Point 🧠
"If a deletion affects things to its LEFT, scan from the RIGHT: you meet the
deleter first, so a counter replaces the stack. Reverse scan + counter = the
O(1)-space version of many 'undo' stack problems."
"""


def backspace_compare_two_pointers(s: str, t: str) -> bool:
    def next_valid(text: str, idx: int) -> int:
        skip = 0
        while idx >= 0:
            if text[idx] == "#":
                skip += 1
            elif skip > 0:
                skip -= 1  # this letter is erased by a later '#'
            else:
                break  # visible letter
            idx -= 1
        return idx  # -1 if no more visible letters

    i, j = len(s) - 1, len(t) - 1
    while i >= 0 or j >= 0:
        i = next_valid(s, i)
        j = next_valid(t, j)
        if i < 0 and j < 0:
            return True  # both exhausted simultaneously
        if i < 0 or j < 0:
            return False  # one has visible letters left, the other doesn't
        if s[i] != t[j]:
            return False
        i -= 1
        j -= 1
    return True


# ================================================================================
# ALTERNATIVE APPROACH 3 — Reverse Generators + zip_longest (lazy, O(1) space)
# ================================================================================
"""
### Thought Process 🧠
Same right-to-left idea, but package the "yield the next visible letter"
logic into a generator `visible(text)`. Then compare the two lazy streams with
`itertools.zip_longest` (using a sentinel for the shorter stream). Because
generators are lazy, no final string is built and the comparison stops at the
first difference.

### Complexity
- TC: O(n + m)
- SC: O(1) extra (a couple of integers per generator; `zip_longest` is lazy)

### Pros
- Much more readable than manual two-pointer bookkeeping: the generator hides
  the skip-counter logic, and `zip_longest` handles "one string is longer"
  automatically.
- Lazy evaluation gives the same early-exit behaviour as the pointer version.

### Cons
- Relies on generators and `itertools`, which may feel like "cheating" in an
  interview that wants explicit pointer manipulation.
- Slightly more Python-specific; harder to port line-by-line to Java/C++.
- Generator overhead makes it a little slower in practice than the plain
  loop version for small inputs.

### DSA Buddy Point 🧠
"Encapsulate the tricky traversal (reverse + skip counter) in a generator,
then the comparison logic becomes a one-liner."
"""


def backspace_compare_generators(s: str, t: str) -> bool:
    from itertools import zip_longest

    def visible(text: str):
        skip = 0
        for ch in reversed(text):
            if ch == "#":
                skip += 1
            elif skip > 0:
                skip -= 1
            else:
                yield ch

    sentinel = object()
    return all(
        a == b for a, b in zip_longest(visible(s), visible(t), fillvalue=sentinel)
    )


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
BACKSPACE STRING COMPARE
│
├── Brute Force
│   └── Repeatedly delete first "char#" pair via string slicing -> O(n^2)
│
├── Bottleneck
│   └── Restarts the search from the beginning after every deletion and
│       rebuilds immutable strings each time
│
├── Key Insight
│   └── The editor text is a STACK: letter -> push, '#' -> pop (if non-empty)
│       The stack at the end is the final text
│
├── My Approach — Stack Build + Compare (BEST for simplicity)
│   └── filtered(s) == filtered(t) -> O(n + m) time, O(n + m) space
│       -> guard `if stack:` for backspace on empty text
│
├── Two Pointers from the End (O(1) space)
│   └── Backspace deletes to the LEFT -> scan from the RIGHT with a skip
│       counter; compare visible letters one by one
│       -> O(n + m) time, O(1) space, early exit on first mismatch
│
└── Reverse Generators + zip_longest
    └── Generator yields visible letters from the end; zip_longest compares
        lazily -> O(n + m) time, O(1) extra space, very readable
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Backspace / undo / delete-last => STACK. Letter pushes, '#' pops, the
  stack IS the final text."
- "Guard the pop with `if stack:` — backspace on empty text does nothing and
  `pop()` on an empty list would crash."
- "Compare FINAL strings, never the raw inputs — different keystrokes can
  produce identical text (and different lengths too)."
- "Reuse one helper for both strings so the two sides can never drift apart
  in logic."
- "O(1)-space follow-up: scan from the END. A '#' only affects characters to
  its left, so going right-to-left you meet each '#' before its victims; a
  `skip` counter replaces the stack."
- "In the two-pointer version, handle three cases after settling both
  pointers: both exhausted -> True; exactly one exhausted -> False; letters
  differ -> False."
- "Consecutive '#'s (even more than there are letters) are fine: the counter
  or the guarded pop simply stops at empty."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                     | Core Idea                                                | TC        | SC        | Pros                                               | Cons                                                      | When to Use                          |
|------------------------------|----------------------------------------------------------|-----------|-----------|----------------------------------------------------|-----------------------------------------------------------|--------------------------------------|
| Brute Force                  | Repeatedly remove first "char#" with string slicing      | O(n^2)    | O(n)      | Mirrors the statement, perfect oracle for tests    | Quadratic, repeated immutable-string rebuilds             | Baseline / correctness check         |
| Stack Build + Compare        | letter push, '#' guarded pop; compare final strings      | O(n + m)  | O(n + m)  | Simplest, hardest to get wrong, reusable helper    | O(n + m) space, no early exit                             | Default choice (your code)           |
| Two Pointers from the End    | Right-to-left scan with skip counters, compare visible   | O(n + m)  | O(1)      | Optimal space, early exit on first mismatch        | Fiddly skip/ending cases, easy to slip                    | Follow-up: "O(1) extra space?"       |
| Reverse Generators           | Generator of visible letters + zip_longest comparison    | O(n + m)  | O(1)      | Readable O(1)-space version, lazy early exit       | Relies on generators/itertools, slightly slower           | Pythonic O(1)-space answer           |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Stack Simulation (undo / backspace) with an O(1)-space
  right-to-left skip-counter variant. Cousins: LC 1047 (Remove All Adjacent
  Duplicates), LC 735 (Asteroid Collision), LC 20 (Valid Parentheses),
  LC 71 (Simplify Path), LC 394 (Decode String).
- Go-to answer: "Process each string with a stack: push letters, pop on '#'
  (only if non-empty). The stacks are the final texts, so compare them.
  O(n + m) time, O(n + m) space. For O(1) space, scan both strings from the
  right with a skip counter, comparing the next visible character of each."
- Good to call out: the empty-stack guard, why a right-to-left scan is
  what makes O(1) space possible, and that both pointers must be re-settled
  to the next visible letter on every iteration.
- Common follow-ups:
  * "Can you do it in O(1) extra space?" -> Right-to-left two pointers with
    skip counters (or the generator version).
  * "What if '#' deleted a whole WORD / the previous token?" -> Same stack
    on tokens instead of characters.
  * "What if the text is streamed and can't be stored?" -> Right-to-left
    won't work on a forward-only stream; you must keep the stack (or at least
    the surviving suffix) in memory.
  * "Add 'undo of undo' (redo)?" -> Keep a second stack of popped items to
    support redo.
"""