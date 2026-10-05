"""
================================================================================
 PROBLEM: Asteroid Collision (LeetCode 735)
================================================================================
We are given an array `asteroids` of integers representing asteroids in a
row. For each asteroid, the ABSOLUTE VALUE is its size and the SIGN is its
direction (positive = moving right, negative = moving left). Every asteroid
moves at the same speed.

Find out the state of the asteroids after all collisions:
- When two asteroids meet, the SMALLER one explodes.
- If both are the SAME size, BOTH explode.
- Two asteroids moving in the same direction never meet.

Return the surviving asteroids in their original left-to-right order.

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Which pairs can actually collide? (Only a RIGHT-moving asteroid (+) that is
  immediately to the LEFT of a LEFT-moving one (-). A (-) followed by a (+)
  moves APART and never meets; two with the same sign move in parallel.
  This is the whole reason a stack works.)
- If sizes are equal, do both disappear? (Yes — both explode, and neither
  continues to collide with anything else.)
- Can a single asteroid trigger a CHAIN of collisions? (Yes — a big (-)
  asteroid can destroy several (+) ones in a row before it dies or gets
  through; the algorithm must keep checking after each destruction.)
- Can an asteroid have size 0? (No — values are non-zero, so the sign always
  gives a clear direction.)
- Does the processing order of collisions matter for the final answer?
  (No — the final surviving set is the same regardless of which colliding
  pair is resolved first, so a left-to-right stack simulation is valid.)

"""

# ================================================================================
# 🔑🔑🔑  STRONG POINTS FOR "COLLISION / CANCELLATION" STACK PROBLEMS  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   A collision happens ONLY when  stack top > 0  AND  incoming < 0.  │
    │   (a right-mover on top, a left-mover arriving.)                    │
    │   Then compare sizes:  top smaller  -> pop top, KEEP fighting.      │
    │                        equal        -> pop top, incoming dies too.  │
    │                        top bigger   -> incoming dies, top survives. │
    │   Otherwise just push — no collision is possible.                   │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

This is a "simulate with a stack" problem — the stack holds the survivors so
far, and ONLY its top can ever interact with the next arrival (everything
deeper is shielded by the top). It's the same family as "Remove Adjacent
Duplicates", "Valid Parentheses" (cancellation by adjacency) and the
monotonic-stack problems, but the pop rule is a physical collision rule
instead of a value comparison. Key ideas:

1. **Only the stack TOP can collide with the incoming asteroid.** Survivors
   deeper in the stack are separated from the newcomer by the top; if the
   top is right-moving and wins, nothing deeper is ever reached.

2. **The collision condition is exactly `asteroid < 0 and stack and
   stack[-1] > 0`.** If the stack is empty, or the top is also moving left,
   or the incoming asteroid moves right, there is NO collision — just push.

3. **Three outcomes per fight, and only one keeps the loop going:**
   - top smaller  -> pop it and CONTINUE (incoming survives this fight and
     may hit the next right-mover below)
   - equal        -> pop it and STOP (both gone, do NOT push incoming)
   - top bigger   -> STOP (incoming gone, do NOT push it)

4. **`while`, not `if`:** one big left-mover can chew through many right-
   movers, so the comparison must repeat until the incoming asteroid dies
   or no right-moving top remains.

5. **A `destroyed` flag (or `while ... else`) decides whether to push** the
   incoming asteroid after the loop. Forgetting that equal sizes destroy
   BOTH, or pushing a destroyed asteroid, are the classic bugs.

6. **Left-movers at the very beginning always survive, right-movers at the
   very end always survive** — there is nothing on the other side to hit
   them. The final answer looks like `[negatives...][positives...]`.
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea
Scan the row, find any adjacent pair `(+, -)`, resolve it (remove the smaller,
or both if equal), and start over. Repeat until no `(+, -)` neighbours exist.
It works, but restarting the scan after every collision is slow.

### The key insight: only the latest survivor matters
Process asteroids left to right and keep the survivors on a stack. A new
asteroid can only collide with whoever is currently on TOP of the stack.
If it wins, it continues to the next top; if it loses or ties, it is gone. If
it never meets a right-mover, it joins the stack. One pass, each asteroid
pushed once and popped at most once.

