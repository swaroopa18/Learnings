"""
================================================================================
 PROBLEM: Decode String (LeetCode 394)
================================================================================
Given an encoded string, return its decoded string. The encoding rule is
`k[encoded_string]`, where `encoded_string` inside the square brackets is
repeated EXACTLY `k` times. `k` is a positive integer (possibly several
digits). The input is always valid: no extra whitespace, brackets are well
formed, and digits appear ONLY as repeat counts (never as part of the text,
e.g. there is no "3a" or "2[2]"). Encodings can be NESTED.

Example: s = "3[a]2[bc]"            -> "aaabcbc"
Example: s = "3[a2[c]]"             -> "accaccacc"
Example: s = "2[abc]3[cd]ef"        -> "abcabccdcdcdef"

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Can `k` have MORE than one digit? (Yes — "100[leetcode]" is valid. Reading
  a single digit is the #1 bug: you must accumulate `k = k * 10 + digit`, or
  collect all consecutive digits.)
- Can encodings be nested? (Yes — "3[a2[c]]". Nesting is exactly why a stack
  (or recursion) is needed: the INNERMOST bracket must be expanded first.)
- Do digits ever appear as normal text inside brackets? (No — digits are only
  repeat counts. That is what makes `isdigit()` a safe test for "this is a
  count" and lets the decoded text be treated as letters only.)
- Is the input guaranteed valid? (Yes — no need to handle unmatched brackets
  or a missing number; if it weren't, add validation.)
- How large can the output be? (Up to ~10^5 characters, so building the
  decoded string is fine, but repeatedly copying large strings deserves
  attention.)

"""

# ================================================================================
# 🔑🔑🔑  STRONG POINTS FOR "NESTED ENCODING / EXPRESSION" STACK PROBLEMS  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   NESTED structure => the most recently opened bracket must be      │
    │   closed FIRST => STACK (or recursion, which is a hidden stack).    │
    │   Push everything until you see ']'. Then UNWIND back to the       │
    │   matching '[', read the number just before it, repeat the text,    │
    │   and PUSH THE RESULT BACK as a single piece so outer levels can    │
    │   treat it as ordinary text.                                        │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

Same family as Valid Parentheses (LC 20), Basic Calculator (LC 224), Remove
Duplicate Letters and Asteroid Collision (LC 735): a stack that stores
partial results until a closing token tells you it's time to combine them.
Key ideas:

1. **`]` is the trigger.** Everything before it that is still on the stack
   belongs to the innermost open bracket. Until you see `]`, just push.

2. **Unwind in three steps on `]`:**
   (a) pop until `[` to collect the inner text (it comes out REVERSED);
   (b) pop `[`, then pop the DIGITS before it to read `k` (again reversed);
   (c) push `k * inner_text` back onto the stack.

3. **The pieces come out in reverse order -> reverse before joining.** Both the
   inner text and the digits are popped last-to-first, so
   `"".join(reversed(...))` restores the original order.

4. **Multi-digit numbers:** keep popping while the top is a digit, then
   `int("".join(reversed(digits)))`. Reading only one digit breaks
   "10[a]" and "100[b]".

5. **Pushing the decoded block back as ONE element** is what makes nesting
   work: when the outer `]` arrives, the inner expansion is already just a
   chunk of text sitting on the stack. (`isdigit()` on that chunk is False —
   decoded text never consists of digits only, since digits are counts.)

6. **Two classic stack layouts for this problem:**
   (i) one stack of characters/strings that you unwind on `]` (your code);
   (ii) two stacks — one for pending counts, one for pending text prefixes —
   updated on `[` and `]`, never unwinding character by character.
   Both are O(output) time; (ii) avoids the digit-popping/reversing step.

7. **Recursion mirrors the stack:** a recursive-descent parser calls itself on
   `[` and returns on `]`; the call stack replaces the explicit stack.
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea
Find an innermost, bracket-free pattern like `2[c]` (a number, `[`, letters,
`]`), replace it with its expansion (`cc`), and repeat until no brackets are
left. A regex can find such patterns for you. It works because the innermost
pattern never contains another bracket, so it is always safe to expand first.

