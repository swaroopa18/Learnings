"""
============================================================
LEETCODE 49 — GROUP ANAGRAMS
============================================================
Problem:
    Given an array of strings, group the anagrams together.
    Anagrams are words made of the same characters in any order.
    e.g. ["eat","tea","tan","ate","nat","bat"]
         → [["bat"],["nat","tan"],["ate","eat","tea"]]

Key Insight:
    Two words are anagrams iff they share the same "signature".
    The trick is choosing the most efficient signature to compute.

Approaches covered:
    1. Sorted string as key      — O(n * k log k)
    2. Character frequency tuple — O(n * k)         ← optimal
    3. Prime product hash        — O(n * k), clever but risky
    4. Counter as key            — O(n * k), Pythonic but slower

============================================================
"""

from collections import defaultdict
from typing import List


# ─────────────────────────────────────────────────────────
# APPROACH 1 — Sort each word, use it as the hash key
# ─────────────────────────────────────────────────────────
# Intuition:
#   Sorting any anagram always produces the same string.
#   "eat" → "aet",  "tea" → "aet",  "ate" → "aet"
#   So we group words by their sorted version.
#
# Time:  O(n * k log k)  — n words, each sorted in O(k log k)
# Space: O(n * k)        — storing all words + sorted keys
# ─────────────────────────────────────────────────────────
class Solution1_Sorting:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        hmap = {}
        for word in strs:
            sorted_word = "".join(sorted(word))   # signature
            hmap.setdefault(sorted_word, []).append(word)
        return list(hmap.values())


# ─────────────────────────────────────────────────────────
# APPROACH 2 — Character frequency tuple as key  ★ OPTIMAL
# ─────────────────────────────────────────────────────────
# Intuition:
#   Instead of sorting, count occurrences of each of the 26
#   letters and turn that count array into a tuple.
#   Avoids the log-factor of sorting entirely.
#   e.g. "eat" → (1,0,0,0,1,0,...,1,0,...) for a,e,t counts
#
# Time:  O(n * k)   — n words, each scanned in O(k)
# Space: O(n * k)   — storing all words + frequency tuples
#
# When to prefer this:
#   When words can be long (large k). Eliminates the log k
#   factor present in the sorting approach.
# ─────────────────────────────────────────────────────────
class Solution2_FrequencyTuple:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        hmap = {}
        for word in strs:
            char_freq = [0] * 26
            for char in word:
                idx = ord(char) - ord("a")   # map 'a'→0, 'b'→1, ...
                char_freq[idx] += 1
            # lists are unhashable; convert to tuple for dict key
            hmap.setdefault(tuple(char_freq), []).append(word)
        return list(hmap.values())


# ─────────────────────────────────────────────────────────
# APPROACH 3 — Prime product hash
# ─────────────────────────────────────────────────────────
# Intuition:
#   Assign each letter a unique prime. The product of a word's
#   letter-primes is unique to that multiset of characters
#   (Fundamental Theorem of Arithmetic).
#   e.g. a=2, b=3, c=5 ...
#   "ab" → 2*3=6,  "ba" → 3*2=6  ✓  same product
#
# Time:  O(n * k)
# Space: O(n)
#
# ⚠ Caveats:
#   • Long words with repeated high-prime letters cause integer
#     overflow in most languages (not Python, but still slow).
#   • Hash collisions are theoretically possible with crafted input.
#   Treat as a clever interview talking point, not production code.
# ─────────────────────────────────────────────────────────
class Solution3_PrimeHash:
    PRIMES = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101]

    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        hmap = defaultdict(list)
        for word in strs:
            key = 1
            for char in word:
                key *= self.PRIMES[ord(char) - ord("a")]
            hmap[key].append(word)
        return list(hmap.values())


# ─────────────────────────────────────────────────────────
# APPROACH 4 — collections.Counter as key (Pythonic)
# ─────────────────────────────────────────────────────────
# Intuition:
#   Counter("eat") == Counter("tea") is True, but Counters are
#   not hashable. Freeze them via frozenset of items().
#
# Time:  O(n * k)
# Space: O(n * k)
#
# Note: frozenset(Counter(w).items()) is readable but slower
# than approach 2 due to Counter overhead. Good for interviews
# where clarity beats micro-optimisation.
# ─────────────────────────────────────────────────────────
from collections import Counter

class Solution4_Counter:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        hmap = defaultdict(list)
        for word in strs:
            key = frozenset(Counter(word).items())  # hashable signature
            hmap[key].append(word)
        return list(hmap.values())


# ─────────────────────────────────────────────────────────
# COMPLEXITY SUMMARY
# ─────────────────────────────────────────────────────────
# n = number of words,  k = max word length
#
# Approach              | Time          | Space   | Notes
# ─────────────────────────────────────────────────────────
# 1. Sorted key         | O(n·k log k)  | O(n·k)  | Simple, readable
# 2. Freq tuple ★       | O(n·k)        | O(n·k)  | Optimal for large k
# 3. Prime product      | O(n·k)        | O(n)    | Clever, risky overflow
# 4. Counter frozenset  | O(n·k)        | O(n·k)  | Pythonic, slower
# ─────────────────────────────────────────────────────────