### Step-by-step trace: asteroidCollision([4, 7, 1, 1, 2, -3, -7, 17, 15, -18, -19])
```
 4  : no collision possible                       -> push       stack=[4]
 7  : positive                                    -> push       stack=[4,7]
 1  : positive                                    -> push       stack=[4,7,1]
 1  : positive                                    -> push       stack=[4,7,1,1]
 2  : positive                                    -> push       stack=[4,7,1,1,2]
-3  : top 2 > 0 -> 2 < 3 -> pop 2 (-3 continues)
      top 1 > 0 -> 1 < 3 -> pop 1
      top 1 > 0 -> 1 < 3 -> pop 1
      top 7 > 0 -> 7 > 3 -> -3 destroyed          -> no push    stack=[4,7]
-7  : top 7 > 0 -> 7 == 7 -> pop 7, BOTH destroyed -> no push   stack=[4]
17  : positive                                    -> push       stack=[4,17]
15  : positive                                    -> push       stack=[4,17,15]
-18 : top 15 -> 15 < 18 -> pop
      top 17 -> 17 < 18 -> pop
      top 4  ->  4 < 18 -> pop
      stack empty -> loop ends, -18 survives      -> push       stack=[-18]
-19 : top -18 is NOT > 0 -> no collision          -> push       stack=[-18,-19]
answer = [-18, -19] ✅
```

### The "aha" moment to remember 🎯
"Collisions only between a (+) already on the stack and an incoming (-).
Loop while that's true: smaller top -> pop and keep going; equal -> pop and
stop (both die); bigger top -> stop (incoming dies). If the incoming one is
still alive afterwards, push it."
"""

# ================================================================================
# ALTERNATIVE APPROACH 1 — Brute Force (rescan and resolve adjacent pairs)
# ================================================================================
"""
### Thought Process 🧠
Repeatedly find the leftmost adjacent pair `arr[i] > 0 and arr[i+1] < 0`,
resolve it (delete the smaller one, or both if equal), and rescan from the
start. Stop when no such pair remains.

### Complexity
- TC: O(n^2) — up to n collisions, each requiring an O(n) rescan plus an
  O(n) list deletion
- SC: O(n) — a working copy of the array

### Pros
- Literally the problem statement turned into code; easy to trust.
- Excellent oracle for testing the stack solution.

### Cons
- Quadratic; the rescan-from-scratch after every collision redoes work.
- Deleting from the middle of a Python list is O(n) each time.

### Bottleneck
After resolving a collision, only the NEIGHBOURHOOD of that collision can
create a new `(+, -)` pair, yet we rescan the whole array. Ask: "can I keep
just the relevant frontier?" -> Yes: the stack's top is exactly that frontier.
"""


def asteroid_collision_brute(asteroids: list[int]) -> list[int]:
    arr = list(asteroids)
    while True:
        for i in range(len(arr) - 1):
            if arr[i] > 0 and arr[i + 1] < 0:
                if arr[i] > -arr[i + 1]:
                    del arr[i + 1]
                elif arr[i] < -arr[i + 1]:
                    del arr[i]
                else:
                    del arr[i:i + 2]
                break
        else:
            return arr


# ================================================================================
# MY APPROACH — Stack of Survivors + `destroyed` Flag (optimal)
# ================================================================================
"""
### Idea
Keep a stack of surviving asteroids. For each incoming asteroid, while it is
moving left AND the stack top is moving right, they collide: pop a smaller
top and continue, or (on equal size) pop the top and mark the incoming one
destroyed, or (top bigger) mark incoming destroyed. After the loop, push the
incoming asteroid only if it was not destroyed.

### Complexity
- TC: O(n) — each asteroid is pushed once and popped at most once; the
  `while` is amortized across the whole array
- SC: O(n) — the stack (which is also the returned answer)

### Pros
- Single pass, optimal time, and the stack IS the output (no post-processing).
- Handles chains (one big asteroid destroying many) naturally via `while`.
- The three comparison branches map one-to-one onto the problem statement,
  so it is easy to explain and verify.
- No special handling for all-same-direction input: no collision condition is
  ever true, everything is pushed.

### Cons
- The `destroyed` flag is a bit of bookkeeping; forgetting to set it in the
  equal or top-bigger branch (or forgetting the `break`) causes wrong output.
- The nested `while` inside `for` looks quadratic to a casual reader; you
  must justify the amortized O(n) claim.

### DSA Buddy Point 🧠
"When elements interact only with their immediate neighbour on one side and
the result of an interaction can expose a NEW neighbour, think STACK:
survivors on the stack, newcomer fights the top repeatedly."

