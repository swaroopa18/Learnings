# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

from typing import Optional

# ============================================================================
# APPROACH 1: HASH SET (STRAIGHTFORWARD)
# ============================================================================
class Solution1:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Use hash set to track visited nodes and find cycle start.
        
        TC: O(n) - visit each node once
        SC: O(n) - store nodes in set
        """
        visited = set()
        curr = head
        
        while curr:
            # First node we've seen before is the cycle start
            if curr in visited:
                return curr
            
            visited.add(curr)
            curr = curr.next
        
        # No cycle found
        return None


# ============================================================================
# APPROACH 2: FLOYD'S ALGORITHM (OPTIMAL) - RECOMMENDED
# ============================================================================
class Solution2:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Floyd's Cycle Detection with mathematical property to find cycle start.
        
        Key Insight: After detecting cycle, distance from head to cycle start
        equals distance from meeting point to cycle start.
        
        TC: O(n) - two passes through the list
        SC: O(1) - only two pointers
        """
        slow = fast = head
        
        # Phase 1: Detect if cycle exists using Floyd's algorithm
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            
            # Cycle detected
            if slow == fast:
                break
        else:
            # No cycle (fast reached end)
            return None
        
        # Phase 2: Find cycle start
        # Reset slow to head, keep fast at meeting point
        slow = head
        
        # Move both one step at a time until they meet
        # They will meet at the cycle start!
        while slow != fast:
            slow = slow.next
            fast = fast.next
        
        return slow

# ============================================================================
# MATHEMATICAL PROOF: WHY FLOYD'S ALGORITHM WORKS
# ============================================================================
"""
VISUAL REPRESENTATION:
----------------------
       a steps        c steps in cycle
    ┌─────────┐    ┌──────────────┐
    │         │    │              │
Head ────────→ X → → → → M        │
               ↑   ↑     ↓        │
               │   │     ↓        │
               │   └─────┘        │
               └──────────────────┘
                   b steps

X = Cycle start
M = Meeting point of slow and fast
a = Distance from head to cycle start
b = Distance from cycle start to meeting point
c = Cycle length

PROOF:
------
When slow and fast meet:
• Slow traveled: a + b
• Fast traveled: a + b + k*c (where k = number of complete cycles)

Since fast moves twice as fast as slow:
  2(a + b) = a + b + k*c
  2a + 2b = a + b + k*c
  a + b = k*c
  a = k*c - b

This means: a = (k-1)*c + (c - b)

Notice: (c - b) is the distance from meeting point back to cycle start!

Therefore: Distance from head to X = Distance from meeting point to X

This is why moving both pointers one step at a time from these positions
will make them meet exactly at the cycle start!

STEP-BY-STEP EXAMPLE:
---------------------
List: 1 → 2 → 3 → 4 → 5
               ↑       ↓
               8 ← 7 ← 6

a = 2 (head to node 3)
c = 6 (cycle length)

Phase 1 (Detection):
Step 0: slow=1, fast=1
Step 1: slow=2, fast=3
Step 2: slow=3, fast=5
Step 3: slow=4, fast=7
Step 4: slow=5, fast=4
Step 5: slow=6, fast=6  ← Meet at node 6

Phase 2 (Find Start):
slow = 1, fast = 6
Step 1: slow=2, fast=7
Step 2: slow=3, fast=8
Step 3: slow=4, fast=4  ← Wait, let me recalculate...

Actually with this cycle:
Step 1: slow=2, fast=7
Step 2: slow=3, fast=8
Step 3: slow=3, fast=3  ← Meet at node 3 (cycle start)!
"""


# ============================================================================
# COMPARISON TABLE
# ============================================================================
"""
╔════════════════╦═══════╦═══════╦════════════════════════════════════╗
║   Approach     ║  TC   ║  SC   ║           Notes                    ║
╠════════════════╬═══════╬═══════╬════════════════════════════════════╣
║ Hash Set       ║ O(n)  ║ O(n)  ║ ✓ Very intuitive                   ║
║                ║       ║       ║ ✓ Easy to implement                ║
║                ║       ║       ║ ✗ Uses extra space                 ║
║                ║       ║       ║ ✓ Good for interviews if explain   ║
╠════════════════╬═══════╬═══════╬════════════════════════════════════╣
║ Floyd's        ║ O(n)  ║ O(1)  ║ ✓ Optimal space complexity         ║
║ Algorithm      ║       ║       ║ ✓ Elegant mathematical solution    ║
║                ║       ║       ║ ✗ Requires proof explanation       ║
║                ║       ║       ║ ✓ Shows deep understanding         ║
╚════════════════╩═══════╩═══════╩════════════════════════════════════╝

INTERVIEW STRATEGY:
-------------------
1. Start by explaining the hash set approach (shows you can solve it)
2. Mention it uses O(n) space
3. Then present Floyd's algorithm as the optimal O(1) space solution
4. Explain the mathematical reasoning (shows deep understanding)
5. Code the cleaner version (Solution 3)

COMMON MISTAKES:
----------------
✗ Forgetting to check if cycle exists before Phase 2
✗ Not resetting slow pointer to head in Phase 2
✗ Moving both pointers at different speeds in Phase 2
✓ Both pointers move ONE step at a time in Phase 2!

RECOMMENDATION:
---------------
Learn Floyd's algorithm (Solution 2) - it's a classic interview problem
and demonstrates strong problem-solving skills. However, hash set approach
is perfectly acceptable if you explain the space trade-off.
"""