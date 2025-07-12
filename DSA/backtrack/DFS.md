**Backtracking** problems (often solved via **DFS**) follow a repeatable *template*. Here’s a clear **mental model + code pattern** to help you master them:

---

## 🔁 **Backtracking = DFS + Undo + Pruning**

### 🧠 Think in terms of:

1. **State**: What defines a node in the DFS tree? (e.g., path, choices left)
2. **Choices**: At each step, what are your valid next moves?
3. **Constraints / Pruning**: Can I skip any branches early?
4. **Goal**: What defines a complete or valid solution?

---

## 📌 Generic Template

```python
def backtrack(path, choices):
    if goal_reached(path):
        results.append(path[:])
        return
    
    for choice in choices:
        if not is_valid(choice, path):
            continue
        
        # make a choice
        path.append(choice)
        
        # explore
        backtrack(path, updated_choices)
        
        # undo the choice (backtrack)
        path.pop()
```

---

## 🛠️ Tips / Tricks

### ✅ 1. **Always undo your move** (path.pop())

You explore a branch → then return and try another → so you must backtrack.

### ✅ 2. **Use "used" flags or sets for permutations**

To prevent reuse (e.g., in permutations):

```python
used = [False] * len(nums)

def backtrack(path):
    if len(path) == len(nums):
        res.append(path[:])
        return
    for i in range(len(nums)):
        if used[i]:
            continue
        used[i] = True
        path.append(nums[i])
        backtrack(path)
        path.pop()
        used[i] = False
```

### ✅ 3. **Sort input to help with duplicates pruning**

In problems like subsets or permutations with duplicates:

```python
nums.sort()
if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
    continue  # skip duplicate
```

### ✅ 4. **DFS vs Backtracking**

* DFS: usually goes deep, may or may not backtrack.
* Backtracking: DFS *with undoing* choices. Always returns to try other options.

---

## 🔥 Common Backtracking Problems

| Problem Type    | Key Idea                                 |
| --------------- | ---------------------------------------- |
| Subsets         | Include/exclude each item                |
| Permutations    | Choose unused items one by one           |
| N-Queens        | Place queens row by row, check for valid |
| Sudoku Solver   | Try numbers in empty cells, validate     |
| Word Search     | DFS from cell, backtrack when needed     |
| Combination Sum | Explore with or without current number   |

---

## 💡 Mindset

* Backtracking = "Try everything, but cut off bad paths early."
* Think in terms of *recursive tree exploration*.
* Use **print statements** to debug paths and decisions.

---
