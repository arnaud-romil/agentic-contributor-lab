import sys
from typing import Optional, TextIO

from todo import TaskNotFoundError, TodoList


def run_cli(
    input_stream: Optional[TextIO] = None,
    output_stream: Optional[TextIO] = None,
) -> None:
    if input_stream is None:
        input_stream = sys.stdin
    if output_stream is None:
        output_stream = sys.stdout

    todos = TodoList()
    while True:
        _print_menu(output_stream)
        choice = _read_line(input_stream, output_stream, "Choice: ")
        if choice is None:
            return

        choice = choice.strip()
        if choice == "1":
            description = _read_line(input_stream, output_stream, "Description: ")
            if description is None:
                return
            try:
                task = todos.add_task(description)
            except ValueError as error:
                print(error, file=output_stream)
            else:
                print(f"Task {task.id} added.", file=output_stream)
        elif choice == "2":
            _print_tasks(todos, output_stream)
        elif choice == "3":
            task_id = _read_task_id(input_stream, output_stream)
            if task_id is None:
                continue
            try:
                todos.mark_completed(task_id)
            except TaskNotFoundError as error:
                print(error, file=output_stream)
            else:
                print(f"Task {task_id} completed.", file=output_stream)
        elif choice == "4":
            task_id = _read_task_id(input_stream, output_stream)
            if task_id is None:
                continue
            try:
                todos.delete_task(task_id)
            except TaskNotFoundError as error:
                print(error, file=output_stream)
            else:
                print(f"Task {task_id} deleted.", file=output_stream)
        elif choice == "5":
            print("Goodbye.", file=output_stream)
            return
        else:
            print("Invalid choice.", file=output_stream)


def _print_menu(output_stream: TextIO) -> None:
    print("\nTODO application", file=output_stream)
    print("1. Add task", file=output_stream)
    print("2. List tasks", file=output_stream)
    print("3. Mark task completed", file=output_stream)
    print("4. Delete task", file=output_stream)
    print("5. Exit", file=output_stream)


def _print_tasks(todos: TodoList, output_stream: TextIO) -> None:
    tasks = todos.list_tasks()
    if not tasks:
        print("No tasks.", file=output_stream)
        return

    for task in tasks:
        status = "x" if task.completed else " "
        print(f"{task.id}. [{status}] {task.description}", file=output_stream)


def _read_task_id(input_stream: TextIO, output_stream: TextIO) -> Optional[int]:
    raw_task_id = _read_line(input_stream, output_stream, "Task ID: ")
    if raw_task_id is None:
        return None

    try:
        return int(raw_task_id)
    except ValueError:
        print("Please enter a valid task ID.", file=output_stream)
        return None


def _read_line(
    input_stream: TextIO,
    output_stream: TextIO,
    prompt: str,
) -> Optional[str]:
    output_stream.write(prompt)
    output_stream.flush()
    line = input_stream.readline()
    if line == "":
        return None
    return line.rstrip("\r\n")


def main() -> None:
    run_cli()


if __name__ == "__main__":
    main()