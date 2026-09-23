"""
================================================================================
 PROBLEM: Number of Flowers in Full Bloom (LeetCode 2251)
================================================================================
Given: `flowers[i] = [start_i, end_i]` — flower `i` is in full bloom on
every day in the INCLUSIVE range `[start_i, end_i]`. Given a `people`
array where `people[j]` is the day person `j` arrives to view flowers,
return an array `answer` where `answer[j]` is the number of flowers in
full bloom on the day person `j` arrives. People can arrive on the same
day / in any order relative to each other.

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Is the bloom range `[start_i, end_i]` INCLUSIVE on both ends? (Yes —
  this is the detail that decides whether you need `upper_bound` vs
  `lower_bound` and `<=` vs `<` at each boundary; getting the
  inclusive/exclusive boundary wrong is the #1 way to get an off-by-one
  here)
- Can multiple people arrive on the same day, and does answer order need
  to match input order (not sorted-by-day order)? (Yes to both — this
  rules out a simple "sort people and sweep once" approach unless you
  separately track original indices; using per-person binary search
  sidesteps that issue entirely by answering each query independently)
- Can `start_i == end_i` (a flower blooms for exactly one day)? (Yes —
  should work fine as long as boundaries are handled as inclusive
  correctly)

"""

# ================================================================================
# 🔑🔑🔑  STRONG POINTS FOR "COUNT ACTIVE INTERVALS AT A POINT" PROBLEMS  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   "How many intervals are ACTIVE at query point p?" decomposes     │
    │   into two INDEPENDENT counting questions:                         │
    │   (# intervals that have STARTED by p) − (# intervals that have    │
    │   ALREADY ENDED before p) = # intervals active AT p.                │
    │   Sort starts and ends SEPARATELY, then binary search each array   │
    │   for every query — no need to keep start/end pairs together.      │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

This is a genuinely different shape of problem from both matrix-search
problems (LC 74 / LC 240) and the binary-search-on-the-answer family
(Koko/Ship/MinSpeed/Bouquets) — here binary search is used as an
EFFICIENT COUNTING primitive (count how many array elements are
`<= x` or `< x`) applied twice per query, not to search for a single
target value or an abstract answer space. Key ideas:

1. **Splitting start times and end times into two SEPARATE sorted
   arrays is the core trick — and it's valid precisely because you only
   ever need COUNTS, not which specific flower a given start/end belongs
   to.** Once you only care about "how many," you can freely discard the
   start-end pairing and sort each list independently.

2. **`# started by day p` = count of start times `<= p`** — this is
   `upper_bound(startTime, p)`, i.e. "index of first element STRICTLY
   greater than p," which equals the count of elements `<= p` because
   the array is sorted from index 0.

3. **`# already ended before day p` = count of end times `< p`** — this
   is `lower_bound(endTime, p)`, i.e. "index of first element `>= p`,"
   which equals the count of elements strictly `< p`. Note the
   asymmetry: started-by uses `<=` (bloom range is start-inclusive) but
   ended-before uses strict `<` (a flower that ends exactly ON day p is
   STILL in bloom on day p, since the range is end-inclusive too) — this
   is exactly where the "inclusive both ends" clarifying question above
   becomes concrete code.

4. **`answer[j] = upper_bound(startTime, p) - lower_bound(endTime, p)`**
   — flowers-in-bloom-at-p = (started by p) − (ended before p). Anything
   that started by p AND hasn't ended before p is, by definition,
   blooming on day p.

5. **Custom `upper_bound`/`lower_bound` are just binary search variants**
   — same `l, r = 0, len(arr)` / `while l < r` / converge-to-l template
   you've used before, just with the comparison flipped between the two
   (`<=` vs `<`) to get "first index greater than value" vs "first index
   not less than value" respectively. Python's built-in `bisect.bisect_right`
   and `bisect.bisect_left` are exact drop-in equivalents for these two
   helper functions.
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea
For each person `p`, loop over EVERY flower and check if
`start_i <= p <= end_i`; count how many satisfy it. Straightforward, but
re-scans all flowers for every single person.

### The key insight: decouple "counting" from "which flower"
You don't need to know WHICH flowers are blooming — just HOW MANY. That
means you don't need to keep `[start, end]` pairs together at all. Once
you accept that, sorting starts and ends into two independent lists (and
throwing away the pairing) is safe, and each becomes searchable on its
own with binary search.

