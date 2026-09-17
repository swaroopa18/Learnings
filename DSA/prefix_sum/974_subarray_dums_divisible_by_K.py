"""
================================================================================
 PROBLEM: Subarray Sums Divisible by K (LeetCode 974)
================================================================================
Given: an integer array `nums` and an integer `k`.
Task: return the TOTAL COUNT of contiguous subarrays whose sum is
divisible by k (i.e. `sum % k == 0`).

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Can nums contain negative numbers? (Yes — unlike LC 523, this problem
  allows negatives, so Python's `%` behavior with negatives matters; see
  the note below)
- Is there a minimum subarray length? (No — unlike LC 523's "Continuous
  Subarray Sum," here even length-1 subarrays count if divisible by k)
- We want a COUNT, not a boolean — this changes the hash map from
  "remainder -> index" to "remainder -> frequency."
"""

# ================================================================================
# ALTERNATIVE APPROACH — Brute Force (check every subarray)
# ================================================================================
"""
### Thought Process 🧠
The most direct reading: for every starting index, extend rightward,
maintain a running sum, and count every time that sum is divisible by k.

### Idea
For each start i, walk j from i to the end, accumulating `total`. Every
time `total % k == 0`, increment the count — no early break needed since
we're counting ALL divisible subarrays, not just checking existence.

### Complexity
- TC: O(n^2) — for each of the n starts, scan up to n elements
- SC: O(1) extra

### Pros
- Directly matches the problem statement, trivial to verify.

### Cons
- Re-derives running sums from scratch for every starting index.

### Bottleneck
Same as always with this family: overlapping work across different start
indices is thrown away and redone. Ask: "does a MATH property of prefix
sums let me count matches without re-scanning?" -> Yes: same
remainder-mod-k idea as LC 523, but this time counting FREQUENCY of each
remainder instead of just its first index.
"""


def subarrays_div_by_k_brute(nums: list[int], k: int) -> int:
    n = len(nums)
    count = 0
    for i in range(n):
        total = 0
        for j in range(i, n):
            total += nums[j]
            if total % k == 0:
                count += 1
    return count


# ================================================================================
# MY APPROACH — Prefix Sum + Hash Map of (remainder -> frequency)
# ================================================================================
"""
### Idea
Same core insight as "Continuous Subarray Sum" (LC 523):
`prefix[j] % k == prefix[i] % k` implies the subarray between i and j sums
to a multiple of k. But here we want a COUNT of all such pairs, not just
"does one exist" — so the hash map tracks how many times each remainder
has appeared, not just the earliest index.

For each new prefix sum's remainder `key`: if `key` has appeared `c` times
before, that means there are exactly `c` earlier prefix sums that would
each form a valid divisible subarray when paired with the current index —
so add `c` to the running `count`. Then increment the frequency of `key`
in the map (whether it existed before or not) so future indices can pair
with THIS one too.

Seed the map with `{0: 1}` — this represents "a prefix sum of 0 occurred
once, before index 0" — so a prefix itself being divisible by k counts as
one match immediately (pairing with that pre-seeded 0).

### Why does it work?
Every PAIR of equal-remainder prefix sums corresponds to exactly one valid
subarray between them. By counting how many prior prefix sums share the
current remainder, we count exactly how many valid subarrays END at the
current index — summing this across all indices gives the total count.

### Complexity
- TC: O(n) — single pass, O(1) hash map operations per element
- SC: O(min(n, k)) — the hash map holds at most k distinct remainders

### Pros
- Optimal time — turns an O(n) "how many earlier matches" search into an
  O(1) frequency lookup.
- The `{0: 1}` seed naturally folds in prefixes that are themselves
  divisible by k, no special-casing needed.

### DSA Buddy Point 🧠
"Counting problems with prefix sums usually want a FREQUENCY map, not an
'earliest index' map — every earlier occurrence of the same remainder is
a separate valid subarray ending here, so you add the full count, not
just check existence."

### Negative Number Note ⚠️
Python's `%` operator always returns a result with the same sign as the
divisor (so for a positive k, `prefix % k` is always in `[0, k-1]`, even
if `prefix` itself is negative). This is exactly the behavior this
solution relies on — in languages where `%` can return negative results
(C++, Java), you'd need to explicitly normalize with
`((prefix % k) + k) % k` to get the same correct grouping.

### What can be improved?
Nothing — O(n) time is optimal since every element must be inspected at
least once, and O(min(n,k)) space is the minimum needed to track
remainder frequencies. This is the accepted optimal solution.
"""


