# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

import heapq
from typing import List, Optional

"""
ALGORITHM APPROACHES FOR MERGE K SORTED LISTS

1. BRUTE FORCE - Collect All Values
   - Extract all values from all lists
   - Sort all values
   - Create new linked list
   - Time: O(N log N), Space: O(N)
   
2. SEQUENTIAL MERGING (Compare One by One)
   - Take first list as result
   - Merge with second list, then third, etc.
   - Time: O(k*N), Space: O(1)
   - Gets slower as result list grows
   
3. PRIORITY QUEUE/MIN-HEAP
   - Use heap to always get minimum element
   - Two variants:
     a) Store all values in heap
     b) Store only head nodes in heap
   - Time: O(N log k), Space: O(k)
   
4. DIVIDE AND CONQUER
   - Pair up lists and merge pairs
   - Repeat until one list remains
   - Time: O(N log k), Space: O(log k)
   - Most efficient and elegant
   
5. MERGE WITH COMPARISON
   - Use k-way merge algorithm
   - Compare heads of all lists each time
   - Time: O(k*N), Space: O(1)
   - Similar to sequential but compares all at once

WHERE:
- N = total number of nodes across all lists
- k = number of lists
"""

# APPROACH 1: Sequential Merging (Your first solution)
# ALGORITHM: Take first list, merge with second, then merge result with third, etc.
# Time: O(k*N) where k is number of lists, N is total nodes
# Space: O(1)
# Why O(k*N)? First merge: N/k nodes, Second merge: 2N/k nodes, ... kth merge: N nodes
# Total: N/k + 2N/k + 3N/k + ... + N = N(1/k + 2/k + ... + k/k) = N * k(k+1)/(2k) = O(k*N)
class Solution1:
    def merge(self, l1, l2):
        result = ListNode(None)
        dummy = result
        while l1 and l2:
            if l1.val < l2.val:
                dummy.next = l1
                l1 = l1.next
            else:
                dummy.next = l2
                l2 = l2.next
            dummy = dummy.next
        if l1:
            dummy.next = l1
        else:
            dummy.next = l2
        return result.next

    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if len(lists) == 0:
            return None
        result = lists[0]
        for li in lists[1:]:
            result = self.merge(result, li)
        return result

# APPROACH 2: Extract All Values (Your second solution)
# ALGORITHM: Extract all node values, sort them, create new linked list
# Time: O(N log N) where N is total nodes
# Space: O(N) 
# Issue: Creates entirely new nodes instead of reusing existing ones
# Why O(N log N)? Extracting: O(N), Sorting: O(N log N), Creating: O(N)
class Solution2:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if len(lists) == 0:
            return None
        min_heap = []
        heapq.heapify(min_heap)
        for li in lists:
            while li:
                heapq.heappush(min_heap, li.val)
                li = li.next
        min_heap.sort()  # This line is unnecessary since heap maintains order
        merged_list = ListNode(0)
        dummy = merged_list
        for num in min_heap:
            dummy.next = ListNode(num)  # Creates new nodes
            dummy = dummy.next
        return merged_list.next

# APPROACH 3: Min-Heap with Nodes (Your third solution)
# ALGORITHM: Use min-heap to track head of each list, always pop minimum
# Time: O(N log k) where N is total nodes, k is number of lists
# Space: O(k)
# This is the most efficient approach among yours!
# Why O(N log k)? N nodes total, each push/pop operation takes O(log k)
class Solution3:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if len(lists) == 0:
            return None
        min_heap = []
        heapq.heapify(min_heap)
        for i, li in enumerate(lists):
            if li:
                heapq.heappush(min_heap, (li.val, i, li))

        merged_list = ListNode(0)
        dummy = merged_list
        while len(min_heap) != 0:
            val, idx, li = heapq.heappop(min_heap)
            dummy.next = li
            dummy = dummy.next
            if li.next:
                heapq.heappush(min_heap, (li.next.val, idx, li.next))
        return merged_list.next

# APPROACH 4: Divide and Conquer (Most Optimal)
# ALGORITHM: Pair up lists and merge pairs, repeat until one list remains
# Round 1: [L1,L2], [L3,L4], [L5,L6] -> merge pairs
# Round 2: [L1+L2, L3+L4], [L5+L6] -> merge pairs  
# Round 3: [L1+L2+L3+L4, L5+L6] -> merge final pair
# Time: O(N log k) where N is total nodes, k is number of lists
# Space: O(log k) due to recursion stack
# Why O(N log k)? log k levels, each level processes N nodes total
class Solution4:
    def merge(self, l1, l2):
        dummy = ListNode(0)
        current = dummy
        
        while l1 and l2:
            if l1.val <= l2.val:
                current.next = l1
                l1 = l1.next
            else:
                current.next = l2
                l2 = l2.next
            current = current.next
        
        current.next = l1 or l2
        return dummy.next
    
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if not lists:
            return None
        
        while len(lists) > 1:
            merged_lists = []
            for i in range(0, len(lists), 2):
                l1 = lists[i]
                l2 = lists[i + 1] if i + 1 < len(lists) else None
                merged_lists.append(self.merge(l1, l2))
            lists = merged_lists
        
        return lists[0]

# APPROACH 5: K-Way Merge with Direct Comparison
# ALGORITHM: At each step, compare heads of all k lists and pick minimum
# Time: O(k*N) where k is number of lists, N is total nodes
# Space: O(1)
# Why O(k*N)? For each of N nodes, we compare across k lists
class Solution5:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if not lists:
            return None
        
        # Remove empty lists
        lists = [l for l in lists if l]
        if not lists:
            return None
            
        dummy = ListNode(0)
        current = dummy
        
        while lists:
            # Find minimum among all list heads
            min_idx = 0
            for i in range(1, len(lists)):
                if lists[i].val < lists[min_idx].val:
                    min_idx = i
            
            # Add minimum node to result
            current.next = lists[min_idx]
            current = current.next
            lists[min_idx] = lists[min_idx].next
            
            # Remove empty lists
            if not lists[min_idx]:
                lists.pop(min_idx)
        
        return dummy.next

# APPROACH 6: Brute Force - Collect and Sort
# ALGORITHM: Traverse all lists, collect values, sort, rebuild
# Time: O(N log N), Space: O(N)
class Solution6:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        values = []
        
        # Collect all values
        for head in lists:
            while head:
                values.append(head.val)
                head = head.next
        
        # Sort values
        values.sort()
        
        # Build new linked list
        dummy = ListNode(0)
        current = dummy
        for val in values:
            current.next = ListNode(val)
            current = current.next
        
        return dummy.next
