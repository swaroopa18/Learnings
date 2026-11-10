"""
================================================================================
 PROBLEM: Add Two Numbers II (LeetCode 445)
================================================================================
Given: two non-empty singly linked lists `l1` and `l2` representing two
non-negative integers. Digits are stored in MOST-significant-digit-first
order (e.g. 7 -> 2 -> 4 -> 3 represents 7243), each node holds one digit.
Task: add the two numbers and return the sum as a linked list in the same
format (most significant digit first).

Follow-up: can you solve it WITHOUT modifying the input lists (i.e. without
reversing them)?

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Are the lists non-empty? (Yes — at least 1 node each)
- Can there be leading zeros? (No, except the number 0 itself)
- Are lists of different lengths? (Yes — handle by treating missing digits
  as 0)
- Am I allowed to modify / reverse the input lists? (This decides between
  the in-place reversal approach and the stack approach — ASK this!)
- Can I convert the lists to integers? (Usually the lists can be 100 digits
  long, which overflows fixed-width ints in Java/C++; Python has bigints
  but interviewers typically want the digit-by-digit solution)
"""

# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

# ================================================================================
# MY APPROACH #1 — Brute Force (convert to integers, add, rebuild list)
# ================================================================================
"""
### Idea
Walk each list, building the integer digit by digit (num = num*10 + digit).
Add the two integers, then convert the sum back to a linked list.

### Complexity
- TC: O(m + n) digit operations (but big-int arithmetic on m/n-digit numbers
  isn't truly O(1) per step in Python — it's fine in practice)
- SC: O(max(m, n)) — for the output list (plus the big-int itself)

### Pros
- Very short and obviously correct in Python.

### Cons
- Relies on Python's arbitrary-precision ints. In Java/C++ the number can
  have up to ~100 digits and overflows long -> wrong answer.
- Interviewer will say "do it without converting to integers" — it sidesteps
  the actual problem (digit-wise addition with carry).

### Bottleneck
It dodges the real challenge: adding digit by digit with carry. The real
difficulty is that linked lists are MSD-first, but addition must start from
the LSD (least significant digit). Ask: "how do I access digits from the
tail of a singly linked list?" -> reverse the lists, or use a stack.
"""


def add_two_numbers_brute(l1, l2):
    num1 = num2 = 0
    while l1:
        num1 = num1 * 10 + l1.val
        l1 = l1.next
    while l2:
        num2 = num2 * 10 + l2.val
        l2 = l2.next

    total = num1 + num2
    if total == 0:
        return ListNode(0)

    head = None
    while total > 0:
        node = ListNode(total % 10)
        node.next = head
        head = node
        total //= 10
    return head


# ================================================================================
# MY APPROACH #2 — Reverse both lists, add (LC 2 style), reverse the result
# ================================================================================
"""
### Idea
Reverse l1 and l2 so the least significant digit comes first. Now it's
exactly "Add Two Numbers" (LeetCode 2): walk both lists together, add
val1 + val2 + carry, emit (total % 10), carry = total // 10. Append a final
node if carry remains. The result is built LSD-first, so reverse it once
more to get MSD-first order.

### Why does it work?
Addition is carried out from the least significant digit upward. Reversing
the lists turns "last node" into "first node", giving us the LSD-first order
we need, using only pointer manipulation. Missing digits in the shorter list
are treated as 0 (`l1.val if l1 else 0`), so different lengths are handled
uniformly.

### Complexity
- TC: O(m + n) — 3 reversals (l1, l2, result) + one pass of addition, all linear
- SC: O(1) extra — reversal is in place and the add step only allocates the
  output list (which is required anyway)

### Pros
- O(1) auxiliary space (beyond the output).
- Reuses the classic "reverse linked list" + "Add Two Numbers" building blocks.

### Cons
- MUTATES the input lists (l1 and l2 end up reversed). Violates the follow-up
  constraint, and it's a side effect the caller may not expect.
- Slightly more code: 3 reversals + addition.

### Bottleneck
Needing to touch the inputs to reach their tails. If we are NOT allowed to
modify the input, we need another way to read digits in reverse order ->
a stack (LIFO) gives exactly that.
"""


class SolutionReverse:
    def reverse(self, li):
        rev = None
        while li:
            temp = li.next
            li.next = rev
            rev = li
            li = temp
        return rev

    def add(self, l1, l2):
        answer = ListNode(0)
        curr = answer
        carry = 0
        while l1 or l2:
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0

            total = val1 + val2 + carry

            rem = total % 10
            carry = total // 10

            curr.next = ListNode(rem)
            curr = curr.next

            l1 = l1.next if l1 else l1
            l2 = l2.next if l2 else l2
        if carry > 0:
            curr.next = ListNode(carry)
        return answer.next

    def addTwoNumbers(self, l1, l2):
        rev1 = self.reverse(l1)
        rev2 = self.reverse(l2)

        answer = self.add(rev1, rev2)

        return self.reverse(answer)