### The key insight: closing brackets arrive in the right order
Reading left to right, the first `]` you meet always closes the INNERMOST open
`[`. So you never need to search for the innermost group — the stack hands it
to you: everything above the most recent `[` is its content.

### Step-by-step trace (your approach): decodeString("3[a2[c]]")
Stack holds characters AND decoded chunks.
```
'3' -> push                        stack=[3]
'[' -> push                        stack=[3, [ ]
'a' -> push                        stack=[3, [, a]
'2' -> push                        stack=[3, [, a, 2]
'[' -> push                        stack=[3, [, a, 2, [ ]
'c' -> push                        stack=[3, [, a, 2, [, c]
']' -> unwind:
        pop until '[' -> inner = reversed([c]) = "c";  pop '['
        pop digits    -> "2" -> k = 2
        push 2 * "c" = "cc"        stack=[3, [, a, cc]
']' -> unwind:
        pop until '[' -> collected [cc, a] -> reversed -> "a" + "cc" = "acc"; pop '['
        pop digits    -> "3" -> k = 3
        push 3 * "acc" = "accaccacc"   stack=[accaccacc]
end -> join the stack -> "accaccacc" ✅
```

### Multi-digit trace: decodeString("10[ab]")
```
'1','0' pushed as separate characters  stack=[1, 0]
'[' 'a' 'b' pushed                      stack=[1, 0, [, a, b]
']' -> inner = "ab"; pop '['; pop digits '0','1' -> reversed "10" -> k = 10
       push "ab"*10                     stack=[abababababababababab]
```

### Two-stack layout trace (alternative): decodeString("3[a2[c]]")
```
cur=[]  counts/prefixes stack = []
'3' -> k=3
'[' -> push (cur=[], k=3);  cur=[], k=0
'a' -> cur=[a]
'2' -> k=2
'[' -> push (cur=[a], k=2); cur=[], k=0
'c' -> cur=[c]
']' -> pop (prev=[a], k=2)  -> prev + ["c"*2] -> cur=[a, cc]
']' -> pop (prev=[],  k=3)  -> prev + ["acc"*3] -> cur=[accaccacc]
answer = "accaccacc" ✅
```

### The "aha" moment to remember 🎯
"A closing bracket closes the innermost open bracket. Push until `]`, then
unwind to `[`, read the full number before it, repeat, and push the result
back as one chunk — nesting then takes care of itself."
"""

# ================================================================================
# ALTERNATIVE APPROACH 1 — Brute Force: Repeatedly Expand Innermost with Regex
# ================================================================================
"""
### Thought Process 🧠
Use the regex `(\\d+)\\[([a-zA-Z]*)\\]` — a number, `[`, only LETTERS (so no
nested brackets inside), `]`. Replace every such match with its expansion.
Repeat until the string stops changing. Each pass resolves at least the
innermost level of every group.

### Complexity
- TC: O(L * d) in the worst case — each of up to `d` passes (d = nesting
  depth) rescans and rebuilds a string up to the decoded length `L`
- SC: O(L) — a new string per pass

### Pros
- Almost a literal restatement of the definition; very short.
- Great oracle for testing the stack solutions.

### Cons
- Re-scans and rebuilds the whole string once per nesting level.
- Regex-based solutions are frowned upon in interviews (hides the real
  algorithmic idea; may be seen as a shortcut).
- Depends on the input being valid and on digits appearing only as counts.

