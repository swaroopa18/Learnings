"""
LC 76 - Minimum Window Substring
=================================
Given two strings s and t, return the minimum window substring of s
such that every character in t (including duplicates) is included.
If no such substring exists, return "".

INTUITION:
----------
Think of a rubber band stretched over s.
- Stretch the RIGHT end until you've caught all chars in t.
- Squeeze the LEFT end to shrink the window as small as possible.
- The moment you lose a required char, stretch right again.
- Keep track of the smallest valid window you ever saw.

KEY TRICK - two frequency maps:
  need  = how many of each char t requires
  have  = how many of each char the current window has
  formed = count of unique chars in t that are FULLY satisfied

When formed == required --> valid window! Try to shrink.

EXAMPLE:
--------
s = "ADOBECODEBANC", t = "ABC"

Step-by-step (right pointer moves forward):
  right=0  'A' -> formed=1  (need A:1, have A:1 ✅)
  right=3  'B' -> formed=2  (have B:1 ✅)
  right=5  'C' -> formed=3  ALL FOUND! window="ADOBEC"
             --> shrink left: remove 'A', formed drops to 2
  ...keep going...
  right=12 Final best window = "BANC" ✅

COMPLEXITY:
-----------
Time  : O(|s| + |t|)  -- each char visited at most twice (right + left pointer)
Space : O(|s| + |t|)  -- for the two frequency maps
"""

def minWindow(s: str, t: str) -> str:
    # Edge case: empty strings
    if not s or not t:
        return ""

    # --- STEP 1: Build the 'need' map from t ---
    # need[ch] = how many times ch must appear in our window
    need = {}
    for ch in t:
        need[ch] = need.get(ch, 0) + 1

    # required = number of UNIQUE chars we need to fully satisfy
    required = len(need)

    # --- STEP 2: Sliding window setup ---
    have = {}       # frequency map of current window
    formed = 0      # how many unique chars are fully satisfied so far
    left = 0        # left pointer

    # best = (window_length, left_index, right_index)
    # start with infinity so any valid window beats it
    best = (float("inf"), 0, 0)

    # --- STEP 3: Expand right pointer ---
    for right in range(len(s)):
        ch = s[right]
        have[ch] = have.get(ch, 0) + 1

        # Check if this char just became fully satisfied
        # (only tick up when we hit EXACTLY the needed count, not more)
        if ch in need and have[ch] == need[ch]:
            formed += 1

        # --- STEP 4: Shrink from left while window is valid ---
        while formed == required:
            window_len = right - left + 1

            # Update best if this window is smaller
            if window_len < best[0]:
                best = (window_len, left, right)

            # Remove the leftmost character
            left_ch = s[left]
            have[left_ch] -= 1

            # If removing it breaks a requirement, formed drops
            if left_ch in need and have[left_ch] < need[left_ch]:
                formed -= 1

            left += 1   # shrink window from left

    # --- STEP 5: Return result ---
    if best[0] == float("inf"):
        return ""   # no valid window found
    return s[best[1]: best[2] + 1]