def subarrays_div_by_k(nums: list[int], k: int) -> int:
    hmap = {0: 1}

    prefix, count = 0, 0
    for i, num in enumerate(nums):
        prefix += num

        key = prefix % k

        if key in hmap:
            count += hmap[key]
        hmap[key] = hmap.get(key, 0) + 1

    return count


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
SUBARRAY SUMS DIVISIBLE BY K (count all)
│
├── Brute Force
│   └── For each start, extend right, count every total % k == 0 -> O(n^2)
│
├── Bottleneck
│   └── Recomputes running sums from scratch per starting index
│
├── Key Math Insight (same as LC 523)
│   └── prefix[i] % k == prefix[j] % k  <=>  subarray between them
│       sums to a multiple of k
│
├── Twist vs. LC 523 — We Want a COUNT, Not a Boolean
│   └── Track FREQUENCY of each remainder, not just earliest index
│       -> every prior occurrence = one more valid subarray ending here
│
├── Optimization — Prefix Sum + Hash Map (remainder -> frequency)
│   ├── Seed hmap = {0: 1} to catch "prefix itself divisible by k"
│   ├── For each i: compute prefix % k
│   ├── Add hmap[key] (however many times seen before) to count
│   └── Increment hmap[key] by 1 (always, whether new or existing)
│
└── Complexity
    └── O(n) time (single pass, O(1) hash ops)
    └── O(min(n,k)) space (map holds at most k distinct remainders)
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "'Count subarrays' vs. 'does one exist' -> frequency map vs.
  earliest-index map. Same remainder-mod-k math, different bookkeeping."
- "Seed {0: 1}, not {0: -1} like LC 523's index-map — here we're counting
  occurrences, so the seed means 'one occurrence of remainder 0 before we
  start,' not 'remainder 0 first seen at index -1.'"
- "Every prior occurrence of the same remainder pairs with the current
  index to form ONE valid subarray — add the full frequency, don't just
  check membership."
- "This is the sibling of LC 560 'Subarray Sum Equals K' (count subarrays
  summing to an exact target) — same frequency-map skeleton, remainder
  matching instead of exact-value matching."
- "Python's % always returns non-negative for positive k — this solution
  quietly relies on that language behavior."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                        | Core Idea                                                | TC   | SC          | Pros                                | Cons                                    | When to Use                        |
|-------------------------------------|------------------------------------------------------------------|------|-------------|--------------------------------------------|----------------------------------------------|------------------------------------------|
| Brute Force                         | Check every subarray's sum, count matches directly                  | O(n^2)| O(1)       | Trivial to write/verify                      | Redoes overlapping sum work every start        | Baseline / correctness check only        |
| Prefix Sum + Hash Map (frequency)   | Count remainder collisions; each is one valid subarray ending here  | O(n) | O(min(n,k)) | Optimal time, elegant seed handles edge case | Requires the remainder-frequency insight upfront | Default optimal choice (your code)       |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Prefix Sum + Hash Map of frequencies (the "count" variant of
  the remainder-matching idea from LC 523; the mod-k sibling of LC 560
  "Subarray Sum Equals K").
- Go-to answer: "Track how many times each prefix-sum remainder mod k has
  occurred. Every prior occurrence of the current remainder is one more
  valid subarray ending here, so add that frequency to a running count,
  then increment the frequency for future indices. Seed with {0: 1} to
  catch prefixes that are themselves divisible by k. O(n) time,
  O(min(n,k)) space."
- Good contrast to bring up: LC 523 asks "does one exist" (needs earliest
  index + a length>=2 check), while this problem asks "how many" (needs
  full frequency counting, no length restriction) — same math, different
  hash map semantics.
- Common follow-up: "What if k could be 0?" -> Not applicable here (k is
  guaranteed nonzero in the constraints), but worth noting `% 0` would
  raise an error if it weren't guaranteed.
"""
