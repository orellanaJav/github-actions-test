import unittest
from lambda_1 import get_formatted_name


class NamesTestCase(unittest.TestCase):

    print('hola')

    def test_first_last_name(self):
        formatted_name = get_formatted_name('Janis', 'Joplin')
        self.assertEqual(formatted_name, 'Janis Joplin')

    def test_first_middle_last_name(self):
        formatted_name = get_formatted_name('Michael', 'J', 'Fox')
        self.assertEqual(formatted_name, 'Michael J Fox')


if __name__ == '__main__':
    unittest.main()
