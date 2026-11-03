"""
============================================================
LEETCODE 49 — GROUP ANAGRAMS
============================================================

Problem:
    Given an array of strings, group the anagrams together.
    Anagrams contain the same characters with the same frequencies.

Example:
    Input:
        ["eat", "tea", "tan", "ate", "nat", "bat"]

    Possible output:
        [["bat"], ["tan", "nat"], ["eat", "tea", "ate"]]

Definitions:
    n = number of strings
    k = maximum length of a string
    u = maximum number of distinct characters in a string

Approaches:
    1. Brute force grouping
    2. Sorted string as dictionary key
    3. Fixed 26-character frequency tuple
    4. Dictionary frequency + frozenset
    5. Dictionary frequency + sorted items
    6. Prime product hash
    7. Counter + frozenset
    8. Extended ASCII frequency array

Complexity notes:
    - Auxiliary space excludes the returned output groups.
    - Hash-table operations are expected O(1) on average.
    - Python integer arithmetic is not constant-time for arbitrarily
      large integers, so prime-product hashing has a simplified
      arithmetic-cost analysis.
============================================================
"""

from collections import Counter, defaultdict
from typing import List


# ------------------------------------------------------------
# APPROACH 1 — BRUTE FORCE GROUPING
# ------------------------------------------------------------
# Compare each word against the representative word of each
# existing group. Sorting is used to check whether two words
# are anagrams.
#
# Time:  O(n^2 * k log k)
# Space: O(n * k) for the groups/representatives; output storage
#        is conventionally excluded from auxiliary space.
# ------------------------------------------------------------

class Solution1_BruteForce:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = []

        for word in strs:
            found = False

            for group in groups:
                if sorted(word) == sorted(group[0]):
                    group.append(word)
                    found = True
                    break

            if not found:
                groups.append([word])

        return groups


# ------------------------------------------------------------
# APPROACH 2 — SORTED STRING AS DICTIONARY KEY
# ------------------------------------------------------------
# Every anagram produces the same sorted string:
#   "eat" -> "aet"
#   "tea" -> "aet"
#   "ate" -> "aet"
#
# Time:  O(n * k log k)
# Space: O(n * k) for stored keys, excluding output.
# ------------------------------------------------------------

class Solution2_Sorting:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        hmap = {}

        for word in strs:
            key = "".join(sorted(word))
            hmap.setdefault(key, []).append(word)

        return list(hmap.values())


# ------------------------------------------------------------
# APPROACH 3 — FIXED 26-CHARACTER FREQUENCY TUPLE
# ------------------------------------------------------------
# For lowercase English letters, count each character in a
# fixed-size array. Convert the list to a tuple because lists
# are not hashable and therefore cannot be dictionary keys.
#
# Assumption: every character is in 'a' through 'z'.
#
# Time:  O(n * (k + 26)) = O(n * k)
# Space: O(26 * n) = O(n) for stored frequency keys.
# ------------------------------------------------------------

class Solution3_FrequencyTuple:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        hmap = {}

        for word in strs:
            char_freq = [0] * 26

            for char in word:
                idx = ord(char) - ord("a")
                char_freq[idx] += 1

            key = tuple(char_freq)
            hmap.setdefault(key, []).append(word)

        return list(hmap.values())


# ------------------------------------------------------------
# APPROACH 4 — DICTIONARY FREQUENCY + FROZENSET
# ------------------------------------------------------------
# Build a frequency dictionary for each word.
# frozenset(freq.items()) is an immutable, unordered, hashable
# representation. Equal frequency maps produce equal frozensets.
#
# Supports arbitrary hashable characters, including Unicode
# code points represented as Python strings.
#
# Time:  O(n * k) expected
# Space: O(n * u) for stored signatures.
# ------------------------------------------------------------

class Solution4_FrequencyFrozenset:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        hmap = {}

        for word in strs:
            freq = {}

            for char in word:
                freq[char] = freq.get(char, 0) + 1

            key = frozenset(freq.items())
            hmap.setdefault(key, []).append(word)

        return list(hmap.values())


# ------------------------------------------------------------
# APPROACH 5 — DICTIONARY FREQUENCY + SORTED ITEMS
# ------------------------------------------------------------
# Build a frequency dictionary, sort its (character, count)
# pairs, and use the resulting tuple as a canonical key.
#
# Time:  O(n * (k + u log u))
# Space: O(n * u) for stored signatures.
# ------------------------------------------------------------

class Solution5_FrequencySortedItems:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        hmap = {}

        for word in strs:
            freq = {}

            for char in word:
                freq[char] = freq.get(char, 0) + 1

            key = tuple(sorted(freq.items()))
            hmap.setdefault(key, []).append(word)

        return list(hmap.values())


# ------------------------------------------------------------
# APPROACH 6 — PRIME PRODUCT HASH
# ------------------------------------------------------------
# Assign a unique prime to each lowercase English letter.
# Multiplication is commutative, and unique prime factorization
# means each character-frequency multiset has a unique product.
#
# Assumption: every character is in 'a' through 'z'.
#
# Time:  O(n * k) under a unit-cost arithmetic model.
# Space: O(n) dictionary keys, excluding output.
#
# Caveat:
#   Python integers do not overflow, but products become very
#   large and arithmetic becomes more expensive as words grow.
#   Fixed-width integer languages can overflow.
# ------------------------------------------------------------

