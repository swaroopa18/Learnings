"""
================================================================================
 PROBLEM: Binary Tree Zigzag Level Order Traversal (LeetCode 103)
================================================================================
Given: the root of a binary tree.
Task: return the zigzag level order traversal of its nodes' values, i.e.
level 0 LEFT -> RIGHT, level 1 RIGHT -> LEFT, level 2 LEFT -> RIGHT, ...
(direction alternates at every level).

Example:
        3
       / \
      9   20
         /  \
        15   7
  Zigzag = [[3], [20, 9], [15, 7]]

Follow-up: can you avoid reversing each level?

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Can the tree be empty? (Yes -> return [])
- Does the first level go left -> right? (Yes, level 0 is L->R)
- How wide / deep can the tree get? (Wide -> BFS queue is big; very deep
  skewed tree + Python recursion limit -> avoid recursive DFS)
- Is the output order within a level strictly required, or only the set of
  values per level? (Strict order -> must handle direction explicitly)
"""

from collections import deque
from typing import List, Optional

# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

# ================================================================================
# MY APPROACH #1 — BFS level by level + reverse odd levels (my solution)
# ================================================================================
"""
### Idea
Standard level-order BFS with a queue. Always enqueue LEFT then RIGHT (so each
level is collected left -> right). Keep a boolean `forward`; after collecting
a level's values, if `forward` is False, reverse that list. Flip `forward`
after every level.

### Why does it work?
BFS with left-then-right enqueueing always yields each level in natural
left -> right order. Zigzag only changes the ORDER INSIDE a level, so
reversing the odd levels afterwards gives exactly the required output.
Children are always enqueued left -> right regardless of direction.

### Complexity
- TC: O(n) — each node is enqueued/dequeued once; reversing a level of size k
  costs O(k), and the sum of all level sizes is n
- SC: O(w) — queue holds at most one level (w = max width, up to ~n/2),
  plus O(n) for the output

### Pros
- Very short, easy to explain, hard to get wrong.
- Reuses the standard BFS template (LC 102) with one extra line.

### Cons
- Extra O(k) reversal pass per odd level (still O(n) total).
- `len(queue)` snapshot per level is required — forgetting it mixes levels.

### Bottleneck
Not asymptotic, just constant-factor: every odd level is built then reversed.
Approaches #2 / #3 avoid the reversal.
"""


class SolutionBFSReverse:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if root is None:
            return []

        result = []
        queue = deque([root])
        forward = True

        while queue:
            count = len(queue)
            values = []
            for _ in range(count):
                node = queue.popleft()
                values.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            if not forward:
                values.reverse()
            result.append(values)
            forward = not forward

        return result


# ================================================================================
# MY APPROACH #2 — BFS with deque per level (append / appendleft)
# ================================================================================
"""
### Idea
Same BFS, but build each level in a deque:
  - forward level  -> values.append(node.val)
  - backward level -> values.appendleft(node.val)
No reversal needed; the level is already in the right order when finished.

### Why does it work?
Nodes still come out of the queue left -> right. Pushing each new value to the
FRONT of the deque produces the reverse order incrementally.

### Complexity
- TC: O(n) — appendleft / append are O(1)
- SC: O(w) for the queue + O(n) for the output

### Pros
- No separate reverse step; each value is placed once.

### Cons
- Needs conversion `list(values)` at the end of each level.
- Slightly more code than approach #1 for the same asymptotics.

### What can be improved?
Pre-size a list and write by index (approach #3) to avoid deque conversion.
"""


