import unittest
from zip import zipped

class ZipTest(unittest.TestCase):
    def test_two_lists_of_dicts(self):
        list1 = [
            dict(a=1, b=2),
            dict(c=3, d=4)
        ]
        list2 = [
            dict(e=5),
            dict(f=6)
        ]
        expected_list = [
            dict(a=1, b=2, e=5),
            dict(c=3, d=4, f=6)
        ]

        z = zipped(list1, list2)
        return self.assertEqual(z, expected_list)

    def test_two_lists_of_dicts_first_longer(self):
        list1 = [
            dict(a=1, b=2),
            dict(c=3, d=4)
        ]
        list2 = [
            dict(e=5)
        ]
        expected_list = [
            dict(a=1, b=2, e=5),
            dict(c=3, d=4)
        ]

        z = zipped(list1, list2)
        return self.assertEqual(z, expected_list)

    def test_two_lists_of_dicts_second_longer(self):
        list1 = [
            dict(a=1, b=2)
        ]
        list2 = [
            dict(e=5),
            dict(f=6)
        ]
        expected_list = [
            dict(a=1, b=2, e=5),
        ]

        z = zipped(list1, list2)
        return self.assertEqual(z, expected_list)

    def test_two_lists_of_dicts_first_longer_with_longest_true(self):
        list1 = [
            dict(a=1, b=2),
            dict(c=3, d=4)
        ]
        list2 = [
            dict(e=5)
        ]
        expected_list = [
            dict(a=1, b=2, e=5),
            dict(c=3, d=4)
        ]

        z = zipped(list1, list2, longest=True)
        return self.assertEqual(z, expected_list)

    def test_two_lists_of_dicts_second_longer_with_longest_true(self):
        list1 = [
            dict(a=1, b=2)
        ]
        list2 = [
            dict(e=5),
            dict(f=6)
        ]
        expected_list = [
            dict(a=1, b=2, e=5),
            dict(f=6)
        ]

        z = zipped(list1, list2, longest=True)
        return self.assertEqual(z, expected_list)

    def test_first_list_is_dict(self):
        list1 = [
            dict(a=1, b=2),
            dict(c=3, d=4)
        ]
        list2 = ['e', 'f']
        expected_list = [
            dict(a=1, b=2),
            dict(c=3, d=4)
        ]

        z = zipped(list1, list2)
        return self.assertEqual(z, expected_list)

    def test_second_list_is_dict(self):
        list1 = ['a', 'b']
        list2 = [
            dict(e=5),
            dict(f=6)
        ]
        expected_list = [
            ('a', dict(e=5)),
            ('b', dict(f=6))
        ]

        z = zipped(list1, list2)
        return self.assertEqual(z, expected_list)

    def test_two_lists_equal_size(self):
        list1 = ['a', 'b']
        list2 = ['c', 'd']
        expected_list = [
            ('a', 'c'),
            ('b', 'd')
        ]

        z = zipped(list1, list2)
        return self.assertEqual(z, expected_list)

    def test_two_lists_first_longer(self):
        list1 = ['a', 'b', 'c']
        list2 = ['d', 'e']
        expected_list = [
            ('a', 'd'),
            ('b', 'e')
        ]

        z = zipped(list1, list2)
        return self.assertEqual(z, expected_list)

    def test_two_lists_second_longer(self):
        list1 = ['a', 'b']
        list2 = ['c', 'd', 'e']
        expected_list = [
            ('a', 'c'),
            ('b', 'd')
        ]

        z = zipped(list1, list2)
        return self.assertEqual(z, expected_list)

    def test_two_lists_first_longer_with_longest_true(self):
        list1 = ['a', 'b', 'c']
        list2 = ['d', 'e']
        expected_list = [
            ('a', 'd'),
            ('b', 'e'),
            ('c', None)
        ]

        z = zipped(list1, list2, longest=True)
        return self.assertEqual(z, expected_list)

    def test_two_lists_second_longer_with_longest_true(self):
        list1 = ['a', 'b']
        list2 = ['c', 'd', 'e']
        expected_list = [
            ('a', 'c'),
            ('b', 'd'),
            (None, 'e')
        ]

        z = zipped(list1, list2, longest=True)
        return self.assertEqual(z, expected_list)

    def test_two_lists_first_longer_with_longest_true_and_fillvalue(self):
        list1 = ['a', 'b', 'c']
        list2 = ['d', 'e']
        expected_list = [
            ('a', 'd'),
            ('b', 'e'),
            ('c', 'Nothing')
        ]

        z = zipped(list1, list2, longest=True, fillvalue='Nothing')
        return self.assertEqual(z, expected_list)

    def test_two_lists_second_longer_with_longest_true_and_fillvalue(self):
        list1 = ['a', 'b']
        list2 = ['c', 'd', 'e']
        expected_list = [
            ('a', 'c'),
            ('b', 'd'),
            ('Nothing', 'e')
        ]

        z = zipped(list1, list2, longest=True, fillvalue='Nothing')
        return self.assertEqual(z, expected_list)

    def test_two_equal_list_with_longest_true(self):
        list1 = ['a', 'b']
        list2 = ['c', 'd']
        expected_list = [
            ('a', 'c'),
            ('b', 'd')
        ]

        z = zipped(list1, list2, longest=True)
        return self.assertEqual(z, expected_list)

if __name__ == '__main__':
    unittest.main()