### Bottleneck
Each pass rediscovers where the innermost groups are by scanning. Ask: "can
the traversal itself hand me the innermost group?" -> Yes: the first `]` always
closes the innermost `[` — a stack.
"""


def decode_string_regex(s: str) -> str:
    import re

    pattern = re.compile(r"(\d+)\[([a-zA-Z]*)\]")
    while True:
        new = pattern.sub(lambda m: int(m.group(1)) * m.group(2), s)
        if new == s:
            return s
        s = new


# ================================================================================
# MY APPROACH — Single Stack of Characters/Chunks, Unwind on "]" (optimal output cost)
# ================================================================================
"""
### Idea
Scan the string once and push every character that is not `]`. On `]`, pop
items until the matching `[` to collect the inner text (reversing the popped
order), pop the `[`, pop the digits before it to form `k` (again reversing),
push `k * inner_text` back as ONE string chunk. After the scan, the stack
contains only text chunks in order; join them for the answer.

### Complexity
- TC: O(L * d) worst case, typically ~O(L) — where `L` is the decoded length
  and `d` the nesting depth: each `]` rebuilds the string for its group, so a
  piece of text can be re-joined once per enclosing level. Under the usual
  constraint (L <= 10^5) this is comfortably fast.
- SC: O(L) — the stack plus the final string

### Pros
- Matches the problem statement step by step; very natural once you see "`]`
  closes the innermost `[`".
- Multi-digit numbers are handled (digits are popped while `isdigit()`).
- Decoded chunks pushed as single elements make nested groups trivial.
- Single pass over the input; clean separation of the three unwind steps.

### Cons
- Lots of reversing: inner text and digits both come out backwards and must be
  reversed — easy to forget one of them.
- The final loop `decoded_str += stack.pop(0)` does `pop(0)` on a list, which
  is O(len(stack)) each time (shifts all remaining items), and repeated string
  `+=` copies the growing result. It is correct, but wasteful.
- `while stack[-1] != "["` assumes valid input (no guard for an empty stack).
- Mixes characters and multi-character strings on one stack, so each unwound
  element can be 1 character or a big chunk (still fine because the joins
  handle both).

### DSA Buddy Point 🧠
"Nested encodings: the first closing bracket always closes the innermost open
one. Unwind to `[`, read the number before it, repeat, and push the result
back as one unit — then outer levels never need to know about inner ones."

### What can be improved?
Correctness is fine (verified against the regex oracle below, including
multi-digit counts and nesting). One simple improvement: replace the final
`while stack: decoded_str += stack.pop(0)` with `return "".join(stack)` —
same result, no O(n) `pop(0)` shifts and no repeated string concatenation.
You can also avoid the digit-popping/reversing by parsing numbers as you scan
(two-stack version below).
"""


class Solution:
    def decodeString(self, s: str) -> str:
        stack = []
        decoded_str = ""
        for char in s:
            if char != "]":
                stack.append(char)
            else:
                en_s = []
                while stack[-1] != "[":
                    en_s.append(stack.pop())
                stack.pop()
                num = []
                while stack and stack[-1].isdigit():
                    num.append(stack.pop())
                number = int("".join(reversed(num)))
                en_string = "".join(reversed(en_s))

                repeated = number * en_string
                stack.append(repeated)
        while stack:
            decoded_str += stack.pop(0)
        return decoded_str


# ================================================================================
# ALTERNATIVE APPROACH 2 — Two Stacks / (prefix, count) Stack (cleanest iterative)
# ================================================================================
"""
### Thought Process 🧠
Keep `cur` (list of text pieces for the group currently being built) and `k`
(the number being read). On a digit: `k = k * 10 + digit`. On `[`: push
`(cur, k)` onto a stack, then start fresh with `cur = []`, `k = 0`. On `]`:
pop `(prev, num)`, then `prev.append("".join(cur) * num)` and `cur = prev`. On
a letter: append it to `cur`. The answer is `"".join(cur)`.

### Complexity
- TC: O(L * d) worst case, typically ~O(L) (same copying behaviour as the
  single-stack version, but no per-character unwinding)
- SC: O(L) — pieces plus the stack of saved prefixes (O(d) saved frames)

### Pros
- Numbers are parsed as you scan (`k = k * 10 + digit`) — no digit popping or
  reversing at all.
