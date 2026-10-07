"""
================================================================================
 PROBLEM: Minimum Add to Make Parentheses Valid (LeetCode 921)
================================================================================
A parentheses string is VALID if and only if:
- it is the empty string, or
- it can be written as `AB` (A concatenated with B), where A and B are valid, or
- it can be written as `(A)`, where A is a valid string.

Given a parentheses string `s` (only '(' and ')'), you may INSERT a parenthesis
at ANY position of the string. Return the MINIMUM number of insertions needed to
make `s` valid.

Example: s = "())"      -> 1   (add '(' at the front: "(())" or "()()" ...)
Example: s = "((("      -> 3   (add three ')' at the end)
Example: s = "()))(("   -> 4   (two unmatched ')' and two unmatched '(')

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Do I return the NUMBER of insertions or the repaired string? (The number — a
  single integer. No need to build the fixed string.)
- Can I insert a parenthesis ANYWHERE, and only '(' / ')'? (Yes — insert either
  kind at any position, including the ends. The input contains only '(' and ')',
  no letters or other bracket types.)
- Is the empty string valid? (Yes -> answer 0.)
- Do I count a "replace" as one operation? (No — the only operation is an
  INSERTION; deleting or replacing characters is not allowed. That is what
  makes the answer exactly "unmatched ')' + unmatched '('".)
- What are the size limits? (n up to 1000 here, so even O(n^2) passes — but the
  interview follow-up is O(n) time and O(1) space.)

"""

# ================================================================================
# 🔑🔑🔑  STRONG POINTS FOR "PARENTHESES BALANCE / MINIMUM FIX" PROBLEMS  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   Scan left to right keeping `open` = number of unmatched '('.      │
    │     '('                         -> open += 1                        │
    │     ')' and open > 0            -> open -= 1   (it matches one)     │
    │     ')' and open == 0           -> unmatched ')', needs a '(' BEFORE│
    │                                    it:  need += 1                   │
    │   Answer = need  +  open   (unmatched ')' + leftover unmatched '(') │
    │   A STACK of '(' only ever holds identical items, so a COUNTER is   │
    │   enough: O(1) space.                                               │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

This is the SIMPLEST problem in the "parentheses" family (Valid Parentheses LC
20, Longest Valid Parentheses LC 32, Minimum Remove to Make Valid LC 1249,
Generate Parentheses LC 22) and a showcase of "replace a stack by a counter
when the stack holds only one kind of symbol". Key ideas:

1. **A ')' with no available '(' MUST be fixed by inserting a '(' before it.**
   Nothing later in the string can match it (matching goes left-to-right: the
   '(' must come first). So the moment we see such a ')' we pay 1 insertion
   immediately — a greedy choice that is always optimal.

2. **A '(' left unmatched at the end MUST get a ')' after it** — again forced:
   nothing to its right will ever match it. So each leftover '(' costs 1.

3. **The two kinds of unmatched characters are independent,** so the answer is
   simply (unmatched ')') + (unmatched '('). No need to decide WHERE to insert.

4. **A stack of '(' is just a counter.** Every item on the stack is the same
   character, so pushing/popping carries no information other than the SIZE.
   Replace the stack with an integer `open` -> O(1) space.

5. **Equivalent prefix-balance formula:** let `b` be the running balance
   (`+1` for '(' and `-1` for ')'), starting at 0, and `m = min(b)` over all
   prefixes (including 0, so `m <= 0`). Then
   `answer = (-m) + (final_balance - m) = final_balance - 2 * m`.
   `-m` = unmatched ')' ; `final_balance - m` = unmatched '(' left at the end.

6. **Order matters:** "(" followed by ")" is fine but ")(" costs 2 even though the
   counts are equal. Counting '(' and ')' totals is NOT enough — you must scan
   left to right so a ')' only cancels an '(' that came BEFORE it.
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea
Repeatedly delete every adjacent "()" pair from the string (a matched pair
cancels itself). When no "()" remains, whatever is left looks like `)))...(((`
— a run of unmatched ')' followed by a run of unmatched '('. Each leftover
character needs exactly one inserted partner, so the answer is the length of
what remains. This is correct, but re-scanning and rebuilding the string after
each deletion is quadratic.

### The key insight: match as you go
Walk left to right. Keep `open`, the number of '(' still waiting for a ')'.
- A '(' adds one waiting opener.
- A ')' cancels one waiting opener if there is one; otherwise it is a ')' that
  can NEVER be matched by what comes later, so it forces one insertion.
