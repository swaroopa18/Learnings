"""
================================================================================
 PROBLEM: Evaluate Reverse Polish Notation (LeetCode 150)
================================================================================
You are given an array of strings `tokens` that represents an arithmetic
expression in REVERSE POLISH NOTATION (postfix). Evaluate the expression and
return the integer result.

- Valid operators are `+`, `-`, `*` and `/`.
- Each operand is an integer (it may be NEGATIVE, e.g. "-11").
- Division between two integers ALWAYS TRUNCATES TOWARD ZERO (-7 / 2 = -3).
- There is no division by zero; the expression is always valid; the answer and
  all intermediate results fit in a 32-bit integer.

Example: ["2","1","+","3","*"]            -> ((2 + 1) * 3)       = 9
Example: ["4","13","5","/","+"]           -> (4 + (13 / 5))      = 6
Example: ["10","6","9","3","+","-11","*","/","*","17","+","5","+"] -> 22

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- How does division round for NEGATIVE results? (Toward ZERO, not toward
  negative infinity. Python's `//` FLOORS: `-7 // 2 == -4`, but the problem
  wants -3. This is the #1 trap in this problem.)
- Can operands be negative, and how do I tell "-11" from the operator "-"?
  (Yes. The operator token is EXACTLY the one-character string "-"; "-11" is a
  number. So test membership in a set of operator STRINGS — do NOT use
  `token.isdigit()` (it is False for "-11") or `token[0]`.)
- In what order do I apply a non-commutative operator? (For `a b -` the answer
  is `a - b`: the FIRST popped value is the RIGHT operand `b`, the SECOND
  popped value is the LEFT operand `a`. Swapping them breaks `-` and `/`.)
- Is the expression guaranteed valid (enough operands, exactly one result at
  the end)? (Yes — so no error handling needed; with invalid input you'd
  validate the stack size.)
- Can the expression be a single number? (Yes — `["18"]` -> 18; make sure the
  final return converts a string token to an int if your stack stores strings.)

"""

# ================================================================================
# 🔑🔑🔑  STRONG POINTS FOR "POSTFIX / EXPRESSION EVALUATION" STACK PROBLEMS  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   POSTFIX means operands come BEFORE their operator, so a STACK     │
    │   evaluates it in one pass:                                         │
    │       number    -> push                                             │
    │       operator  -> pop b (right), pop a (left), push (a OP b)       │
    │   The single value left on the stack is the answer.                 │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

This is the cleanest "evaluate with a stack" problem: no precedence, no
parentheses (those are the hard parts of Basic Calculator, LC 224/227 — RPN is
what an infix expression is CONVERTED to by the shunting-yard algorithm). Key
ideas:

1. **Operands before operators => the two most recent values on the stack are
   exactly the operands of the next operator.** When you read `+`, its two
   operands are the top two items; their result becomes ONE new operand for a
   later operator. That is why a stack (LIFO) fits perfectly.

2. **Pop order: `b = pop()` first, then `a = pop()`; compute `a OP b`.** The
   top of the stack is the RIGHT operand. For `+` and `*` order doesn't matter;
   for `-` and `/` it absolutely does.

3. **Tell operators from numbers with a membership test on the token string**
   (`token in {"+", "-", "*", "/"}`), because a token like "-11" is a number.

4. **Division must TRUNCATE TOWARD ZERO.** `int(a / b)` does that (float
   division, then drop the fraction) and is fine for 32-bit values since
   doubles represent them exactly. A float-free equivalent is
   `q = abs(a) // abs(b); q if (a < 0) == (b < 0) else -q`. Never use bare
   `a // b` — it floors (rounds toward -infinity).

5. **Convert tokens to `int` once** — either when pushing a number or when
   popping; the stack should hold INTS (or be converted consistently), never a
   mix you have to remember to convert later.

6. **One pass, O(n) time, O(n) space (stack depth is at most about n / 2).**
   Each token is pushed once and popped at most once.

