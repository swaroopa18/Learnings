"""
================================================================================
 PROBLEM: Basic Calculator II (LeetCode 227)
================================================================================
Given a string `s` which represents an expression, evaluate it and return its
value. The expression contains NON-NEGATIVE integers and the operators
`+`, `-`, `*`, `/`, separated by any number of spaces. There are NO
parentheses and NO unary minus. Integer division TRUNCATES TOWARD ZERO.
The expression is always valid and all intermediate results fit in a 32-bit
integer. You may NOT use built-in expression evaluators such as `eval()`.

Example: s = "3+2*2"      -> 7
Example: s = " 3/2 "      -> 1
Example: s = " 3+5 / 2 "  -> 5
Example: s = "14-3/2"     -> 13

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- What is the precedence? (`*` and `/` bind tighter than `+` and `-`; operators
  of the same level are LEFT-associative: "8/2/2" = (8/2)/2 = 2, not 8/(2/2).)
- Can numbers have MORE than one digit, and can there be spaces around them?
  (Yes — "100 + 20" is valid. Accumulate `num = num * 10 + digit` and ignore
  spaces. Spaces are never inside a number.)
- Are there parentheses or a unary minus ("-3", "2*-3")? (No — those appear in
  Basic Calculator I (LC 224). Here every operand is a non-negative literal.)
- How does `/` round for negative results? (Toward ZERO. Negative values can
  appear on a stack once you push `-num`, so division must truncate toward zero:
  Python's `//` FLOORS (-3 // 2 == -2) and would give a wrong answer.)
- Is the expression valid, and what is its size? (Valid; up to 3 * 10^5
  characters — so an O(n^2) solution will TLE and the intended one is O(n).)

"""

# ================================================================================
# 🔑🔑🔑  STRONG POINTS FOR "EXPRESSION WITH PRECEDENCE" PROBLEMS  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   Split the expression into TERMS separated by + and -.             │
    │   Inside a term, * and / are applied immediately; at the end        │
    │   you just ADD all the (signed) terms.                              │
    │                                                                     │
    │   Implementation: remember the PREVIOUS operator. When you finish   │
    │   reading a number, decide what to do with it based on THAT         │
    │   operator:                                                         │
    │      '+'  -> push  +num        '-'  -> push  -num                   │
    │      '*'  -> top = top * num   '/'  -> top = trunc(top / num)       │
    │   Answer = sum(stack). Append a sentinel '+' to flush the last num. │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

This is the "evaluate with a stack" problem where PRECEDENCE enters the picture
(Evaluate RPN, LC 150, had none; Basic Calculator I, LC 224, adds parentheses
and unary minus). The trick is to avoid a full precedence-parser: since only
two precedence levels exist, you can apply `*` and `/` on the spot and defer
`+` and `-` by pushing signed terms. Key ideas:

1. **Act on the PREVIOUS operator when a NEW operator (or the end) arrives.**
   A number is only complete once you see what follows it, and what to do with
   it depends on what came BEFORE it. So keep `prev_op` (initially '+') and
   process the finished number at the next operator.

2. **`+` and `-` just push the signed number; `*` and `/` modify the top.**
   `3+2*2`: push 3, push 2, then the `*` multiplies the TOP (2) by 2 -> 4.
   Stack [3, 4] -> sum 7. Precedence is respected without ever comparing
   precedences.

3. **Sentinel `'+'` at the end flushes the last number.** Without it the final
   number is never pushed. (Loop to `len(s)` inclusive and treat index `len(s)`
   as '+'.)

4. **Division must truncate toward ZERO — and the stack can hold NEGATIVES.**
   After `-`, a negative term sits on the stack, so a following `/` sees a
   negative left operand: `"14-3/2"` -> stack [14, -3] -> `/2` -> trunc(-1.5)
   = -1 (NOT -2). Use `int(a / b)` (or an `abs`-based integer helper); bare
   `a // b` floors and is WRONG here.

5. **Multi-digit numbers and spaces:** `num = num * 10 + int(ch)` for digits;
   `continue` on spaces WITHOUT flushing the number (otherwise "1 + 2" would
   flush at the space and break "12  3"-style handling of internal spacing
   around operators).

6. **O(1)-space refinement:** you never need the whole stack — only the running
   `result` and the current term `last`. On `+`/`-`, fold `last` into `result`;
   on `*`/`/`, update `last`.

