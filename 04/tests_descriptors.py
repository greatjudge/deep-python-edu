import unittest
from descriptors import Integer, String, PositiveInteger, Password


class Data:
    num = Integer()
    name = String()
    price = PositiveInteger()
    password = Password()

    def __init__(self, num=10, name='name', price=10):
        self.num = num
        self.name = name
        self.price = price


class IntegerDescTest(unittest.TestCase):
    def setUp(self) -> None:
        self.data = Data()

    def test_normal(self):
        self.data.num = 100
        self.assertEqual(self.data.num, 100)
        self.assertEqual(self.data._num, 100)

    def test_exception(self):
        self.data.num = 10
        with self.subTest():
            for value in (550.34, 'not int', '50', list):
                with self.assertRaises(TypeError) as ex:
                    self.data.num = value
                self.assertEqual(str(ex.exception),
                                 f'num must be integer not {type(value)}')
                self.assertEqual(self.data.num, 10)


class PosIntDescTest(unittest.TestCase):
    def setUp(self) -> None:
        self.data = Data()

    def test_normal(self):
        self.data.price = 100
        self.assertEqual(self.data.price, 100)
        self.assertEqual(self.data._price, 100)

    def test_value_error(self):
        self.data.price = 99
        with self.subTest():
            with self.assertRaises(ValueError) as ex:
                self.data.price = -50
            self.assertEqual(str(ex.exception),
                             f'price must be >= 0, you set -50')
            self.assertEqual(self.data.price, 99)

    def test_type_error(self):
        self.data.price = 10
        with self.subTest():
            for value in (550.34, 'not int', '50', list, 0.0):
                with self.assertRaises(TypeError) as ex:
                    self.data.price = value
                self.assertEqual(str(ex.exception),
                                 f'price must be integer not {type(value)}')
                self.assertEqual(self.data.price, 10)


class StringDescTest(unittest.TestCase):
    def setUp(self) -> None:
        self.data = Data()

    def test_normal(self):
        self.data.name = 'value'
        self.assertEqual(self.data.name, 'value')
        self.assertEqual(self.data._name, 'value')

    def test_error(self):
        self.data.name = 'string'
        with self.subTest():
            for value in (550.34, tuple(), 50, list, 0.0):
                with self.assertRaises(TypeError) as ex:
                    self.data.name = value
                self.assertEqual(str(ex.exception),
                                 f'name must be str not {type(value)}')
                self.assertEqual(self.data.name, 'string')


class PasswordDescTest(unittest.TestCase):
    def setUp(self) -> None:
        self.data = Data()

    def test_normal(self):
        self.data.password = 'password'
        self.assertEqual(self.data.password, 'password')
        self.assertEqual(self.data._password, 'password')

    def test_error(self):
        self.data.password = 'password'
        with self.subTest():
            with self.assertRaises(ValueError) as ex:
                self.data.password = 'less6'
            self.assertEqual(str(ex.exception),
                             f'Password is too small.'
                             f' It must be 6 at least'
                             )
            self.assertEqual(self.data.password, 'password')

            with self.assertRaises(ValueError) as ex:
                self.data.password = '1234567890'
            self.assertEqual(str(ex.exception),
                             f'Password can`be be entirely numeric')
            self.assertEqual(self.data.password, 'password')