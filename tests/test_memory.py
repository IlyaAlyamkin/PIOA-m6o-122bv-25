import unittest

from src.db.backend.errors import (
    DuplicateIDError,
    InvalidAgeError,
    MissingColumnError,
    RecordNotFoundError,
    TableAlreadyExistsError,
    UnknownColumnError,
)
from src.db.backend.memory import MemoryDatabase
from src.db.backend.students import STUDENT_COLUMNS, StudentRepository
from src.db.backend.table import Table


class TestTable(unittest.TestCase):
    def test_insert_and_select(self) -> None:
        table = Table(("student_id", "name"))
        table.insert_record({"student_id": 1, "name": "Иван"})

        self.assertEqual(
            table.select_records(),
            [{"student_id": 1, "name": "Иван"}],
        )

    def test_select_with_filter(self) -> None:
        table = Table(("student_id", "name"))
        table.insert_record({"student_id": 1, "name": "Иван"})
        table.insert_record({"student_id": 2, "name": "Мария"})

        self.assertEqual(
            table.select_records(name="Мария"),
            [{"student_id": 2, "name": "Мария"}],
        )

    def test_missing_column_on_insert(self) -> None:
        table = Table(("student_id", "name"))
        with self.assertRaises(MissingColumnError):
            table.insert_record({"student_id": 1})

    def test_unknown_column_on_insert(self) -> None:
        table = Table(("student_id", "name"))
        with self.assertRaises(UnknownColumnError):
            table.insert_record({"student_id": 1, "name": "A", "extra": 1})


class TestMemoryDatabase(unittest.TestCase):
    def setUp(self) -> None:
        self.database = MemoryDatabase()
        self.repository = StudentRepository(self.database)

    def test_create_table_twice_raises(self) -> None:
        self.database.create_table("extra", ("id",))
        with self.assertRaises(TableAlreadyExistsError):
            self.database.create_table("extra", ("id",))

    def test_create_record(self) -> None:
        record = self.repository.create_record(1, "John", "Doe", 20, "M")
        self.assertEqual(
            record,
            {
                "student_id": 1,
                "first_name": "John",
                "second_name": "Doe",
                "age": 20,
                "sex": "M",
            },
        )

    def test_create_record_negative_age(self) -> None:
        with self.assertRaises(InvalidAgeError) as context:
            self.repository.create_record(1, "John", "Doe", -1, "M")
        self.assertEqual(str(context.exception), "Поле age не может быть отрицательным.")

    def test_create_record_duplicate_id(self) -> None:
        self.repository.create_record(1, "John", "Doe", 20, "M")
        with self.assertRaises(DuplicateIDError) as context:
            self.repository.create_record(1, "Jane", "Smith", 22, "F")
        self.assertEqual(str(context.exception), "Запись с id=1 уже существует.")

    def test_select_record_filters(self) -> None:
        self.repository.create_record(1, "John", "Doe", 20, "M")
        self.repository.create_record(2, "Jane", "Smith", 22, "F")

        self.assertEqual(len(self.repository.select_record()), 2)
        self.assertEqual(
            self.repository.select_record(student_id=1),
            [
                {
                    "student_id": 1,
                    "first_name": "John",
                    "second_name": "Doe",
                    "age": 20,
                    "sex": "M",
                }
            ],
        )

    def test_update_record_partial(self) -> None:
        self.repository.create_record(1, "Old", "Name", 20, "M")
        updated = self.repository.update_record(1, first_name="New")
        self.assertEqual(updated["first_name"], "New")
        self.assertEqual(updated["second_name"], "Name")

    def test_update_record_not_found(self) -> None:
        with self.assertRaises(RecordNotFoundError):
            self.repository.update_record(99, first_name="X")

    def test_delete_record(self) -> None:
        self.repository.create_record(1, "A", "B", 20, "M")
        deleted = self.repository.delete_record(1)
        self.assertEqual(deleted["student_id"], 1)
        self.assertEqual(self.repository.select_record(), [])

    def test_students_table_has_expected_columns(self) -> None:
        table = self.database._load_table("students")
        self.assertEqual(table.columns, STUDENT_COLUMNS)

    def test_select_record_with_all_filters(self) -> None:
        self.repository.create_record(1, "Ann", "Lee", 20, "F")
        self.repository.create_record(2, "Ann", "Kim", 20, "M")

        found = self.repository.select_record(
            first_name="Ann",
            age=20,
            sex="F",
        )
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["student_id"], 1)

    def test_update_record_negative_age(self) -> None:
        self.repository.create_record(1, "A", "B", 20, "M")
        with self.assertRaises(InvalidAgeError):
            self.repository.update_record(1, age=-1)
