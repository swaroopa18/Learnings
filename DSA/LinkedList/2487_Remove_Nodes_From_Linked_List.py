"""
================================================================================
 PROBLEM: Remove Nodes From Linked List (LeetCode 2487)
================================================================================
Given: the head of a singly linked list.
Task: remove every node that has a node with a STRICTLY GREATER value
somewhere to its right. Return the head of the modified list.

Example: head = [5, 2, 13, 3, 8] -> [13, 8]
  (5 removed: 13 is to its right; 2 removed: 13; 3 removed: 8;
   13 and 8 survive: nothing greater to their right)

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- "Greater" means strictly greater? (Yes — equal values to the right do NOT
  cause removal, so [5, 5] stays [5, 5]; the pop condition is `<`, not `<=`)
- Is the list non-empty? (Yes — at least 1 node, so the last node always
  survives since nothing is to its right)
- Can I modify the list in place / reuse nodes? (Yes — the solutions below
  re-link existing nodes instead of allocating new ones, except brute force)
- Does the relative order of survivors matter? (Yes, preserved as in the
  original list)
"""

# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

# ================================================================================
# MY APPROACH #1 — Brute Force (for each node, scan the rest for a greater value)
# ================================================================================
"""
### Idea
For every node, walk forward through all nodes to its right. If any node is
strictly greater, skip the current node; otherwise keep it by appending it
to the result list.

### Complexity
- TC: O(n^2) — each node may scan every node after it (worst case: a
  non-increasing list, where every node survives but each still scans the
  whole suffix looking for a greater value)
- SC: O(1) extra — if re-linking nodes; O(n) if copying values into new nodes
  as written below

### Pros
- Directly mirrors the problem statement; trivial to verify.

### Cons
- Quadratic; re-scans the same suffix for every node.

### Bottleneck
For each node we only need to know ONE fact: "what is the maximum value to
my right?" Recomputing that by scanning is wasteful. Two ways to get it for
free:
  (a) sweep from the RIGHT keeping a running max (needs reverse access ->
      reverse the list), or
  (b) sweep from the LEFT with a monotonic stack that discards a node as
      soon as a bigger one shows up to its right.
"""


def remove_nodes_brute(head):
    dummy = ListNode(0)
    tail = dummy
    curr = head
    while curr:
        nxt = curr.next
        has_greater = False
        while nxt:
            if nxt.val > curr.val:
                has_greater = True
                break
            nxt = nxt.next
        if not has_greater:
            tail.next = ListNode(curr.val)
            tail = tail.next
        curr = curr.next
    return dummy.next


# ================================================================================
# MY APPROACH #2 — Monotonic (non-increasing) Stack  (your solution)
# ================================================================================
"""
### Idea
Scan left to right, keeping a stack of nodes that are still "alive". For
each incoming node:
  1. While the stack top's value is strictly smaller than head.val, pop it —
     the incoming node is a greater value to its right, so it must be removed.
  2. Push the incoming node.
When the scan ends, the stack holds exactly the survivors, in original
order, with values in non-increasing order. Chain them together with a dummy
head to build the result list.

### Why does it work?
A node should be deleted iff some later node is strictly bigger. The moment
that later node arrives, every smaller node still on the stack is
permanently doomed, and the `while` pops all of them. Nodes that are never
popped never saw a bigger value to their right. Each node is pushed once and
popped at most once.

Note: the last node of the list is always on the stack (nothing comes after
it), and its `.next` is already None, so the rebuilt list needs no explicit
`curr.next = None` termination.

### Complexity
- TC: O(n) — each node is pushed once and popped at most once; the final
  rebuild loop is O(n)
- SC: O(n) — stack (worst case: non-increasing list keeps everything)

### Pros
- Linear time, single scan + one rebuild.
- Same monotonic-stack template as "Next Greater Node" — easy to recognize
  and explain.
- Doesn't reverse or otherwise disturb the original list while scanning.

### Cons
- O(n) extra space for the stack (survivors can be the entire list).
- Needs a second pass to re-link survivors (the nodes' old `.next` pointers
  are overwritten during rebuild, which is fine here).

### Bottleneck
The stack costs O(n) space. To drop it, we need the "max to my right" without
storing nodes -> process from the right using a running max, which means
reversing the list (in place, O(1) extra space).
"""


class SolutionStack:
    def removeNodes(self, head):
        stack = []
        while head:
            while stack and stack[-1].val < head.val:
                stack.pop()
            stack.append(head)
            head = head.next

        result = ListNode(0)
        curr = result
        for node in stack:
            curr.next = node
            curr = curr.next
        return result.next


# ================================================================================
# MY APPROACH #3 — Reverse, filter with running max, reverse back (O(1) space)
# ================================================================================
"""
### Idea
1. Reverse the list. Now "nodes to the right" in the original are "nodes
   already seen" in the reversed list.
2. Walk the reversed list keeping `max_val` = the max of everything kept so
   far (the head of the reversed list, i.e. the original last node, is
   always kept). For each next node: if its value < max_val, unlink it;
   otherwise keep it and update max_val.
3. Reverse the list back to restore the original order.

### Why does it work?
In the reversed list, everything before a node is exactly what used to be to
its right. A node survives iff its value is >= the max of all those earlier
nodes — i.e. iff it is a running (weak) maximum of the reversed sequence.
Equal values survive because the condition to delete is strictly smaller.

### Complexity
- TC: O(n) — two reversals + one filtering pass
- SC: O(1) extra — all in-place pointer manipulation

### Pros
- Constant extra space (no stack, no recursion).
- Re-links existing nodes; allocates nothing.

### Cons
- Mutates the list structure during processing (fine here since the problem
  asks for the modified list anyway).
- Three passes and a bit more pointer juggling -> easier to introduce bugs
  (off-by-one on `curr.next` deletion).

### What can be improved?
- Nothing asymptotically: O(n) time is optimal (must see every node) and
  O(1) extra space is optimal.
- A recursive solution is also possible (recurse to the end, then on the way
  back keep a node only if it's >= the max so far), but it uses O(n) call
  stack — same space class as the explicit stack and risks recursion limits
  in Python for long lists.
"""


