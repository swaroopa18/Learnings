"""
================================================================================
 PROBLEM: Diameter of Binary Tree (LeetCode 543)
================================================================================
Given the `root` of a binary tree, return the LENGTH of the DIAMETER of the
tree. The diameter is the length of the LONGEST path between ANY two nodes in
the tree. This path may or may not pass through the root. The length of a path
is the number of EDGES between the two nodes.

Example: root = [1,2,3,4,5]   ->  3
         (path 4 -> 2 -> 1 -> 3  or  5 -> 2 -> 1 -> 3, i.e. 3 edges)
Example: root = [1,2]         ->  1
Example: root = [1]           ->  0

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Is the length measured in EDGES or NODES? (EDGES. A single node has diameter
  0. Mixing this up is the classic off-by-one — with node-counted heights
  (null = 0, leaf = 1) the edge count through a node is `left + right`, with
  NO `+ 1` or `- 1`.)
- Must the longest path pass through the ROOT? (No — it can live entirely
  inside a subtree, e.g. a long zig-zag deep in the left subtree. That is why we
  must check EVERY node, not just the root.)
- Are the path endpoints required to be leaves? (No — but the longest path
  always ends at leaves anyway, since extending a path never makes it shorter.)
- Do node VALUES matter? (No — only the shape. Contrast with LC 124 (Maximum
  Path Sum) where values matter.)
- How big can the tree be / how deep? (Up to 10^4 nodes; a skewed tree is 10^4
  deep, so recursive solutions in Python can hit the recursion limit — the
  iterative post-order version avoids that.)

"""

from collections import deque
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ================================================================================
# 🔑🔑🔑  STRONG POINTS FOR "TREE DIAMETER / PATH THROUGH A NODE" PROBLEMS  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   The longest path "bending" at a node X uses the DEEPEST chain     │
    │   going down on each side:                                          │
    │        edges through X = height(X.left) + height(X.right)           │
    │   (height counted in NODES: null = 0, leaf = 1).                    │
    │   Diameter = MAX of that value over ALL nodes.                      │
    │                                                                     │
    │   Compute it in ONE post-order DFS: each call RETURNS its height    │
    │   (for its parent) and RECORDS left + right in a running maximum.   │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

This is the textbook example of the "return one thing, record another" tree-DP
pattern: the value a subtree must report UP to its parent (its height) is
different from the value you are optimizing (the best path bending inside it).
Key ideas:

1. **Every path has a unique TOPMOST node** (the one closest to the root). The
   path goes down-left from it and down-right from it. So enumerating the
   topmost node covers every possible path exactly once.

2. **At a given topmost node X the best path = deepest left chain + deepest
   right chain** = `height(left) + height(right)` in EDGES when heights are
   counted in nodes (null = 0, leaf = 1). Example: a leaf has `0 + 0 = 0`.

3. **Post-order DFS is the natural fit:** a node needs the heights of both
   children BEFORE it can compute its own candidate and its own height.

