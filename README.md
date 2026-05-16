## Алямкин Илья Владимирович, М6О-122БВ-25, Python

In-memory и файловая СУБД студентов с общим объектно-ориентированным интерфейсом.

## Структура проекта

```
PIOA-НомерГруппы/
├── src/
│   └── db/
│       ├── backend/
│       │   ├── __init__.py
│       │   ├── database.py      # абстрактный класс Database
│       │   ├── errors.py        # пользовательские исключения
│       │   ├── file.py          # FileDatabase (JSON на диске)
│       │   ├── memory.py        # MemoryDatabase (в памяти)
│       │   ├── students.py      # StudentRepository (таблица students)
│       │   └── table.py         # класс Table
│       ├── __init__.py
│       ├── __main__.py
│       └── tui.py
├── data/                        # JSON-файлы таблиц (для FileDatabase)
├── tests/
│   ├── __init__.py
│   ├── test_memory.py
│   └── test_file_database.py
└── README.md
```

## In-memory и файловая реализация

| Аспект | MemoryDatabase | FileDatabase |
|--------|----------------|--------------|
| Хранение | словарь таблиц в RAM | каталог `data/`, файл на таблицу (`имя.json`) |
| Сохранение после выхода | нет | да |
| Интерфейс | `Database` | `Database` |
| Формат на диске | — | JSON: `columns`, `records` |

Обе реализации используют класс `Table` и методы `create_table`, `insert_record`, `select_records`, `update_record`, `delete_record`.

Для работы со студентами в TUI применяется `StudentRepository` (таблица `students`, поля: `student_id`, `first_name`, `second_name`, `age`, `sex`).

## Функциональность

- выбор типа БД при старте: **1** — in-memory, **2** — файловая;
- добавление, просмотр, поиск по фильтрам, обновление, удаление записей;
- проверка возраста, уникальности `student_id`, схемы таблицы;
- обработка ошибок файлов (повреждённый JSON, некорректная структура) через `InvalidStorageDataError`.

## Запуск

Из корня проекта:

```bash
python -m src.db
```

При выборе файловой БД данные сохраняются в `data/students.json`.

## Тесты

```bash
pip install pytest pytest-cov
python -m pytest
```

Только `unittest`:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Порог покрытия **≥ 80%** задан в `pyproject.toml`.

## Требования

- Python **3.12+**
