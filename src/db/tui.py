try:
    from .backend.csv_file import CsvFileDatabase
    from .backend.errors import DatabaseError
    from .backend.file import FileDatabase
    from .backend.memory import MemoryDatabase
    from .backend.students import StudentRepository
except ImportError:  # pragma: no cover
    from backend.csv_file import CsvFileDatabase
    from backend.errors import DatabaseError
    from backend.file import FileDatabase
    from backend.memory import MemoryDatabase
    from backend.students import StudentRepository


def _choose_repository() -> StudentRepository:
    print("Выберите тип базы данных:")
    print("1. In-memory")
    print("2. File database (JSON)")
    print("3. File database (CSV)")

    choice = input("Введите номер: ").strip()
    if choice == "2":
        database = FileDatabase()
    elif choice == "3":
        database = CsvFileDatabase()
    else:
        database = MemoryDatabase()

    return StudentRepository(database)


def _print_menu() -> None:
    print("\n=== База студентов ===")
    print("1. Добавить запись")
    print("2. Показать все записи")
    print("3. Найти записи по фильтру")
    print("4. Обновить запись")
    print("5. Удалить запись")
    print("0. Выход")


def _read_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число.")


def _read_optional_int(prompt: str) -> int | None:
    while True:
        raw = input(prompt).strip()

        if raw == "":
            return None

        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число или оставьте поле пустым.")


def _print_records(records: list[dict]) -> None:
    if not records:
        print("Записи не найдены.")
        return

    for record in records:
        print(record)


def _add_student(repository: StudentRepository) -> None:
    print("\nДобавление записи")

    student_id = _read_int("id: ")
    first_name = input("first_name: ").strip()
    second_name = input("second_name: ").strip()
    age = _read_int("age: ")
    sex = input("sex: ").strip()

    try:
        record = repository.create_record(
            student_id,
            first_name,
            second_name,
            age,
            sex,
        )
        print(f"Запись добавлена: {record}")

    except DatabaseError as exc:
        print(f"Ошибка: {exc}")


def _show_all_students(repository: StudentRepository) -> None:
    print("\nСписок записей")
    _print_records(repository.select_record())


def _find_students_by_filter(repository: StudentRepository) -> None:
    print("\nПоиск по фильтру (Enter = пропустить поле)")

    student_id = _read_optional_int("id: ")
    first_name = input("first_name: ").strip() or None
    second_name = input("second_name: ").strip() or None
    age = _read_optional_int("age: ")
    sex = input("sex: ").strip() or None

    records = repository.select_record(
        student_id=student_id,
        first_name=first_name,
        second_name=second_name,
        age=age,
        sex=sex,
    )
    _print_records(records)


def _update_student(repository: StudentRepository) -> None:
    print("\nОбновление записи (Enter = оставить старое значение)")
    student_id = _read_int("id записи для изменения: ")

    first_name_raw = input("new first_name: ").strip()
    second_name_raw = input("new second_name: ").strip()
    age = _read_optional_int("new age: ")
    sex_raw = input("new sex: ").strip()

    first_name = None if first_name_raw == "" else first_name_raw
    second_name = None if second_name_raw == "" else second_name_raw
    sex = None if sex_raw == "" else sex_raw

    try:
        updated = repository.update_record(
            student_id=student_id,
            first_name=first_name,
            second_name=second_name,
            age=age,
            sex=sex,
        )
        print(f"Запись обновлена: {updated}")
    except DatabaseError as exc:
        print(f"Ошибка: {exc}")


def _delete_student(repository: StudentRepository) -> None:
    print("\nУдаление записи")
    student_id = _read_int("id записи для удаления: ")
    try:
        deleted = repository.delete_record(student_id)
        print(f"Запись удалена: {deleted}")
    except DatabaseError as exc:
        print(f"Ошибка: {exc}")


def run() -> None:
    """Запускает основной цикл текстового пользовательского интерфейса."""
    repository = _choose_repository()

    while True:
        _print_menu()
        action = input("Выберите действие: ").strip()
        if action == "1":
            _add_student(repository)

        elif action == "2":
            _show_all_students(repository)

        elif action == "3":
            _find_students_by_filter(repository)

        elif action == "4":
            _update_student(repository)

        elif action == "5":
            _delete_student(repository)

        elif action == "0":
            print("Выход из программы.")
            break

        else:
            print("Неизвестная команда. Повторите ввод.")
