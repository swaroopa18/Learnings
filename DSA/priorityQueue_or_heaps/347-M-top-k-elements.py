import heapq
from typing import List
from collections import Counter, defaultdict


# APPROACH 1: Min Heap (Size K)
class Solution1:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        """
        Uses a min heap of size k to maintain the k most frequent elements.
        
        Time Complexity: O(n log k) where n is length of nums
        - Building frequency map: O(n)
        - Processing each unique element with heap operations: O(unique_elements * log k)
        - In worst case, unique_elements = n, so O(n log k)
        
        Space Complexity: O(n) for frequency map + O(k) for heap = O(n)
        
        Pros: Memory efficient when k is small, good for streaming data
        Cons: Slower than bucket sort for large datasets
        """
        hmap = {}
        for num in nums:
            hmap[num] = hmap.get(num, 0) + 1

        min_heap = []
        for num, freq in hmap.items():
            heapq.heappush(min_heap, (freq, num))
            if len(min_heap) > k:
                heapq.heappop(min_heap)

        return [num for _, num in min_heap]


# APPROACH 2: Bucket Sort (Optimal for this problem)
class Solution2:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        """
        Uses bucket sort based on frequency counts.
        
        Time Complexity: O(n) where n is length of nums
        - Building frequency map: O(n)
        - Filling buckets: O(unique_elements) ≤ O(n)
        - Extracting result: O(n) in worst case
        
        Space Complexity: O(n) for frequency map + O(n) for buckets = O(n)
        
        Pros: Optimal time complexity, simple logic
        Cons: Uses more space when frequencies are sparse
        """
        # Step 1: Build frequency map
        freq = {}
        for num in nums:
            freq[num] = freq.get(num, 0) + 1
        
        # Step 2: Create buckets indexed by frequency
        # Maximum possible frequency is len(nums) (all elements are same)
        buckets = [[] for _ in range(len(nums) + 1)]
        for num, count in freq.items():
            buckets[count].append(num)
        
        # Step 3: Collect result from highest frequency to lowest
        result = []
        for i in range(len(buckets) - 1, -1, -1):  # Iterate backwards
            for num in buckets[i]:
                if len(result) < k:
                    result.append(num)
                else:
                    break
            if len(result) == k:  # Early termination optimization
                break
        
        return result


# APPROACH 3: Max Heap (Alternative heap approach)
class Solution3:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        """
        Uses a max heap to get top k elements directly.
        
        Time Complexity: O(n + m log m) where m is number of unique elements
        - Building frequency map: O(n)
        - Building heap: O(m)
        - Extracting k elements: O(k log m)
        
        Space Complexity: O(n) for frequency map + O(m) for heap = O(n)
        
        Pros: Intuitive, can easily get top k in sorted order
        Cons: Less efficient than min heap approach when k is small
        """
        # Step 1: Build frequency map
        freq = Counter(nums)
        
        # Step 2: Create max heap (negate counts for max heap behavior)
        max_heap = [(-count, num) for num, count in freq.items()]
        heapq.heapify(max_heap)
        
        # Step 3: Extract top k elements
        result = []
        for _ in range(k):
            _, num = heapq.heappop(max_heap)
            result.append(num)
        
        return result


# APPROACH 4: Sorting (Simple but less efficient)
class Solution4:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        """
        Sort elements by frequency and take top k.
        
        Time Complexity: O(n + m log m) where m is number of unique elements
        - Building frequency map: O(n)
        - Sorting: O(m log m)
        
        Space Complexity: O(n) for frequency map + O(m) for sorting = O(n)
        
        Pros: Simple to implement and understand
        Cons: Not optimal, requires sorting entire frequency map
        """
        freq = Counter(nums)
        
        # Sort by frequency (descending) and take first k elements
        sorted_items = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        
        return [num for num, _ in sorted_items[:k]]


# APPROACH 5: Quick Select (Advanced - Average O(n))
class Solution5:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        """
        Uses quickselect algorithm to find kth most frequent element.
        
        Time Complexity: O(n) average case, O(n²) worst case
        - Building frequency map: O(n)
        - Quickselect: O(m) average, O(m²) worst case where m is unique elements
        
        Space Complexity: O(n) for frequency map
        
        Pros: Optimal average time complexity, doesn't require sorting
        Cons: Complex implementation, worst case is quadratic
        """
        freq = Counter(nums)
        unique_nums = list(freq.keys())
        
        def quickselect(left, right, k_smallest):
            """Find kth smallest element by frequency"""
            if left == right:
                return
            
            # Choose random pivot
            pivot_idx = left
            pivot_freq = freq[unique_nums[pivot_idx]]
            
            # Partition around pivot
            store_idx = left
            for i in range(left, right):
                if freq[unique_nums[i]] < pivot_freq:
                    unique_nums[store_idx], unique_nums[i] = unique_nums[i], unique_nums[store_idx]
                    store_idx += 1
            
            # Place pivot in correct position
            unique_nums[store_idx], unique_nums[right] = unique_nums[right], unique_nums[store_idx]
            
            # Recursively search in appropriate half
            if k_smallest == store_idx:
                return
            elif k_smallest < store_idx:
                quickselect(left, store_idx - 1, k_smallest)
            else:
                quickselect(store_idx + 1, right, k_smallest)
        
        n = len(unique_nums)
        quickselect(0, n - 1, n - k)  # Find (n-k)th smallest = kth largest
        
        return unique_nums[n - k:]


# PERFORMANCE COMPARISON AND RECOMMENDATIONS:

"""
WHEN TO USE EACH APPROACH:

1. BUCKET SORT (Solution2) - RECOMMENDED FOR MOST CASES
   - Best overall performance: O(n) time
   - Use when: General purpose, optimal solution needed
   - Avoid when: Memory is extremely constrained

2. MIN HEAP (Solution1) - GOOD FOR SMALL K
   - Use when: k is small relative to number of unique elements
   - Use when: Streaming data or memory constrained
   - Avoid when: k is large or you need optimal time complexity

3. MAX HEAP (Solution3) - GOOD FOR EDUCATIONAL PURPOSES
   - Use when: You need results in frequency order
   - Use when: Learning heap data structures
   - Avoid when: k is small (min heap is better)

4. SORTING (Solution4) - SIMPLE BUT SUBOPTIMAL
   - Use when: Code simplicity is priority over performance
   - Use when: Quick prototype or small datasets
   - Avoid when: Performance matters

5. QUICK SELECT (Solution5) - ADVANCED OPTIMIZATION
   - Use when: You need theoretical O(n) average case
   - Use when: You're familiar with quickselect algorithm
   - Avoid when: Worst case O(n²) is unacceptable

OVERALL RECOMMENDATION:
Use bucket sort (Solution2) for most production code - it's optimal, 
simple to understand, and performs well in practice.
"""