# https://leetcode.com/problems/remove-nth-node-from-end-of-list/
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# SOLUTION 1: Two-Pass Approach
class Solution1:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        """
        Two-pass approach: First pass to count nodes, second pass to remove
        
        Time Complexity: O(L) where L is the length of the linked list
        - First pass: O(L) to count all nodes
        - Second pass: O(L-n) to reach the node before target
        - Total: O(L) + O(L-n) = O(L)
        
        Space Complexity: O(1) - only using constant extra space
        
        Pros: Easy to understand and implement
        Cons: Requires two passes through the list
        """
        # Create dummy node to handle edge case where head needs to be removed
        dummy = ListNode(0)
        dummy.next = head

        # First pass: Calculate the length of the linked list
        length = 0
        temp = head
        while temp:
            length += 1
            temp = temp.next

        # Second pass: Find the node before the one to be removed
        current = dummy
        for _ in range(length - n):
            current = current.next
        
        # Remove the nth node from end
        current.next = current.next.next

        return dummy.next

# SOLUTION 2: One-Pass Two-Pointer Approach (Optimal)
class Solution2:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        """
        One-pass two-pointer approach using fast and slow pointers
        
        Time Complexity: O(L) where L is the length of the linked list
        - Single pass through the list
        - Fast pointer moves L steps, slow pointer moves (L-n) steps
        
        Space Complexity: O(1) - only using constant extra space
        
        Pros: Single pass, more efficient
        Cons: Slightly more complex logic
        """
        # Create dummy node to handle edge case where head needs to be removed
        dummy = ListNode(0, head)
        fast = slow = dummy

        # Move fast pointer n+1 steps ahead
        # This creates a gap of n+1 between fast and slow
        for _ in range(n + 1):
            fast = fast.next

        # Move both pointers until fast reaches the end
        # When fast is None, slow will be at the node before the target
        while fast:
            slow = slow.next
            fast = fast.next

        # Remove the nth node from end
        slow.next = slow.next.next

        return dummy.next

# SOLUTION 3: Stack-based Approach (Alternative)
class Solution4:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        """
        Stack-based approach for educational purposes
        
        Time Complexity: O(L) where L is the length of the linked list
        Space Complexity: O(L) - stack stores all nodes
        
        Pros: Different approach, easy to understand
        Cons: Uses extra space, not optimal for this problem
        """
        if not head:
            return None
            
        # Push all nodes onto stack
        stack = []
        current = head
        while current:
            stack.append(current)
            current = current.next
        
        # Pop n nodes to reach the target
        for _ in range(n):
            stack.pop()
        
        # If stack is empty, we need to remove head
        if not stack:
            return head.next
        
        # Remove the target node
        prev_node = stack[-1]
        prev_node.next = prev_node.next.next if prev_node.next else None
        
        return head

"""
COMPLEXITY ANALYSIS SUMMARY:

1. Two-Pass Approach (Solution1):
   - Time: O(L) - two passes through the list
   - Space: O(1) - constant space
   - Simple but less efficient

2. Two-Pointer Approach (Solution2 & Solution3):
   - Time: O(L) - single pass through the list
   - Space: O(1) - constant space
   - Most efficient and optimal

3. Stack Approach (Solution4):
   - Time: O(L) - single pass
   - Space: O(L) - stores all nodes in stack
   - Not optimal for space but educational

KEY INSIGHTS:
- Dummy node technique simplifies edge case handling
- Two-pointer approach is most efficient for this problem
- The gap between pointers should be n+1 for proper positioning
- Input validation improves robustness
- Stack approach trades space for conceptual simplicity

RECOMMENDATION:
Use Solution2 (Two-Pointer) for interviews - it's optimal and demonstrates
advanced pointer manipulation techniques.
"""