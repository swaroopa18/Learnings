"""
================================================================================
 PROBLEM: Binary Tree Right Side View (LeetCode 199)
================================================================================
Given: the root of a binary tree.
Task: imagine standing on the RIGHT side of the tree; return the values of the
nodes you can see, ordered from top to bottom.
(= the rightmost node of every level, as seen from the right.)

Example:
        1
       / \
      2   3
       \   \
        5   4
  Right side view = [1, 3, 4]

Note: a node in the LEFT subtree is visible if the right side is shorter at
that depth, e.g.
        1
       /
      2
  Right side view = [1, 2]

Follow-up: can you do it with DFS in O(h) extra space?

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Can the tree be empty? (Yes -> return [])
- Is it "rightmost node per level" or "rightmost child chain"? (Per level —
  a left child can be visible if the right side has no node at that depth)
- How deep / wide can the tree get? (Wide -> BFS queue is large; deep skewed
  + Python recursion limit -> prefer iterative)
- Do they want a particular space bound? (O(w) BFS vs O(h) DFS)
"""

from collections import deque
from typing import List, Optional

# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

# ================================================================================
# MY APPROACH #1 — BFS level by level, take the LAST node of each level (mine)
# ================================================================================
"""
### Idea
Standard level-order BFS. At the start of each level the queue holds exactly
that level's nodes, left -> right, so `queue[-1]` is the rightmost node of the
level. Record its value, then process the level (`count = len(queue)`) and
enqueue children left then right.

### Why does it work?
Enqueueing LEFT before RIGHT keeps every level ordered left -> right. The last
node of a level is therefore the one visible from the right side. Taking the
snapshot BEFORE the inner loop is what makes `queue[-1]` the last node of the
CURRENT level (not of the next one).

### Complexity
- TC: O(n) — every node is enqueued and dequeued once
- SC: O(w) — queue holds at most one level (w = max width, up to ~n/2),
  plus O(h) for the output

### Pros
- Simple, iterative, no recursion-depth risk.
- Reuses the BFS template (LC 102); one extra line.

### Cons
- O(w) space, which is O(n) for a complete tree (DFS needs only O(h)).
- Visits every node even though only one per level is needed.

### Bottleneck
Not time, only space: the queue holds an entire level.
(Code hygiene: `from collections import deque` is required, and the
`node is not None` check is redundant since only non-None children are pushed.)
"""


class SolutionBFSLast:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []

        output = []
        queue = deque([root])

        while queue:
            count = len(queue)
            output.append(queue[-1].val)  # rightmost node of this level
            for _ in range(count):
                node = queue.popleft()
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

        return output


# ================================================================================
# MY APPROACH #2 — BFS, record the LAST node while looping (index check)
# ================================================================================
"""
### Idea
Same BFS but without peeking at `queue[-1]`: inside the level loop, when the
loop index `i == count - 1`, that node is the rightmost of the level -> record.

### Complexity
- TC: O(n)
- SC: O(w)

### Pros
- Works the same for any queue/list type (no negative indexing on the deque).

### Cons
- An extra comparison on every iteration; marginally more code than #1.
"""


class SolutionBFSIndex:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []

        output = []
        queue = deque([root])

        while queue:
            count = len(queue)
            for i in range(count):
                node = queue.popleft()
                if i == count - 1:
                    output.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

        return output


# ================================================================================
# MY APPROACH #3 — BFS right-to-left, take the FIRST node of each level
# ================================================================================
"""
### Idea
Enqueue RIGHT before LEFT so each level is ordered right -> left. The first
node dequeued in a level (i == 0) is the rightmost one -> record it.

### Complexity
- TC: O(n)
- SC: O(w)

### Pros
- Natural reading: "first thing I see from the right".

### Cons
- Reversed enqueue order is easy to mix up; no complexity gain.
"""


class SolutionBFSRightFirst:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []

        output = []
        queue = deque([root])

        while queue:
            count = len(queue)
            for i in range(count):
                node = queue.popleft()
                if i == 0:
                    output.append(node.val)
                if node.right:
                    queue.append(node.right)
                if node.left:
                    queue.append(node.left)

        return output


# ================================================================================
# MY APPROACH #4 — Recursive DFS, RIGHT first, record first node per depth
# ================================================================================
"""
### Idea
DFS that visits ROOT -> RIGHT -> LEFT and carries `depth`. The FIRST node ever
reached at a new depth is the rightmost one at that depth (we go right first),
so when `depth == len(output)` append its value.

### Why does it work?
Visiting right before left means that for any depth, the first node reached is
the one furthest right. A left node is recorded only when the right side has no
node at that depth, which is exactly the "visible from the right" rule.
`depth == len(output)` is a cheap "have I seen this depth yet?" test.

### Complexity
- TC: O(n) — each node visited once
- SC: O(h) — recursion stack (O(log n) balanced, O(n) skewed), plus the output

### Pros
- O(h) extra space — better than BFS on wide trees.
- Very short.

### Cons
- Recursion depth = height -> stack-overflow risk in Python on deep trees.
- Visits every node even though only one per level matters.

### Bottleneck
The implicit call stack on a skewed tree.
"""