7. **Two-pass solutions (tokenize, then do `*`/`/`, then `+`/`-`) are valid but
   usually quadratic** because of list `pop(i)` shifts and repeated
   `"*" in ops` scans.
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea
Tokenize the string into a list of numbers and a list of operators. First scan
for every `*` or `/` and replace "a OP b" by its result (so `3+2*2` becomes
`3+4`). Then evaluate the remaining `+`/`-` from left to right. That is exactly
how you'd do it by hand: multiplication/division first, addition/subtraction
second. It works, but removing items from the middle of Python lists and
re-checking `"*" in ops` after every step makes it slow on long inputs.

### The key insight: terms
Rewrite `3+2*2-6/3` as terms `+3`, `+(2*2)`, `-(6/3)`. Everything is just a sum
of terms. While scanning, keep the CURRENT term on top of a stack: `*` and `/`
update it, `+` and `-` start a new term.

### Step-by-step trace (stack + previous operator): "3+2*2"
```
prev='+', num=0, stack=[]
'3'  -> num = 3
'+'  -> finish num with prev '+': push 3                 stack=[3]     prev='+'  num=0
'2'  -> num = 2
'*'  -> finish num with prev '+': push 2                 stack=[3, 2]  prev='*'  num=0
'2'  -> num = 2
end  -> sentinel '+': finish num with prev '*':
        top = 2 * 2 = 4                                  stack=[3, 4]
sum = 7 ✅
```

### Negative-term trace: "14-3/2"
```
'14' then '-' : push 14                                   stack=[14]      prev='-'
'3'  then '/' : finish with prev '-': push -3             stack=[14, -3]  prev='/'
'2'  then end : finish with prev '/': top = trunc(-3/2)
                = int(-1.5) = -1                           stack=[14, -1]
sum = 13 ✅
(floor division would give -3 // 2 = -2 -> sum 12 ❌ — the classic trap)
```

### O(1)-space trace: "3+2*2"   (result, last, prev)
```
start: result=0, last=0, prev='+'
'3' then '+': prev '+': result += last (0); last = 3   -> result=0, last=3, prev='+'
'2' then '*': prev '+': result += last (3); last = 2   -> result=3, last=2, prev='*'
'2' then end : prev '*': last = 2 * 2 = 4              -> result=3, last=4
answer = result + last = 7 ✅
```

### The "aha" moment to remember 🎯
"Don't parse precedence — apply * and / immediately to the current term, and
turn + / - into signed terms to add up at the end. Process each number when the
NEXT operator arrives, using the PREVIOUS operator."
"""

# ================================================================================
# ALTERNATIVE APPROACH 1 — Brute Force: Tokenize, Collapse * and /, Then + and -
# ================================================================================
"""
### Thought Process 🧠
Scan the string once, building two lists: `nums` (all numbers, with multi-digit
accumulation) and `ops` (all operators). Phase 1: while a `*` or `/` exists in
`ops`, walk left to right; when `ops[i]` is `*` or `/`, replace `nums[i]` by
`nums[i] OP nums[i + 1]` and delete `nums[i + 1]` and `ops[i]`. Phase 2: apply
the remaining `+`/`-` from the front, again replacing and deleting.

### Complexity
- TC: O(n^2) worst case — `"*" in ops` re-scans the operator list on every
  iteration, and `nums.pop(i + 1)` / `ops.pop(i)` shift list elements (O(n)
  each); with up to ~1.5 * 10^5 operators this is far too slow
- SC: O(n) — the two lists

### Pros
- Mirrors "do * and / first, then + and -" exactly; very natural.
- `//` is SAFE here: every operand is a non-negative literal, and Phase 1
  only combines non-negative values, so floor and truncation agree (the
  `int(...)` around `//` is redundant).
- Works for any number of digits; spaces are skipped.

### Cons
- Quadratic time: repeated membership tests and mid-list deletions.
- Fragile: relies on the non-negativity argument above; reusing the same code
  where negative intermediates exist (unary minus, subtraction before division)
  would silently give wrong results.
- Phase 2 reuses a stale `result` variable pattern and index juggling that is
  easy to get wrong.

