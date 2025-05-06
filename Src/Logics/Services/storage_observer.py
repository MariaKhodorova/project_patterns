from Src.Models.event_type import event_type
from Src.exceptions import exception_proxy

#
# Наблюдатель для складских операций
# Отвечает за уведомление зарегистрированных обработчиков при возникновении событий
#
class storage_observer:
    _observers = []

    @staticmethod
    def raise_event(handle_event: str, reference: None):
        """
        Сформировать и распространить событие среди подписчиков

        Args:
            handle_event (str): Тип события
            reference (None): Зарезервировано для ссылки на объект события (пока не используется)
        """
        # Проверка корректности типа события
        exception_proxy.validate(handle_event, str)

        # Уведомление всех подписанных объектов
        for object in storage_observer._observers:
            if object is not None:
                object.handle_event(handle_event)
