import unittest
from unittest.mock import patch

from src.db import tui


class TestTui(unittest.TestCase):
    def test_run_memory_database_flow(self) -> None:
        user_input = [
            "1",
            "1",
            "7",
            "Ann",
            "Lee",
            "22",
            "F",
            "2",
            "0",
        ]
        with patch("builtins.input", side_effect=user_input):
            with patch("builtins.print"):
                tui.run()

    def test_run_file_database_flow(self) -> None:
        user_input = [
            "2",
            "1",
            "3",
            "Bob",
            "Brown",
            "19",
            "M",
            "0",
        ]
        with patch("builtins.input", side_effect=user_input):
            with patch("builtins.print"):
                tui.run()

    def test_run_csv_file_database_flow(self) -> None:
        user_input = [
            "3",
            "1",
            "4",
            "Ann",
            "Lee",
            "21",
            "F",
            "0",
        ]
        with patch("builtins.input", side_effect=user_input):
            with patch("builtins.print"):
                tui.run()

    def test_run_unknown_command(self) -> None:
        user_input = ["1", "bad", "0"]
        with patch("builtins.input", side_effect=user_input):
            with patch("builtins.print"):
                tui.run()