### Step-by-step trace: fullBloomFlowers([[1,6],[3,7],[9,12],[4,13]], people=[2,3,7,11])
```
startTime sorted: [1, 3, 4, 9]
endTime   sorted: [6, 7, 12, 13]

person p=2:
  upper_bound(startTime, 2) -> first index with value > 2 -> index 1
    (started by day 2: just flower with start=1 -> count 1)
  lower_bound(endTime, 2)   -> first index with value >= 2 -> index 0
    (ended before day 2: none -> count 0)
  answer = 1 - 0 = 1 ✅ (only [1,6] is blooming on day 2)

person p=3:
  upper_bound(startTime, 3) -> first index with value > 3 -> index 2
    (started by day 3: starts 1,3 -> count 2)
  lower_bound(endTime, 3)   -> first index with value >= 3 -> index 0
    (ended before day 3: none -> count 0)
  answer = 2 - 0 = 2 ✅ ([1,6] and [3,7] both blooming)

person p=7:
  upper_bound(startTime, 7) -> first index with value > 7 -> starts are
    [1,3,4,9]; 9 is the first one > 7, at index 3 -> count 3
    (started by day 7: 1, 3, 4 -> count 3)
  lower_bound(endTime, 7)   -> first index with value >= 7 -> ends are
    [6,7,12,13]; 7 is the first one >= 7, at index 1 -> count 1
    (ended before day 7: just end=6 -> count 1)
  answer = 3 - 1 = 2 ✅ (blooming on day 7: [3,7] and [4,13] -> 2)
```

### The "aha" moment to remember 🎯
"Count active intervals at a point" almost always splits into "count
starts `<= p`" minus "count ends `< p`" (or `< p+1` / `<= p-1` depending
on exact inclusivity conventions) — memorize the DECOMPOSITION, then
just carefully match `<=` vs `<` to whatever inclusive/exclusive
boundary the problem statement specifies. Get the boundary comparisons
right by re-deriving them from the problem's own wording every time,
rather than reusing a memorized `<=`/`<` pairing from a different
problem with different inclusivity rules.
"""

# ================================================================================
# ALTERNATIVE APPROACH — Brute Force (check every flower per person)
# ================================================================================
"""
### Thought Process 🧠
For each person, loop over all flowers and count how many have
`start_i <= p <= end_i`.

### Complexity
- TC: O(people * flowers) — nested loop, no reuse of work across queries
- SC: O(1) extra (ignoring the output array)

### Pros
- Obviously correct, easiest to write and verify.

### Cons
- Recomputes everything from scratch for every person — wildly
  redundant when `people` and `flowers` are both large (up to 5*10^4
  each in this problem's constraints -> up to 2.5*10^9 operations,
  far too slow).

### Bottleneck
Treats each query as fully independent with no shared preprocessing.
Ask: "can I do O(n log n) preprocessing ONCE, then answer each query in
O(log n) instead of O(n)?" -> Yes: sort starts/ends once, binary search
per query (main approach below).
"""


def full_bloom_flowers_brute(flowers: list[list[int]], people: list[int]) -> list[int]:
    answers = []
    for p in people:
        count = 0
        for start, end in flowers:
            if start <= p <= end:
                count += 1
        answers.append(count)
    return answers


# ================================================================================
# MY APPROACH — Sort Starts/Ends Separately + Binary Search per Query (optimal)
# ================================================================================
"""
### Idea
Split `flowers` into two separate lists, `startTime` and `endTime`, sort
each independently (the pairing between a flower's start and end is no
longer needed once you only care about counts). For each person `p`:
`answer[j] = (# starts <= p) - (# ends < p)`, computed via two binary
searches: `upper_bound(startTime, p)` gives the first count, and
`lower_bound(endTime, p)` gives the second.

### Complexity
- TC: O((n + q) log n) — sorting `startTime`/`endTime` is O(n log n)
  each; each of `q` people does two O(log n) binary searches
- SC: O(n) for the two sorted arrays (O(1) extra beyond the required
  output if flowers/people are allowed to be modified in place, but
  typically counted as O(n) for the copies)

### Pros
- Fully decouples preprocessing (sort once) from querying (binary
  search per person) — the classic "pay a bit up front, then answer
  each query cheaply" trade-off.
- Handles people arriving in ANY order (including duplicates and
  unsorted input) correctly, since each query is answered
  independently — no need to sort `people` and remember original
  indices.
- `upper_bound`/`lower_bound` are small, reusable, well-understood
  binary search primitives (equivalent to `bisect.bisect_right` /
  `bisect.bisect_left`) that generalize to many other "count elements
  satisfying X" problems.

### Cons
- Requires getting the `<=` vs `<` boundary distinction exactly right
  (see Strong Points above) — an easy place to introduce a subtle
  off-by-one if the inclusive/exclusive convention isn't double-checked
  against the problem statement.