At the end, any openers still waiting also need one insertion each.

### Step-by-step trace: "()))(("
```
char  action                                  open  need(unmatched ')')
'('   open += 1                                1     0
')'   open > 0 -> open -= 1                    0     0
')'   open == 0 -> unmatched ')': need += 1    0     1
')'   open == 0 -> unmatched ')': need += 1    0     2
'('   open += 1                                1     2
'('   open += 1                                2     2
answer = need + open = 2 + 2 = 4 ✅
```
(Insert '(' twice before the two unmatched ')', and ')' twice at the end.)

### Same trace with a stack (your first solution)
```
'(' -> push                      stack=['(']
')' -> top is '(' -> pop         stack=[]
')' -> stack empty -> count = 1
')' -> stack empty -> count = 2
'(' -> push                      stack=['(']
'(' -> push                      stack=['(', '(']
answer = count + len(stack) = 2 + 2 = 4 ✅
```

### Same trace with the prefix-balance formula
```
prefix balances (start at 0): 0, 1, 0, -1, -2, -1, 0
min m = -2        final balance = 0
answer = final - 2*m = 0 - 2*(-2) = 4 ✅
```

### Why counting totals is not enough: ")("
```
')' -> open == 0 -> unmatched ')': need = 1
'(' -> open = 1
answer = 1 + 1 = 2   (equal counts, but order makes it 2, not 0)
```

### The "aha" moment to remember 🎯
"Unmatched ')' (seen when nothing is open) + leftover unmatched '(' = the
answer. Since every stack item is the same '(', a single counter replaces the
stack."
"""

# ================================================================================
# ALTERNATIVE APPROACH 1 — Brute Force (repeatedly delete "()" pairs)
# ================================================================================
"""
### Thought Process 🧠
While the string contains the substring "()", replace every "()" by the empty
string (matched pairs cancel). When none remain, the leftover has the shape
`)))(((`; its length is the answer, because each leftover character needs
exactly one inserted partner.

### Complexity
- TC: O(n^2) — up to n / 2 rounds in the worst case (e.g. "((((...))))" peels
  one layer per round), each round an O(n) scan/rebuild of the string
- SC: O(n) — a new string per round

### Pros
- A literal reading of "matched pairs cancel"; very easy to trust.
- Excellent oracle for validating the O(n) solutions.

### Cons
- Quadratic in the worst case and allocates a new string every round.
- Says nothing about WHERE to insert; just a count by cancellation.

### Bottleneck
Each round rescans the whole string although a matched pair only affects its
immediate neighbours. Ask: "can I cancel pairs in a single left-to-right pass,
remembering only how many '(' are still open?" -> Yes: a stack / counter.
"""


def min_add_brute(s: str) -> int:
    while "()" in s:
        s = s.replace("()", "")
    return len(s)


# ================================================================================
# MY APPROACH 1 — Stack of Unmatched '(' + Counter of Unmatched ')'
# ================================================================================
"""
### Idea
Scan the string once. Push every '(' onto a stack. For a ')': if the stack is
non-empty (its top is '('), pop it — they match. Otherwise the ')' is
unmatched: increment `count`. At the end every '(' still on the stack is also
unmatched, so the answer is `count + len(stack)`.

### Complexity
- TC: O(n) — one pass; each push/pop is O(1)
- SC: O(n) — the stack can hold up to n '(' characters (e.g. "((((...")

### Pros
- Natural extension of the Valid Parentheses stack solution; instantly
  recognizable to interviewers.
- Correct for the order-sensitive cases (")(" -> 2) because a ')' only matches
  an '(' that is already on the stack.
- Shows clear separation: `count` = unmatched ')', `len(stack)` = unmatched '('.

### Cons
- O(n) extra space for a stack that only ever contains the SAME character —
  it carries no information beyond its size.
- The `stack[-1] == "("` check is redundant: the stack only ever holds '(' so
  `elif stack:` is enough.

### DSA Buddy Point 🧠
"Stack of one symbol type = counter. If every element you push is identical,
only the stack's SIZE matters — keep an integer instead."

