import unittest
from unittest.mock import patch

from src.db.backend.memory import StudentTable
from src.db.tui import TUI, run


class TestTui(unittest.TestCase):
    def test_run_rejects_unknown_command_then_exits(self) -> None:
        user_input = ["nope", "0"]

        with patch("builtins.input", side_effect=user_input):
            with patch("builtins.print"):
                TUI(StudentTable()).run()

    def test_run_add_student_success(self) -> None:
        user_input = ["1", "7", "Ann", "Lee", "22", "F", "0"]

        with patch("builtins.input", side_effect=user_input):
            with patch("builtins.print"):
                TUI(StudentTable()).run()

    def test_run_add_student_invalid_id_then_success(self) -> None:
        user_input = ["1", "oops", "3", "Bob", "Brown", "19", "M", "0"]

        with patch("builtins.input", side_effect=user_input):
            with patch("builtins.print"):
                TUI(StudentTable()).run()

    def test_run_add_duplicate_id_shows_error(self) -> None:
        user_input = [
            "1",
            "1",
            "A",
            "B",
            "20",
            "M",
            "1",
            "1",
            "C",
            "D",
            "21",
            "F",
            "0",
        ]

        with patch("builtins.input", side_effect=user_input):
            with patch("builtins.print"):
                TUI(StudentTable()).run()

    def test_run_show_all_when_empty(self) -> None:
        user_input = ["2", "0"]

        with patch("builtins.input", side_effect=user_input):
            with patch("builtins.print"):
                TUI(StudentTable()).run()

    def test_run_find_with_optional_int_retry(self) -> None:
        user_input = [
            "1",
            "1",
            "A",
            "B",
            "20",
            "M",
            "3",
            "",
            "",
            "",
            "bad",
            "20",
            "",
            "0",
        ]

        with patch("builtins.input", side_effect=user_input):
            with patch("builtins.print"):
                TUI(StudentTable()).run()

    def test_run_update_and_delete(self) -> None:
        user_input = [
            "1",
            "10",
            "X",
            "Y",
            "18",
            "M",
            "4",
            "10",
            "X2",
            "",
            "",
            "",
            "5",
            "10",
            "0",
        ]

        with patch("builtins.input", side_effect=user_input):
            with patch("builtins.print"):
                TUI(StudentTable()).run()

    def test_run_update_not_found(self) -> None:
        user_input = ["4", "999", "", "", "", "", "0"]

        with patch("builtins.input", side_effect=user_input):
            with patch("builtins.print"):
                TUI(StudentTable()).run()

    def test_run_delete_not_found(self) -> None:
        user_input = ["5", "999", "0"]

        with patch("builtins.input", side_effect=user_input):
            with patch("builtins.print"):
                TUI(StudentTable()).run()

    def test_default_table_is_created(self) -> None:
        tui = TUI()
        self.assertIsInstance(tui.table, StudentTable)

    def test_module_run_function(self) -> None:
        user_input = ["0"]

        with patch("builtins.input", side_effect=user_input):
            with patch("builtins.print"):
                run()
