from typing import Any

from .errors import (
    InvalidAgeError,
    MissingColumnError,
    RecordNotFoundError,
    UnknownColumnError,
)


class Table:
    """Таблица с фиксированным набором колонок."""

    def __init__(
        self,
        columns: tuple[str, ...],
        records: list[dict[str, Any]] | None = None,
    ) -> None:
        self.columns = columns
        self.records: list[dict[str, Any]] = []

        if records is not None:
            for record in records:
                self.insert_record(record)

    def insert_record(self, record: dict[str, Any]) -> None:
        """Добавляет запись, если она соответствует схеме таблицы."""
        normalized = self._normalize_record(record)
        self._validate_record_schema(normalized)
        self.records.append(normalized)

    def select_records(self, **filters: Any) -> list[dict[str, Any]]:
        """Возвращает записи, удовлетворяющие всем переданным фильтрам."""
        unknown_filters = [key for key in filters if key not in self.columns]
        if unknown_filters:
            raise UnknownColumnError(
                f"Поле '{unknown_filters[0]}' не определено в структуре таблицы."
            )

        if not filters:
            return [record.copy() for record in self.records]

        result: list[dict[str, Any]] = []
        for record in self.records:
            if all(record.get(key) == value for key, value in filters.items()):
                result.append(record.copy())

        return result

    def update_record(
        self,
        key_column: str,
        key_value: Any,
        updates: dict[str, Any | None],
    ) -> dict[str, Any]:
        """Обновляет запись по ключу. Значение None в updates поле не меняет."""
        if key_column not in self.columns:
            raise UnknownColumnError(
                f"Поле '{key_column}' не определено в структуре таблицы."
            )

        unknown_updates = [key for key in updates if key not in self.columns]
        if unknown_updates:
            raise UnknownColumnError(
                f"Поле '{unknown_updates[0]}' не определено в структуре таблицы."
            )

        for index, record in enumerate(self.records):
            if record.get(key_column) != key_value:
                continue

            updated = record.copy()
            for column, value in updates.items():
                if value is not None:
                    updated[column] = (
                        value.strip() if isinstance(value, str) else value
                    )

            self._validate_age(updated)
            self.records[index] = updated
            return updated.copy()

        raise RecordNotFoundError("Запись с таким id не найдена.")

    def delete_record(self, key_column: str, key_value: Any) -> dict[str, Any]:
        """Удаляет запись по ключу и возвращает удалённую копию."""
        if key_column not in self.columns:
            raise UnknownColumnError(
                f"Поле '{key_column}' не определено в структуре таблицы."
            )

        for index, record in enumerate(self.records):
            if record.get(key_column) == key_value:
                return self.records.pop(index)

        raise RecordNotFoundError("Запись с таким id не найдена.")

    def _normalize_record(self, record: dict[str, Any]) -> dict[str, Any]:
        normalized = record.copy()
        for column in self.columns:
            if column not in normalized:
                continue
            value = normalized[column]
            if isinstance(value, str):
                normalized[column] = value.strip()
        return normalized

    def _validate_record_schema(self, record: dict[str, Any]) -> None:
        missing_columns = [column for column in self.columns if column not in record]
        if missing_columns:
            raise MissingColumnError(
                f"Отсутствует поле '{missing_columns[0]}' в записи."
            )

        extra_columns = [column for column in record if column not in self.columns]
        if extra_columns:
            raise UnknownColumnError(
                f"Поле '{extra_columns[0]}' не определено в структуре таблицы."
            )

        self._validate_age(record)

    def _validate_age(self, record: dict[str, Any]) -> None:
        if "age" in record and record["age"] < 0:
            raise InvalidAgeError("Поле age не может быть отрицательным.")
