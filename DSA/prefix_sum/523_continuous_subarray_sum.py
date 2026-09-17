"""
================================================================================
 PROBLEM: Continuous Subarray Sum (LeetCode 523)
================================================================================
Given: an integer array `nums` and an integer `k`.
Task: return True if there exists a contiguous subarray of length >= 2
whose sum is a multiple of k (i.e. `sum % k == 0`), False otherwise.

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Does "multiple of k" include 0 itself? (Yes — a subarray summing to 0
  counts, since 0 % k == 0)
- Can k be 0? (LeetCode guarantees k >= 1 for this problem — confirm, since
  `% 0` would crash)
- Must the subarray length be strictly >= 2? (Yes — a single element is
  never a valid answer here, even if it's itself a multiple of k)
- Can nums contain negative numbers? (Constraints typically say
  non-negative, but the modulo-hashmap approach works either way in
  Python, since Python's `%` always returns a non-negative result for a
  positive k)
"""

# ================================================================================
# MY APPROACH #1 — Brute Force (check every subarray)
# ================================================================================
"""
### Idea
Try every possible starting index i, and for each one, extend the ending
index j rightward, maintaining a running `total`. Whenever the subarray
length is >= 2 and `total % k == 0`, we've found a match.

### Complexity
- TC: O(n^2) — for each of the n starting points, we may extend up to n
  elements before finding a match or reaching the end
- SC: O(1) extra

### Pros
- Directly implements the problem statement — trivial to verify correct.
- No modular-arithmetic insight required to write it.

### Cons
- Quadratic — re-derives the running sum from scratch for every starting
  index, redoing overlapping work.

### Bottleneck
Every different starting index recomputes sums over elements it already
summed as part of a different (earlier) starting index's scan. Ask: "is
there a property of PREFIX SUMS that could tell me, in O(1), whether some
earlier prefix sum shares a useful relationship with the current one?" ->
Yes: if two prefix sums have the SAME remainder mod k, the subarray
between them is a multiple of k (see the optimal approach below).
"""


def check_subarray_sum_brute(nums: list[int], k: int) -> bool:
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if j - i + 1 >= 2 and total % k == 0:
                return True
    return False


