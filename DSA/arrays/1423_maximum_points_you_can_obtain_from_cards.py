"""
LeetCode 1423 - Maximum Points You Can Obtain from Cards
=========================================================
Problem:
    Given an array `cardPoints` and an integer k, you can pick exactly k cards
    from either the beginning or the end of the row (any combination).
    Return the maximum score (sum) you can achieve.

Example:
    cardPoints = [1, 2, 3, 4, 5, 6, 1], k = 3
    Best pick: [4, 5, 6] → but those aren't reachable from ends directly.
    Best reachable: cardPoints[:1] + cardPoints[-2:] = [1] + [6,1] = 8
    OR cardPoints[:3] = [1,2,3] = 6
    OR cardPoints[-3:] = [6,1] → wait, k=3 so [5,6,1] = 12 ✓
    Answer: 12

Constraint reminder:
    - 1 <= cardPoints.length <= 10^5
    - 1 <= cardPoints[i] <= 10^4
    - 1 <= k <= cardPoints.length
"""

from typing import List


# =============================================================================
# APPROACH 1 — Naive Brute Force (Your First Version, Buggy)
# =============================================================================
# BUG: range(k) gives i in [0, k-1], so the case i=k (all from the left)
# is never evaluated. This causes the answer to be wrong when the optimal
# pick is entirely from the left side.
#
# Example where it fails:
#   cardPoints = [9, 7, 7, 9, 7, 7, 9], k = 7
#   The full sum is the answer, but i never reaches k, so it's missed.
#
# Time Complexity : O(k^2) — for each of the k iterations, sum() is O(k)
# Space Complexity: O(1)   — no extra space beyond a few variables

class SolutionV1_Buggy:
    def maxScore(self, cardPoints: List[int], k: int) -> int:
        max_points = 0
        for i in range(k):                                    # BUG: should be range(k+1)
            points = sum(cardPoints[:i]) + sum(cardPoints[i - k:])
            max_points = max(points, max_points)
        return max_points


# =============================================================================
# APPROACH 2 — Fixed Brute Force with Explicit Edge Cases (Your Second Version)
# =============================================================================
# This fixes the off-by-one bug by using range(k+1) and handling i=0 and i=k
# as special cases to avoid the ambiguous slice cardPoints[0 - k:] == cardPoints[-k:]
# when i=0 (which Python resolves as a right-side slice, giving wrong logic).
#
# Note: The special-casing for i=0 and i=k is correct but unnecessary if you
# just write: sum(cardPoints[:i]) + sum(cardPoints[len-k+i:])
# (see Approach 3 for the clean version).
#
# Time Complexity : O(k^2) — k+1 iterations, each sum() call is O(k)
# Space Complexity: O(1)

class SolutionV2_Fixed:
    def maxScore(self, cardPoints: List[int], k: int) -> int:
        max_points = 0
        for i in range(k + 1):                               # Fixed: k+1 so i reaches k
            if i == 0:
                points = sum(cardPoints[-k:])                # All from right
            elif i == k:
                points = sum(cardPoints[:i])                 # All from left
            else:
                points = sum(cardPoints[:i]) + sum(cardPoints[i - k:])
            max_points = max(points, max_points)
        return max_points


# =============================================================================
# APPROACH 3 — Sliding Window on the Taken Cards (Your Third / Best Version)
# =============================================================================
# Key insight:
#   Taking i cards from the left and (k-i) cards from the right is equivalent
#   to starting with all k left cards and then "sliding" one card at a time
#   from the left window to the right.
#
# Algorithm:
#   1. Start with score = sum(cardPoints[:k])  → take all k from the left.
#   2. For i in 1..k:
#        Remove cardPoints[k-i] from the window (losing a left card)
#        Add    cardPoints[n-i]  to the window   (gaining a right card)
#      This simulates: i cards from right, (k-i) cards from left.
#   3. Track the best score seen.
#
# Why this is O(n) and not O(k^2):
#   Each step does O(1) arithmetic instead of recomputing the full sum.
#
# Time Complexity : O(k)  — one pass of k+1 steps (k ≤ n, so O(n) worst case)
# Space Complexity: O(1)  — only a few integer variables

