# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

from typing import Optional

# ============================================================================
# APPROACH 1: RECURSIVE
# ============================================================================
class Solution1:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Swap adjacent nodes recursively.
        
        TC: O(n) - visit each node once
        SC: O(n) - recursive call stack depth
        """
        # Base case: empty list or single node
        if not head or not head.next:
            return head
        
        # Identify the pair to swap
        first = head          # 1st node in current pair
        second = head.next    # 2nd node in current pair
        
        # Recursively swap remaining list and attach to first node
        first.next = self.swapPairs(second.next)
        
        # Complete the swap: second points to first
        second.next = first
        
        # Return second as new head of this segment
        return second


# ============================================================================
# APPROACH 2: ITERATIVE (RECOMMENDED)
# ============================================================================
class Solution2:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Swap adjacent nodes iteratively using a dummy node.
        
        TC: O(n) - single pass through the list
        SC: O(1) - only uses pointers, no extra space
        """
        # Dummy node simplifies edge cases (empty list, swapping head)
        dummy = ListNode(0, head)
        prev = dummy
        
        # Process pairs while we have at least 2 nodes
        while head and head.next:
            first = head
            second = head.next
            
            # Perform the swap:
            # Before: prev -> first -> second -> remaining
            # After:  prev -> second -> first -> remaining
            prev.next = second           # prev points to second
            first.next = second.next     # first points to remaining
            second.next = first          # second points to first
            
            # Move pointers forward for next iteration
            prev = first                 # prev is now the swapped first node
            head = first.next            # head moves to next unprocessed node
        
        return dummy.next


# ============================================================================
# APPROACH 3: CLEANER ITERATIVE (BEST)
# ============================================================================
class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Most readable iterative solution.
        
        TC: O(n) - single pass
        SC: O(1) - constant space
        """
        dummy = ListNode(0, head)
        prev = dummy
        curr = head
        
        while curr and curr.next:
            # Save references
            next_pair = curr.next.next
            second = curr.next
            
            # Swap the pair
            prev.next = second
            second.next = curr
            curr.next = next_pair
            
            # Move to next pair
            prev = curr
            curr = next_pair
        
        return dummy.next