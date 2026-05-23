class Node:
    def __init__(self, val):
        self.next = None
        self.prev = None
        self.val = val


class CircularDeque:

    def __init__(self, capacity:int):
        self.capacity = capacity
        self.root = Node(None)
        self.root.next = self.root
        self.root.prev = self.root
        self.size = 0

    def insertFront(self,val)->bool:
        if self.size>=self.capacity:
            return False
        new_node = Node(val)
        new_node.prev = self.root
        self.root.next.prev = new_node
        new_node.next = self.root.next
        self.root.next = new_node
        self.size+=1
        return True


    def insertBack(self,val)->bool:
        if self.size >= self.capacity:
            return False
        new_node = Node(val)
        new_node.next = self.root
        new_node.prev = self.root.prev
        self.root.prev.next = new_node
        self.root.prev = new_node
        self.size += 1
        return True

    def removeFront(self)->bool:
        if self.isEmpty():
            return False
        remove_node = self.root.next
        self.root.next = remove_node.next
        remove_node.next.prev = self.root
        self.size-=1
        return True


    def removeBack(self)->bool:
        if self.isEmpty():
            return False
        remove_node = self.root.prev
        self.root.prev = remove_node.prev
        remove_node.prev.next = self.root
        self.size-=1
        return True

    def getFront(self)->int:
        if self.isEmpty():
            return -1
        return self.root.next.val

    def getBack(self)->int:
        if self.isEmpty():
            return -1
        return self.root.prev.val

    def isFull(self)->bool:
        return self.size==self.capacity

    def isEmpty(self)->bool:
        return self.size==0


if __name__ == "__main__":
    dq = CircularDeque(3)

    print("isEmpty:", dq.isEmpty())              # True
    print("insertFront(1):", dq.insertFront(1))  # True
    print("insertBack(2):", dq.insertBack(2))    # True
    print("insertFront(3):", dq.insertFront(3))  # True  → [3, 1, 2]
    print("isFull:", dq.isFull())                # True
    print("insertBack(9):", dq.insertBack(9))    # False (full)
    print("getFront:", dq.getFront())            # 3
    print("getBack:", dq.getBack())              # 2
    print("removeFront:", dq.removeFront())      # True  → [1, 2]
    print("getFront:", dq.getFront())            # 1
    print("removeBack:", dq.removeBack())        # True  → [1]
    print("getBack:", dq.getBack())              # 1
    print("removeFront:", dq.removeFront())      # True  → []
    print("isEmpty:", dq.isEmpty())              # True
    print("getFront:", dq.getFront())            # -1


