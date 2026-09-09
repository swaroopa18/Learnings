"""
================================================================================
PROBLEM: Append Characters to Make Subsequence
LeetCode 2486
================================================================================

1. PROBLEM STATEMENT
--------------------------------------------------------------------------------
You are given two strings `s` and `t`, consisting of lowercase English
letters only.

You are allowed to APPEND characters to the END of `s` (as many as you like,
in any order you choose). You want to make `t` a subsequence of `s` after
these appends.

Return the MINIMUM number of characters that need to be appended to the end
of `s` so that `t` becomes a subsequence of `s`.

A subsequence is a string obtained by deleting some (possibly zero)
characters from another string without changing the relative order of the
remaining characters.

Constraints (typical for this problem):
    1 <= s.length, t.length <= 10^5
    s and t consist only of lowercase English letters.


2. INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
Before coding, a candidate should ask:

  - Can I only APPEND to the end of `s`, or can I also insert characters in
    the middle? (Confirmed: only appending to the end is allowed — this is
    the key constraint that makes the problem tractable with two pointers.)
  - Are `s` and `t` guaranteed to be lowercase English letters only, or could
    there be other characters/case sensitivity to worry about?
  - Can `s` or `t` be empty strings? What should the answer be in that case?
  - Is `t` allowed to already be a subsequence of `s`? (Then answer is 0.)
  - Do we need to actually construct the resulting string, or just return the
    COUNT of characters we would need to append?
  - What is the expected time complexity given `s`, `t` can be up to 10^5
    characters? (This hints that an O(n + m) solution is expected.)


3. EXAMPLES & EDGE CASES
--------------------------------------------------------------------------------
Example 1:
    s = "coaching", t = "coding"
    Output: 4
    Explanation: "co" is already a matching prefix-subsequence of "coaching"
    (c-o-...-i-n-g can be found in order), but after using s = "coaching" we
    can match "c","o","in" ... eventually we can only match "coin" as a
    subsequence out of "coaching", leaving "g" unmatched... Actually walking
    it with two pointers: we match c,o,a(no)...,i,n,g -> we manage to match
    "coing"? Let's just trust the two-pointer simulation (done in code below)
    which gives leftover = 4, meaning we append "ding" to make
    "coachingding" contain "coding" as a subsequence.

Example 2:
    s = "abcde", t = "a"
    Output: 0
    Explanation: "a" is already a subsequence of "abcde".

Example 3:
    s = "z", t = "abcde"
    Output: 5
    Explanation: None of "abcde" matches "z", so all 5 characters must be
    appended.

Edge Cases to consider:
  - t is already fully a subsequence of s -> answer 0.
  - s and t share no common characters at all -> answer len(t).
  - s is much shorter than t -> most/all of t needs appending.
  - s is much longer than t -> still O(n) scan needed, but likely answer 0
    or small.
  - t is a single character -> just check if that character exists in s
    anywhere (in order, trivially true if it exists at all since there's
    nothing before it to worry about).
  - Duplicate characters in s and t (e.g. s = "aaaa", t = "aaaaa") -> ensure
    greedy matching still works correctly (it does, see proof below).


4. ALL MEANINGFULLY DIFFERENT APPROACHES
================================================================================

--------------------------------------------------------------------------------
APPROACH 1: Two-Pointer Greedy Matching (Brute-force-simple / Optimal)
--------------------------------------------------------------------------------
INTUITION (DSA-buddy explanation):

Think about what "t is a subsequence of s" actually means: if you walk
through `s` left to right, you should be able to "pick off" the characters
of `t` in order, skipping over characters of `s` that don't match.

Since we're ONLY allowed to append to the END of `s`, any character of `t`
that we cannot find (in order) while scanning `s` from left to right MUST be
appended at the end. There is no way around it, because appending only
happens after everything already in `s` — appended characters can never help
match something that should have appeared *before* the end of `s`.

So the strategy is simple and greedy:
  - Use two pointers, `i` for `s` and `j` for `t`.
  - Walk `i` through `s` from left to right.
  - Whenever s[i] == t[j], that means we've successfully matched the next
    needed character of `t`, so advance `j` as well.
  - Whether it matched or not, always advance `i` (we consume `s` left to
    right regardless).
  - Stop when either pointer reaches the end of its string.
  - At the end, whatever is LEFT UNMATCHED in `t` (i.e., len(t) - j) is
    exactly the number of characters we must append.

WHY GREEDY WORKS (proof of correctness):
  - Greedily matching t[j] as early as possible in s never hurts: if s[i]
    matches t[j], taking that match now can only leave MORE of s available
    for matching t[j+1], t[j+2], ... later (never less). This is the classic
    "earliest matching" greedy argument used in subsequence-checking
    problems (same idea as LeetCode 392 "Is Subsequence").
  - Therefore scanning once, greedily consuming t whenever s matches,
    finds the maximum possible number of matched characters. Whatever
    isn't matched genuinely cannot be matched using only the existing `s`,
    so it must be appended.

ALGORITHM (step by step):
  1. Initialize i = 0 (pointer into s), j = 0 (pointer into t).
  2. While i < len(s) and j < len(t):
       a. If s[i] == t[j]: this character of t is satisfied -> j += 1
       b. Always: i += 1 (move forward in s regardless of match)
  3. After the loop, j represents how many characters of t were
     successfully matched as a subsequence.
  4. The answer is len(t) - j (characters of t that still need to be
     appended).

DATA STRUCTURES USED: None beyond two integer pointers — O(1) extra space.

TIME COMPLEXITY: O(n) where n = len(s). We scan s at most once; j never
     exceeds len(t) so the loop runs at most n iterations (bounded by
     min considerations, but strictly the while-loop condition on i is
     what terminates it — each iteration increments i, so at most n
     iterations total).

SPACE COMPLEXITY: O(1). Only two integer pointers are used, no extra data
     structures or recursion stack.

WHY A "BETTER" APPROACH ISN'T REALLY NEEDED HERE:
This IS the optimal approach for this specific problem — appending is only
allowed at the end, which collapses the problem to a single linear subsequence
scan. There isn't a meaningfully different "brute force" that is asymptotically
worse yet conceptually distinct, other than restating the same idea using
different Python idioms (shown below as Approach 2 for interview flexibility).


--------------------------------------------------------------------------------
APPROACH 2: Pythonic Two-Pointer using iter() + all() (Same complexity, different style)
--------------------------------------------------------------------------------
INTUITION:
This is functionally identical to Approach 1 but expressed idiomatically in
Python using an iterator over `s` and the built-in `all()` short-circuiting
behavior with `next()`. It's useful to show in an interview if asked "can you
write this more concisely in Python?", but it is NOT a different algorithm —
same greedy two-pointer idea under the hood, just hidden inside iterator
machinery.

ALGORITHM:
  1. Create an iterator over s: it = iter(s).
  2. For each character c in t, try to advance the iterator until we find c
     (using `any(x == c for x in it)`), which consumes the iterator as it
     searches — mimicking the "always advance i" behavior from Approach 1.
  3. Count how many characters of t were matched; unmatched count is the
     answer. Equivalently, count how many characters of t FAILED to be found
     using a generator expression with `sum`.

TIME COMPLEXITY: O(n) — the shared iterator `it` is only ever advanced
     forward, so across the whole loop over t, the iterator moves through s
     at most once, i.e., total work is O(len(s) + len(t)).

SPACE COMPLEXITY: O(1) additional space (the iterator itself is O(1)).

WHEN TO PREFER: Approach 1 is clearer for teaching/interviews since the
     pointer movement is explicit. Approach 2 is a nice "one-liner" flex but
     can be harder to explain and debug live — many interviewers prefer the
     explicit two-pointer version (Approach 1).


5. APPROACH COMPARISON
================================================================================
+----------------------+---------------------------+-----------------+-----------------+---------------------------+---------------------------+------------+-------------------------+
| Approach              | Main Idea                 | Time Complexity | Space Complexity | Advantages                | Disadvantages             | Difficulty | Interview Suitability   |
+----------------------+---------------------------+-----------------+-----------------+---------------------------+---------------------------+------------+-------------------------+
| 1. Explicit Two-Pointer | Greedily match t as a    | O(n)            | O(1)             | Clear, easy to explain,   | None significant           | Easy       | Excellent (preferred)   |
|    Greedy Scan          | subsequence of s          |                 |                  | easy to trace/debug       |                             |            |                          |
+----------------------+---------------------------+-----------------+-----------------+---------------------------+---------------------------+------------+-------------------------+
| 2. Iterator/any()      | Same greedy idea, but     | O(n + m)        | O(1)             | Concise, "Pythonic"       | Harder to explain/debug    | Easy       | Good (as a follow-up    |
|    based               | implemented via Python's  |                 |                  | one-liner style           | live, obscures the pointer |            | "cleaner code" answer)  |
|                        | iterator protocol         |                 |                  |                           | movement                   |            |                          |
+----------------------+---------------------------+-----------------+-----------------+---------------------------+---------------------------+------------+-------------------------+

(n = len(s), m = len(t); both approaches are asymptotically equivalent —
O(n) dominates since m <= n in the useful matching region, and unmatched
characters are counted in O(1) per character.)


6. BEST INTERVIEW APPROACH & DSA PATTERN
================================================================================
BEST APPROACH: Approach 1 — Explicit Two-Pointer Greedy Scan.
  - It is optimal (O(n) time, O(1) space), trivial to explain, trivial to
    trace on a whiteboard, and directly demonstrates understanding of *why*
    greedy matching is correct for subsequence problems.

UNDERLYING DSA PATTERN: "Two Pointers — Subsequence Matching"
  - This is the same core pattern as LeetCode 392 "Is Subsequence".
  - Recognizable clues in the problem statement:
      * Two strings being compared where ORDER matters but not
        contiguity ("subsequence", not "substring").
      * An operation is restricted to only the END of one string
        (appending), which signals that a single left-to-right pass
        is sufficient — no need to consider insertions in the middle.
      * The question asks for a MINIMUM COUNT related to matching,
        which is a strong hint for a greedy two-pointer counting scan.

HOW TO RECOGNIZE THIS PATTERN IN FUTURE PROBLEMS:
  - Whenever you see "is X a subsequence of Y" or "minimum insertions/
    deletions to make X a subsequence of Y (restricted to one end)",
    think: two pointers, greedy earliest-match strategy.
  - If insertions were allowed ANYWHERE (not just the end), the problem
    would instead become a Dynamic Programming problem (e.g., "Minimum
    ASCII Delete Sum" or "Shortest Common Supersequence" style DP with
    edit-distance-like state), because you'd need to consider all possible
    insertion positions, not just a single linear scan.

RECOMMENDED INTERVIEW-SOLVING PROGRESSION:
  1. Clarify constraints (only append at the end? lowercase only? etc.)
  2. State the key insight: since we can only append at the end, matching
     characters of t against s in a single left-to-right pass is sufficient
     and optimal — restate the greedy argument briefly.
  3. Write the two-pointer solution directly (Approach 1) — no need to
     write a separate, slower brute force since the two-pointer approach
     IS the natural first correct idea here.
  4. Walk through a dry run example to prove correctness to the interviewer.
  5. State time/space complexity: O(n) / O(1).
  6. Optionally mention the Pythonic iterator-based rewrite (Approach 2) if
     asked for alternative styles.


7. FOLLOW-UP QUESTIONS
================================================================================
  - "What if you could insert characters ANYWHERE in s, not just append at
     the end?"
      -> This becomes a different (harder) problem — essentially computing
         the minimum number of insertions needed to make t a subsequence of
         s, solvable via Dynamic Programming based on the Longest Common
         Subsequence (LCS) of s and t:
             answer = len(t) - LCS(s, t)
         DP table would be O(n*m) time and O(n*m) (or O(min(n,m)) with
         rolling array) space.

  - "What if you needed to return the actual resulting string, not just the
     count?"
      -> Track the unmatched suffix of t (t[j:] after the two-pointer scan)
         and append it directly: result = s + t[j:].

  - "What if s or t could contain uppercase letters or other characters —
     does case sensitivity matter?"
      -> Comparisons would need to explicitly decide whether 'A' == 'a'
         (case-insensitive) or not; as given, comparisons are already
         case-sensitive by default in Python, so no code change needed
         unless case-insensitivity is explicitly required.

  - "What if there were multiple query strings t1, t2, ..., tk against the
     same s, and you needed the answer for each?"
      -> Since each query is independent and O(n) per query, total is
         O(k * n). If s is fixed and huge, you could preprocess s into a
         structure like "next occurrence of each character after position i"
         (a 26-column table of size n) to answer each query t in O(len(t))
         time via binary/greedy jumps instead of O(len(s)) per query.

  - "How would the solution change if you were also allowed a limited
     budget of characters you could append (e.g., at most K), and needed to
     know if it's feasible?"
      -> Run the same two-pointer scan, compute leftover = len(t) - j, and
         check leftover <= K.


================================================================================
IMPLEMENTATIONS
================================================================================
"""

