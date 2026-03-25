# ============================================================
# PROBLEM: Valid Palindrome II (LeetCode 680)
# ============================================================
# Given a string s, return True if s can be a palindrome
# after deleting AT MOST ONE character from it.
#
# Example:
#   Input:  "abca"   → Output: True  (remove 'b' or 'c')
#   Input:  "abc"    → Output: False
#   Input:  "deeee"  → Output: True  (remove one 'e')
# ============================================================


# ============================================================
# STRATEGY: Two Pointers with One Allowed Skip
# ============================================================
# Core Idea:
#   A palindrome reads the same forwards and backwards.
#   Use two pointers (left, right) moving inward.
#   - If characters match → move both pointers inward (no skip used)
#   - If characters DON'T match → we MUST use our one allowed deletion here.
#     Try skipping the LEFT character OR the RIGHT character,
#     and check if either resulting substring is a palindrome.
#   - If neither works → not a valid palindrome even with one deletion.
#
# Why this works:
#   The mismatch point is the ONLY place a deletion can help.
#   Trying both options (skip left or skip right) covers all cases.
# ============================================================


# ============================================================
# APPROACH 1: Two Pointers (Optimal)
# ============================================================
# Time Complexity : O(n) — single pass + at most one O(n) sub-check
# Space Complexity: O(1) — no extra data structures
# ============================================================

class Solution:
    def validPalindrome(self, s: str) -> bool:

        def isPalindrome(l: int, r: int) -> bool:
            # Standard palindrome check on s[l..r] using two pointers
            while l < r:
                if s[l] != s[r]:
                    return False
                l += 1
                r -= 1
            return True

        left, right = 0, len(s) - 1

        while left < right:
            if s[left] != s[right]:
                # Mismatch found — try skipping one character from either side
                # Option A: skip s[left]  → check s[left+1 .. right]
                # Option B: skip s[right] → check s[left   .. right-1]
                return isPalindrome(left + 1, right) or isPalindrome(left, right - 1)
            left += 1
            right -= 1

        return True  # No mismatch found → already a palindrome


# ============================================================
# APPROACH 2: Pythonic Slice Check (Cleaner, slight extra space)
# ============================================================
# Same algorithm, but uses string slicing instead of index helpers.
#
# Time Complexity : O(n)
# Space Complexity: O(n) — slicing creates new string copies
# ============================================================

class SolutionSlice:
    def validPalindrome(self, s: str) -> bool:

        def isPalindrome(sub: str) -> bool:
            return sub == sub[::-1]

        left, right = 0, len(s) - 1

        while left < right:
            if s[left] != s[right]:
                # Try removing either the left or right character
                return isPalindrome(s[left + 1: right + 1]) or isPalindrome(s[left: right])
            left += 1
            right -= 1

        return True


# ============================================================
# APPROACH 3: Recursive (Intuitive but not recommended for large n)
# ============================================================
# Time Complexity : O(n) but with recursive call overhead
# Space Complexity: O(n) — call stack depth
# Not preferred: Python has a default recursion limit of ~1000
# ============================================================

class SolutionRecursive:
    def validPalindrome(self, s: str) -> bool:

        def helper(l: int, r: int, skips_left: int) -> bool:
            while l < r:
                if s[l] != s[r]:
                    if skips_left == 0:
                        return False
                    # Try both deletions with skips reduced to 0
                    return helper(l + 1, r, 0) or helper(l, r - 1, 0)
                l += 1
                r -= 1
            return True

        return helper(0, len(s) - 1, skips_left=1)


# ============================================================
# COMPLEXITY SUMMARY
# ============================================================
#
# Approach             | Time  | Space | Notes
# ---------------------|-------|-------|----------------------
# Two Pointers         | O(n)  | O(1)  | ✅ Best overall
# Pythonic Slice       | O(n)  | O(n)  | Clean but uses memory
# Recursive            | O(n)  | O(n)  | Stack overflow risk
#
# ============================================================


# ============================================================
# EDGE CASES TO CONSIDER
# ============================================================
# 1. Already a palindrome        → "racecar"  → True  (no deletion needed)
# 2. Single character            → "a"        → True
# 3. Two different characters    → "ab"       → True  (delete one)
# 4. Requires exact one deletion → "abca"     → True
# 5. Needs more than one skip    → "abcdef"   → False
# 6. All same characters         → "aaaa"     → True
# ============================================================