"""
================================================================================
 PROBLEM: Binary Tree Postorder Traversal (LeetCode 145)
================================================================================
Given: the root of a binary tree.
Task: return the postorder traversal of its nodes' values, i.e.
LEFT subtree -> RIGHT subtree -> ROOT (children are always visited before
their parent).

Example:
        1
       / \
      2   3
     / \
    4   5
  Postorder = [4, 5, 2, 3, 1]

Follow-up: recursion is trivial — can you do it iteratively?

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Can the tree be empty? (Yes -> return [])
- How deep can the tree get? (Very skewed trees + Python's default recursion
  limit of ~1000 make recursion risky -> prefer an iterative solution)
- Am I allowed to modify the tree (even temporarily)? (Decides whether
  Morris traversal, or the "detach children" trick, is on the table)
- Is O(h) extra space acceptable, or do they want O(1)? (Decides between
  one-stack and Morris)
"""

from typing import List, Optional

# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

# ================================================================================
# MY APPROACH #1 — Recursive with a shared result list (direct definition)
# ================================================================================
"""
### Idea
Helper `post(node, res)`: recurse left, recurse right, THEN append node.val.
The only difference from inorder/preorder is WHERE the append happens
(after both recursive calls).

### Complexity
- TC: O(n) — each node is visited exactly once, O(1) work per node
- SC: O(h) — recursion stack depth equals tree height h
  (O(log n) balanced, O(n) skewed), plus O(n) for the required output

### Pros
- Shortest, clearest, mirrors the definition; easy to adapt for
  preorder / inorder (move the append line).

### Cons
- Recursion depth = height -> stack-overflow risk in Python on deep trees.
- Interviewers almost always follow up with "now do it iteratively".
- (Note: avoid the `post(L) + post(R) + [val]` concatenation form — it
  recopies subtrees at every level, O(n*h) / O(n^2) on skewed trees.)

### Bottleneck
Relying on the implicit call stack. Postorder is the trickiest order to
simulate with an explicit stack, because you can't visit a node when you
first pop it — its children must be done first. Two classic tricks:
  (a) reverse of "Root -> Right -> Left"  -> approach #2
  (b) peek the stack and track the last visited node -> approach #3
"""


class SolutionRecursive:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        def post(node, res):
            if node is None:
                return

            post(node.left, res)
            post(node.right, res)
            res.append(node.val)

        res = []
        post(root, res)
        return res


# ================================================================================
# MY APPROACH #2 — Reverse of modified preorder (two-stack / stack + reverse)
# ================================================================================
"""
### Idea
Postorder is Left -> Right -> Root. Reverse it and you get
Root -> Right -> Left, which is just PREORDER with the children swapped.
So:
  1. Do a preorder-style walk but visit Root -> RIGHT -> LEFT. With a stack
     this means: pop node, record it, push LEFT first then RIGHT (so RIGHT
     is popped first).
  2. Reverse the recorded sequence to get Left -> Right -> Root.

Two equivalent ways to do the "reverse":
  - Variant A (two stacks): push each popped node onto `stack2`; popping
    `stack2` at the end yields nodes in reversed order.
  - Variant B (list + reverse): append values to `res` and return `res[::-1]`.

### Why does it work?
Reversing the sequence (Root, Right, Left) yields (Left, Right, Root) —
exactly the postorder definition, applied recursively at every node.

### Complexity
- TC: O(n) — each node pushed/popped once, plus one O(n) reversal
- SC: O(n) — Variant A: stack2 holds every node; Variant B: `res` holds all
  values plus the working stack (O(h) worst case) and the reversed copy

### Pros
- Very easy to write and remember: it is preorder + one reverse.
- No `lastVisited` bookkeeping, so far fewer chances for off-by-one bugs.

### Cons
- O(n) extra space, even for a balanced tree, because it must hold the whole
  reversed order before it can output anything.
- Cannot be turned into a lazy iterator (the first postorder node isn't
  known until the whole tree has been walked).

### Bottleneck
The O(n) buffer. The one-stack version only keeps a single root-to-node
path (O(h)), and Morris removes even that.
"""


