# ================================================================================
# PROBLEM: Find Floor and Ceil in a Sorted Array
# ================================================================================
"""
Given:
    - A sorted array `arr` of integers.
    - An integer `x`.

Task:
    1. Find the FLOOR of x:
       The largest element in `arr` that is <= x.

    2. Find the CEIL of x:
       The smallest element in `arr` that is >= x.

Requirements:
    - Return the index (0-based).
    - If multiple occurrences exist:
        * Floor -> return the LAST occurrence.
        * Ceil  -> return the FIRST occurrence.
    - If no valid element exists, return -1.

Example:

    arr = [1, 2, 2, 4, 6, 8]
    x = 2

    Floor:
        largest element <= 2 = 2
        last occurrence = index 2

    Ceil:
        smallest element >= 2 = 2
        first occurrence = index 1

    output:
        floor = 2
        ceil  = 1
"""

# --------------------------------------------------------------------------------
# INTERVIEW CLARIFYING QUESTIONS
# --------------------------------------------------------------------------------
"""
- Is the array sorted? (Yes, in increasing/non-decreasing order.)
- Can duplicate values exist? (Yes.)
- Should we return the value or index? (Index.)
- For duplicate floor values, which index? (Last occurrence.)
- For duplicate ceil values, which index? (First occurrence.)
- What if no floor exists? (Return -1.)
- What if no ceil exists? (Return -1.)
- Is O(log n) expected? (Yes, because the array is sorted.)
"""


# ================================================================================
# 🔑🔑🔑 STRONG POINTS FOR FLOOR AND CEIL PROBLEMS 🔑🔑🔑
# ================================================================================
"""
1. These are both BINARY SEARCH boundary problems.

2. FLOOR:
       Find the largest index `i` such that:
           arr[i] <= x

   Because we want the LAST valid index, whenever we find a valid
   element, we continue searching to the RIGHT.

3. CEIL:
       Find the smallest index `i` such that:
           arr[i] >= x

   Because we want the FIRST valid index, whenever we find a valid
   element, we continue searching to the LEFT.

4. Floor and Ceil are almost mirror images:

   FLOOR:
       arr[mid] <= x
           -> valid answer
           -> save mid
           -> search RIGHT
           -> l = mid + 1

       arr[mid] > x
           -> too large
           -> search LEFT
           -> r = mid - 1


   CEIL:
       arr[mid] >= x
           -> valid answer
           -> save mid
           -> search LEFT
           -> r = mid - 1

       arr[mid] < x
           -> too small
           -> search RIGHT
           -> l = mid + 1

5. The most important thing to remember:

       FLOOR = last position where arr[i] <= x

       CEIL  = first position where arr[i] >= x

6. Do NOT immediately return when arr[mid] == x.

   There may be duplicates.

   Example:
       arr = [1, 2, 2, 2, 5]
       x = 2

   Floor must return index 3.
   Ceil must return index 1.

7. Therefore, even when we find x, we continue searching:
   - Floor -> RIGHT
   - Ceil  -> LEFT
"""


# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea

We could scan the complete array.

For every element:
    - For floor, keep the largest value <= x.
    - For ceil, keep the smallest value >= x.

This takes O(n).

But because the array is sorted, we can do better with binary search.

The goal is to find a BOUNDARY.

-------------------------------------------------------------------------------

### FLOOR

Floor means:

    largest element <= x

Example:

    arr = [1, 2, 2, 4, 6, 8]
    x = 5

Elements <= 5 are:

    [1, 2, 2, 4]

The largest one is:

    4

Its index is:

    3

During binary search:

    if arr[mid] <= x:

        mid is a valid answer.

        But there may be another valid element to the RIGHT.

        Therefore:
            answer = mid
            lower = mid + 1

    else:

        arr[mid] is too large.

        Search LEFT:

            upper = mid - 1

At the end, `answer` contains the last valid index.


-------------------------------------------------------------------------------

### CEIL

Ceil means:

    smallest element >= x

Example:

    arr = [1, 2, 2, 4, 6, 8]
    x = 5

Elements >= 5 are:

    [6, 8]

The smallest one is:

    6

Its index is:

    4

