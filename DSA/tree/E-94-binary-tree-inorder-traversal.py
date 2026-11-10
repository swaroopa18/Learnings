"""
================================================================================
 PROBLEM: Binary Tree Inorder Traversal (LeetCode 94)
================================================================================
Given: the root of a binary tree.
Task: return the inorder traversal of its nodes' values, i.e.
LEFT subtree -> ROOT -> RIGHT subtree.

Example:
        1
       / \
      2   3
     / \
    4   5
  Inorder = [4, 2, 5, 1, 3]

Follow-up: recursion is trivial — can you do it iteratively?

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Can the tree be empty? (Yes -> return [])
- Is it a BST? (Not required; but for a BST, inorder gives SORTED order —
  worth mentioning)
- How deep can the tree get? (If it can be very skewed, e.g. 10^5 nodes,
  Python's default recursion limit of ~1000 makes recursion unsafe -> prefer
  the iterative or Morris solution)
- Am I allowed to temporarily modify the tree? (Decides whether Morris
  traversal is on the table)
"""

from typing import List, Optional

# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

# ================================================================================
# MY APPROACH #1 — Recursive with concatenation (simplest, direct definition)
# ================================================================================
"""
### Idea
Translate the definition literally: inorder(root) = inorder(root.left)
+ [root.val] + inorder(root.right), with an empty list for a None node.

### Complexity
- TC: O(n) calls, but each call builds a NEW list by concatenation, copying
  every element of its subtree. Total copying cost is O(n * h) —
  O(n^2) on a skewed tree (e.g. every node has only a left child).
- SC: O(h) recursion depth + O(n) for the output, plus transient temporary
  lists created by the concatenations

### Pros
- Shortest possible code; reads exactly like the definition.

### Cons
- Hidden quadratic cost from repeated list concatenation on skewed trees.
- Allocates many throw-away lists.
- Recursion depth = tree height; may hit Python's recursion limit.

### Bottleneck
Each recursive call returns a fresh list that the caller then copies into
another fresh list. Fix: pass ONE shared result list down the recursion and
`append` into it (amortized O(1) per node) -> approach #2.
"""


class SolutionConcat:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if root is None:
            return []
        return (
            self.inorderTraversal(root.left)
            + [root.val]
            + self.inorderTraversal(root.right)
        )


# ================================================================================
# MY APPROACH #2 — Recursive with a shared result list (your Approach 2)
# ================================================================================
"""
### Idea
Use a helper `inorder(node, res)` that recurses left, appends node.val to a
single shared list, then recurses right. The list is created once, so there
is no copying between calls.

### Why does it work?
The call order is exactly L -> root -> R. The `append` happens after the left
subtree is fully done and before the right subtree starts, which is the
definition of inorder. Because every node appends exactly once, `res` ends
up in the right order.

### Complexity
- TC: O(n) — each node is visited exactly once, O(1) work per node
- SC: O(h) — recursion stack depth equals tree height h
  (O(log n) balanced, O(n) skewed), plus O(n) for the required output

### Pros
- Clean, easy to write and explain; true O(n) time.
- Same template for preorder / postorder — just move the append line.

### Cons
- Recursion depth = height -> stack overflow risk in Python on deep/skewed
  trees (default limit ~1000).
- Interviewers usually ask for the iterative version next.

### Bottleneck
Reliance on the implicit call stack. Replace it with an explicit stack that
we manage ourselves -> approach #3 (no recursion limit issues).
"""


class SolutionRecursive:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        def inorder(node, res):
            if node is None:
                return
            inorder(node.left, res)
            res.append(node.val)
            inorder(node.right, res)

        res = []
        inorder(root, res)
        return res


# ================================================================================
# MY APPROACH #3 — Iterative with an explicit stack (your Approach 1)
# ================================================================================
"""
### Idea
Simulate the recursion's call stack by hand:
  1. From `curr`, go as far LEFT as possible, pushing every node on the way.
  2. Pop the top (the leftmost unvisited node) -> visit it (append its val).
  3. Move to its RIGHT child and repeat (the right subtree gets the same
     "go left, push everything" treatment).
Loop while there is something to process: `while stack or curr`.

### Why does it work?
The stack holds exactly the ancestors whose LEFT subtree is currently being
explored and which are still waiting to be visited. Popping returns to the
nearest such ancestor right after its left subtree is finished — that is
precisely when inorder visits the node. Then we explore its right subtree.

### Complexity
- TC: O(n) — each node is pushed once and popped once
- SC: O(h) — stack holds at most one root-to-node path (O(n) if skewed),
  plus O(n) for the output

### Pros
- No recursion -> no stack-overflow risk from Python's recursion limit.
- Doesn't modify the tree.
- Easy to turn into a lazy iterator (BST Iterator, LC 173) — pause after
  each pop.

### Cons
- Still O(h) extra space.
- The `while stack or curr` / inner `while curr` structure is easy to get
  subtly wrong under interview pressure.

### What can be improved?
- Space can go down to O(1) with Morris traversal (approach #4), at the
  cost of temporarily modifying the tree.
"""


class SolutionIterative:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        stack, res = [], []
        curr = root

        while stack or curr:
            while curr:
                stack.append(curr)
                curr = curr.left

            curr = stack.pop()
            res.append(curr.val)

            curr = curr.right

        return res