class SolutionTwoStack:
    # Variant A: two stacks
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []

        stack1, stack2 = [root], []

        while stack1:
            node = stack1.pop()
            stack2.append(node)

            if node.left:
                stack1.append(node.left)
            if node.right:
                stack1.append(node.right)

        res = []
        while stack2:
            res.append(stack2.pop().val)

        return res


class SolutionReversePreorder:
    # Variant B: one stack + reverse the result list
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []

        stack = [root]
        res = []

        while stack:
            node = stack.pop()
            res.append(node.val)

            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)

        return res[::-1]


# ================================================================================
# MY APPROACH #3 — One-Stack Iterative with `lastVisited` (optimal iterative)
# ================================================================================
"""
### Idea
Walk like iterative inorder, but when we get back to a node we PEEK at it
instead of popping blindly:
  1. Go as far LEFT as possible, pushing every node.
  2. Peek the stack top `node`.
       - If it has a right child that we have NOT just finished
         (`lastVisited != node.right`), move into the right subtree.
       - Otherwise both subtrees are done -> pop, record its value, and set
         lastVisited = that node.
`lastVisited` is how we tell "I'm returning from the right subtree" apart
from "I'm arriving at this node for the first time from its left side".

### Why does it work?
A node is peeked up to twice: once after finishing its left subtree
(then we dive into the right subtree if any) and once after finishing its
right subtree (then we record it). Only `lastVisited` distinguishes the two
cases. Recording happens only after both children are done -> postorder.

### Complexity
- TC: O(n) — each node is pushed once, popped once, and peeked at most twice
- SC: O(h) — the stack holds a single root-to-node path (O(n) if skewed),
  plus O(n) for the output

### Pros
- Only O(h) extra space (vs O(n) for the two-stack trick) and no reversal.
- Doesn't modify the tree.
- Can be turned into a lazy iterator.

### Cons
- The trickiest iterative traversal to write: easy to forget `lastVisited`,
  causing an infinite loop or re-processing the right subtree.
- Compares nodes with `!=` — works since nodes are distinct objects, but
  prefer `is not` to compare identity.

### What can be improved?
- O(1) extra space is possible with Morris traversal (approach #5), at the
  cost of temporarily modifying the tree.
"""


class SolutionOneStack:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        stack = []
        result = []
        lastVisited = None
        curr = root

        while curr or stack:
            if curr:
                stack.append(curr)
                curr = curr.left
            else:
                node = stack[-1]

                if node.right and lastVisited != node.right:
                    curr = node.right
                else:
                    result.append(node.val)
                    lastVisited = stack.pop()

        return result


# ================================================================================
# MY APPROACH #4 — Detach children & re-push (destructive stack trick)
# ================================================================================
"""
### Idea
Use a stack and treat each node in two phases:
  - If the popped node is a LEAF -> record its value.
  - Otherwise: detach its children (set node.left = node.right = None) so
    it becomes a leaf, push the node back, then push RIGHT, then LEFT.
    LEFT is popped first and fully processed, then RIGHT, and finally the
    node itself — which is now a leaf, so it gets recorded.

### Why does it work?
Pushing (node, right, left) makes the pop order left-subtree, right-subtree,
node. Detaching the children turns the node into a leaf, so on its second
pop the "leaf -> record" branch fires exactly once. No `lastVisited` needed.

### Complexity
- TC: O(n) — each node is pushed at most twice and popped at most twice
- SC: O(h) — stack holds a node plus its pending right sibling per level
  (about 2h entries in the worst case), plus O(n) for the output

### Pros
- Simple logic, no `lastVisited` tracking; O(h) space.

### Cons
- DESTRUCTIVE: the tree is permanently destroyed (every internal node ends
  up with left = right = None). The caller loses the tree — a surprising
  side effect and a red flag in an interview unless you ask first.
- If you wanted to keep the tree you'd have to restore the pointers (extra
  bookkeeping that defeats the simplicity).

### What can be improved?
Use approach #3 (non-destructive, same O(h) space), or Morris (#5) if
temporary modification is OK AND it is restored.
(Also: `curr = root` in the original code was unused and can be deleted.)
"""


