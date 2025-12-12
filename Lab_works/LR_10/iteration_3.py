import math
import concurrent.futures as futures
from functools import partial
from iteration_1 import integrate_1


def integrate_parallel(f: callable, a: float, b: float, *, n_jobs: int = 6, n_iter: int = 1000):
    """
        Считает интеграл переданной функции методом левых прямоугольников, разбивая всю работу на несколько процессов.

        Parametrs:
            f (callable): Функция, интеграл которой мы считаем.
            a (float): Левая граница.
            b (float): Правая граница.
            n_jobs (float): Количество потоков.
            n_iter (int): Количество прямоугольников.

        Returns:
            float: возвращает значение интеграла (приблизительная площадь под графиком)

        Raises:
            TypeError: если f не вызываемое, 'a', 'b' не числовые, 'n_iter' не целое.
            ZeroDivisionError: если 'n_iter' равна 0.

        Example:
            >>> round(integrate_1(math.cos, 0, math.pi / 2, n_iter=100), 5)
            1.00783
    """
    executor = futures.ProcessPoolExecutor(max_workers=n_jobs)
    spawn = partial(executor.submit, integrate_1, f, n_iter=n_iter // n_jobs)
    step = (b - a) / n_jobs
    fs = [spawn(a + i * step, a + (i + 1) * step) for i in range(n_jobs)]

    return sum(list(f.result() for f in futures.as_completed(fs)))


#print(round(integrate_parallel(math.sin, 0, math.pi), 5))
