'''

We will use a file-sharing system to share a very large file which consists of m small chunks with IDs from 1 to m.

When users join the system, the system should assign a unique ID to them. The unique ID should be used once for each user, but when a user leaves the system, the ID can be reused again.

Users can request a certain chunk of the file, the system should return a list of IDs of all the users who own this chunk. If the user receives a non-empty list of IDs, they receive the requested chunk successfully.
'''

import heapq

class FileSharing:

    def __init__(self, m: int):
        self.counter = 1
        self.chunks = [set() for _ in range(m + 1)]  # 1-indexed; slot 0 unused
        self.removed_user = []                         # min-heap of recycled IDs
        self.owner = {}                                # userId → set of chunkIds

    def join(self, ownedChunks: list) -> int:
        uid = heapq.heappop(self.removed_user) if self.removed_user else self.counter
        if uid == self.counter:
            self.counter += 1
        self.owner[uid] = set(ownedChunks)
        for chunk in ownedChunks:
            self.chunks[chunk].add(uid)
        return uid

    def leave(self, userId: int) -> None:
        for chunk in self.owner.pop(userId):
            self.chunks[chunk].discard(userId)
        heapq.heappush(self.removed_user, userId)

    def request(self, userId: int, chunkId: int) -> list:
        if userId not in self.owner:
            return []
        owners = sorted(self.chunks[chunkId])
        if owners:                               # non-empty → user receives the chunk
            self.chunks[chunkId].add(userId)
            self.owner[userId].add(chunkId)
        return owners

file = FileSharing(5)
print(file.join([1,2,3,4]))
print(file.join([5]))
print(file.request(2,2))
file.leave(1)
print(file.request(2,2))
print(file.request(2,1))