7. **A dictionary of operator -> function** (`{"+": lambda x, y: x + y, ...}`
   or `operator.add` etc.) removes a long if/elif chain and makes adding new
   operators trivial.
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea
Scan the token list for the FIRST operator. Its two operands are the two tokens
right before it. Replace those three tokens with the single computed result.
Repeat until one token remains. Correct, but each replacement shifts the list
and each scan restarts from the beginning -> O(n^2).

### The key insight: the stack remembers "the latest unfinished operands"
Process tokens left to right. Numbers can't be combined yet, so remember them
on a stack. The moment an operator appears, the two numbers on top of the stack
are exactly its operands (that's what postfix guarantees). Replace them by the
result and carry on. Nothing is ever rescanned.

### Step-by-step trace: ["4", "13", "5", "/", "+"]
```
"4"  -> number, push                      stack=[4]
"13" -> number, push                      stack=[4, 13]
"5"  -> number, push                      stack=[4, 13, 5]
"/"  -> operator: b=5, a=13 -> int(13/5)=2   stack=[4, 2]
"+"  -> operator: b=2, a=4  -> 4 + 2 = 6     stack=[6]
answer = 6 ✅
```

### Longer trace: ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
```
10, 6, 9, 3  -> push                      stack=[10, 6, 9, 3]
"+"  : b=3, a=9   -> 12                   stack=[10, 6, 12]
"-11": a NUMBER (not the "-" operator)    stack=[10, 6, 12, -11]
"*"  : b=-11, a=12 -> -132                stack=[10, 6, -132]
"/"  : b=-132, a=6 -> int(6 / -132) = 0   stack=[10, 0]        (truncates toward 0)
"*"  : b=0, a=10    -> 0                  stack=[0]
17   -> push                              stack=[0, 17]
"+"  : 0 + 17 = 17                         stack=[17]
5    -> push                              stack=[17, 5]
"+"  : 17 + 5 = 22                         stack=[22]
answer = 22 ✅
```

### Why truncation matters: ["-7", "2", "/"]
```
a = -7, b = 2
int(-7 / 2)  = int(-3.5) = -3   ✅ (toward zero, what the problem wants)
-7 // 2      = -4               ❌ (floor division — wrong answer!)
```

### The "aha" moment to remember 🎯
"Postfix => stack. Numbers push; an operator pops the right operand first,
then the left, and pushes the result. Mind the pop ORDER and TRUNCATING
division."
"""

# ================================================================================
# ALTERNATIVE APPROACH 1 — Brute Force (repeatedly collapse the first operator)
# ================================================================================
"""
### Thought Process 🧠
While more than one token remains, find the FIRST operator at index `i`. Its
operands are `tokens[i - 2]` (left) and `tokens[i - 1]` (right). Replace the
three tokens `tokens[i-2:i+1]` by the string of their result. Repeat.

### Complexity
- TC: O(n^2) — about n / 2 collapses, each needing an O(n) search from the start
  and an O(n) list slice replacement
- SC: O(n) — a working copy of the token list

### Pros
- Literal translation of "evaluate innermost operations first"; easy to trust.
- Perfect oracle for testing the stack solutions.

### Cons
- Quadratic: re-scans the already-processed prefix after every collapse and
  shifts the list on every replacement.
- Slower, and the explanation hides the stack insight.

### Bottleneck
After a collapse, the next operator's operands are always located right where
the last result was written — the algorithm doesn't need to rescan from the
start. Ask: "can I keep only the latest unfinished values?" -> Yes: a stack.
"""


def _trunc_div(a: int, b: int) -> int:
    """Integer division that truncates toward zero (no floats)."""
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


def _apply(op: str, a: int, b: int) -> int:
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    return _trunc_div(a, b)


_OPERATORS = {"+", "-", "*", "/"}


def eval_rpn_brute(tokens: list[str]) -> int:
    arr = list(tokens)
    while len(arr) > 1:
        for i, tok in enumerate(arr):
            if tok in _OPERATORS:
                result = _apply(tok, int(arr[i - 2]), int(arr[i - 1]))
                arr[i - 2 : i + 1] = [str(result)]
                break
    return int(arr[0])


# ================================================================================
# MY APPROACH — Stack + Operator Dictionary of Lambdas (optimal)
# ================================================================================
"""
### Idea
Build a dictionary mapping each operator string to a two-argument function.
Scan tokens: if the token is NOT an operator, push it; otherwise pop `b` then
`a`, convert both with `int(...)`, compute `operations[token](a, b)`, and push
the integer result. After the scan the stack holds the answer; return
`int(stack[-1])` (the `int` handles the single-token case where the stack still
holds a string).

### Complexity
- TC: O(n) — each token is processed once; every push/pop is O(1)
- SC: O(n) — the stack (at most about n / 2 items at once)

### Pros
- Table-driven: no if/elif chain, and new operators are one dictionary entry.
- Correct operand order (`b` popped first, `a` second) and correct truncating
  division via `int(x / y)`.
- Uses `token not in operations` (a membership test) — so negative numbers
  like "-11" are correctly treated as numbers, not as the "-" operator.
- One pass, optimal time, tiny code.

### Cons
- The stack mixes TYPES: numbers are pushed as strings, results as ints, so
  every pop needs `int(...)` and the final `int(stack[-1])` is required for the
  single-token case. Easy to forget.
- `int(x / y)` goes through floating point; exact for the problem's 32-bit
  range (doubles hold integers up to 2^53), but an integer-only truncating
  division is safer in general.
- The annotation `List[str]` needs `from typing import List` outside LeetCode
  (use `list[str]` in Python 3.9+, as in this file).

### DSA Buddy Point 🧠
"Evaluate postfix with a stack; numbers push, operators pop (right operand
first). Division truncates toward zero — `int(a / b)` for small values or
`abs`-based integer division for exactness."

