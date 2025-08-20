# https://leetcode.com/problems/find-eventual-safe-states/
from typing import List

# ============================================================================
# SOLUTION 1: THREE-COLOR DFS (YOUR FIRST APPROACH)
# ============================================================================
class Solution1:
    def eventualSafeNodes(self, graph: List[List[int]]) -> List[int]:
        """
        Time Complexity: O(V + E) where V = nodes, E = edges
        Space Complexity: O(V) for visited arrays + recursion stack
        
        Colors:
        - White (not visited): visited[i] = False
        - Gray (in current path): in_stack[i] = True  
        - Black (completely processed): safenodes[i] = True/False
        """
        n = len(graph)
        safenodes = [False] * n
        visited = [False] * n
        in_stack = [False] * n
        
        def is_safenode(node):
            # If already processed, return cached result
            if visited[node]:
                return safenodes[node]
            
            # Mark as visited and add to current path
            visited[node] = True
            in_stack[node] = True
            
            # Check all neighbors
            for neighbor in graph[node]:
                # Cycle detected: neighbor is in current path
                if in_stack[neighbor]:
                    safenodes[node] = False
                    in_stack[node] = False
                    return False
                
                # If neighbor is unsafe, current node is also unsafe
                if not is_safenode(neighbor):
                    safenodes[node] = False
                    in_stack[node] = False
                    return False
            
            # All neighbors are safe, so current node is safe
            safenodes[node] = True
            in_stack[node] = False
            return True
        
        # Process all nodes
        for node in range(n):
            if not visited[node]:
                is_safenode(node)
        
        return [i for i, safe in enumerate(safenodes) if safe]


# ============================================================================
# SOLUTION 2: THREE-STATE DFS (CLEANER APPROACH)
# ============================================================================
class Solution2:
    def eventualSafeNodes(self, graph: List[List[int]]) -> List[int]:
        """
        Time Complexity: O(V + E) - each node visited once
        Space Complexity: O(V) - states array + recursion stack
        
        States:
        - 0: White (unvisited)
        - 1: Gray (currently being processed/in recursion stack)
        - 2: Black (completely processed and safe)
        
        This is more elegant and standard for cycle detection problems.
        """
        n = len(graph)
        states = [0] * n  # 0: unvisited, 1: visiting, 2: safe
        
        def dfs(node):
            # If already processed, return whether it's safe
            if states[node] != 0:
                return states[node] == 2
            
            # Mark as currently being processed
            states[node] = 1
            
            # Check all neighbors
            for neighbor in graph[node]:
                # If neighbor is unsafe, current node is unsafe
                if not dfs(neighbor):
                    return False
            
            # All neighbors are safe, mark current as safe
            states[node] = 2
            return True
        
        return [i for i in range(n) if dfs(i)]


# ============================================================================
# SOLUTION 3: TOPOLOGICAL SORT APPROACH (ALTERNATIVE)
# TC: O(V + E), SC: O(V)
# ============================================================================
class Solution3:
    def eventualSafeNodes(self, graph: List[List[int]]) -> List[int]:
        """
        Topological sort on reversed graph.
        
        Time Complexity: O(V + E)
        Space Complexity: O(V)
        
        Key insight: Reverse the graph and find nodes with no incoming edges.
        Safe nodes in original = nodes with no outgoing edges in reversed graph.
        """
        n = len(graph)
        
        # Build reverse graph and calculate out-degrees
        reverse_graph = [[] for _ in range(n)]
        out_degree = [0] * n
        
        for node in range(n):
            for neighbor in graph[node]:
                reverse_graph[neighbor].append(node)
                out_degree[node] += 1
        
        # Initialize queue with terminal nodes (out-degree = 0)
        from collections import deque
        queue = deque([i for i in range(n) if out_degree[i] == 0])
        safe_nodes = []
        
        while queue:
            node = queue.popleft()
            safe_nodes.append(node)
            
            # For each node pointing to current node in reverse graph
            for prev_node in reverse_graph[node]:
                out_degree[prev_node] -= 1
                if out_degree[prev_node] == 0:
                    queue.append(prev_node)
        
        return sorted(safe_nodes)


"""
COMPREHENSIVE ANALYSIS:

1. **PROBLEM UNDERSTANDING**:
   - Safe node: all paths from it eventually reach a terminal node
   - Unsafe node: at least one path leads to a cycle
   - Terminal node: node with no outgoing edges (always safe)

2. **APPROACH COMPARISON**:
   
   **Solution 1 (Three arrays)**:
   ✅ Correct logic
   ❌ More complex state management
   ❌ Redundant terminal node preprocessing
   ❌ Less readable
   
   **Solution 2 (Single state array)**:
   ✅ Cleaner and more standard
   ✅ Easier to understand and implement
   ✅ Standard three-color DFS pattern
   ✅ Better for interviews
   
   **Solution 3 (Topological sort)**:
   ✅ Different algorithmic approach
   ✅ Iterative (no recursion stack issues)
   ❌ More complex to implement
   ❌ Less intuitive

3. **WHY SOLUTION 2 IS BETTER**:
   - Standard three-color DFS pattern
   - Single state array instead of three boolean arrays
   - Cleaner logic flow
   - Less prone to bugs
   - More commonly used in competitive programming

4. **CYCLE DETECTION LOGIC**:
   - When we encounter a node with state = 1 during DFS, it means we've found a back edge (cycle)
   - Any node that can reach a cycle is unsafe
   - Any node that cannot reach a cycle is safe

5. **STATE MEANINGS**:
   - State 0: Unvisited (white)
   - State 1: Currently being processed (gray) - in recursion stack
   - State 2: Completely processed and safe (black)

6. **TIME COMPLEXITY ANALYSIS**:
   - Each node is visited at most once: O(V)
   - Each edge is traversed at most once: O(E)
   - Total: O(V + E)

7. **SPACE COMPLEXITY**:
   - States array: O(V)
   - Recursion stack: O(V) in worst case
   - Total: O(V)

8. **EDGE CASES**:
   - Empty graph: return []
   - All terminal nodes: return all nodes
   - Single cycle: return empty or nodes not in cycle
   - Self-loops: node with self-loop is unsafe

9. **INTERVIEW TIPS**:
   - Start with explaining what makes a node safe/unsafe
   - Mention cycle detection is key
   - Implement Solution 2 (cleaner three-state approach)
   - Explain the three colors/states clearly
   - Discuss time/space complexity

10. **COMMON MISTAKES TO AVOID**:
    - Not handling the case where we revisit a node in the same path (cycle)
    - Forgetting to mark nodes as safe after processing all neighbors
    - Not using memoization (visiting same node multiple times)
    - Incorrect state transitions

RECOMMENDATION: Use Solution 2 - it's the cleanest and most standard approach.
"""