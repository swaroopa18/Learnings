"""
================================================================================
 PROBLEM: Path Sum II (LeetCode 113)
================================================================================
Given: the root of a binary tree and an integer targetSum.
Task: return ALL root-to-LEAF paths where the sum of the node values equals
targetSum. Each path is a list of node VALUES (not nodes). A leaf is a node
with no children.

Example:
          5
         / \
        4   8
       /   / \
      11  13  4
     /  \    / \
    7    2  5   1
  targetSum = 22 -> [[5, 4, 11, 2], [5, 8, 4, 5]]

Note: values can be negative or zero, so a partial sum can exceed the target
and still come back to it later -> you must NOT prune when sum > target.

Follow-up: can you avoid recomputing the sum of the path at every node?

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Can the tree be empty? (Yes -> return [])
- Must the path end at a LEAF? (Yes -> a path that hits the target at an
  internal node does not count)
- Can values be negative / zero? (Yes -> no pruning on "sum > target")
- Do I return values or nodes? (Values, as lists of ints)
- How deep can the tree get? (Skewed + Python recursion limit -> consider
  iterative DFS)
"""

from collections import deque
from typing import List, Optional

# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

# ================================================================================
# MY APPROACH #1 — Backtracking DFS, recompute sum(path) at every node (mine)
# ================================================================================
"""
### Idea
DFS with ONE shared list `path`. On entering a node append its value; if the
node is a leaf and sum(path) == targetSum, save a COPY of the path. Recurse into
left and right, then pop the value (backtrack) on the way out.

### Why does it work?
`path` always holds exactly the root-to-current-node values (append on entry,
pop on exit). Saving `path[:]` (a copy) at a valid leaf freezes the answer
before later backtracking mutates the list.

### Complexity
- TC: O(n * h) — `sum(path)` costs O(h) and is evaluated at every node
  (it runs BEFORE the leaf check in this code); plus O(h) per saved path
- SC: O(h) recursion stack + path list, plus the output

### Pros
- Correct, short, classic backtracking template.
- Doesn't prune, so negative values are handled.

### Cons
- Recomputes the sum from scratch at every node: O(h) work per node instead of
  O(1). The cheap fix is to carry a running sum / remaining target.
- The leaf check should come FIRST so that sum() runs only at leaves
  (`node.left is None and node.right is None and sum(path) == targetSum`).
- The early `return` inside the if-block duplicates the `path.pop()`; easy to
  forget one of the two pops and corrupt the path.
- Recursion depth = height -> stack-overflow risk on skewed trees.

### Bottleneck
The repeated `sum(path)`. Everything else is already optimal for output
enumeration.
"""


class SolutionBacktrackSum:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        result = []

        def dfs(node, path):
            if node is None:
                return
            path.append(node.val)
            if sum(path) == targetSum and node.left is None and not node.right:
                result.append(path[:])
                path.pop()
                return
            dfs(node.left, path)
            dfs(node.right, path)
            path.pop()

        dfs(root, [])
        return result


# ================================================================================
# MY APPROACH #2 — Backtracking DFS with a running remaining target (optimal DFS)
# ================================================================================
"""
### Idea
Same backtracking, but pass `remaining = targetSum - (sum so far)` down the
recursion. At each node subtract node.val; at a leaf, the path is valid iff
remaining == 0. No `sum(path)` needed.

### Why does it work?
`remaining` is just the target minus the prefix sum, updated in O(1) at every
step, so the leaf test is O(1). `path` still tracks the actual values via
append / pop.

### Complexity
- TC: O(n + k*h) — O(1) work per node, plus O(h) to copy each of the k valid
  paths; worst case O(n * h) only if many paths are valid (e.g. all zeros)
- SC: O(h) recursion stack + path, plus the output

### Pros
- Removes the O(h) sum from every node; the usual "optimal" answer.
- Single shared path list -> no per-node list copies.
- Single pop at the end of the function (no early return needed).

### Cons
- Still recursive -> recursion limit on very deep trees.
- Must copy the path when saving (`path[:]` / `list(path)`), or the output
  will end up full of empty lists.

### Bottleneck
Only the unavoidable O(h) copy for each valid path.
"""


