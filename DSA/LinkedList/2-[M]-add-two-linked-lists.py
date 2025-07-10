# https://leetcode.com/problems/add-two-numbers/description/

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
from typing import Optional

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def addTwoNumbers(
        self, l1: Optional[ListNode], l2: Optional[ListNode]
    ) -> Optional[ListNode]:
        """
        Add two numbers represented as linked lists (digits stored in reverse order).
        
        Time Complexity: O(max(m, n)) where m and n are lengths of l1 and l2
        - We traverse both lists once, visiting each node exactly once
        - The loop runs for max(len(l1), len(l2)) iterations
        
        Space Complexity: O(max(m, n)) 
        - We create a new linked list with at most max(m, n) + 1 nodes
        - The +1 accounts for potential final carry digit
        - No additional data structures used beyond the result list
        """
        dummy_head = ListNode(0)
        current = dummy_head
        carry = 0
        
        while l1 or l2 or carry:
            digit1 = l1.val if l1 else 0
            digit2 = l2.val if l2 else 0
            
            total = digit1 + digit2 + carry
            carry = total // 10 
            digit = total % 10 
            
            current.next = ListNode(digit)
            current = current.next
            
            if l1:
                l1 = l1.next
            if l2:
                l2 = l2.next
        
        return dummy_head.next


# Alternative implementation with slightly cleaner pointer management
class SolutionAlternative:
    def addTwoNumbers(
        self, l1: Optional[ListNode], l2: Optional[ListNode]
    ) -> Optional[ListNode]:
        """
        Cleaner version with improved readability.
        Same time and space complexity as above.
        """
        dummy = ListNode(0)
        tail = dummy
        carry = 0
        
        while l1 or l2 or carry:
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0
            
            total = val1 + val2 + carry
            carry, digit = divmod(total, 10)  # More pythonic way to get carry and digit
            
            tail.next = ListNode(digit)
            tail = tail.next
            
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
        
        return dummy.next
