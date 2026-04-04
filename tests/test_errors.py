import unittest

from src.db.backend.errors import (
    DuplicateIDError,
    InvalidAgeError,
    RecordNotFoundError,
    StudentTableError,
)


class TestErrors(unittest.TestCase):
    def test_exception_hierarchy(self) -> None:
        self.assertTrue(issubclass(StudentTableError, Exception))
        self.assertTrue(issubclass(InvalidAgeError, StudentTableError))
        self.assertTrue(issubclass(DuplicateIDError, StudentTableError))
        self.assertTrue(issubclass(RecordNotFoundError, StudentTableError))

    def test_can_raise_with_message(self) -> None:
        with self.assertRaises(StudentTableError) as ctx:
            raise StudentTableError("msg")
        self.assertEqual(str(ctx.exception), "msg")
