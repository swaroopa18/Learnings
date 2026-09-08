"""
=============================================================================
PROBLEM: Partition Labels
LeetCode #763
=============================================================================

1. PROBLEM STATEMENT
-----------------------------------------------------------------------------
You are given a string `s`. You want to partition `s` into as many parts as
possible so that each letter appears in at most one part.

Formally: split `s` into a sequence of contiguous, non-overlapping
substrings whose concatenation equals `s`, such that no character occurs
in more than one substring. Return a list of integers representing the
SIZE of each partition, in order.

Input:
    s: str -- consists of lowercase English letters, 1 <= len(s) <= 500

Output:
    List[int] -- the length of each partition, in the order they occur

Example:
    Input:  s = "ababcbacadefegdehijhklij"
    Output: [9, 7, 8]
    Explanation:
        "ababcbaca", "defegde", "hijhklij"
        Each letter appears in only one substring.
        A partition like "ababcbacadefegde", "hijhklij" is incorrect,
        because it splits s into less parts.


2. INTERVIEW CLARIFYING QUESTIONS
-----------------------------------------------------------------------------
Before coding, a strong candidate should ask:

  - Is the string guaranteed to contain only lowercase English letters,
    or could it include uppercase, digits, unicode, etc.? (Affects whether
    we can use a fixed-size array of 26 vs a hash map.)
  - Can the string be empty? What should we return for s = ""? (Typically [].)
  - Are we asked for partition SIZES, or the actual substrings themselves?
    (LeetCode asks for sizes; some variants ask for substrings.)
  - Should partitions be maximized in count (as many parts as possible),
    confirming greedy "cut as soon as possible" is the right objective?
  - Is there any constraint on partition size (min/max length)? (No, per
    problem statement, but worth confirming.)
  - What's the expected time/space complexity given the constraints
    (len(s) <= 500 is tiny, but we should still aim for optimal O(n))?


3. EXAMPLES & EDGE CASES
-----------------------------------------------------------------------------
  Example 1:
      s = "ababcbacadefegdehijhklij" -> [9, 7, 8]

  Example 2:
      s = "eccbbbbdec" -> [10]
      (every character's last occurrence pushes the boundary to the end,
       so the whole string is a single partition)

  Edge cases to consider:
    - Empty string ""            -> [] (no partitions)
    - Single character "a"       -> [1]
    - All identical characters "aaaa" -> [4] (one partition)
    - All unique characters "abcdef"  -> [1,1,1,1,1,1] (each is its own
      partition since no letter repeats)
    - A character's occurrences span almost the whole string (e.g. "a...a")
      forces one giant partition even if everything else is unique.


4. ALL MEANINGFULLY DIFFERENT APPROACHES
-----------------------------------------------------------------------------

--------------------------------------------------------------------
APPROACH 1: Brute Force -- Repeatedly Extend Boundary by Rescanning
--------------------------------------------------------------------
Intuition (taught from scratch):
    Think about what makes a valid cut point. If we start a partition at
    index `start`, we can only "close" it at some index `end` if NO
    character inside [start, end] reappears later, outside this range.
    A brute way to check this: for the current window [start, end], scan
    every character in the window, find where each of THOSE characters
    last occurs in the whole string, and if that last-occurrence extends
    beyond our current `end`, we must grow the window to include it. We
    repeat this "grow and re-scan" process until the window stops growing.

Algorithm:
    1. start = 0
    2. While start < len(s):
        a. end = start
        b. i = start
        c. While i <= end:
             - Find the last index of s[i] anywhere in s (search from the
               back, or scan the whole string) -> last_occurrence
             - end = max(end, last_occurrence)
             - i += 1
        d. Partition found: length = end - start + 1
        e. start = end + 1

Why it works:
    We keep expanding `end` until every character we've swept over has its
    last occurrence within [start, end]. Once the scan finishes without
    end growing further, no character inside can leak into a future
    partition, so it's safe to cut.

Why a better approach may exist:
    For every position, we potentially rescan a large chunk of the string
    (or the whole string) to find "last occurrence", which is wasteful.
    We're recomputing the same "last index of character X" information
    over and over.

Time Complexity: O(n^2) in the worst case -- for each of the n starting
    positions of a window, we might rescan up to n characters, and for
    each of those, search for the last occurrence in O(n) time
    (or O(1) if we precompute last occurrences, but the "brute" spirit
    here rescans the window as it grows, so overall it's O(n^2)).
Space Complexity: O(1) extra (excluding output), if we search for last
    occurrence with s.rfind(); O(n) if we cache all results.

Python Implementation:
"""
from typing import List


