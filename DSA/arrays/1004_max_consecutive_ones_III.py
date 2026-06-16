# ============================================================
# LC 1004 - Max Consecutive Ones III
# ALL VARIANTS SIDE BY SIDE
# ============================================================
# Same O(n) time, O(1) space across all versions.
# The difference is only in STYLE and READABILITY.
# Pick the one that clicks best in your head during interviews.
# ============================================================

from typing import List

# ============================================================
# VARIANT 1: Track ones (your current solution)
# ============================================================
# STYLE: Count what you WANT (1s), derive cost from it
# FORMULA: zeros_in_window = window_size - ones
#
# Mental model: "I know how many good players I have,
#                so bad players = total - good"

class V1_TrackOnes:
    def longestOnes(self, nums: List[int], k: int) -> int:
        start, ones, max_len = 0, 0, 0

        for end, num in enumerate(nums):
            ones += num                            # num is 0 or 1, elegant!

            while end - start + 1 - ones > k:     # zeros > k → shrink
                ones -= nums[start]
                start += 1

            max_len = max(max_len, end - start + 1)

        return max_len

# ✅ Pros: mirrors LC 424 exactly (ones ↔ max_freq). Great pattern recognition.
# ❌ Cons: cost formula (window_size - ones) feels indirect to some people.


# ============================================================
# VARIANT 2: Track zeros (flipped perspective)
# ============================================================
# STYLE: Count what you SPEND (0s directly)
# FORMULA: if zeros > k → shrink
#
# Mental model: "I have a k-token budget.
#                Every 0 I include spends one token."

class V2_TrackZeros:
    def longestOnes(self, nums: List[int], k: int) -> int:
        start, zeros, max_len = 0, 0, 0

        for end, num in enumerate(nums):
            if num == 0:
                zeros += 1                  # spending a token

            while zeros > k:               # over budget → shrink
                if nums[start] == 0:
                    zeros -= 1             # refund a token
                start += 1

            max_len = max(max_len, end - start + 1)

        return max_len

# ✅ Pros: condition (zeros > k) reads like plain English. Very beginner-friendly.
# ❌ Cons: needs explicit if-check when shrinking. Slightly more verbose.


# ============================================================
# VARIANT 3: if instead of while (no re-shrink loop)
# ============================================================
# STYLE: Never shrink MORE than 1 step per iteration
# KEY INSIGHT: window never needs to shrink by more than 1
#              because end only moves 1 step at a time.
#              So while → if is safe here!
#
# Mental model: "If the bus gets too full by 1 person,
#                just drop 1 from the back. Never more."

class V3_IfShrink:
    def longestOnes(self, nums: List[int], k: int) -> int:
        start, ones, max_len = 0, 0, 0

        for end, num in enumerate(nums):
            ones += num

            if end - start + 1 - ones > k:    # ← if, not while!
                ones -= nums[start]
                start += 1

            max_len = max(max_len, end - start + 1)

        return max_len

# ✅ Pros: fastest in practice (no inner loop). Very clean.
# ✅ Window size never shrinks below best seen — same watermark idea as LC 424!
# ❌ Cons: subtle — only works because end moves by 1 each step.
#          Using while is safer habit for general sliding window problems.
# 💡 Note: max_len = end - start + 1 always equals the current window size,
#           which never shrinks → so max() is technically optional here,
#           but keep it for clarity.


# ============================================================
# VARIANT 4: Deque-based (track zero indices)
# ============================================================
# STYLE: Store positions of 0s, use them to jump start pointer
# FORMULA: if we've seen more than k zeros,
#           jump start to just after the oldest zero
#
# Mental model: "Keep a waitlist of zero positions.
#                When budget runs out, remove the oldest zero
#                from the waitlist and move the bus door past it."

from collections import deque

class V4_Deque:
    def longestOnes(self, nums: List[int], k: int) -> int:
        zero_positions = deque()   # stores indices of 0s in current window
        start, max_len = 0, 0

        for end, num in enumerate(nums):
            if num == 0:
                zero_positions.append(end)

            if len(zero_positions) > k:          # too many zeros
                start = zero_positions.popleft() + 1   # jump past oldest 0

            max_len = max(max_len, end - start + 1)

        return max_len

# ✅ Pros: start pointer jumps directly — no sliding one by one.
#          Very readable: "pop oldest zero, start from next position."
# ❌ Cons: O(k) space for the deque. Not O(1) anymore.
#          Overkill for this problem, but great for understanding.


# ============================================================
# COMPARISON TABLE
# ============================================================
#
#  Variant        What you track   Shrink   Space   Best for...
#  ───────────── ──────────────── ──────── ─────── ─────────────────────────
#  V1 TrackOnes  ones count        while    O(1)   LC 424 pattern recognition
#  V2 TrackZeros zeros count       while    O(1)   Plain English readability
#  V3 IfShrink   ones count        if       O(1)   Clean / interview-friendly
#  V4 Deque      zero indices      if       O(k)   Intuitive jumping logic
#
# ============================================================
# WHICH ONE SHOULD YOU USE?
# ============================================================
#
#  In an interview:     → V3 (if-shrink). Cleanest, fastest, easiest to explain.
#  For pattern memory:  → V1 (track ones). Directly mirrors LC 424.
#  For beginners:       → V2 (track zeros). Reads like plain English.
#  For understanding:   → V4 (deque). Most visual, easiest to trace.
#
# ============================================================
# QUICK TEST — all variants should give same output
# ============================================================
if __name__ == "__main__":
    tests = [
        ([1,1,1,0,0,0,1,1,1,1,0], 2, 6),
        ([0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], 3, 10),
        ([1,1,1], 0, 3),
        ([0,0,0], 0, 0),
        ([0,0,0], 3, 3),
    ]

    variants = [
        ("V1 TrackOnes",  V1_TrackOnes()),
        ("V2 TrackZeros", V2_TrackZeros()),
        ("V3 IfShrink",   V3_IfShrink()),
        ("V4 Deque",      V4_Deque()),
    ]

    for nums, k, expected in tests:
        print(f"\nnums={nums}, k={k}, expected={expected}")
        for name, sol in variants:
            result = sol.longestOnes(nums, k)
            status = "✅" if result == expected else "❌"
            print(f"  {status} {name}: {result}")