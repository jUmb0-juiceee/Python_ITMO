import math


def integrate_1(f: callable, a: float, b: float, *, n_iter: int = 1000) -> float:
    """
    Считает интеграл переданной функции методом левых прямоугольников.

    Parametrs:
        f (callable): Функция, интеграл которой мы считаем.
        a (float): Левая граница.
        b (float): Правая граница.
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
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i*step) * step
    return acc

#print(integrate(lambda x: x ** 2 + 3 * x + 15, 0, 3, n_iter=100))
