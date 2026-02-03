# https://leetcode.com/problems/kth-largest-element-in-an-array/

import heapq
from typing import List
from queue import PriorityQueue


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
    
# APPROACH 1-2: MIN-HEAP (YOUR SOLUTION)class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        min_heap = []
        for num in nums:
            heapq.heappush(min_heap, num)
            if len(min_heap) > k:
                heapq.heappop(min_heap)
        return min_heap[0]


# APPROACH 2: QUICKSELECT (OPTIMAL AVERAGE CASE)
# Time Complexity: O(n) average, O(n²) worst case
# Space Complexity: O(1) iterative, O(log n) recursive
class Solution2:
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


# APPROACH 6: PRIORITY QUEUE (THREAD-SAFE MIN-HEAP)
# Time Complexity: O(n log k)
# Space Complexity: O(k)
class Solution6:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        """
        PRIORITY QUEUE APPROACH:
        - Similar to min-heap but using Python's queue.PriorityQueue
        - Thread-safe implementation of heap
        - Maintains k largest elements using min-heap property
        
        ADVANTAGES:
        1. Thread-safe operations
        2. Clean API with put() and get() methods
        3. Same time complexity as heapq approach
        
        DISADVANTAGES:
        1. Slightly more overhead than heapq
        2. No direct access to peek at top element
        3. Requires get() to access minimum element
        """
        pq = PriorityQueue()
        
        # Add first k elements
        for i in range(k):
            pq.put(nums[i])
        
        # For remaining elements, if larger than smallest in queue,
        # remove smallest and add new element
        for i in range(k, len(nums)):
            if not pq.empty() and nums[i] > pq.queue[0]:  # peek at minimum
                pq.get()  # remove minimum
                pq.put(nums[i])  # add new element
        
        return pq.get()  # return minimum of k largest elements


# APPROACH 7: PRIORITY QUEUE (MAX-HEAP VARIANT)
# Time Complexity: O(n + k log n)
# Space Complexity: O(n)
class Solution7:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        """
        PRIORITY QUEUE MAX-HEAP APPROACH:
        - Add all elements as negative values to simulate max-heap
        - Extract k-1 largest elements
        - Return kth largest element
        
        ADVANTAGES:
        1. Straightforward logic
        2. Thread-safe
        3. Good for multiple queries on same dataset
        
        DISADVANTAGES:
        1. Uses O(n) space
        2. Slower than min-heap approach for small k
        """
        pq = PriorityQueue()
        
        # Add all elements as negative (to simulate max-heap)
        for num in nums:
            pq.put(-num)
        
        # Extract k-1 largest elements
        for _ in range(k - 1):
            pq.get()
        
        # Return kth largest (negate back)
        return -pq.get()


"""
COMPLEXITY COMPARISON AND RECOMMENDATIONS:

1. **Small k (k << n)**: 
   - **MIN-HEAP (Solution 1)** - O(n log k) ✅ RECOMMENDED
   - **PRIORITY QUEUE (Solution 6)** - O(n log k) ✅ ALTERNATIVE (if thread-safety needed)
   - Best space efficiency and performance

2. **Large k (k close to n)**:
   - **QUICKSELECT (Solution 2)** - O(n) average ✅ RECOMMENDED
   - Best average case performance

3. **Multiple queries on same array**:
   - **SORTING (Solution 3)** - O(n log n) once, then O(1) per query
   - Or MAX-HEAP for partial sorting

4. **Streaming data**:
   - **MIN-HEAP (Solution 1)** ✅ RECOMMENDED
   - **PRIORITY QUEUE (Solution 6)** ✅ ALTERNATIVE (if thread-safety needed)
   - Can handle continuous data flow

5. **Limited integer range**:
   - **BUCKET SORT (Solution 5)** - O(n) ✅ RECOMMENDED
   - Linear time complexity

6. **Multi-threaded environment**:
   - **PRIORITY QUEUE (Solution 6 or 7)** ✅ RECOMMENDED
   - Thread-safe operations

DECISION TREE:
- k ≤ log n: Use MIN-HEAP
- k > log n: Use QUICKSELECT
- Need stability: Use SORTING
- Streaming: Use MIN-HEAP
- Limited range: Use BUCKET SORT
- Multi-threaded: Use PRIORITY QUEUE

PRIORITY QUEUE vs HEAPQ:
- PriorityQueue: Thread-safe, cleaner API, slightly more overhead
- heapq: Faster, direct access to elements, not thread-safe
- For single-threaded applications: prefer heapq
- For multi-threaded applications: prefer PriorityQueue

YOUR SOLUTION ANALYSIS:
Your min-heap solution is excellent for small k values and is the most commonly
used approach in practice due to its:
- Predictable performance
- Space efficiency
- Suitability for streaming data
- Clean implementation
"""