### What can be improved?
Correctness is fine (verified against brute force below). Optional: drop the
redundant `stack[-1] == "("` test (`elif stack:`), and replace the stack by an
integer counter to get O(1) space — that is exactly your second solution.
"""


class SolutionStack:
    def minAddToMakeValid(self, s: str) -> int:
        stack = []
        count = 0
        for char in s:
            if char == "(":
                stack.append(char)
            elif stack and stack[-1] == "(":
                stack.pop()
            else:
                count += 1
        return count + len(stack)


# ================================================================================
# MY APPROACH 2 — Two Counters (optimal time AND space)
# ================================================================================
"""
### Idea
Replace the stack by an integer `openBraces` (number of unmatched '(' so far)
and keep `closeBraces` for the unmatched ')' count. For '(' increment the open
counter; for ')' decrement it if positive (matched), otherwise increment the
unmatched-')' counter. Return the sum of both counters.

### Complexity
- TC: O(n) — a single pass with O(1) work per character
- SC: O(1) — two integers

### Pros
- Optimal on both axes; tiny and fast.
- The logic maps one-to-one onto the problem: unmatched ')' needs a '(' before
  it; unmatched '(' needs a ')' after it.
- No data structure, so nothing to initialize or index incorrectly.

### Cons
- Variable names are slightly misleading: these are PARENTHESES, not "braces",
  and `closeBraces` counts only UNMATCHED ')' (not all ')'). Clearer names:
  `open_count` / `unmatched_close`.
- Without the stack picture the greedy argument (why paying immediately for an
  unmatched ')' is optimal) is less visible; be ready to explain it.

### DSA Buddy Point 🧠
"For bracket-balance questions with ONE bracket type, a running balance is
enough: balance < 0 means an unmatched ')' (reset the balance and pay 1);
balance > 0 at the end means unmatched '('."

