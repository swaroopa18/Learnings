"""
====================================================================
LeetCode 1673. Find the Most Competitive Subsequence
====================================================================

------------------------------------------------------------------
1. PROBLEM STATEMENT
------------------------------------------------------------------
Given an integer array `nums` and a positive integer `k`, return the
most competitive subsequence of `nums` of size `k`.

An array's subsequence is a resulting array obtained by erasing some
(possibly zero) elements from the array, without changing the
relative order of the remaining elements.

We define that a subsequence `a` is more competitive than a
subsequence `b` (of the same length) if in the first position where
`a` and `b` differ, subsequence `a` has a number less than the
corresponding number in `b`. For example, [1, 3, 4] is more
competitive than [1, 3, 5] because the first position they differ
is at the final number, and 4 is less than 5.

Inputs:
    nums: List[int]   -- 1 <= len(nums) <= 10^5, 0 <= nums[i] <= 10^9
    k:    int         -- 1 <= k <= len(nums)

Output:
    List[int] of length k -- the most competitive subsequence.

------------------------------------------------------------------
2. INTERVIEW CLARIFYING QUESTIONS
------------------------------------------------------------------
- Can `nums` contain duplicate values? (Yes — algorithm must handle
  ties correctly; when values are equal we should NOT pop, since
  that changes nothing and popping a needed element could hurt us.)
- Is `k` guaranteed to be between 1 and len(nums)? (Problem
  guarantees this, but worth confirming so we skip validation.)
- Should the result preserve the *relative order* of the original
  array (true subsequence), or can we reorder? (Must preserve
  relative order — that's the definition of subsequence.)
- Are the numbers guaranteed non-negative integers, and is there an
  upper bound that matters for complexity (e.g., could we bucket
  sort)? (Bounded by 10^9, so comparison-based approaches are the
  practical choice.)
- What should happen if k == len(nums)? (Answer is just `nums`
  itself — no elements can be discarded.)

------------------------------------------------------------------
3. EXAMPLES & EDGE CASES
------------------------------------------------------------------
Example 1:
    nums = [3,5,2,6], k = 2
    Output: [2,6]
    Explanation: Among the set of every possible subsequence:
    {[3,5], [3,2], [3,6], [5,2], [5,6], [2,6]}, [2,6] is the most
    competitive.

Example 2:
    nums = [2,4,3,3,5,4,9,6], k = 4
    Output: [2,3,3,4]

Edge cases to consider:
    - k == len(nums): must return nums unchanged (no room to discard
      anything). The "remaining count" guard must allow this.
    - k == 1: answer is simply the minimum value that still allows a
      valid subsequence — here that's just the global minimum,
      returned as [min(nums)].
    - All elements equal, e.g. [5,5,5,5], k = 2 -> [5,5]. Ties must
      never trigger a pop (strict '>' comparison, not '>=').
    - Strictly increasing array, e.g. [1,2,3,4], k = 2 -> [1,2].
      Nothing should ever get popped because nothing decreases.
    - Strictly decreasing array, e.g. [4,3,2,1], k = 2 -> [2,1].
      Every earlier, larger element gets popped as long as enough
      elements remain to still reach length k.
    - Large input size (10^5) -> must be near-linear; an O(n^2)
      brute force will time out.

------------------------------------------------------------------
4. ALL MEANINGFULLY DIFFERENT APPROACHES
------------------------------------------------------------------

--------------------------------------------------------------
Approach A (Brute Force / Greedy-with-scan): Repeated Min Scan
--------------------------------------------------------------
INTUITION (taught from scratch):
Think about building the answer one position at a time. For the
very first output element, we're allowed to pick from a "search
window" of the array: we must leave enough elements *after* our pick
to still fill up the remaining k-1 slots. If nums has n elements and
we need k total, and we've already picked p elements, our search
window for the next pick starts right after the previous pick and
ends at index `n - (k - p)` inclusive (leaving exactly enough tail
elements).

Within that allowed window, the most competitive choice is simply
the smallest value available (and among duplicates, the leftmost
one, since picking the leftmost minimum leaves the most elements
behind for future picks). So: scan the window, find the minimum,
record it, then move the window to just after that minimum's index,
and shrink... actually widen the window's right edge by one (since
one fewer element needs to be reserved for the future).

ALGORITHM:
1. l = 0, r = n - k (this is the initial right boundary of the
   search window for the first pick).
2. While r < n (we still have picks to make):
   a. Find the minimum value in nums[l..r] and its leftmost index.
   b. Append that minimum to the output.
   c. Move l to just after that minimum's index.
   d. Increment r by 1 (window widens because one fewer future pick
      is owed).
3. Return output.

This is exactly the user's first submitted solution:

    class Solution:
        def mostCompetitive(self, nums: List[int], k: int) -> List[int]:
            n = len(nums)
            l, r = 0, n - k
            output = []
            while r < n:
                min_val = min(nums[l : r + 1])
                min_index = nums.index(min_val, l)
                output.append(min_val)
                l = min_index + 1
                r += 1
            return output

WHY IT WORKS:
- The window [l, r] always represents exactly the valid range to
  pick from, given how many picks remain and how many trailing
  elements must be preserved.
- Picking the smallest available value greedily is optimal because
  the comparison rule is lexicographic: the earliest differing
  position dominates the outcome, so minimizing every position (in
  order, subject to feasibility) is exactly the definition of
  "most competitive."
- Using `nums.index(min_val, l)` picks the *leftmost* occurrence of
  the minimum, which is important: leaving more room after it gives
  more flexibility (and correctness) for future picks.

WHY A BETTER APPROACH MAY EXIST:
- `min(nums[l:r+1])` re-scans a slice on every iteration, and
  `nums.index(...)` scans again to relocate it. Each of the k
  iterations can look at O(n) elements in the worst case (e.g. a
  strictly decreasing array forces r to grow across nearly the
  whole array while l barely moves), giving O(n*k) time overall,
  which degrades to O(n^2) when k is close to n. This is too slow
  for n up to 10^5.
- Slicing (`nums[l:r+1]`) also creates new list objects repeatedly,
  adding avoidable overhead.

TIME COMPLEXITY: O(n * k) worst case (each of k output positions can
scan up to O(n) elements for the min and the index lookup).
SPACE COMPLEXITY: O(k) for the output (ignoring temporary slices);
O(n) extra if you count the slice copies.

------------------------------------------------------
Approach B (Optimal): Monotonic Stack (Greedy + Stack)
------------------------------------------------------
INTUITION (taught from scratch):
We still want the same greedy idea — at each step prefer smaller
numbers as early as possible — but instead of re-scanning a window
every time, we process nums left to right *once* and maintain a
stack that always holds the "best so far" prefix of the answer.

For each new number `num` at index `idx`:
- While the stack is non-empty AND the top of the stack is strictly
  greater than `num` AND we can still afford to remove it (i.e.
  after removing it we would still be able to collect k elements
  total, counting what's left in `stack` after popping plus all
  the elements from idx to the end that haven't been processed yet)
  → pop the stack. Popping a larger element in favor of a smaller
  upcoming one always makes the sequence more competitive.
- Push `num` onto the stack.
- If the stack now exceeds size k, pop the extra (this only happens
  when we're forced to push without being able to remove enough,
  but we cap the stack length defensively).

The "afford to remove" check is: `len(stack) - 1 + remaining >= k`,
where `remaining` is the count of elements strictly after `idx`
(i.e., `len(nums) - idx - 1`). This guarantees that even after
popping, there are still enough future elements to reach length k.

ALGORITHM:
1. stack = []
2. For idx, num in enumerate(nums):
     remaining = len(nums) - idx - 1
     while stack and stack[-1] > num and (len(stack) - 1) + remaining >= k:
         stack.pop()
     stack.append(num)
3. Return stack[:k]  (or ensure the stack never exceeds k during
   the loop, as in the user's version below).

This is exactly the user's second submitted solution:

    class Solution:
        def mostCompetitive(self, nums: List[int], k: int) -> List[int]:
            stack = []
            for idx, num in enumerate(nums):
                remaining = len(nums) - idx - 1
                while stack and stack[-1] > num and len(stack) + remaining >= k:
                    stack.pop()
                stack.append(num)
                if len(stack) > k:
                    stack.pop()
            return stack

Note: the condition here is written as
`len(stack) + remaining >= k` (checked *before* popping, i.e. using
the stack length that still includes the element about to be
popped). This is equivalent to the "afford to remove" check above:
if we pop, the new stack size is `len(stack) - 1`, and we need
`(len(stack) - 1) + remaining >= k - 1` for it to still be possible
to finish (we need k - 1 *more* elements after this pop, since num
itself will be pushed right after). Both `len(stack) + remaining >= k`
and `(len(stack)-1) + remaining >= k-1` simplify to the same
inequality, so the user's version is correct — just phrased in
terms of "total elements that could still exist" rather than
"elements still needed."

WHY IT WORKS (monotonic stack invariant):
- The stack is maintained to be as "non-decreasing as possible from
  left to right" — we only allow a larger element to be removed in
  favor of a smaller one when it's safe (enough elements remain to
  hit length k).
- Each element is pushed exactly once and popped at most once, so
  the total work across the whole loop (not per-iteration) is
  bounded — this is the classic monotonic-stack amortized analysis.
- The final `if len(stack) > k: stack.pop()` is a safety net for
  the case where popping wasn't allowed (not enough remaining
  elements) but the stack still temporarily exceeds k right after a
  push; trimming from the end keeps only the first k competitive
  choices made so far. In practice, because of the "remaining"
  guard in the while-condition, the stack never grows more than 1
  past k, so this single trim is sufficient.

WHY THIS IS OPTIMAL:
- Every element of nums is looked at once when it's pushed, and
  popped at most once total across the entire algorithm (not once
  per outer iteration) — this is what makes it O(n) rather than
  O(n*k). The `while` loop looks like nested iteration, but the
  amortized cost is O(1) per element because a popped element is
  gone for good.

TIME COMPLEXITY: O(n) — amortized; each element is pushed once and
popped at most once across the whole run.
SPACE COMPLEXITY: O(k) — the stack never holds more than k+1
elements at any point (before the trim), and the output is size k.

------------------------------------------------------------------
5. APPROACH COMPARISON
------------------------------------------------------------------

| Approach                        | Main Idea                                                                 | Time Complexity | Space Complexity | Advantages                                              | Disadvantages                                        | Difficulty | Interview Suitability |
|----------------------------------|----------------------------------------------------------------------------|------------------|-------------------|-----------------------------------------------------------|---------------------------------------------------------|------------|------------------------|
| A. Repeated Min-Scan (windowed)  | Repeatedly find min in a shrinking/widening valid window                  | O(n * k)         | O(k) (+O(n) slices) | Very intuitive; easy to explain and prove correct first    | Too slow for n up to 1e5 when k is large (worst case n^2) | Easy       | Good as a warm-up, not as final answer |
| B. Monotonic Stack               | Greedily build an increasing stack, popping larger elements when safe     | O(n) amortized   | O(k)              | Optimal, elegant, standard interview pattern               | The "can we still reach k" guard is easy to get subtly wrong | Medium     | Excellent — this is the expected optimal solution |

------------------------------------------------------------------
6. BEST INTERVIEW APPROACH & DSA PATTERN
------------------------------------------------------------------
BEST APPROACH: Approach B — the Monotonic Stack.

UNDERLYING PATTERN: "Monotonic Stack for Lexicographically Smallest
Subsequence under a length constraint." This is the same family as
problems like "Remove K Digits" (LeetCode 402) and "Smallest
Subsequence of Distinct Characters" (LeetCode 316).

CLUES THAT REVEAL THE PATTERN:
- The problem asks for the "most competitive" / "smallest" result
  under lexicographic-style comparison.
- We're choosing a *subsequence* (order-preserving), not a subset.
- There's a length constraint (exactly k elements), which becomes
  the "can we still afford to remove this?" feasibility check.
- The greedy intuition "smaller elements earlier are always better,
  as long as we don't run out of remaining elements" is the
  hallmark of a monotonic (increasing) stack.

WHY THIS PATTERN IS APPROPRIATE:
Because comparisons are decided by the *first* differing position,
any local improvement (swapping a bigger earlier element for a
smaller later one) can only help or be neutral — never hurt — as
long as it doesn't jeopardize hitting the required final length.
That "never hurts unless it breaks feasibility" property is exactly
what a monotonic stack with a feasibility guard captures.

HOW TO RECOGNIZE THIS PATTERN IN FUTURE PROBLEMS:
Look for phrases like "smallest/largest possible sequence/number",
"remove exactly/at most X elements", "subsequence", and lexicographic
comparison. Whenever you want to greedily prefer smaller (or larger)
values earlier while preserving relative order and respecting a
count constraint, reach for a monotonic stack with a "remaining
elements" feasibility check on every pop.

RECOMMENDED INTERVIEW-SOLVING PROGRESSION:
1. Start by explaining the brute-force windowed-min idea (Approach
   A) out loud to show you understand *why* greedy-smallest-first
   is correct — this earns "correctness" credit fast.
2. Point out the O(n*k) inefficiency and that repeated scans are
   the bottleneck.
3. Introduce the monotonic stack: "instead of re-scanning, process
   once and maintain the best prefix so far, popping only when
   it's safe."
4. Write Approach B, and explicitly narrate the feasibility
   condition (`len(stack) + remaining >= k`) since that's the part
   interviewers probe hardest.
5. Dry-run a small example on the whiteboard to demonstrate
   correctness and the amortized O(n) bound.

------------------------------------------------------------------
7. FOLLOW-UP QUESTIONS
------------------------------------------------------------------
- "What if we wanted the LEAST competitive (lexicographically
  largest) subsequence of length k instead?"
  -> Flip the comparison in the while-loop: pop while
  `stack[-1] < num` instead of `> num`.

- "What if nums could contain negative numbers?"
  -> No change needed; the comparisons (`>`, `<`) work identically
  for negative integers. The algorithm doesn't rely on non-negativity.

- "What if k could be 0?"
  -> The result should be an empty list. Both algorithms would need
  a guard: Approach B already handles it naturally (the loop never
  finds room to push if the trimming logic caps at k=0 — worth
  explicitly testing), while Approach A's initial `r = n - k` would
  just equal n, so the while condition `r < n` is false immediately
  and an empty list is returned correctly with no special-casing.

- "Can you solve this without extra space (in-place)?"
  -> The stack itself can be built directly inside a prefix of
  `nums` (using two pointers to overwrite as we go), achieving O(1)
  extra space beyond the input array, though this sacrifices some
  readability.

- "What if elements are streamed one at a time and you don't know
  the total length n in advance?"
  -> The monotonic stack approach breaks down because the
  "remaining" feasibility check requires knowing how many elements
  are left. You'd need either a two-pass approach (first pass to
  get n) or a different online algorithm with weaker guarantees.

- "How would you prove the greedy choice is optimal (exchange
  argument)?"
  -> Suppose an optimal answer keeps a larger element `x` over a
  later smaller element `y` at the first position where our greedy
  answer differs from it, while it's still feasible to swap x for y
  and still complete a valid length-k subsequence. Then swapping
  x -> y produces a strictly more competitive sequence (since y < x
  at the first differing position), contradicting optimality of the
  original answer. Hence greedy must match the optimal choice at
  every step where a swap is feasible.

------------------------------------------------------------------
IMPLEMENTATIONS
------------------------------------------------------------------
"""

