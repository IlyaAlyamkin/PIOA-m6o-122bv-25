from .errors import (
    DuplicateIDError,
    InvalidAgeError,
    InvalidFieldError,
    RecordNotFoundError,
)

type StudentRecord = tuple[int, str, str, int, str]

_FIELD_INDEX: dict[str, int] = {
    "id": 0,
    "first_name": 1,
    "second_name": 2,
    "age": 3,
    "sex": 4,
}


class StudentTable:
    def __init__(self) -> None:
        self._student: list[StudentRecord] = []

    def create_record(
        self,
        student_id: int,
        first_name: str,
        second_name: str,
        age: int,
        sex: str,
    ) -> StudentRecord:
        if age < 0:
            raise InvalidAgeError("Поле age не может быть отрицательным.")

        if any(record[0] == student_id for record in self._student):
            raise DuplicateIDError(f"Запись с id={student_id} уже существует.")

        new_record: StudentRecord = (
            student_id,
            first_name.strip(),
            second_name.strip(),
            age,
            sex.strip(),
        )
        self._student.append(new_record)
        return new_record

    def select_record(
        self,
        student_id: int | None = None,
        first_name: str | None = None,
        second_name: str | None = None,
        age: int | None = None,
        sex: str | None = None,
    ) -> list[StudentRecord]:
        if (
            student_id is None
            and first_name is None
            and second_name is None
            and age is None
            and sex is None
        ):
            return self._student.copy()

        result: list[StudentRecord] = []

        for record in self._student:
            if student_id is not None and record[0] != student_id:
                continue

            if first_name is not None and record[1] != first_name:
                continue

            if second_name is not None and record[2] != second_name:
                continue

            if age is not None and record[3] != age:
                continue

            if sex is not None and record[4] != sex:
                continue

            result.append(record)

        return result

    def update_record(
        self,
        student_id: int,
        first_name: str | None = None,
        second_name: str | None = None,
        age: int | None = None,
        sex: str | None = None,
    ) -> StudentRecord:
        for i, record in enumerate(self._student):
            if record[0] != student_id:
                continue

            new_first_name = record[1] if first_name is None else first_name.strip()
            new_second_name = record[2] if second_name is None else second_name.strip()
            new_age = record[3] if age is None else age
            new_sex = record[4] if sex is None else sex.strip()

            if new_age < 0:
                raise InvalidAgeError("Поле age не может быть отрицательным.")

            updated_record: StudentRecord = (
                record[0],
                new_first_name,
                new_second_name,
                new_age,
                new_sex,
            )
            self._student[i] = updated_record
            return updated_record

        raise RecordNotFoundError("Запись с таким id не найдена.")

    def delete_record(self, student_id: int) -> StudentRecord:
        for i, record in enumerate(self._student):
            if record[0] == student_id:
                return self._student.pop(i)

        raise RecordNotFoundError("Запись с таким id не найдена.")

    def sort_records(self, field: str, *, descending: bool = False) -> list[StudentRecord]:
        if field not in _FIELD_INDEX:
            raise InvalidFieldError(f"Неизвестное поле: {field}")

        index = _FIELD_INDEX[field]
        return sorted(
            self._student,
            key=lambda record: record[index],
            reverse=descending,
        )
