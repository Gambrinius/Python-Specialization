import unittest


def factorize(x):
    """ Factorize positive integer and return its factors.
        :type x: int,>=0
        :rtype: tuple[N],N>0
    """
    pass


class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exception(self):
        cases = ['string', 1.5]
        for x in cases:
            with self.subTest(x=x):
                self.assertRaises(TypeError, factorize, x)

    def test_negative(self):
        cases = [-1, -10, -100]
        for x in cases:
            with self.subTest(x=x):
                self.assertRaises(ValueError, factorize, x)

    def test_zero_and_one_cases(self):
        cases = [0, 1]
        for case in cases:
            with self.subTest(x=case):
                self.assertTupleEqual(factorize(case), (case,))

    def test_simple_numbers(self):
        cases = [3, 13, 29]
        for case in cases:
            with self.subTest(x=case):
                self.assertTupleEqual(factorize(case), (case,))

    def test_two_simple_multipliers(self):
        cases = [6, 26, 121]
        results = [(2, 3), (2, 13), (11, 11)]
        for i, case in enumerate(cases):
            with self.subTest(x=case):
                self.assertTupleEqual(factorize(case), results[i])

    def test_many_multipliers(self):
        cases = [1001, 9699690]
        results = [(7, 11, 13), (2, 3, 5, 7, 11, 13, 17, 19)]
        for i, case in enumerate(cases):
            with self.subTest(x=case):
                self.assertTupleEqual(factorize(case), results[i])


if __name__ == '__main__':
    unittest.main()