class SolutionV3_SlidingWindow:
    def maxScore(self, cardPoints: List[int], k: int) -> int:
        n = len(cardPoints)
        score = sum(cardPoints[:k])   # Initial window: all k from the left — O(k)
        best = score

        for i in range(1, k + 1):
            score = score + cardPoints[n - i] - cardPoints[k - i]
            # Add the i-th card from the right, remove the i-th card from left-end
            best = max(best, score)

        return best


# =============================================================================
# APPROACH 4 — Minimum Subarray Window (Alternative Elegant O(n) approach)
# =============================================================================
# Key insight:
#   Maximising the sum of k cards picked from both ends
#   ≡ Minimising the sum of the (n - k) cards left in the middle.
#
# Algorithm:
#   1. Compute total = sum of all cards.
#   2. Find the minimum sum subarray of length (n - k) using a sliding window.
#   3. Answer = total - min_subarray_sum.
#
# Edge case: if k == n, there are 0 cards left in the middle, so return total.
#
# Time Complexity : O(n)  — one pass for total, one pass for the window
# Space Complexity: O(1)

class SolutionV4_MinWindow:
    def maxScore(self, cardPoints: List[int], k: int) -> int:
        n = len(cardPoints)
        total = sum(cardPoints)           # O(n)

        window_size = n - k
        if window_size == 0:             # Taking all cards
            return total

        # Find minimum sum window of size (n - k)
        window_sum = sum(cardPoints[:window_size])
        min_sum = window_sum

        for i in range(window_size, n):
            window_sum += cardPoints[i] - cardPoints[i - window_size]
            min_sum = min(min_sum, window_sum)

        return total - min_sum


# =============================================================================
# APPROACH 5 — Prefix + Suffix Sums (Precomputed, most explicit / readable)
# =============================================================================
# Precompute:
#   prefix[i] = sum of first i cards      (left picks)
#   suffix[i] = sum of last i cards       (right picks)
# Then the answer is max(prefix[i] + suffix[k-i]) for i in 0..k.
#
# This makes the logic extremely transparent but uses O(n) extra space.
#
# Time Complexity : O(n)  — O(n) to build prefix/suffix, O(k) to scan
# Space Complexity: O(n)  — two arrays of length n+1

class SolutionV5_PrefixSuffix:
    def maxScore(self, cardPoints: List[int], k: int) -> int:
        n = len(cardPoints)

        prefix = [0] * (k + 1)
        for i in range(1, k + 1):
            prefix[i] = prefix[i - 1] + cardPoints[i - 1]

        suffix = [0] * (k + 1)
        for i in range(1, k + 1):
            suffix[i] = suffix[i - 1] + cardPoints[n - i]

        return max(prefix[i] + suffix[k - i] for i in range(k + 1))


# =============================================================================
# COMPLEXITY SUMMARY
# =============================================================================
# | Approach                  | Time    | Space | Notes                      |
# |---------------------------|---------|-------|----------------------------|
# | V1 - Buggy brute force    | O(k^2)  | O(1)  | Wrong answer (off-by-one)  |
# | V2 - Fixed brute force    | O(k^2)  | O(1)  | Correct but slow           |
# | V3 - Sliding window (✓)   | O(k)    | O(1)  | Best: fast & minimal space |
# | V4 - Min window (✓)       | O(n)    | O(1)  | Elegant alternative        |
# | V5 - Prefix+Suffix (✓)    | O(n)    | O(n)  | Most readable, uses space  |
#
# Recommendation: Use V3 (Sliding Window) for interviews — O(k) time, O(1)
# space, clean logic. V4 is equally good and may be more intuitive to some.
# =============================================================================