### What can be improved?
Correctness is fine (verified against the brute-force oracle below). Optional
polish: convert to `int` ONCE at push time (`stack.append(int(token))`) so the
stack holds only ints, which removes both the `int(a)`/`int(b)` conversions and
the `int(stack[-1])` at the end (`return stack[0]`). You can also use the
`operator` module (`operator.add`, ...) instead of lambdas, and exact
integer-only truncating division instead of `int(x / y)`.
"""


class Solution:
    def evalRPN(self, tokens: list[str]) -> int:
        operations = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: int(x / y),
        }

        stack = []
        for token in tokens:
            if token not in operations:
                stack.append(token)
            else:
                b = stack.pop()
                a = stack.pop()
                stack.append(operations[token](int(a), int(b)))
        return int(stack[-1])


# ================================================================================
# ALTERNATIVE APPROACH 2 — Int-Only Stack with Exact Truncating Division
# ================================================================================
"""
### Thought Process 🧠
Same algorithm, cleaned up: convert each number to `int` when pushing, so the
stack contains only integers. Handle operators with a small if/elif chain and
use an exact, float-free helper for division that truncates toward zero. Return
`stack[0]` (the lone value left).

### Complexity
- TC: O(n)
- SC: O(n)

### Pros
- Homogeneous int stack — no repeated `int(...)` conversions and no mixed-type
  surprises.
- Exact integer arithmetic: no floating-point at all (safe even for huge
  Python ints, where `int(a / b)` could lose precision).
- Explicit branches make the operand order and the division rule very easy to
  audit.

### Cons
- More lines than the dictionary version.
- A hand-written truncating division helper is one more place to make a sign
  mistake.

### DSA Buddy Point 🧠
"Normalize data types at the boundary (convert tokens to ints once, on the
way in) so the rest of the algorithm never has to think about types."
"""


def eval_rpn_clean(tokens: list[str]) -> int:
    stack: list[int] = []
    for token in tokens:
        if token in _OPERATORS:
            b = stack.pop()
            a = stack.pop()
            stack.append(_apply(token, a, b))
        else:
            stack.append(int(token))
    return stack[0]


# ================================================================================
# ALTERNATIVE APPROACH 3 — In-Place Array-Backed Stack (reuse the token list)
# ================================================================================
"""
### Thought Process 🧠
Use the front of the (copied) token list as the stack with an index `top`. For
a number, write `int(token)` at `top + 1`. For an operator, read the two values
at `top - 1` and `top`, write the result at `top - 1`, and decrement `top`. The
write position never passes the read position, so no unread token is
overwritten. The answer is `arr[0]`.