class SolutionBFSDeque:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if root is None:
            return []

        result = []
        queue = deque([root])
        forward = True

        while queue:
            values = deque()
            for _ in range(len(queue)):
                node = queue.popleft()
                if forward:
                    values.append(node.val)
                else:
                    values.appendleft(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(list(values))
            forward = not forward

        return result


# ================================================================================
# MY APPROACH #3 — BFS with index placement (pre-sized list)
# ================================================================================
"""
### Idea
Since we know the level size `count` up front, allocate `values = [0] * count`
and put the i-th dequeued node at:
  - index i              if the level is left -> right
  - index count - 1 - i   if the level is right -> left

### Complexity
- TC: O(n)
- SC: O(w) queue + O(n) output

### Pros
- No reversal, no deque conversion; writes each value exactly once.

### Cons
- Index arithmetic is an easy place for off-by-one bugs.

### Bottleneck
Nothing asymptotic; purely a style/constant-factor choice.
"""


class SolutionBFSIndex:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if root is None:
            return []

        result = []
        queue = deque([root])
        forward = True

        while queue:
            count = len(queue)
            values = [0] * count
            for i in range(count):
                node = queue.popleft()
                idx = i if forward else count - 1 - i
                values[idx] = node.val
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(values)
            forward = not forward

        return result


# ================================================================================
# MY APPROACH #4 — Two stacks (classic zigzag, no queue)
# ================================================================================
"""
### Idea
Use two stacks: `cur` (the level being read) and `nxt` (the next level).
Popping a stack reverses insertion order, so the push order of children
decides the direction of the NEXT level:
  - current level read L->R: push LEFT then RIGHT  -> next pops R->L
  - current level read R->L: push RIGHT then LEFT  -> next pops L->R
When `cur` is empty, swap `cur` and `nxt`, flip direction.

### Why does it work?
A stack is LIFO, so the order children are pushed is exactly reversed when they
are popped. Alternating the push order alternates the reading direction.

### Complexity
- TC: O(n) — each node pushed and popped once
- SC: O(w) — the two stacks hold at most two adjacent levels; O(n) output

### Pros
- No reverse and no index math; direction is "free" from the LIFO property.
- Good to mention as the textbook answer.

### Cons
- Push order flips each level — easy to get backwards.
- Level boundaries are implicit (swap stacks) instead of `len(queue)`.
"""


class SolutionTwoStacks:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if root is None:
            return []

        result = []
        cur, nxt = [root], []
        left_to_right = True

        while cur:
            values = []
            while cur:
                node = cur.pop()
                values.append(node.val)
                if left_to_right:
                    if node.left:
                        nxt.append(node.left)
                    if node.right:
                        nxt.append(node.right)
                else:
                    if node.right:
                        nxt.append(node.right)
                    if node.left:
                        nxt.append(node.left)

            result.append(values)
            cur, nxt = nxt, []
            left_to_right = not left_to_right

        return result


# ================================================================================
# MY APPROACH #5 — Recursive DFS with depth (deque per level)
# ================================================================================
"""
### Idea
DFS that always visits LEFT before RIGHT and carries `depth`. Keep
`levels[depth]` as a deque; even depth -> append, odd depth -> appendleft.
Convert deques to lists at the end.

### Why does it work?
A left-first DFS reaches the nodes of any single level in left -> right order,
so appending gives L->R and appendleft gives R->L.

### Complexity
- TC: O(n)
- SC: O(h) recursion stack + O(n) output

### Pros
- Compact; shows you can solve level problems without BFS.

### Cons
- Recursion depth = tree height -> stack overflow risk in Python on skewed trees.
- Not a "natural" level traversal; interviewers may still expect BFS.
"""


class SolutionDFS:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        levels = []

        def dfs(node, depth):
            if node is None:
                return
            if depth == len(levels):
                levels.append(deque())
            if depth % 2 == 0:
                levels[depth].append(node.val)
            else:
                levels[depth].appendleft(node.val)
            dfs(node.left, depth + 1)
            dfs(node.right, depth + 1)

        dfs(root, 0)
        return [list(level) for level in levels]


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
BINARY TREE ZIGZAG LEVEL ORDER
│
├── Definition
│   └── Level order, direction alternates: L->R, R->L, L->R, ...
│
├── Core Insight
│   └── Always traverse children left -> right; only the ORDER INSIDE a
│       level changes -> fix it per level (reverse / deque / index / stack)
│
├── BFS + reverse odd levels  (my solution)
│   └── queue, len(queue) snapshot, flip `forward`, reverse when False
│       └── O(n) time, O(w) space
│
├── BFS + deque (append / appendleft)
│   └── builds the level in the right order, no reverse
│
├── BFS + index placement
│   └── values[i] or values[count-1-i] on a pre-sized list
│
├── Two stacks
│   └── LIFO flips order; push order (L,R) vs (R,L) alternates per level
│       └── O(n) time, O(w) space
│
└── DFS with depth
    └── left-first DFS, deque per depth: append (even) / appendleft (odd)
        └── O(n) time, O(h) recursion stack
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Zigzag = level order + alternate the direction. Children are ALWAYS enqueued
  left then right; direction only affects how the level's values are ordered."
- "Take `count = len(queue)` BEFORE the inner loop — that is what separates
  one level from the next."
- "Flip `forward` once per LEVEL, not once per node."
- "Reverse AFTER collecting the level (or use appendleft / index math) — never
  change the enqueue order in the queue-based version, it breaks the next level."
- "Two-stack version: the push order is the opposite of the direction you want
  for the NEXT level."
- "Empty tree -> []. Check this before creating the queue."
- "Code hygiene: `from collections import deque` is required; check
  `root is None` before using `result`."
- "Same family: LC 102 (Level Order), LC 107 (Level Order II), LC 199 (Right
  Side View), LC 637 (Average of Levels), LC 429 (N-ary Level Order)."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                   | Core Idea                                         | TC   | SC (extra) | Pros                               | Cons                                       | When to Use                     |
|----------------------------|---------------------------------------------------|------|------------|------------------------------------|--------------------------------------------|---------------------------------|
| BFS + reverse (mine)       | Level order, reverse values on odd levels         | O(n) | O(w)       | Shortest; easy to explain          | Extra reverse pass per odd level           | Default first answer            |
| BFS + deque                | append / appendleft by direction                  | O(n) | O(w)       | No reverse step                    | Deque -> list conversion                   | "Avoid reversing" follow-up     |
| BFS + index placement      | Write to values[i] or values[count-1-i]           | O(n) | O(w)       | Single write per value             | Index off-by-one risk                      | Clean, no extra structures      |
| Two stacks                 | LIFO flips order; alternate child push order      | O(n) | O(w)       | No reverse; classic textbook       | Push order is easy to flip wrongly         | Stack-based variant asked       |
| DFS + depth                | Left-first DFS, deque per depth                   | O(n) | O(h)       | Compact; no queue                  | Recursion limit on skewed trees            | Shallow trees / DFS preference  |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: BFS level order (tree) with a per-level twist.
- Go-to answer: "Zigzag is just level order where the direction alternates.
  I run a standard BFS with a queue, snapshot the level size, enqueue left then
  right, and reverse the collected values on every other level using a boolean
  flag. That's O(n) time and O(w) space, where w is the maximum width. To avoid
  the reversal I can build each level in a deque using appendleft on backward
  levels, or write into a pre-sized list by index, or use two stacks."
- Good to mention: children are always enqueued left -> right; only the
  within-level order changes. Complexity stays O(n) because the reversals sum
  to the total number of nodes.
- Common follow-ups:
  * "Can you avoid reversing?" -> deque appendleft / index placement / two stacks.
  * "Can you do it with DFS?" -> depth-indexed deques (watch recursion depth).
  * "Right-to-left first instead?" -> start with forward = False.
  * "N-ary tree?" -> same idea, iterate over node.children (LC 429 style).
  * "Space?" -> O(w), which can be O(n) for a complete binary tree.
"""