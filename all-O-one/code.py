'''
A data structure where you make sure that you can increment into a key and decrement a key
Have to find the maximum value and the minimum value
Methods:
increment(key)
decrement(key)
getMaxKey()
getMinKey()
'''

class Bucket:
    def __init__(self, count):
        self.count = count
        self.keys = set()
        self.prev = self.next = None


class AllOOne:
    def __init__(self):
        self.key_map = {}
        # Positive DLL (ascending): pos_head(0) ↔ bucket(1) ↔ bucket(2) ↔ ... ↔ pos_tail(+inf)
        self.pos_head = Bucket(0)
        self.pos_tail = Bucket(float('inf'))
        self.pos_head.next = self.pos_tail
        self.pos_tail.prev = self.pos_head
        # Negative DLL (head=-1 side, tail=most negative): neg_head(0) ↔ bucket(-1) ↔ bucket(-2) ↔ ... ↔ neg_tail(-inf)
        self.neg_head = Bucket(0)
        self.neg_tail = Bucket(float('-inf'))
        self.neg_head.next = self.neg_tail
        self.neg_tail.prev = self.neg_head

    def _insert_after(self, node, new_node):
        new_node.prev = node
        new_node.next = node.next
        node.next.prev = new_node
        node.next = new_node

    def _remove_bucket(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def increment(self, key: str) -> None:
        if key not in self.key_map:
            if self.pos_head.next.count != 1:
                self._insert_after(self.pos_head, Bucket(1))
            self.pos_head.next.keys.add(key)
            self.key_map[key] = self.pos_head.next
            return

        curr = self.key_map[key]
        target = curr.count + 1

        if target == 0:
            curr.keys.discard(key)
            del self.key_map[key]
            if not curr.keys:
                self._remove_bucket(curr)
            return

        if curr.count < 0:
            # In neg DLL: move toward neg_head (count increases, less negative)
            if curr.prev.count != target:
                self._insert_after(curr.prev, Bucket(target))
            dest = curr.prev
        else:
            # In pos DLL: move toward pos_tail (count increases)
            if curr.next.count != target:
                self._insert_after(curr, Bucket(target))
            dest = curr.next

        dest.keys.add(key)
        self.key_map[key] = dest
        curr.keys.discard(key)
        if not curr.keys:
            self._remove_bucket(curr)

    def decrement(self, key: str) -> None:
        if key not in self.key_map:
            if self.neg_head.next.count != -1:
                self._insert_after(self.neg_head, Bucket(-1))
            self.neg_head.next.keys.add(key)
            self.key_map[key] = self.neg_head.next
            return

        curr = self.key_map[key]
        target = curr.count - 1

        if target == 0:
            curr.keys.discard(key)
            del self.key_map[key]
            if not curr.keys:
                self._remove_bucket(curr)
            return

        if curr.count > 0:
            # In pos DLL: move toward pos_head (count decreases)
            if curr.prev.count != target:
                self._insert_after(curr.prev, Bucket(target))
            dest = curr.prev
        else:
            # In neg DLL: move toward neg_tail (count decreases, more negative)
            if curr.next.count != target:
                self._insert_after(curr, Bucket(target))
            dest = curr.next

        dest.keys.add(key)
        self.key_map[key] = dest
        curr.keys.discard(key)
        if not curr.keys:
            self._remove_bucket(curr)

    def getMaxKey(self) -> str:
        if self.pos_tail.prev is not self.pos_head:
            return next(iter(self.pos_tail.prev.keys))
        if self.neg_head.next is not self.neg_tail:
            return next(iter(self.neg_head.next.keys))
        return ""

    def getMinKey(self) -> str:
        if self.neg_tail.prev is not self.neg_head:
            return next(iter(self.neg_tail.prev.keys))
        if self.pos_head.next is not self.pos_tail:
            return next(iter(self.pos_head.next.keys))
        return ""
