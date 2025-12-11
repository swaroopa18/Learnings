# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

from typing import Optional

# ============================================================================
# APPROACH 1: FLOYD'S CYCLE DETECTION (TORTOISE & HARE) - RECOMMENDED
# ============================================================================
class Solution1:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        """
        Floyd's Cycle Detection Algorithm using two pointers.
        
        Concept: If there's a cycle, fast pointer will eventually catch up 
        to slow pointer (like runners on a circular track).
        
        TC: O(n) - fast pointer visits each node at most twice
        SC: O(1) - only two pointers used
        """
        slow = fast = head
        
        # Fast moves 2 steps, slow moves 1 step
        while fast and fast.next:
            slow = slow.next          # Move 1 step
            fast = fast.next.next     # Move 2 steps
            
            # If they meet, there's a cycle
            if slow == fast:
                return True
        
        # Fast reached end, no cycle exists
        return False


# ============================================================================
# APPROACH 2: HASH SET (STRAIGHTFORWARD)
# ============================================================================
class Solution2:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        """
        Track visited nodes using a hash set.
        
        TC: O(n) - visit each node once
        SC: O(n) - store all nodes in set
        """
        visited = set()
        curr = head
        
        while curr:
            # If we've seen this node before, there's a cycle
            if curr in visited:
                return True
            
            # Mark node as visited
            visited.add(curr)
            curr = curr.next
        
        # Reached end without revisiting any node
        return False


# ============================================================================
# APPROACH 3: NODE MARKING (MODIFYING INPUT - NOT RECOMMENDED)
# ============================================================================
class Solution3:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        """
        Mark visited nodes by modifying them (destructive approach).
        
        WARNING: Modifies the original list structure!
        
        TC: O(n)
        SC: O(1)
        """
        curr = head
        
        while curr:
            # Check if node was already visited
            if hasattr(curr, 'visited'):
                return True
            
            # Mark as visited
            curr.visited = True
            curr = curr.next
        
        return False


# ============================================================================
# APPROACH 4: OPTIMIZED TWO-POINTER (EARLY EXIT)
# ============================================================================
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        """
        Enhanced Floyd's algorithm with early exit optimization.
        
        TC: O(n)
        SC: O(1)
        """
        # Handle empty list or single node
        if not head or not head.next:
            return False
        
        # Start slow at head, fast one step ahead
        slow = head
        fast = head.next
        
        # Loop until they meet or fast reaches end
        while slow != fast:
            # If fast reaches end, no cycle
            if not fast or not fast.next:
                return False
            
            slow = slow.next
            fast = fast.next.next
        
        # They met, cycle exists
        return True


# ============================================================================
# COMPARISON & ANALYSIS
# ============================================================================
"""
╔════════════════╦═══════╦═══════╦════════════════════════════════════╗
║   Approach     ║  TC   ║  SC   ║           Notes                    ║
╠════════════════╬═══════╬═══════╬════════════════════════════════════╣
║ Two Pointers   ║ O(n)  ║ O(1)  ║ ✓ Optimal, most commonly used     ║
║ (Floyd's)      ║       ║       ║ ✓ No extra space                   ║
║                ║       ║       ║ ✓ Non-destructive                  ║
╠════════════════╬═══════╬═══════╬════════════════════════════════════╣
║ Hash Set       ║ O(n)  ║ O(n)  ║ ✓ Intuitive and simple             ║
║                ║       ║       ║ ✗ Uses extra space                 ║
║                ║       ║       ║ ✓ Easy to understand               ║
╠════════════════╬═══════╬═══════╬════════════════════════════════════╣
║ Node Marking   ║ O(n)  ║ O(1)  ║ ✗ Modifies input (destructive)    ║
║                ║       ║       ║ ✗ Not acceptable in interviews     ║
║                ║       ║       ║ ✗ Breaks original data structure   ║
╚════════════════╩═══════╩═══════╩════════════════════════════════════╝

WHY FLOYD'S ALGORITHM WORKS:
-----------------------------
• In a cycle, fast pointer gains 1 position per iteration on slow pointer
• They MUST eventually meet (like running laps on a track)
• If no cycle, fast pointer reaches end (None)

VISUAL EXAMPLE:
---------------
List with cycle: 1 → 2 → 3 → 4 → 5
                          ↑       ↓
                          8 ← 7 ← 6

Step 0: slow=1, fast=1
Step 1: slow=2, fast=3
Step 2: slow=3, fast=5
Step 3: slow=4, fast=7
Step 4: slow=5, fast=4
Step 5: slow=6, fast=6  ← MEET! Cycle detected

RECOMMENDATION:
---------------
Use Solution1 (Floyd's Algorithm) - it's the gold standard for this problem.
Perfect balance of efficiency, elegance, and space optimization.
"""