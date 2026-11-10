"""
================================================================================
 PROBLEM: Next Greater Node In Linked List (LeetCode 1019)
================================================================================
Given: the head of a singly linked list with `n` nodes.
Task: for each node, find the value of the FIRST node that is strictly
greater than it and appears AFTER it in the list. Return an array `answer`
where answer[i] is that value for the (i+1)-th node (1-indexed in the
statement), or 0 if no such node exists.

Example: head = [2, 1, 5] -> [5, 5, 0]

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- "Greater" means strictly greater? (Yes — equal values do NOT count, so
  the stack pop condition is `<`, not `<=`)
- Do I return the VALUE of the next greater node or its index/distance?
  (The value — this differs from "Daily Temperatures", which returns the
  distance)
- What if no greater node exists? (Return 0 for that position)
- Is the list non-empty? How large can n be? (n up to ~10^4 in LC, so
  O(n^2) passes but is not ideal; O(n) is the target)
"""

# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

# ================================================================================
# MY APPROACH #1 — Brute Force (for each node, scan the rest of the list)
# ================================================================================
"""
### Idea
For every node, walk forward through the remaining nodes until you find one
with a strictly larger value. Record it, or 0 if you reach the end.

### Complexity
- TC: O(n^2) — each node may scan all the nodes after it (worst case: a
  non-increasing list, where nothing is ever greater)
- SC: O(1) extra — only the output array

### Pros
- Directly mirrors the problem statement; trivial to get right.
- No extra data structure.

### Cons
- Quadratic in the worst case; re-scans the same suffix over and over.

### Bottleneck
Each node independently re-searches the part of the list that earlier nodes
already looked at. When we meet a new value `v`, it is the answer for EVERY
earlier node that was still "waiting" for something bigger and is smaller
than `v`. Ask: "can I keep the list of still-waiting nodes and resolve many
of them at once?" -> Yes: a monotonic stack.
"""


def next_larger_nodes_brute(head):
    answer = []
    curr = head
    while curr:
        nxt = curr.next
        while nxt and nxt.val <= curr.val:
            nxt = nxt.next
        answer.append(nxt.val if nxt else 0)
        curr = curr.next
    return answer


# ================================================================================
# MY APPROACH #2 — Monotonic Stack + HashMap (index -> next greater value)
# ================================================================================
"""
### Idea
Walk the list once with a running index `idx`. Keep a stack of
(index, value) pairs for nodes still waiting for a greater value. For each
new node `head.val`:
  1. While the stack top's value is strictly smaller than head.val, pop it
     and record hmap[popped_index] = head.val (this node IS its next greater).
  2. Push (idx, head.val).
After the walk, build the answer by reading hmap.get(j, 0) for each index;
nodes still on the stack never found a greater value -> 0.

### Why does it work?
The stack always stays in non-increasing order of value from bottom to top
(anything smaller than the incoming value is popped before pushing). So the
moment a bigger value arrives, it resolves ALL waiting smaller nodes in one
go, and each of those nodes is resolved by the FIRST greater value after it
(because it is popped at the first opportunity). Every node is pushed once
and popped at most once.

### Complexity
- TC: O(n) — each node is pushed once and popped at most once; the final
  answer-building loop is O(n)
- SC: O(n) — stack (worst case: non-increasing list) + hashmap + answer array

### Pros
- Linear time, standard "next greater element" template.
- Easy to explain: the hashmap decouples "discovering" answers from
  "building" the output array.

### Cons
- The hashmap and the second pass are unnecessary overhead: we don't know
  the list length up front, but we CAN grow the answer array as we go.

### Bottleneck
The extra hashmap + second pass exist only because we don't know `n` until
the walk is done. Ask: "can I write the result straight into the answer
array?" -> Yes: append a placeholder 0 for every node as we visit it, then
overwrite answer[index] when its next greater value shows up.
"""


class SolutionHashMap:
    def nextLargerNodes(self, head):
        hmap = {}
        stack = []
        idx = 0
        while head:
            while stack and stack[-1][1] < head.val:
                index, _ = stack.pop()
                hmap[index] = head.val
            stack.append((idx, head.val))
            head = head.next
            idx += 1
        answer = []

        for j in range(idx):
            answer.append(hmap.get(j, 0))
        return answer