from typing import List


class Solution:
    def mostCompetitive_bruteForce(self, nums: List[int], k: int) -> List[int]:
        """Approach A: Repeated Min-Scan over a shrinking/widening window.
        Time: O(n*k) worst case | Space: O(k)
        """
        n = len(nums)
        l, r = 0, n - k
        output = []
        while r < n:
            min_val = min(nums[l:r + 1])
            min_index = nums.index(min_val, l)
            output.append(min_val)
            l = min_index + 1
            r += 1
        return output

    def mostCompetitive(self, nums: List[int], k: int) -> List[int]:
        """Approach B (Optimal): Monotonic Stack.
        Time: O(n) amortized | Space: O(k)
        """
        stack = []
        n = len(nums)
        for idx, num in enumerate(nums):
            remaining = n - idx - 1
            while stack and stack[-1] > num and len(stack) + remaining >= k:
                stack.pop()
            stack.append(num)
            if len(stack) > k:
                stack.pop()
        return stack


# ------------------------------------------------------------------
# TEST CASES
# ------------------------------------------------------------------
if __name__ == "__main__":
    sol = Solution()

    tests = [
        # (nums, k, expected)
        ([3, 5, 2, 6], 2, [2, 6]),
        ([2, 4, 3, 3, 5, 4, 9, 6], 4, [2, 3, 3, 4]),
        ([1, 2, 3, 4], 2, [1, 2]),                # strictly increasing
        ([4, 3, 2, 1], 2, [2, 1]),                # strictly decreasing
        ([5, 5, 5, 5], 2, [5, 5]),                # all duplicates
        ([1, 2, 3, 4], 4, [1, 2, 3, 4]),          # k == len(nums)
        ([9, 1, 8, 2, 7, 3], 1, [1]),             # k == 1 -> global-ish min feasible
    ]

    for nums, k, expected in tests:
        got_optimal = sol.mostCompetitive(list(nums), k)
        got_brute = sol.mostCompetitive_bruteForce(list(nums), k)
        status_opt = "PASS" if got_optimal == expected else "FAIL"
        status_brute = "PASS" if got_brute == expected else "FAIL"
        print(f"nums={nums}, k={k} -> expected={expected}")
        print(f"  Optimal (stack) : {got_optimal}  [{status_opt}]")
        print(f"  Brute (min-scan): {got_brute}  [{status_brute}]")