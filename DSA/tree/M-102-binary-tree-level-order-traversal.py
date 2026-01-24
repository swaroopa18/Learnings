# Definition for a binary tree node.
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ========================================
# APPROACH 1: BFS Level Order Traversal (Iterative)
# ========================================
# Time Complexity: O(n) - visit each node exactly once
# Space Complexity: O(w) - maximum width of tree (worst case O(n/2) for complete tree)
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        # Edge case: empty tree
        if root is None:
            return []
        
        queue = deque([root])
        result = []
        
        while queue:
            size = len(queue)  # CRITICAL: capture current level size
            level = []  # Store values for current level
            
            # Process all nodes at current level
            for _ in range(size):
                node = queue.popleft()
                level.append(node.val)
                
                # Add children for next level
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            result.append(level)  # Add current level to result
        
        return result


# ========================================
# APPROACH 2: Recursive DFS with Level Tracking
# ========================================
# Time Complexity: O(n)
# Space Complexity: O(h) - recursion stack height
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        result = []
        
        def dfs(node, level):
            if not node:
                return
            
            # If this is a new level, create a new list
            if level == len(result):
                result.append([])
            
            # Add current node to its level
            result[level].append(node.val)
            
            # Recurse on children with incremented level
            dfs(node.left, level + 1)
            dfs(node.right, level + 1)
        
        dfs(root, 0)
        return result


# ========================================
# APPROACH 3: BFS with Null Separator (Alternative)
# ========================================
# Time Complexity: O(n)
# Space Complexity: O(w)
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        
        queue = deque([root, None])  # None marks end of level
        result = []
        level = []
        
        while queue:
            node = queue.popleft()
            
            if node is None:
                # End of current level
                result.append(level)
                level = []
                
                # If queue not empty, add separator for next level
                if queue:
                    queue.append(None)
            else:
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        
        return result


# ========================================
# STEP-BY-STEP DRY RUN
# ========================================
"""
Input Tree:
        3
       / \
      9  20
        /  \
       15   7

Expected Output: [[3], [9, 20], [15, 7]]

BFS EXECUTION TRACE:
-------------------

Initial State:
  queue = [3]
  result = []

ITERATION 1 (Level 0):
  size = 1
  level = []
  
  For loop (i=0):
    - node = 3 (dequeue)
    - level = [3]
    - enqueue 9, 20
    - queue = [9, 20]
  
  result = [[3]]

ITERATION 2 (Level 1):
  size = 2
  level = []
  
  For loop (i=0):
    - node = 9 (dequeue)
    - level = [9]
    - no children
    - queue = [20]
  
  For loop (i=1):
    - node = 20 (dequeue)
    - level = [9, 20]
    - enqueue 15, 7
    - queue = [15, 7]
  
  result = [[3], [9, 20]]

ITERATION 3 (Level 2):
  size = 2
  level = []
  
  For loop (i=0):
    - node = 15 (dequeue)
    - level = [15]
    - no children
    - queue = [7]
  
  For loop (i=1):
    - node = 7 (dequeue)
    - level = [15, 7]
    - no children
    - queue = []
  
  result = [[3], [9, 20], [15, 7]]

ITERATION 4:
  queue is empty, exit while loop

Final Result: [[3], [9, 20], [15, 7]] ✓
"""


# ========================================
# VISUAL REPRESENTATION
# ========================================
"""
Queue Evolution (BFS):
---------------------
Level 0: queue = [3]           → process → result = [[3]]
Level 1: queue = [9, 20]       → process → result = [[3], [9, 20]]
Level 2: queue = [15, 7]       → process → result = [[3], [9, 20], [15, 7]]
Level 3: queue = []            → done


DFS Recursion Tree:
------------------
dfs(3, level=0)
├── result[0] = [3]
├── dfs(9, level=1)
│   ├── result[1] = [9]
│   ├── dfs(null, level=2)
│   └── dfs(null, level=2)
└── dfs(20, level=1)
    ├── result[1] = [9, 20]
    ├── dfs(15, level=2)
    │   └── result[2] = [15]
    └── dfs(7, level=2)
        └── result[2] = [15, 7]

Final: [[3], [9, 20], [15, 7]]
"""


# ========================================
# COMPARISON OF APPROACHES
# ========================================
"""
| Approach          | Time | Space | Pros                              | Cons                     |
|-------------------|------|-------|-----------------------------------|--------------------------|
| BFS (Iterative)   | O(n) | O(w)  | Natural, easy to understand       | More space for wide tree |
| DFS (Recursive)   | O(n) | O(h)  | Less space for balanced tree      | Less intuitive           |
| BFS (Null Sep)    | O(n) | O(w)  | Alternative pattern               | More complex logic       |

Where:
- n = number of nodes
- h = height (best: log n, worst: n)
- w = max width (worst: n/2 for complete tree)

Space Complexity Analysis:
- Complete binary tree: BFS uses O(n/2), DFS uses O(log n) → DFS better
- Skewed tree: Both use O(n) → Similar
- Balanced tree: BFS uses O(n/2), DFS uses O(log n) → DFS better
"""


