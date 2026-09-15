# ============================================================
# LC 1004 - Max Consecutive Ones III
# ALL VARIANTS SIDE BY SIDE
# ============================================================
# Same O(n) time, O(1) space across all versions.
# The difference is only in STYLE and READABILITY.
# Pick the one that clicks best in your head during interviews.
# ============================================================

from typing import List
from collections import deque

# ============================================================
# VARIANT 1: Track ones
# ============================================================
# STYLE: Count what you WANT (1s), derive cost from it
#
# FORMULA:
#   zeros_in_window = window_size - ones
#
# Mental model:
#   "I know how many good players I have,
#    so bad players = total - good."
#
# PATTERN:
#   Very similar to LC 424 (Longest Repeating Character
#   Replacement):
#
#       window_size - max_freq <= k
#
# Here:
#
#       window_size - ones <= k
#
# ============================================================

class V1_TrackOnes:
    def longestOnes(self, nums: List[int], k: int) -> int:
        start, ones, max_len = 0, 0, 0

        for end, num in enumerate(nums):
            ones += num

            while end - start + 1 - ones > k:
                ones -= nums[start]
                start += 1

            max_len = max(max_len, end - start + 1)

        return max_len


# ============================================================
# VARIANT 2: Track zeros
# ============================================================
# STYLE: Count what you SPEND (0s directly)
#
# FORMULA:
#   zeros <= k
#
# Mental model:
#   "I have a k-token budget.
#    Every 0 I include spends one token."
#
# ============================================================

class V2_TrackZeros:
    def longestOnes(self, nums: List[int], k: int) -> int:
        start, zeros, max_len = 0, 0, 0

        for end, num in enumerate(nums):
            if num == 0:
                zeros += 1

            while zeros > k:
                if nums[start] == 0:
                    zeros -= 1
                start += 1

            max_len = max(max_len, end - start + 1)

        return max_len


# ============================================================
# VARIANT 3: if instead of while
# ============================================================
# STYLE: Never shrink MORE than 1 step per iteration
#
# KEY INSIGHT:
#   end moves exactly one step at a time.
#
# Therefore, when the new element makes the window invalid,
# we only need to move start forward by one.
#
# Mental model:
#   "The window only gets one person bigger at a time.
#    If it becomes invalid, remove one person."
#
# IMPORTANT:
#   This is a specialized optimization for this problem.
#   `while` is the safer general sliding-window habit.
#
# ============================================================

class V3_IfShrink:
    def longestOnes(self, nums: List[int], k: int) -> int:
        start, ones, max_len = 0, 0, 0

        for end, num in enumerate(nums):
            ones += num

            if end - start + 1 - ones > k:
                ones -= nums[start]
                start += 1

            max_len = max(max_len, end - start + 1)

        return max_len


# ============================================================
# VARIANT 4: Deque-based
# ============================================================
# STYLE: Store positions of 0s
#
# FORMULA:
#   If we've seen more than k zeros,
#   jump start to just after the oldest zero.
#
# Mental model:
#   "Keep a waitlist of zero positions.
#    When the budget runs out, remove the oldest zero
#    and move the door past it."
#
# SPACE:
#   O(k)
#
# ============================================================

class V4_Deque:
    def longestOnes(self, nums: List[int], k: int) -> int:
        zero_positions = deque()

        start, max_len = 0, 0

        for end, num in enumerate(nums):
            if num == 0:
                zero_positions.append(end)

            if len(zero_positions) > k:
                start = zero_positions.popleft() + 1

            max_len = max(max_len, end - start + 1)

        return max_len


# ============================================================
# VARIANT 5: Track ones explicitly + zero budget
# ============================================================
# STYLE:
#   Explicitly maintain:
#
#       count = number of 1s in current window
#       zeros = number of 0s in current window
#
# KEY IDEA:
#   When a new 0 arrives:
#
#       If zeros == k:
#           shrink first to make room
#
#       Then add the new 0.
#
# The answer is directly:
#
#       count = number of 1s in current valid window
#
# Mental model:
#   "I'm trying to maximize the number of 1s.
#    I can afford at most k zeros.
#    When another zero arrives, make room before adding it."
#
# IMPORTANT:
#   Use `zeros == k`, NOT `zeros >= k`.
#
# Why?
#   We're about to add a new zero.
#   If we already have k zeros, we must free one slot first.
#
# This also handles k = 0 correctly.
#
# ============================================================

class V5_TrackOnesExplicit:
    def longestOnes(self, nums: List[int], k: int) -> int:
        start = 0
        max_count, count, zeros = 0, 0, 0

        for i, num in enumerate(nums):

            if num == 1:
                count += 1

            else:
                # We are about to add another 0.
                # If the zero budget is already full,
                # shrink until one zero slot is available.
                while zeros == k:
                    if nums[start] == 0:
                        zeros -= 1
                    else:
                        count -= 1

                    start += 1

                zeros += 1
                count += 1

            max_count = max(max_count, count)

        return max_count


# ============================================================
# COMPARISON TABLE
# ============================================================
#
#  Variant        Tracks             Shrink   Space   Best for...
#  ─────────────  ─────────────────  ───────  ──────  ─────────────────────
#  V1             ones               while    O(1)    LC 424 pattern
#  V2             zeros              while    O(1)    Plain English
#  V3             ones               if       O(1)    Clean optimization
#  V4             zero indices       if       O(k)    Visual/jump logic
#  V5             ones + zeros       while    O(1)    Explicit ones count
#
#
# ANSWER REPRESENTATION:
#
#  V1 → window length
#  V2 → window length
#  V3 → window length
#  V4 → window length
#  V5 → number of 1s
#
# ============================================================


# ============================================================
# WHICH ONE SHOULD YOU USE?
# ============================================================
#
# In an interview:
#   → V3
#      Cleanest and very concise.
#
# For pattern memory:
#   → V1
#      Mirrors LC 424 directly.
#
# For beginners:
#   → V2
#      `zeros > k` reads like plain English.
#
# For understanding the "jump":
#   → V4
#      Very visual, but uses O(k) space.
#
# For explicitly tracking the number of 1s:
#   → V5
#      `count` directly represents the answer.
#
# Overall recommendation:
#   V1 or V3
#
# ============================================================