- Two O(log n) searches per query is slightly more constant-factor work
  than a single-pass sweep-line approach (see below) if `people` were
  allowed to be answered in sorted order and re-mapped — but this
  approach is simpler to write correctly and get right under interview
  time pressure.

### DSA Buddy Point 🧠
"Once a problem only needs COUNTS of intervals satisfying some
condition at a query point, ask whether start times and end times can
be sorted and queried INDEPENDENTLY of each other — you often don't
need to keep interval pairs together at all, which is what unlocks
clean binary search on two separate sorted arrays."

### What can be improved?
Nothing significant in complexity class — O((n + q) log n) is already
near-optimal for this problem (any comparison-based approach needs at
least the sort). A sweep-line + offline-sorted-queries approach can
reduce the per-query cost to amortized O(1) after an O(n log n + q log q)
sort, but adds real complexity (tracking original indices to remap
answers back to input order) for the same overall complexity class — see
below.
"""


class Solution:
    def fullBloomFlowers(
        self, flowers: list[list[int]], people: list[int]
    ) -> list[int]:
        startTime = []
        endTime = []

        for f in flowers:
            startTime.append(f[0])
            endTime.append(f[1])

        startTime.sort()
        endTime.sort()

        answers = []

        def upper_bound(arr, value):
            l, r = 0, len(arr)

            while l < r:
                mid = (l + r) // 2

                if arr[mid] <= value:
                    l = mid + 1
                else:
                    r = mid

            return l

        def lower_bound(arr, value):
            l, r = 0, len(arr)

            while l < r:
                mid = (l + r) // 2

                if arr[mid] < value:
                    l = mid + 1
                else:
                    r = mid

            return l

        for p in people:
            answers.append(upper_bound(startTime, p) - lower_bound(endTime, p))
        return answers


# ================================================================================
# ALTERNATIVE / OPTIONAL APPROACH — Sweep Line with Offline Sorted Queries
# ================================================================================
"""
### Thought Process 🧠
Sort `people` (keeping track of ORIGINAL indices, since the output must
match input order), then sweep through starts and ends and people's
query days TOGETHER in increasing day order, maintaining a running
`active` counter: increment it for every start `<=` the current query
day not yet consumed, decrement it for every end `<` the current query
day not yet consumed. Assign `active` to `answer[original_index]` at
each query day. This avoids repeating a fresh binary search per query by
advancing three pointers together in one linear pass (after the O(n log
n + q log q) sorts).

### Complexity
- TC: O(n log n + q log q) — dominated by sorting; the sweep itself is
  O(n + q) since each of the three pointers (starts, ends, people) only
  moves forward
- SC: O(q) to remember original indices for re-mapping answers back to
  input order, plus O(n) for the sorted start/end copies

### Pros
- Slightly better constant factor than the binary-search-per-query
  approach — O(1) amortized work per query point during the sweep,
  instead of O(log n) per query.
- Natural fit if `people` is already expected to be processed in
  sorted/streaming day order for other reasons in a larger system.

### Cons
- More bookkeeping: must sort `people` alongside a parallel array of
  original indices (e.g. `sorted(enumerate(people), key=lambda x: x[1])`),
  then remember to write `answer[original_index]`, not `answer[j]` in
  sorted order — a common source of bugs if the re-mapping step is
  forgotten or done incorrectly.
- Same overall O(n log n + q log q) complexity class as the binary
  search approach (both are sort-dominated) — the sweep doesn't change
  the asymptotic class, so the added bookkeeping buys a constant-factor
  win, not a Big-O win.

### DSA Buddy Point 🧠
"When you find yourself re-deriving the same 'how far has this pointer
advanced' state on every query, and queries CAN be processed in sorted
order (with index remapping), a sweep line can turn per-query O(log n)
into per-query amortized O(1) — but only bother with this once the
simpler binary-search-per-query version is proven correct and its
performance is actually insufficient."