class SolutionReverse:
    def reverse(self, head):
        rev = None
        while head:
            temp = head.next
            head.next = rev
            rev = head
            head = temp
        return rev

    def removeNodes(self, head):
        head = self.reverse(head)
        curr = head
        max_val = head.val
        while curr.next:
            if curr.next.val < max_val:
                curr.next = curr.next.next  # unlink the smaller node
            else:
                curr = curr.next
                max_val = curr.val
        return self.reverse(head)


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
REMOVE NODES FROM LINKED LIST
│
├── Brute Force
│   └── For each node, scan the suffix for a strictly greater value
│       └── O(n^2) time
│
├── Bottleneck
│   └── Each node only needs "max value to my right"; re-scanning for it is
│       wasteful. A larger value to the right dooms ALL smaller nodes before it.
│
├── Key Observation
│   └── Survivors are exactly the nodes that are >= everything after them
│       -> they form a non-increasing sequence (a monotonic stack's contents)
│
├── Optimization A — Monotonic Stack (left to right)
│   ├── pop while stack top < incoming  (doomed nodes)
│   ├── push incoming
│   └── re-link stack contents with a dummy head
│       └── O(n) time, O(n) space
│
└── Optimization B — Reverse + running max (O(1) space)
    ├── reverse list
    ├── keep node iff val >= max_val so far, else unlink
    └── reverse back
        └── O(n) time, O(1) extra space
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Remove nodes with a greater value to the right == keep only the nodes that
  are >= every node after them. Survivors form a NON-INCREASING sequence."
- "Monotonic stack: pop while stack[-1].val < incoming.val. Each node is
  pushed and popped at most once, so the nested while is still O(n)."
- "Strictly greater => `<` in the pop condition. Equal values must survive
  (e.g. [5, 5] -> [5, 5])."
- "The last node always survives (nothing to its right), so its .next is
  already None — no explicit tail termination needed when re-linking."
- "To get O(1) space, sweep from the right: reverse the list, track a
  running max, delete smaller nodes, reverse back. 'Need to look at the
  right side of a singly linked list' -> reverse it."
- "Use a dummy head when rebuilding so you don't special-case the first node."
- "Same family as: LC 1019 (Next Greater Node in Linked List), LC 496/503
  (Next Greater Element), LC 739 (Daily Temperatures), LC 316 / 402 (Remove
  Duplicate Letters / Remove K Digits — stack with removals)."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                  | Core Idea                                             | TC     | SC (extra) | Pros                                   | Cons                                              | When to Use                          |
|---------------------------|-------------------------------------------------------|--------|------------|----------------------------------------|---------------------------------------------------|--------------------------------------|
| Brute Force               | Scan suffix of every node for a strictly greater val  | O(n^2) | O(1)*      | Simplest; mirrors the statement        | Quadratic; re-scans same suffix                   | Tiny n / first-pass baseline         |
| Monotonic Stack           | Pop smaller nodes when a bigger one arrives; relink   | O(n)   | O(n)       | Linear; standard template; clear logic | O(n) stack; second pass to relink                 | Default answer (your code)           |
| Reverse + running max     | Reverse, keep nodes >= max so far, reverse back       | O(n)   | O(1)       | Constant extra space; in place         | 3 passes; fiddly pointer deletion                 | Interviewer asks for O(1) space      |

* O(1) if re-linking existing nodes; the code above copies values (O(n)).

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Monotonic Stack on a linked list ("discard anything smaller once
  a bigger element arrives"). Cousin of LC 1019 (Next Greater Node) and
  LC 402 (Remove K Digits).
- Go-to answer: "A node must go iff some node to its right is strictly
  bigger. I scan left to right with a stack: for each incoming node I pop
  every smaller node (they now have a bigger node to their right), then push
  the incoming one. At the end the stack holds exactly the survivors in
  order, so I chain them together. O(n) time, O(n) space. If space matters,
  I can reverse the list, keep nodes >= a running max, and reverse back for
  O(1) extra space."
- Good to mention the brute force first (O(n^2) suffix scan) and then the
  key insight: "a bigger value to the right dooms all smaller nodes before it
  — so smaller nodes can be discarded eagerly via a stack."
- Common follow-ups:
  * "Remove nodes with a greater-OR-EQUAL value to the right?" -> pop
    condition becomes `<=`.
  * "Do it in O(1) extra space?" -> reverse + running max + reverse back.
  * "Recursive solution?" -> recurse to the tail; on return, compare each
    node with the (already filtered) next; keep only if val >= next's val;
    O(n) call stack.
  * "Remove nodes with a SMALLER value to the right?" -> flip the comparison
    (monotonic increasing stack).
"""