# ================================================================================
# MY APPROACH #3 — Two Stacks (optimal for the follow-up: no input mutation)
# ================================================================================
"""
### Idea
Push every node of l1 onto stack1 and every node of l2 onto stack2. Popping
from a stack yields digits from the least significant end. Pop from both
(using 0 when one stack is empty), add with carry, and PREPEND each new
digit node to the front of the answer list:

    new_node.next = answer
    answer = new_node

Because we generate digits LSD-first but always insert at the head, the
final list is already in MSD-first order — no final reversal needed. After
the loop, if carry > 0, prepend one last node.

### Why does it work?
A stack reverses access order (LIFO), so the tail digits come out first
without touching the original pointers. Head-insertion into the answer
reverses the produced order back, so we get the correct MSD-first list in a
single pass.

### Complexity
- TC: O(m + n) — one pass to fill stacks, one pass to pop & add
- SC: O(m + n) — two stacks holding every node (the output list is
  required anyway)

### Pros
- Does NOT modify the input lists -> satisfies the follow-up.
- Only ONE pass of building the answer, no final reversal.
- Easy to reason about and explain.

### Cons
- O(m + n) extra space for the stacks vs. O(1) for the reversal approach.
- Minor: storing whole nodes is wasteful — you could push just `node.val`.

### What can be improved?
- Push `l1.val` instead of the node object (same big-O, less memory).
- Space can be cut to O(1) extra with the reverse approach, but that mutates
  the input (you could reverse the inputs back afterwards to restore them —
  still O(1) extra, at the cost of two more passes).
- A recursive solution (pad the shorter list's length with leading zeros,
  recurse to the end, add on the way back) also avoids mutation but uses
  O(max(m, n)) call stack space — same cost class as the stacks.
"""


class SolutionStack:
    def addTwoNumbers(self, l1, l2):
        stack1, stack2 = [], []

        while l1:
            stack1.append(l1)
            l1 = l1.next
        while l2:
            stack2.append(l2)
            l2 = l2.next

        carry = 0
        answer = None
        while stack1 or stack2:
            val1 = stack1.pop().val if stack1 else 0
            val2 = stack2.pop().val if stack2 else 0
            total = val1 + val2 + carry
            carry = total // 10
            rem = total % 10

            new_node = ListNode(rem)
            new_node.next = answer
            answer = new_node

        if carry > 0:
            new_node = ListNode(carry)
            new_node.next = answer
            answer = new_node
        return answer


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
ADD TWO NUMBERS II
│
├── Brute Force
│   └── Lists -> ints, add, ints -> list
│       └── O(m + n), but overflows in Java/C++ and dodges the real problem
│
├── Bottleneck
│   └── Digits are MSD-first, but addition must start at the LSD (tail).
│       A singly linked list can't be walked backwards.
│
├── Key Observation
│   └── "Need to process a sequence in reverse order" -> reverse it,
│       or use a stack (LIFO)
│
├── Optimization A — Reverse lists (O(1) extra space)
│   ├── reverse(l1), reverse(l2)
│   ├── add LSD-first with carry (Add Two Numbers I)
│   └── reverse(result)           ⚠ mutates inputs
│
└── Optimization B — Two Stacks (follow-up friendly)
    ├── push all nodes of l1, l2 onto stacks
    ├── pop both, total = v1 + v2 + carry
    └── prepend new node to answer (head insertion) -> already MSD-first
        └── O(m + n) time, O(m + n) space, inputs untouched
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Linked list is MSD-first but addition goes LSD-first -> need reverse
  access: either reverse the list (O(1) space, mutates) or use a stack
  (O(n) space, no mutation)."
- "Building the answer by HEAD INSERTION reverses the order for free — digits
  produced LSD-first end up MSD-first, so no final reverse is needed."
- "Always handle the leftover carry AFTER the loop (e.g. 5 + 5 = 10 -> new
  leading node 1)."
- "Treat an exhausted list/stack as 0 (`x.val if x else 0`) to handle
  different lengths without special-casing."
- "Loop condition `while l1 or l2` (+ post-loop carry check) is the standard
  template shared with LC 2 (Add Two Numbers), LC 67 (Add Binary), LC 415
  (Add Strings)."
- "Don't convert to int in an interview — it sidesteps the problem and
  overflows in fixed-width languages."
- "The follow-up 'without modifying the input' is the signal to pick stacks
  (or recursion)."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach         | Core Idea                                    | TC       | SC (extra)  | Pros                                   | Cons                                          | When to Use                          |
|------------------|----------------------------------------------|----------|-------------|----------------------------------------|-----------------------------------------------|--------------------------------------|
| Convert to ints  | Build ints, add, rebuild list                | O(m + n) | O(m + n)    | Shortest code in Python                | Overflows in Java/C++; dodges the real problem | Quick sanity check / Python-only     |
| Reverse lists    | Reverse l1, l2, add LSD-first, reverse result | O(m + n) | O(1)        | Constant auxiliary space               | Mutates input; 3 reversals                     | Mutation is allowed, space is tight  |
| Two stacks       | Stack for LIFO access; prepend result nodes  | O(m + n) | O(m + n)    | No mutation; single build pass         | O(n) extra space for stacks                    | Follow-up: don't modify inputs       |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Linked list digit-wise addition with carry; "reverse access" via
  stack or in-place reversal. Same family as LC 2 (Add Two Numbers),
  LC 67 (Add Binary), LC 415 (Add Strings).
- Go-to answer: "Digits are MSD-first but I must add from the LSD. I push
  both lists onto stacks, pop digits together adding the carry, and prepend
  each result digit to the answer list so it's already in the right order.
  O(m + n) time and space, and the inputs stay untouched. If mutation is
  allowed I can instead reverse both lists, add, and reverse back for O(1)
  extra space."
- Good to mention the int-conversion idea first and why it fails (overflow in
  fixed-width languages, avoids the real problem), then identify the
  bottleneck: "can't walk a singly linked list backwards".
- Common follow-ups:
  * "Don't modify the inputs?" -> stacks or recursion with length padding.
  * "Can you do it in O(1) extra space and still not modify inputs?" ->
    reverse in place, add, then reverse the inputs back to restore them.
"""