During binary search:

    if arr[mid] >= x:

        mid is a valid answer.

        But there may be another valid element to the LEFT.

        Therefore:
            answer = mid
            upper = mid - 1

    else:

        arr[mid] is too small.

        Search RIGHT:

            lower = mid + 1

At the end, `answer` contains the first valid index.


-------------------------------------------------------------------------------

### The easiest way to remember

FLOOR:

    <= x

    Valid?
       YES -> save + go RIGHT
       NO  -> go LEFT


CEIL:

    >= x

    Valid?
       YES -> save + go LEFT
       NO  -> go RIGHT
"""


# ================================================================================
# ALTERNATIVE APPROACH — Linear Scan
# ================================================================================
"""
### Thought Process

We can simply scan the array.

For every element:

    Floor:
        If arr[i] <= x:
            update answer

    Ceil:
        If arr[i] >= x:
            take the first valid element

Because the array is sorted, this can be implemented easily.

### Complexity

- TC: O(n)
- SC: O(1)

### Pros

- Very easy to understand.
- Easy to implement.
- Useful as a brute-force solution before optimizing.

### Cons

- Does not take advantage of binary search.
- O(n) instead of O(log n).
"""


def find_floor_linear(arr: list[int], x: int) -> int:
    answer = -1

    for i, value in enumerate(arr):
        if value <= x:
            answer = i
        else:
            # Since array is sorted, everything after this is larger.
            break

    return answer


def find_ceil_linear(arr: list[int], x: int) -> int:
    for i, value in enumerate(arr):
        if value >= x:
            return i

    return -1


# ================================================================================
# MY APPROACH — Binary Search for Floor
# ================================================================================
"""
### Idea

Find the LAST index where:

    arr[mid] <= x

Whenever we find a valid element:

    answer = mid

Then search to the RIGHT because we want the largest possible
valid element.

### Conditions

    arr[mid] <= x
        -> valid
        -> save answer
        -> search right

    arr[mid] > x
        -> invalid because it is too large
        -> search left

### Complexity

- TC: O(log n)
- SC: O(1)
"""


def find_floor(arr: list[int], x: int) -> int:
    l, r = 0, len(arr) - 1
    answer = -1

    while l <= r:
        mid = (l + r) // 2

        if arr[mid] <= x:
            # Valid floor candidate.
            answer = mid

            # There may be a larger valid element on the right.
            l = mid + 1

        else:
            # arr[mid] is greater than x.
            # Search on the left.
            r = mid - 1

    return answer


# ================================================================================
# MY APPROACH — Binary Search for Ceil
# ================================================================================
"""
### Idea

Find the FIRST index where:

    arr[mid] >= x

Whenever we find a valid element:

    answer = mid

Then search to the LEFT because we want the smallest possible
valid element.

### Conditions

    arr[mid] >= x
        -> valid
        -> save answer
        -> search left

    arr[mid] < x
        -> invalid because it is too small
        -> search right

### Complexity

- TC: O(log n)
- SC: O(1)
"""


def find_ceil(arr: list[int], x: int) -> int:
    l, r = 0, len(arr) - 1
    answer = -1

    while l <= r:
        mid = (l + r) // 2

        if arr[mid] >= x:
            # Valid ceil candidate.
            answer = mid

            # There may be a smaller valid element on the left.
            r = mid - 1

        else:
            # arr[mid] is smaller than x.
            # Search on the right.
            l = mid + 1

    return answer


# ================================================================================
# FLOOR + CEIL TOGETHER
# ================================================================================
"""
Sometimes an interviewer may ask for both floor and ceil.

We can simply call the two binary-search functions.

Example:

    arr = [1, 2, 2, 4, 6, 8]
    x = 2

    floor = find_floor(arr, x)
    ceil  = find_ceil(arr, x)

    floor = 2
    ceil  = 1
