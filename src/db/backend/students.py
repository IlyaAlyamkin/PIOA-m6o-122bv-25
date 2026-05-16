from typing import Any

from .database import Database
from .errors import DuplicateIDError, TableAlreadyExistsError

STUDENTS_TABLE = "students"
STUDENT_COLUMNS = ("student_id", "first_name", "second_name", "age", "sex")


class StudentRepository:
    """Операции над таблицей студентов через общий интерфейс Database."""

    def __init__(self, database: Database) -> None:
        self._database = database
        self._ensure_students_table()

    def create_record(
        self,
        student_id: int,
        first_name: str,
        second_name: str,
        age: int,
        sex: str,
    ) -> dict[str, Any]:
        if self._database.select_records(STUDENTS_TABLE, student_id=student_id):
            raise DuplicateIDError(f"Запись с id={student_id} уже существует.")

        record = {
            "student_id": student_id,
            "first_name": first_name,
            "second_name": second_name,
            "age": age,
            "sex": sex,
        }
        self._database.insert_record(STUDENTS_TABLE, record)
        return record

    def select_record(
        self,
        student_id: int | None = None,
        first_name: str | None = None,
        second_name: str | None = None,
        age: int | None = None,
        sex: str | None = None,
    ) -> list[dict[str, Any]]:
        filters: dict[str, Any] = {}
        if student_id is not None:
            filters["student_id"] = student_id
        if first_name is not None:
            filters["first_name"] = first_name
        if second_name is not None:
            filters["second_name"] = second_name
        if age is not None:
            filters["age"] = age
        if sex is not None:
            filters["sex"] = sex

        return self._database.select_records(STUDENTS_TABLE, **filters)

    def update_record(
        self,
        student_id: int,
        first_name: str | None = None,
        second_name: str | None = None,
        age: int | None = None,
        sex: str | None = None,
    ) -> dict[str, Any]:
        updates = {
            "first_name": first_name,
            "second_name": second_name,
            "age": age,
            "sex": sex,
        }
        return self._database.update_record(
            STUDENTS_TABLE,
            "student_id",
            student_id,
            updates,
        )

    def delete_record(self, student_id: int) -> dict[str, Any]:
        return self._database.delete_record(
            STUDENTS_TABLE,
            "student_id",
            student_id,
        )

    def _ensure_students_table(self) -> None:
        try:
            self._database.create_table(STUDENTS_TABLE, STUDENT_COLUMNS)
        except TableAlreadyExistsError:
            pass
