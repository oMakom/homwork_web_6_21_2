# Импорт встроенной библиотеки для работы веб-сервера
import os
import urllib
from http.server import BaseHTTPRequestHandler, HTTPServer

# Для начала определим настройки запуска
hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8080  # Порт для доступа по сети


class MyServer(BaseHTTPRequestHandler):
    """Специальный класс, который отвечает за обработку входящих запросов от клиентов."""

    def do_GET(self):
        """Метод для обработки входящих GET-запросов."""
        file_path = os.path.join(os.path.dirname(__file__), "contacts.html")
        # проверка налисия файла
        if not os.path.isfile(file_path):
            # ФАЙЛА НЕТ → отдаём 404 и свою страницу ошибки
            self.send_response(404)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            error_html = """
                    <!DOCTYPE html>
                    <html lang="ru">
                    <head>
                        <meta charset="UTF-8">
                        <title>Ошибка 404</title>
                        <style>
                            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                            h1 { color: #d9534f; }
                        </style>
                    </head>
                    <body>
                        <h1>404 — Файл contacts.html не найден!</h1>
                        <p>Сервер не смог найти запрашиваемый файл.</p>
                        <a href="/">Вернуться на главную</a>
                    </body>
                    </html>
                    """
            self.wfile.write(error_html.encode('utf-8'))
            return  # Важно: выходим из метода, дальше ничего не делаем
        #Читаем файле если есть
        with open(file_path, "rb") as file:
            content = file.read()

        self.send_response(200)  # Отправка кода ответа
        self.send_header(
            "Content-type", "text/html; charset=utf-8"
        )  # Отправка типа данных, который будет передаваться
        self.end_headers()  # Завершение формирования заголовков ответа
        self.wfile.write(content)  # Тело ответа

    def do_POST(self):
        """Метод для обработки входящих POST-запросов"""
        # Получаем размер тела запроса
        content_length = int(self.headers.get("Content-Length", 0))
        # Читаем тело запроса
        body = self.rfile.read(content_length)
        # Декодируем байты в строку (для корректного вывода кириллицы)
        body_read = urllib.parse.unquote(body.decode("utf-8"))
        # Печатаем в консоль все данные, полученные от пользователя
        print(f"Получен POST-запрос. Данные: {body_read}")
        # Парсим форму, чтобы удобно вытащить отдельные поля
        data = urllib.parse.parse_qs(body_read)
        # (parse_qs возвращает списки)
        name = data.get("name", [""])
        email = data.get("email", [""])
        message = data.get("message", [""])
        print(f"Имя: {name}")
        print(f"Email: {email}")
        print(f"Сообщение: {message}")
        # Отправляем ответ клиенту
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        # Возвращаем пользователя на форму заполнения
        file_path = os.path.join(os.path.dirname(__file__), "contacts.html")
        with open(file_path, "rb") as file:
            content = file.read()
        self.wfile.write(content)


if __name__ == "__main__":
    # Инициализация веб-сервера, который будет по заданным параметрах в сети
    # принимать запросы и отправлять их на обработку специальному классу, который был описан выше
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Cтарт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")
