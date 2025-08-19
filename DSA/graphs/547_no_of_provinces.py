# https://leetcode.com/problems/number-of-provinces/submissions/1740963146/
from typing import List


class Solution:
    """
    Problem: Number of Provinces
    Given an n x n matrix isConnected where isConnected[i][j] = 1 if the ith city 
    and jth city are directly connected, and isConnected[i][j] = 0 otherwise.
    Return the total number of provinces.
    """
    
    def findCircleNum_original_unionfind(self, isConnected: List[List[int]]) -> int:
        """
        ORIGINAL SOLUTION 1: Manual Union-Find approach (Complex & Buggy)
        
        Issues with this approach:
        - Overly complex logic with multiple dictionaries
        - Potential bugs in merging logic
        - Unnecessary tracking of city counts
        - Not following standard Union-Find pattern
        
        TC: O(n^3) - Due to the nested loop for merging provinces
        SC: O(n) - For provinces and city_counts dictionaries
        """
        provinces = {}
        city_counts = {}
        tag, count = "p", 0
        
        for i in range(len(isConnected)):
            for j in range(len(isConnected[0])):
                if isConnected[i][j]:
                    if i not in provinces and j not in provinces:
                        p_name = tag + str(count)
                        provinces[i] = p_name
                        provinces[j] = p_name
                        count += 1
                        city_counts[p_name] = city_counts.get(p_name, 0) + 2 if i != j else 1
                    elif i in provinces and j not in provinces:
                        p_name = provinces[i]
                        provinces[j] = p_name
                        city_counts[p_name] = city_counts.get(p_name, 0) + 1
                    elif j in provinces and i not in provinces:
                        p_name = provinces[j]
                        provinces[i] = p_name
                        city_counts[p_name] = city_counts.get(p_name, 0) + 1
                    elif provinces[i] != provinces[j]:
                        old_p, new_p = provinces[j], provinces[i]
                        for city, p in list(provinces.items()):
                            if p == old_p:
                                provinces[city] = new_p
                        city_counts[new_p] = city_counts.get(new_p, 0) + city_counts.get(old_p, 0)
                        city_counts[old_p] = 0 
        
        return sum(1 for v in city_counts.values() if v > 0)

    def findCircleNum_original_dfs(self, isConnected: List[List[int]]) -> int:
        """
        ORIGINAL SOLUTION 2: DFS approach (Clean & Correct)
        
        This solution correctly identifies connected components using DFS.
        For each unvisited city, start a DFS to mark all connected cities
        and increment province count.
        
        TC: O(n^2) - Visit each cell in the matrix once
        SC: O(n) - For visited set and recursion stack in worst case
        """
        n = len(isConnected)
        visited = set()

        def dfs(city):
            # Explore all neighbors of current city
            for nei in range(n):
                if isConnected[city][nei] and nei not in visited:
                    visited.add(nei)
                    dfs(nei)

        provinces = 0
        for city in range(n):
            if city not in visited:
                provinces += 1  # Found a new province
                visited.add(city)
                dfs(city)  # Mark all cities in this province
        
        return provinces

    def findCircleNum_dfs_iterative(self, isConnected: List[List[int]]) -> int:
        """
        IMPROVED SOLUTION 1: Iterative DFS (Avoids recursion stack overflow)
        
        Same logic as recursive DFS but uses explicit stack to avoid
        potential stack overflow for large inputs.
        
        TC: O(n^2) - Visit each cell in the matrix once
        SC: O(n) - For visited set and explicit stack
        """
        n = len(isConnected)
        visited = set()
        provinces = 0
        
        for city in range(n):
            if city not in visited:
                provinces += 1
                # Use iterative DFS with explicit stack
                stack = [city]
                while stack:
                    curr = stack.pop()
                    if curr in visited:
                        continue
                    visited.add(curr)
                    # Add all unvisited neighbors to stack
                    for neighbor in range(n):
                        if isConnected[curr][neighbor] and neighbor not in visited:
                            stack.append(neighbor)
        
        return provinces

    def findCircleNum_union_find(self, isConnected: List[List[int]]) -> int:
        """
        IMPROVED SOLUTION 2: Proper Union-Find with Path Compression
        
        Standard Union-Find implementation with path compression for efficiency.
        Each city initially forms its own set, then union connected cities.
        
        TC: O(n^2 * α(n)) where α is inverse Ackermann function (nearly constant)
        SC: O(n) - For parent array
        """
        n = len(isConnected)
        parent = list(range(n))  # Each city is its own parent initially
        
        def find(x):
            """Find root with path compression"""
            if parent[x] != x:
                parent[x] = find(parent[x])  # Path compression
            return parent[x]
        
        def union(x, y):
            """Union two sets"""
            root_x, root_y = find(x), find(y)
            if root_x != root_y:
                parent[root_x] = root_y
        
        # Union all directly connected cities
        for i in range(n):
            for j in range(i + 1, n):  # Only check upper triangle
                if isConnected[i][j]:
                    union(i, j)
        
        # Count unique roots (provinces)
        return len(set(find(i) for i in range(n)))

    def findCircleNum_union_find_optimized(self, isConnected: List[List[int]]) -> int:
        """
        IMPROVED SOLUTION 3: Union-Find with Rank and Path Compression
        
        Most optimized Union-Find with both path compression and union by rank.
        
        TC: O(n^2 * α(n)) - Nearly O(n^2) in practice
        SC: O(n) - For parent and rank arrays
        """
        n = len(isConnected)
        parent = list(range(n))
        rank = [0] * n  # Rank for union by rank optimization
        self.provinces = n  # Track number of provinces
        
        def find(x):
            """Find root with path compression"""
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            """Union by rank with path compression"""
            root_x, root_y = find(x), find(y)
            if root_x == root_y:
                return
            
            # Union by rank: attach smaller tree to larger tree
            if rank[root_x] < rank[root_y]:
                parent[root_x] = root_y
            elif rank[root_x] > rank[root_y]:
                parent[root_y] = root_x
            else:
                parent[root_y] = root_x
                rank[root_x] += 1
            
            self.provinces -= 1  # One less province after union
        
        # Process all connections
        for i in range(n):
            for j in range(i + 1, n):
                if isConnected[i][j]:
                    union(i, j)
        
        return self.provinces

    def findCircleNum_bfs(self, isConnected: List[List[int]]) -> int:
        """
        ALTERNATIVE SOLUTION: BFS approach
        
        Uses BFS instead of DFS to find connected components.
        Same time/space complexity as DFS but explores level by level.
        
        TC: O(n^2) - Visit each cell once
        SC: O(n) - For visited set and queue
        """
        from collections import deque
        
        n = len(isConnected)
        visited = set()
        provinces = 0
        
        for city in range(n):
            if city not in visited:
                provinces += 1
                queue = deque([city])
                
                while queue:
                    curr = queue.popleft()
                    if curr in visited:
                        continue
                    visited.add(curr)
                    
                    # Add all unvisited neighbors to queue
                    for neighbor in range(n):
                        if isConnected[curr][neighbor] and neighbor not in visited:
                            queue.append(neighbor)
        
        return provinces


"""
SUMMARY & RECOMMENDATIONS:

1. **Best for Interview**: findCircleNum_original_dfs (clean, easy to understand)
2. **Best for Production**: findCircleNum_union_find_optimized (most efficient)
3. **Best for Learning**: Study both DFS and Union-Find approaches

KEY INSIGHTS:
- DFS/BFS: O(n^2) time, simpler to implement
- Union-Find: Nearly O(n^2) time with optimizations, more complex but extensible
- All approaches have O(n) space complexity

WHEN TO USE WHICH:
- DFS/BFS: When you need to find connected components once
- Union-Find: When you have dynamic connectivity queries or need to track changes
"""