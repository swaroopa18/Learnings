"""
================================================================================
 PROBLEM: Cousins in Binary Tree (LeetCode 993)
================================================================================
Given: the root of a binary tree with UNIQUE values, and two different values
x and y.
Task: return True if the nodes with values x and y are COUSINS, i.e.
  1. they are at the SAME depth (level), and
  2. they have DIFFERENT parents.

Example:
        1
       / \
      2   3
     /     \
    4       5
  x = 4, y = 5 -> True   (same depth 2, parents 2 and 3)
  x = 2, y = 3 -> False  (same depth 1, but SAME parent 1 -> siblings)
  x = 1, y = 4 -> False  (different depths)

Follow-up: can you stop early instead of traversing the whole tree?

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Are the values unique? (Yes -> a value identifies exactly one node, so I can
  look nodes up by value)
- Are x and y guaranteed to exist in the tree? (Yes -> no "not found" branch
  strictly needed, but handling it is cheap)
- Can x == y? (No -> they are different nodes)
- Can one of them be the root? (Yes -> root has no parent and depth 0, so it
  can never be a cousin)
- Is early exit expected? (Decides between full traversal and early-stop DFS /
  level-by-level BFS)
"""

from collections import deque
from typing import Optional

# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

# ================================================================================
# MY APPROACH #1 — Recursive DFS recording (level, parent) for x and y (mine)
# ================================================================================
"""
### Idea
DFS over the whole tree carrying `level` and `parent`. When the current node's
value equals x (or y), store its level and parent. At the end, x and y are
cousins iff the levels are equal AND the parents are different.

### Why does it work?
Cousins are defined by exactly two facts: depth and parent. DFS can compute
both for every node (depth = recursion level, parent = the caller's node), so
we only need to capture them for the two target values and compare.

### Complexity
- TC: O(n) — every node is visited once (no early exit)
- SC: O(h) — recursion stack (O(log n) balanced, O(n) skewed)

### Pros
- Short and mirrors the definition directly.
- Easy to explain: "find depth and parent of both, then compare".

### Cons
- No early termination: keeps traversing even after both nodes are found.
- Recursion depth = height -> stack-overflow risk in Python on skewed trees.
- Uses instance attributes (self.x_level, ...) as shared state; fine for LC,
  but mutable state is clumsier than returning values or using a dict.
- Comparing parents with `!=` works since nodes are distinct objects, but
  `is not` states the identity intent more clearly.

### Bottleneck
Full traversal + the implicit call stack. If neither x nor y is found, both
levels are None and both parents are None, so the check still returns False
(because the parents are equal), which is the right answer by luck of the
`and` — worth knowing but not relying on.
"""


class SolutionDFS:
    def isCousins(self, root: Optional[TreeNode], x: int, y: int) -> bool:
        self.x_level = None
        self.y_level = None
        self.x_parent = None
        self.y_parent = None

        def dfs(node, level, parent):
            if node is None:
                return
            if node.val == x:
                self.x_level = level
                self.x_parent = parent
            if node.val == y:
                self.y_level = level
                self.y_parent = parent

            dfs(node.left, level + 1, node)
            dfs(node.right, level + 1, node)

        dfs(root, 0, None)
        return self.x_level == self.y_level and (self.x_parent != self.y_parent)


# ================================================================================
# MY APPROACH #2 — BFS level by level with a sibling check (early exit)
# ================================================================================
"""
### Idea
Standard level-order BFS (`count = len(queue)` per level). While processing a
level:
  - note whether x and y appear in THIS level;
  - when expanding a node that has BOTH children, if those two children are
    exactly x and y, they are siblings -> return False immediately.
After finishing a level:
  - both found      -> cousins (same level, and siblings were ruled out) -> True
  - exactly one found -> different levels -> False
  - none found      -> go to the next level.

### Why does it work?
BFS processes one depth at a time, so "both found in the same level" is the
same-depth test. The sibling check catches the only way same-depth nodes can
share a parent (both are children of one node). The loop can stop at the first
level that contains x or y.

### Complexity
- TC: O(n) worst case; stops at the level of the first target found
- SC: O(w) — queue holds at most one level (w = max width)

### Pros
- Natural for "same level" questions; early exit.
- No parent pointers or extra maps needed.

### Cons
- O(w) space, which is O(n) for a wide / complete tree.
- Two separate checks (sibling check + level check) must both be remembered.

### Bottleneck
Forgetting the sibling check (answers True for siblings), or doing it AFTER
enqueueing and mixing up which level you are in.
"""


