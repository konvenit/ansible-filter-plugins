import unittest
from defined import defined
from ansible import errors

class DefinedTest(unittest.TestCase):
    def test_none_variable_without_name(self):
        variable = None
        with self.assertRaises(errors.AnsibleFilterError) as ctx:
            defined(variable)

        self.assertEqual(str(ctx.exception), "Variable not defined")

    def test_none_variable_with_name(self):
        variable = None
        with self.assertRaises(errors.AnsibleFilterError) as ctx:
            defined(variable, 'var')

        self.assertEqual(str(ctx.exception), "Variable not defined: var")

    def test_empty_variable_without_name(self):
        variable= ''
        with self.assertRaises(errors.AnsibleFilterError) as ctx:
            defined(variable)

        self.assertEqual(str(ctx.exception), "Variable not defined")

    def test_empty_variable_with_name(self):
        variable= ''
        with self.assertRaises(errors.AnsibleFilterError) as ctx:
            defined(variable, 'var')

        self.assertEqual(str(ctx.exception), "Variable not defined: var")

    def test_false_variable_without_name(self):
        variable = False
        output = defined(variable)
        self.assertEqual(output, variable)

    def test_false_variable_with_name(self):
        variable = False
        output = defined(variable, 'var')
        self.assertEqual(output, variable)

    def test_zero_variable_without_name(self):
        variable = 0
        output = defined(variable)
        self.assertEqual(output, variable)

    def test_zero_variable_with_name(self):
        variable = 0
        output = defined(variable, 'var')
        self.assertEqual(output, variable)

    def test_defined_variable_without_name(self):
        variable = 'Hello'
        output = defined(variable)
        self.assertEqual(output, variable)

    def test_defined_variable_with_name(self):
        variable = 'Hello'
        output = defined(variable, 'var')
        self.assertEqual(output, variable)

if __name__ == '__main__':
    unittest.main()
