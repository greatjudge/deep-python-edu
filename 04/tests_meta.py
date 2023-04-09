import unittest
from custom_meta import CustomMeta

class CustomClass(metaclass=CustomMeta):
    x = 50

    def __init__(self, val=99):
        self.val = val

    def line(self):
        return 100

    def __add__(self, other):
        return self.custom_val + other.custom_val


class TestMeta(unittest.TestCase):
    def setUp(self) -> None:
        self.inst =  CustomClass()

    def test_meta_static_attrs(self):
        inst_2 = CustomClass(23)
        self.assertEqual(50, self.inst.custom_x)
        self.assertEqual(50, CustomClass.custom_x)
        self.assertEqual(99, self.inst.custom_val)
        self.assertEqual(23, inst_2.custom_val)
        self.assertEqual(100, self.inst.custom_line())

    def test_meta_error(self):
        with self.subTest():
            with self.assertRaises(AttributeError):
                a = self.inst.x
            with self.assertRaises(AttributeError):
                a = self.inst.val
            with self.assertRaises(AttributeError):
                a = self.inst.line()

    def test_not_change_magic(self):
        inst = CustomClass(100)
        other = CustomClass(110)
        self.assertEqual(inst.__add__(other), 210)

    def test_dynamic_attrs(self):
        with self.subTest():
            self.inst.dynamic = "added later"
            with self.assertRaises(AttributeError):
                a = self.inst.dynamic
            self.assertEqual("added later", self.inst.custom_dynamic)

            self.inst.dynamic = "some value"
            self.assertEqual("some value", self.inst.custom_dynamic)

            self.inst.custom_dynamic = "another value"
            self.assertEqual("some value", self.inst.custom_dynamic)
            self.assertEqual("another value", self.inst.custom_custom_dynamic)


if __name__ == '__main__':
    unittest.main()