class SolutionDetach:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        res, stack = [], [root]
        while stack:
            node = stack.pop()
            if not node:
                continue
            if not node.left and not node.right:
                res.append(node.val)
            else:
                left = node.left
                right = node.right
                node.left = None
                node.right = None
                stack.append(node)
                if right:
                    stack.append(right)
                if left:
                    stack.append(left)
        return res


# ================================================================================
# MY APPROACH #5 — Morris Traversal (O(1) extra space, bonus / follow-up)
# ================================================================================
"""
### Idea
Morris postorder = Morris PREORDER on the MIRRORED tree, then reverse.
  - Mirrored preorder visits Root -> Right -> Left, whose reverse is
    Left -> Right -> Root (postorder).
  - So we run the Morris trick with the roles of left/right swapped:
      * If curr has no RIGHT child: record curr, go LEFT.
      * Else find predecessor = the leftmost node of curr.right's subtree:
          - If predecessor.left is None: record curr (we visit the root on
            the FIRST arrival), thread predecessor.left = curr, go RIGHT.
          - Else (thread exists, right subtree finished): remove the thread
            and go LEFT.
  - Finally return the recorded list reversed.

### Why does it work?
The thread (pred.left -> curr) lets us climb back to `curr` after exploring
its right subtree, without a stack. Because we record the root before
descending (preorder-style) and then reverse the full sequence, we obtain
Left, Right, Root.

### Complexity
- TC: O(n) — each edge on a right-subtree's leftmost spine is walked at most
  twice (once creating the thread, once removing it); one O(n) reversal
- SC: O(1) extra (excluding the O(n) output list)

### Pros
- True O(1) auxiliary space — no stack, no recursion.

### Cons
- Temporarily modifies the tree (restored at the end), so it's unsafe if the
  tree is shared with concurrent readers.
- Hard to derive and explain; the "mirror + reverse" idea is non-obvious.
- Still needs the O(n) output list to be reversed.

### What can be improved?
Nothing asymptotically — it's the space-optimal solution. In practice the
one-stack version is preferred unless O(1) space is explicitly required.
"""


class SolutionMorris:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        res = []
        curr = root

        while curr:
            if not curr.right:
                res.append(curr.val)
                curr = curr.left
            else:
                predecessor = curr.right
                while predecessor.left and predecessor.left != curr:
                    predecessor = predecessor.left

                if not predecessor.left:
                    res.append(curr.val)
                    predecessor.left = curr  # create thread
                    curr = curr.right
                else:
                    predecessor.left = None  # remove thread
                    curr = curr.left

        return res[::-1]


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
BINARY TREE POSTORDER TRAVERSAL
│
├── Definition
│   └── Left -> Right -> Root (children BEFORE the parent)
│
├── Recursive
│   └── post(left); post(right); append(val)
│       └── O(n) time, O(h) recursion stack
│
├── Bottleneck
│   └── Can't record a node the first time it's popped from an explicit
│       stack — both children must be finished first. Recursion depth is
│       also a risk on skewed trees.
│
├── Trick A — Reverse of modified preorder
│   ├── preorder with children swapped: Root -> Right -> Left
│   └── reverse it -> Left -> Right -> Root
│       └── O(n) time, O(n) space (two-stack or list + reverse)
│
├── Trick B — One stack + lastVisited
│   ├── go left pushing nodes
│   ├── peek: right child unvisited? go right
│   └── else pop + record, lastVisited = node
│       └── O(n) time, O(h) space, tree untouched
│
├── Trick C — Detach children & re-push (destructive)
│   └── turn node into a leaf, push node, right, left; leaf -> record
│       └── O(n) time, O(h) space — but destroys the tree
│
└── Morris Traversal
    ├── mirrored Morris preorder (Root -> Right -> Left) with threads
    └── reverse the result
        └── O(n) time, O(1) extra space (tree temporarily modified)
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Postorder = Left, Right, Root. Children before parent. Typical uses:
  deleting a tree, evaluating postfix/expression trees, bottom-up DP on
  trees (height, diameter, subtree sums)."
