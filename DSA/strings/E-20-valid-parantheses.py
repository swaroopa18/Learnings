class Solution:
    def isValid(self, s: str) -> bool:
        """
        Approach: Stack-based matching
        Time Complexity: O(n) - single pass through string
        Space Complexity: O(n) - worst case, all opening brackets
        
        Key Insight:
        - Opening brackets are pushed onto stack (as their closing counterpart)
        - Closing brackets must match the top of the stack
        - Stack must be empty at the end (all brackets closed)
        """
        stack = []
        
        # Map opening brackets to their corresponding closing brackets
        # This allows us to push the expected closing bracket onto the stack
        braces = {"(": ")", "[": "]", "{": "}"}

        for char in s:
            # Case 1: Opening bracket found
            if char in braces:
                # Push the EXPECTED closing bracket onto stack
                stack.append(braces[char])
            
            # Case 2: Closing bracket found
            # Check if stack is empty (no matching opening) OR
            # top of stack doesn't match current closing bracket
            elif len(stack) == 0 or char != stack[-1]:
                return False  # Invalid: either no opening or wrong type
            
            # Case 3: Closing bracket matches top of stack
            else:
                stack.pop()  # Remove the matched closing bracket
        
        # Valid only if all brackets were matched (stack is empty)
        return len(stack) == 0


# Alternative implementation with clearer condition handling
class SolutionAlternative:
    def isValid(self, s: str) -> bool:
        stack = []
        brackets = {"(": ")", "[": "]", "{": "}"}

        for char in s:
            if char in brackets:
                # Opening bracket: push expected closing bracket
                stack.append(brackets[char])
            else:
                # Closing bracket: check if it matches
                if not stack or stack[-1] != char:
                    return False
                stack.pop()
        
        return not stack