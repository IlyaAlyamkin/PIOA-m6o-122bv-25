import csv
import tempfile
import unittest
from pathlib import Path

from src.db.backend.csv_file import CsvFileDatabase
from src.db.backend.errors import (
    InvalidStorageDataError,
    TableNotFoundError,
)
from src.db.backend.students import StudentRepository


class TestCsvFileDatabase(unittest.TestCase):
    def test_data_is_saved_between_instances(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            first_db = CsvFileDatabase(directory)
            first_db.create_table("students", ("student_id", "name"))
            first_db.insert_record(
                "students",
                {"student_id": 1, "name": "Иван"},
            )

            second_db = CsvFileDatabase(directory)
            records = second_db.select_records("students")

            self.assertEqual(
                records,
                [{"student_id": 1, "name": "Иван"}],
            )

    def test_csv_file_contains_header_and_data(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db = CsvFileDatabase(directory)
            db.create_table("students", ("student_id", "name"))
            db.insert_record("students", {"student_id": 1, "name": "Иван"})

            table_path = Path(directory) / "students.csv"
            with table_path.open("r", encoding="utf-8", newline="") as file:
                rows = list(csv.reader(file))

            self.assertEqual(
                rows,
                [
                    ["student_id", "name"],
                    ["1", "Иван"],
                ],
            )

    def test_empty_table_is_saved_with_header_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db = CsvFileDatabase(directory)
            db.create_table("students", ("student_id", "name"))

            table_path = Path(directory) / "students.csv"
            with table_path.open("r", encoding="utf-8", newline="") as file:
                rows = list(csv.reader(file))

            self.assertEqual(rows, [["student_id", "name"]])
            self.assertEqual(CsvFileDatabase(directory).select_records("students"), [])

    def test_select_with_filters(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db = CsvFileDatabase(directory)
            db.create_table("students", ("student_id", "name"))
            db.insert_record("students", {"student_id": 1, "name": "Иван"})
            db.insert_record("students", {"student_id": 2, "name": "Мария"})

            records = db.select_records("students", name="Мария")

            self.assertEqual(
                records,
                [{"student_id": 2, "name": "Мария"}],
            )

    def test_select_from_missing_table(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db = CsvFileDatabase(directory)

            with self.assertRaises(TableNotFoundError):
                db.select_records("students")

    def test_invalid_structure_raises(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            table_path = Path(directory) / "students.csv"
            table_path.write_text("student_id,name\n1\n", encoding="utf-8")

            db = CsvFileDatabase(directory)
            with self.assertRaises(InvalidStorageDataError):
                db.select_records("students")

    def test_empty_file_raises(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            table_path = Path(directory) / "students.csv"
            table_path.write_text("", encoding="utf-8")

            db = CsvFileDatabase(directory)
            with self.assertRaises(InvalidStorageDataError):
                db.select_records("students")

    def test_student_repository_persists_update_and_delete(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            first_repo = StudentRepository(CsvFileDatabase(directory))
            first_repo.create_record(1, "Ann", "Lee", 20, "F")
            first_repo.update_record(1, first_name="Anna")

            second_repo = StudentRepository(CsvFileDatabase(directory))
            self.assertEqual(
                second_repo.select_record(student_id=1)[0]["first_name"],
                "Anna",
            )

            second_repo.delete_record(1)
            self.assertEqual(second_repo.select_record(), [])