### What can be improved?
Complexity-wise nothing — O(n) time is optimal (every asteroid must be
examined). Your code is correct as written: the loop condition is exactly
`asteroid < 0 and stack and stack[-1] > 0`, the smaller-top case pops and
continues, the equal case pops and breaks with `destroyed = True`, and the
bigger-top case breaks with `destroyed = True`. Optional style variants (next
approaches) remove the flag with `while ... else`, or reuse the input array
as the stack to avoid allocating a second list.
"""


class Solution:
    def asteroidCollision(self, asteroids: list[int]) -> list[int]:
        stack = []

        for asteroid in asteroids:
            destroyed = False
            while asteroid < 0 and stack and stack[-1] > 0:
                if stack[-1] < -asteroid:
                    stack.pop()
                elif stack[-1] == -asteroid:
                    stack.pop()
                    destroyed = True
                    break
                else:
                    destroyed = True
                    break
            if not destroyed:
                stack.append(asteroid)

        return stack


# ================================================================================
# ALTERNATIVE APPROACH 2 — Stack with `while ... else` (no flag)
# ================================================================================
"""
### Thought Process 🧠
Same algorithm, but use Python's `while ... else`: the `else` block runs only
if the loop ended WITHOUT a `break`. A `break` means the incoming asteroid
was destroyed (equal or top bigger), so the push in the `else` is skipped
automatically. If the loop ends because the condition became false (stack
empty / top not moving right / incoming moving right), the asteroid survives
and is pushed.

### Complexity
- TC: O(n)
- SC: O(n)

### Pros
- Removes the `destroyed` flag; slightly shorter and arguably more elegant.
- Same single-pass amortized O(n) behaviour.

### Cons
- `while ... else` is unfamiliar to many readers (and many interviewers) and
  is easy to misread as "else of the last comparison"; may need a comment.
- The `continue` after popping a smaller top is easy to forget — without it
  the code would fall through to the `break`.

### DSA Buddy Point 🧠
"`for/while ... else` means 'no break happened'. Great for 'search failed /
nothing blocked me' logic — but only use it if your reader knows the idiom."
"""


def asteroid_collision_while_else(asteroids: list[int]) -> list[int]:
    stack = []
    for a in asteroids:
        while stack and a < 0 < stack[-1]:
            if stack[-1] < -a:
                stack.pop()
                continue  # incoming survived this fight, keep going
            if stack[-1] == -a:
                stack.pop()  # both explode
            break  # incoming destroyed (equal or top bigger)
        else:
            stack.append(a)  # no break -> incoming survived
    return stack


# ================================================================================
# ALTERNATIVE APPROACH 3 — In-Place Stack (reuse a copy of the array + top ptr)
# ================================================================================
"""
### Thought Process 🧠
Treat the front of the array as the stack: keep an integer `top` (index of the
current stack top, -1 if empty) and write survivors to `arr[top + 1]`. Since
the write position `top + 1` is never ahead of the read position, writing
never overwrites an asteroid that hasn't been read yet. At the end the answer
is `arr[:top + 1]`.

### Complexity
- TC: O(n)
- SC: O(1) EXTRA beyond the output if you may modify the input (this version
  copies the input first for safety, so O(n) as written; the final slice is
  the returned answer)

### Pros
- Demonstrates the classic "stack in the array's own prefix" space trick;
  useful when asked to minimize extra memory.
- Same logic, no list append/pop overhead.

### Cons
- Pointer arithmetic (`top + 1`, `top -= 1`) is easier to get off-by-one than
  `append`/`pop`.
- Mutating the caller's input is usually undesirable unless permitted.
- Little real-world gain in Python — the stack version is already O(n).

