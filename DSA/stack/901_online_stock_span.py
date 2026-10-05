"""
================================================================================
 PROBLEM: Online Stock Span (LeetCode 901)
================================================================================
Design a class `StockSpanner` that collects daily price quotes for a stock
and returns the SPAN of that stock's price for the current day.

The span of the stock's price on day `i` is the maximum number of
CONSECUTIVE days (starting from day `i` and going BACKWARD) for which the
stock price was LESS THAN OR EQUAL TO the price on day `i`.

- `StockSpanner()` initializes the object.
- `next(price)` takes today's price and returns the span for today.

Example: prices 100, 80, 60, 70, 60, 75, 85 -> spans 1, 1, 1, 2, 1, 4, 6.

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Is the comparison `<=` (non-strict)? (Yes — equal prices EXTEND the span.
  This is the opposite of Daily Temperatures / Next Greater Element, where
  equal does NOT count. It decides whether the stack pops on `>=` or `>`.)
- Does the span include today itself? (Yes — the minimum span is 1.)
- Is this ONLINE — do prices arrive one at a time with no look-ahead? (Yes —
  that's why it is a class with `next()`, not a function over a full array;
  only backward-looking structures work.)
- How many calls and what is the price range? (Up to 10^4 calls, so O(n)
  per call in the worst case is too slow overall -> need amortized O(1).)

"""

# ================================================================================
# 🔑🔑🔑  STRONG POINTS FOR "PREVIOUS GREATER ELEMENT / SPAN" PROBLEMS  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   Span = distance back to the PREVIOUS STRICTLY GREATER price.      │
    │   Keep a MONOTONIC DECREASING stack of (day, price) pairs: any      │
    │   price <= today's is "swallowed" by today and can be popped        │
    │   FOREVER — it can never be the blocker for a future day.           │
    │   span = today - day_of_top_of_stack  (or day + 1 if empty).        │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

This is the MIRROR IMAGE of Next Greater Element / Daily Temperatures: those
look FORWARD for the next greater element and resolve waiting elements when a
bigger one arrives; Stock Span looks BACKWARD for the previous greater
element and resolves the CURRENT element immediately when it arrives. Key
ideas:

1. **Span(i) = i - (index of previous element strictly greater than
   price[i])**, with "previous greater index = -1" if none exists. So the
   problem is really "find previous greater element" in an online stream.