### Complexity
- TC: O(n)
- SC: O(1) EXTRA beyond the list itself if the input may be mutated (this
  version copies the list first, so O(n) as written)

### Pros
- Showcases the "stack in the array's own prefix" space trick.
- No `append`/`pop` overhead.

### Cons
- Index arithmetic (`top`, `top - 1`) is easier to get off by one than
  `push`/`pop`.
- Mutates the caller's list unless you copy it; marginal real-world gain in
  Python.

### DSA Buddy Point 🧠
"A stack that never grows past the number of tokens already read can live in
the input array itself — `top` is the stack pointer."
"""


def eval_rpn_inplace(tokens: list[str]) -> int:
    arr: list = list(tokens)  # drop the copy if mutation is allowed
    top = -1
    for token in tokens:
        if token in _OPERATORS:
            b = arr[top]
            a = arr[top - 1]
            top -= 1
            arr[top] = _apply(token, a, b)
        else:
            top += 1
            arr[top] = int(token)
    return arr[0]


# ================================================================================
# ALTERNATIVE APPROACH 4 — Recursive Evaluation from the End (expression tree)
# ================================================================================
"""
### Thought Process 🧠
The LAST token of a valid RPN expression is the ROOT of its expression tree. If
it is a number, return it. If it is an operator, the tokens before it contain
the RIGHT subtree first (immediately before the operator, read from the end)
and then the LEFT subtree. So walk the list BACKWARD with a shared index:
`ev()` takes a token; for an operator, `right = ev()`, then `left = ev()`, then
return `left OP right`.

### Complexity
- TC: O(n) — every token is consumed exactly once
- SC: O(depth) — the recursion depth equals the height of the expression tree
  (up to about n / 2 for a chain like `1 1 1 1 + + +`)

### Pros
- Mirrors the grammar of the expression: "operator = (left subtree, right
  subtree, operator)". Easy to extend to build or print the tree.
- No explicit stack and no popping order to memorize (right is evaluated first
  because we walk backward).

### Cons
- Recursion depth can reach thousands for long chains — Python's default limit
  (~1000) can be exceeded (n can be 10^4) unless you raise it.
- Slightly unintuitive: you read the expression BACKWARD and evaluate the right
  operand before the left one.