# ================================================================================
# MY APPROACH #3 — Monotonic Stack + in-place answer array (optimal / cleanest)
# ================================================================================
"""
### Idea
Same monotonic-stack logic, but write results directly into `answer`.
For each node:
  1. Pop all stack entries with value < head.val and set
     answer[index] = head.val.
  2. Push (len(answer), head.val) — `len(answer)` is exactly this node's
     index because we append one slot per node.
  3. Append 0 as the default for this node (stays 0 if never resolved).
No hashmap, no second pass.

### Why does it work?
`answer` doubles as the index counter (`len(answer)` == current node index)
and as the result store. Defaulting each slot to 0 means nodes left on the
stack at the end already have the correct answer (no greater value exists).

### Complexity
- TC: O(n) — single pass; each node pushed and popped at most once
- SC: O(n) — stack (worst case) + answer array (required output anyway).
  Only the stack is true auxiliary space, and no hashmap is needed.

### Pros
- Single pass, no hashmap, fewer variables (no separate idx).
- Output array is built directly; unresolved nodes are 0 automatically.

### Cons
- The "len(answer) as the index" trick is slightly subtle; mention it
  explicitly to the interviewer.
- Still O(n) stack space in the worst case (decreasing list).

### What can be improved?
- Nothing asymptotically — O(n) time is optimal (must read every node) and
  O(n) space is needed for the output; the stack is the only extra.
- Micro-optimization: store only the index on the stack and look the value
  up from a values list (instead of (index, value) tuples).
- Alternative: reverse the list and sweep with a stack of "candidates"
  (monotonic from the right) — same complexity, but needs to mutate/reverse
  the list or copy values.
"""


class SolutionInPlace:
    def nextLargerNodes(self, head):
        answer = []
        stack = []
        while head:
            while stack and stack[-1][1] < head.val:
                index, _ = stack.pop()
                answer[index] = head.val
            stack.append((len(answer), head.val))
            answer.append(0)
            head = head.next
        return answer


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
NEXT GREATER NODE IN LINKED LIST
│
├── Brute Force
│   └── For each node, scan forward until a strictly greater value
│       └── O(n^2) time, O(1) extra space
│
├── Bottleneck
│   └── Repeated re-scanning of the same suffix; one big value could resolve
│       MANY earlier smaller nodes at once
│
├── Key Observation
│   └── "Next greater element" -> monotonic (non-increasing) stack of nodes
│       still waiting for a greater value
│
├── Optimization A — Monotonic Stack + HashMap
│   ├── pop while stack top < current -> hmap[index] = current
│   ├── push (idx, val)
│   └── second pass: answer[j] = hmap.get(j, 0)
│
└── Optimization B — Monotonic Stack + in-place answer
    ├── answer.append(0) per node (default = no greater)
    ├── pop while stack top < current -> answer[index] = current
    └── push (len(answer), val)   ← index trick, single pass, no hashmap
        └── O(n) time, O(n) space
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Next greater element to the right -> monotonic stack, always. Each element
  is pushed once and popped once => O(n) even though there's a nested while."
- "Store INDICES (or (index, value) pairs) on the stack so popped elements
  know WHERE to write their answer."
- "Strictly greater => pop condition is `stack[-1][1] < head.val`. Using
  `<=` would wrongly resolve equal values."
- "Elements left on the stack at the end have NO next greater -> answer 0.
  Default-initialize to 0 so no cleanup is needed."
- "A linked list has no random access and no known length — appending a 0
  per node while walking solves both problems and gives index = len(answer)."
- "Same template as: LC 496 / 503 (Next Greater Element I / II),
  LC 739 (Daily Temperatures — store distance instead of value),
  LC 84 (Largest Rectangle in Histogram)."
- "For 'next smaller', flip the comparison; for 'previous greater', read the
  stack top BEFORE pushing."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                     | Core Idea                                          | TC       | SC (extra)       | Pros                                   | Cons                                           | When to Use                         |
|------------------------------|----------------------------------------------------|----------|------------------|----------------------------------------|------------------------------------------------|-------------------------------------|
| Brute Force                  | Scan forward from every node                       | O(n^2)   | O(1)             | Simplest; no extra structures          | Quadratic; re-scans the same suffix            | Tiny n / first-pass baseline        |
| Monotonic Stack + HashMap    | Stack resolves waiting nodes; map index -> value   | O(n)     | O(n)             | Linear; clear separation of concerns   | Extra hashmap + second pass                    | Explaining the idea step by step    |
| Monotonic Stack + in-place   | Same stack; write straight into `answer`           | O(n)     | O(n)             | Single pass, no hashmap, default 0     | `len(answer)` index trick is a bit subtle      | Default optimal choice (your code)  |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Monotonic Stack ("next greater element") on a linked list.
  Same family as LC 496/503 (Next Greater Element), LC 739 (Daily
  Temperatures), LC 901 (Online Stock Span).
- Go-to answer: "I walk the list once keeping a stack of (index, value) for
  nodes still waiting for a greater value. When a new value arrives, I pop
  every smaller entry and set its answer to the new value, then push the new
  node. I append 0 for each node as a default, so anything left on the
  stack correctly stays 0. O(n) time, O(n) space."
- Good to mention the brute force first (scan forward per node, O(n^2)) and
  then the key insight: "one larger value resolves many earlier smaller
  nodes at once, so keep the unresolved ones on a monotonic stack."
- Common follow-ups:
  * "What if 'greater or equal' counts?" -> change pop condition to `<=`.
  * "Return the distance/number of nodes instead of the value?" -> store
    the index and write `current_idx - popped_idx` (Daily Temperatures).
  * "Previous greater node?" -> read the stack top before pushing; no pops
    needed to record, just maintain the stack.
  * "Circular linked list?" -> iterate twice around (like LC 503), using
    modulo indexing over a copied value array.
"""