2. **Pop on `>=` (price >= top's price)**: every popped day had a price <=
   today's, so it lies INSIDE today's span. After the pops, whatever is on
   top is the nearest day with a strictly greater price — the span's
   boundary.

3. **Popped entries are discarded permanently, and that's safe.** Any future
   day that is higher than today also beats the popped ones; any future day
   that is lower than today is blocked by today (or something even closer),
   long before it could reach the popped ones. Today dominates them.

4. **Stack stays strictly decreasing in price from bottom to top**, so each
   day is pushed once and popped at most once => amortized O(1) per `next()`
   call.

5. **Empty stack => today is the largest so far => span = day + 1** (the
   whole history, including today). Storing the absolute `day` counter in
   the stack makes this a one-liner.
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea
Store every price. For each `next(price)`, walk backward from today while the
earlier prices are <= today's price and count how many days you passed. Easy,
but a long rising streak makes every call re-walk the whole history -> O(n)
per call, O(n^2) overall.

### The key insight: today's span can SWALLOW earlier spans
If today's price is 75 and an earlier day with price 70 had a span of 2, then
that 70-day's entire span is already inside 75's span too — you don't need to
re-walk those days one by one. A stack that remembers only the "walls"
(strictly bigger prices still standing) lets you jump straight to the
boundary.

### Step-by-step trace: prices 100, 80, 60, 70, 60, 75, 85
Stack entries are (day, price). day starts at 0.
```
next(100): day=0, stack empty                       -> span = 0+1 = 1
           push (0,100)                             stack=[(0,100)]
next(80):  day=1, 100>=80? no pop                   -> span = 1-0 = 1
           push (1,80)                              stack=[(0,100),(1,80)]
next(60):  day=2, 80>=60? no pop                    -> span = 2-1 = 1
           push (2,60)                              stack=[(0,100),(1,80),(2,60)]
next(70):  day=3, 70>=60 -> pop (2,60)
           70>=80? no                               -> span = 3-1 = 2
           push (3,70)                              stack=[(0,100),(1,80),(3,70)]
next(60):  day=4, 60>=70? no pop                    -> span = 4-3 = 1
           push (4,60)                              stack=[(0,100),(1,80),(3,70),(4,60)]
next(75):  day=5, 75>=60 -> pop (4,60)
           75>=70 -> pop (3,70)
           75>=80? no                               -> span = 5-1 = 4
           push (5,75)                              stack=[(0,100),(1,80),(5,75)]
next(85):  day=6, 85>=75 -> pop (5,75)
           85>=80 -> pop (1,80)
           85>=100? no                              -> span = 6-0 = 6
           push (6,85)                              stack=[(0,100),(6,85)]
spans = 1, 1, 1, 2, 1, 4, 6 ✅
```

### The "aha" moment to remember 🎯
"Span = distance to the previous STRICTLY greater element. Stack of
(index, price), pop while top <= current (i.e. `price >= top`), then span =
current index - index of the new top (or index + 1 if empty)."
"""

# ================================================================================
# ALTERNATIVE APPROACH 1 — Brute Force (store prices, walk backward)
# ================================================================================
"""
### Thought Process 🧠
Keep a list of all prices so far. On `next(price)`, append it, then count
backward from today while `prices[j] <= price`.

### Complexity
- TC: O(n) per call -> O(n^2) over n calls (worst case: strictly increasing
  prices, every call walks the whole history)
- SC: O(n) — stores every price

### Pros
- Trivially correct; perfect reference implementation for testing.

### Cons
- 10^4 calls with increasing prices ~ 5*10^7 steps — borderline in Python,
  and unacceptable as a "design" answer in an interview.
- Re-walks the same days again and again for consecutive calls.

### Bottleneck
Every call recounts days that a previous call already proved are "<=". Ask:
"can I reuse previous spans?" -> Yes: either a monotonic stack (discard
dominated days) or span-based jumping (next approaches).
"""


class StockSpannerBrute:
    def __init__(self):
        self.prices = []

    def next(self, price: int) -> int:
        self.prices.append(price)
        span = 0
        j = len(self.prices) - 1
        while j >= 0 and self.prices[j] <= price:
            span += 1
            j -= 1
        return span


# ================================================================================
# MY APPROACH — Monotonic Stack of (day, price) (optimal)
# ================================================================================
"""
### Idea
Keep a global `day` counter and a stack of `(day, price)` pairs whose prices
are strictly decreasing from bottom to top. For each new price, pop every
entry with price <= today's (they're inside today's span and can never block
a future day). The new top (if any) is the nearest strictly greater price, so
`span = day - top_day`; if the stack is empty, `span = day + 1`. Push today's
`(day, price)` and increment `day`.

### Complexity
- TC: O(1) amortized per `next()` call, O(n) total over n calls — each day is
  pushed once and popped at most once
- SC: O(n) worst case (strictly decreasing prices keep everything on the
  stack); often much smaller

### Pros
- Optimal amortized time and the standard interview answer.
- Stores only "walls" — dominated days are discarded, so memory is usually
  less than keeping every price.
- Using absolute day indices makes the empty-stack case (`day + 1`) and the
  normal case (`day - top_day`) trivial to compute.

### Cons
- Individual calls can be O(n) in the worst case (one huge price pops
  everything) — only the AMORTIZED bound is O(1). Be ready to say that.