4. **Return `1 + max(left, right)` to the parent, but update the answer with
   `left + right`.** The path through X can use BOTH sides, but the parent can
   extend only ONE side (a path can't fork upward), so what X returns must be
   one chain, not two.

5. **Recomputing heights for every node is wasteful.** Calling `dfs(left) +
   dfs(right)` separately at each node re-walks the same subtrees again and
   again (O(n * h)). One DFS that computes heights ONCE and updates the answer
   on the way up is O(n).

6. **The same pattern solves a whole family:** LC 124 (Binary Tree Maximum Path
   Sum), LC 687 (Longest Univalue Path), LC 110 (Balanced Binary Tree), LC 1245
   (Tree Diameter on a general tree), LC 337 (House Robber III).
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea
For EVERY node, compute the height of its left subtree and of its right subtree
(each with its own DFS) and add them — that is the longest path whose topmost
node is this one. Take the maximum over all nodes. That is exactly your first
solution (a BFS visits every node; `dfs` computes a height). It is correct, but
each node's two DFS calls walk its whole subtree, so deep trees repeat a lot of
work.

### The key insight: heights are already computed on the way up
When a DFS finishes a node, it has just computed the heights of both children to
return its own height. So the candidate `left + right` is available FOR FREE at
that moment. One post-order pass can both compute heights and track the best
`left + right`.

### Step-by-step trace (single DFS): tree [1, 2, 3, 4, 5]
```
        1
       / \
      2   3
     / \
    4   5
```
```
dfs(4): left=0, right=0 -> diameter=max(0, 0)=0, return 1
dfs(5): left=0, right=0 -> diameter=max(0, 0)=0, return 1
dfs(2): left=1, right=1 -> diameter=max(0, 2)=2, return 2
dfs(3): left=0, right=0 -> diameter stays 2,     return 1
dfs(1): left=2, right=1 -> diameter=max(2, 3)=3, return 3
answer = 3 ✅   (path 4 -> 2 -> 1 -> 3)
```

### Why it must check every node: path NOT through the root
```
tree [1, 2, null, 3, 4, 5, null, null, 6]

        1
       /
      2
     / \
    3   4
   /     \
  5       6

Through the root: 1 -> 2 -> 3 -> 5            = 3 edges
Bending at node 2: 5 -> 3 -> 2 -> 4 -> 6      = 4 edges   <- the diameter
Checking only the root would return 3 (wrong); checking every node gives 4 ✅
```

### Where the brute force wastes work (your first solution)
```
For a chain 1 -> 2 -> 3 -> ... -> n:
  node 1 calls dfs on a subtree of size n-1
  node 2 calls dfs on a subtree of size n-2
  ...
total ~ n^2 / 2 steps -> O(n^2) for a skewed tree
```

### The "aha" moment to remember 🎯
"Diameter = max over nodes of (left height + right height). Return the height
(one chain) to the parent, but record left + right (two chains) in a running
maximum — all in a single post-order DFS."
"""

# ================================================================================
# ALTERNATIVE APPROACH 1 — Brute Force: BFS Over Nodes + Fresh Height DFS per Node
# ================================================================================
"""
### Thought Process 🧠
Visit every node with a level-order traversal. For each node, compute the height
of its left subtree and its right subtree by calling a separate recursive
`dfs(height)` function on each, and use `dfs(left) + dfs(right)` as the length of
the longest path whose topmost node is this node. The answer is the maximum
over all nodes.

### Complexity
- TC: O(n * h) in the worst case — each node's two height DFS calls cost the
  size of that node's subtree; summed over all nodes this is the sum of
  subtree sizes: O(n^2) for a skewed tree (n * h with h = n), O(n log n) for a
  balanced one
- SC: O(w) for the BFS queue (w = widest level, up to n / 2) + O(h) recursion
  stack for the height DFS

### Pros
- Easy to derive straight from the definition: "longest path through a node =
  left depth + right depth, then max over nodes".
- Separates concerns clearly: BFS enumerates nodes, DFS measures heights.
- Perfect for testing the optimized versions.

### Cons
- Re-computes the same subtree heights many times (every ancestor re-walks
  the whole subtree below it).
- O(n^2) on skewed trees (10^4 nodes -> ~5 * 10^7 steps, and the recursion
  depth also hits 10^4).
- Uses two traversals (a BFS plus nested DFS) where one DFS suffices.

### Bottleneck
Each ancestor recomputes heights that its descendants already computed. Ask:
"can the DFS that computes a node's height also report the candidate diameter
at that node?" -> Yes: one post-order DFS that updates a running maximum.
"""


class SolutionBFSHeights:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0

        def dfs(node):
            if node is None:
                return 0

            left = dfs(node.left)
            right = dfs(node.right)
            return 1 + max(left, right)

        queue = deque([root])
        max_diameter = 0

        while queue:
            node = queue.popleft()
            left = node.left
            right = node.right
            max_diameter = max(max_diameter, dfs(left) + dfs(right))
            if left:
                queue.append(left)
            if right:
                queue.append(right)
        return max_diameter


# ================================================================================
# MY APPROACH — Single Post-Order DFS with a Running Maximum (optimal)
# ================================================================================
"""
### Idea
Write `dfs(node)` returning the HEIGHT of the subtree rooted at `node`, counted
in nodes (`None` -> 0, so a leaf returns 1). While computing it, take the left
and right heights and update `self.diameter = max(self.diameter, left + right)`
— the number of edges of the longest path whose topmost node is `node`. Return
`1 + max(left, right)` to the parent. After `dfs(root)`, `self.diameter` holds
the answer.

### Complexity
- TC: O(n) — every node is visited exactly once, O(1) work per node
- SC: O(h) — recursion depth equals the tree height (O(log n) balanced, O(n)
  skewed); plus one integer for the running maximum

### Pros
- Optimal time: each node's height is computed ONCE and reused.
- Elegant: "return height, record diameter" captures the key idea that the
  parent can only extend ONE child chain but the answer may use BOTH.
- Handles a path that does not pass through the root automatically, since every
  node's `left + right` is considered.
- `self.diameter` is reset to 0 on each call to `diameterOfBinaryTree`, so
  reusing the same `Solution` instance across test cases is safe.

### Cons
- Recursion depth can reach 10^4 on a skewed tree; Python's default limit is
  1000, so it may need `sys.setrecursionlimit(...)` or the iterative version.
- Uses mutable state (`self.diameter`) updated inside a nested function — slightly
  less clean than returning a tuple or using `nonlocal`.
- Forgetting that `dfs` returns NODE-count height (so `left + right` is already
  the EDGE count) is the classic off-by-one.

### DSA Buddy Point 🧠
"Tree DP pattern: the value you RETURN to the parent (one chain) differs from
the value you are OPTIMIZING (a path that may bend at this node). Return one,
record the other."

### What can be improved?
Complexity-wise nothing — O(n) time is optimal (every node must be seen).
Optional: use `nonlocal` or return a `(height, diameter)` tuple to avoid instance
state (next approach), and use an explicit stack if recursion depth could exceed
Python's limit (the iterative post-order approach below).
"""


class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0

        def dfs(node):
            if node is None:
                return 0

            left = dfs(node.left)
            right = dfs(node.right)

            self.diameter = max(self.diameter, left + right)
            return 1 + max(left, right)

        self.diameter = 0
        dfs(root)

        return self.diameter


# ================================================================================
# ALTERNATIVE APPROACH 2 — Pure DFS Returning (height, diameter) Tuples (no state)
# ================================================================================
"""
### Thought Process 🧠
Make `dfs(node)` return BOTH values for its subtree: `(height, best_diameter)`.
For `None` return `(0, 0)`. For a node, combine the children's results:
`height = 1 + max(lh, rh)` and
`diameter = max(ld, rd, lh + rh)` (the best path inside the left subtree, inside
the right subtree, or bending at this node).

### Complexity
- TC: O(n)
- SC: O(h) — recursion depth (plus tiny tuples)

### Pros
- Purely functional: no instance variable, no `nonlocal`, trivially thread- and
  reuse-safe.
- Makes the recurrence explicit: `diameter(T) = max(diameter(L), diameter(R),
  height(L) + height(R))` — easy to prove correct by induction.

### Cons
- Allocates a tuple per call (slightly more overhead than a shared integer).
- Same recursion-depth limitation as the other recursive versions.

### DSA Buddy Point 🧠
"When a subtree must report several facts to its parent, return them as a
tuple — each call becomes a pure function of its children's results."
"""


def diameter_tuple(root: Optional[TreeNode]) -> int:
    def dfs(node):
        if node is None:
            return 0, 0
        lh, ld = dfs(node.left)
        rh, rd = dfs(node.right)
        return 1 + max(lh, rh), max(ld, rd, lh + rh)

    return dfs(root)[1]


# ================================================================================
# ALTERNATIVE APPROACH 3 — Iterative Post-Order (explicit stack, no recursion)
# ================================================================================
"""
### Thought Process 🧠
Avoid recursion entirely. Produce an order in which every node appears BEFORE its
parent... Do a stack-based pre-order that visits `node, then pushes left, then
right` and records the visit order; reading that order BACKWARD guarantees every
child is processed before its parent. Walk it backward keeping a dictionary
`height[node]` (missing / `None` child -> 0): for each node set
`lh = height.get(left, 0)`, `rh = height.get(right, 0)`, update
`diameter = max(diameter, lh + rh)` and store `height[node] = 1 + max(lh, rh)`.

### Complexity
- TC: O(n)
- SC: O(n) — the visit order list, the stack, and the height dictionary
  (no recursion, so no recursion-limit risk)

### Pros
- Immune to Python's recursion limit — safe for 10^4-deep skewed trees.
- Makes the "children before parent" requirement explicit.
- Same answer as the recursive DFS, with the same simple per-node formula.

### Cons
- More code and extra O(n) memory (order list + heights) compared with the
  recursive version's O(h) stack.
- Dictionary keyed by node objects (hashable by identity) — fine here but not
  possible if nodes are unhashable.

### DSA Buddy Point 🧠
"Reverse of a (node, left, right)-style pre-order visits children before
parents — a cheap way to simulate post-order iteratively."
"""


def diameter_iterative(root: Optional[TreeNode]) -> int:
    if root is None:
        return 0
    order = []
    stack = [root]
    while stack:
        node = stack.pop()
        order.append(node)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)

    height: dict = {}
    diameter = 0
    for node in reversed(order):
        lh = height.get(node.left, 0)
        rh = height.get(node.right, 0)
        diameter = max(diameter, lh + rh)
        height[node] = 1 + max(lh, rh)
    return diameter


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
DIAMETER OF BINARY TREE
│
├── Brute Force (your first code)
│   └── BFS over every node; compute dfs(left) + dfs(right) fresh at each one
│       -> O(n * h) time (O(n^2) skewed), O(w + h) space
│
├── Bottleneck
│   └── Every ancestor re-walks the same subtrees to recompute heights
│
├── Key Insight
│   └── Longest path bending at node X = height(left) + height(right) (edges,
│       node-counted heights). Diameter = max over ALL nodes. The parent can
│       extend only ONE chain: RETURN 1 + max(l, r), RECORD l + r
│
├── My Approach — Single post-order DFS + running max (OPTIMAL)
│   └── self.diameter = max(self.diameter, left + right); return 1 + max(left, right)
│       -> O(n) time, O(h) space
│
├── DFS returning (height, diameter) tuples
│   └── diameter = max(ld, rd, lh + rh) -> O(n) time, O(h) space, no state
│
└── Iterative post-order (explicit stack)
    └── reverse of (node, left, right) pre-order + heights dict
        -> O(n) time, O(n) space, no recursion-limit risk
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Diameter = max over every node of (height(left) + height(right)) — counted in
  EDGES when height(None) = 0 and a leaf's height = 1."
- "The longest path need NOT pass through the root — check every node."
- "Return the HEIGHT to the parent (one chain), but update the answer with
  left + right (two chains) — a parent can't use both child chains of a child."
- "Compute heights ONCE in a post-order DFS; calling a fresh height function at
  every node is O(n * h)."
- "A leaf contributes 0 (0 + 0); a single-node tree has diameter 0."
- "Node values are irrelevant — only the shape matters (unlike LC 124)."
- "Recursion depth = tree height (up to 10^4 skewed): raise the recursion limit
  or use the iterative post-order version."
- "Same pattern: LC 124 (Max Path Sum), LC 687 (Longest Univalue Path), LC 110
  (Balanced Binary Tree), LC 1245 (Tree Diameter), LC 337 (House Robber III)."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                           | Core Idea                                                        | TC           | SC       | Pros                                                | Cons                                                         | When to Use                              |
|------------------------------------|------------------------------------------------------------------|--------------|----------|-----------------------------------------------------|--------------------------------------------------------------|------------------------------------------|
| BFS + fresh height DFS per node    | max over nodes of dfs(left) + dfs(right)                         | O(n * h)     | O(w + h) | Straight from the definition, great oracle          | Recomputes heights; O(n^2) on skewed trees                   | Baseline / first idea (your 1st code)    |
| Single post-order DFS + running max| return 1 + max(l, r); record l + r in self.diameter              | O(n)         | O(h)     | Optimal, elegant "return one, record another"       | Recursion-depth risk; mutable state                          | Default answer (your 2nd code)           |
| DFS returning (height, diameter)   | diameter = max(ld, rd, lh + rh)                                  | O(n)         | O(h)     | Purely functional, easy induction proof             | Tuple allocation per call; recursion depth                   | When you want no shared state            |
| Iterative post-order               | Reverse pre-order + heights dict, no recursion                   | O(n)         | O(n)     | No recursion limit issues                           | More code and extra memory                                   | Very deep / skewed trees                 |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Tree DP / post-order DFS where the RETURNED value (height) differs
  from the OPTIMIZED value (path bending at a node). Relatives: LC 124
  (Binary Tree Maximum Path Sum), LC 687 (Longest Univalue Path), LC 110
  (Balanced Binary Tree), LC 104 (Maximum Depth), LC 1245 (Tree Diameter),
  LC 337 (House Robber III).
- Go-to answer: "Run a post-order DFS where each call returns the height of its
  subtree (None -> 0, leaf -> 1). At each node, the longest path with this node
  as its topmost node has `left + right` edges, so I update a running maximum
  with that, and return `1 + max(left, right)` to the parent. The running maximum
  is the diameter. O(n) time, O(h) space."
- Good to call out: edges vs nodes (single node -> 0), that the diameter may not
  pass through the root, why the parent receives only ONE chain, and why
  recomputing heights per node is O(n * h).
- Common follow-ups:
  * "Return the actual path, not just its length?" -> Also return the deepest
    leaf (or the list of nodes) for each subtree and rebuild the path at the best
    node.
  * "Node VALUES count (maximum path sum)?" -> LC 124: same recursion, but
    return `val + max(0, left_gain, right_gain)` and record
    `val + max(0, left_gain) + max(0, right_gain)`.
  * "N-ary tree or general graph?" -> Keep the TWO largest child heights at each
    node (LC 1245), or run BFS/DFS twice from the farthest node.
  * "Skewed tree of 10^5 nodes in Python?" -> Use the iterative post-order or
    raise the recursion limit.
"""


def build_tree(vals):
    """Build a tree from a LeetCode-style level-order list with None holes."""
    if not vals:
        return None
    root = TreeNode(vals[0])
    q = deque([root])
    i = 1
    while q and i < len(vals):
        node = q.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            q.append(node.right)
        i += 1
    return root


if __name__ == "__main__":
    import random

    def oracle(root) -> int:
        """Independent check: longest path in the undirected tree via double BFS."""
        adj: dict = {}
        stack = [root]
        while stack:
            node = stack.pop()
            adj.setdefault(node, [])
            for child in (node.left, node.right):
                if child:
                    adj.setdefault(child, []).append(node)
                    adj[node].append(child)
                    stack.append(child)

        def farthest(start):
            dist = {start: 0}
            q = deque([start])
            last = start
            while q:
                cur = q.popleft()
                last = cur
                for nxt in adj[cur]:
                    if nxt not in dist:
                        dist[nxt] = dist[cur] + 1
                        q.append(nxt)
            return last, dist[last]

        a, _ = farthest(root)
        _, d = farthest(a)
        return d

    classics = {
        (1, 2, 3, 4, 5): 3,
        (1, 2): 1,
        (1,): 0,
        (1, 2, 3): 2,
        (1, None, 2, None, 3): 2,
        (1, 2, None, 3, 4, 5, None, None, 6): 4,  # best path does NOT use the root
    }

    def random_tree(n: int):
        root = TreeNode(0)
        free = [(root, "left"), (root, "right")]
        for k in range(1, n):
            parent, side = free.pop(random.randrange(len(free)))
            node = TreeNode(k)
            setattr(parent, side, node)
            free.append((node, "left"))
            free.append((node, "right"))
        return root

    fns = [
        SolutionBFSHeights().diameterOfBinaryTree,
        Solution().diameterOfBinaryTree,
        diameter_tuple,
        diameter_iterative,
    ]

    for vals, expected in classics.items():
        for f in fns:
            assert f(build_tree(list(vals))) == expected, (f.__name__, vals, expected)
        assert oracle(build_tree(list(vals))) == expected, ("oracle", vals)

    count = len(classics)
    for _ in range(2000):
        t = random_tree(random.randint(1, 25))
        expected = oracle(t)
        for f in fns:
            assert f(t) == expected, (f.__name__, expected)
        count += 1

    # skewed chains: recursion-friendly size for all, big size for the iterative one
    chain = TreeNode(0)
    cur = chain
    for k in range(1, 400):
        cur.left = TreeNode(k)
        cur = cur.left
    for f in fns:
        assert f(chain) == 399, f.__name__
    big = TreeNode(0)
    cur = big
    for k in range(1, 20000):
        cur.right = TreeNode(k)
        cur = cur.right
    assert diameter_iterative(big) == 19999
    count += 2

    print("All approaches agree on", count, "cases ✅")