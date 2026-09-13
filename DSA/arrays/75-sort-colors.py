# https://leetcode.com/problems/sort-colors/

from typing import List

"""
Bubble sort approach
- Time Complexity: O(n²) - worst and average case
- Space Complexity: O(1) - in-place sorting
- How it works: Repeatedly steps through the list, compares adjacent elements 
  and swaps them if they're in wrong order. The pass is repeated until no swaps are needed.
- Note: This is actually selection sort implementation, not bubble sort
"""
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        for i in range(0, len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] > nums[j]:
                    nums[i], nums[j] = nums[j], nums[i]

"""
Selection sort approach (corrected implementation)
- Time Complexity: O(n²) - worst, average, and best case
- Space Complexity: O(1) - in-place sorting
- How it works: Finds the minimum element and places it at the beginning, 
  then finds the second minimum and places it at the second position, and so on.
"""
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        for i in range(0, len(nums)):
            min_idx = i
            for j in range(i + 1, len(nums)):
                if nums[j] < nums[min_idx]:
                    min_idx = j
            nums[i], nums[min_idx] = nums[min_idx], nums[i]

"""
Merge sort approach
- Time Complexity: O(n log n) - worst, average, and best case
- Space Complexity: O(n) - requires additional space for merging
- How it works: Divide and conquer algorithm that divides the array into halves,
  recursively sorts them, then merges the sorted halves back together.
- Pros: Stable sort, guaranteed O(n log n) performance
- Cons: Requires extra space, not in-place
"""
class Solution:
    def merge(self, left, right):
        l, r = 0, 0
        lLen, rLen = len(left), len(right)
        result = []
        
        # Merge the two sorted arrays
        while l < lLen and r < rLen:
            if left[l] < right[r]:
                result.append(left[l])
                l += 1
            else:
                result.append(right[r])
                r += 1
        
        # Add remaining elements
        if l < lLen:
            result.extend(left[l:])
        if r < rLen:
            result.extend(right[r:])
        return result

    def mergeSort(self, nums):
        if len(nums) <= 1:
            return nums
        mid = len(nums) // 2
        return self.merge(self.mergeSort(nums[:mid]), self.mergeSort(nums[mid:]))

    def sortColors(self, nums: List[int]) -> None:
        n = len(nums)
        sortedNums = self.mergeSort(nums)
        # Copy sorted elements back to original array
        for i in range(0, n):
            nums[i] = sortedNums[i]

"""
Quick sort approach
- Time Complexity: O(n log n) - average case, O(n²) - worst case (rare)
- Space Complexity: O(log n) - average case due to recursion stack
- How it works: Picks a pivot element, partitions array around pivot,
  then recursively sorts the sub-arrays.
- Pros: In-place sorting, good average performance
- Cons: Worst case O(n²), not stable
- Note: This implementation creates new arrays, making it O(n) space
"""
class Solution:
    def quickSort(self, nums):
        if len(nums) <= 1:
            return nums
        pivot = nums[0]
        left, right = [], []
        
        # Partition around pivot
        for num in nums[1:]:
            if num < pivot:
                left.append(num)
            else:
                right.append(num)
        
        # Recursively sort and combine
        return self.quickSort(left) + [pivot] + self.quickSort(right)

    def sortColors(self, nums: List[int]) -> None:
        sortedNums = self.quickSort(nums)
        for i in range(len(nums)):
            nums[i] = sortedNums[i]

"""
Counting Sort approach (Two-pass solution)
- Time Complexity: O(n) - two passes through the array
- Space Complexity: O(1) - only uses constant extra space (counts array of size 3)
- How it works: First pass counts occurrences of each color (0, 1, 2),
  second pass reconstructs the array based on counts.
- Pros: Simple to understand, O(n) time complexity, works well for small range of values
- Cons: Requires two passes, not as elegant as Dutch National Flag for this problem
"""
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        counts = [0, 0, 0]  # Count of 0s, 1s, 2s
        
        # First pass: count occurrences
        for num in nums:
            counts[num] += 1
        
        # Second pass: reconstruct array
        idx = 0
        for color in range(3):
            for _ in range(counts[color]):
                nums[idx] = color
                idx += 1
                
"""
Dutch National Flag Algorithm (Optimal for this specific problem)
- Time Complexity: O(n) - single pass
- Space Complexity: O(1) - in-place
- How it works: Uses three pointers to partition array into three regions:
  [0...low-1] contains 0s, [low...mid-1] contains 1s, [high+1...n-1] contains 2s
- This is the most efficient approach for sorting colors (0, 1, 2)
"""
class Solution:
    def sortColors(self, nums: List[int]) -> None:

        # Three pointers divide the array into four regions:
        #
        # [0 ... low-1]     -> all 0s
        # [low ... mid-1]   -> all 1s
        # [mid ... high]    -> unknown elements
        # [high+1 ... n-1]  -> all 2s
        #
        # We keep processing the unknown region [mid ... high].
        low = mid = 0
        high = len(nums) - 1

        while mid <= high:

            # If the current element is 0,
            # it belongs to the left (0s) region.
            if nums[mid] == 0:

                # Swap the 0 with nums[low].
                #
                # Why is it safe to increment mid afterward?
                # nums[low] is already inside the processed region
                # [low ... mid-1], which contains only 1s.
                #
                # Therefore, after the swap:
                # - 0 is placed correctly at low
                # - 1 comes to mid, which is already known to be correct
                nums[low], nums[mid] = nums[mid], nums[low]

                low += 1
                mid += 1

            # If the current element is 1,
            # it already belongs to the middle region.
            elif nums[mid] == 1:

                # Nothing needs to be done.
                # Simply mark this element as processed.
                mid += 1

            # If the current element is 2,
            # it belongs to the right (2s) region.
            else:  # nums[mid] == 2

                # Swap the 2 with nums[high] so that the 2
                # moves to the right side.
                #
                # IMPORTANT:
                # nums[high] is part of the UNKNOWN region,
                # so it could be 0, 1, or 2.
                #
                # Therefore, after the swap, the new element
                # at nums[mid] has NOT been processed yet.
                nums[mid], nums[high] = nums[high], nums[mid]

                high -= 1

                # Do NOT increment mid here.
                #
                # The element that came from high into mid
                # could be:
                #   0 -> needs to be moved to the left
                #   1 -> needs to be marked as processed
                #   2 -> needs to be moved to the right again
                #
                # So we must process nums[mid] again.