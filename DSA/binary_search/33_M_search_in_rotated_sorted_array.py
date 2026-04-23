"""
Search in Rotated Sorted Array — Complete Notes & Approaches

Problem:
Given a rotated sorted array, search for a target element.
Return its index or -1 if not found.

------------------------------------------------------------
APPROACH 1: One-Pass Binary Search (Optimal)
------------------------------------------------------------
Idea:
- At least one half (left or right) is always sorted.
- Identify the sorted half and check if target lies in it.

Time Complexity: O(log n)
Space Complexity: O(1)
"""

from typing import List


class SolutionOptimal:
    def search(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums) - 1

        while l <= r:
            mid = (l + r) // 2

            if nums[mid] == target:
                return mid

            # Left half is sorted
            if nums[l] <= nums[mid]:
                if nums[l] <= target < nums[mid]:
                    r = mid - 1
                else:
                    l = mid + 1

            # Right half is sorted
            else:
                if nums[mid] < target <= nums[r]:
                    l = mid + 1
                else:
                    r = mid - 1

        return -1


"""
------------------------------------------------------------
APPROACH 2: Find Pivot + Binary Search
------------------------------------------------------------
Idea:
1. Find the index of smallest element (pivot)
2. Decide which half to search
3. Apply normal binary search

Time Complexity: O(log n)
Space Complexity: O(1)
"""


class SolutionPivot:
    def search(self, nums: List[int], target: int) -> int:

        def find_pivot(nums):
            l, r = 0, len(nums) - 1
            while l < r:
                mid = (l + r) // 2
                if nums[mid] > nums[r]:
                    l = mid + 1
                else:
                    r = mid
            return l

        def binary_search(nums, l, r, target):
            while l <= r:
                mid = (l + r) // 2
                if nums[mid] == target:
                    return mid
                elif nums[mid] < target:
                    l = mid + 1
                else:
                    r = mid - 1
            return -1

        pivot = find_pivot(nums)

        # Decide search range
        if nums[pivot] <= target <= nums[-1]:
            return binary_search(nums, pivot, len(nums) - 1, target)
        else:
            return binary_search(nums, 0, pivot - 1, target)


"""
------------------------------------------------------------
APPROACH 3: Mapping Trick (Modified Binary Search)
------------------------------------------------------------
Idea:
- Treat rotated array as virtually sorted using infinity mapping
- Compare values relative to target side

Time Complexity: O(log n)
Space Complexity: O(1)
"""


class SolutionMapping:
    def search(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums) - 1

        while l <= r:
            mid = (l + r) // 2

            # Check if nums[mid] and target are on same side
            if (nums[mid] < nums[0]) == (target < nums[0]):
                num = nums[mid]
            elif target < nums[0]:
                num = float("-inf")
            else:
                num = float("inf")

            if num == target:
                return mid
            elif num < target:
                l = mid + 1
            else:
                r = mid - 1

        return -1


"""
------------------------------------------------------------
APPROACH 4: Brute Force (Linear Search)
------------------------------------------------------------
Idea:
- Simply scan the array

Time Complexity: O(n)
Space Complexity: O(1)
"""


class SolutionBrute:
    def search(self, nums: List[int], target: int) -> int:
        for i, val in enumerate(nums):
            if val == target:
                return i
        return -1


"""
------------------------------------------------------------
SUMMARY
------------------------------------------------------------

Approach           Time       Space     Notes
------------------------------------------------------------
Optimal (1-pass)   O(log n)   O(1)      Best & most used
Pivot + BS         O(log n)   O(1)      Cleaner logic split
Mapping Trick      O(log n)   O(1)      Clever but less intuitive
Brute Force        O(n)       O(1)      Only for small inputs

------------------------------------------------------------
WHEN TO USE WHAT?
------------------------------------------------------------
- Interviews → Approach 1 (most expected)
- Debug clarity → Approach 2
- Advanced trick → Approach 3
- Baseline → Approach 4
"""