class SolutionBacktrackRemaining:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        result = []
        path = []

        def dfs(node, remaining):
            if node is None:
                return

            path.append(node.val)
            remaining -= node.val

            if node.left is None and node.right is None:
                if remaining == 0:
                    result.append(path[:])
            else:
                dfs(node.left, remaining)
                dfs(node.right, remaining)

            path.pop()

        dfs(root, targetSum)
        return result


# ================================================================================
# MY APPROACH #3 — Recursive DFS passing a NEW path (no explicit backtracking)
# ================================================================================
"""
### Idea
Pass `path + [node.val]` (a new list) to each child. Because every call has its
own list, nothing needs to be popped and no copy is needed when saving.

### Complexity
- TC: O(n * h) — building a new list of length up to h at every node
- SC: O(h^2) worst case — each active call frame holds its own list
  (1 + 2 + ... + h elements along the current path), plus the output

### Pros
- Easiest to get right: no pop, no copy, no shared state.

### Cons
- Allocates a new list at every node -> worse time and space than #2.
- Interviewers usually follow up with "can you avoid the copies?"
"""


class SolutionNewPath:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        result = []

        def dfs(node, remaining, path):
            if node is None:
                return

            remaining -= node.val
            path = path + [node.val]

            if node.left is None and node.right is None:
                if remaining == 0:
                    result.append(path)
                return

            dfs(node.left, remaining, path)
            dfs(node.right, remaining, path)

        dfs(root, targetSum, [])
        return result


# ================================================================================
# MY APPROACH #4 — Iterative DFS with (node, remaining, path) on a stack
# ================================================================================
"""
### Idea
Replace recursion with an explicit stack whose entries carry their own state:
(node, remaining, path). Pop an entry, extend the path, and either record it
(valid leaf) or push the children with the updated remaining and path.

### Complexity
- TC: O(n * h) — a new path list (up to length h) is built for each node
- SC: O(n * h) worst case for stored paths (O(h^2) for a balanced-ish stack),
  plus the output

### Pros
- No recursion limit -> safe for deeply skewed trees.
- Each stack entry is self-contained; no backtracking bookkeeping.

### Cons
- Per-node path copies make it heavier than the recursive backtracking (#2).
- More code than recursion.

### What can be improved?
Use parent pointers (#5) to avoid storing a full path per entry.
"""


class SolutionIterativeStack:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        if not root:
            return []

        result = []
        stack = [(root, targetSum, [])]

        while stack:
            node, remaining, path = stack.pop()
            remaining -= node.val
            path = path + [node.val]

            if node.left is None and node.right is None:
                if remaining == 0:
                    result.append(path)
                continue

            if node.right:
                stack.append((node.right, remaining, path))
            if node.left:
                stack.append((node.left, remaining, path))

        return result


# ================================================================================
# MY APPROACH #5 — Iterative DFS + parent map, rebuild path only for valid leaves
# ================================================================================
"""
### Idea
Walk the tree iteratively, storing only (node, remaining) on the stack and a
`parent` dict (node -> parent). When a leaf has remaining == 0, rebuild the path
by walking up the parent links to the root and reversing it.

### Why does it work?
Every node has a unique root-to-node path, and the parent links encode it. We
only pay the O(h) reconstruction for leaves that actually match.

### Complexity
- TC: O(n + k*h) — O(1) per node, O(h) to rebuild each of the k valid paths
- SC: O(n) — the parent map, plus the output

### Pros
- No recursion and no per-node path copies; work proportional to the answer.

### Cons
- O(n) extra space for the parent map (more than the O(h) of recursion).
- More moving parts (map + reconstruction + reverse).

### Bottleneck
The O(n) parent map; recursion (#2) uses only O(h).
"""


