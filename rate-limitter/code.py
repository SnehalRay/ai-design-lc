from collections import deque

'''
Make a rate limiter
User will be unique

Sliding window approach

methods:
adding (user, timestamp) -> boolean
_queue_pop(queue,timestamp) -> pops expired timestamps

timestamp - stored >= window_size
'''

class RateLimiter:
    def __init__(self, window_size=10, max_length = 5):
        self.window_size = window_size
        self.max_length = max_length
        self.hashmap = {} #user: queue()

    def adding_data(self, user: str, timestamp: int) -> bool:
        if self.max_length == 0:
            return False
        if user not in self.hashmap:
            self.hashmap[user] = deque([timestamp])
            return True
        self._queue_pop(self.hashmap[user], timestamp)
        if len(self.hashmap[user]) >= self.max_length:
            return False
        self.hashmap[user].append(timestamp)
        return True

    def _queue_pop(self, queue, timestamp) -> None:
        while queue and timestamp - queue[0] >= self.window_size:
            queue.popleft()


if __name__ == "__main__":
    rl = RateLimiter(window_size=10, max_length=5)

    # fill up to limit
    for i in range(5):
        print(rl.adding_data("alice", 1))   # True x5

    # over limit
    print(rl.adding_data("alice", 1))       # False

    # window expires — oldest entries are now >= 10s old
    print(rl.adding_data("alice", 11))      # True

    # new user always allowed
    print(rl.adding_data("bob", 5))         # True

    # zero max_length — nothing allowed
    rl_zero = RateLimiter(window_size=10, max_length=0)
    print(rl_zero.adding_data("alice", 1))  # False
    