### DSA Buddy Point 🧠
"A stack whose size never exceeds the number of items read so far can live
INSIDE the input array: `top` is the stack pointer, the prefix is the stack."
"""


def asteroid_collision_inplace(asteroids: list[int]) -> list[int]:
    arr = list(asteroids)  # work on a copy; drop this line if mutation is OK
    top = -1
    for a in asteroids:
        alive = True
        while alive and a < 0 and top >= 0 and arr[top] > 0:
            if arr[top] < -a:
                top -= 1  # pop smaller top, keep fighting
            elif arr[top] == -a:
                top -= 1  # both explode
                alive = False
            else:
                alive = False  # incoming destroyed
        if alive:
            top += 1
            arr[top] = a
    return arr[: top + 1]


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
ASTEROID COLLISION
│
├── Brute Force
│   └── Rescan for adjacent (+, -) pair, resolve, restart -> O(n^2)
│
├── Bottleneck
│   └── Each collision only affects the local neighbourhood, but brute force
│       rescans the whole array every time
│
├── Key Insight
│   └── Only a (+) on the stack top and an incoming (-) can collide. Survivors
│       live on a stack; the newcomer keeps fighting the top until it dies
│       or no (+) top remains
│
├── My Approach — Stack + destroyed flag (BEST / standard)
│   └── while asteroid < 0 and stack and stack[-1] > 0:
│         top < |a| -> pop, continue
│         top == |a| -> pop, destroyed, break
│         top > |a| -> destroyed, break
│       push if not destroyed -> O(n) time, O(n) space
│
├── Stack with while ... else
│   └── break == incoming died; else-branch pushes survivors -> same O(n),
│       no flag, needs idiom familiarity
│
└── In-Place Stack (top pointer in the array)
    └── write survivors to arr[top + 1] -> O(n) time, O(1) extra if mutation
        allowed
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Collision condition is exactly: incoming < 0 AND stack top > 0. Every
  other combination (+,+), (-,-), (-,+), or empty stack means NO collision —
  just push."
- "Three outcomes: top smaller -> pop and CONTINUE; equal -> pop and STOP,
  both die; top bigger -> STOP, incoming dies. Only the first keeps the loop
  going."
- "`while`, not `if` — one large left-mover can destroy a whole run of
  right-movers."
- "Only push the incoming asteroid if it survived the loop (`destroyed`
  flag, or `while ... else`)."
- "O(n) total despite the nested loop: each asteroid is pushed once and
  popped at most once."
- "Sanity shape of the answer: some left-movers first, then some right-
  movers — a (+) followed later by a (-) can never both survive."
- "Equal-size collision removes BOTH — easy to remember to pop the top, easy
  to forget not to push the incoming one."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                     | Core Idea                                                | TC     | SC        | Pros                                           | Cons                                                   | When to Use                          |
|------------------------------|----------------------------------------------------------|--------|-----------|------------------------------------------------|--------------------------------------------------------|--------------------------------------|
| Brute Force                  | Repeatedly resolve an adjacent (+,-) pair, rescan        | O(n^2) | O(n)      | Literal translation, great oracle for testing  | Quadratic, rescans and deletes from middle each time   | Baseline / correctness check         |
| Stack + destroyed flag       | Survivors on a stack; newcomer fights the top in a loop  | O(n)   | O(n)      | Optimal, mirrors the statement, easy to explain| Flag/`break` bookkeeping, amortized argument needed    | Default optimal choice (your code)   |
| Stack with while ... else    | Same, but `else` pushes only when no `break` occurred    | O(n)   | O(n)      | No flag, compact                               | Unfamiliar idiom, `continue` easy to forget            | When comfortable with while/else     |
| In-Place Stack (top pointer) | Use array prefix as the stack with an index pointer      | O(n)   | O(1)*     | Space-trick showcase, no append/pop overhead   | Off-by-one prone, mutates input unless copied          | Follow-up: "reduce extra space?"     |

*O(1) extra only if mutating the input is allowed; the version above copies.

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Stack Simulation (adjacent cancellation / collision). Cousins:
  LC 20 (Valid Parentheses), LC 1047 (Remove All Adjacent Duplicates),
  LC 394 (Decode String), LC 739/503/901 (monotonic stack family).
- Go-to answer: "Iterate left to right keeping a stack of survivors. A
  collision only happens when the incoming asteroid moves left and the stack
  top moves right. While that holds: if the top is smaller, pop it and keep
  fighting; if equal, pop it and discard the incoming one; if the top is
  bigger, discard the incoming one. Push the incoming asteroid if it
  survives. O(n) time, O(n) space."
- Good to call out: why only the stack top can collide, why equal sizes
  destroy BOTH, why it's `while` not `if`, and why it's amortized O(n).
- Common follow-ups:
  * "What if asteroids have different speeds?" -> Collision timing now
    matters; you'd need an event-driven simulation (priority queue of
    collision times) — the simple stack no longer suffices.
  * "What if the winner is the BIGGER absolute value but ties go to the
    right-mover (or left-mover)?" -> Only the equal branch changes (don't
    pop both; pop just the loser).
  * "Return the number of survivors only?" -> Same stack, return `len`.
  * "Reduce extra space?" -> In-place stack using a `top` pointer.
"""
