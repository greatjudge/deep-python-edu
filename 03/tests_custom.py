import unittest
from custom_list import CustomList

class SubtractionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.results = {((5, 1, 3, 7), (1, 2, 7)): [4, -1, -4, 7],
                        ((1, 2, 7), (5, 1, 3, 7)): [-4, 1, 4, -7],
                        ((5, 1, 3, 7), (1, 2, 7, 3)): [4, -1, -4, 4],
                        ((1, ), (1, 2, 7, 3)): [0, -2, -7, -3],
                        ((5, 1, 3, 7), (1, )): [4, 1, 3, 7],
                        ((5, 1, 3, 7), tuple()): [5, 1, 3, 7],
                        (tuple(), (1, 2, 7, 3)): [-1, -2, -7, -3],
                        (tuple(), tuple()): []}

        self.false_results = {((5, 1, 3, 7), (1, 2, 7)): [4, -1, 0, 7],
                        ((1, 2, 7), (5, 1, 3, 7)): [-4, 3, 4, -7],
                        ((5, 1, 3, 7), (1, 2, 7, 3)): [1, -1, -4, 4],
                        ((1,), (1, 2, 7, 3)): [0, 2, 7, -3],
                        ((5, 1, 3, 7), (1,)): [5, 0, 3, 7],
                        ((5, 1, 3, 7), tuple()): [-5, 1, -3, 7],
                        (tuple(), (1, 2, 7, 3)): [-1, 2, -7, 3]}

    def test_correct_subtraction(self):
        with self.subTest():
            for (left_tup, right_tup), result in self.results.items():
                left, right = CustomList(left_tup), CustomList(right_tup)
                self.assertEqual(list(left - right), list(result))
                self.assertEqual(list(left - list(right)), list(result))
                self.assertEqual(list(list(left) - right), list(result))

                self.assertEqual(list(left), list(left_tup))
                self.assertEqual(list(right), list(right_tup))

    def test_incorrect_subtraction(self):
        with self.subTest():
            for (left_tup, right_tup), result in self.false_results.items():
                left, right = CustomList(left_tup), CustomList(right_tup)
                self.assertNotEqual(list(left - right), list(result))
                self.assertNotEqual(list(left - list(right)), list(result))
                self.assertNotEqual(list(list(left) - right), list(result))

                self.assertEqual(list(left), list(left_tup))
                self.assertEqual(list(right), list(right_tup))

    def test_result_is_customlist(self):
        with self.subTest():
            for (left_tup, right_tup), result in self.results.items():
                left, right = CustomList(left_tup), CustomList(right_tup)
                self.assertIsInstance(left - right, CustomList)
                self.assertIsInstance(left - list(right), CustomList)
                self.assertIsInstance(list(left) - right, CustomList)

                self.assertEqual(list(left), list(left_tup))
                self.assertEqual(list(right), list(right_tup))

    def test_not_change(self):
        with self.subTest():
            for (old_left, old_right), result in self.results.items():
                left, right = list(old_left), list(old_right)
                CustomList(left) - CustomList(right)
                self.assertEqual(list(left), list(old_left))
                self.assertEqual(list(right), list(old_right))


class AdditionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.results = {((5, 1, 3, 7), (1, 2, 7)): [6, 3, 10, 7],
                        ((1, 2, 7), (5, 1, 3, 7)): [6, 3, 10, 7],
                        ((5, 1, 3, 7), (1, 2, 7, 3)): [6, 3, 10, 10],
                        ((1, ), (1, 2, 7, 3)): [2, 2, 7, 3],
                        ((5, 1, 3, 7), (1, )): [6, 1, 3, 7],
                        ((5, 1, 3, 7), tuple()): [5, 1, 3, 7],
                        (tuple(), (1, 2, 7, 3)): [1, 2, 7, 3],
                        (tuple(), tuple()): []}

        self.false_results = {((5, 1, 3, 7), (1, 2, 7)): [-6, -3, 10, 7],
                        ((1, 2, 7), (5, 1, 3, 7)): [6, 3, 10, 0],
                        ((5, 1, 3, 7), (1, 2, 7, 3)): [6, 3, 3, 10],
                        ((1,), (1, 2, 7, 3)): [2, -2, -7, 3],
                        ((5, 1, 3, 7), (1,)): [0, -1, 3, 7],
                        ((5, 1, 3, 7), tuple()): [1, 1, 3, 7],
                        (tuple(), (1, 2, 7, 3)): [1, 3, 7, 3]}

    def test_correct_addition(self):
        with self.subTest():
            for (left_tup, right_tup), result in self.results.items():
                left, right = CustomList(left_tup), CustomList(right_tup)
                self.assertEqual(list(left + right), list(result))
                self.assertEqual(list(left + list(right)), list(result))
                self.assertEqual(list(list(left) + right), list(result))

                self.assertEqual(list(left), list(left_tup))
                self.assertEqual(list(right), list(right_tup))

    def test_incorrect_addition(self):
        with self.subTest():
            for (left_tup, right_tup), result in self.false_results.items():
                left, right = CustomList(left_tup), CustomList(right_tup)
                self.assertNotEqual(list(left + right), list(result))
                self.assertNotEqual(list(left + list(right)), list(result))
                self.assertNotEqual(list(list(left) + right), list(result))

                self.assertEqual(list(left), list(left_tup))
                self.assertEqual(list(right), list(right_tup))

    def test_result_is_customlist(self):
        with self.subTest():
            for (left_tup, right_tup), result in self.results.items():
                left, right = CustomList(left_tup), CustomList(right_tup)
                self.assertIsInstance(left + right, CustomList)
                self.assertIsInstance(left + list(right), CustomList)
                self.assertIsInstance(list(left) + right, CustomList)

                self.assertEqual(list(left), list(left_tup))
                self.assertEqual(list(right), list(right_tup))

    def test_not_change(self):
        with self.subTest():
            for (old_left, old_right), result in self.results.items():
                left, right = list(old_left), list(old_right)
                CustomList(left) + CustomList(right)
                self.assertEqual(list(left), list(old_left))
                self.assertEqual(list(right), list(old_right))


class EqualTest(unittest.TestCase):
    def setUp(self):
        self.equal = {(1, 2, 3, 4): (1, 2, 3, 4),
                      (1, 2, 3, 4): (5, 5),
                      (5, 5): (1, 2, 3, 4),
                      (-1, -2, -3, -4): (-5, -5),
                      (-5, -5): (-1, -2, -3, -4),
                      (0, 0, 0, 0): (),
                      (): (0, 0, 0, 0)}
        self.not_equal = {(1, 2, 3, 4): (1, 2, 3),
                          (-1, -2, -3, -4): (-5, -5, 5),
                          (): (1, 1),
                          (1, 1): ()}

    def test_equal(self):
        for list1, list2 in self.equal.items():
            left, right = CustomList(list1), CustomList(list2)
            self.assertEqual(left, right)

            self.assertEqual(list(left), list(list1))
            self.assertEqual(list(right), list(list2))

    def test_not_equal(self):
        for list1, list2 in self.not_equal.items():
            left, right = CustomList(list1), CustomList(list2)
            self.assertNotEqual(left, right)

            self.assertEqual(list(left), list(list1))
            self.assertEqual(list(right), list(list2))


class LessGreaterTest(unittest.TestCase):
    def setUp(self):
        self.less = {(1, 2, 3): (1, 2, 3, 4),
                      (1, 2, 3, 4): (5, 5, 5),
                      (5, 5): (1, 1, 19),
                      (-1, -2, -3, -4): (-5, 5),
                      (0, 0, 0, 0): (5, ),
                      (): (0, 1, 0, 0)}
        self.greater = {(1, 2, 3, 4): (1, 2, 3),
                          (-1, -2, -3, -4): (-5, -5, -5),
                          (5, 5): (1, 1),
                          (1, 1): ()}

    def test_less(self):
        for tup1, tup2 in self.less.items():
            list1, list2 = CustomList(tup1), CustomList(tup2)
            self.assertLess(list1, list2)

            self.assertEqual(list(list1), list(tup1))
            self.assertEqual(list(list2), list(tup2))

    def test_great(self):
        for tup1, tup2 in self.greater.items():
            list1, list2 = CustomList(tup1), CustomList(tup2)
            self.assertGreater(list1, list2)

            self.assertEqual(list(list1), list(tup1))
            self.assertEqual(list(list2), list(tup2))


class TestStr(unittest.TestCase):
    def test_str(self):
        lst = CustomList([1, 2, 3, -1])
        self.assertEqual(f'{[1, 2, 3, -1]}, {5}', str(lst))


if __name__ == '__main__':
    unittest.main()
