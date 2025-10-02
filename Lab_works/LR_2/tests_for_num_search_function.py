from LR_2 import num_search
import unittest

class TestMySolution(unittest.TestCase):
    """
        Класс тестирования функции бинарного поиска.

        Содержит тестовые случаи для проверки различных сценариев работы
        функции num_search, включая нормальные, граничные и ошибочные случаи.
    """
    def test_sample1(self) -> None:
        """
            Тест поиска числа 32 в диапазоне [0, 100] (нормальный случай).
        """
        self.assertEqual(num_search(32, 0, 100), [32, 7])

    def test_sample2(self) -> None:
        """
            Тест поиска числа 111 в диапазоне [0, 100] (ошибочный случай).
        """
        self.assertEqual(num_search(111, 0, 100), 'Данного числа нет в этом диапазоне, попробуйте задать данные ещё раз')

    def test_sample3(self) -> None:
        """
            Тест поиска числа 0 в диапазоне [0, 100] (граничный случай).
        """
        self.assertEqual(num_search(0, 0, 100), [0, 6])

    def test_sample4(self) -> None:
        """
            Тест поиска числа 100 в диапазоне [0, 100] (граничный случай).
        """
        self.assertEqual(num_search(100, 0, 100), [100, 7])

    def test_sample5(self) -> None:
        """
            Тест поиска числа 55 в диапазоне [7, 85] (нормальный случай).
        """
        self.assertEqual(num_search(55, 7, 85), [55, 7])

    def test_sample6(self) -> None:
        """
            Тест поиска числа 88 в диапазоне [0, 1000] (нормальный случай).
        """
        self.assertEqual(num_search(88, 0, 1000), [88, 8])

    def test_sample7(self) -> None:
        """
            Тест поиска числа -443 в диапазоне [-1000, -4] (нормальный случай).
        """
        self.assertEqual(num_search(-443, -1000, -4), [-443, 10])

    def test_sample8(self) -> None:
        """
            Тест поиска числа 5 в диапазоне [0, 10] (нормальный случай).
        """
        self.assertEqual(num_search(5, 0, 10), [5, 1])

    def test_sample9(self) -> None:
        """
            Тест поиска числа 5 в диапазоне [0, 10] (нормальный случай).
        """
        self.assertEqual(num_search(1, 100, 10), 'Левая граница не может быть больше правой, попробуйте задать данные ещё раз')

if __name__ == '__main__':
    """
    Точка запуска тестов. 
    """
    unittest.main()
