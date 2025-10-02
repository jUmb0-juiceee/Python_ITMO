from LR_1_1 import two_sum
import unittest


class TestMySolution(unittest.TestCase):

    def test_sample1(self):
        self.assertEqual(two_sum([3, 3], 6), [0, 1])

    def test_sample2(self):
        self.assertEqual(two_sum([2,7,11,15], 9), [0, 1])

    def test_sample3(self):
        self.assertEqual(two_sum([3,2,4], 6), [1, 2])

    def test_adding_negatives(self):
        self.assertEqual(two_sum([-1, -5], -6), [0, 1])

    def test_adding_zero(self):
        self.assertEqual(two_sum([6, 5, 0, 2], 5), [1, 2])

    def test_wrong_data_type1(self):
        self.assertEqual(two_sum([8, '1'], 9), 'ERROR (тип данных)')

    def test_wrong_data_type2(self):
        self.assertEqual(two_sum([3.5, 2.5], 6), 'ERROR (тип данных)')

    def test_single_element(self):
        self.assertEqual(two_sum([1], 1), None)

    def test_a_lot_of_elements(self):
        self.assertEqual(two_sum([1, 2, 3, 4, 67, 15, 7, 6, 7, 7], 14), [6, 8])

    def test_no_combination(self):
        self.assertEqual(two_sum([65, 65, 65, 65, 65], 1), None)


if __name__ == '__main__':
    unittest.main()
