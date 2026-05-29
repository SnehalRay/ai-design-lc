'''
Goal is to create a todo list

-add task (userId, taskDescription, due date (int), list of tags)
-get all the tasks (userId) -> return all tasks incomplete
-get getTasksForTag (userId, tags) -> return a list of all tasks incomplete with the tag by the user
- get all complete tasks (userId)
'''

from datetime import datetime
from typing import List

class Task:
    def __init__(self, user_id: int, description: str, due_date: datetime, tags: set[str]):
        self._user_id = user_id
        self._description = description
        self._due_date = due_date
        self._tags = set(tags)
        self._completed = False

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    def due_date(self) -> datetime:
        return self._due_date

    @due_date.setter
    def due_date(self, value: datetime):
        self._due_date = value

    @property
    def tags(self) -> set[str]:
        return set(self._tags)

    def add_tag(self, tag: str):
        self._tags.add(tag)

    def remove_tag(self, tag: str):
        self._tags.discard(tag)

    @property
    def completed(self) -> bool:
        return self._completed

    @completed.setter
    def completed(self, value: bool):
        self._completed = value


class ToDoList:

    def __init__(self):
        self._id = 1
        self._tasks: dict[int, list[Task]] = {}

    def add_task(self, user_id: int, task_description: str, due_date: datetime, tags: List[str]) -> Task:
        task = Task(self._id, task_description, due_date, set(tags))
        self._id += 1
        if user_id not in self._tasks:
            self._tasks[user_id] = []
        self._tasks[user_id].append(task)
        return task

    def get_all_tasks(self, user_id: int) -> List[Task]:
        return [t for t in self._tasks.get(user_id, []) if not t.completed]

    def get_all_tasks_for_tag(self, user_id: int, tag: str) -> List[Task]:
        return [t for t in self._tasks.get(user_id, []) if not t.completed and tag in t.tags]

    def get_all_complete_tasks(self, user_id: int) -> List[Task]:
        return [t for t in self._tasks.get(user_id, []) if t.completed]