### Bottleneck
Each collapse is local — you only need the number just before the operator —
yet the algorithm rescans the whole operator list and shifts arrays after each
one. Ask: "can I apply * and / the moment I read them, to the term currently
being built?" -> Yes: the single-stack / `last` variable approaches.
"""


class SolutionTwoPassLists:
    def calculate(self, s: str) -> int:
        nums, ops = [], []

        operations = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: int(x // y),
        }

        digit = 0
        for i in range(len(s)):
            if s[i] == " ":
                continue
            if s[i].isdigit():
                digit = digit * 10 + int(s[i])
            else:
                nums.append(digit)
                digit = 0
                ops.append(s[i])
        nums.append(digit)

        i = 0
        while "*" in ops or "/" in ops:
            if ops[i] == "*" or ops[i] == "/":
                if ops[i] == "*":
                    result = operations["*"](nums[i], nums[i + 1])
                if ops[i] == "/":
                    result = operations["/"](nums[i], nums[i + 1])
                nums[i] = result
                nums.pop(i + 1)
                ops.pop(i)
            else:
                i += 1

        i = 0
        while ops:
            if ops[i] == "+":
                result = operations["+"](nums[i], nums[i + 1])
            if ops[i] == "-":
                result = operations["-"](nums[i], nums[i + 1])
            nums[i] = result
            nums.pop(i + 1)
            ops.pop(i)

        return nums[0]


# ================================================================================
# MY APPROACH — Single Stack + Previous Operator (optimal time)
# ================================================================================
"""
### Idea
Scan the string once (to `len(s)` inclusive, treating index `len(s)` as a
sentinel '+'). Accumulate digits into `digit`; skip spaces. When a non-digit
(operator or sentinel) arrives, FINISH the number using the PREVIOUS operator
`ops`:
- '+' -> push `digit`;  '-' -> push `-digit`
- '*' -> push `top * digit`;  '/' -> push `trunc(top / digit)` (pop the top
  first, then push the result)
Then store the new operator in `ops` and reset `digit`. At the end the stack
holds the signed terms: return `sum(nums)`.