# ================================================================================
# MY APPROACH #4 — Morris Traversal (O(1) extra space, bonus / follow-up)
# ================================================================================
"""
### Idea
Use the tree's own unused `right = None` pointers as a temporary "return
path" so no stack is needed. For the current node `curr`:
  - If `curr.left` is None: visit curr, then go right.
  - Else find its INORDER PREDECESSOR `pred` (the rightmost node in
    curr.left's subtree).
      * If pred.right is None: set pred.right = curr (create a temporary
        thread back to curr), then go left.
      * Else (pred.right is curr -> we already explored the left subtree):
        remove the thread (pred.right = None), visit curr, go right.

### Why does it work?
The thread guarantees that once the left subtree is finished, the walk
returns to `curr` automatically. Each edge is traversed at most a constant
number of times (once to find a predecessor, once to remove the thread), so
the total work stays linear. The tree is fully restored by the end.

### Complexity
- TC: O(n) — each node's predecessor search is amortized: every edge on the
  left-subtree's right spine is walked at most twice overall
- SC: O(1) extra (excluding the O(n) output list)

### Pros
- True O(1) auxiliary space — no recursion, no stack.

### Cons
- Temporarily MODIFIES the tree (restored at the end) -> unsafe if other
  threads read the tree concurrently or if you crash mid-way.
- Harder to write and explain; easy to forget to remove the thread.

### What can be improved?
Nothing asymptotically; this is the space-optimal solution. In practice the
iterative stack version is preferred unless O(1) space is explicitly asked.
"""


class SolutionMorris:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        res = []
        curr = root
        while curr:
            if curr.left is None:
                res.append(curr.val)
                curr = curr.right
            else:
                pred = curr.left
                while pred.right and pred.right is not curr:
                    pred = pred.right

                if pred.right is None:
                    pred.right = curr  # create thread
                    curr = curr.left
                else:
                    pred.right = None  # remove thread
                    res.append(curr.val)
                    curr = curr.right
        return res


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
BINARY TREE INORDER TRAVERSAL
│
├── Definition
│   └── Left -> Root -> Right (for a BST this yields sorted order)
│
├── Recursive (direct)
│   ├── Concatenation: inorder(L) + [val] + inorder(R)
│   │   └── O(n*h) copying (O(n^2) skewed) — avoid
│   └── Shared list + append
│       └── O(n) time, O(h) recursion stack
│
├── Bottleneck
│   └── Recursion depth = height -> overflow risk; need own stack
│
├── Iterative (explicit stack)
│   ├── go left, push all nodes
│   ├── pop -> visit
│   └── move to right child, repeat
│       └── O(n) time, O(h) space
│
└── Morris Traversal
    ├── find inorder predecessor of curr in left subtree
    ├── thread pred.right -> curr, go left; on return remove thread, visit
    └── O(n) time, O(1) extra space (tree temporarily modified)
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Inorder = Left, Root, Right. For a BST it yields values in sorted order."
- "Recursive template: only the position of `res.append(node.val)` changes
  between preorder (before), inorder (between), postorder (after)."
- "Avoid `inorder(L) + [val] + inorder(R)` for big/skewed trees — list
  concatenation copies every subtree, giving O(n^2) worst case."
- "Iterative loop: `while stack or curr` — `curr` handles 'still going left',
  `stack` handles 'ancestors waiting to be visited'. Push on the way DOWN
  the left spine, visit on the way back UP (on pop), then go RIGHT."
- "The explicit stack replaces the call stack: space is O(h), O(n) when the
  tree is skewed, O(log n) when balanced."
- "Python's default recursion limit (~1000) can crash recursion on skewed
  trees; iterative/Morris don't have this issue."
- "Morris traversal: temporary threads via pred.right = curr give O(1) space;
  ALWAYS remove the thread on the second visit to restore the tree."
- "Same stack pattern powers: LC 173 (BST Iterator), LC 230 (Kth Smallest in
  BST), LC 98 (Validate BST), LC 99 (Recover BST)."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                  | Core Idea                                          | TC           | SC (extra)  | Pros                                   | Cons                                                    | When to Use                          |
|---------------------------|----------------------------------------------------|--------------|-------------|----------------------------------------|---------------------------------------------------------|--------------------------------------|
| Recursive (concatenation) | inorder(L) + [val] + inorder(R)                    | O(n*h) worst | O(h) + temp | Shortest; mirrors the definition       | Quadratic copying on skewed trees; recursion limit      | Tiny trees / readability             |
| Recursive (shared list)   | Helper appends to one shared list                  | O(n)         | O(h)        | Clean, linear, easy to adapt           | Recursion depth risk in Python                          | Default first answer                 |
| Iterative (stack)         | Push left spine, pop+visit, go right               | O(n)         | O(h)        | No recursion limit; tree untouched     | Loop invariants a bit subtle                            | Interviewer asks for non-recursive   |
| Morris traversal          | Thread predecessor.right -> curr, remove afterwards | O(n)         | O(1)        | Constant extra space                   | Temporarily modifies tree; trickier to code             | O(1)-space follow-up                 |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Tree DFS traversal (inorder). Foundation for BST problems —
  LC 98, 173, 230, 99.
- Go-to answer: "Inorder is left, root, right. Recursively that's O(n) time
  and O(h) space. Iteratively I keep a stack: go as far left as possible
  pushing nodes, pop and record a node, then move to its right child and
  repeat. That's O(n) time and O(h) space with no recursion-depth risk. If
  O(1) space is required, Morris traversal threads each node's inorder
  predecessor back to it and removes the thread afterwards."
- Good to mention: the concatenation version looks elegant but is O(n^2) on
  a skewed tree; passing a shared list fixes it.
- Common follow-ups:
  * "Preorder / postorder iteratively?" -> preorder: pop, visit, push right
    then left; postorder: modified preorder (root, right, left) reversed, or
    track last-visited node.
  * "Inorder of a BST gives?" -> sorted ascending order.
  * "Find the k-th smallest in a BST?" -> iterative inorder, stop after k pops.
  * "O(1) extra space?" -> Morris traversal.
  * "Level order instead?" -> BFS with a queue (LC 102).
"""