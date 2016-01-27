import unittest
from todict import todict

class ToDictTest(unittest.TestCase):
    def test_one_key(self):
        input_list = ['user1', 'user2', 'user3']
        input_key = 'name'
        expected_output = [
            dict(name='user1'),
            dict(name='user2'),
            dict(name='user3')
        ]

        output = todict(input_list, input_key)
        return self.assertEqual(output, expected_output)

    def test_two_keys(self):
        input_list = [
            ['user1', 'pwd1'],
            ['user2', 'pwd2'],
            ['user3', 'pwd3']
        ]
        input_keys = ('name', 'password')
        expected_output = [
            dict(name='user1', password='pwd1'),
            dict(name='user2', password='pwd2'),
            dict(name='user3', password='pwd3')
        ]

        output = todict(input_list, *input_keys)
        return self.assertEqual(output, expected_output)

    def test_list_longer_than_number_of_keys(self):
        input_list = [
            ['user1', 'pwd1', '1000'],
            ['user2', 'pwd2', '2000'],
            ['user3', 'pwd3', '3000']
        ]
        input_keys = ('name', 'password')
        expected_output = [
            dict(name='user1', password='pwd1'),
            dict(name='user2', password='pwd2'),
            dict(name='user3', password='pwd3')
        ]

        output = todict(input_list, *input_keys)
        return self.assertEqual(output, expected_output)

    def test_number_of_keys_longer_than_list(self):
        input_list = [
            ['user1', 'pwd1'],
            ['user2', 'pwd2'],
            ['user3', 'pwd3']
        ]
        input_keys = ('name', 'password', 'uid')
        expected_output = [
            dict(name='user1', password='pwd1', uid=None),
            dict(name='user2', password='pwd2', uid=None),
            dict(name='user3', password='pwd3', uid=None)
        ]

        output = todict(input_list, *input_keys)
        return self.assertEqual(output, expected_output)

    def test_empty_list(self):
        input_list = [
            ['user1'],
            []
        ]
        input_keys = ('name',)
        expected_output = [
            dict(name='user1'),
            dict(name=None)
        ]

        output = todict(input_list, *input_keys)
        return self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()
