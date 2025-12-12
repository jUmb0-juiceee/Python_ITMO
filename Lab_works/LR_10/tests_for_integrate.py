import math
from iteration_1 import integrate_1
from iteration_2 import integrate_async
from iteration_3 import integrate_parallel
import unittest


class TestMySolution(unittest.TestCase):

    def tests_iteration_1(self):
        self.assertEqual(round(integrate_1(math.cos, 0, math.pi / 2, n_iter=100), 5), 1.00783)
        self.assertEqual(round(integrate_1(lambda x: x ** 2 + 3 * x + 15, 0, 3, n_iter=100), 5), 67.23045)

    def tests_iteration_2(self):
        self.assertEqual(round(integrate_async(math.cos, 0, math.pi / 2, n_iter=100), 5), 1.00783)
        self.assertEqual(round(integrate_async(lambda x: x ** 2 + 3 * x + 15, 0, 3, n_iter=100), 5), 67.23045)

    def tests_iteration_3(self):
        self.assertEqual(round(integrate_parallel(math.cos, 0, math.pi / 2, n_iter=100), 5), 1.00816)
        self.assertEqual(round(integrate_parallel(math.sin, 0, math.pi, n_iter=100), 5), 1.99982)
