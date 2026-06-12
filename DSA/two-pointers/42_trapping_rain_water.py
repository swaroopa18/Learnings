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
# MY INTUITION (plain English)
# ============================================================
# Imagine you have a bunch of walls of different heights in a
# row, and it rains. Water gets trapped in the gaps between
# tall walls.
#
# The key idea:
#   At any gap, how much water sits there depends on the
#   shorter of the two tallest walls on its left and right —
#   because water spills over the shorter wall first.
#   So water at any spot = shorter surrounding wall minus
#   the height of the ground at that spot.
#
# First attempt:
#   I first went through all the walls and noted down, for
#   each spot, the tallest wall seen to its left and the
#   tallest wall seen to its right. Then I went through again
#   and used those notes to calculate the water at each spot.
#   It works, but I was carrying around two big lists of notes
#   the whole time.
#
# Better idea:
#   I don't need to write everything down first. Instead, use
#   two fingers — one starting from the left end and one from
#   the right end. Whichever finger is pointing at the shorter
#   wall, move that one inward. Why? Because when one side is
#   shorter, that side is what limits the water — no need to
#   care about what's on the other side at all. So calculate
#   the water right there on the spot and keep moving.
#   No lists needed, just two fingers walking toward each other.
# ============================================================


# ============================================================
# KEY INSIGHT (applies to ALL approaches)
# ============================================================
# Water above any bar i is determined by:
#
#   water[i] = min(max_left[i], max_right[i]) - height[i]
#
# Think of it like pouring water into a valley —
# the water level is capped by the SHORTER of the two walls.
# If this value is negative (bar taller than both walls), water[i] = 0.
# ============================================================


# ============================================================
# APPROACH 1: Prefix/Suffix Max Arrays
# ============================================================
# Strategy:
#   Pre-compute two arrays:
#     max_left[i]  = max height in height[0..i-1]   (tallest wall LEFT of i)
#     max_right[i] = max height in height[i+1..n-1] (tallest wall RIGHT of i)
#   Then apply the key insight above for each bar.
#
# Common pitfall:
#   Using max(height[:i]) inside a loop is O(n) per call → O(n²) total.
#   Fix: build max_left and max_right incrementally (running max) → O(n).
#
# Time : O(n)  — three linear passes
# Space: O(n)  — two extra arrays of size n
# ============================================================

from typing import List

class SolutionPrefixSuffix:
    def trap(self, height: List[int]) -> int:
        n = len(height)
        max_left  = [0] * n
        max_right = [0] * n

        for i in range(1, n):
            max_left[i] = max(max_left[i - 1], height[i - 1])

        for i in range(n - 2, -1, -1):
            max_right[i] = max(max_right[i + 1], height[i + 1])

        total = 0
        for i in range(n):
            water = min(max_left[i], max_right[i]) - height[i]
            if water > 0:
                total += water

        return total


# ============================================================
# APPROACH 2: Two Pointers — Optimal
# ============================================================
# Strategy:
#   Eliminate both extra arrays by observing:
#     → If max_left < max_right, the left wall is the bottleneck.
#       We don't need the exact right max — knowing it's ≥ max_left
#       is enough to compute water at the left pointer safely.
#     → Symmetrically, if max_right ≤ max_left, process the right pointer.
#
#   Move the pointer on the SHORTER side inward each step.
#
# Critical order of operations:
#   ✅  curr     = max_left - height[l]        # compute water with OLD max
#       max_left = max(max_left, height[l])    # THEN update running max
#
#   ❌  max_left = max(max_left, height[l])    # wrong: counts bar as its own wall
#       curr     = max_left - height[l]        # always 0 or negative
#
# Time : O(n)  — single pass, each element visited once
# Space: O(1)  — only a handful of variables
# ============================================================

class SolutionTwoPointers:
    def trap(self, height: List[int]) -> int:
        l, r = 0, len(height) - 1
        max_left, max_right = height[l], height[r]
        total = 0

        while l < r:
            if max_left < max_right:
                l += 1
                curr     = max_left - height[l]       # water at bar l
                max_left = max(max_left, height[l])   # update running max
            else:
                r -= 1
                curr      = max_right - height[r]     # water at bar r
                max_right = max(max_right, height[r]) # update running max

            if curr > 0:
                total += curr

        return total


# ============================================================
# APPROACH 2b: Two Pointers — Condensed variant
# ============================================================
# Same logic as above; update the max first, then subtract height.
# This works because max(max_left, height[l]) - height[l] >= 0 always,
# so the curr > 0 guard is unnecessary.
# ============================================================

class Solution:
    def trap(self, height: List[int]) -> int:
        left, right = 0, len(height) - 1
        left_max, right_max = height[left], height[right]
        output = 0

        while left < right:
            if left_max < right_max:
                left += 1
                left_max = max(left_max, height[left])
                output  += left_max - height[left]
            else:
                right -= 1
                right_max = max(right_max, height[right])
                output   += right_max - height[right]

        return output


# ============================================================
# APPROACH 3: Monotonic Stack
# ============================================================
# Strategy:
#   Maintain a stack of indices whose heights are non-increasing.
#   When a taller bar arrives at index i:
#     - Pop the top (the "floor" of a water pocket).
#     - If the stack is now empty, there's no left wall → skip.
#     - Otherwise, the new top is the left wall; i is the right wall.
#     - Compute the horizontal water trapped between the two walls.
#
#   This approach accumulates water in horizontal layers rather than
#   per-bar vertically, making it intuitive for certain problem variants.
#
# Time : O(n)  — each index pushed and popped at most once
# Space: O(n)  — stack can hold up to n indices in the worst case
# ============================================================

class SolutionStack:
    def trap(self, height: List[int]) -> int:
        stack = []   # indices; heights[stack[i]] are non-increasing
        total = 0

        for i, h in enumerate(height):
            while stack and h > height[stack[-1]]:
                bottom = stack.pop()          # floor of the water pocket
                if not stack:
                    break                     # no left wall → no water here
                left_wall      = stack[-1]
                width          = i - left_wall - 1
                bounded_height = min(height[left_wall], h) - height[bottom]
                total         += width * bounded_height

            stack.append(i)

        return total


# ============================================================
# COMPLEXITY SUMMARY
# ============================================================
#
# Approach              | Time  | Space | Notes
# ----------------------|-------|-------|------------------------------
# Prefix/Suffix (fixed) | O(n)  | O(n)  | Intuitive; needs 2 arrays
# Two Pointers          | O(n)  | O(1)  | ✅ Best — no extra space
# Stack-Based           | O(n)  | O(n)  | Useful for horizontal layers
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
#
# ============================================================


# ============================================================
# EDGE CASES
# ============================================================
#
# Case                       | Input        | Output | Reason
# ---------------------------|--------------|--------|------------------------
# All bars same height       | [3,3,3,3]    | 0      | Flat — no valley
# Monotonically increasing   | [1,2,3,4]    | 0      | No left wall ever
# Monotonically decreasing   | [4,3,2,1]    | 0      | No right wall ever
# Single valley              | [3,0,3]      | 3      | Symmetric walls
# Empty or single bar        | [] or [5]    | 0      | Nothing to trap
# Lone spike in middle       | [0,5,0]      | 0      | No enclosing walls
#
# ============================================================