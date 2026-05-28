from collections import deque
from sortedcontainers import SortedList

'''
the way to find the average
- keep the last m elements (so might use a queue?)
- remove the smallest k element and the largest k element
- find the average of the remaining

m=3
k=1
[1,7,3,4,5,6,2,8]

m=3
=> [6,2,8]
k=1
[6] so avg is 6?

Design: 3 SortedLists (low/mid/high) + running mid_sum
- low : exactly k smallest elements
- mid : exactly m-2k middle elements, sum tracked in mid_sum
- high: exactly k largest elements
- deque: FIFO order so we know which element leaves the window

Invariant (once window is full):
  max(low) <= min(mid) <= min(high)
  len(low)=k, len(mid)=m-2k, len(high)=k
'''

class MKAverage:

    def __init__(self, m: int, k: int):
        self.m = m
        self.k = k
        self.queue = deque()
        self.low = SortedList()
        self.mid = SortedList()
        self.high = SortedList()
        self.mid_sum = 0

    def addElement(self, num: int) -> None:
        self.queue.append(num)
        self._insert(num)

        if len(self.queue) > self.m:
            oldest = self.queue.popleft()
            self._remove(oldest)

        self._rebalance()

    def calculateMKAverage(self) -> int:
        if len(self.queue) < self.m:
            return -1
        return self.mid_sum // (self.m - 2 * self.k)

    def _insert(self, num: int) -> None:
        if not self.low or num <= self.low[-1]:
            self.low.add(num)
        elif not self.high or num >= self.high[0]:
            self.high.add(num)
        else:
            self.mid.add(num)
            self.mid_sum += num

    def _remove(self, num: int) -> None:
        if num <= self.low[-1]:
            self.low.remove(num)
        elif num >= self.high[0]:
            self.high.remove(num)
        else:
            self.mid.remove(num)
            self.mid_sum -= num

    def _rebalance(self) -> None:
        # Fix low to exactly k elements
        if len(self.low) > self.k:
            val = self.low.pop()        # max of low
            self.mid.add(val)
            self.mid_sum += val
        elif len(self.low) < self.k and self.mid:
            val = self.mid.pop(0)       # min of mid
            self.mid_sum -= val
            self.low.add(val)

        # Fix high to exactly k elements (mid absorbs/gives the difference)
        if len(self.high) > self.k:
            val = self.high.pop(0)      # min of high
            self.mid.add(val)
            self.mid_sum += val
        elif len(self.high) < self.k and self.mid:
            val = self.mid.pop()        # max of mid
            self.mid_sum -= val
            self.high.add(val)


if __name__ == "__main__":
    obj = MKAverage(3, 1)
    obj.addElement(3)
    obj.addElement(1)
    obj.addElement(12)
    print(obj.calculateMKAverage())  # window=[3,1,12], drop 1 and 12 → 3
    obj.addElement(5) 
    obj.addElement(3) 
    print(obj.calculateMKAverage())  # window=[12,5,3], drop 3 and 12 → 5
    obj.addElement(4)
    print(obj.calculateMKAverage())  # window=[5,3,4], drop 3 and 5 → 4
