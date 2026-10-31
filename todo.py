from collections import namedtuple
from typing import List


class TaskNotFoundError(LookupError):
    def __init__(self, task_id):
        super().__init__(f"Task {task_id} does not exist.")
        self.task_id = task_id


Task = namedtuple("Task", "id description completed")


class TodoList:
    def __init__(self):
        self._tasks = {}
        self._next_id = 1

    def add_task(self, description: str) -> Task:
        if not isinstance(description, str) or not description.strip():
            raise ValueError("Task description cannot be empty.")

        task = Task(self._next_id, description.strip(), False)
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def list_tasks(self) -> List[Task]:
        return list(self._tasks.values())

    def mark_completed(self, task_id: int) -> Task:
        task = self._get_task(task_id)
        completed_task = task._replace(completed=True)
        self._tasks[task_id] = completed_task
        return completed_task

    def delete_task(self, task_id: int) -> Task:
        task = self._get_task(task_id)
        del self._tasks[task_id]
        return task

    def _get_task(self, task_id: int) -> Task:
        if type(task_id) is not int or task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        return self._tasks[task_id]