- Each group is processed exactly once at its `]`; the code is short and has
  a clear mental model: "save the prefix, build the group, merge on close".
- Appending to a list and joining once avoids quadratic string concatenation.

### Cons
- Needs a mental model of "saved state per open bracket", which is slightly
  less literal than "unwind the stack".
- Easy to forget to reset `k = 0` after `[`, or to push the pair BEFORE
  resetting `cur`.

### DSA Buddy Point 🧠
"For nested structures, save the state of the enclosing level when you enter
a bracket and merge the finished child into it when you leave — the same
pattern as evaluating nested parentheses in Basic Calculator."
"""


def decode_string_two_stacks(s: str) -> str:
    stack: list[tuple[list[str], int]] = []
    cur: list[str] = []
    k = 0
    for ch in s:
        if ch.isdigit():
            k = k * 10 + int(ch)
        elif ch == "[":
            stack.append((cur, k))
            cur, k = [], 0
        elif ch == "]":
            prev, num = stack.pop()
            prev.append("".join(cur) * num)
            cur = prev
        else:
            cur.append(ch)
    return "".join(cur)


# ================================================================================
# ALTERNATIVE APPROACH 3 — Recursive Descent (the call stack as the stack)
# ================================================================================
"""
### Thought Process 🧠
Write `parse()` that reads characters from a shared index `i` and builds the
text of the CURRENT level until it meets `]` (or the end). When it sees digits,
it reads `k`; when it sees `[`, it advances past it, calls `parse()` to get the
inner text, skips the matching `]`, and appends `inner * k`. Letters are
appended directly. The top-level call returns the full decoded string.

### Complexity
- TC: O(L * d) worst case, typically ~O(L)
- SC: O(L + d) — result pieces plus recursion depth `d` (nesting depth)

### Pros
- Mirrors the grammar of the encoding directly: `parse` = sequence of
  letters and `k[parse]`; very readable and easy to extend (e.g., to support
  more operators).
- No reversing and no explicit stack of pairs.

### Cons
- Recursion depth equals nesting depth; Python's recursion limit (~1000)
  could be hit by pathologically nested input.
- Needs a shared mutable index (`nonlocal i` or an object) — a slight
  readability tax.