class SolutionBruteForce:
    def partitionLabels(self, s: str) -> List[int]:
        n = len(s)
        result = []
        start = 0

        while start < n:
            end = start
            i = start
            while i <= end:
                last_occurrence = s.rfind(s[i])  # O(n) scan from the back
                end = max(end, last_occurrence)
                i += 1
            result.append(end - start + 1)
            start = end + 1

        return result


"""
--------------------------------------------------------------------
APPROACH 2 (OPTIMAL): Greedy with Precomputed Last-Occurrence Map
--------------------------------------------------------------------
Intuition (taught from scratch):
    The brute force approach's biggest waste is repeatedly asking
    "where does this character last appear?" To fix this, PRECOMPUTE the
    answer for every character ONCE, in a single pass, using a hash map
    (or fixed array since only lowercase letters exist): last[char] = the
    highest index at which `char` occurs in s.

    Now do a SECOND pass, greedily growing a window:
      - Keep a running `end`, which is the farthest we must extend the
        CURRENT partition to keep it "safe" (i.e., self-contained).
      - As we walk through s, for each character we visit, update
        end = max(end, last[current_char]). This says: "since this
        character appears again later, my partition can't close before
        that point."
      - The key insight: when our current index `idx` actually REACHES
        `end`, it means every character we've seen so far in this window
        has its last occurrence at or before `idx`. Nothing leaks out. We
        can safely CUT here.
      - Record the partition size, reset the window, and continue.

    This is a classic "greedy interval merging" idea: each character
    defines an interval [first_occurrence, last_occurrence], and we're
    merging overlapping intervals in a single left-to-right sweep,
    without ever forming the intervals explicitly.

Algorithm:
    1. Build `last`: a map from character -> its last index in s. (1 pass)
    2. Initialize size = 0, start_of_window_end = 0 (this "end" is the
       current farthest boundary of the open partition).
    3. For idx, char in enumerate(s):
         size += 1
         end = max(end, last[char])
         if idx == end:               # window has closed
             output.append(size)
             size = 0
             # end will be correctly recomputed by max() on the next
             # iteration, so resetting it isn't strictly required, but
             # setting it to `last[char]` (equal to idx here) is a safe,
             # harmless value that gets overwritten anyway.
    4. Return output.

Why it works (correctness reasoning):
    - `end` always represents the smallest index such that closing the
      partition there is *valid so far*, given everything seen up to now:
      it's the max of all last-occurrences of characters encountered
      since the last cut.
    - We can never cut before `idx == end`, because up until then, some
      character in the window is guaranteed to reappear later (that's
      exactly what keeps `end` ahead of `idx`).
    - The moment `idx == end`, by definition every character seen in the
      current window has last occurrence <= idx, i.e. <= end. So none of
      them appear again later. It is safe -- and it is also the EARLIEST
      safe point, which is exactly what "maximize number of partitions"
      requires (cut as early as possible, every time).
    - Because it's a single greedy left-to-right sweep with no
      backtracking, and each cut is provably the earliest valid cut, the
      result is optimal (maximum number of partitions).

Time Complexity: O(n) -- one pass to build `last` (O(n)), one pass to
    build partitions (O(n)). Overall O(n).
Space Complexity: O(1) extra -- `last` has at most 26 entries (fixed
    alphabet size), independent of n. (Output list doesn't count as
    extra space since it's the required return value.)

Python Implementation (this is the version you shared -- annotated):
"""


