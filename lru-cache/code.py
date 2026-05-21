class Node:

    def __init__(self, key, val):
        self.next = None
        self.prev = None
        self.key = key
        self.val = val

class LRUCache:

    def __init__(self, capacity):
        self.back, self.front = Node(0,0), Node(0,0)
        self.cache = {} #key: Node
        self.back.next = self.front
        self.front.prev = self.back
        self.capacity = capacity

    def push(self,key,value)->None:
        if key in self.cache:
            self.remove(self.cache[key])
        node = Node(key,value)
        self.add_to_end(node)
        self.cache[key] = node

        if len(self.cache)>self.capacity:
            remove_node = self.back.next
            if remove_node.key in self.cache:
                self.remove(remove_node)
                del self.cache[remove_node.key]


    def get(self,key)->int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self.remove(node)
        self.add_to_end(node)
        return node.val

    #HELPER FUNCTION:
    def add_to_end(self,node)-> None:
        prev,nxt = self.front.prev, self.front
        prev.next = node
        node.prev = prev
        nxt.prev = node
        node.next = nxt

    def remove(self,node)->None:
        prev,nxt = node.prev, node.next
        prev.next = nxt
        nxt.prev = prev