### DSA Buddy Point 🧠
"Anything you can do with an explicit stack for nested structures you can do
with recursion; pick recursion when the grammar is clear and depth is small,
and the explicit stack when depth might be large."
"""


def decode_string_recursive(s: str) -> str:
    i = 0

    def parse() -> str:
        nonlocal i
        parts: list[str] = []
        k = 0
        while i < len(s) and s[i] != "]":
            ch = s[i]
            if ch.isdigit():
                k = k * 10 + int(ch)
                i += 1
            elif ch == "[":
                i += 1  # skip '['
                inner = parse()
                i += 1  # skip ']'
                parts.append(inner * k)
                k = 0
            else:
                parts.append(ch)
                i += 1
        return "".join(parts)

    return parse()


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
DECODE STRING
│
├── Brute Force
│   └── Regex-expand innermost "k[letters]" repeatedly until none remain
│       -> O(L * d) time, O(L) space
│
├── Bottleneck
│   └── Every pass rescans the whole string just to find the innermost
│       groups, which a left-to-right scan gets for free
│
├── Key Insight
│   └── The FIRST ']' always closes the INNERMOST '[' -> STACK
│       Push until ']', then unwind to '[', read k, repeat, push back as one chunk
│
├── My Approach — Single Stack of chars/chunks (unwind on ']')
│   └── pop to '[' (reverse), pop digits (reverse), push k * text
│       -> O(L * d) worst / ~O(L) typical time, O(L) space
│       -> improve: final "".join(stack) instead of pop(0) + string +=
│
├── Two Stacks / (prefix, count) Stack (cleanest iterative)
│   └── k = k*10 + digit; '[' saves (cur, k); ']' merges cur into prefix
│       -> same complexity, no digit popping or reversing
│
└── Recursive Descent
    └── parse() builds a level until ']'; '[' recurses; k read from digits
        -> same complexity, O(d) recursion depth
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Nested brackets => STACK (or recursion). The first ']' always closes the
  innermost '['."
- "On ']': unwind to '[' for the text, then read the number just before it,
  repeat the text, and PUSH THE RESULT BACK as one chunk."
- "Popped items come out REVERSED — reverse the inner text AND the digit
  string before using them."
- "Numbers can be multi-digit: pop digits while `isdigit()`, or accumulate
  `k = k * 10 + digit` as you scan. Never assume a single digit."
- "Final answer: `\"\".join(stack)` — never `stack.pop(0)` in a loop and never
  repeated `+=` on a growing string."
- "Two-stack version: on '[' SAVE (current text, k) and reset; on ']' MERGE
  `k * current` into the saved text. No reversing needed."
- "Cost is driven by the OUTPUT size: each nesting level may re-copy its text,
  so worst case is O(L * d), typically about O(L)."
- "Cousins: LC 20 (Valid Parentheses), LC 224 (Basic Calculator), LC 726
  (Number of Atoms), LC 735 (Asteroid Collision), LC 1021."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                         | Core Idea                                                   | TC                       | SC          | Pros                                                | Cons                                                         | When to Use                                  |
|----------------------------------|-------------------------------------------------------------|--------------------------|-------------|-----------------------------------------------------|--------------------------------------------------------------|----------------------------------------------|
| Regex Brute Force                | Repeatedly expand innermost "k[letters]" via regex          | O(L * d)                 | O(L)        | Shortest, great oracle for testing                  | Rescans every pass, hides the algorithm, frowned on          | Baseline / correctness check                 |
| Single Stack, Unwind on ']'      | Push until ']'; pop to '[', read k, repeat, push back       | O(L * d) worst, ~O(L)    | O(L)        | Literal, handles multi-digit, simple nesting        | Reversals; final pop(0)/+= loop wasteful                     | Default answer (your code)                   |
| Two Stacks / (prefix, k) Stack   | Save (cur, k) on '[', merge on ']', parse k while scanning  | O(L * d) worst, ~O(L)    | O(L)        | No digit popping/reversing, clean and short         | Needs the "save the enclosing state" mental model            | Cleanest iterative version                   |
| Recursive Descent                | parse() until ']'; recurse on '['                           | O(L * d) worst, ~O(L)    | O(L + d)    | Mirrors the grammar; easy to extend                 | Recursion-depth limit; shared index                          | When depth is small / grammar-style solution |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Stack for NESTED structure (unwind on a closing token).
  Cousins: LC 20 (Valid Parentheses), LC 224/227 (Basic Calculator), LC 726
  (Number of Atoms), LC 735 (Asteroid Collision), LC 844 (Backspace String
  Compare), LC 71 (Simplify Path).
- Go-to answer: "Scan left to right. Push every character until a `]`. On
  `]`, pop to the matching `[` to get the inner text, pop the digits before
  it to get k, then push `k * text` back as one piece. At the end, join the
  stack. Alternatively keep a stack of (prefix, k) pairs and parse k while
  scanning. Time is proportional to the output size (O(L * d) worst case),
  space O(L)."
- Good to call out: multi-digit counts, why the result is pushed back as one
  chunk, the reversal of popped pieces, and using `join` instead of repeated
  concatenation.
- Common follow-ups:
  * "What if the input might be invalid?" -> Validate brackets/digits and raise
    on a missing count or unmatched bracket.
  * "What if the decoded string is huge?" -> Generate lazily with a generator
    (yield pieces) or compute only the length / the k-th character without
    materializing the string.
  * "Support letters adjacent to digits like 3a?" -> Change the grammar:
    parse `k` followed by either `[...]` or a single token.
  * "Avoid deep recursion?" -> Use the explicit two-stack version.
"""