- "Reverse(Postorder) = Root, Right, Left = preorder with children swapped.
  So: iterative preorder (push left then right) + reverse the result."
- "Order of pushes matters: push LEFT first, then RIGHT, so RIGHT is popped
  first (Root -> Right -> Left). Pushing right first gives Root -> Left ->
  Right, whose reverse is Right -> Left -> Root — WRONG."
- "One-stack version: PEEK, don't pop immediately. `lastVisited` tells you
  whether you're returning from the right subtree (record the node) or
  arriving from the left subtree (go right first)."
- "Postorder is the hardest of the three orders to do iteratively because
  a node is touched up to THREE times: first arrival, after left, after right."
- "Two-stack / reverse = O(n) space; one-stack = O(h) space; Morris = O(1)."
- "Never leave the tree modified: the detach trick destroys it; Morris must
  remove every thread it creates."
- "Same family: LC 94 (Inorder), LC 144 (Preorder), LC 173 (BST Iterator),
  LC 590 (N-ary Postorder), LC 124 / 543 (bottom-up tree DP)."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                     | Core Idea                                            | TC     | SC (extra) | Pros                                   | Cons                                              | When to Use                          |
|------------------------------|------------------------------------------------------|--------|------------|----------------------------------------|---------------------------------------------------|--------------------------------------|
| Recursive (shared list)      | post(L); post(R); append(val)                        | O(n)   | O(h)       | Simplest; mirrors the definition       | Recursion limit on deep/skewed trees              | Default first answer                 |
| Reverse preorder (2-stack/rev)| Root->Right->Left, then reverse                      | O(n)   | O(n)       | Easy; no lastVisited                   | O(n) buffer; can't be lazy                        | Quick iterative answer               |
| One-stack + lastVisited      | Peek stack; go right unless it was just visited      | O(n)   | O(h)       | Space-efficient; non-destructive       | Trickiest logic; easy to get wrong                | "Do it iteratively, best space"      |
| Detach & re-push             | Make node a leaf, push node, right, left             | O(n)   | O(h)       | Simple logic                           | DESTROYS the tree                                 | Only if tree is disposable (avoid)   |
| Morris (mirrored + reverse)  | Thread predecessor.left -> curr, then reverse        | O(n)   | O(1)       | Constant extra space                   | Temporarily modifies tree; hard to explain        | O(1)-space follow-up                 |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Tree DFS traversal (postorder) — the basis of bottom-up tree DP.
- Go-to answer: "Postorder is left, right, root. Recursively it's O(n) time
  and O(h) space. Iteratively, the easiest approach is to do a preorder-style
  walk in Root -> Right -> Left order with a stack and reverse the result:
  O(n) time and space. To keep space at O(h) I use a single stack, peek at
  the top, and track the last visited node so I only record a node after its
  right subtree is done. If O(1) space is needed, Morris traversal does the
  mirrored preorder with temporary threads and reverses the result."
- Good to mention: why postorder is harder than inorder/preorder (a node
  is revisited three times) and why the reverse trick works.
- Common follow-ups:
  * "Can you avoid the reversal?" -> one-stack + lastVisited.
  * "Can you do it in O(1) extra space?" -> Morris traversal.
  * "Is it OK to destroy the tree?" -> ask first; otherwise avoid the
    detach trick.
  * "Postorder of an N-ary tree?" -> same reverse trick: preorder with
    children pushed left-to-right, then reverse (LC 590).
  * "Evaluate an expression tree?" -> postorder gives operands before
    operator (postfix).
"""