```python
"""
================================================================================
 PROBLEM: Check if a Number Is a Palindrome (Recursion)
================================================================================
Given an integer `n`, determine whether it is a palindrome.

A palindrome number reads the same forward and backward.

Examples:
    Input:  n = 121
    Output: True

    Input:  n = 123
    Output: False

    Input:  n = 0
    Output: True

    Input:  n = -121
    Output: False  # Standard definition: negative numbers are not palindromes

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Is the input an integer? (Yes.)
- Are negative numbers allowed? (They may be; clarify how they should be
  treated. Under the standard definition, negative numbers are not palindromes.)
- Can I convert the number to a string? (If the goal is to practise recursion
  and arithmetic, reverse the number using digit extraction instead.)
- Should I return a Boolean or print the result? (Return True or False.)
- Can the number be zero? (Yes, and zero is a palindrome.)
"""

# ================================================================================
# 🔑🔑🔑  STRONG POINTS FOR PALINDROME PROBLEMS  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   REVERSE THE NUMBER USING RECURSION                                │
    │                                                                     │
    │   Last digit:       x % 10                                          │
    │   Remove last digit: x // 10                                        │
    │   Append digit:     rev * 10 + x % 10                               │
    │                                                                     │
    │   A number is a palindrome if its reverse equals the original.     │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

Key ideas:

1. **Extract the last digit:** `x % 10` gives the rightmost digit.

2. **Remove the last digit:** `x // 10` removes the rightmost digit.

3. **Build the reversed number:** Multiply `rev` by 10 and add the extracted
   digit.

4. **Base case:** When x becomes 0, return the reversed number.

5. **Compare:** If the reversed number equals the original number, it is
   a palindrome.

6. **Negative-number handling:** Your original code converts negative inputs
   to positive values. This means `-121` returns True, because its absolute
   value is a palindrome. Under the standard definition, negative numbers
   should return False because the minus sign does not appear at the end.
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Step 1: Understand the recursive helper

The helper function `reverse(x, rev)` has two responsibilities:

- `x`: The remaining digits to process.
- `rev`: The reversed number constructed so far.

Initially, call `reverse(n, 0)`.

### Step 2: Trace isPalindrome(121)

    reverse(121, 0)
        -> reverse(12, 1)
        -> reverse(1, 12)
        -> reverse(0, 121)
        -> return 121

Finally:

    121 == 121 -> True

### Step 3: Trace isPalindrome(123)

    reverse(123, 0)
        -> reverse(12, 3)
        -> reverse(1, 32)
        -> reverse(0, 321)
        -> return 321

Finally:

    321 == 123 -> False

### The "aha" moment to remember 🎯

The recursive function does not reverse the digits all at once. It extracts
one digit per call and appends it to the reversed number.

The key formula is:

    reverse(x // 10, rev * 10 + x % 10)
"""

# ================================================================================
# APPROACH 1 — Recursive Number Reversal (YOUR APPROACH)
# ================================================================================
"""
### Thought Process 🧠

1. Store the original number.
2. Handle negative numbers according to the problem's definition.
3. Recursively reverse the digits.
4. Compare the reversed number with the original.

### Complexity
Let d be the number of digits in n.

- TC: O(d) — each recursive call processes one digit.
- SC: O(d) — recursive call stack.

Since d = O(log10(n)) for positive n:
- TC: O(log n)
- SC: O(log n)

### Pros
- Uses recursion to reverse the number.
- Does not require string conversion.
- Processes each digit once.

### Cons
- Recursive calls use additional stack space.
- Reversing a negative number using its absolute value changes the usual
  palindrome interpretation.
- Very large inputs may hit Python's recursion limit.

### Important Correction
Your original code uses:

    if n < 0:
        n = -n

That makes `isPalindrome(-121)` return True. If the intended problem follows
the standard definition, return False for negative inputs instead.
"""


class Solution:
    def isPalindrome(self, n):
        if n < 0:
            return False

        def reverse(x, rev):
            if x == 0:
                return rev

            return reverse(x // 10, rev * 10 + x % 10)

        return reverse(n, 0) == n


# ================================================================================
# APPROACH 2 — Iterative Number Reversal
# ================================================================================
"""
### Thought Process 🧠

Use a loop instead of recursion to extract digits and construct the reversed
number.

### Complexity
- TC: O(d) — each digit is processed once.
- SC: O(1) auxiliary space.

### Pros
- Avoids recursion-depth limitations.
- Uses constant auxiliary space.
- Easy to implement and explain.

### Cons
- Does not practise recursion.
"""


def is_palindrome_iterative(n: int) -> bool:
    if n < 0:
        return False

    original = n
    rev = 0

    while n > 0:
        digit = n % 10
        rev = rev * 10 + digit
        n //= 10

    return rev == original


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
PALINDROME NUMBER
│
├── Recursive Approach
│   ├── Extract digit: x % 10
│   ├── Remove digit: x // 10
│   ├── Append digit: rev * 10 + x % 10
│   └── Base case: x == 0
│
├── Final Comparison
│   └── reversed_number == original_number
│
├── Edge Cases
│   ├── 0 -> True
│   ├── 121 -> True
│   ├── 123 -> False
│   └── -121 -> False under the standard definition
│
└── Complexity
    ├── Recursive: O(d) time, O(d) stack space
    └── Iterative: O(d) time, O(1) auxiliary space
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "A palindrome reads the same forward and backward."

- "Use modulo 10 to extract the last digit and integer division by 10 to
  remove it."

- "Build the reverse using rev * 10 + digit."

- "The base case is x == 0, when no digits remain."

- "Save the original number before reversing it if the input variable will
  be modified."

- "Negative-number behaviour depends on the problem definition. Under the
  standard definition, negative numbers are not palindromes."

- "For d digits, reversal takes O(d) time. Recursion uses O(d) stack space,
  while the iterative version uses O(1) auxiliary space."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                  | Core Idea                    | TC   | SC   | Best Use                         |
|--------------------------|------------------------------|------|------|----------------------------------|
| Recursive Number Reversal| Reverse digits recursively   | O(d) | O(d) | Recursion practice               |
| Iterative Number Reversal| Reverse digits with a loop   | O(d) | O(1) | Avoiding recursion overhead      |

Here, d is the number of digits in the input.
"""

# ================================================================================
# INTERVIEW SNAPSHOT
# ================================================================================
"""
- Pattern: Recursion + digit manipulation.
- Key formula: reverse(x // 10, rev * 10 + x % 10).
- Base case: x == 0.
- Final check: reversed number == original number.
- Time complexity: O(d).
- Recursive space complexity: O(d).
- Common bug: converting a negative number to its absolute value and
  accidentally treating a negative palindrome as valid.
- Follow-up: Can you solve it iteratively? Yes, with O(d) time and O(1)
  auxiliary space.
"""
```