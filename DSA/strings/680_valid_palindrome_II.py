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
# APPROACH 1: Two Pointers (Optimal, helper function)
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
# APPROACH 1b: Two Pointers (Optimal, inlined — no helper function)
# ============================================================
# Same exact algorithm as Approach 1. The only difference is style:
# instead of calling a reusable isPalindrome(l, r) helper twice,
# the two "skip left" / "skip right" checks are written out inline
# as their own while-loops directly inside validPalindrome.
#
# Why this is worth having as a separate version:
#   - No function-call / closure overhead — everything is flat,
#     plain local variables (useful if an interviewer specifically
#     asks you to avoid nested helper functions).
#   - Slightly more verbose, but makes the "try both options" step
#     very explicit and easy to trace by eye — good for whiteboard
#     explanations.
#   - Uses `left <= right` (instead of `l < r`) as the loop guard —
#     a common alternate style since crossing pointers is also a
#     safe stopping condition.
#
# Time Complexity : O(n) — same as Approach 1
# Space Complexity: O(1) — same as Approach 1
# ============================================================

class SolutionInline:
    def validPalindrome(self, s: str) -> bool:
        l, r = 0, len(s) - 1
        left, right = False, False
        while l <= r:
            if s[l] != s[r]:
                # Option A: skip s[l] → verify s[l+1 .. r] is a palindrome
                left, right = l + 1, r
                while (left <= right) and s[left] == s[right]:
                    left += 1
                    right -= 1
                if left >= right:
                    return True

                # Option B: skip s[r] → verify s[l .. r-1] is a palindrome
                left, right = l, r - 1
                while (left <= right) and s[left] == s[right]:
                    left += 1
                    right -= 1
                if left >= right:
                    return True

                return False

            l += 1
            r -= 1
        return True


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
# ---------------------|-------|-------|----------------------------------
# Two Pointers         | O(n)  | O(1)  | ✅ Best overall, uses a helper fn
# Two Pointers (Inline) | O(n) | O(1)  | Same algorithm, no helper function
# Pythonic Slice        | O(n) | O(n)  | Clean but uses memory
# Recursive             | O(n) | O(n)  | Stack overflow risk
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


# ============================================================
# DSA BUDDY NOTE 🧠
# ============================================================
# Approach 1 and Approach 1b are the SAME idea — two pointers,
# one allowed skip at the first mismatch. Approach 1 wraps the
# "check if this range is a palindrome" logic in a helper so it
# can be reused for both the "skip left" and "skip right" cases.
# Approach 1b inlines that same check twice instead.
#
# Takeaway: when you see yourself writing the same while-loop
# twice with slightly different bounds, that's usually a sign
# you *could* extract a helper function — not that you *must*.
# Both are O(n)/O(1); pick the helper-function version for
# cleaner code, or the inline version if you want to avoid
# nested functions (e.g. some interviewers prefer flat code).
# ============================================================