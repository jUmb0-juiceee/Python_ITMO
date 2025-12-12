import timeit
import time
from iteration_1 import integrate_1
from iteration_2 import integrate_async
from iteration_3 import integrate_parallel


def poly_func(x):
    return x**2 + 3*x + 15


def benchmark():
    for i in range(2, 6):
        start = time.perf_counter()
        ans = round(integrate_1(poly_func, 0, 100, n_iter=10**i), 5)
        end = time.perf_counter()
        print(f'Первая итерация ({10**i} прямоугольников): затраченное время - {round(end - start, 6)}, ответ - {ans}')
    print('=' * 50)

    for i in range(2, 10, 2):
        start = time.perf_counter()
        ans = round(integrate_async(poly_func, 0, 100, n_iter=100000, n_jobs=i), 5)
        end = time.perf_counter()
        print(f'Вторая итерация ({100000} прямоугольников, {i} потоков): затраченное время - {round(end - start, 6)}, ответ - {ans}')
    print('=' * 50)

    for i in range(2, 10, 2):
        start = time.perf_counter()
        ans = round(integrate_parallel(poly_func, 0, 100, n_iter=100000, n_jobs=i), 5)
        end = time.perf_counter()
        print(f'Третья итерация ({100000} прямоугольников, {i} процессов): затраченное время - {round(end - start, 6)}, ответ - {ans}')
    print('=' * 50)

if __name__ == '__main__':
    benchmark()