class SolutionBFSLevel:
    def isCousins(self, root: Optional[TreeNode], x: int, y: int) -> bool:
        if not root:
            return False

        queue = deque([root])

        while queue:
            found_x = found_y = False
            for _ in range(len(queue)):
                node = queue.popleft()

                if node.val == x:
                    found_x = True
                if node.val == y:
                    found_y = True

                # Same parent -> siblings, not cousins
                if node.left and node.right:
                    l, r = node.left.val, node.right.val
                    if (l == x and r == y) or (l == y and r == x):
                        return False

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            if found_x and found_y:
                return True
            if found_x or found_y:
                return False

        return False


# ================================================================================
# MY APPROACH #3 — BFS storing (node, parent) pairs
# ================================================================================
"""
### Idea
Put (node, parent) tuples in the queue. Process level by level; whenever the
dequeued node is x or y, remember its parent. At the end of the level:
  - both parents recorded -> cousins iff the parents are different
  - exactly one recorded  -> different levels -> False

### Complexity
- TC: O(n) worst case, stops at the first level containing x or y
- SC: O(w) for the queue

### Pros
- Parent is tracked explicitly, so there is no special "both children" check.
- Early exit at the target level.

### Cons
- Slightly more memory per queue entry (tuples).
- Must reset the two parent variables at the start of every level.
"""


class SolutionBFSParent:
    def isCousins(self, root: Optional[TreeNode], x: int, y: int) -> bool:
        if not root:
            return False

        queue = deque([(root, None)])

        while queue:
            x_parent = y_parent = None
            found_x = found_y = False

            for _ in range(len(queue)):
                node, parent = queue.popleft()

                if node.val == x:
                    found_x, x_parent = True, parent
                if node.val == y:
                    found_y, y_parent = True, parent

                if node.left:
                    queue.append((node.left, node))
                if node.right:
                    queue.append((node.right, node))

            if found_x and found_y:
                return x_parent is not y_parent
            if found_x or found_y:
                return False

        return False


# ================================================================================
# MY APPROACH #4 — Iterative DFS with early exit (dict of value -> (parent, depth))
# ================================================================================
"""
### Idea
Use a stack of (node, parent, depth). When a popped node's value is x or y,
store `info[val] = (parent, depth)`. As soon as both are recorded, break out of
the loop and compare:
  depth equal AND parent is not the same node.

### Why does it work?
Same two facts as approach #1 (depth + parent), but gathered with an explicit
stack, so there is no recursion limit and the traversal stops once both targets
are known.

### Complexity
- TC: O(n) worst case; early exit once both nodes are found
- SC: O(h) — stack holds a root-to-node path plus pending siblings
  (about 2h entries worst case), plus O(1) for the dict

### Pros
- No recursion-depth risk; early termination; O(h) space.

### Cons
- Needs the "both found" guard; if a value might be missing, check
  `len(info) == 2` before unpacking.

### What can be improved?
Nothing asymptotically; it is the space-friendly, early-exit version of #1.
"""


