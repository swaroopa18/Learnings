"""
LC 904 - Fruit Into Baskets
Pattern: Sliding Window (longest subarray with at most K=2 distinct values)

PROBLEM INTUITION:
  You walk a fruit row left to right. You have exactly 2 baskets.
  Each basket holds only ONE type of fruit (unlimited quantity).
  Find the longest contiguous stretch you can pick.
  → Translate: longest subarray with at most 2 distinct values.

============================================================
SOLUTION 1 — Your Version A  (shrink by 1 each time)
============================================================
Time : O(n)   — each element added once, removed at most once
Space: O(1)   — baskets dict holds at most 3 keys momentarily

Approach: fixed single-step shrink from left.
Subtle issue: only shrinks left by 1 when window is invalid,
so it never GROWS invalid beyond size 3. Works correctly but
only moves start forward one step at a time.
"""
from typing import List
from collections import defaultdict


def totalFruit_v1(fruits: List[int]) -> int:
    baskets = {}
    start = 0
    max_fruits = 0

    for fruit in fruits:
        baskets[fruit] = baskets.get(fruit, 0) + 1

        if len(baskets) > 2:                        # window invalid
            baskets[fruits[start]] -= 1
            if baskets[fruits[start]] == 0:
                del baskets[fruits[start]]
            start += 1

        max_fruits = max(max_fruits, sum(baskets.values()))

    return max_fruits


"""
============================================================
SOLUTION 2 — Your Version B  (inner while loop shrink)
============================================================
Time : O(n)   — amortised; each element processed twice at most
Space: O(1)   — at most 3 keys in baskets at once

Approach: expand end greedily; when window breaks (>2 types),
shrink start in a while loop until valid again.
Using (end - start + 1) instead of sum(baskets.values()) is
a nice O(1) window-size calculation — good catch!

Minor note: `len(baskets.values())` → prefer `len(baskets)` 
(same result, avoids creating a view object unnecessarily).
"""
def totalFruit_v2(fruits: List[int]) -> int:
    baskets = {}
    start = 0
    max_fruits = 0

    for end, fruit in enumerate(fruits):
        baskets[fruit] = baskets.get(fruit, 0) + 1

        while len(baskets) > 2:                     # shrink until valid
            baskets[fruits[start]] -= 1
            if baskets[fruits[start]] == 0:
                del baskets[fruits[start]]
            start += 1

        max_fruits = max(max_fruits, end - start + 1)

    return max_fruits


"""
============================================================
SOLUTION 3 — Cleaner Version B  (tiny style improvements)
============================================================
Time : O(n)
Space: O(1)

Changes from your V2:
  • len(baskets) instead of len(baskets.values())
  • defaultdict(int) removes the .get() boilerplate
  • one fewer mental hop when reading the shrink step
"""
def totalFruit_v3_clean(fruits: List[int]) -> int:
    baskets: dict[int, int] = defaultdict(int)
    start = 0
    max_fruits = 0

    for end, fruit in enumerate(fruits):
        baskets[fruit] += 1

        while len(baskets) > 2:
            left_fruit = fruits[start]
            baskets[left_fruit] -= 1
            if baskets[left_fruit] == 0:
                del baskets[left_fruit]
            start += 1

        max_fruits = max(max_fruits, end - start + 1)

    return max_fruits


"""
============================================================
SOLUTION 4 — Generalised: at most K distinct types
============================================================
Time : O(n)
Space: O(k)   — baskets holds at most k+1 keys momentarily

This is the "boss mode" version. The problem fixes k=2, but
interviews often follow up: "what if you had k baskets?"
Just parameterise and you're done.
"""
def totalFruit_k_baskets(fruits: List[int], k: int = 2) -> int:
    baskets: dict[int, int] = defaultdict(int)
    start = 0
    max_fruits = 0

    for end, fruit in enumerate(fruits):
        baskets[fruit] += 1

        while len(baskets) > k:
            left_fruit = fruits[start]
            baskets[left_fruit] -= 1
            if baskets[left_fruit] == 0:
                del baskets[left_fruit]
            start += 1

        max_fruits = max(max_fruits, end - start + 1)

    return max_fruits


"""
============================================================
SOLUTION 5 — Most Pythonic  (Counter + sliding window)
============================================================
Time : O(n)
Space: O(1)

Uses collections.Counter which already handles the zero-cleanup
via subtraction — Counter drops keys that reach 0 automatically
when you use subtract() + manual cleanup, but here we keep it
explicit for clarity. The real win is readability.
"""
from collections import Counter

def totalFruit_pythonic(fruits: List[int]) -> int:
    window = Counter()
    start = 0
    max_fruits = 0

    for end, fruit in enumerate(fruits):
        window[fruit] += 1

        while len(window) > 2:
            window[fruits[start]] -= 1
            if window[fruits[start]] == 0:
                del window[fruits[start]]
            start += 1

        max_fruits = max(max_fruits, end - start + 1)

    return max_fruits


"""
============================================================
COMPLEXITY CHEAT SHEET
============================================================

                  Time      Space     Notes
  ─────────────────────────────────────────────────────────
  V1 (your A)   O(n)      O(1)      single-step shrink; correct
  V2 (your B)   O(n)*     O(1)      while-loop shrink; cleaner
  V3 clean      O(n)*     O(1)      same logic, neater syntax
  V4 k-baskets  O(n)*     O(k)      interview follow-up ready
  V5 pythonic   O(n)*     O(1)      Counter, most readable
  ─────────────────────────────────────────────────────────
  * amortised — start pointer moves right at most n times total
    across ALL iterations, so inner while = O(n) overall

WHY NOT O(n²)?
  It looks like a nested loop, but think about the `start`
  pointer: it only ever moves RIGHT, never resets. So across
  the entire run, the while loop body executes at most n times
  total — same as the outer for loop. Total work = O(2n) = O(n).

SPACE IS O(1) (not O(n)):
  The baskets dict holds at most 3 keys at any moment (2 valid
  types + 1 newcomer before shrink). That's a constant, no
  matter how large the input array is.

PATTERN TO REMEMBER:
  "Longest subarray with at most K distinct values"
  = sliding window + frequency map + shrink-from-left
  Same skeleton applies to: LC 340, LC 159, LC 3, LC 992.
"""


# ── quick smoke test ──────────────────────────────────────
if __name__ == "__main__":
    cases = [
        ([1, 2, 1],          3),
        ([0, 1, 2, 2],       3),
        ([1, 2, 3, 2, 2],    4),
        ([3, 3, 3, 1, 2, 1, 1, 2, 3, 3, 4], 5),
        ([1],                1),
        ([1, 1, 1, 1],       4),
    ]

    fns = [
        totalFruit_v1,
        totalFruit_v2,
        totalFruit_v3_clean,
        lambda f: totalFruit_k_baskets(f, k=2),
        totalFruit_pythonic,
    ]

    all_pass = True
    for fruits, expected in cases:
        for fn in fns:
            result = fn(fruits)
            if result != expected:
                print(f"FAIL  {fn.__name__}({fruits}) → {result}, expected {expected}")
                all_pass = False

    if all_pass:
        print("All tests passed ✓")