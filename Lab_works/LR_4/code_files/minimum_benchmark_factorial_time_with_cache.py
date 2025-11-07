import timeit
import matplotlib.pyplot as plt
import random
from functools import lru_cache


@lru_cache
def fact_recursive(n: int) -> int:
    """Рекурсивный факториал"""
    if n == 0:
        return 1
    return n * fact_recursive(n - 1)


@lru_cache
def fact_iterative(n: int) -> int:
    """Нерекурсивный факториал"""
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res


def benchmark(func, n: int, number=100, repeat=5) -> int:
    """Возвращает минимальное время выполнения func для числа n"""
    # производим несколько повторов и возвращаем минимальное время
    times = timeit.repeat(lambda: func(n), number=number, repeat=repeat)
    return min(times)


def main():
    """
    Основная функция программы, в которой формируется набор данных, происходит вызов бэнчмарка по инимальному времени
    работы двух алгоритмов и выводится визуализация.
    """

    # составляем фиксированный набор данных
    random.seed(42)
    test_data = list(range(10, 300, 10))

    # заводим массивы для сбора данных о времени работы двух функций
    res_recursive = []
    res_iterative = []

    # вычисление среднего времени работы для двух алгоритьмах на каждом элемента набора данных
    for n in test_data:
        res_recursive.append(benchmark(fact_recursive, n))
        res_iterative.append(benchmark(fact_iterative, n))

    # Визуализация
    plt.plot(test_data, res_recursive, label="Рекурсивный")
    plt.plot(test_data, res_iterative, label="Итеративный")
    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение рекурс. и итерат. факториала по ср. времени выполнения")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
