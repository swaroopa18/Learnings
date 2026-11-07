"""
LeetCode 707 - Design Linked List
----------------------------------
Design a singly linked list with these operations (indices are 0-based):

    get(index)              -> value at index, or -1 if index is invalid
    addAtHead(val)          -> insert a new node before the first node
    addAtTail(val)          -> append a new node as the last node
    addAtIndex(index, val)  -> insert before the node currently at `index`;
                               if index == size it appends; if index > size
                               (or index < 0) nothing happens
    deleteAtIndex(index)    -> delete the node at `index` if it is valid

Two approaches are given below.

Summary
-------
 #  Approach                         get   addHead  addTail  addIndex  delete   Notes
 1  Head + size (your 1st version)   O(n)  O(1)     O(n)     O(n)      O(n)     Simplest state, slow tail append
 2  Head + tail + size (RECOMMENDED) O(n)  O(1)     O(1)     O(n)      O(n)*    O(1) tail append; *O(1) at head

All approaches use O(1) extra space per operation and O(n) space to store
the n nodes.

Invariants worth remembering (every method must preserve these):
    - `size` always equals the number of nodes in the list.
    - `head` is None  <=>  size == 0.
    - (Approach 2) `tail` is the LAST node, and `tail` is None <=> size == 0.
"""


class ListNode:
    def __init__(self, val=0, next_node=None):
        self.val = val
        self.next = next_node


class MyLinkedListBasic:
    """
    Approach 1: Singly Linked List with `head` and `size` (your first version)
    ----------------------------------------------------------------------------
    State:
      - head : first node (None when empty)
      - size : number of nodes, so index checks are O(1) and never need a walk

    Idea per operation:
      - get(index):
          Walk from head, counting. Return the value when the counter hits
          `index`, otherwise fall off the end and return -1.
      - addAtHead(val):
          Delegates to addAtIndex(0, val), so there is only one insert path.
      - addAtTail(val):
          Bump size, then walk to the last node (curr.next is None) and hook
          the new node on. If the list is empty the new node becomes head.
      - addAtIndex(index, val):
          * Reject index < 0 or index > size.
          * index == size  -> it's really an append, reuse addAtTail.
          * index == 0     -> new node points at old head, becomes new head.
          * otherwise      -> a DUMMY node placed before head lets us walk to
            the node just BEFORE `index` (the predecessor) and splice:
                new_node.next = pred.next
                pred.next     = new_node
      - deleteAtIndex(index):
          * Reject index < 0 or index >= size.
          * Use a dummy node again so deleting the head needs no special
            case: find the predecessor and set pred.next = pred.next.next.
          * Re-point head to dummy.next (this is what makes head deletion work).

    The dummy-node trick:
      - A dummy node sitting before head means EVERY real node, including the
        first, has a predecessor. That removes the "is this the head?" branch
        from delete (and is the standard technique for list problems).

    Time Complexity:
      - get          O(n)  -- walk up to `index` nodes
      - addAtHead    O(1)  -- no walking
      - addAtTail    O(n)  -- must walk to the end because there is no tail pointer
      - addAtIndex   O(n)  -- walk to the predecessor
      - deleteAtIndex O(n) -- walk to the predecessor
    Space Complexity: O(1) extra per operation.

    Things to be aware of:
      - `size` is updated in several places (addAtTail, addAtIndex,
        deleteAtIndex). addAtIndex deliberately does NOT bump size on the
        `index == size` path because addAtTail does it. Easy to double count
        or miss when editing.
      - The `while curr` / `while curr and curr.next` checks are defensive:
        because index is validated against `size` first, the loop always
        finds its target, so those conditions never end the loop on their own.
      - addAtTail is the weak spot: n appends cost O(n^2) overall. Approach 2
        fixes exactly this.
    """

    def __init__(self):
        self.head = None
        self.size = 0

    def get(self, index: int) -> int:
        if index < 0:
            return -1

        idx = 0
        curr = self.head
        while curr:
            if idx == index:
                return curr.val
            idx += 1
            curr = curr.next
        return -1

    def addAtHead(self, val: int) -> None:
        self.addAtIndex(0, val)

    def addAtTail(self, val: int) -> None:
        self.size += 1
        new_node = ListNode(val)
        if not self.head:
            self.head = new_node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node

    def addAtIndex(self, index: int, val: int) -> None:
        if index < 0 or self.size < index:
            return
        if self.size == index:
            self.addAtTail(val)
            return
        new_node = ListNode(val)
        self.size += 1
        if index == 0:
            new_node.next = self.head
            self.head = new_node
            return

        dummy = ListNode(0, self.head)
        curr = dummy
        idx = 0
        while curr:
            if idx == index:
                temp = curr.next
                new_node.next = temp
                curr.next = new_node
                break
            else:
                idx += 1
                curr = curr.next
        self.head = dummy.next

    def deleteAtIndex(self, index: int) -> None:
        if index < 0 or self.size <= index:
            return
        dummy = ListNode(0, self.head)
        curr = dummy
        idx = 0
        while curr and curr.next:
            if idx == index:
                curr.next = curr.next.next
                break
            else:
                curr = curr.next
                idx += 1
        self.size -= 1
        self.head = dummy.next


