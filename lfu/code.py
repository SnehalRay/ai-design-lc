'''
Implement an LFU Cache with a capacity
two main methods: int get(int key)
void put(int key, int value)
'''
from collections import defaultdict


class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.freq = 1
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = Node(0, 0)  # sentinel
        self.tail = Node(0, 0)  # sentinel
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def add_front(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1

    def remove_back(self):
        if self.is_empty():
            return None
        node = self.tail.prev
        self.remove(node)
        return node

    def is_empty(self):
        return self.size == 0


class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.min_freq = 0
        self.key_map = {}
        self.freq_map = defaultdict(DoublyLinkedList)

    def _update(self, node):
        self.freq_map[node.freq].remove(node)
        if self.freq_map[node.freq].is_empty() and node.freq == self.min_freq:
            self.min_freq += 1
        node.freq += 1
        self.freq_map[node.freq].add_front(node)

    def get(self, key):
        if key not in self.key_map:
            return -1
        node = self.key_map[key]
        self._update(node)
        return node.val

    def put(self, key, value):
        if self.capacity == 0:
            return
        if key in self.key_map:
            node = self.key_map[key]
            node.val = value
            self._update(node)
        else:
            if self.size == self.capacity:
                evicted = self.freq_map[self.min_freq].remove_back()
                del self.key_map[evicted.key]
                self.size -= 1
            node = Node(key, value)
            self.key_map[key] = node
            self.freq_map[1].add_front(node)
            self.min_freq = 1
            self.size += 1


if __name__ == "__main__":
    cache = LFUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    print(cache.get(1))
    cache.put(3,3)
    print(cache.get(2))
    print(cache.get(3))
    print(cache.get(1))
    print(cache.get(1))
    print(cache.get(3))
    cache.put(4,4)
    print(cache.get(3))



    # assert cache.get(1) == 1      # freq[1]=2, freq[2]=1
    # cache.put(3, 3)               # evicts key 2 (min_freq=1, LRU in that bucket)
    # assert cache.get(2) == -1
    # assert cache.get(3) == 3
    # cache.put(4, 4)               # evicts key 3 (freq[3]=1, freq[1]=2)
    # assert cache.get(1) == 1
    # assert cache.get(3) == -1
    # assert cache.get(4) == 4
    # print("All assertions passed")