from typing import Optional


class Solution:
    # ----------------------------------------------------------------------
    # APPROACH 1: Explicit Two-Pointer Greedy Scan (RECOMMENDED / OPTIMAL)
    # Time:  O(n)  where n = len(s)
    # Space: O(1)
    # ----------------------------------------------------------------------
    def appendCharacters(self, s: str, t: str) -> int:
        i, j = 0, 0  # i -> pointer into s, j -> pointer into t

        while i < len(s) and j < len(t):
            if s[i] == t[j]:
                # Matched the next required character of t
                j += 1
            i += 1  # always advance through s

        # Whatever remains unmatched in t must be appended
        return len(t) - j

    # ----------------------------------------------------------------------
    # APPROACH 2: Pythonic Iterator-based Two-Pointer (same complexity)
    # Time:  O(n + m)
    # Space: O(1)
    # ----------------------------------------------------------------------
    def appendCharacters_iterator(self, s: str, t: str) -> int:
        it = iter(s)
        matched = 0
        for c in t:
            # Advance the shared iterator until we find c, or exhaust s
            if any(x == c for x in it):
                matched += 1
            else:
                break  # s is exhausted; no more characters can match
        return len(t) - matched


# ================================================================================
# DRY RUNS
# ================================================================================
def _dry_run(s: str, t: str) -> None:
    """Helper to print a step-by-step trace of Approach 1 for teaching purposes."""
    i, j = 0, 0
    print(f"\nDry run: s = {s!r}, t = {t!r}")
    while i < len(s) and j < len(t):
        if s[i] == t[j]:
            print(f"  i={i} s[i]={s[i]!r} == t[j]={t[j]!r} (j={j}) -> match, j -> {j+1}")
            j += 1
        else:
            print(f"  i={i} s[i]={s[i]!r} != t[j]={t[j]!r} (j={j}) -> skip")
        i += 1
    leftover = len(t) - j
    print(f"  Final: j={j}, matched {j}/{len(t)} chars of t -> append {leftover} char(s): {t[j:]!r}")


# ================================================================================
# TEST CASES
# ================================================================================
if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ("coaching", "coding"),   # general case
        ("abcde", "a"),           # t already fully matched early -> 0
        ("z", "abcde"),           # no overlap -> full len(t)
        ("abcde", "abcde"),       # t == s -> 0
        ("aaaa", "aaaaa"),        # duplicates, need 1 more 'a'
        ("", "abc"),              # empty s -> must append all of t
        ("abc", ""),              # empty t -> already trivially subsequence -> 0
        ("abcabcabc", "aabbcc"),  # interleaved duplicates
    ]

    for s_val, t_val in test_cases:
        result_1 = sol.appendCharacters(s_val, t_val)
        result_2 = sol.appendCharacters_iterator(s_val, t_val)
        status = "OK" if result_1 == result_2 else "MISMATCH!"
        print(f"s={s_val!r:15} t={t_val!r:10} -> approach1={result_1}, approach2={result_2}  [{status}]")

    # Detailed trace for the classic example
    _dry_run("coaching", "coding")
    _dry_run("abcabcabc", "aabbcc")