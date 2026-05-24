'''
Implement the RandomizedSet class:

RandomizedSet() Initializes the RandomizedSet object.
bool insert(int val) Inserts an item val into the set if not present. Returns true if the item was not present, false otherwise.
bool remove(int val) Removes an item val from the set if present. Returns true if the item was present, false otherwise.
int getRandom() Returns a random element from the current set of elements (it's guaranteed that at least one element exists when this method is called). Each element must have the same probability of being returned.
You must implement the functions of the class such that each function works in average O(1) time complexity.


self.lst = []
self.hashmap = defaultdict(list)
'''

from collections import defaultdict
import random

class RandomizedCollection:

    def __init__(self):
        self.lst = []
        self.hashmap = defaultdict(set)

    def insert(self,val:int)->bool:
        res = True
        if val in self.hashmap:
            res = False
        self.hashmap[val].add(len(self.lst))
        self.lst.append(val)
        return res

    def remove(self,val:int)->bool:
        if val not in self.hashmap:
            return False
        last_idx = self.hashmap[val].pop()
        if last_idx == len(self.lst)-1:
            self.lst.pop()
        else:
            last_ele = self.lst.pop()
            old_idx = len(self.lst)  # index last_ele occupied before the pop
            self.lst[last_idx] = last_ele
            self.hashmap[last_ele].discard(old_idx)
            self.hashmap[last_ele].add(last_idx)
        if len(self.hashmap[val])==0:
            del self.hashmap[val]
        return True


    def getRandom(self)->int:
        if not self.lst:
            return None
        return random.choice(self.lst)


def main():
    rc = RandomizedCollection()

    print("insert(5):", rc.insert(5))   # True  (first occurrence)
    print("insert(5):", rc.insert(5))   # False (duplicate)
    print("insert(3):", rc.insert(3))   # True
    print("lst:", rc.lst, "map:", dict(rc.hashmap))

    # 5 appears twice, 3 once — getRandom should reflect that distribution
    counts = {3: 0, 5: 0}
    for _ in range(9000):
        counts[rc.getRandom()] += 1
    print("getRandom distribution (expect ~2:1 for 5:3):", counts)

    # Remove one 5 — list should still have [5, 3]
    print("\nremove(5):", rc.remove(5))  # True
    print("lst:", rc.lst, "map:", dict(rc.hashmap))

    # Remove the second 5
    print("remove(5):", rc.remove(5))   # True
    print("lst:", rc.lst, "map:", dict(rc.hashmap))

    # 5 is gone — removing again should return False
    print("remove(5):", rc.remove(5))   # False

    # Remove 3 — collection should be empty
    print("remove(3):", rc.remove(3))   # True
    print("lst:", rc.lst, "map:", dict(rc.hashmap))

    # Same-value swap edge case: [5, 3, 5], remove one 5 via swap with last element (also 5)
    print("\n--- same-value swap edge case ---")
    rc2 = RandomizedCollection()
    rc2.insert(5); rc2.insert(3); rc2.insert(5)
    print("lst:", rc2.lst, "map:", dict(rc2.hashmap))
    rc2.remove(5)
    print("after remove(5):", rc2.lst, "map:", dict(rc2.hashmap))
    rc2.remove(5)
    print("after remove(5):", rc2.lst, "map:", dict(rc2.hashmap))


if __name__ == "__main__":
    main()