- `>=` vs `>` is easy to flip by mistake; the span definition ("less than or
  EQUAL") is what forces the non-strict pop.

### DSA Buddy Point 🧠
"Online / streaming 'how far back is the previous greater' => stack of
(index, value); pop while top <= current; distance to the new top is the
answer. Equal values are popped here because the span INCLUDES equals."

### What can be improved?
Complexity-wise nothing — amortized O(1) per call is optimal. Your code is
correct as is: pop on `>=`, `span = day + 1` for an empty stack, and
`day - stack[-1][0]` otherwise all match the definition. One optional
variant (next approach) stores `(price, span)` and ACCUMULATES popped spans
instead of storing absolute days, so no global `day` counter is needed.
"""


class StockSpanner:

    def __init__(self):
        self.stack = []
        self.day = 0

    def next(self, price: int) -> int:
        while self.stack and price >= self.stack[-1][1]:
            self.stack.pop()
        span = self.day + 1 if not self.stack else self.day - self.stack[-1][0]
        self.stack.append((self.day, price))
        self.day += 1
        return span


# Your StockSpanner object will be instantiated and called as such:
# obj = StockSpanner()
# param_1 = obj.next(price)


# ================================================================================
# ALTERNATIVE APPROACH 2 — Stack of (price, span) with Accumulated Spans
# ================================================================================
"""
### Thought Process 🧠
Store `(price, span)` instead of `(day, price)`. When today's price swallows a
stack entry, ADD that entry's span to today's running span — an entry's span
already counts all the days it covered, so today inherits them in one step.
Start with `span = 1` (today itself). No `day` counter is needed.

### Complexity
- TC: O(1) amortized per call, O(n) total
- SC: O(n) worst case

### Pros
- Self-contained entries; no global day index to maintain.
- Very readable: "I absorb the spans of everything I'm bigger than."
- Very common in editorial solutions, so familiar to interviewers.

### Cons
- The "add the popped span" step is slightly less obvious than computing a
  day difference; forgetting to add (or double-counting today) gives
  off-by-one errors.
- Same `>=` pop requirement as the index-based version.

### DSA Buddy Point 🧠
"Two equivalent encodings: store absolute indices and subtract, OR store
spans and accumulate. Pick whichever you can write bug-free under pressure."
"""


class StockSpannerAccumulate:
    def __init__(self):
        self.stack = []  # (price, span)

    def next(self, price: int) -> int:
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            span += self.stack.pop()[1]
        self.stack.append((price, span))
        return span


# ================================================================================
# ALTERNATIVE APPROACH 3 — Span Array + Jump Pointers (no explicit stack)
# ================================================================================
"""
### Thought Process 🧠
Keep every price and its span in two arrays. For the new price, start with
`span = 1`, `j = len - 2` (yesterday). While `prices[j] <= price`, absorb
`spans[j]` into today's span and JUMP back by `spans[j]` days — the whole
block of days covered by `j`'s span is already known to be <= `prices[j]`,
hence <= today's price. Stop when you reach a strictly greater price or run
off the start.

### Complexity
- TC: O(1) amortized per call (jumps follow chains of already-computed
  spans; each block is skipped over a bounded number of times)
- SC: O(n) — keeps ALL prices and spans (no discarding of dominated days)

### Pros
- No explicit stack; reuses the `spans` array as a "jump back" pointer —
  the same trick as the O(1)-space Daily Temperatures solution, mirrored.
- Good talking point showing you understand WHY the stack works (spans cover
  contiguous blocks).

### Cons
- Always O(n) memory (the stack version can be far smaller for volatile
  data).
- Harder to prove the amortized bound than the stack version.

### DSA Buddy Point 🧠
"A monotonic stack and a 'jump via stored answers' array are two views of
the same idea: previously computed answers describe whole blocks you can
skip."
"""


class StockSpannerJump:
    def __init__(self):
        self.prices = []
        self.spans = []

    def next(self, price: int) -> int:
        span = 1
        j = len(self.prices) - 1
        while j >= 0 and self.prices[j] <= price:
            span += self.spans[j]
            j -= self.spans[j]
        self.prices.append(price)
        self.spans.append(span)
        return span


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
ONLINE STOCK SPAN
│
├── Brute Force
│   └── Store prices; walk back while price[j] <= today -> O(n) per call
│
├── Bottleneck
│   └── Re-walks days earlier calls already proved are <= (spans overlap)
│
├── Key Insight
│   └── Span = distance to PREVIOUS STRICTLY GREATER price. A bigger price
│       swallows smaller ones forever -> monotonic decreasing stack
│
├── My Approach — Stack of (day, price) (BEST / standard)
│   └── pop while price >= top.price; span = day - top.day (or day + 1)
│       -> O(1) amortized per call, O(n) space; `>=` because span counts
│       equal prices
│
├── Stack of (price, span) — Accumulate
│   └── span = 1; span += popped.span for each pop; push (price, span)
│       -> same complexity, no day counter
│
└── Span Array + Jump Pointers
    └── j -= spans[j] while prices[j] <= price; span += spans[j]
        -> O(1) amortized, O(n) space, no explicit stack
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Stock Span = PREVIOUS greater element problem, online. Mirror of Next
  Greater Element: there the stack holds elements WAITING for a future
  answer; here each new element is resolved IMMEDIATELY from history."
- "Pop on `>=` because the span includes EQUAL prices. Daily Temperatures /
  NGE pop on `<` (strict) — equals must not count there. Always re-derive
  from the problem's wording."
- "Popped days are dominated by today and can be discarded permanently — a
  future day either beats today (and them) or is blocked by today first."
- "Empty stack => today is the max so far => span = day + 1; otherwise
  span = day - top_day. Absolute indices make both cases trivial."
- "Amortized O(1) per call (O(n) total): every day is pushed once and popped
  at most once. A single call can still be O(n)."
- "Encoding choice: (day, price) with subtraction, OR (price, span) with
  accumulation — both are the same algorithm."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                         | Core Idea                                              | TC (per call / total)      | SC   | Pros                                            | Cons                                                    | When to Use                          |
|----------------------------------|--------------------------------------------------------|----------------------------|------|-------------------------------------------------|---------------------------------------------------------|--------------------------------------|
| Brute Force                      | Store prices; walk back while <= today                 | O(n) / O(n^2)              | O(n) | Trivial, great for validation                   | Quadratic, re-walks the same days                       | Baseline / correctness check         |
| Stack of (day, price)            | Pop while price >= top; span = day - top_day          | O(1) amortized / O(n)      | O(n) | Optimal, standard, discards dominated days      | Worst-case single call is O(n); `>=` easy to flip       | Default optimal choice (your code)   |
| Stack of (price, span)           | Accumulate popped spans into today's span              | O(1) amortized / O(n)      | O(n) | No day counter, very readable                   | Accumulation step easy to get off-by-one                | Equivalent alternative encoding      |
| Span Array + Jump Pointers       | j -= spans[j] while prices[j] <= price                 | O(1) amortized / O(n)      | O(n) | No explicit stack, shows deep understanding     | Always O(n) memory, harder to prove                     | Follow-up: "without a stack?"        |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Monotonic Stack — PREVIOUS Greater Element (online). Cousins:
  LC 739 (Daily Temperatures), LC 503/496 (Next Greater Element), LC 84
  (Largest Rectangle in Histogram), LC 907 (Sum of Subarray Minimums).
- Go-to answer: "Span is the distance back to the previous strictly greater
  price. Keep a stack of (day, price) with strictly decreasing prices. On
  next(price), pop every entry with price <= today's, then span = day -
  stack top's day (or day + 1 if empty). Push today. Amortized O(1) per call,
  O(n) space."
- Good to call out: non-strict pop (`>=`) because equals extend the span,
  amortized (not worst-case) O(1), and why discarding popped days is safe.
- Common follow-ups:
  * "Why is it safe to discard popped days?" -> Today dominates them: any
    future day either beats today (and so them) or is blocked by today first.
  * "Can you avoid storing days?" -> (price, span) accumulation version.
  * "What if the span should use STRICTLY lower prices?" -> flip the pop to
    `>` (then equal prices stay on the stack and block the span).
  * "Offline / full array given?" -> same logic as computing the
    previous-greater-index for each i in one pass (LC 739 mirrored).
"""