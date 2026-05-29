'''
Have a task manager
Have the ability to add a task, per user and their priority
Being able to edit the priority of a task
Being able to remove a task
Execute whatever is at top
'''

import heapq
from enum import Enum

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class TaskManager:

    def __init__(self):
        self.map = {}   # taskID: (priority, userID, insertion_order)
        self.heap = []  # (-priority.value, insertion_order, taskID)
        self.counter = 0

    def add_task(self, taskID: int, userId: int, priority: Priority):
        if taskID in self.map:
            raise ValueError(f"task {taskID} already exists")
        self.counter += 1
        self.map[taskID] = (priority, userId, self.counter)
        heapq.heappush(self.heap, (-priority.value, self.counter, taskID))

    def edit_task(self, taskID: int, priority: Priority):
        if taskID not in self.map:
            raise KeyError(f"task {taskID} not found")
        _, userId, order = self.map[taskID]
        self.map[taskID] = (priority, userId, order)
        # Push updated entry; old heap entry is stale and will be skipped in exec
        heapq.heappush(self.heap, (-priority.value, order, taskID))

    def remove_task(self, taskID: int):
        if taskID not in self.map:
            raise KeyError(f"task {taskID} not found")
        del self.map[taskID]

    def exec(self):
        while self.heap:
            neg_pri, order, taskID = heapq.heappop(self.heap)
            if taskID not in self.map:
                continue  # lazy-deleted via remove_task
            stored_pri, userId, stored_order = self.map[taskID]
            if -neg_pri != stored_pri.value:
                continue  # stale entry superseded by edit_task
            del self.map[taskID]
            return taskID
        return None


priority = Priority
task = TaskManager()
task.add_task(1,1,priority.LOW)
task.add_task(2,1,priority.LOW)
task.add_task(3,1,priority.LOW)
task.edit_task(3,priority.HIGH)
task.add_task(4,1,priority.HIGH)
print(task.exec())
print(task.exec())
print(task.exec())
print(task.exec())
print(task.exec())

