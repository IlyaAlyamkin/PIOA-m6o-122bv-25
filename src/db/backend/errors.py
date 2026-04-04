class StudentTableError(Exception):
    """Базовый класс для ошибок, связанных с таблицей Student."""

    pass


class InvalidAgeError(StudentTableError):
    """Ошибка, возникающая при попытке создать запись с некорректным возрастом."""

    pass


class DuplicateIDError(StudentTableError):
    """Ошибка, возникающая при попытке создать запись с уже существующим идентификатором."""

    pass


class RecordNotFoundError(StudentTableError):
    """Ошибка, возникающая при обращении к несуществующей записи по id."""

    pass