class SolutionIterativeDFS:
    def isCousins(self, root: Optional[TreeNode], x: int, y: int) -> bool:
        if not root:
            return False

        info = {}
        stack = [(root, None, 0)]

        while stack:
            node, parent, depth = stack.pop()

            if node.val == x or node.val == y:
                info[node.val] = (parent, depth)
                if len(info) == 2:
                    break

            if node.right:
                stack.append((node.right, node, depth + 1))
            if node.left:
                stack.append((node.left, node, depth + 1))

        if len(info) < 2:
            return False

        (px, dx), (py, dy) = info[x], info[y]
        return dx == dy and px is not py


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
COUSINS IN BINARY TREE
│
├── Definition
│   └── same depth AND different parents
│       (same depth + same parent = siblings, NOT cousins)
│
├── Core Insight
│   └── Only two facts matter per target node: its DEPTH and its PARENT.
│       Collect them for x and y, then compare.
│
├── Recursive DFS  (my solution)
│   └── dfs(node, level, parent): store (level, parent) when val is x or y
│       └── O(n) time, O(h) space, no early exit
│
├── BFS level by level
│   ├── found_x / found_y per level -> both: cousins, one: False
│   └── sibling check: node's two children are exactly {x, y} -> False
│       └── O(n) time, O(w) space, early exit
│
├── BFS with (node, parent) tuples
│   └── record parent when x / y is dequeued; compare at end of the level
│
└── Iterative DFS + early exit
    └── stack of (node, parent, depth); dict value -> (parent, depth)
        └── O(n) time, O(h) space, stops once both found
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Cousins = same depth AND different parents. Both conditions are required:
  same depth alone is not enough (siblings), different parent alone is not
  enough (different depths)."
- "Values are unique, so a value identifies one node; compare parents as nodes
  (use `is not`), depths as ints."
- "The root has no parent and depth 0 -> it can never be a cousin of anything."
- "BFS version: the sibling check looks at ONE node's two children while
  expanding it; the same-level check is 'both found in the same level'."
- "BFS version: after a level where only ONE of x / y was found, return False
  immediately — the other one is at a different depth."
- "DFS version stores state outside the recursion (self.* or nonlocal); remember
  to initialize it, and remember it has no early exit."
- "Early exit matters only for performance; worst case is still O(n)."
- "Same family: LC 102 (Level Order), LC 199 (Right Side View), LC 236 (LCA),
  LC 863 (Nodes at Distance K), LC 513 (Bottom Left Value)."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                     | Core Idea                                          | TC   | SC (extra) | Pros                                   | Cons                                          | When to Use                          |
|------------------------------|----------------------------------------------------|------|------------|----------------------------------------|-----------------------------------------------|--------------------------------------|
| Recursive DFS (mine)         | Record (level, parent) of x and y, then compare    | O(n) | O(h)       | Shortest; mirrors the definition       | No early exit; recursion limit on skewed trees | Default first answer                 |
| BFS level + sibling check    | Both found in one level; children are not {x, y}   | O(n) | O(w)       | Early exit; no parent bookkeeping      | Two separate checks to remember               | "Same level" intuition               |
| BFS with (node, parent)      | Queue holds parents; compare at end of level       | O(n) | O(w)       | Explicit parent; early exit            | Tuple overhead; reset per level               | Clean and hard to get wrong          |
| Iterative DFS + early exit   | Stack of (node, parent, depth); dict by value      | O(n) | O(h)       | No recursion limit; O(h) space; early  | Needs the "both found" guard                  | Deep trees, space-conscious answer   |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Tree traversal that tracks (depth, parent) — BFS levels or DFS with
  extra parameters.
- Go-to answer: "Two nodes are cousins if they are at the same depth but have
  different parents. I run a DFS carrying the level and the parent, and when I
  hit x or y I record both. At the end I return level_x == level_y and
  parent_x != parent_y. That's O(n) time and O(h) space. If I want an early exit
  I can use BFS: process one level at a time, return True if both appear in the
  same level, return False if only one appears, and return False early if x and
  y are the two children of the same node."
- Good to mention: why both conditions are needed (siblings share depth AND
  parent; nodes at different depths can have different parents), and that the
  root can never be a cousin.
- Common follow-ups:
  * "Stop early?" -> BFS by level, or iterative DFS that breaks when both found.
  * "Are x and y siblings?" -> same depth AND same parent (just flip the check).
  * "Values not unique?" -> compare by node references instead of values.
  * "Nodes might be missing?" -> guard with found flags / len(info) == 2.
  * "Do it for K nodes?" -> collect (depth, parent) for all K and check groups.
"""