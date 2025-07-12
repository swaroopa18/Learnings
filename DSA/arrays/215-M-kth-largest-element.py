# https://leetcode.com/problems/kth-largest-element-in-an-array/

from typing import List
import heapq
import random


# APPROACH 1: MIN-HEAP (YOUR SOLUTION)
# Time Complexity: O(n log k) - each push/pop on the heap of size k costs log k.
# Space Complexity: O(k) - heap size
class Solution1:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        """
        MIN-HEAP APPROACH:
        - Maintain a min-heap of size k containing the k largest elements
        - The root (min_heap[0]) will be the kth largest element
        - For each new element, if it's larger than the smallest in our k largest,
          replace the smallest with the new element
        
        DISADVANTAGES:
        1. Not optimal for large k values (k close to n)
        2. Always O(n log k) - no best case optimization
        """
        min_heap = nums[:k]
        heapq.heapify(min_heap)  # O(k) time
        
        for num in nums[k:]:
            if min_heap[0] < num:
                heapq.heappop(min_heap)    # Remove smallest - O(log k)
                heapq.heappush(min_heap, num)  # Add new element - O(log k)
        
        return min_heap[0]


# APPROACH 2: QUICKSELECT (OPTIMAL AVERAGE CASE)
# Time Complexity: O(n) average, O(n²) worst case
# Space Complexity: O(1) iterative, O(log n) recursive
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        n = len(nums)
        k = n - k
        def quickSelect(l, r):
            pivot, p = nums[r], l
            for i in range(l, r):
                if nums[i] <= pivot:
                    nums[p], nums[i] = nums[i], nums[p]
                    p += 1
            nums[p], nums[r] = nums[r], nums[p]
            if p > k:
                return quickSelect(l, p - 1)
            elif p < k:
                return quickSelect(p + 1, r)
            else:
                return pivot
        return quickSelect(0, n - 1)


# APPROACH 3: SORTING (SIMPLE BUT NOT OPTIMAL)
# Time Complexity: O(n log n)
# Space Complexity: O(1) if in-place sorting
class Solution3:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        nums.sort(reverse=True)
        return nums[k-1]


# APPROACH 4: MAX-HEAP (ALTERNATIVE HEAP APPROACH)
# Time Complexity: O(n + k log n)
# Space Complexity: O(n)
class Solution4:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        max_heap = [-num for num in nums]
        heapq.heapify(max_heap)
        
        # Pop k-1 largest elements
        for _ in range(k-1):
            heapq.heappop(max_heap)
        
        # Return kth largest (negate back)
        return -max_heap[0]


# APPROACH 5: BUCKET SORT (FOR LIMITED RANGE)
# Time Complexity: O(n + range)
# Space Complexity: O(range)
class Solution5:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        """
        BUCKET SORT APPROACH:
        - Use when number range is limited
        - Count frequency of each number
        - Find kth largest by counting from maximum
        
        ADVANTAGES:
        1. Linear time O(n) when range is small
        2. Stable performance
        
        DISADVANTAGES:
        1. Only works for limited integer ranges
        2. High space complexity for large ranges
        3. Not general purpose
        """
        min_val, max_val = min(nums), max(nums)
        
        # Count frequency of each number
        count = [0] * (max_val - min_val + 1)
        for num in nums:
            count[num - min_val] += 1
        
        # Find kth largest by counting from maximum
        remaining = k
        for i in range(len(count) - 1, -1, -1):
            remaining -= count[i]
            if remaining <= 0:
                return i + min_val
        
        return -1  # Should never reach here


"""
COMPLEXITY COMPARISON AND RECOMMENDATIONS:

1. **Small k (k << n)**: 
   - **MIN-HEAP (Solution 1)** - O(n log k) ✅ RECOMMENDED
   - Best space efficiency and performance

2. **Large k (k close to n)**:
   - **QUICKSELECT (Solution 2)** - O(n) average ✅ RECOMMENDED
   - Best average case performance

3. **Multiple queries on same array**:
   - **SORTING (Solution 3)** - O(n log n) once, then O(1) per query
   - Or MAX-HEAP for partial sorting

4. **Streaming data**:
   - **MIN-HEAP (Solution 1)** ✅ RECOMMENDED
   - Can handle continuous data flow

5. **Limited integer range**:
   - **BUCKET SORT (Solution 5)** - O(n) ✅ RECOMMENDED
   - Linear time complexity

DECISION TREE:
- k ≤ log n: Use MIN-HEAP
- k > log n: Use QUICKSELECT
- Need stability: Use SORTING
- Streaming: Use MIN-HEAP
- Limited range: Use BUCKET SORT

YOUR SOLUTION ANALYSIS:
Your min-heap solution is excellent for small k values and is the most commonly
used approach in practice due to its:
- Predictable performance
- Space efficiency
- Suitability for streaming data
- Clean implementation
"""

# Test all approaches
if __name__ == "__main__":
    test_cases = [
        ([3,2,1,5,6,4], 2),  # Expected: 5
        ([3,2,3,1,2,4,5,5,6], 4),  # Expected: 4
        ([1], 1),  # Expected: 1
        ([7,10,4,3,20,15], 3),  # Expected: 10
    ]
    
    solutions = [Solution1(), Solution2(), Solution3(), Solution4(), Solution5()]
    
    for i, (nums, k) in enumerate(test_cases):
        print(f"Test case {i+1}: nums={nums}, k={k}")
        for j, sol in enumerate(solutions, 1):
            result = sol.findKthLargest(nums.copy(), k)  # Use copy to avoid modification
            print(f"  Solution {j}: {result}")
        print()