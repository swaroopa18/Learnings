# ============================================================
# Problem: Permutation in String (LeetCode 567)
# Given s1 and s2, return True if any permutation of s1
# is a substring of s2.
# ============================================================


# ============================================================
# Approach 1: Sliding Window with Frequency Maps (OPTIMAL)
# ------------------------------------------------------------
# Strategy:
#   - Build a frequency map for s1.
#   - Build a frequency map for the first window of s2
#     (of length equal to s1).
#   - Slide the window across s2 one character at a time:
#       * Add the new right character.
#       * Remove the old left character (delete key if count hits 0).
#       * Compare maps — if equal, a permutation is found.
#
# Why delete keys at 0?
#   Keeping zero-count keys would cause false mismatches
#   when comparing dicts (e.g., {'a': 0} != {}).
#
# Note: The map comparison BEFORE sliding handles the first window.
#       The final `return s1_map == s2_map` handles the last window,
#       which is never checked inside the loop body.
#
# Time Complexity : O(n)  — n = len(s2)
#                   Each character is added/removed at most once.
#                   Dict comparison is O(1) — at most 26 keys.
# Space Complexity: O(1)  — maps hold at most 26 entries (a–z).
#
# Best approach for interviews and production.
# ============================================================

class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        s1_len = len(s1)

        # Frequency map for s1
        s1_map = {}
        for char in s1:
            s1_map[char] = s1_map.get(char, 0) + 1

        # Frequency map for the first window of s2
        s2_map = {}
        for char in s2[:s1_len]:
            s2_map[char] = s2_map.get(char, 0) + 1

        start, l2 = 0, s1_len
        while l2 < len(s2):
            if s1_map == s2_map:   # Check current window before sliding
                return True
            # Remove leftmost character of old window
            s2_map[s2[start]] = s2_map.get(s2[start], 0) - 1
            if s2_map[s2[start]] == 0:
                del s2_map[s2[start]]   # Avoid zero-count key mismatches
            # Add new rightmost character
            s2_map[s2[l2]] = s2_map.get(s2[l2], 0) + 1
            l2 += 1
            start += 1

        return s1_map == s2_map   # Check the final window


# ============================================================
# Approach 2: Sliding Window with Sorting (SUBOPTIMAL)
# ------------------------------------------------------------
# Strategy:
#   - Sort s1 once.
#   - For each position in s2, sort the current window slice
#     and compare it to sorted s1.
#
# Why it's worse:
#   - Sorting a window of length k costs O(k log k).
#   - This is repeated for every window (~n times).
#   - Total: O(n * k log k) vs O(n) for Approach 1.
#
# Code smell:
#   - `str(sorted(...)) == str(s1)` converts lists to strings
#     for comparison — unnecessary overhead.
#   - Cleaner equivalent: sorted(s2[l2:l2+s1_len]) == s1
#     (s1 is already sorted at the top of the function).
#
# Time Complexity : O(n * k log k) — n = len(s2), k = len(s1)
# Space Complexity: O(k) — for the sorted window slice each step
#
# Acceptable for very short strings; avoid for large inputs.
# ============================================================

class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        s1 = sorted(list(s1))   # Sort s1 once — O(k log k)
        s2 = list(s2)
        l2 = 0
        s1_len = len(s1)
        while l2 < len(s2) - s1_len + 1:
            # Sort current window and compare — O(k log k) per iteration
            if str(s1) == str(sorted(s2[l2: l2 + s1_len])):
                return True
            l2 += 1
        return False


# ============================================================
# Approach 3: Sliding Window with Match Counter (CLEANEST O(n))
# ------------------------------------------------------------
# Strategy:
#   - Use a single array of size 26 to track the DIFFERENCE
#     in character counts between s1 and the current window.
#       count[i] > 0  →  s1 has more of character i than window
#       count[i] < 0  →  window has more of character i than s1
#       count[i] == 0 →  balanced for character i
#   - Track `matches`: number of characters where count[i] == 0.
#     When matches == 26, all characters are balanced → permutation found.
#   - On each slide:
#       * Adding new right char: decrement count; update matches.
#       * Removing old left char: increment count; update matches.
#
# Why this is cleaner than Approach 1:
#   - No dict comparison on every step (O(26) implicitly in Approach 1).
#   - A single integer `matches` tells us instantly if we have a hit.
#   - No key deletion bookkeeping needed.
#   - Uses a fixed array instead of dicts — better cache performance.
#
# Time Complexity : O(n)  — n = len(s2), same as Approach 1
# Space Complexity: O(1)  — fixed array of 26 integers
#
# Preferred in interviews for its clarity and constant-factor efficiency.
# ============================================================

