"""
========================================================
LeetCode 6 - ZigZag Conversion
========================================================

PROBLEM:
    Write the string "PAYPALISHIRING" in a zigzag pattern on a
    given number of rows and then read line by line.

    Example with numRows = 3:
        P   A   H   N
        A P L S I I G
        Y   I   R
    Output: "PAHNAPLSIIGYIR"

    Example with numRows = 4:
        P     I    N
        A   L S  I G
        Y A   H R
        P     I
    Output: "PINALSIGYAHRPI"

========================================================
APPROACH 1 — Column Matrix (Your Original Solution)
========================================================

IDEA:
    Simulate the zigzag by building a 2D list of columns.
    - Even columns: fill top-to-bottom (indices 0 → numRows-1)
    - Odd columns: fill bottom-to-top (indices numRows-2 → 1)
    Then read row by row to get the result.

COMPLEXITY:
    Time  : O(n)  — each character is visited twice (write + read)
    Space : O(n * numRows) — the 2D output matrix
              ↑ Much worse than needed; most cells are 0 (wasted space)

ISSUES FIXED vs YOUR VERSION:
    1. Removed debug `print(output, col)` statement.
    2. Used `None` instead of `0` as the empty sentinel so digits/
       special characters in `s` don't get skipped silently.
    3. Added early return for numRows == 1 (no zigzag needed).
"""

class SolutionMatrix:
    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1 or numRows >= len(s):
            return s

        output = []
        col = 0
        i = 0

        while i < len(s):
            output.append([None] * numRows)          

            if col % 2 == 0:                         # downward column
                idx = 0
                while idx < numRows and i < len(s):
                    output[col][idx] = s[i]
                    i += 1
                    idx += 1
            else:                                    # diagonal column (upward)
                idx = numRows - 2
                while idx > 0 and i < len(s):
                    output[col][idx] = s[i]
                    i += 1
                    idx -= 1
            col += 1

        result = []
        for row in range(numRows):
            for c in range(len(output)):
                if output[c][row] is not None:
                    result.append(output[c][row])

        return "".join(result)


"""
========================================================
APPROACH 2 — Row Accumulator (Your Optimised Solution) ✅ BEST
========================================================

IDEA:
    Maintain one string per row. Walk through `s`, appending each
    character to the current row's string. Use a `step` variable
    (+1 or -1) to bounce direction at the top and bottom rows.

COMPLEXITY:
    Time  : O(n)  — single pass through s
    Space : O(n)  — only the rows[] list (total characters = n)

WHY IT'S BETTER:
    - No wasted empty cells like Approach 1.
    - Cleaner, shorter, and more Pythonic.
    - Handles edge cases (numRows == 1) with a single early return.

VISUAL TRACE (s="PAYPALISHIRING", numRows=3):
    row=0  step=+1  → P
    row=1  step=+1  → A
    row=2  step=-1  → Y  (hit bottom, flip)
    row=1  step=-1  → P
    row=0  step=+1  → A  (hit top, flip)
    ...
    rows = ["PAHN", "APLSIIG", "YIR"]
    result = "PAHNAPLSIIGYIR" ✓
"""

class SolutionRows:
    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1 or numRows >= len(s):        # edge case
            return s

        rows = [""] * numRows
        row = 0
        step = 1                                     # start going down

        for ch in s:
            rows[row] += ch

            if row == 0:
                step = 1                             # hit top → go down
            elif row == numRows - 1:
                step = -1                            # hit bottom → go up

            row += step

        return "".join(rows)


"""
========================================================
APPROACH 3 — Mathematical Index Mapping (No simulation)
========================================================

IDEA:
    Each "cycle" of zigzag has length  cycle = 2 * (numRows - 1).
    For each row r, the characters that belong to it can be
    calculated directly using modular arithmetic — no simulation needed.

    For row r (0-indexed):
        - First character in each cycle: index  r
        - Second character (diagonal, exists only for 0 < r < numRows-1):
              index  cycle - r

    We collect these by jumping cycle positions at a time.

COMPLEXITY:
    Time  : O(n)  — each character accessed exactly once
    Space : O(n)  — result list

ADVANTAGE OVER APPROACH 2:
    No auxiliary `rows[]` list needed; builds result directly.
    Slightly more complex to read but demonstrates the math clearly.
"""

class SolutionMath:
    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1 or numRows >= len(s):
            return s

        cycle = 2 * (numRows - 1)
        result = []

        for r in range(numRows):
            for j in range(r, len(s), cycle):
                result.append(s[j])                  # first char of cycle

                # diagonal character (only for middle rows)
                diag = j + cycle - 2 * r
                if 0 < r < numRows - 1 and diag < len(s):
                    result.append(s[diag])

        return "".join(result)


"""
========================================================
COMPARISON SUMMARY
========================================================

┌──────────────────┬────────────┬────────────┬──────────────────────────┐
│ Approach         │ Time       │ Space      │ Notes                    │
├──────────────────┼────────────┼────────────┼──────────────────────────┤
│ 1. Matrix        │ O(n)       │ O(n·rows)  │ Intuitive but wasteful   │
│ 2. Row Accum ✅  │ O(n)       │ O(n)       │ Clean, Pythonic, simple  │
│ 3. Math Index    │ O(n)       │ O(n)       │ No aux rows, clever math │
└──────────────────┴────────────┴────────────┴──────────────────────────┘

RECOMMENDATION:
    Use Approach 2 in interviews — it's the easiest to explain and code
    under pressure. Use Approach 3 to impress with mathematical thinking.

EDGE CASES TO ALWAYS HANDLE:
    - numRows == 1  → return s as-is (no zigzag)
    - numRows >= len(s)  → return s as-is (single column)
    - Empty string → returns "" naturally
"""

# ======================================================
# TESTS
# ======================================================
if __name__ == "__main__":
    test_cases = [
        ("PAYPALISHIRING", 3, "PAHNAPLSIIGYIR"),
        ("PAYPALISHIRING", 4, "PINALSIGYAHRPI"),
        ("A",              1, "A"),
        ("AB",             1, "AB"),
        ("AB",             2, "AB"),
    ]

    solutions = [
        ("Matrix (Approach 1)",   SolutionMatrix()),
        ("Row Accum (Approach 2)", SolutionRows()),
        ("Math Index (Approach 3)", SolutionMath()),
    ]

    for name, sol in solutions:
        print(f"\n--- {name} ---")
        for s, rows, expected in test_cases:
            result = sol.convert(s, rows)
            status = "✓" if result == expected else "✗"
            print(f"  {status}  convert({s!r}, {rows}) = {result!r}")