class SolutionParentMap:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        if not root:
            return []

        result = []
        parent = {root: None}
        stack = [(root, targetSum - root.val)]

        while stack:
            node, remaining = stack.pop()

            if node.left is None and node.right is None:
                if remaining == 0:
                    path = []
                    cur = node
                    while cur:
                        path.append(cur.val)
                        cur = parent[cur]
                    result.append(path[::-1])
                continue

            if node.right:
                parent[node.right] = node
                stack.append((node.right, remaining - node.right.val))
            if node.left:
                parent[node.left] = node
                stack.append((node.left, remaining - node.left.val))

        return result


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
PATH SUM II
│
├── Definition
│   └── All root-to-LEAF paths whose values add up to targetSum
│
├── Core Insight
│   └── Backtracking on a tree: append on entry, pop on exit.
│       Track the running sum (or remaining target) in O(1).
│
├── Backtracking + sum(path)  (my solution)
│   └── recomputes the sum at every node
│       └── O(n*h) time, O(h) space
│
├── Backtracking + remaining target  (optimal DFS)
│   └── remaining -= node.val; leaf and remaining == 0 -> save path[:]
│       └── O(n + k*h) time, O(h) space
│
├── Recursive with a new path each call
│   └── path + [val]; no pop, no copy
│       └── O(n*h) time, O(h^2) space
│
├── Iterative DFS (stack of (node, remaining, path))
│   └── no recursion limit, but copies the path per node
│
└── Iterative DFS + parent map
    └── store (node, remaining); rebuild the path only for valid leaves
        └── O(n + k*h) time, O(n) space
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Path must end at a LEAF: node.left is None AND node.right is None. Hitting
  the target at an internal node does NOT count."
- "Values can be negative or zero -> never prune when the sum exceeds the
  target; always walk to the leaves."
- "Save a COPY of the path (`path[:]`): the shared list keeps being mutated by
  later backtracking."
- "Every `append` needs exactly one matching `pop` on EVERY exit path. Using an
  early `return` after saving the path means you must pop before returning
  (or restructure so there is one pop at the end)."
- "Carry `remaining = target - prefix_sum` instead of calling sum(path): O(1)
  per node instead of O(h)."
- "Put the cheap leaf check first, the sum check second."
- "Empty tree -> []. A single node equal to the target -> [[val]]."
- "k = number of valid paths: output size is O(k*h), so O(h) per answer is
  unavoidable."
- "Same family: LC 112 (Path Sum), LC 437 (Path Sum III, prefix sums), LC 257
  (Binary Tree Paths), LC 129 (Sum Root to Leaf Numbers), LC 124 (Max Path
  Sum), LC 39 / 40 (Combination Sum, same backtracking template)."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                       | Core Idea                                           | TC         | SC (extra) | Pros                                   | Cons                                           | When to Use                          |
|--------------------------------|-----------------------------------------------------|------------|------------|----------------------------------------|------------------------------------------------|--------------------------------------|
| Backtracking + sum(path) (mine)| Shared path; sum recomputed at each node            | O(n*h)     | O(h)       | Short; classic template                | Recomputes sum every node                      | Quick correct first draft            |
| Backtracking + remaining       | Shared path; carry remaining target                 | O(n + k*h) | O(h)       | Optimal DFS; no per-node copies        | Recursion limit; must copy on save             | Default / best answer                |
| Recursive new path             | Pass path + [val]; no pop                           | O(n*h)     | O(h^2)     | No backtracking bugs                   | Copies at every node                           | Simplicity over performance          |
| Iterative stack (path copies)  | Stack of (node, remaining, path)                    | O(n*h)     | O(n*h)     | No recursion limit                     | Heavy path copies                              | "Do it iteratively" (simple)         |
| Iterative + parent map         | Stack of (node, remaining); rebuild from parents    | O(n + k*h) | O(n)       | No recursion; work ~ answer size       | O(n) map; more code                            | Iterative with good time complexity  |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Tree DFS + backtracking (path enumeration).
- Go-to answer: "I run a DFS with one shared path list. On entering a node I
  append its value and subtract it from the remaining target. At a leaf with
  remaining equal to zero I save a copy of the path. Then I pop the value on
  the way back up. That's O(n) traversal plus O(h) per saved path, with O(h)
  extra space. I don't prune on sum > target because values can be negative.
  My first version recomputed sum(path) at each node, which is O(n*h); carrying
  the remaining target fixes that."
- Good to mention: why the path is copied when saved, why every exit path must
  pop, and that the leaf condition is mandatory.
- Common follow-ups:
  * "Avoid recomputing the sum?" -> carry the remaining target.
  * "Do it iteratively?" -> stack of (node, remaining, path), or parent map.
  * "Only return True/False (any path)?" -> LC 112, return on the first match.
  * "Path can start / end anywhere?" -> LC 437, prefix sums + hash map.
  * "Count the paths instead of listing them?" -> keep a counter, no path list.
"""