# ========================================
# BFS LEVEL ORDER PATTERN (TEMPLATE)
# ========================================
"""
This is the STANDARD pattern for level-order problems:

def level_order_template(root):
    if not root:
        return []
    
    queue = deque([root])
    result = []
    
    while queue:
        level_size = len(queue)  # 1. Capture size
        current_level = []        # 2. Create level container
        
        for _ in range(level_size):  # 3. Process current level
            node = queue.popleft()
            current_level.append(node.val)
            
            # 4. Add children for next level
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(current_level)  # 5. Save level result
    
    return result

KEY STEPS:
1. Capture level size before loop
2. Create container for current level
3. Process exactly 'size' nodes
4. Add children to queue
5. Save level to result
"""


# ========================================
# COMMON MISTAKES & FIXES
# ========================================
"""
MISTAKE 1: Not capturing queue size
❌ Bad:
    for _ in range(len(queue)):  # len(queue) changes during iteration!
        node = queue.popleft()
        ...

✅ Good:
    size = len(queue)
    for _ in range(size):
        ...


MISTAKE 2: Reusing level list
❌ Bad:
    level = []  # Outside while loop
    while queue:
        size = len(queue)
        for _ in range(size):
            level.append(...)  # Accumulates across levels!
        result.append(level)

✅ Good:
    while queue:
        level = []  # Fresh list for each level
        ...


MISTAKE 3: Appending node instead of value
❌ Bad:
    level.append(node)  # Appends TreeNode object

✅ Good:
    level.append(node.val)  # Appends integer value


MISTAKE 4: Not checking null before appending
❌ Bad:
    queue.append(node.left)   # May append None
    queue.append(node.right)  # May append None

✅ Good:
    if node.left:
        queue.append(node.left)
    if node.right:
        queue.append(node.right)
"""


# ========================================
# VARIATIONS & RELATED PROBLEMS
# ========================================
"""
Using the SAME BFS template, you can solve:

1. Binary Tree Zigzag Level Order (LC 103)
   - Alternate reversing each level
   - Add: level.reverse() if level_num % 2 == 1

2. Binary Tree Right Side View (LC 199)
   - Return last element of each level
   - Add: result.append(level[-1])

3. Binary Tree Level Order Traversal II (LC 107)
   - Return levels bottom-up
   - Return: result[::-1]

4. Average of Levels (LC 637)
   - Calculate average per level
   - Add: result.append(sum(level) / len(level))

5. Maximum Level Sum (LC 1161)
   - Find level with maximum sum
   - Track: max_sum and corresponding level

6. N-ary Tree Level Order (LC 429)
   - Same pattern, iterate through all children
"""


# ========================================
# EDGE CASES TO TEST
# ========================================
"""
1. Empty tree:
   Input: root = None
   Output: []

2. Single node:
   Input: root = TreeNode(1)
   Output: [[1]]

3. Left skewed:
   Input:     1
             /
            2
           /
          3
   Output: [[1], [2], [3]]

4. Right skewed:
   Input: 1
           \
            2
             \
              3
   Output: [[1], [2], [3]]

5. Complete binary tree:
   Input:     1
            /   \
           2     3
          / \   / \
         4   5 6   7
   Output: [[1], [2, 3], [4, 5, 6, 7]]

6. Unbalanced tree:
   Input:     1
            /   \
           2     3
          /
         4
   Output: [[1], [2, 3], [4]]
"""


# ========================================
# INTERVIEW TIPS
# ========================================
"""
1. START WITH CLARIFICATIONS:
   - "Should I return levels top-to-bottom?" (Yes)
   - "What about empty tree?" (Return [])
   - "Can values be negative?" (Usually yes)

2. EXPLAIN YOUR APPROACH:
   "I'll use BFS with a queue. For each level, I'll capture the 
    queue size, process exactly that many nodes, and collect their
    values in a list. Then I'll add children for the next level."

3. MENTION TIME/SPACE:
   "Time is O(n) since we visit each node once. Space is O(w) for
    the queue, where w is the maximum width. For a complete binary
    tree, the last level has n/2 nodes, so it's O(n)."

4. OFFER ALTERNATIVES:
   "We could also solve this with DFS recursively, tracking the
    level number. That would use O(h) space instead of O(w)."

5. TEST WITH EXAMPLE:
   Always walk through a small example showing queue evolution.
"""


# ========================================
# OPTIMIZATION NOTES
# ========================================
"""
1. For very wide trees (O(n/2) width), DFS uses less space
2. For very deep trees, BFS avoids stack overflow
3. BFS is more natural for level-based problems
4. DFS might be slightly faster due to better cache locality
5. BFS is easier to understand and explain in interviews

RECOMMENDATION: Use BFS (Approach 1) as default for level order problems
"""