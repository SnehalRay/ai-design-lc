'''
A router object with a given memory limit
you can add a packet - must be unique (from id, to id, timestamp).
forward: basically send it in a FIFO method
get count
'''

from datetime import datetime
from typing import Optional


class Packet:
    def __init__(self, from_id: int, to_id: int, timestamp: datetime):
        self.__from_id = from_id
        self.__to_id = to_id
        self.__timestamp = timestamp

    @property
    def from_id(self) -> int:
        return self.__from_id

    @property
    def to_id(self) -> int:
        return self.__to_id

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp
    
class Router:
    def __init__(self, memoryLimit: int):
        self.__memory_limit = memoryLimit
        self.__store: dict[tuple[int, int], Packet] = {}

    def add_packet(self, from_id: int, to_id: int, timestamp: datetime) -> bool:
        if (from_id, to_id) in self.__store:
            return False
        if len(self.__store) == self.__memory_limit:
            self.__store.pop(next(iter(self.__store)))
        self.__store[(from_id, to_id)] = Packet(from_id, to_id, timestamp)
        return True

    def get_forward(self) -> Optional[Packet]:
        if not self.__store:
            return None
        key = next(iter(self.__store))
        return self.__store.pop(key)

    def get_count(self) -> int:
        return len(self.__store)
    
router = Router(2)

print(router.add_packet(1,2,datetime.now()))
print(router.add_packet(1,2,datetime.now()))
print(router.add_packet(2,3,datetime.now()))
print(router.add_packet(3,4,datetime.now()))
print(router.get_count())
res = router.get_forward()
print(res.from_id, res.to_id)