### What can be improved?
Nothing in complexity class over the binary search approach for this
specific problem's constraints — both are O(n log n + q log q)
overall. Reach for the sweep-line version specifically when you need
the better constant factor, not by default.
"""

# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
NUMBER OF FLOWERS IN FULL BLOOM
│
├── Brute Force
│   └── For each person, scan all flowers -> O(people * flowers)
│
├── Bottleneck
│   └── No preprocessing reused across queries — redoes full work
│       every single query
│
├── Key Insight
│   └── "# blooming at p" = "# started by p" − "# already ended before p"
│       -> decouple start times and end times into two independent
│       sorted arrays (pairing not needed once you only need COUNTS)
│
├── My Approach — Sort Separately + Binary Search per Query (BEST for
│   │   simplicity / handles unordered people trivially)
│   └── upper_bound(startTime, p) − lower_bound(endTime, p) per person
│       -> O((n + q) log n) time, O(n) space
│       -> upper_bound uses <=  (start-inclusive bloom range)
│       -> lower_bound  uses <  (end-inclusive bloom range: a flower
│          ending exactly on day p is still blooming on day p)
│
└── Sweep Line + Offline Sorted Queries (better constant factor)
    └── Sort people with original indices, advance 3 pointers together
        -> O(n log n + q log q) time, O(n + q) space
        -> same Big-O class, less per-query overhead, more bookkeeping
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "'How many intervals are active at point p?' almost always
  decomposes into (# started by p) − (# ended before p) — memorize this
  decomposition as the default first move for interval-counting-at-a-
  point problems."
- "Once a problem only needs COUNTS, not which specific interval, you
  can safely sort start times and end times INDEPENDENTLY, discarding
  the start-end pairing — this is what unlocks clean, separate binary
  searches on two 1-D arrays instead of juggling interval objects."
- "Match `<=` vs `<` boundary comparisons EXACTLY to the problem's
  stated inclusivity — here, both ends of `[start, end]` are inclusive,
  which is why 'started by p' uses `<=` (upper_bound) but 'ended before
  p' uses strict `<` (lower_bound): an interval ending exactly ON day p
  is still active on day p, so it must NOT be subtracted yet."
- "Custom `upper_bound`/`lower_bound` binary search helpers are directly
  equivalent to Python's `bisect.bisect_right`/`bisect.bisect_left` —
  recognizing this means you can reach for the standard library `bisect`
  module directly in a real submission instead of hand-rolling these,
  once you understand what each one computes."
- "A binary-search-per-query approach trades a bit of per-query
  constant factor (O(log n) instead of amortized O(1)) for much simpler
  code that handles unordered/duplicate query days for free — prefer it
  by default, and only reach for a sweep-line + index-remapping version
  if profiling shows the constant factor actually matters."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                              | Core Idea                                                          | TC                        | SC   | Pros                                                     | Cons                                                              | When to Use                              |
|------------------------------------------|-------------------------------------------------------------------------|-----------------------------|------|----------------------------------------------------------------|--------------------------------------------------------------------------|----------------------------------------------|
| Brute Force                              | For each person, scan all flowers                                        | O(people * flowers)         | O(1) | Trivial, obviously correct                                       | Far too slow for large inputs, no shared preprocessing                     | Baseline / correctness check only            |
| Sort Separately + Binary Search per Query | (# starts <= p) − (# ends < p), via upper_bound/lower_bound per person    | O((n + q) log n)            | O(n) | Simple, handles unordered/duplicate people trivially, reusable helpers | Two binary searches per query — slightly more per-query work than sweep      | Default optimal choice (your code)            |
| Sweep Line + Offline Sorted Queries       | Sort people w/ original indices, sweep 3 pointers together in one pass    | O(n log n + q log q)        | O(n+q)| Better constant factor — amortized O(1) per query during the sweep    | More bookkeeping (index remapping), same Big-O class as binary search        | When constant factor matters at scale         |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Interval-Counting-at-a-Point via Decoupled Start/End Arrays —
  a distinct technique from both matrix-search binary search (LC 74/240)
  and binary-search-on-the-answer (Koko/Ship/MinSpeed/Bouquets); here
  binary search is used purely as an efficient "count elements <= x" /
  "count elements < x" primitive, applied twice per query.
- Go-to answer: "Split flowers into separate sorted `startTime` and
  `endTime` arrays — the start/end pairing isn't needed once you only
  need counts. For each person on day p, the number of flowers in bloom
  is (# starts <= p) − (# ends < p), computed with two binary searches:
  upper_bound on startTime, lower_bound on endTime. O((n+q) log n) time,
  O(n) space."
- Good to explicitly call out the `<=` vs `<` boundary asymmetry if
  discussing this problem — it's the single detail most likely to trip
  someone up, and directly follows from the bloom range being inclusive
  on BOTH ends.
- Common follow-up: "What if you need to answer MANY repeated queries
  efficiently, or people arrive in a stream?" -> A sweep-line approach
  (sort people with original indices, advance three pointers together)
  achieves the same O(n log n + q log q) overall complexity with a
  better O(1) amortized cost per query, at the expense of extra
  bookkeeping to remap answers back to original input order.
"""