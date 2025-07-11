# Definition for singly-linked list.
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

"""
ALGORITHM: Three-Pointer Reversal with Boundary Tracking
1. Use a dummy node to handle edge cases (reversing from head)
2. Navigate to the node before the reversal section
3. Reverse the sublist using three pointers
4. Reconnect the reversed section to the original list

TIME COMPLEXITY: O(n) where n is the number of nodes
- We traverse the list at most twice: once to find the start position, once to reverse
- Each node is visited a constant number of times

SPACE COMPLEXITY: O(1) 

APPROACH:
- Use dummy node to simplify edge case handling
- Track three key positions: before reversal, start of reversal, end of reversal
- Perform standard linked list reversal on the sublist
- Carefully reconnect the boundaries
"""

class Solution:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        # Create dummy node to handle edge case where left=1 (reversing from head)
        dummy = ListNode(0)
        dummy.next = head
        
        # STEP 1: Find the node just before the reversal starts
        # 'first' will point to the node before position 'left'
        first = dummy
        for _ in range(left - 1):
            first = first.next
        
        # STEP 2: Set up pointers for reversal
        # 'second' points to the first node to be reversed (position 'left')
        second = first.next
        current = second  # Current node being processed
        third = None      # Previous node in the reversed section
        
        # STEP 3: Reverse the sublist from position 'left' to 'right'
        # Standard three-pointer reversal technique
        for _ in range(right - left + 1):
            tail = current.next
            current.next = third
            third = current
            current = tail
        
        first.next = third
        # 'second' (original first node of reversed section) connects to remaining list
        second.next = current
        
        # Return the head of the modified list
        return dummy.next

# ============================================================================
# RECURSIVE SOLUTION
# ============================================================================

"""
Time: O(n), Space: O(n) due to recursion stack
"""

class SolutionRecursive:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        def reverse_n(head, n):
            """Reverse first n nodes of linked list"""
            if n == 1:
                return head
            
            last = reverse_n(head.next, n - 1)
            successor = head.next.next
            head.next.next = head
            head.next = successor
            return last
        
        if left == 1:
            return reverse_n(head, right)
        
        head.next = self.reverseBetween(head.next, left - 1, right - 1)
        return head

# ============================================================================
# ITERATIVE WITH STACK
# ============================================================================

"""
Time: O(n), Space: O(k) where k = right - left + 1
Uses stack to store nodes, then rebuilds connections
"""

class SolutionStack:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        if not head or left == right:
            return head
            
        dummy = ListNode(0)
        dummy.next = head
        prev = dummy
        
        # Move to position before 'left'
        for _ in range(left - 1):
            prev = prev.next
            
        # Collect nodes to reverse in stack
        stack = []
        curr = prev.next
        for _ in range(right - left + 1):
            stack.append(curr)
            curr = curr.next
            
        # Rebuild connections using stack (LIFO gives reversal)
        while stack:
            node = stack.pop()
            prev.next = node
            prev = node
        prev.next = curr
        
        return dummy.next


# ============================================================================
# ONE-PASS WITH NODE SWAPPING
# ============================================================================

"""
APPROACH 4: ONE-PASS WITH NODE SWAPPING
Time: O(n), Space: O(1)
Alternative iterative approach that swaps nodes instead of reversing pointers
"""

class SolutionSwapping:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        if not head or left == right:
            return head
            
        dummy = ListNode(0)
        dummy.next = head
        prev = dummy
        
        # Move to position before 'left'
        for _ in range(left - 1):
            prev = prev.next
            
        # Current points to the 'left' node
        curr = prev.next
        
        # Perform swaps: move next node to front repeatedly
        for _ in range(right - left):
            next_node = curr.next
            curr.next = next_node.next
            next_node.next = prev.next
            prev.next = next_node
            
        return dummy.next

"""
COMPARISON OF APPROACHES:

1. YOUR ORIGINAL APPROACH (Three-Pointer):
   ✅ Most intuitive and standard
   ✅ O(1) space, O(n) time
   ✅ Easy to understand and debug
   ✅ Handles all edge cases cleanly

2. RECURSIVE APPROACH:
   ❌ O(n) space due to call stack
   ❌ More complex to understand
   ✅ Elegant mathematical thinking
   ⚠️ Risk of stack overflow for large lists

3. STACK APPROACH:
   ❌ O(k) extra space for stack
   ❌ Two passes through the reversal section
   ✅ Very intuitive logic
   ⚠️ Additional memory overhead

4. NODE SWAPPING APPROACH:
   ✅ O(1) space, O(n) time
   ✅ Different perspective on the problem
   ❌ Less intuitive pointer manipulation
   ⚠️ More complex edge case handling

RECOMMENDATION: 
Your original approach is the BEST for interviews and production code because:
- Most commonly expected solution
- Optimal time and space complexity
- Clear, readable, and maintainable
- Standard technique that applies to many linked list problems

The alternatives are good to know for demonstrating different problem-solving approaches!
"""