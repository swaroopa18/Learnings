"""
LEETCODE 79 - WORD SEARCH
==========================================================================
PROBLEM STATEMENT
--------------------------------------------------------------------------
Given an m x n grid of characters `board` and a string `word`, return
True if `word` exists in the grid.

The word can be constructed from letters of sequentially adjacent cells,
where "adjacent" cells are horizontally or vertically neighboring. The
same cell may not be used more than once *within the same path*.

Example:
    board = [["A","B","C","E"],
             ["S","F","C","S"],
             ["A","D","E","E"]]
    word  = "ABCCED"   -> True
    word  = "SEE"      -> True
    word  = "ABCB"     -> False  (the second 'B' would reuse the first B)

==========================================================================
CORE IDEA: BACKTRACKING (DFS WITH UNDO)
--------------------------------------------------------------------------
This is a classic "search + undo" (backtracking) problem, not a pure
graph-traversal problem, because:

  1. We are not just checking reachability - we must match the board
     letters to the word letters IN ORDER.
  2. A cell can be reused across *different* attempts, but not within
     the SAME path. That's why we mark a cell as visited before
     recursing and UNMARK it (undo) after we return from that
     recursive call - this is the defining trait of backtracking.

Think of it as: "try a move, explore fully, then take the move back so
the board is clean for the next attempt."

We try every cell in the grid as a possible starting point for
word[0], and from each start we DFS in the 4 directions, matching one
character of `word` per step.

==========================================================================
"""

from typing import List


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        ROWS, COLS = len(board), len(board[0])

        # `visited` tracks cells that are part of the CURRENT path being
        # explored. It gets a cell added right before recursing deeper,
        # and that same cell removed right after we return - that
        # add-then-remove pattern is the "backtrack" step.
        visited = set()

        def backtrack(r: int, c: int, idx: int) -> bool:
            """
            Try to match word[idx:] starting from board[r][c].

            r, c  -> current cell being checked
            idx   -> index into `word` we are currently trying to match
            """

            # BASE CASE: we've successfully matched every character.
            if idx == len(word):
                return True

            # PRUNE / FAIL CASES:
            #   - out of grid bounds
            #   - cell already used in this path
            #   - letter mismatch
            if (
                r < 0
                or c < 0
                or r >= ROWS
                or c >= COLS
                or (r, c) in visited
                or board[r][c] != word[idx]
            ):
                return False

            # CHOOSE: mark this cell as used for the current path.
            visited.add((r, c))

            # EXPLORE: try to extend the match in all 4 directions.
            # Short-circuit `or` means we stop at the first direction
            # that leads to a full match - a natural pruning benefit.
            answer = (
                backtrack(r + 1, c, idx + 1)
                or backtrack(r, c + 1, idx + 1)
                or backtrack(r - 1, c, idx + 1)
                or backtrack(r, c - 1, idx + 1)
            )

            # UN-CHOOSE (undo): whether we succeeded or failed, remove
            # this cell from `visited` before returning, so sibling
            # branches / other starting points can reuse it.
            visited.remove((r, c))

            return answer

        # Try every cell as a possible start of the word.
        for i in range(ROWS):
            for j in range(COLS):
                if backtrack(i, j, 0):
                    return True

        return False


"""
==========================================================================
COMPLEXITY ANALYSIS (of the code above)
--------------------------------------------------------------------------
Let:
    N = number of rows      (ROWS)
    M = number of columns   (COLS)
    L = len(word)

TIME COMPLEXITY:  O(N * M * 4^L)
    - We attempt a start at every one of the N*M cells:            O(N*M)
    - From each start, in the worst case the DFS branches into up
      to 4 directions at every one of the L characters we still
      need to match:                                                O(4^L)
    - Combined (start loop x DFS work per start):        O(N * M * 4^L)

    In practice this is a big overestimate - the branching factor is
    really <=3 after the first step (we don't go back the way we
    came... except this particular implementation DOES allow
    revisiting the parent direction, it just immediately fails
    because that cell is already in `visited`). Also, mismatched
    letters prune branches immediately, so real-world runtime is
    usually far below the worst case.

SPACE COMPLEXITY:  O(L)
    - `visited` holds at most L cells at any moment (one path's
      worth of cells), since we undo (remove) as we backtrack.
    - The recursion call stack also goes at most L frames deep.
    - (We don't count the input `board` itself as extra space.)

==========================================================================
IS THERE A BETTER SOLUTION?
--------------------------------------------------------------------------
Asymptotically, backtracking is essentially required here - Word Search
is NP-hard-flavored in the sense that there's no known way to avoid
exploring a search tree in the worst case, so no solution will beat
O(N * M * 4^L) in the *worst case* by changing algorithmic paradigm.

That said, there are two categories of real, meaningful improvements:

  (A) CONSTANT-FACTOR / PRACTICAL SPEEDUPS  (same asymptotic class,
      but noticeably faster in practice and on LeetCode's judge)

      1. Mark visited cells IN-PLACE on the board instead of using a
         Python `set`. Set operations (hashing tuples, add/remove)
         are slow compared to a plain array write. Temporarily
         overwrite board[r][c] with a sentinel like '#' (which can't
         match any real letter), then restore it during backtrack.
         This avoids all the hashing overhead of `visited`.

      2. Early frequency pruning: before searching at all, count the
         letters in `board` and the letters in `word` (via
         collections.Counter). If any letter in `word` appears more
         times than it appears on the whole board, the word can
         never be found - return False immediately, no search needed.

      3. Reverse the word if the last letter is rarer on the board
         than the first letter. Searching from the rarer letter means
         fewer valid starting cells, which prunes the search tree
         faster (fail fast).

      4. Bound checking without extra `visited` lookups by folding
         the bounds/letter checks into the recursive call signature
         itself (already done above), and returning as early as
         possible.

  (B) DIFFERENT DATA STRUCTURE FOR MANY WORDS (Word Search II style)
      If you needed to search for a *list* of many words in the same
      board (LeetCode 212 - Word Search II) rather than just one,
      doing a fresh DFS per word is wasteful - O(K * N * M * 4^L) for
      K words. The standard trick there is to build a TRIE out of all
      K words first, then do a SINGLE combined DFS/backtracking pass
      over the board, walking the trie alongside the board so that
      common prefixes across words are explored only once. This
      changes the complexity to depend on the trie's total size
      rather than re-searching from scratch per word.

Below is an optimized single-word version implementing improvements
(A.1) and (A.2), which is the most impactful "better solution" for
this exact problem (LeetCode 79) while keeping the same worst-case
asymptotic bound.
==========================================================================
"""

