import unittest
import io
from unittest.mock import patch, Mock
import requests
from currencies import get_currencies, file_log, solve_quadratic, logger


class TestGetCurrencies(unittest.TestCase):

    def setUp(self):
        self.valid_data = {
            "Valute": {
                "USD": {"Value": 74.0},
                "EUR": {"Value": 90.0}
            }
        }

    @patch('requests.get')
    def test_correct_return(self, mock_get):
        """Проверка корректного возврата реальных курсов"""
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = self.valid_data
        mock_get.return_value = mock_response

        result = get_currencies(['USD', 'EUR'])
        self.assertEqual(result, {'USD': 74.0, 'EUR': 90.0})

    @patch('requests.get')
    def test_nonexistent_currency(self, mock_get):
        """Проверка поведения при несуществующей валюте"""
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = self.valid_data
        mock_get.return_value = mock_response

        with self.assertRaises(KeyError):
            get_currencies(['GBP'])  # GBP нет в данных

    @patch('requests.get', side_effect=requests.exceptions.ConnectionError)
    def test_connection_error(self, mock_get):
        """Проверка выброса ConnectionError"""
        with self.assertRaises(requests.exceptions.ConnectionError):
            get_currencies(['USD'])

    @patch('requests.get')
    def test_invalid_json(self, mock_get):
        """Проверка выброса ValueError при некорректном JSON"""
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.side_effect = ValueError("Некорректный JSON")
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            get_currencies(['USD'])

    @patch('requests.get')
    def test_missing_valute_key(self, mock_get):
        """Проверка выброса KeyError при отсутствии ключа 'Valute'"""
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {}  # нет ключа 'Valute'
        mock_get.return_value = mock_response

        with self.assertRaises(KeyError):
            get_currencies(['USD'])


class TestFileLogger(unittest.TestCase):

    def setUp(self):
        self.logger = file_log
        with open("app.log", "w", encoding="utf-8") as f:
            f.write("")  # Очищаем файл перед каждым тестом

    def get_log_content(self):
        with open("app.log", "r", encoding="utf-8") as f:
            return f.read()

    def test_get_currencies_success(self):
        result = get_currencies(['USD', 'EUR'], handle=self.logger)  # Тест корректного выполнения
        log = self.get_log_content()

        self.assertIn("INFO", log)
        self.assertIn("get_currencies", log)
        self.assertIn("Результат", log)
        self.assertIsInstance(result, dict)
        self.assertIn("USD", result)

    def test_get_currencies_nonexistent_currency(self):
        with self.assertRaises(KeyError):
            get_currencies(['nonexistant'], handle=self.logger)  # Проверка поведения при несуществующей валюте

        log = self.get_log_content()
        self.assertIn("ERROR", log)
        self.assertIn("nonexistant", log)

    def test_solve_quadratic_success(self):
        # Проверка успешного решения квадратного уравнения
        result = solve_quadratic(1, -3, 2, handle=self.logger)  # x^2 - 3x + 2 = 0 -> [1, 2]
        log = self.get_log_content()

        self.assertIn("INFO", log)
        self.assertIn("solve_quadratic", log)
        self.assertEqual(result, [1.0, 2.0])

    def test_solve_quadratic_a_zero(self):
        # Проверка случая a = 0
        result = solve_quadratic(0, 2, -8, handle=self.logger)
        log = self.get_log_content()

        self.assertIn("CRITICAL", log)
        self.assertIsNone(result)


class TestLoggerWithStream(unittest.TestCase):

    def setUp(self):
        # Поток для логов
        self.stream = io.StringIO()

        # Пример обёрнутой функции с декоратором
        @logger(handle=self.stream)
        def wrapped_success(x, y):
            return x + y
        self.wrapped_success = wrapped_success

        @logger(handle=self.stream)
        def wrapped_error():
            # Функция, которая вызовет ValueError
            raise ValueError("Тестовая ошибка")
        self.wrapped_error = wrapped_error

        @logger(handle=self.stream)
        def wrapped_get_currencies():
            # Пробуем вызвать get_currencies с некорректным URL, чтобы вызвать ConnectionError
            return get_currencies(['USD'], url="https://invalid-url-for-test")
        self.wrapped_get_currencies = wrapped_get_currencies

    def test_logging_success(self):
        # Тестируем успешный вызов функции
        result = self.wrapped_success(2, 3)
        logs = self.stream.getvalue()

        self.assertEqual(result, 5)
        self.assertIn("INFO", logs)  # должен быть лог уровня INFO
        self.assertIn("wrapped_success", logs)  # имя функции
        # Обычно декоратор может писать аргументы и результат
        self.assertIn("args=(2, 3)", logs)

    def test_logging_error(self):
        # Тестируем логирование ошибок и проброс исключения
        with self.assertRaises(ValueError):
            self.wrapped_error()

        logs = self.stream.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("ValueError", logs)
        self.assertIn("Тестовая ошибка", logs)

    def test_get_currencies_connection_error(self):
        # Тестируем ConnectionError при вызове get_currencies с некорректным URL
        with self.assertRaises(Exception):  # requests выбросит ConnectionError
            self.wrapped_get_currencies()

        logs = self.stream.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("ConnectionError", logs)  # проверяем, что лог содержит ошибку сети


if __name__ == '__main__':
    unittest.main()