class SolutionDFSRightFirst:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        output = []

        def dfs(node, depth):
            if node is None:
                return
            if depth == len(output):
                output.append(node.val)
            dfs(node.right, depth + 1)
            dfs(node.left, depth + 1)

        dfs(root, 0)
        return output


# ================================================================================
# MY APPROACH #5 — Iterative DFS with a stack of (node, depth)
# ================================================================================
"""
### Idea
Same as #4 but with an explicit stack of (node, depth) pairs. Pop a node; if
its depth is new, record it. Push LEFT first, then RIGHT, so RIGHT is popped
first (Root -> Right -> Left).

### Complexity
- TC: O(n)
- SC: O(h) — stack holds a root-to-node path plus pending siblings
  (worst case about 2h entries), plus the output

### Pros
- No recursion-limit risk; keeps the O(h) space advantage of DFS.

### Cons
- Push order is easy to get backwards: pushing right first gives the LEFT view.
"""


class SolutionDFSIterative:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []

        output = []
        stack = [(root, 0)]

        while stack:
            node, depth = stack.pop()
            if depth == len(output):
                output.append(node.val)
            if node.left:
                stack.append((node.left, depth + 1))
            if node.right:
                stack.append((node.right, depth + 1))  # popped first

        return output


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
BINARY TREE RIGHT SIDE VIEW
│
├── Definition
│   └── Rightmost node of every level, top to bottom
│
├── Core Insight
│   └── One value per DEPTH -> either "last node of the level" (BFS)
│       or "first node reached at a new depth, going right first" (DFS)
│
├── BFS, last of level  (my solution)
│   ├── left-then-right enqueue, take queue[-1] before the inner loop
│   └── O(n) time, O(w) space
│
├── BFS, right-first
│   └── right-then-left enqueue, take the first node of each level
│
├── DFS recursive, right-first
│   └── if depth == len(output): append; go right, then left
│       └── O(n) time, O(h) space
│
└── DFS iterative
    └── stack of (node, depth); push left then right
        └── O(n) time, O(h) space, no recursion limit
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Right side view = one node per level: the rightmost one. A LEFT child can be
  visible when the right side is shorter at that depth."
- "BFS: take the level snapshot (`count = len(queue)`) and read `queue[-1]`
  BEFORE the inner loop, otherwise you read the next level's last node."
- "DFS: go RIGHT first and record only when `depth == len(output)`. The first
  node reached at a new depth is the rightmost one."
- "Iterative DFS: push LEFT then RIGHT so RIGHT is popped first. Pushing right
  first gives the LEFT side view."
- "Left side view (mirror): take queue[0] in BFS, or go left first in DFS."
- "Only non-None children are pushed, so `if node is not None` inside the BFS
  loop is redundant."
- "Empty tree -> []. Check before creating the queue."
- "BFS = O(w) space, DFS = O(h) space. Wide tree -> DFS wins; deep skewed tree
  -> BFS / iterative DFS (no recursion limit)."
- "Same family: LC 102 (Level Order), LC 103 (Zigzag), LC 513 (Bottom Left
  Value), LC 637 (Average of Levels), LC 515 (Largest Value per Row)."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                   | Core Idea                                          | TC   | SC (extra) | Pros                                | Cons                                    | When to Use                       |
|----------------------------|----------------------------------------------------|------|------------|-------------------------------------|-----------------------------------------|-----------------------------------|
| BFS, last of level (mine)  | Level order, record queue[-1] per level            | O(n) | O(w)       | Simple; no recursion risk           | O(w) space on wide trees                | Default first answer              |
| BFS, index == count-1      | Record node when i is the last in the level        | O(n) | O(w)       | No negative indexing                | Extra comparison per node               | Same as #1, different style       |
| BFS, right-first           | Enqueue right then left; record the first node     | O(n) | O(w)       | "First visible node" intuition      | Reversed enqueue order is error-prone   | Symmetry with left side view      |
| DFS recursive, right-first | Record when depth == len(output); go right first   | O(n) | O(h)       | Least space on wide trees; short    | Recursion limit on skewed trees         | "Do it with O(h) space"           |
| DFS iterative              | Stack of (node, depth); push left then right       | O(n) | O(h)       | O(h) space, no recursion limit      | Push order easy to flip                 | Deep trees + O(h) space           |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Tree traversal with per-level state (BFS level order / depth-tracking DFS).
- Go-to answer: "The right side view is the rightmost node of every level. I do
  a level-order BFS with a queue: at the start of each level I read the last
  element of the queue, since children are enqueued left then right, then I
  process the level and enqueue the next one. That's O(n) time and O(w) space.
  Alternatively, a right-first DFS carrying the depth records the first node
  seen at each new depth, giving O(n) time and only O(h) space."
- Good to mention: a left child can appear in the view when the right subtree
  is shorter; the first-node-per-depth idea handles it automatically.
- Common follow-ups:
  * "Left side view?" -> take queue[0], or DFS going left first.
  * "Do it with less space?" -> DFS, O(h) instead of O(w).
  * "Avoid recursion?" -> iterative DFS with (node, depth) stack.
  * "Return values for both sides?" -> record first and last node of each level.
  * "N-ary tree?" -> same idea, iterate over node.children (LC 429 style).
"""