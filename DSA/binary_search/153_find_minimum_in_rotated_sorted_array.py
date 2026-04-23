"""
Find Minimum in Rotated Sorted Array — Complete Notes & Approaches

Problem:
Given a rotated sorted array with NO duplicates,
return the minimum element.

------------------------------------------------------------
APPROACH 1: Your Approach (Tracking Minimum)
------------------------------------------------------------
Idea:
- Use binary search
- Track minimum while narrowing search space
- If left half is sorted → minimum is at left boundary
- Else → minimum lies in right half

Time Complexity: O(log n)
Space Complexity: O(1)
"""

from typing import List
import math


class SolutionTracking:
    def findMin(self, nums: List[int]) -> int:
        l, r = 0, len(nums) - 1
        minimum = math.inf

        while l <= r:
            mid = (l + r) // 2

            # Left half is sorted
            if nums[l] <= nums[mid]:
                minimum = min(minimum, nums[l])
                l = mid + 1
            else:
                minimum = min(minimum, nums[mid])
                r = mid - 1

        return minimum


"""
------------------------------------------------------------
APPROACH 2: Optimal (Cleaner Binary Search)
------------------------------------------------------------
Idea:
- Compare mid with right
- Minimum always lies in UNSORTED half

Key Insight:
- If nums[mid] > nums[r] → min is in right half
- Else → min is in left half (including mid)

Time Complexity: O(log n)
Space Complexity: O(1)
"""


class SolutionOptimal:
    def findMin(self, nums: List[int]) -> int:
        l, r = 0, len(nums) - 1

        while l < r:
            mid = (l + r) // 2

            if nums[mid] > nums[r]:
                l = mid + 1
            else:
                r = mid

        return nums[l]


"""
------------------------------------------------------------
APPROACH 3: Check Already Sorted Optimization
------------------------------------------------------------
Idea:
- If array is already sorted → return first element
- Otherwise use binary search

Time Complexity: O(log n)
Space Complexity: O(1)
"""


class SolutionSortedCheck:
    def findMin(self, nums: List[int]) -> int:
        l, r = 0, len(nums) - 1

        while l < r:
            # Already sorted
            if nums[l] < nums[r]:
                return nums[l]

            mid = (l + r) // 2

            if nums[mid] >= nums[l]:
                l = mid + 1
            else:
                r = mid

        return nums[l]


"""
------------------------------------------------------------
APPROACH 4: Brute Force
------------------------------------------------------------
Idea:
- Simply return min()

Time Complexity: O(n)
Space Complexity: O(1)
"""


class SolutionBrute:
    def findMin(self, nums: List[int]) -> int:
        return min(nums)


"""
------------------------------------------------------------
EDGE CASES
------------------------------------------------------------
- Single element → return that element
- No rotation → first element is minimum
- Fully rotated (same as sorted)
- Two elements

------------------------------------------------------------
SUMMARY
------------------------------------------------------------

Approach              Time       Space     Notes
------------------------------------------------------------
Tracking (yours)      O(log n)   O(1)      Slightly verbose
Optimal (mid vs r)    O(log n)   O(1)      Cleanest & best
Sorted check          O(log n)   O(1)      Early exit optimization
Brute force           O(n)       O(1)      Simplest

------------------------------------------------------------
KEY TAKEAWAY
------------------------------------------------------------
👉 Minimum always lies in the UNSORTED half
👉 Comparing with nums[r] is the cleanest trick
"""