"""


def find_floor_and_ceil(arr: list[int], x: int) -> tuple[int, int]:
    floor_index = find_floor(arr, x)
    ceil_index = find_ceil(arr, x)

    return floor_index, ceil_index


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
FLOOR AND CEIL
│
├── FLOOR
│   │
│   ├── Definition
│   │   └── Largest element <= x
│   │
│   ├── Boundary
│   │   └── Last index where arr[i] <= x
│   │
│   ├── Valid condition
│   │   └── arr[mid] <= x
│   │
│   ├── Valid
│   │   ├── Save answer
│   │   └── Search RIGHT
│   │       └── l = mid + 1
│   │
│   └── Invalid
│       └── arr[mid] > x
│           └── Search LEFT
│               └── r = mid - 1
│
│
└── CEIL
    │
    ├── Definition
    │   └── Smallest element >= x
    │
    ├── Boundary
    │   └── First index where arr[i] >= x
    │
    ├── Valid condition
    │   └── arr[mid] >= x
    │
    ├── Valid
    │   ├── Save answer
    │   └── Search LEFT
    │       └── r = mid - 1
    │
    └── Invalid
        └── arr[mid] < x
            └── Search RIGHT
                └── l = mid + 1
"""


# ================================================================================
# 🔥 MOST IMPORTANT PATTERN TO MEMORIZE
# ================================================================================
"""
                    FLOOR                  CEIL
                    -----                  ----

Goal:               MAX <= x               MIN >= x

Valid condition:    arr[mid] <= x           arr[mid] >= x

When valid:         Save + RIGHT            Save + LEFT

Pointer:             l = mid + 1            r = mid - 1

Other condition:    arr[mid] > x            arr[mid] < x

Other movement:     r = mid - 1             l = mid + 1


Easy memory trick:

    FLOOR -> want something LOWER/equal
             Once valid, try RIGHT for a bigger value.

    CEIL  -> want something HIGHER/equal
             Once valid, try LEFT for a smaller value.
"""


# ================================================================================
# RELATION TO LOWER BOUND / UPPER BOUND
# ================================================================================
"""
These problems are closely related to standard binary-search boundaries.

CEIL:

    First index where:

        arr[i] >= x

    This is exactly the classic LOWER BOUND.

    lower_bound(x) = first position with arr[i] >= x


FLOOR:

    Last index where:

        arr[i] <= x

    This can be viewed as:

        upper_bound(x) - 1

    where upper_bound(x) is the first index with:

        arr[i] > x


Therefore:

    CEIL  = lower_bound(x)

    FLOOR = upper_bound(x) - 1


This relationship is extremely useful in interviews.
"""


# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach          | Floor                         | Ceil                         | TC       | SC   |
|------------------|-------------------------------|------------------------------|----------|------|
| Linear Scan      | Track last <= x               | Return first >= x            | O(n)     | O(1) |
| Binary Search    | Last index where <= x         | First index where >= x       | O(log n) | O(1) |

### Interview recommendation

Use binary search because the array is sorted.

The key is not simply "binary search".

The real pattern is:

    BINARY SEARCH + BOUNDARY

Floor:
    Find RIGHTMOST valid position.

Ceil:
    Find LEFTMOST valid position.
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- FLOOR = largest element <= x.
- CEIL  = smallest element >= x.

- FLOOR asks for the RIGHTMOST valid position.
- CEIL asks for the LEFTMOST valid position.

- Floor condition:
      arr[mid] <= x

- Ceil condition:
      arr[mid] >= x

- Floor valid:
      answer = mid
      l = mid + 1

- Ceil valid:
      answer = mid
      r = mid - 1

- Never immediately return when arr[mid] == x if duplicates are possible.

- `answer = -1` handles the case where no valid element exists.

- Both solutions run in:
      TC: O(log n)
      SC: O(1)

- CEIL is the classic LOWER BOUND:
      first index where arr[i] >= x

- FLOOR is:
      last index where arr[i] <= x
      or equivalently upper_bound(x) - 1
"""


# ================================================================================
# INTERVIEW SNAPSHOT
# ================================================================================
"""
Pattern:
    Binary Search + Boundary Search

FLOOR:
    Largest element <= x
    -> Find RIGHTMOST valid index
    -> Valid: arr[mid] <= x
    -> Move RIGHT

CEIL:
    Smallest element >= x
    -> Find LEFTMOST valid index
    -> Valid: arr[mid] >= x
    -> Move LEFT

Duplicates:
    Floor -> LAST occurrence
    Ceil  -> FIRST occurrence

Complexity:
    O(log n) time
    O(1) auxiliary space

One-line memory trick:

    FLOOR -> <= -> save -> RIGHT
    CEIL  -> >= -> save -> LEFT
"""