class Solution:
    def partitionLabels(self, s: str) -> List[int]:
        # Step 1: record the LAST index at which each character appears.
        last = {}
        for idx, char in enumerate(s):
            last[char] = idx  # later occurrences overwrite earlier ones

        output = []
        size, end = 0, 0

        # Step 2: greedily sweep left to right, growing the window
        # until idx catches up with the farthest required boundary.
        for idx, char in enumerate(s):
            size += 1
            end = max(end, last[char])

            if idx == end:
                # The window [idx - size + 1, idx] is self-contained.
                output.append(size)
                size = 0
                # NOTE: setting end = last[char] here is harmless but not
                # necessary -- last[char] == idx at this point (proof: end
                # >= last[char] always since end = max(end, last[char]),
                # and last[char] >= idx always since char = s[idx] so idx
                # is itself an occurrence of char; end == idx forces
                # last[char] == idx too). On the very next iteration,
                # end gets overwritten by max(end, last[next_char]) anyway,
                # so this line could equally be `end = 0` with identical
                # behavior. It's a stylistic/redundant choice, not a bug.
                end = last[char]

        return output


"""
5. APPROACH COMPARISON
-----------------------------------------------------------------------------
+----------------------+---------------------------------+-----------+-----------+------------------------------+-------------------------------------+------------+------------------------+
| Approach              | Main Idea                       | Time      | Space     | Advantages                    | Disadvantages                        | Difficulty | Interview Suitability  |
+----------------------+---------------------------------+-----------+-----------+------------------------------+-------------------------------------+------------+------------------------+
| Brute Force           | Rescan for last occurrence      | O(n^2)    | O(1)      | Simple to reason about,       | Slow on large inputs;                | Easy       | Only as a warm-up /    |
|                        | while window grows              |           |           | no precomputation needed      | repeated redundant scanning          |            | to show initial thought|
+------------------------+---------------------------------+-----------+-----------+------------------------------+---------------------------------------+------------+------------------------+
| Greedy + Last-Occ Map  | Precompute last index per char, | O(n)      | O(1)      | Optimal, single pass after    | Requires the "aha" insight that      | Medium     | Ideal -- expected      |
| (OPTIMAL)              | greedily extend window boundary |           | (26 keys) | precompute, elegant, easy to  | idx == end is the correct cut signal | (once seen)| final solution         |
|                        | until idx == end                |           |           | explain once understood       |                                       |            |                         |
+------------------------+---------------------------------+-----------+-----------+------------------------------+---------------------------------------+------------+------------------------+


6. BEST INTERVIEW APPROACH & DSA PATTERN
-----------------------------------------------------------------------------
Best approach: Approach 2 -- Greedy with precomputed last-occurrence map.
It's O(n) time, O(1) extra space, and demonstrates strong pattern
recognition, which interviewers value highly.

Underlying DSA Pattern(s):
    - "Merge Intervals" pattern, applied implicitly. Each character
      effectively defines an interval [first_index, last_index]. Two
      characters whose intervals overlap MUST end up in the same
      partition (because you can't cut between them without splitting
      one of their occurrences into two parts). This is exactly the
      logic behind merging overlapping intervals -- except we never
      construct the intervals explicitly; we discover the "current
      merged interval's end" on the fly using a greedy sweep.
    - Also classifiable as a "Greedy / Two-Pointer Window" pattern: we
      maintain a window with a floating right boundary (`end`) that only
      ever grows, and we commit ("cut") the moment the window's actual
      right edge (`idx`) reaches that boundary.

Clues in the problem that reveal the pattern:
    - "Each letter appears in at most one part" -- this is a classic
      signal for interval-overlap / merge-style reasoning: any two
      occurrences of the same letter effectively "link" everything
      between them into one connected group.
    - "As many parts as possible" -- signals greedy: always cut as early
      as legally possible, never delay a valid cut.
    - Need for indices/last-occurrence -- signals precomputing a
      lookup table (hash map / fixed array) as a first pass.

How to recognize this pattern in future problems:
    Whenever a problem talks about grouping/partitioning items such that
    "related" items (by index range, by shared value, by interval, etc.)
    must stay together, and asks for the maximum number of groups or the
    boundaries of merged groups, think:
      1. Can I express "relatedness" as an interval range for each item?
      2. Can I precompute, for each item, the last position I need to
         worry about (its "reach")?
      3. Can I do a single greedy sweep, tracking the farthest reach seen
         so far, and cut whenever my current position catches up to it?
    This exact template also applies to problems like "Merge Intervals",
    "Minimum number of arrows to burst balloons", and "Video stitching".

Recommended interview-solving progression:
    1. Start by explaining the brute-force idea out loud (rescan to find
       last occurrence) to show you understand correctness first.
    2. Point out the redundant recomputation of "last occurrence" as the
       bottleneck.
    3. Propose precomputing last occurrences in a single pass (hash map
       or size-26 array since the alphabet is fixed).
    4. Introduce the greedy window (`end` tracks farthest needed reach),
       and explain why `idx == end` is exactly the correct, earliest safe
       cut point.
    5. Code the O(n)/O(1) solution, then dry-run it on the example to
       confirm.


7. FOLLOW-UP QUESTIONS
-----------------------------------------------------------------------------
  - "What if the string could include uppercase letters, digits, or
    unicode characters?"
      -> Swap the fixed 26-slot array for a hash map (as this solution
         already does with a dict) -- no other change needed since the
         algorithm doesn't depend on alphabet size, just O(1) lookups.

  - "Can you return the actual substrings instead of just their lengths?"
      -> Track `start` alongside `size`/`end`; when idx == end, append
         s[start:idx+1] instead of `size`, and set start = idx + 1.

  - "What if you needed to partition into AT MOST k parts (merging small
    partitions together if there are too many)?"
      -> First compute the partitions via this greedy algorithm to get
         the maximum-count partitioning, then greedily merge adjacent
         partitions (smallest first, or leftmost first) until only k
         remain -- this becomes a variant requiring a different
         merge strategy/heap.

  - "What if the string is a stream and you can't see the whole string
    upfront (can't precompute last-occurrence)?"
      -> The greedy trick relies on knowing "the last occurrence" ahead
         of time, so streaming breaks it directly. You'd need to either
         buffer the stream, or maintain a different structure (e.g.
         track "characters seen but not yet closed" and only commit a
         cut once you have external confirmation no more occurrences are
         coming, such as an end-of-stream marker per character).

  - "What's the time/space complexity if the alphabet size is huge
    (e.g., arbitrary Unicode strings)?"
      -> Time stays O(n) (hash map operations are still O(1) amortized
         average case). Space for the map becomes O(min(n, alphabet
         size)) instead of O(26), since we can have at most one entry
         per DISTINCT character actually present.

  - "Can you solve it without extra space for the last-occurrence map?"
      -> Not while keeping O(n) time in general; you'd fall back to the
         O(n^2) brute-force `rfind` approach, trading space for time.
"""


# -----------------------------------------------------------------------
# QUICK SELF-TEST / DRY RUN (executable)
# -----------------------------------------------------------------------
if __name__ == "__main__":
    tests = [
        ("ababcbacadefegdehijhklij", [9, 7, 8]),
        ("eccbbbbdec", [10]),
        ("", []),
        ("a", [1]),
        ("aaaa", [4]),
        ("abcdef", [1, 1, 1, 1, 1, 1]),
    ]

    for sol_cls in (Solution, SolutionBruteForce):
        sol = sol_cls()
        print(f"--- Testing {sol_cls.__name__} ---")
        for s, expected in tests:
            got = sol.partitionLabels(s)
            status = "PASS" if got == expected else "FAIL"
            print(f"  {status}: s={s!r:30} expected={expected} got={got}")