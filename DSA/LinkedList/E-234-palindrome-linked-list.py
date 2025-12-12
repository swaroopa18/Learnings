# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

from typing import Optional

# ============================================================================
# APPROACH 1: COPY AND REVERSE (SIMPLE BUT USES EXTRA SPACE)
# ============================================================================
class Solution1:
    def reverse(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Create a NEW reversed copy of the list.
        
        TC: O(n) - traverse once
        SC: O(n) - create new nodes
        """
        reversed_head = None
        
        while head:
            # Create new node with current value
            new_node = ListNode(head.val)
            # Insert at front of reversed list
            new_node.next = reversed_head
            reversed_head = new_node
            
            head = head.next
        
        return reversed_head
    
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        """
        Compare original list with its reversed copy.
        
        TC: O(n) - two passes (reverse + compare)
        SC: O(n) - entire copy of the list
        """
        # Create reversed copy
        reversed_list = self.reverse(head)
        
        # Compare original with reversed
        original = head
        while original:
            if original.val != reversed_list.val:
                return False
            original = original.next
            reversed_list = reversed_list.next
        
        return True


# ============================================================================
# APPROACH 2: IN-PLACE REVERSAL (OPTIMAL) - RECOMMENDED
# ============================================================================
class Solution2:
    def reverse(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Reverse list IN-PLACE by changing pointers (no new nodes).
        
        TC: O(n)
        SC: O(1)
        """
        prev = None
        
        while head:
            # Save next node before changing pointer
            next_node = head.next
            # Reverse the pointer
            head.next = prev
            # Move prev and head forward
            prev = head
            head = next_node
        
        return prev
    
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        """
        Find middle, reverse second half, compare, then restore.
        
        Steps:
        1. Use slow/fast pointers to find middle
        2. Reverse second half in-place
        3. Compare first half with reversed second half
        
        TC: O(n) - three passes (find middle, reverse, compare)
        SC: O(1) - only pointers used
        """
        # Edge case: empty or single node
        if not head or not head.next:
            return True
        
        # Step 1: Find middle using slow/fast pointers
        slow = fast = head
        
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        # Adjust for odd/even length
        # If odd length, skip middle element
        # If even length, slow is at start of second half
        second_half = slow.next if fast else slow
        
        # Step 2: Reverse second half
        reversed_second = self.reverse(second_half)
        
        # Step 3: Compare first half with reversed second half
        first = head
        second = reversed_second
        
        while second:  # Compare until end of second half
            if first.val != second.val:
                return False
            first = first.next
            second = second.next
        
        return True


# ============================================================================
# APPROACH 3: ARRAY CONVERSION (MOST STRAIGHTFORWARD)
# ============================================================================
class Solution3:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        """
        Convert to array and use two pointers.
        
        TC: O(n)
        SC: O(n) - store all values in array
        """
        values = []
        
        # Convert linked list to array
        curr = head
        while curr:
            values.append(curr.val)
            curr = curr.next
        
        # Two pointer palindrome check
        left, right = 0, len(values) - 1
        
        while left < right:
            if values[left] != values[right]:
                return False
            left += 1
            right -= 1
        
        return True


# ============================================================================
# APPROACH 4: OPTIMIZED WITH LIST RESTORATION (BEST PRACTICE)
# ============================================================================
class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        """
        Same as Solution2 but RESTORES the list structure after checking.
        This is important if the list is used elsewhere!
        
        TC: O(n)
        SC: O(1)
        """
        if not head or not head.next:
            return True
        
        # Find middle
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        # Reverse second half
        prev = None
        curr = slow
        while curr:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node
        
        # Compare and track result
        is_palindrome = True
        first = head
        second = prev  # prev is now head of reversed second half
        
        while second:
            if first.val != second.val:
                is_palindrome = False
                break  # Can break early but still need to restore
            first = first.next
            second = second.next
        
        # RESTORE: Reverse the second half back
        prev_restore = None
        curr = prev
        while curr:
            next_node = curr.next
            curr.next = prev_restore
            prev_restore = curr
            curr = next_node
        
        return is_palindrome


# ============================================================================
# VISUAL WALKTHROUGH
# ============================================================================
"""
EXAMPLE: List = 1 → 2 → 3 → 2 → 1

STEP 1: Find Middle
-------------------
Initial: slow=1, fast=1
  Iter1: slow=2, fast=3
  Iter2: slow=3, fast=None (reached end)
  
Middle found at node 3 (odd length, so skip this node)

STEP 2: Reverse Second Half
----------------------------
Original:  1 → 2 → 3 → 2 → 1
                   ↑
Second half: 2 → 1

Reverse it:  1 ← 2

Result:
First half:  1 → 2 → 3
Second half: 2 → 1 (reversed) or 1 ← 2

STEP 3: Compare
---------------
First:  1 → 2 → 3
Second: 2 → 1

Compare 1 == 2? No, wait...

Actually for odd length:
First:  1 → 2 → 3
Second: 2 → 1 (we start from 2)

Wait, let me recalculate properly:

List: 1 → 2 → 3 → 2 → 1

After finding middle (node 3), second_half starts at node after middle:
second_half = 2 → 1

Reverse second_half: 1 → 2

Compare:
Position 0: first=1, second=1 ✓
Position 1: first=2, second=2 ✓
Position 2: first=3, second=None (done)

Result: PALINDROME! ✓

EXAMPLE 2: List = 1 → 2 (even length)
--------------------------------------
Find middle: slow=2, fast=None (even, slow IS the second half start)
Second half: 2
Reverse: 2
Compare: first=1, second=2 ✗
Result: NOT PALINDROME


EXAMPLE 3: List = 1 → 2 → 2 → 1 (even length)
----------------------------------------------
Find middle: slow=2 (second one), fast=None
Second half: 2 → 1
Reverse: 1 → 2
Compare:
  first=1, second=1 ✓
  first=2, second=2 ✓
Result: PALINDROME! ✓
"""


# ============================================================================
# KEY DIFFERENCES BETWEEN SOLUTIONS
# ============================================================================
"""
Solution1 vs Solution2 - THE CRITICAL DIFFERENCE:
--------------------------------------------------

Solution1.reverse() - CREATES NEW NODES:
    temp = ListNode(head.val)  ← NEW NODE!
    temp.next = reverse
    
    Result: Original list unchanged, new reversed copy created
    Memory: O(n) extra space

Solution2.reverse() - MODIFIES EXISTING NODES:
    temp = head.next           ← Just a pointer!
    head.next = reverse        ← Changes existing node
    
    Result: Original list structure changed
    Memory: O(1) space

Visual difference:
------------------
Original: 1 → 2 → 3

Solution1.reverse():
  Original: 1 → 2 → 3 (unchanged)
  New copy: 3 → 2 → 1 (separate nodes in memory)

Solution2.reverse():
  After:    3 → 2 → 1 (same nodes, pointers changed)
  Original list is destroyed!
"""


# ============================================================================
# COMPARISON TABLE
# ============================================================================
"""
╔════════════════════╦═══════╦═══════╦════════════════════════════════╗
║     Approach       ║  TC   ║  SC   ║          Notes                 ║
╠════════════════════╬═══════╬═══════╬════════════════════════════════╣
║ Copy & Reverse     ║ O(n)  ║ O(n)  ║ ✓ Simple and clear             ║
║ (Solution1)        ║       ║       ║ ✓ Doesn't modify original      ║
║                    ║       ║       ║ ✗ Uses extra space             ║
║                    ║       ║       ║ ✗ Creates n new nodes          ║
╠════════════════════╬═══════╬═══════╬════════════════════════════════╣
║ In-Place Reversal  ║ O(n)  ║ O(1)  ║ ✓ Optimal space                ║
║ (Solution2)        ║       ║       ║ ✓ Most efficient               ║
║                    ║       ║       ║ ✗ Destroys original structure  ║
║                    ║       ║       ║ ⚠ Should restore if needed     ║
╠════════════════════╬═══════╬═══════╬════════════════════════════════╣
║ Array Conversion   ║ O(n)  ║ O(n)  ║ ✓ Most intuitive               ║
║ (Solution3)        ║       ║       ║ ✓ Easiest to implement         ║
║                    ║       ║       ║ ✗ Uses extra space             ║
║                    ║       ║       ║ ✓ Good for interviews          ║
╠════════════════════╬═══════╬═══════╬════════════════════════════════╣
║ With Restoration   ║ O(n)  ║ O(1)  ║ ✓ Optimal space                ║
║ (Solution4)        ║       ║       ║ ✓ Restores original            ║
║                    ║       ║       ║ ✓ Production-ready             ║
║                    ║       ║       ║ ✗ Slightly more complex        ║
╚════════════════════╩═══════╩═══════╩════════════════════════════════╝

INTERVIEW STRATEGY:
-------------------
1. Start with array approach (shows you can solve it quickly)
2. Mention O(n) space usage
3. Present in-place reversal as O(1) space optimization
4. Explain the slow/fast pointer technique for finding middle
5. Bonus points: Mention you could restore the list if needed

COMMON MISTAKES:
----------------
✗ Not handling odd vs even length correctly
✗ Comparing entire list instead of just first half vs second half
✗ Off-by-one errors when finding middle
✗ Not considering single-node edge case
✓ Solution2 handles all cases elegantly!

KEY INSIGHT:
------------
The middle-finding technique:
• For ODD length (1→2→3→2→1): fast reaches end, slow at middle
  → Skip middle node (it doesn't need comparison)
• For EVEN length (1→2→2→1): fast reaches end, slow at second half start
  → Compare both halves completely

RECOMMENDATION:
---------------
Learn Solution2 (in-place reversal) - it's the optimal solution and
demonstrates strong space optimization skills. However, be prepared to
discuss the trade-off of modifying the input and mention restoration
(Solution4) for real-world scenarios.
"""