# ============================================================
# PROBLEM: Trapping Rain Water (LeetCode 42)
# ============================================================
# Given n non-negative integers representing an elevation map
# where the width of each bar is 1, compute how much water
# it can trap after raining.
#
# Example:
#   Input:  height = [0,1,0,2,1,0,1,3,2,1,2,1]
#   Output: 6
#
#   Input:  height = [4,2,0,3,2,5]
#   Output: 9
# ============================================================


# ============================================================
# KEY INSIGHT (applies to ALL approaches)
# ============================================================
# Water above any bar i is determined by:
#
#   water[i] = min(max_height_to_left, max_height_to_right) - height[i]
#
# Think of it like pouring water into a valley —
# the water level is limited by the SHORTER of the two surrounding walls.
# If this value is negative (bar is taller than both walls), no water sits here.
# ============================================================


# ============================================================
# APPROACH 1: Prefix/Suffix Max Arrays (your first solution)
# ============================================================
# Strategy:
#   Pre-compute two arrays:
#     max_left[i]  = max height in height[0..i-1]   (tallest wall to the LEFT)
#     max_right[i] = max height in height[i+1..n-1] (tallest wall to the RIGHT)
#   Then for each bar, apply the key insight above.
#
# Why slicing (height[:i]) is suboptimal:
#   Each max(height[:i]) call is O(i), making the loop O(n²) total.
#   Fix: build max_left incrementally → max_left[i] = max(max_left[i-1], height[i-1])
#   (shown in the corrected version below)
#
# Time Complexity : O(n²) as written due to slicing inside loop
#                   O(n)  with incremental fix (see below)
# Space Complexity: O(n)  — two extra arrays of size n
# ============================================================

from typing import List

class SolutionPrefixSuffix:
    def trap(self, height: List[int]) -> int:
        n = len(height)
        max_left  = [0] * n
        max_right = [0] * n

        # ⚠️  Original uses max(height[:i]) → O(n) per iteration = O(n²) total
        # ✅  Incremental fix: carry forward the running max instead
        for i in range(1, n):
            max_left[i] = max(max_left[i - 1], height[i - 1])   # running max from left

        for i in range(n - 2, -1, -1):
            max_right[i] = max(max_right[i + 1], height[i + 1]) # running max from right

        total = 0
        for i in range(n):
            # Water trapped = bounded by shorter wall, minus the bar's own height
            water = min(max_left[i], max_right[i]) - height[i]
            if water > 0:
                total += water

        return total


# ============================================================
# APPROACH 2: Two Pointers — Optimal (your second solution)
# ============================================================
# Strategy:
#   Eliminate the extra arrays entirely by observing:
#     → If max_left < max_right, the LEFT side is the limiting wall.
#       We don't need to know the exact right max — we know it's ≥ max_left,
#       so water at l is fully determined by max_left alone.
#     → Symmetrically, if max_right ≤ max_left, process the right pointer.
#
#   Move the pointer on the SHORTER side inward each step.
#   Update the running max AFTER computing water (order matters!).
#
# Why the order of operations matters:
#   curr = min(max_left, max_right) - height[l]   ← use OLD max before update
#   max_left = max(max_left, height[l])            ← THEN update
#   Swapping these two lines would count the bar's own height as a wall.
#
# Time Complexity : O(n)  — single pass, each element visited once
# Space Complexity: O(1)  — only a handful of variables
# ============================================================

class SolutionTwoPointers:
    def trap(self, height: List[int]) -> int:
        n = len(height)
        max_left  = height[0]       # tallest wall seen from the left so far
        max_right = height[n - 1]   # tallest wall seen from the right so far
        l, r = 0, n - 1
        total = 0

        while l < r:
            if max_left < max_right:
                # Left wall is the bottleneck → safe to process left side
                l += 1
                curr = min(max_left, max_right) - height[l]  # water at bar l
                max_left = max(max_left, height[l])           # update running max
            else:
                # Right wall is the bottleneck → safe to process right side
                r -= 1
                curr = min(max_left, max_right) - height[r]  # water at bar r
                max_right = max(max_right, height[r])         # update running max

            if curr > 0:
                total += curr

        return total


# ============================================================
# APPROACH 3: Stack-Based (alternative perspective)
# ============================================================
# Strategy:
#   Use a monotonic decreasing stack of indices.
#   When a taller bar is found, it can trap water with the previous bars.
#   Pop the stack and calculate the horizontal water trapped between
#   the popped bar and the new taller bar.
#
# Useful for: thinking about water trapped in horizontal layers.
#
# Time Complexity : O(n)  — each bar pushed and popped at most once
# Space Complexity: O(n)  — stack can hold up to n indices
# ============================================================

class SolutionStack:
    def trap(self, height: List[int]) -> int:
        stack = []  # stores indices; heights are non-increasing in the stack
        total = 0

        for i, h in enumerate(height):
            # Current bar is taller than the stack top → water can be trapped
            while stack and h > height[stack[-1]]:
                bottom = stack.pop()            # the "floor" of the water pocket
                if not stack:
                    break                       # no left wall → no water
                left_wall = stack[-1]
                width     = i - left_wall - 1
                bounded_height = min(height[left_wall], h) - height[bottom]
                total += width * bounded_height

            stack.append(i)

        return total


# ============================================================
# COMPLEXITY SUMMARY
# ============================================================
#
# Approach              | Time  | Space | Notes
# ----------------------|-------|-------|---------------------------
# Prefix/Suffix (fixed) | O(n)  | O(n)  | Intuitive, needs 2 arrays
# Two Pointers          | O(n)  | O(1)  | ✅ Best — no extra space
# Stack-Based           | O(n)  | O(n)  | Good for horizontal layers
#
# ============================================================


# ============================================================
# VISUAL WALKTHROUGH  height = [4, 2, 0, 3, 2, 5]
# ============================================================
#
#  5 |                 █
#  4 | █               █
#  3 | █       █       █
#  2 | █   █   █   █   █
#  1 | █   █   █   █   █
#  0 |─█───█───█───█───█───█─
#      4   2   0   3   2   5
#
#  max_left  = [0, 4, 4, 4, 4, 4]
#  max_right = [5, 5, 5, 5, 5, 0]
#  water     = [0, 2, 4, 1, 2, 0]  → total = 9
# ============================================================


# ============================================================
# EDGE CASES TO CONSIDER
# ============================================================
# 1. All bars same height    → [3,3,3,3]    → 0  (flat, no valley)
# 2. Monotonically increasing → [1,2,3,4]   → 0  (no left wall ever)
# 3. Monotonically decreasing → [4,3,2,1]   → 0  (no right wall ever)
# 4. Single valley            → [3,0,3]     → 3
# 5. Empty / single bar       → [] or [5]   → 0
# 6. Large spike in middle    → [0,5,0]     → 0  (no enclosing wall)
# ============================================================

