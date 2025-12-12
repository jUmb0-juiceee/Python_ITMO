import requests
import sys
import io
import functools
import json
import logging


def create_logger():
    """
        Создаёт логгер, записывающий всё в файл.

        Returns:
            Настроенный логгер.
    """
    logger_obj = logging.getLogger("file_logger")
    logger_obj.setLevel(logging.INFO)  # сможем писать и info, и error

    if logger_obj.handlers:  # если логгер уже имеет обработчики -  возвращаем уже настроенный логгер (на всякий случай)
        return logger_obj

    handler = logging.FileHandler("app.log", encoding="utf-8")  # задаём логгеру форму файла
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")  # создаём новый формат
    handler.setFormatter(formatter)  # присваиваем формат обработчику

    logger_obj.addHandler(handler)  # присваиваем обработчик логгеру
    return logger_obj


def reading_log(log):
    """
    Функция нужна для вызова полного вывода всего логгера перед тем, как поднять ошибку, из-за чего остановится вся
    программа.

    Args:
        log: логгер, внутри которого хранятся все записи.
    """
    with open("app.log", "r", encoding="utf-8") as f:  # выводим всё, что есть в логгере
        content = f.read()
        print(content)
        f.close()
        return None


file_log = create_logger()


def logger(func=None, *, handle=None):
    import functools

    if func is None:
        return lambda f: logger(f, handle=handle)

    @functools.wraps(func)
    def inner(*args, **kwargs):
        if handle is not None:
            try:
                if hasattr(handle, "info"):
                    handle.info(f"Старт {func.__name__}, args={args}")
                else:
                    handle.write(f"INFO: Старт {func.__name__}, args={args}\n")
                result = func(*args, **kwargs)
                if hasattr(handle, "info"):
                    handle.info(f"Завершение {func.__name__}, результат={result}")
                else:
                    handle.write(f"INFO: Завершение {func.__name__}, результат={result}\n")
                return result
            except Exception as e:
                if hasattr(handle, "error"):
                    handle.error(f"{type(e).__name__}: {e}")
                else:
                    handle.write(f"ERROR: {type(e).__name__}: {e}\n")
                raise
        else:
            return func(*args, **kwargs)
    return inner


@logger()
def get_currencies(currency_codes: list, url: str = 'https://www.cbr-xml-daily.ru/daily_json.js',
                   handle=file_log) -> dict:
    """
    Функция выполняет запрос к API Центробанка, чтобы вывести курсы запрошенных валют.
    Args:
        currency_codes: массив с кодами валют, курсы которых мы запрашиваем
        url: url-ссылка на страницу json с валютами и всей информацией о них
        handle: привязанный логгер

    Returns:
        currencies: словарь в котором коду каждой валюты соответсвует её эквивалент в рублях
    """
    handle.info(f'Начало работы функции get_currencies. Аргументы: currency_codes = {currency_codes}')
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        currencies = {}

        if "Valute" in data:
            for code in currency_codes:
                if code in data["Valute"]:
                    if not isinstance(data["Valute"][code]["Value"], (int, float)):
                        handle.error(f"Курс {code} не числовой")
                        reading_log(handle)
                        raise TypeError(f"Курс валюты '{code}' имеет неверный тип")
                    else:
                        currencies[code] = data["Valute"][code]["Value"]
                else:
                    handle.error(f"Валюты '{code}' нет в данных API")
                    reading_log(handle)
                    raise KeyError(f"Валюта '{code}' не найдена")

        else:
            handle.error("Ключ 'Valute' отсутствует в данных API")
            reading_log(handle)
            raise KeyError("Нет ключа 'Valute' в данных API")
        handle.info(f'Успешное завершение работы функции get_currencies. Результат: currencies = {currencies}')
        return currencies

    except ValueError as e:
        handle.error(f"Некорректный JSON: {e}")
        reading_log(handle)
        raise

    except requests.exceptions.ConnectionError as e:
        handle.error(f"Ошибка сети, API недоступен: {e}")
        reading_log(handle)
        raise

    except requests.exceptions.RequestException as e:
        handle.error(f"Ошибка при запросе API: {e}")
        reading_log(handle)
        raise

    except Exception as e:
        handle.error(f"Упали с исключением: {e}")
        reading_log(handle)
        raise


@logger()
def solve_quadratic(a: int, b: int, c: int, handle=file_log) -> list:
    """
    Функция для вычисления корней квадратного уравнения

    Args:
        a: коэффициент
        b: коэффициент
        c: коэффициент
        handle: привязанный логгер

    Returns:
        ans: массив с корнями квадратного уравнения
    """
    handle.info(f'Начало работы функции solve_quadratic. Аргументы: a = {a}, b = {b}, c = {c}')
    try:
        D = b**2 - 4 * a * c
        if a == 0:
            handle.critical(f'Невозможный случай. Уравнение не явлается квадратным')
            return None
        elif D < 0:
            handle.warning(f'Дискриминант меньше нуля')
            return None
        elif D == 0:
            ans = [-b / (2 * a)]
            handle.info(f'Успешное завершение работы функции solve_quadratic. Результат: ans = {ans}')
            return ans
        else:
            ans = [(-b - D**(1/2)) / (2 * a), (-b + D**(1/2)) / (2 * a)]
            handle.info(f'Успешное завершение работы функции solve_quadratic. Результат: ans = {ans}')
            return ans

    except ValueError as e:
        handle.error(f"Неверные данные: {e}")
        raise


if __name__ == '__main__':
    open("app.log", "w", encoding="utf-8").close()  # очищаем логгер, поскольку можем использовать его не в первый раз

    currency_list = ['USD', 'EUR', 'GBP', 'JPY']
    currency_data = get_currencies(currency_list, handle=file_log)
    print(currency_data)

    for test in [(1, 7, 12), (1, -1, -12), (0, 2, -15)]:
        ans = solve_quadratic(*test, handle=file_log)
        print(ans)

    with open("app.log", "r", encoding="utf-8") as f:  # выводим всё, что есть в логгере
        content = f.read()
        print(content)
        f.close()