from collections import Counter


class OptimizedSolution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        ROWS, COLS = len(board), len(board[0])

        # --- Improvement 1: Early pruning via letter frequency ---
        # If the board doesn't even contain enough copies of some
        # letter that `word` needs, there's no point searching at all.
        board_counts = Counter(ch for row in board for ch in row)
        word_counts = Counter(word)
        for ch, needed in word_counts.items():
            if board_counts[ch] < needed:
                return False

        # --- Improvement 2: Search from the rarer end of the word ---
        # If the board has fewer copies of word's last letter than its
        # first letter, reversing `word` means we start our DFS from
        # cells that are rarer on the board -> fewer starting points
        # to try -> faster failure/success on average.
        if board_counts[word[0]] > board_counts[word[-1]]:
            word = word[::-1]

        L = len(word)

        def backtrack(r: int, c: int, idx: int) -> bool:
            if idx == L:
                return True
            if (
                r < 0
                or c < 0
                or r >= ROWS
                or c >= COLS
                or board[r][c] != word[idx]
            ):
                return False

            # --- Improvement 3: mark in-place instead of a set ---
            temp = board[r][c]
            board[r][c] = "#"  # sentinel: matches no real letter

            found = (
                backtrack(r + 1, c, idx + 1)
                or backtrack(r, c + 1, idx + 1)
                or backtrack(r - 1, c, idx + 1)
                or backtrack(r, c - 1, idx + 1)
            )

            board[r][c] = temp  # undo (restore the original letter)
            return found

        for i in range(ROWS):
            for j in range(COLS):
                if backtrack(i, j, 0):
                    return True
        return False


class OptimizedSolution2:
    def exist(self, board: List[List[str]], word: str) -> bool:
        ROWS, COLS, L = len(board), len(board[0]), len(word)
        # Pruning 1
        if L > ROWS * COLS:
            return False

        # Pruning 2
        board_counts = Counter(ch for row in board for ch in row)
        word_counts = Counter(word)
        for ch, needed in word_counts.items():
            if board_counts[ch] < needed:
                return False

        # Pruning 3
        if board_counts[word[0]] > board_counts[word[-1]]:
            word = word[::-1]

        def backtrack(r, c, idx):
            if idx == L:
                return True
            if r < 0 or c < 0 or r >= ROWS or c >= COLS or board[r][c] != word[idx]:
                return False

            board[r][c] = "#"
            answer = (
                backtrack(r + 1, c, idx + 1)
                or backtrack(r, c + 1, idx + 1)
                or backtrack(r - 1, c, idx + 1)
                or backtrack(r, c - 1, idx + 1)
            )
            board[r][c] = word[idx]
            return answer

        for i in range(ROWS):
            for j in range(COLS):
                if board[i][j] == word[0] and backtrack(i, j, 0):
                    return True
        return False


"""
--------------------------------------------------------------------------
COMPLEXITY OF THE OPTIMIZED VERSION
--------------------------------------------------------------------------
TIME:  Still O(N * M * 4^L) worst case (unchanged asymptotically),
       but with a much smaller constant factor:
         - No hashing/set overhead per cell (in-place marking instead).
         - Whole searches can be skipped entirely via the frequency
           check.
         - Fewer starting points explored on average thanks to
           starting from the rarer letter.

SPACE: O(L) for the recursion stack, and O(1) EXTRA space beyond that
       (aside from the small Counter objects, which use O(1) space
       since the alphabet is bounded) - we no longer need the
       `visited` set at all, because the board array itself is
       reused as the "visited" marker.
"""