class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2):
            return False

        # count[i] = freq of char i in s1 minus freq in current window
        count = [0] * 26
        for i in range(len(s1)):
            count[ord(s1[i]) - ord('a')] += 1   # s1 contributes +1
            count[ord(s2[i]) - ord('a')] -= 1   # window contributes -1

        # matches = number of characters that are perfectly balanced
        matches = sum(1 for c in count if c == 0)

        left = 0
        for right in range(len(s1), len(s2)):
            if matches == 26:
                return True

            # Add new right character into window
            idx = ord(s2[right]) - ord('a')
            if count[idx] == 0:
                matches -= 1        # Was balanced, now going negative
            count[idx] -= 1
            if count[idx] == 0:
                matches += 1        # Now balanced again

            # Remove old left character from window
            idx = ord(s2[left]) - ord('a')
            if count[idx] == 0:
                matches -= 1        # Was balanced, now going positive
            count[idx] += 1
            if count[idx] == 0:
                matches += 1        # Now balanced again

            left += 1

        return matches == 26        # Check the final window


# ============================================================
# Approach 4: Sliding Window with Single Difference Map
# ------------------------------------------------------------
# Strategy:
#   - Use ONE map (counter_map) initialized from s1 with positive counts.
#   - Subtract the first window of s2 from that same map.
#     Map now holds the NET difference: positive = s1 has more,
#     negative = window has more, zero = balanced.
#   - Only characters in s1 are tracked — characters exclusive to s2
#     are simply ignored (the `if char in counter_map` guards).
#   - Slide the window: undo the left char (+1), apply the right char (-1).
#   - If all values in the map are 0, a permutation is found.
#
# How it differs from Approach 1 (two maps):
#   - Approach 1 keeps two separate maps and checks equality.
#   - This approach merges them into one difference map and checks
#     all-zeros — same idea, half the space, slightly cleaner reads.
#
# How it differs from Approach 3 (match counter):
#   - Approach 3 uses a fixed array + integer `matches` for O(1) check.
#   - This approach uses a dict + `all(v == 0 ...)` which is O(k) per
#     step (k = unique chars in s1, at most 26) — asymptotically the
#     same but with slightly more overhead than a single integer check.
#
# Subtle correctness point:
#   - Characters in s2 but NOT in s1 are skipped entirely.
#     This is safe because their absence from the map means they can
#     never affect whether all values are zero.
#   - Zero values are NOT deleted here (unlike Approach 1), so
#     are_frequencies_zeros() must tolerate them — and it does via
#     `all(value == 0 ...)`.
#
# Time Complexity : O(n)  — n = len(s2)
#                   are_frequencies_zeros is O(k), k ≤ 26 → O(1)
# Space Complexity: O(k)  — k = unique chars in s1, at most 26 → O(1)
# ============================================================

class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        def are_frequencies_zeros(hmap):
            return all(value == 0 for value in hmap.values())

        s1_len = len(s1)

        # Build difference map from s1 (positive counts)
        counter_map = {}
        for char in s1:
            counter_map[char] = counter_map.get(char, 0) + 1

        # Subtract first window of s2 (only chars present in s1)
        for char in s2[:s1_len]:
            if char in counter_map:
                counter_map[char] = counter_map.get(char, 0) - 1

        start, l2 = 0, s1_len
        while l2 < len(s2):
            if are_frequencies_zeros(counter_map):
                return True
            # Undo left char leaving window (only if it's tracked)
            if s2[start] in counter_map:
                counter_map[s2[start]] = counter_map.get(s2[start], 0) + 1
            # Apply new right char entering window (only if it's tracked)
            if s2[l2] in counter_map:
                counter_map[s2[l2]] = counter_map.get(s2[l2], 0) - 1
            l2 += 1
            start += 1

        return are_frequencies_zeros(counter_map)   # Check the final window


# ============================================================
# Comparison Summary
# ------------------------------------------------------------
#  Approach              | Time           | Space | Notes
# -----------------------|----------------|-------|----------------------
#  1. Freq Maps          | O(n)           | O(1)  | Correct & optimal
#  2. Sort Window        | O(n * k log k) | O(k)  | Simple but slow
#  3. Match Counter      | O(n)           | O(1)  | Cleanest — use this
# ------------------------------------------------------------
# Approaches 1 and 3 are both O(n) / O(1).
# Approach 3 avoids dict comparison overhead and is preferred
# in interviews for its single-integer `matches` termination check.
# ============================================================