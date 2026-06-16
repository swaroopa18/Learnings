# ============================================================
# LC 424 - Longest Repeating Character Replacement
# ============================================================
# PROBLEM:
#   Given string s and int k, you can replace at most k characters.
#   Return the length of the longest substring with all same characters
#   after at most k replacements.
#
# KEY INSIGHT (the one thing to tattoo on your brain):
#   A window is VALID if:
#       (window_size - max_freq_in_window) <= k
#   i.e. the number of "non-dominant" chars we need to replace <= k
# ============================================================


# ============================================================
# APPROACH 1: Sliding Window (Optimal) — O(n) time, O(1) space
# ============================================================
# MENTAL MODEL:
#   Think of the window like a bus.
#   - max_freq = the most popular passenger type
#   - Everyone else needs a "replacement seat" (costs 1 k each)
#   - If the cost > k, shrink the bus from the front
#
# WHY max_freq NEVER DECREASES:
#   This is the trickiest part. When we shrink the window,
#   we don't recompute max_freq downward. Why?
#   Because we only care about windows LARGER than what we've
#   already seen. A smaller max_freq would only produce a
#   smaller or equal window — not useful.
#   So max_freq is a "historical high watermark", not the live max.

class Solution:
    def characterReplacement_sliding_window(self, s: str, k: int) -> int:
        window = {}
        max_freq = 0   # highest freq ever seen in any window (watermark!)
        max_len = 0
        start = 0

        for end, char in enumerate(s):
            window[char] = window.get(char, 0) + 1
            max_freq = max(max_freq, window[char])  # only goes UP

            # cost = chars we need to replace = window_size - max_freq
            while (end - start + 1) - max_freq > k:
                window[s[start]] -= 1
                start += 1
                # NOTE: we do NOT update max_freq downward here — intentional!

            max_len = max(max_len, end - start + 1)

        return max_len

# Time:  O(n)
# Space: O(1) — window has at most 26 keys (only uppercase letters)


# ============================================================
# APPROACH 2: Sliding Window — Strict / Recalculate max_freq
# ============================================================
# MENTAL MODEL: Same bus, but now we actually recount passengers
#               every time someone gets off.
#
# WHEN TO USE THIS VERSION:
#   If the problem allowed lowercase + uppercase + digits, the
#   "never decrease max_freq" trick still works for correctness,
#   but if you're uncomfortable with it in an interview, this
#   strict version is easier to reason about.
#
# TRADE-OFF:
#   Each shrink step recalculates max(window.values()) → O(26) = O(1)
#   Still O(n) overall, just with a bigger constant.

class Solution2:
    def characterReplacement_strict(self, s: str, k: int) -> int:
        window = {}
        max_len = 0
        start = 0

        for end, char in enumerate(s):
            window[char] = window.get(char, 0) + 1

            # Recompute max_freq honestly every step
            max_freq = max(window.values())

            while (end - start + 1) - max_freq > k:
                window[s[start]] -= 1
                if window[s[start]] == 0:
                    del window[s[start]]
                start += 1
                max_freq = max(window.values()) if window else 0

            max_len = max(max_len, end - start + 1)

        return max_len

# Time:  O(n * 26) = O(n)
# Space: O(1)


# ============================================================
# APPROACH 3: Brute Force — O(n^2) time
# ============================================================
# MENTAL MODEL:
#   For each character type (A-Z), try every possible starting
#   position and greedily extend the window as long as we can
#   replace non-matching chars using our k budget.
#
# WHY THIS IS FLAWED (your original approach's problem):
#   Your Solution 2 above only tracks ONE character type at a time
#   from position i — so "AABABBA" with k=1, starting at index 0,
#   might find a long run of A's but miss that a B-dominant window
#   from index 3 could be even longer.
#   The fix: iterate over ALL 26 characters as the "dominant" one.

class Solution3:
    def characterReplacement_brute(self, s: str, k: int) -> int:
        max_len = 0

        for target_char in set(s):           # try each character as dominant
            budget = k
            count = 0
            start = 0

            for end in range(len(s)):
                if s[end] == target_char:
                    count += 1               # free — it's our target
                elif budget > 0:
                    budget -= 1             # pay 1 replacement
                    count += 1
                else:
                    # window is broken — slide start forward
                    # until we free up budget or hit another target_char
                    while start <= end and s[start] != target_char:
                        budget += 1
                        start += 1
                    start += 1              # skip the target_char at start too
                    # count stays same — we lost one and gained one

            max_len = max(max_len, count)   # count = end - start + 1 equivalent

        return max_len

# Time:  O(26 * n) = O(n) — surprisingly, but with high constant
# Space: O(1)
# NOTE: This approach is harder to get exactly right. Stick to Approach 1.


# ============================================================
# CHEAT SHEET — When to use what
# ============================================================
#
#  Approach          Time    Space   Use when...
#  ─────────────── ──────── ─────── ──────────────────────────────────
#  Sliding Window  O(n)     O(1)    Always. This is THE answer.
#  (watermark)
#
#  Strict Recalc   O(n)     O(1)    When you want to reason step-by-step
#                                   without the "watermark trick"
#
#  Brute Force     O(26n)   O(1)    Only for understanding / debugging
#
# ============================================================
# COMMON BUGS TO WATCH OUT FOR
# ============================================================
#
# Bug 1: Forgetting that max_freq is a watermark, not live max
#   → The window can only grow if we beat the current max_freq.
#     This is what makes the O(n) trick correct.
#
# Bug 2: Recalculating max from scratch after shrink inside while loop
#   → Expensive and usually unnecessary. Only do it in strict mode.
#
# Bug 3: Off-by-one in window size
#   → window_size = end - start + 1, NOT end - start
#
# Bug 4 (your original code): Only checking one char as dominant per i
#   → You'd miss cases where a different char becomes dominant later.
#
# ============================================================
# SIMILAR PROBLEMS (same pattern, same key insight!)
# ============================================================
#   - LC 1004: Max Consecutive Ones III  (k zeros → k replacements)
#   - LC 1208: Get Equal Substrings Within Budget
#   - LC 2024: Maximize the Confusion of an Exam
#
# The pattern is always:
#   valid_window = some_cost_function(window) <= k