class MyLinkedList:
    """
    Approach 2 (RECOMMENDED): Singly Linked List with `head`, `tail` and `size`
    -----------------------------------------------------------------------------
    State:
      - head : first node (None when empty)
      - tail : last node  (None when empty)
      - size : number of nodes

    Idea:
      - Keep a direct pointer to the last node so appending never needs a walk.
      - Each method has ONE clear responsibility and updates `size` exactly
        once, at its own end.

    Idea per operation:
      - get(index):
          Validate against size (index < 0 or index >= size -> -1), then walk
          `index` steps from head. No None checks needed in the loop because
          the validation guarantees the node exists.
      - addAtHead(val):
          Empty list: head and tail both become the new node.
          Otherwise: new_node.next = head; head = new_node. Tail is untouched.
      - addAtTail(val):
          Empty list: head and tail both become the new node.
          Otherwise: tail.next = new_node; tail = new_node. O(1), no walk.
      - addAtIndex(index, val):
          * Reject index < 0 or index > size.
          * index == 0     -> addAtHead.
          * index == size  -> addAtTail.
          * otherwise      -> walk index - 1 steps to the predecessor and
            splice: new_node = ListNode(val, pred.next); pred.next = new_node.
            Head and tail cannot change on this path (the new node is strictly
            in the middle), which is why the two ends are handled separately
            above.
      - deleteAtIndex(index):
          * Reject index < 0 or index >= size.
          * index == 0: head = head.next. If the list is now empty, also reset
            tail = None (otherwise tail would point at a deleted node).
          * otherwise walk to the predecessor. If the node being removed is
            the tail, move tail back to the predecessor. Then unlink:
            pred.next = pred.next.next.

    Edge cases handled:
      - Empty list: get/delete return or do nothing; adds set head AND tail.
      - Deleting the only node: head becomes None and tail is reset to None.
      - Deleting the last node: tail moves back to its predecessor.
      - Inserting at index == size behaves as an append and updates tail.
      - Negative and too-large indices are rejected before any pointer moves.

    Time Complexity:
      - get           O(n)
      - addAtHead     O(1)
      - addAtTail     O(1)  -- the improvement over Approach 1
      - addAtIndex    O(n)  -- O(1) when index is 0 or size
      - deleteAtIndex O(n)  -- O(1) when deleting the head
    Space Complexity: O(1) extra per operation.

    Why it's better:
      - n appends cost O(n) total instead of O(n^2).
      - Cleaner flow: ends are special-cased explicitly and the middle case
        is a plain predecessor splice, with no dummy node or `while curr`
        guards to reason about.
      - `size` has a single owner per method, so it can't drift.

    Still not O(1) for the middle: a singly linked list can't remove or insert
    at an arbitrary position without first finding the predecessor. Deleting
    the TAIL is also O(n) here, because we must walk to the node before it.
    A doubly linked list (prev pointers) makes tail deletion O(1).
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def get(self, index: int) -> int:
        if index < 0 or index >= self.size:
            return -1

        curr = self.head
        for _ in range(index):
            curr = curr.next

        return curr.val

    def addAtHead(self, val: int) -> None:
        new_node = ListNode(val)

        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node

        self.size += 1

    def addAtTail(self, val: int) -> None:
        new_node = ListNode(val)

        if not self.tail:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1

    def addAtIndex(self, index: int, val: int) -> None:
        if index < 0 or index > self.size:
            return

        if index == 0:
            self.addAtHead(val)
            return

        if index == self.size:
            self.addAtTail(val)
            return

        curr = self.head
        for _ in range(index - 1):
            curr = curr.next

        new_node = ListNode(val, curr.next)
        curr.next = new_node
        self.size += 1

    def deleteAtIndex(self, index: int) -> None:
        if index < 0 or index >= self.size:
            return

        if index == 0:
            self.head = self.head.next
            self.size -= 1

            if self.size == 0:
                self.tail = None
            return

        curr = self.head
        for _ in range(index - 1):
            curr = curr.next

        if curr.next == self.tail:
            self.tail = curr

        curr.next = curr.next.next
        self.size -= 1


# Your MyLinkedList object will be instantiated and called as such:
# obj = MyLinkedList()
# param_1 = obj.get(index)
# obj.addAtHead(val)
# obj.addAtTail(val)
# obj.addAtIndex(index,val)
# obj.deleteAtIndex(index)