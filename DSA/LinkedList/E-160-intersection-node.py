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
    def getIntersectionNode(
        self, headA: ListNode, headB: ListNode
    ) -> Optional[ListNode]:
        """
        Store all nodes from list A, then check list B for first match.
        
        TC: O(m + n) - traverse both lists
        SC: O(m) - store all nodes from list A
        """
        visited = set()
        
        # Store all nodes from list A
        curr = headA
        while curr:
            visited.add(curr)
            curr = curr.next
        
        # Check list B for first node in set
        curr = headB
        while curr:
            if curr in visited:
                return curr  # First intersection point
            curr = curr.next
        
        return None  # No intersection


# ============================================================================
# APPROACH 2: TWO POINTERS (OPTIMAL & ELEGANT) - RECOMMENDED
# ============================================================================
class Solution2:
    def getIntersectionNode(
        self, headA: ListNode, headB: ListNode
    ) -> Optional[ListNode]:
        """
        Two pointers that switch lists when reaching end.
        
        Key Insight: By switching lists, both pointers travel same total distance.
        They will meet at intersection (or None if no intersection).
        
        TC: O(m + n) - each pointer traverses both lists at most once
        SC: O(1) - only two pointers
        """
        if not headA or not headB:
            return None
        
        p1, p2 = headA, headB
        
        # Keep moving until they meet (at intersection or None)
        while p1 != p2:
            # When p1 reaches end of A, switch to B
            # When p2 reaches end of B, switch to A
            p1 = p1.next if p1 else headB
            p2 = p2.next if p2 else headA
        
        # Either intersection node or None
        return p1


# ============================================================================
# APPROACH 3: LENGTH DIFFERENCE (ALTERNATIVE O(1) SPACE)
# ============================================================================
class Solution3:
    def getIntersectionNode(
        self, headA: ListNode, headB: ListNode
    ) -> Optional[ListNode]:
        """
        Calculate lengths, align the longer list, then traverse together.
        
        TC: O(m + n) - three passes total
        SC: O(1) - only pointers and counters
        """
        def get_length(head):
            length = 0
            while head:
                length += 1
                head = head.next
            return length
        
        # Get lengths of both lists
        lenA = get_length(headA)
        lenB = get_length(headB)
        
        # Align the starting points
        # Move the longer list's pointer ahead by the difference
        while lenA > lenB:
            headA = headA.next
            lenA -= 1
        
        while lenB > lenA:
            headB = headB.next
            lenB -= 1
        
        # Now traverse together until they meet
        while headA != headB:
            headA = headA.next
            headB = headB.next
        
        return headA  # Intersection or None

# ============================================================================
# WHY THE TWO-POINTER APPROACH WORKS (THE MAGIC!)
# ============================================================================
"""
VISUAL EXAMPLE:
---------------
List A: a1 → a2 → c1 → c2 → c3
                   ↑
List B: b1 → b2 → b3 ─┘

Where c1→c2→c3 is the intersection part.

Let's say:
- Length of A before intersection = a (2 nodes: a1, a2)
- Length of B before intersection = b (3 nodes: b1, b2, b3)
- Length of intersection = c (3 nodes: c1, c2, c3)

Total length A = a + c = 2 + 3 = 5
Total length B = b + c = 3 + 3 = 6

POINTER MOVEMENTS:
------------------
p1 path: a1→a2→c1→c2→c3→None→b1→b2→b3→c1 (meets at c1)
p2 path: b1→b2→b3→c1→c2→c3→None→a1→a2→c1 (meets at c1)

p1 travels: a + c + b = 2 + 3 + 3 = 8 steps to c1
p2 travels: b + c + a = 3 + 3 + 2 = 8 steps to c1

SAME DISTANCE! They meet at intersection!

NO INTERSECTION CASE:
---------------------
List A: a1 → a2 → a3
List B: b1 → b2

p1 path: a1→a2→a3→None→b1→b2→None
p2 path: b1→b2→None→a1→a2→a3→None

Both become None at the same time (after a+b steps each)
Return None (no intersection)

KEY INSIGHT:
------------
By having each pointer traverse BOTH lists:
• If there's intersection: they meet at intersection node
• If no intersection: they both become None together

Distance each travels = a + c + b = b + c + a (same!)
"""


# ============================================================================
# STEP-BY-STEP TRACE EXAMPLE
# ============================================================================
"""
List A: 1 → 2 → 7 → 8 → 9
             ↑
List B: 3 → 4 ─┘

Iteration | p1 position | p2 position | p1==p2?
----------|-------------|-------------|--------
   0      |      1      |      3      |   No
   1      |      2      |      4      |   No
   2      |      7      |      7      |   YES! ✓

Return node 7 (intersection point)

List A: 1 → 2 → 3
List B: 4 → 5 → 6

Iteration | p1 position | p2 position | p1==p2?
----------|-------------|-------------|--------
   0      |      1      |      4      |   No
   1      |      2      |      5      |   No
   2      |      3      |      6      |   No
   3      |      4      |    None     |   No
   4      |      5      |      1      |   No
   5      |      6      |      2      |   No
   6      |    None     |      3      |   No
   7      |    None     |    None     |   YES! ✓

Return None (no intersection)
"""


# ============================================================================
# COMPARISON TABLE
# ============================================================================
"""
╔════════════════════╦═══════╦═══════╦════════════════════════════════╗
║     Approach       ║  TC   ║  SC   ║          Notes                 ║
╠════════════════════╬═══════╬═══════╬════════════════════════════════╣
║ Hash Set           ║ O(m+n)║ O(m)  ║ ✓ Most intuitive               ║
║                    ║       ║       ║ ✓ Easy to implement            ║
║                    ║       ║       ║ ✗ Uses extra space             ║
╠════════════════════╬═══════╬═══════╬════════════════════════════════╣
║ Two Pointers       ║ O(m+n)║ O(1)  ║ ✓ Optimal space                ║
║ (Switch Lists)     ║       ║       ║ ✓ Elegant & clever             ║
║                    ║       ║       ║ ✓ Most popular solution        ║
║                    ║       ║       ║ ⚠ Requires explanation         ║
╠════════════════════╬═══════╬═══════╬════════════════════════════════╣
║ Length Difference  ║ O(m+n)║ O(1)  ║ ✓ Very intuitive logic         ║
║                    ║       ║       ║ ✓ Easy to understand           ║
║                    ║       ║       ║ ✗ Requires 3 passes            ║
║                    ║       ║       ║ ✓ Good alternative approach    ║
╚════════════════════╩═══════╩═══════╩════════════════════════════════╝

INTERVIEW STRATEGY:
-------------------
1. Start with hash set (shows you can solve it)
2. Mention O(m) space usage
3. Present two-pointer approach as optimal O(1) solution
4. Explain the "travel same distance" insight
5. Draw a diagram if possible (interviewers love this!)

COMMON PITFALLS:
----------------
✗ Using 'is' vs '==' - we want node identity, not value comparison
✗ Not handling no-intersection case (infinite loop!)
✗ Forgetting None check at the start
✓ The two-pointer approach naturally handles all cases!

FUN FACT:
---------
This problem is sometimes called "Intersection of Two Linked Lists" or
"Find the merge point of two linked lists". The two-pointer solution
is considered one of the most elegant in linked list problems!

RECOMMENDATION:
---------------
Master the two-pointer approach (Solution 2) - it's the most impressive
solution and shows deep algorithmic thinking. But be ready to explain
WHY it works with the distance argument!
"""