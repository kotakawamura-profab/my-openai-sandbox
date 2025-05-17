import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

DATA_FILE = Path('tasks.json')

@dataclass
class Task:
    description: str
    completed: bool = False

@dataclass
class TaskManager:
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, description: str):
        self.tasks.append(Task(description=description))
        self.save()

    def list_tasks(self) -> List[Task]:
        return self.tasks

    def complete_task(self, index: int):
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = True
            self.save()

    def delete_task(self, index: int):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save()

    def save(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([task.__dict__ for task in self.tasks], f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls):
        if DATA_FILE.exists():
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            tasks = [Task(**item) for item in data]
            return cls(tasks=tasks)
        return cls()


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Simple task manager')
    subparsers = parser.add_subparsers(dest='command')

    add_parser = subparsers.add_parser('add', help='Add a task')
    add_parser.add_argument('description', help='Task description')

    list_parser = subparsers.add_parser('list', help='List tasks')

    done_parser = subparsers.add_parser('done', help='Mark task as completed')
    done_parser.add_argument('index', type=int, help='Task index (starting from 1)')

    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('index', type=int, help='Task index (starting from 1)')

    args = parser.parse_args()
    manager = TaskManager.load()

    if args.command == 'add':
        manager.add_task(args.description)
        print(f'Added task: {args.description}')
    elif args.command == 'list':
        for i, task in enumerate(manager.list_tasks(), start=1):
            status = '✓' if task.completed else ' '
            print(f'{i}. [{status}] {task.description}')
    elif args.command == 'done':
        manager.complete_task(args.index - 1)
        print(f'Task {args.index} marked as completed')
    elif args.command == 'delete':
        manager.delete_task(args.index - 1)
        print(f'Task {args.index} deleted')
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