### Complexity
- TC: O(n) — one pass; every push/pop is O(1); `sum` is O(#terms)
- SC: O(n) — the stack of terms (up to ~n / 2 entries, e.g. "1+1+1+...")

### Pros
- Handles precedence without comparing precedences: `*` and `/` modify the
  current term, `+` and `-` start a new signed term.
- Handles multi-digit numbers and arbitrary spaces.
- `int(x / y)` truncates toward zero, so a NEGATIVE term on the stack
  ("14-3/2" -> -3 / 2 = -1) is divided correctly — a bare `//` would floor.
- The sentinel `'+'` at index `len(s)` flushes the last number with no extra
  code after the loop.
- Easy to extend (e.g., add `%`) and a stepping stone to Basic Calculator I.

### Cons
- O(n) extra space for the stack (the `last`-variable version removes it).
- `int(x / y)` goes through floating point; exact for 32-bit values, but an
  integer-only division is safer for arbitrarily large numbers.
- The variable name `ops` holds a SINGLE previous operator, not a list — a
  confusing name (`prev_op` reads better).
- In the digit branch `int(s[i])` is correct here (the digit branch is never
  reached for the sentinel), but `int(char)` is the more consistent choice.

### DSA Buddy Point 🧠
"Two precedence levels? Don't build a parser. Apply `*` and `/` to the top of
the stack immediately, push `+`/`-` terms as signed numbers, and sum at the end.
Process each number when the NEXT operator arrives, using the PREVIOUS one."

### What can be improved?
Correctness is fine (verified against an independent oracle below). Optional
polish: (1) rename `ops` to `prev_op`; (2) use `char` consistently; (3) replace
the stack with two variables (`result`, `last`) to get O(1) space — the next
approach; (4) use exact integer-only truncating division.
"""


class Solution:
    def calculate(self, s: str) -> int:
        nums, ops = [], "+"

        operations = {
            "*": lambda x, y: x * y,
            "/": lambda x, y: int(x / y),
        }

        digit = 0
        for i in range(len(s) + 1):
            char = "+" if i == len(s) else s[i]
            if char == " ":
                continue
            if char.isdigit():
                digit = digit * 10 + int(s[i])
            else:
                if ops == "+":
                    nums.append(digit)
                elif ops == "-":
                    nums.append(-digit)
                elif ops == "*":
                    nums.append(operations["*"](nums.pop(), digit))
                else:
                    nums.append(operations["/"](nums.pop(), digit))
                ops = char
                digit = 0
        return sum(nums)


# ================================================================================
# ALTERNATIVE APPROACH 2 — O(1) Extra Space: Running `result` + Current Term `last`
# ================================================================================
"""
### Thought Process 🧠
Only the CURRENT term (the top of the stack) is ever modified; all earlier
terms are final. So replace the stack with two integers: `result` (sum of all
finished terms) and `last` (the current, still-growing term). When the previous
operator is `+` or `-`, the current term is finished: add `last` to `result`,
and start a new term with `+num` / `-num`. When it is `*` or `/`, update
`last` in place. The answer is `result + last`.

### Complexity
- TC: O(n)
- SC: O(1) extra — a few integers (no stack, no tokens list)

### Pros
- Optimal time AND space.
- Same logic as the stack version, minimal code, and it shows you understand
  WHY only the top of the stack ever matters.
- Uses an exact, float-free truncating division (the `last` value can be
  negative after `-`, so truncation toward zero is required).

### Cons
- Slightly harder to read than the stack version: `result` and `last` must be
  updated in the right order (`result += last` BEFORE overwriting `last`).
- Forgetting the final `result + last` (or the sentinel) drops the last term.

### DSA Buddy Point 🧠
"If a stack is only ever modified at its top and read once at the end, replace
it with a running total plus the current top value."
"""


def _trunc_div(a: int, b: int) -> int:
    """Integer division truncating toward zero, without floats."""
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


def calculate_o1_space(s: str) -> int:
    result, last, num, prev = 0, 0, 0, "+"
    for i in range(len(s) + 1):
        char = "+" if i == len(s) else s[i]
        if char == " ":
            continue
        if char.isdigit():
            num = num * 10 + int(char)
        else:
            if prev == "+":
                result += last
                last = num
            elif prev == "-":
                result += last
                last = -num
            elif prev == "*":
                last = last * num
            else:
                last = _trunc_div(last, num)
            prev, num = char, 0
    return result + last


# ================================================================================
# ALTERNATIVE APPROACH 3 — Two Stacks with Precedence (shunting-yard evaluation)
# ================================================================================
"""
### Thought Process 🧠
The general, precedence-aware way: one stack for numbers, one for operators.
Before pushing a new operator, APPLY every operator on the stack whose
precedence is GREATER THAN OR EQUAL to the new one (>= makes equal-precedence
operators left-associative). Push the new operator. After the scan, apply
everything left. This is the shunting-yard idea evaluated on the fly.

### Complexity
- TC: O(n) — each number and operator is pushed once and popped once
- SC: O(n) — the two stacks

### Pros
- Generalizes to ANY set of binary operators and precedences, and extends to
  parentheses and unary minus (Basic Calculator I, LC 224 / III, LC 772).
- Teaches the standard theory behind expression parsers.

### Cons
- More code than needed for just two precedence levels.
- Two stacks and a precedence table to get right; the `>=` (not `>`) pop
  condition is easy to flip, which breaks left-associativity ("8/2/2").

### DSA Buddy Point 🧠
"Pop operators of higher OR EQUAL precedence before pushing a new one —
equal means left-associative. Learn this once and you can do any infix
calculator problem."
"""


def calculate_two_stacks(s: str) -> int:
    prec = {"+": 1, "-": 1, "*": 2, "/": 2}
    nums: list[int] = []
    ops: list[str] = []

    def apply() -> None:
        b = nums.pop()
        a = nums.pop()
        op = ops.pop()
        if op == "+":
            nums.append(a + b)
        elif op == "-":
            nums.append(a - b)
        elif op == "*":
            nums.append(a * b)
        else:
            nums.append(_trunc_div(a, b))

    i, n = 0, len(s)
    while i < n:
        ch = s[i]
        if ch == " ":
            i += 1
        elif ch.isdigit():
            num = 0
            while i < n and s[i].isdigit():
                num = num * 10 + int(s[i])
                i += 1
            nums.append(num)
        else:
            while ops and prec[ops[-1]] >= prec[ch]:
                apply()
            ops.append(ch)
            i += 1
    while ops:
        apply()
    return nums[0]


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
BASIC CALCULATOR II
│
├── Brute Force (two-pass lists)
│   └── tokenize -> collapse all * and / -> then + and -  -> O(n^2) time
│       ("*" in ops re-scans + list pops shift elements)
│
├── Bottleneck
│   └── Each collapse is local, but the algorithm rescans the operator list
│       and shifts arrays after every one
│
├── Key Insight
│   └── Expression = sum of TERMS split at + and -. Inside a term, * and /
│       apply immediately; + and - push signed terms. Process each number
│       when the NEXT operator arrives, using the PREVIOUS operator
│
├── My Approach — Single Stack + previous operator (OPTIMAL time)
│   └── '+' push n; '-' push -n; '*' top*=n; '/' top=trunc(top/n); sum at end
│       -> O(n) time, O(n) space; sentinel '+' flushes the last number
│       -> int(x / y) because the stack can hold NEGATIVES
│
├── O(1) Space: result + last
│   └── fold `last` into `result` on + / -; update `last` on * / /
│       -> O(n) time, O(1) extra space
│
└── Two Stacks with Precedence (shunting-yard evaluation)
    └── pop ops with precedence >= new op before pushing
        -> O(n) time, O(n) space, generalizes to parentheses (LC 224)
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Expression with + - * / and no parentheses => terms. Apply * and / to the
  current term immediately; turn + and - into signed terms; answer = sum."
- "Use the PREVIOUS operator when a number completes (the next operator — or a
  sentinel '+' at the end — is the trigger)."
- "Division truncates toward ZERO and the stack can hold NEGATIVE terms (after
  '-'), so use `int(a / b)` or an abs-based helper — never bare `//`."
- "Parse multi-digit numbers with `num = num * 10 + digit`; SKIP spaces
  without flushing the number."
- "The final number needs flushing: loop to `len(s)` inclusive with a sentinel
  '+', or add the last term after the loop."
- "Space optimization: only the top of the stack changes, so keep `result` and
  `last` instead of the stack (O(1) space)."
- "Two-pass tokenize-and-collapse solutions are natural but quadratic because
  of `pop(i)` shifts and repeated `in` scans on the operator list."
- "Equal-precedence operators are LEFT-associative: pop on `>=`, not `>`
  (8/2/2 = 2)."
- "Next problems: LC 224 (adds parentheses and unary minus), LC 772 (Basic
  Calculator III: everything), LC 150 (RPN), LC 282 (Expression Add Operators)."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                          | Core Idea                                                      | TC       | SC     | Pros                                                     | Cons                                                          | When to Use                               |
|-----------------------------------|----------------------------------------------------------------|----------|--------|----------------------------------------------------------|---------------------------------------------------------------|-------------------------------------------|
| Two-pass lists (brute force)      | Tokenize, collapse * and /, then evaluate + and -              | O(n^2)   | O(n)   | Mirrors hand evaluation; `//` safe (non-negative values) | Quadratic (`in` scans + pops), fragile with negatives         | Baseline / first idea (your 1st code)     |
| Single stack + previous operator  | Push signed terms; * and / modify the top; sum at the end      | O(n)     | O(n)   | Optimal time, no precedence logic, extensible            | O(n) stack, `int(x / y)` uses floats, `ops` naming            | Default answer (your 2nd code)            |
| O(1)-space `result` + `last`      | Fold `last` into `result` on + / -; update `last` on * / /     | O(n)     | O(1)   | Optimal time and space, minimal code                     | Update order matters; easy to drop the final term             | Follow-up: "can you use O(1) space?"      |
| Two stacks with precedence        | Pop operators of precedence >= new one before pushing          | O(n)     | O(n)   | Generalizes (parentheses, more operators, LC 224/772)    | More code; `>=` vs `>` pitfall                                | When the problem may grow (parentheses)   |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Stack for expression evaluation with operator precedence (terms +
  previous operator). Relatives: LC 224 (Basic Calculator I — parentheses),
  LC 772 (Basic Calculator III — both), LC 150 (Evaluate RPN), LC 394
  (Decode String), LC 282 (Expression Add Operators).
- Go-to answer: "Scan the string, accumulating multi-digit numbers and
  skipping spaces. Keep the previous operator (initially '+'). When I reach a
  new operator — or the end, using a sentinel '+' — I finish the number based
  on the previous operator: '+' pushes it, '-' pushes its negative, '*' and '/'
  combine it with the top of the stack (division truncating toward zero).
  The answer is the sum of the stack. O(n) time; O(n) space, or O(1) by keeping
  just a running result and the last term."
- Good to call out: why `*` and `/` are applied immediately (precedence for
  free), why division can see a negative operand (after '-') and so must
  truncate toward zero rather than floor, and the sentinel for the last number.
- Common follow-ups:
  * "Add parentheses and unary minus?" -> LC 224: push (result, sign) on '(' and
    restore on ')' (or recurse), or use two stacks with precedence.
  * "Add `^` (right-associative) or `%`?" -> Extend the precedence table; pop
    on `>` instead of `>=` for right-associative operators.
  * "Can you do it in O(1) space?" -> Track `result` and `last`.
  * "What if the input might be invalid?" -> Validate token order and division
    by zero; raise a clear error.
"""