### DSA Buddy Point 🧠
"An RPN token list is a serialized expression tree (post-order). Reading it
backward gives the root first, then the right subtree, then the left."
"""


def eval_rpn_recursive(tokens: list[str]) -> int:
    i = len(tokens) - 1

    def ev() -> int:
        nonlocal i
        token = tokens[i]
        i -= 1
        if token in _OPERATORS:
            right = ev()
            left = ev()
            return _apply(token, left, right)
        return int(token)

    return ev()


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
EVALUATE REVERSE POLISH NOTATION
│
├── Brute Force
│   └── Collapse the first "a b op" triple repeatedly -> O(n^2) time
│
├── Bottleneck
│   └── Restarts the scan and re-shifts the list after every collapse, though
│       the next operands are always the most recent results
│
├── Key Insight
│   └── Postfix: an operator's operands are the two most recent values =>
│       STACK. number -> push; operator -> pop b (right), pop a (left), push a OP b
│
├── My Approach — Stack + operator dictionary (OPTIMAL)
│   └── tokens as strings on the stack, int() on pop; int(x / y) truncates
│       -> O(n) time, O(n) space
│       -> improve: convert to int on PUSH; return stack[0]
│
├── Int-Only Stack + exact truncating division
│   └── no floats, no mixed types -> O(n) time, O(n) space
│
├── In-Place Array-Backed Stack
│   └── top pointer inside the token list -> O(n) time, O(1) extra if mutable
│
└── Recursive from the end (expression tree)
    └── last token = root; ev(): right first, then left
        -> O(n) time, O(depth) recursion
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Postfix => stack. Push numbers; on an operator, pop the RIGHT operand first
  (`b`), then the LEFT operand (`a`), push `a OP b`."
- "Pop order matters for `-` and `/`: the first popped value is the right
  operand."
- "Division truncates TOWARD ZERO. `int(a / b)` works for 32-bit ranges; bare
  `a // b` FLOORS and gives -4 for -7 / 2 instead of -3."
- "Tell operators from numbers by MEMBERSHIP in {'+', '-', '*', '/'} — a token
  like '-11' is a number (so `isdigit()` and `token[0]` checks are traps)."
- "Convert tokens to ints once (at push) so the stack holds a single type."
- "Single-token input (['18']) must still return an int."
- "One pass, O(n) time; the stack holds at most about n / 2 values."
- "Relatives: LC 224/227 (Basic Calculator — needs precedence and
  parentheses), LC 394 (Decode String), LC 20 (Valid Parentheses), LC 735
  (Asteroid Collision), shunting-yard algorithm (infix -> postfix)."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                         | Core Idea                                                  | TC       | SC           | Pros                                              | Cons                                                      | When to Use                              |
|----------------------------------|------------------------------------------------------------|----------|--------------|---------------------------------------------------|-----------------------------------------------------------|------------------------------------------|
| Brute Force                      | Collapse the first "a b op" triple repeatedly              | O(n^2)   | O(n)         | Literal, great oracle for testing                 | Quadratic: rescans and shifts the list each time          | Baseline / correctness check             |
| Stack + operator dictionary      | push tokens; operator pops b, a, pushes op(a, b)           | O(n)     | O(n)         | Table-driven, short, correct order, optimal       | Mixed string/int stack, float-based int(x / y)            | Default answer (your code)               |
| Int-only stack + exact division  | int(token) on push; if/elif; abs-based truncating division | O(n)     | O(n)         | Single-type stack, no floats, easy to audit       | Longer, hand-written division helper                      | Cleanest production-style version        |
| In-place array-backed stack      | `top` pointer inside the token list                        | O(n)     | O(1)* extra  | Space-trick showcase, no append/pop overhead      | Off-by-one prone, mutates input unless copied             | Follow-up: "reduce extra space?"         |
| Recursive from the end           | Last token = root; evaluate right subtree then left        | O(n)     | O(depth)     | Mirrors the expression-tree structure             | Deep recursion on long chains; backward reading           | "Another way?" / tree-based discussion   |

*O(1) extra only if the input list may be modified; the version above copies it.

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Stack for expression evaluation (postfix). Relatives: LC 224 / 227
  (Basic Calculator I/II), LC 394 (Decode String), LC 20 (Valid Parentheses),
  LC 735 (Asteroid Collision), LC 726 (Number of Atoms).
- Go-to answer: "Iterate over the tokens with a stack. If a token is a number,
  push it as an int. If it is an operator, pop the right operand `b`, then the
  left operand `a`, compute `a OP b`, and push the result. For division,
  truncate toward zero. The one value left on the stack is the answer.
  O(n) time, O(n) space."
- Good to call out: the pop order (b first, then a), truncation toward zero
  versus Python's floor division, and that "-11" is a number not an operator.
- Common follow-ups:
  * "Infix input like '3 + 4 * 2'?" -> Convert to postfix with the shunting-yard
    algorithm (operator stack + precedence), or evaluate directly with two
    stacks (LC 224 / 227).
  * "What if the expression may be invalid?" -> Check the stack has at least two
    values before an operator, and exactly one value at the end.
  * "Could overflow happen?" -> Python ints are unbounded; in Java/C++ use
    `long` for intermediates (the problem guarantees 32-bit-safe values).
  * "Unary minus or more operators (%, ^)?" -> Add dictionary entries (and an
    arity table for unary operators).
"""

