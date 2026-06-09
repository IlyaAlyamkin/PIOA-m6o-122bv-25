import csv
from pathlib import Path
from typing import Any

from .database import Database
from .errors import InvalidStorageDataError, TableNotFoundError
from .table import Table


class CsvFileDatabase(Database):
    """База данных, которая хранит таблицы в CSV-файлах."""

    def __init__(self, directory: str = "data_csv") -> None:
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def _table_exists(self, table_name: str) -> bool:
        return self._get_table_path(table_name).exists()

    def _load_table(self, table_name: str) -> Table:
        table_path = self._get_table_path(table_name)
        if not table_path.exists():
            raise TableNotFoundError(
                f"Таблица '{table_name}' не существует."
            )

        try:
            with table_path.open("r", encoding="utf-8", newline="") as file:
                reader = csv.reader(file)
                rows = list(reader)
        except csv.Error as error:
            raise InvalidStorageDataError(
                "Файл таблицы содержит некорректный CSV."
            ) from error

        return self._deserialize_table(rows)

    def _save_table(self, table_name: str, table: Table) -> None:
        table_path = self._get_table_path(table_name)

        with table_path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self._serialize_table(table))

    def _get_table_path(self, table_name: str) -> Path:
        return self.directory / f"{table_name}.csv"

    def _serialize_table(self, table: Table) -> list[list[str]]:
        rows = [list(table.columns)]
        for record in table.records:
            rows.append([str(record[column]) for column in table.columns])
        return rows

    def _deserialize_table(self, rows: list[list[str]]) -> Table:
        if not rows or not rows[0]:
            raise InvalidStorageDataError(
                "Файл таблицы имеет некорректную структуру."
            )

        columns = tuple(rows[0])
        records: list[dict[str, Any]] = []

        for row in rows[1:]:
            if len(row) != len(columns):
                raise InvalidStorageDataError(
                    "Файл таблицы имеет некорректную структуру."
                )

            records.append(
                {
                    column: self._parse_cell(value)
                    for column, value in zip(columns, row, strict=True)
                }
            )

        return Table(columns, records)

    def _parse_cell(self, value: str) -> Any:
        if value == "":
            return value

        try:
            return int(value)
        except ValueError:
            return value