# ================================================================================
# MY APPROACH #2 — Prefix Sum + Hash Map of (remainder -> earliest index)
# ================================================================================
"""
### Idea
Key insight: if two prefix sums `prefix[i]` and `prefix[j]` (i < j) have
the SAME remainder when divided by k, then the sum of the subarray between
them, `prefix[j] - prefix[i]`, is exactly divisible by k. This is because:

    prefix[j] % k == prefix[i] % k
    => (prefix[j] - prefix[i]) % k == 0

So instead of tracking prefix sums directly, track prefix sums MOD k, and
remember the EARLIEST index at which each remainder was first seen (using
the earliest index maximizes the distance to any future match, giving the
best chance of satisfying the length >= 2 requirement). Seed the map with
`{0: -1}` to handle the case where a prefix itself (from index 0) is
already a multiple of k.

For each new index i, if we've seen this remainder before at index
`hmap[key]`, and the gap `i - hmap[key] >= 2`, we've found a valid
subarray. Otherwise, only store the remainder if it's NEW (never
overwrite an existing entry — keeping the earliest index is what
maximizes future match potential).

--------------------------------------------------------------------------------
### 🔰 BEGINNER-FRIENDLY WALKTHROUGH
--------------------------------------------------------------------------------
If the "prefix sum mod k" idea feels abstract, build it up slowly:

1.  **What's a prefix sum?**
    `prefix[i]` = sum of all elements from index 0 up to i.
    Example: nums = [23, 2, 4, 6, 7], prefix sums are
    [23, 25, 29, 35, 42].

2.  **Why do we care about the sum of a subarray?**
    The sum of any subarray nums[i+1 .. j] can be written as
    `prefix[j] - prefix[i]`. So instead of adding up a chunk of the
    array every time, we can get any subarray's sum by subtracting two
    prefix sums. This is the classic "prefix sum" trick used to avoid
    recomputation.

3.  **Why remainders (mod k) instead of the raw prefix sums?**
    We don't actually need to know the subarray sum itself — we only
    need to know IF it's divisible by k. A number is divisible by k
    exactly when its remainder mod k is 0. So instead of asking
    "is `prefix[j] - prefix[i]` divisible by k?", we can ask the
    equivalent, easier question: "do `prefix[j]` and `prefix[i]` leave
    the SAME remainder when divided by k?" If they do, their
    difference is guaranteed to be a clean multiple of k. Try it with
    real numbers: 29 % 5 == 4 and 4 % 5 == 4 — same remainder — and
    indeed 29 - 4 = 25, which is divisible by 5.

4.  **Why a hash map?**
    We walk through the array once, and at each index we compute
    `prefix % k`. We want to know: "have we seen this exact remainder
    before, at some earlier index?" A hash map lets us check that in
    O(1) instead of re-scanning everything we've seen so far.

5.  **Why store only the index, and only the FIRST time we see a
    remainder?**
    We're not trying to find the sum — we already know it'll be a
    multiple of k. We just need to know the two index positions are at
    least 2 apart (subarray length >= 2). Keeping the *earliest* index
    for each remainder gives any future match the biggest possible gap,
    so it's the safest choice — it never causes us to miss a valid
    answer, and overwriting it with a later index only shrinks that
    gap.

6.  **Why seed the map with `{0: -1}`?**
    Imagine nums = [5, 5] and k = 5. The prefix sum after index 1 is
    10, and 10 % 5 == 0 — meaning the subarray from the very start is
    already a multiple of k. To detect this "starts-from-index-0" case
    with the same logic as everything else, we pretend a remainder of
    0 was already seen at index -1 (i.e., "before the array began").
    That way index 1 sees remainder 0 already in the map at -1, and
    `1 - (-1) = 2 >= 2`, so it correctly returns True.

7.  **Putting it together, one line at a time (see code below):**
    - `prefix += num` → keep a running total as we scan left to right.
    - `key = prefix % k` → reduce that running total to "just the
      remainder," which is all we actually need.
    - `if key in hmap` → have we seen this remainder before?
      - if yes, and the two indices are far enough apart, we're done.
      - if no, remember this index as the first time we saw it.

### Why does it work?
Same-remainder prefix sums are exactly the mathematical condition for "the
subarray between them sums to a multiple of k." Using the hash map to
recall the FIRST time each remainder appeared turns an O(n) search for a
matching earlier prefix into an O(1) lookup.

### Complexity
- TC: O(n) — single pass, O(1) hash map operations per element
- SC: O(min(n, k)) — the hash map holds at most k distinct remainders
  (or fewer, bounded by n if n < k)

### Pros
- Optimal time — single pass, no recomputation of sums.
- The `{0: -1}` seed elegantly handles the "prefix itself is a multiple of
  k" edge case without a special branch.

### DSA Buddy Point 🧠
"Multiple-of-k subarray sum -> think prefix sums MOD k, not raw prefix
sums. Two equal remainders anywhere in the array means everything between
them sums to a multiple of k."

### Edge Case ⚠️
Only store a remainder in the map the FIRST time it's seen — never
overwrite it on a later occurrence. Overwriting would shrink the gap
`i - hmap[key]` for future lookups, potentially causing you to miss a
valid subarray that only satisfies `>= 2` when measured against the
EARLIEST occurrence of that remainder.

### What can be improved?
Nothing — O(n) time is optimal since every element must be inspected at
least once, and O(min(n,k)) space is the minimum needed to track
remainder-to-index mappings. This is the accepted optimal solution.
"""


