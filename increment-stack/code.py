

class CustomStack:
    def __init__(self, maxSize:int):
        self.maxSize = maxSize
        self.stk = []
        self.lazy = [0] * maxSize

    def push(self, x:int)->bool:
        if len(self.stk) == self.maxSize:
            return False
        self.stk.append(x)
        return True

    def pop(self)->int:
        if not self.stk:
            return -1
        i = len(self.stk) - 1
        if i > 0:
            self.lazy[i - 1] += self.lazy[i]  # propagate deferred increment down
        val = self.stk.pop() + self.lazy[i]
        self.lazy[i] = 0
        return val

    def inc(self, k:int, val:int)->None:
        if self.stk:
            i = min(k, len(self.stk)) - 1
            self.lazy[i] += val  # defer: mark top of affected range

stk = CustomStack(3)
print(stk.push(1))
print(stk.push(2))
print(stk.push(3))
print(stk.push(4))
print(stk.pop())
print(stk.push(3))
print(stk.inc(2,100))
print(stk.pop())
print(stk.pop())
print(stk.pop())

