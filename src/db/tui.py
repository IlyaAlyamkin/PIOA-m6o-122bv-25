from backend.memory import create_record, delete_record, select_record, update_record
def _print_menu() -> None:
    # Символ \n обозначает перевод строки.
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

def _add_student() -> None:
    print("\nДобавление записи")

    student_id = _read_int("id: ")
    first_name = input("first_name: ").strip()
    second_name = input("second_name: ").strip()
    age = _read_int("age: ")
    sex = input("sex: ").strip()

    try:
        record = create_record(student_id, first_name, second_name, age, sex)
        print(f"Запись добавлена: {record}")

    except ValueError as exc:
        print(f"Ошибка: {exc}")

def _print_records(records: list[tuple[int, str, str, int, str]]) -> None:
    if not records:
        print("Записи не найдены.")
        return

    for record in records:
        print(record)
def _show_all_students() -> None:
    print("\nСписок записей")
    _print_records(select_record())
def _read_optional_int(prompt: str) -> int | None:
    while True:
        raw = input(prompt).strip()

        if raw == "":
            return None

        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число или оставьте поле пустым.")
def _find_students_by_filter() -> None:
    print("\nПоиск по фильтру (Enter = пропустить поле)")

    student_id = _read_optional_int("id: ")

    first_name = input("first_name: ").strip() or None
    second_name = input("second_name: ").strip() or None

    age = _read_optional_int("age: ")
    sex = input("sex: ").strip() or None

    records = select_record(
        student_id=student_id,
        first_name=first_name,
        second_name=second_name,
        age=age,
        sex=sex,
    )

    _print_records(records)


def _update_student() -> None:
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
        updated = update_record(
            student_id=student_id,
            first_name=first_name,
            second_name=second_name,
            age=age,
            sex=sex,
        )
        print(f"Запись обновлена: {updated}")
    except ValueError as exc:
        print(f"Ошибка: {exc}")


def _delete_student() -> None:
    print("\nУдаление записи")
    student_id = _read_int("id записи для удаления: ")
    try:
        deleted = delete_record(student_id)
        print(f"Запись удалена: {deleted}")
    except ValueError as exc:
        print(f"Ошибка: {exc}")


def run() -> None:
    """
    Запускает основной цикл текстового пользовательского интерфейса.

    Цикл выполняется до тех пор, пока пользователь явно
    не выберет завершение программы.
    """
    while True:
        _print_menu()
        action = input("Выберите действие: ").strip()
        if action == "1":
            _add_student()

        elif action == "2":
            _show_all_students()

        elif action == "3":
            _find_students_by_filter()

        elif action == "4":
            _update_student()

        elif action == "5":
            _delete_student()

        elif action == "0":
            print("Выход из программы.")
            break

        else:
            print("Неизвестная команда. Повторите ввод.")



