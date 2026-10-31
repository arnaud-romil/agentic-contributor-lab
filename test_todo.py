import io
import unittest

from app import run_cli
from todo import TaskNotFoundError, TodoList


class TodoListTests(unittest.TestCase):
    def setUp(self):
        self.todos = TodoList()

    def test_new_task_has_unique_id_and_is_incomplete(self):
        first = self.todos.add_task("Buy milk")
        second = self.todos.add_task("Call Sam")

        self.assertEqual(first.id, 1)
        self.assertEqual(second.id, 2)
        self.assertFalse(first.completed)
        self.assertEqual(self.todos.list_tasks(), [first, second])

    def test_empty_description_is_rejected(self):
        for description in ("", "   "):
            with self.subTest(description=description):
                with self.assertRaises(ValueError):
                    self.todos.add_task(description)

    def test_mark_task_completed(self):
        task = self.todos.add_task("Buy milk")

        completed = self.todos.mark_completed(task.id)

        self.assertTrue(completed.completed)
        self.assertEqual(self.todos.list_tasks(), [completed])

    def test_delete_task_and_do_not_reuse_id(self):
        first = self.todos.add_task("Buy milk")
        self.todos.delete_task(first.id)

        next_task = self.todos.add_task("Call Sam")

        self.assertEqual(self.todos.list_tasks(), [next_task])
        self.assertEqual(next_task.id, 2)

    def test_unknown_ids_raise_task_not_found(self):
        for operation in (
            self.todos.mark_completed,
            self.todos.delete_task,
        ):
            with self.subTest(operation=operation.__name__):
                with self.assertRaises(TaskNotFoundError):
                    operation(42)


class CommandLineTests(unittest.TestCase):
    def run_app(self, commands):
        output = io.StringIO()
        run_cli(io.StringIO(commands), output)
        return output.getvalue()

    def test_menu_supports_adding_listing_completing_and_deleting(self):
        output = self.run_app("1\nBuy milk\n2\n3\n1\n2\n4\n1\n2\n5\n")

        self.assertIn("1. [ ] Buy milk", output)
        self.assertIn("1. [x] Buy milk", output)
        self.assertIn("No tasks.", output)

    def test_invalid_task_ids_are_reported_without_exiting(self):
        output = self.run_app("3\nabc\n3\n42\n4\n42\n5\n")

        self.assertIn("Please enter a valid task ID.", output)
        self.assertEqual(output.count("Task 42 does not exist."), 2)
        self.assertIn("Goodbye.", output)

    def test_empty_description_is_rejected(self):
        output = self.run_app("1\n   \n2\n5\n")

        self.assertIn("Task description cannot be empty.", output)
        self.assertIn("No tasks.", output)


if __name__ == "__main__":
    unittest.main()