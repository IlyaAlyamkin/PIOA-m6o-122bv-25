import unittest

from src.db.backend.errors import (
    DuplicateIDError,
    InvalidAgeError,
    RecordNotFoundError,
)
from src.db.backend.memory import StudentTable


class TestMemory(unittest.TestCase):
    def setUp(self) -> None:
        self.student_table = StudentTable()
        self.assertIsInstance(self.student_table, StudentTable)

    def test_student_table_allocation(self) -> None:
        student_table = StudentTable()
        self.assertIsInstance(student_table, StudentTable)

    def test_create_record(self) -> None:
        cases = [
            (1, "John", "Doe", 20, "M"),
            (2, "Jane", "Smith", 22, "F"),
            (3, "Alice", "Johnson", 19, "F"),
            (4, "Bob", "Brown", 21, "M"),
            (5, "Charlie", "Davis", 18, "M"),
            (6, "Eve", "Miller", 23, "F"),
            (7, "Frank", "Wilson", 20, "M"),
            (8, "Grace", "Moore", 22, "F"),
            (9, "Hank", "Taylor", 19, "M"),
            (10, "Ivy", "Anderson", 21, "F"),
            (11, "Jack", "Thomas", 18, "M"),
            (12, "Kathy", "Jackson", 23, "F"),
        ]

        for test_data in cases:
            # Используем subTest для изоляции каждого тестового случая и улучшения читаемости результатов тестирования.
            # Это позволяет нам видеть, какой именно набор данных вызвал ошибку, если тест не пройдет.
            with self.subTest(test_data=test_data):
                record = self.student_table.create_record(*test_data)
                self.assertEqual(record, test_data)

    def test_create_record_negative_age(self) -> None:
        cases = [
            (1, "John", "Doe", -1, "M"),
            (2, "Jane", "Smith", -5, "F"),
            (3, "Alice", "Johnson", -10, "F"),
        ]
        error_message = "Поле age не может быть отрицательным."

        for test_data in cases:
            with self.subTest(test_data=test_data):
                with self.assertRaises(InvalidAgeError) as context:
                    self.student_table.create_record(*test_data)
                self.assertEqual(str(context.exception), error_message)

    def test_create_record_duplicate_id(self) -> None:
        test_data_1 = (1, "John", "Doe", 20, "M")
        test_data_2 = (1, "Jane", "Smith", 22, "F")
        error_message = "Запись с id=1 уже существует."

        self.student_table.create_record(*test_data_1)

        with self.assertRaises(DuplicateIDError) as context:
            self.student_table.create_record(*test_data_2)

        self.assertEqual(str(context.exception), error_message)

    def test_select_record(self) -> None:
        # Подготовка тестовых данных для проверки функции select_record.
        test_datas = [
            (1, "John", "Doe", 20, "M"),
            (2, "Jane", "Smith", 22, "F"),
            (3, "Alice", "Johnson", 19, "F"),
            (4, "Bob", "Brown", 21, "M"),
            (5, "Charlie", "Davis", 18, "M"),
            (6, "Eve", "Miller", 23, "F"),
            (7, "Frank", "Wilson", 20, "M"),
            (8, "Grace", "Moore", 22, "F"),
            (9, "Hank", "Taylor", 19, "M"),
            (10, "Ivy", "Anderson", 21, "F"),
        ]

        for test_data in test_datas:
            self.student_table.create_record(*test_data)

        # Формирование тестовых случаев для функции select_record.
        # Каждый случай включает в себя описание, набор фильтров и ожидаемый результат.
        cases = [
            {
                "name": "Выбор без фильтров",
                "filters": {},
                "expected": test_datas,
            },
            {
                "name": "Фильтр по ID",
                "filters": {"student_id": 1},
                "expected": [test_datas[0]],
            },
            {
                "name": "Фильтр по имени",
                "filters": {"first_name": "Jane"},
                "expected": [test_datas[1]],
            },
            {
                "name": "Фильтр по фамилии",
                "filters": {"second_name": "Johnson"},
                "expected": [test_datas[2]],
            },
            {
                "name": "Фильтр по возрасту",
                "filters": {"age": 20},
                "expected": [test_datas[0], test_datas[6]],
            },
            {
                "name": "Фильтр по полу",
                "filters": {"sex": "F"},
                "expected": [
                    test_datas[1],
                    test_datas[2],
                    test_datas[5],
                    test_datas[7],
                    test_datas[9],
                ],
            },
        ]

        for case in cases:
            with self.subTest(
                case=case["name"], filters=case["filters"], expected=case["expected"]
            ):
                records = self.student_table.select_record(**case["filters"])
                self.assertEqual(records, case["expected"])

    def test_create_record_strips_whitespace(self) -> None:
        record = self.student_table.create_record(1, "  Ann ", "  Lee  ", 21, " F ")
        self.assertEqual(record, (1, "Ann", "Lee", 21, "F"))

    def test_select_record_no_matches(self) -> None:
        self.student_table.create_record(1, "Solo", "One", 20, "M")
        self.assertEqual(
            self.student_table.select_record(student_id=99),
            [],
        )

    def test_select_record_combined_filters(self) -> None:
        self.student_table.create_record(1, "Ann", "Lee", 20, "F")
        self.student_table.create_record(2, "Ann", "Kim", 20, "M")
        found = self.student_table.select_record(
            first_name="Ann",
            age=20,
            sex="F",
        )
        self.assertEqual(found, [(1, "Ann", "Lee", 20, "F")])

    def test_update_record_partial_fields(self) -> None:
        self.student_table.create_record(1, "Old", "Name", 20, "M")
        updated = self.student_table.update_record(1, first_name="New")
        self.assertEqual(updated, (1, "New", "Name", 20, "M"))

    def test_update_record_all_fields(self) -> None:
        self.student_table.create_record(1, "A", "B", 20, "M")
        updated = self.student_table.update_record(
            1,
            first_name="C",
            second_name="D",
            age=21,
            sex="F",
        )
        self.assertEqual(updated, (1, "C", "D", 21, "F"))

    def test_update_record_negative_age(self) -> None:
        self.student_table.create_record(1, "A", "B", 20, "M")
        with self.assertRaises(InvalidAgeError) as ctx:
            self.student_table.update_record(1, age=-1)
        self.assertEqual(str(ctx.exception), "Поле age не может быть отрицательным.")

    def test_update_record_not_found(self) -> None:
        with self.assertRaises(RecordNotFoundError) as ctx:
            self.student_table.update_record(999, first_name="X")
        self.assertEqual(str(ctx.exception), "Запись с таким id не найдена.")

    def test_delete_record_removes_row(self) -> None:
        self.student_table.create_record(1, "A", "B", 20, "M")
        deleted = self.student_table.delete_record(1)
        self.assertEqual(deleted, (1, "A", "B", 20, "M"))
        self.assertEqual(self.student_table.select_record(), [])

    def test_delete_record_not_found(self) -> None:
        with self.assertRaises(RecordNotFoundError) as ctx:
            self.student_table.delete_record(42)
        self.assertEqual(str(ctx.exception), "Запись с таким id не найдена.")

    def test_update_record_after_skipping_other_rows(self) -> None:
        self.student_table.create_record(1, "A", "A", 20, "M")
        self.student_table.create_record(2, "B", "B", 21, "F")
        updated = self.student_table.update_record(2, first_name="Bee")
        self.assertEqual(updated, (2, "Bee", "B", 21, "F"))

    def test_delete_record_after_skipping_other_rows(self) -> None:
        self.student_table.create_record(1, "A", "A", 20, "M")
        self.student_table.create_record(2, "B", "B", 21, "F")
        deleted = self.student_table.delete_record(2)
        self.assertEqual(deleted, (2, "B", "B", 21, "F"))
        self.assertEqual(len(self.student_table.select_record()), 1)
