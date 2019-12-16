from .task import Task
from .socket import Socket


def run_tasks(tasks):
    running = [task.run() for task in tasks]
    while len(running):
        for i, task in enumerate(running):
            try:
                task.send(None)
            except StopIteration:
                running.pop(i)