class Solution6_PrimeProduct:
    PRIMES = [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67,
        71, 73, 79, 83, 89, 97, 101
    ]

    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        hmap = defaultdict(list)

        for word in strs:
            key = 1

            for char in word:
                key *= self.PRIMES[ord(char) - ord("a")]

            hmap[key].append(word)

        return list(hmap.values())


# ------------------------------------------------------------
# APPROACH 7 — COUNTER + FROZENSET
# ------------------------------------------------------------
# Counter handles frequency counting. Convert its items to a
# frozenset to create a hashable, order-independent key.
#
# Supports arbitrary hashable characters.
#
# Time:  O(n * k) expected
# Space: O(n * u) for stored signatures.
# ------------------------------------------------------------

class Solution7_CounterFrozenset:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        hmap = defaultdict(list)

        for word in strs:
            key = frozenset(Counter(word).items())
            hmap[key].append(word)

        return list(hmap.values())


# ------------------------------------------------------------
# APPROACH 8 — EXTENDED ASCII FREQUENCY ARRAY
# ------------------------------------------------------------
# Use an array with 128 slots to count ASCII characters.
#
# Assumption: every character has ord(char) < 128.
# For the full 256-value byte range, use an array of size 256.
# This does NOT support arbitrary Unicode characters.
#
# Time:  O(n * (k + 128)) = O(n * k)
# Space: O(128 * n) = O(n) for stored keys.
# ------------------------------------------------------------

class Solution8_ASCII_Frequency:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        hmap = {}

        for word in strs:
            freq = [0] * 128

            for char in word:
                code = ord(char)

                if code >= 128:
                    raise ValueError("Input must contain ASCII characters")

                freq[code] += 1

            key = tuple(freq)
            hmap.setdefault(key, []).append(word)

        return list(hmap.values())


# ------------------------------------------------------------
# COMPLEXITY SUMMARY
# ------------------------------------------------------------
#
# Approach                         Time                  Signature space
# -----------------------------------------------------------------------
# 1. Brute force                   O(n^2 * k log k)       Depends on groups
# 2. Sorted string                 O(n * k log k)         O(n * k)
# 3. Fixed 26 frequency tuple      O(n * k)               O(n)
# 4. Dict + frozenset              O(n * k) expected      O(n * u)
# 5. Dict + sorted items           O(n * (k + u log u))   O(n * u)
# 6. Prime product                 O(n * k)*              O(n) keys
# 7. Counter + frozenset           O(n * k) expected      O(n * u)
# 8. ASCII frequency array         O(n * k)               O(n)
#
# *Prime-product complexity assumes constant-cost multiplication.
# Actual big-integer multiplication cost grows with integer size.
#
# Output storage is excluded from the signature-space column.
# ------------------------------------------------------------


# ------------------------------------------------------------
# EDGE CASES
# ------------------------------------------------------------

def run_edge_case_tests():
    test_cases = [
        ([], []),
        (["abc"], [["abc"]]),
        (["", ""], [["", ""]]),
        (["abc", "abc", "abc"], [["abc", "abc", "abc"]]),
        (["abc", "def", "ghi"], [["abc"], ["def"], ["ghi"]]),
        (["aabb", "bbaa", "abab"], [["aabb", "bbaa", "abab"]]),
        (["a", "aa", "aaa"], [["a"], ["aa"], ["aaa"]]),
    ]

    # All these implementations support lowercase English input.
    solutions = [
        Solution1_BruteForce(),
        Solution2_Sorting(),
        Solution3_FrequencyTuple(),
        Solution4_FrequencyFrozenset(),
        Solution5_FrequencySortedItems(),
        Solution6_PrimeProduct(),
        Solution7_CounterFrozenset(),
        Solution8_ASCII_Frequency(),
    ]

    for solution in solutions:
        for strs, expected_groups in test_cases:
            result = solution.groupAnagrams(strs)

            # Group ordering and order within each group do not matter.
            normalize = lambda groups: sorted(
                tuple(sorted(group)) for group in groups
            )

            assert normalize(result) == normalize(expected_groups), (
                solution.__class__.__name__,
                strs,
                result,
                expected_groups,
            )

    print("All edge-case tests passed.")


if __name__ == "__main__":
    run_edge_case_tests()


# ------------------------------------------------------------
# INTERVIEW TAKEAWAYS
# ------------------------------------------------------------
#
# 1. Identify input constraints before choosing a signature.
# 2. Sorting is simple and works for arbitrary comparable characters.
# 3. A fixed frequency array is excellent for a bounded alphabet.
# 4. Convert lists to tuples before using them as dictionary keys.
# 5. frozenset(freq.items()) provides an unordered, hashable key.
# 6. Prime products are mathematically interesting but impractical
#    for long strings because integers become very large.
# 7. Distinguish auxiliary space from output storage.
#
# Recommended solutions to master:
#   - Approach 2: sorted string
#   - Approach 3: fixed frequency tuple
#   - Approach 4: dictionary frequency + frozenset
# ------------------------------------------------------------
