#!/usr/bin/env python3.6
""" Tests the """
import unittest
import pcutils
pcutils.add_to_python_path(__file__, '..')
import basic_utils


class TestBasicUtils(unittest.TestCase):
    """ Tests the basic_utils module"""

    def test_clear_screen(self):
        """ Tests that the right amount of new lines were printed, including the last
        one added automatically by python"""
        expected = "\n" * 81
        with pcutils.MockPrint() as mocked_print:
            basic_utils.clear_screen()
            print_output = mocked_print.stdout
        self.assertEqual(expected, print_output)

    def test_ask_int_with_valid_int_as_input(self):
        """ Tests that ask_int returns an int by passing a valid int in the form of a string"""
        with pcutils.MockInput(["1", "2"]):
            self.assertEqual(1, basic_utils.ask_int(""))

    def test_ask_int_with_invalid_int_as_input(self):
        """ Tests that ask_int returns an int by passing an invalid int and then a valid int, both
        in the form of a string"""
        expected = "test error message\n"
        with pcutils.MockInput(["a", "2"], loop=False), pcutils.MockPrint() as mocked_print:
            self.assertEqual(2, basic_utils.ask_int("", error_message="test error message"))
            self.assertEqual(expected, mocked_print.stdout)

    def test_isint_not_int(self):
        """ Tests that isint returns false when a non-integer string is passed in"""
        self.assertFalse(basic_utils.isint("a"))

    def test_isint_valid_int(self):
        """ Tests that isint returns true when an integer string is passed in"""
        self.assertTrue(basic_utils.isint("1"))

    def test_write_to_json(self):
        """ Tests that data was written to a json file correctly"""
        data_to_write = {"hello": "world"}
        expected = '{\n    "hello": "world"\n}'
        with pcutils.TemporaryFile(suffix=".json") as temp_file:
            basic_utils.write_to_json(temp_file.path, data_to_write)
            file_contents = temp_file.read()
        self.assertEqual(expected, file_contents)


if __name__ == '__main__':
    unittest.main()
