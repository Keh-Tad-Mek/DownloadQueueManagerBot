import unittest
from utils.validate_queue_name import name_is_valid


class TestNameIsValid(unittest.TestCase):
    def test_valid_simple(self):
        self.assertEqual(name_is_valid("movies")[0], True)

    def test_valid_with_underscore(self):
        self.assertEqual(name_is_valid("my_movies")[0], True)

    def test_valid_with_numbers(self):
        self.assertEqual(name_is_valid("movies2024")[0], True)

    def test_valid_mixed_case(self):
        self.assertEqual(name_is_valid("MyMovies")[0], True)

    def test_invalid_too_short(self):
        self.assertEqual(name_is_valid("abc")[0], False)

    def test_invalid_too_long(self):
        self.assertEqual(name_is_valid("a" * 21)[0], False)

    def test_invalid_just_underscore(self):
        self.assertEqual(name_is_valid("_")[0], False)

    def test_invalid_starts_with_underscore(self):
        self.assertEqual(name_is_valid("_movies")[0], False)

    def test_invalid_ends_with_underscore(self):
        self.assertEqual(name_is_valid("movies_")[0], False)

    def test_invalid_starts_with_number(self):
        self.assertEqual(name_is_valid("2movies")[0], False)

    def test_invalid_all_numbers(self):
        self.assertEqual(name_is_valid("12345")[0], False)

    def test_invalid_contains_symbol(self):
        self.assertEqual(name_is_valid("mov!es")[0], False)


if __name__ == "__main__":
    unittest.main()