### What can be improved?
Complexity-wise nothing — O(n) time and O(1) space is optimal (every character
must be read). Only the naming could be improved (see Cons). The next
approach is an equivalent formula using the minimum prefix balance.
"""


class Solution:
    def minAddToMakeValid(self, s: str) -> int:
        openBraces = 0
        closeBraces = 0
        for char in s:
            if char == "(":
                openBraces += 1
            elif openBraces > 0:
                openBraces -= 1
            else:
                closeBraces += 1
        return openBraces + closeBraces


# ================================================================================
# ALTERNATIVE APPROACH 3 — Prefix Balance Minimum Formula
# ================================================================================
"""
### Thought Process 🧠
Define the prefix balance `b_i` = (#'(' - #')') among the first `i` characters,
with `b_0 = 0`. The string is valid iff every `b_i >= 0` and `b_n == 0`. Let
`m = min(b_i)` over all `i` (so `m <= 0`). To keep every prefix non-negative we
must insert `-m` opening parentheses (one for each unit by which the balance
dips below 0). After that the final balance becomes `b_n - m`, which equals
the number of unmatched '(' we must close with that many ')' at the end. Total:
`(-m) + (b_n - m) = b_n - 2 * m`.

### Complexity
- TC: O(n) — one pass tracking the running balance and its minimum
- SC: O(1)

### Pros
- A closed-form view of the greedy: you can read the answer straight from the
  balance curve (depth of the deepest dip + height of the final level above
  that dip).
- Generalizes to related problems (Longest Valid Parentheses LC 32, Remove
  Invalid Parentheses ideas) that reason about prefix balances.

### Cons
- Less obvious to derive under interview pressure than the counter version.
- Easy to forget to include `b_0 = 0` in the minimum (needed for strings that
  never dip below 0, e.g. "((("), which would give a wrong `m`.

### DSA Buddy Point 🧠
"Any bracket-balance question can be read off the prefix-sum curve: the lowest
point = unmatched ')' ; the final value minus the lowest point = unmatched '('."
"""


def min_add_prefix_balance(s: str) -> int:
    balance = 0
    lowest = 0  # include b_0 = 0 in the minimum
    for ch in s:
        balance += 1 if ch == "(" else -1
        lowest = min(lowest, balance)
    return balance - 2 * lowest


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
MINIMUM ADD TO MAKE PARENTHESES VALID
│
├── Brute Force
│   └── Delete "()" pairs until none remain; answer = length of what's left
│       -> O(n^2) time, O(n) space
│
├── Bottleneck
│   └── Each round rescans the whole string although a matched pair only
│       affects its neighbours
│
├── Key Insight
│   └── Unmatched ')' (seen with nothing open) needs a '(' BEFORE it;
│       leftover unmatched '(' needs a ')' AFTER it. Answer = both counts
│
├── My Approach 1 — Stack + counter
│   └── push '(' ; ')' pops if possible else count += 1
│       answer = count + len(stack) -> O(n) time, O(n) space
│       -> stack holds identical '(' => can be a counter
│
├── My Approach 2 — Two counters (OPTIMAL)
│   └── open += 1 on '('; on ')' open -= 1 if open > 0 else close += 1
│       -> O(n) time, O(1) space
│
└── Prefix Balance Formula
    └── b_i = running balance (b_0 = 0), m = min b_i  (m <= 0)
        answer = b_n - 2*m -> O(n) time, O(1) space
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Answer = unmatched ')' + unmatched '('. Compute both in ONE left-to-right
  pass."
- "A ')' with no open '(' can NEVER be matched later (matching is left to
  right) -> pay 1 insertion immediately; the greedy choice is optimal."
- "Leftover '(' at the end each need one ')' appended -> add `open` to the
  count."
- "Order matters: ')(' costs 2 even though the counts are equal — never just
  compare total counts."
- "A stack that holds only identical symbols ('(') is just a counter —
  replace it for O(1) space."
- "Prefix-balance view: answer = final_balance - 2 * min_prefix_balance (with
  the initial 0 included in the minimum)."
- "Valid parentheses (LC 20) needs a stack because there are MULTIPLE bracket
  types; with ONE type, a counter suffices."
- "Cousins: LC 20 (Valid Parentheses), LC 1249 (Minimum Remove to Make Valid),
  LC 1541 (Minimum Insertions to Balance a Parentheses String), LC 32 (Longest
  Valid Parentheses), LC 22 (Generate Parentheses), LC 301 (Remove Invalid
  Parentheses)."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                      | Core Idea                                                   | TC     | SC     | Pros                                              | Cons                                                      | When to Use                              |
|-------------------------------|-------------------------------------------------------------|--------|--------|---------------------------------------------------|-----------------------------------------------------------|------------------------------------------|
| Brute Force (delete "()")     | Cancel pairs repeatedly; remaining length is the answer     | O(n^2) | O(n)   | Literal, great oracle for testing                 | Quadratic, rebuilds the string each round                 | Baseline / correctness check             |
| Stack + counter               | push '(' ; pop on ')' else count += 1; add len(stack)       | O(n)   | O(n)   | Familiar to Valid Parentheses, correct, clear     | Stack of identical items wastes O(n) space                | First idea / explanation (your 1st code) |
| Two counters                  | open / unmatched-close counters instead of a stack          | O(n)   | O(1)   | Optimal time and space, tiny                      | Naming confusion ("braces"), greedy proof less visible    | Default optimal choice (your 2nd code)   |
| Prefix balance formula        | answer = final_balance - 2 * min_prefix_balance             | O(n)   | O(1)   | Closed form, generalizes to other balance problems| Easy to forget b_0 = 0 in the minimum                     | When reasoning about balance curves      |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Greedy balance counting (a stack reduced to a counter).
  Relatives: LC 20 (Valid Parentheses), LC 1249 (Minimum Remove to Make Valid
  Parentheses), LC 1541 (Min Insertions to Balance a Parentheses String), LC 32
  (Longest Valid Parentheses), LC 678 (Valid Parenthesis String), LC 22.
- Go-to answer: "Scan left to right with `open` = number of unmatched '('.
  '(' increments it. A ')' decrements it if it is positive; otherwise it is an
  unmatched ')' that needs a '(' inserted before it, so I increment a `need`
  counter. At the end each remaining unmatched '(' needs a ')' appended. The
  answer is `need + open`. O(n) time, O(1) space."
- Good to call out: why unmatched ')' must be fixed immediately (nothing later
  can match it), why order matters (")(" is 2), and that the stack of '(' is
  just a counter.
- Common follow-ups:
  * "Return the repaired string?" -> Record insertion positions (or build the
    string while scanning): prepend '(' for each unmatched ')' at its index;
    append ')' for the leftover count.
  * "Each '(' needs TWO ')' (LC 1541)?" -> Track need in units of single ')':
    each '(' adds 2 to the requirement, and a lone ')' may need an inserted
    second ')' first.
  * "Minimum REMOVALS instead of insertions (LC 1249)?" -> Same scan, but mark
    unmatched indices for deletion (first pass for ')', second pass for '(').
  * "Multiple bracket types?" -> A real stack is required (counters lose the
    type); the answer is no longer a simple sum.
"""