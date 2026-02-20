import math
from collections import deque
from functools import lru_cache

# =============================================================================
# PROBLEM: Least Number of Perfect Squares that Sum to n (LeetCode 279)
# =============================================================================
# Given a positive integer n, return the minimum number of perfect squares
# (e.g. 1, 4, 9, 16, ...) that sum to n.
# =============================================================================


# -----------------------------------------------------------------------------
# VERSION 1 — Backtracking (Naive, TLE)
# -----------------------------------------------------------------------------
# ⚠️  BUG:   idx > (n // 2) is a wrong upper bound. Should be sqrt(n).
#             Won't cause wrong answers but allows far too many iterations.
# ⚠️  PERF:  Stores full `path` list just to call len() — wasteful.
# ⚠️  PERF:  No `count > min_required` pruning, so dead branches are explored.
# -----------------------------------------------------------------------------
class SolutionV1:
    def numSquares(self, n: int) -> int:
        min_required = math.inf

        if n == 1:
            return 1

        def backtrack(idx, path, curr):
            nonlocal min_required
            if curr == n:
                min_required = min(min_required, len(path))
                return
            if curr > n or idx > (n // 2):   # ⚠️ wrong pruning limit
                return
            path.append(idx)
            backtrack(idx, path, curr + idx * idx)
            path.pop()
            backtrack(idx + 1, path, curr)

        backtrack(1, [], 0)
        return min_required


# -----------------------------------------------------------------------------
# VERSION 2 — Backtracking with Better Pruning
# -----------------------------------------------------------------------------
# ✅  Fixed:  idx > math.sqrt(n) is the correct upper bound.
# ✅  Fixed:  count > min_required prunes branches worse than current best.
# ✅  Fixed:  tracking `count` (int) instead of a list.
# ⚠️  STILL:  Exponential in worst case — same (idx, curr) states are
#             recomputed with no memory. Memoization/DP solves this.
# -----------------------------------------------------------------------------
class SolutionV2:
    def numSquares(self, n: int) -> int:
        min_required = math.inf

        if n == 1:
            return 1

        def backtrack(idx, count, curr):
            nonlocal min_required
            if curr == n:
                min_required = min(min_required, count)
                return
            if curr > n or idx > math.sqrt(n) or count > min_required:
                return
            backtrack(idx, count + 1, curr + idx * idx)
            backtrack(idx + 1, count, curr)

        backtrack(1, 0, 0)
        return min_required


# -----------------------------------------------------------------------------
# VERSION 3 — Bottom-Up DP ✅  (Recommended)
# -----------------------------------------------------------------------------
# 💡  Intuition: dp[target] = min squares that sum to `target`.
#     For each target, subtract every perfect square s² that fits,
#     and build on the already-solved subproblem dp[target - s²].
#
# ✅  Time:  O(n * sqrt(n))
# ✅  Space: O(n)
# ⚠️  Minor: `square = []` before the inner loop was dead code (removed).
# -----------------------------------------------------------------------------
class SolutionV3:
    def numSquares(self, n: int) -> int:
        dp = [n] * (n + 1)   # worst case: all 1²s → dp[i] = i
        dp[0] = 0             # base case: 0 squares needed to reach 0

        for target in range(1, n + 1):
            for s in range(1, target + 1):
                sq = s * s
                if sq > target:
                    break
                dp[target] = min(dp[target], 1 + dp[target - sq])

        return dp[n]


# -----------------------------------------------------------------------------
# VERSION 4 — Top-Down DP with Memoization
# -----------------------------------------------------------------------------
# 💡  Same recurrence as bottom-up DP but driven by recursion.
#     memo[remaining] = min squares needed to sum to `remaining`.
#     lru_cache ensures each subproblem is solved exactly once.
#
# 💡  Key insight: once dp(X) is computed, every future call to dp(X)
#     is an O(1) lookup — this is what collapses exponential backtracking
#     down to O(n * sqrt(n)).
#
# ✅  Time:  O(n * sqrt(n))
# ✅  Space: O(n)  (call stack + cache)
# -----------------------------------------------------------------------------
class SolutionV4:
    def numSquares(self, n: int) -> int:
        squares = [s * s for s in range(1, int(n ** 0.5) + 1)]

        @lru_cache(maxsize=None)
        def dp(remaining):
            if remaining == 0:
                return 0
            min_count = remaining           # worst case: all 1s
            for sq in squares:
                if sq > remaining:
                    break
                min_count = min(min_count, 1 + dp(remaining - sq))
            return min_count

        return dp(n)


# -----------------------------------------------------------------------------
# VERSION 5 — BFS (Graph Shortest Path) 🔥
# -----------------------------------------------------------------------------
# 💡  Intuition: reframe as a graph problem.
#     - Nodes   : integers 0 … n
#     - Edges   : x → x + s²  for every perfect square s²
#     - Goal    : shortest path from node 0 to node n
#     BFS explores level by level, where each level = one more square added.
#     The FIRST time we reach n, that depth is guaranteed to be the minimum.
#
# 💡  Why elegant?
#     - No recurrence to reason about — BFS correctness is self-evident.
#     - visited set ensures each node is processed at most once.
#
# ✅  Time:  O(n * sqrt(n))
# ✅  Space: O(n)
# -----------------------------------------------------------------------------
class SolutionV5:
    def numSquares(self, n: int) -> int:
        squares = [s * s for s in range(1, int(n ** 0.5) + 1)]

        visited = {0}
        queue = deque([0])
        depth = 0

        while queue:
            depth += 1
            for _ in range(len(queue)):
                curr = queue.popleft()
                for sq in squares:
                    nxt = curr + sq
                    if nxt == n:
                        return depth        # 🎯 first hit = minimum
                    if nxt < n and nxt not in visited:
                        visited.add(nxt)
                        queue.append(nxt)

        return depth


# =============================================================================
# QUICK TEST
# =============================================================================
if __name__ == "__main__":
    test_cases = [
        (12, 3),   # 4+4+4
        (13, 2),   # 4+9
        (1,  1),
        (4,  1),
        (100, 1),  # 10²
    ]

    versions = [SolutionV1, SolutionV2, SolutionV3, SolutionV4, SolutionV5]
    labels   = ["V1 Backtrack (naive)",
                "V2 Backtrack (pruned)",
                "V3 Bottom-Up DP",
                "V4 Memo Top-Down",
                "V5 BFS"]

    print(f"{'':30} " + "  ".join(f"n={n}" for n, _ in test_cases))
    print("-" * 70)
    for label, cls in zip(labels, versions):
        results = [cls().numSquares(n) for n, _ in test_cases]
        passed  = all(r == exp for r, (_, exp) in zip(results, test_cases))
        status  = "✅" if passed else "❌"
        print(f"{status} {label:28} " + "  ".join(f"{'':3}{r}" for r in results))