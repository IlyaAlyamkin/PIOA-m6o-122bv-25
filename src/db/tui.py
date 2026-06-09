try:
    from .backend.errors import StudentTableError
    from .backend.memory import StudentTable
except ImportError:  
    from backend.errors import StudentTableError
    from backend.memory import StudentTable


class TUI:
    """Текстовый интерфейс для работы с таблицей студентов."""

    def __init__(self, table: StudentTable | None = None) -> None:
        self.table = table or StudentTable()

    def run(self) -> None:
        """Запускает основной цикл взаимодействия с пользователем."""
        while True:
            self._print_menu()
            action = input("Выберите действие: ").strip()

            if action == "1":
                self._add_student()

            elif action == "2":
                self._show_all_students()

            elif action == "3":
                self._find_students_by_filter()

            elif action == "4":
                self._update_student()

            elif action == "5":
                self._delete_student()

            elif action == "6":
                self._sort_students()

            elif action == "0":
                print("Выход из программы.")
                break

            else:
                print("Неизвестная команда. Повторите ввод.")

    def _print_menu(self) -> None:
        print("\n=== База студентов ===")
        print("1. Добавить запись")
        print("2. Показать все записи")
        print("3. Найти записи по фильтру")
        print("4. Обновить запись")
        print("5. Удалить запись")
        print("6. Сортировать записи")
        print("0. Выход")

    def _read_int(self, prompt: str) -> int:
        while True:
            raw = input(prompt).strip()
            try:
                return int(raw)
            except ValueError:
                print("Ошибка: введите целое число.")

    def _read_optional_int(self, prompt: str) -> int | None:
        while True:
            raw = input(prompt).strip()

            if raw == "":
                return None

            try:
                return int(raw)
            except ValueError:
                print("Ошибка: введите целое число или оставьте поле пустым.")

    def _print_records(self, records: list[tuple[int, str, str, int, str]]) -> None:
        if not records:
            print("Записи не найдены.")
            return

        for record in records:
            print(record)

    def _add_student(self) -> None:
        print("\nДобавление записи")

        student_id = self._read_int("id: ")
        first_name = input("first_name: ").strip()
        second_name = input("second_name: ").strip()
        age = self._read_int("age: ")
        sex = input("sex: ").strip()

        try:
            record = self.table.create_record(
                student_id,
                first_name,
                second_name,
                age,
                sex,
            )
            print(f"Запись добавлена: {record}")

        except StudentTableError as exc:
            print(f"Ошибка: {exc}")

    def _show_all_students(self) -> None:
        print("\nСписок записей")
        self._print_records(self.table.select_record())

    def _find_students_by_filter(self) -> None:
        print("\nПоиск по фильтру (Enter = пропустить поле)")

        student_id = self._read_optional_int("id: ")
        first_name = input("first_name: ").strip() or None
        second_name = input("second_name: ").strip() or None
        age = self._read_optional_int("age: ")
        sex = input("sex: ").strip() or None

        records = self.table.select_record(
            student_id=student_id,
            first_name=first_name,
            second_name=second_name,
            age=age,
            sex=sex,
        )
        self._print_records(records)

    def _update_student(self) -> None:
        print("\nОбновление записи (Enter = оставить старое значение)")
        student_id = self._read_int("id записи для изменения: ")

        first_name_raw = input("new first_name: ").strip()
        second_name_raw = input("new second_name: ").strip()
        age = self._read_optional_int("new age: ")
        sex_raw = input("new sex: ").strip()

        first_name = None if first_name_raw == "" else first_name_raw
        second_name = None if second_name_raw == "" else second_name_raw
        sex = None if sex_raw == "" else sex_raw

        try:
            updated = self.table.update_record(
                student_id=student_id,
                first_name=first_name,
                second_name=second_name,
                age=age,
                sex=sex,
            )
            print(f"Запись обновлена: {updated}")
        except StudentTableError as exc:
            print(f"Ошибка: {exc}")

    def _sort_students(self) -> None:
        print("\nСортировка записей")
        print("1. id")
        print("2. first_name")
        print("3. second_name")
        print("4. age")
        print("5. sex")

        field_map = {
            "1": "id",
            "2": "first_name",
            "3": "second_name",
            "4": "age",
            "5": "sex",
        }

        field_choice = input("Выберите поле: ").strip()
        field = field_map.get(field_choice)

        if field is None:
            print("Ошибка: неверный выбор поля.")
            return

        print("1. По возрастанию")
        print("2. По убыванию")
        order_choice = input("Выберите порядок: ").strip()

        if order_choice == "1":
            descending = False
        elif order_choice == "2":
            descending = True
        else:
            print("Ошибка: неверный выбор порядка.")
            return

        try:
            records = self.table.sort_records(field, descending=descending)
            self._print_records(records)
        except StudentTableError as exc:
            print(f"Ошибка: {exc}")

    def _delete_student(self) -> None:
        print("\nУдаление записи")
        student_id = self._read_int("id записи для удаления: ")
        try:
            deleted = self.table.delete_record(student_id)
            print(f"Запись удалена: {deleted}")
        except StudentTableError as exc:
            print(f"Ошибка: {exc}")


def run() -> None:
    """Запускает TUI (точка входа для __main__ и тестов)."""
    TUI().run()