def check_subarray_sum(nums: list[int], k: int) -> bool:
    # hmap maps: remainder (prefix sum % k) -> earliest index it was seen at.
    # Seed with {0: -1} so a prefix that's ALREADY a multiple of k (starting
    # from index 0) is correctly detected as if remainder 0 occurred "before
    # the array started."
    hmap = {0: -1}
    prefix = 0  # running sum of nums[0..i], updated as we scan left to right
    for i, num in enumerate(nums):
        prefix += num          # step 1: extend the running prefix sum
        key = prefix % k       # step 2: we only care about the remainder mod k

        if key in hmap:
            # We've seen this remainder before at index hmap[key].
            # Equal remainders => everything between the two indices sums
            # to a multiple of k. Just need the gap to be >= 2 (subarray
            # length requirement).
            if i - hmap[key] >= 2:
                return True
            # else: gap too small, but keep the EARLIEST index as-is —
            # do NOT overwrite, since that would only shrink future gaps.
        else:
            # First time seeing this remainder — record it.
            hmap[key] = i

    return False


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
CONTINUOUS SUBARRAY SUM (multiple of k, length >= 2)
│
├── Brute Force
│   └── For each start, extend right, check sum % k == 0 -> O(n^2)
│
├── Bottleneck
│   └── Recomputes running sums from scratch per starting index
│
├── Key Math Insight
│   └── prefix[i] % k == prefix[j] % k  <=>  (prefix[j]-prefix[i]) % k == 0
│       -> Equal remainders = a multiple-of-k subarray exists between them
│
├── Optimization — Prefix Sum + Hash Map (remainder -> earliest index)
│   ├── Seed hmap = {0: -1} to catch "prefix itself is a multiple of k"
│   ├── For each i: compute prefix % k
│   ├── If remainder seen before at index p, and i - p >= 2 -> True
│   └── Else: store remainder -> i ONLY if it's the first time seen
│
└── Complexity
    └── O(n) time (single pass, O(1) hash ops)
    └── O(min(n,k)) space (map holds at most k distinct remainders)
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "'Subarray sum is a multiple of k' -> prefix sums MOD k, not raw prefix
  sums. Equal remainders bracket a multiple-of-k subarray."
- "Seed the hashmap with {0: -1} — this represents 'a prefix sum of 0
  occurred before index 0,' letting the first real prefix itself count as
  a match if it's already a multiple of k."
- "Only store the FIRST occurrence of each remainder — overwriting with a
  later index shrinks the gap and can cause you to miss valid subarrays
  that need the >= 2 length requirement satisfied against the earliest
  occurrence."
- "This is the modular-arithmetic sibling of the classic 'prefix sum + hash
  map for subarray sum == target' pattern (LC 560) — same skeleton, mod k
  instead of exact target matching."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                        | Core Idea                                              | TC   | SC          | Pros                             | Cons                                    | When to Use                       |
|-------------------------------------|---------------------------------------------------------------|------|-------------|----------------------------------------|--------------------------------------------|----------------------------------------|
| Brute Force                         | Check every subarray's sum directly                              | O(n^2)| O(1)       | Trivial to write/verify                 | Redoes overlapping sum work every start     | Baseline / correctness check only     |
| Prefix Sum + Hash Map (mod k)       | Equal remainders mod k -> multiple-of-k subarray exists between them | O(n) | O(min(n,k)) | Optimal time, elegant edge-case handling | Requires the modular-arithmetic insight upfront | Default optimal choice (your code)    |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Prefix Sum + Hash Map, using remainders instead of raw values
  (same family as LC 560 "Subarray Sum Equals K," adapted for the "sum is
  a multiple of k" condition instead of an exact target).
- Go-to answer: "Track prefix sums mod k in a hash map, remembering the
  EARLIEST index each remainder was seen. Two equal remainders mean the
  subarray between them sums to a multiple of k. Seed the map with
  {0: -1} to catch the case where a prefix itself already qualifies.
  O(n) time, O(min(n,k)) space."
- Good to mention brute force first to establish the O(n^2) baseline, then
  pivot to "what mathematical property of prefix sums could shortcut this
  search?" as the insight that unlocks the hash map approach.
- Common follow-up: "Why store only the FIRST occurrence of each
  remainder?" -> Because it maximizes the index gap for any future match,
  giving the best chance of satisfying length >= 2 — overwriting with a
  later index could cause you to miss a valid answer.
"""