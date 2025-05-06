from Src.exceptions import argument_exception, exception_proxy
from Src.Logics.convert_factory import convert_factory
from Src.settings import settings
from Src.settings_manager import settings_manager
from Src.Models.event_type import event_type
from abc import ABC, abstractmethod
import json

#
# Базовый абстрактный сервис
# Используется для реализации логики, связанной с обработкой данных и событий
#
class service(ABC):
    # Набор данных для обработки
    __data = []
    # Текущие настройки приложения
    __settings: settings = None

    def __init__(self, data: list) -> None:
        """
        Инициализация сервиса

        Args:
            data (list): Входные данные для обработки

        Raises:
            argument_exception: Если список данных пуст
        """
        if len(data) == 0:
            raise argument_exception("Некорректно переданы параметры!")

        self.__data = data
        options = settings_manager()
        self.__settings = options.settings

    @property
    def data(self):
        """
        Получить текущие данные

        Returns:
            list: Данные, с которыми работает сервис
        """
        return self.__data

    @property
    def settings(self) -> settings:
        """
        Получить текущие настройки

        Returns:
            settings: Настройки, полученные через settings_manager
        """
        return self.__settings

    @abstractmethod
    def handle_event(self, event_type: str):
        """
        Обработать событие

        Args:
            event_type (str): Тип события для обработки

        Raises:
            exception_proxy: Если тип события некорректен
        """
        exception_proxy.validate(event_type, str)

    #
    # Общие методы для формирования ответа для Web-сервера
    #

    def create_response(self, app, data: list = None):
        """
        Сформировать HTTP-ответ для Web-сервера

        Args:
            app: Объект приложения (например, Flask)
            data (list, optional): Альтернативные данные для сериализации

        Returns:
            response: HTTP-ответ с JSON-содержимым
        """
        inner_data = self.__data if data is None else data
        return service.create_response(app, inner_data)

    @staticmethod
    def create_response(app, data: list):
        """
        Сформировать HTTP-ответ для Web-сервера (статический метод)

        Args:
            app: Объект приложения
            data (list): Список данных для сериализации

        Returns:
            response: HTTP-ответ с JSON-содержимым

        Raises:
            argument_exception: Если объект app не передан
        """
        if app is None:
            raise argument_exception("Некорректно переданы параметры!")

        exception_proxy.validate(data, list)

        # Преобразование данных в сериализованный формат
        dest_data = convert_factory().serialize(data)

        # Преобразование в JSON
        json_text = json.dumps(dest_data, sort_keys=True, indent=4, ensure_ascii=False)

        # Формирование HTTP-ответа
        result = app.response_class(
            response=f"{json_text}",
            status=200,
            mimetype="application/json; charset=utf-8"
        )

        return result
