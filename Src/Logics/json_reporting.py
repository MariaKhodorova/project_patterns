from Src.Logics.reporting import reporting
from Src.exceptions import operation_exception
from Src.Logics.convert_factory import convert_factory
import json

#
# Класс — реализация построения отчетных данных в формате JSON
#
class json_reporting(reporting):

    def create(self, storage_key: str):
        """
        Сформировать JSON-отчет по ключу хранилища

        Args:
            storage_key (str): Ключ доступа к данным из хранилища

        Returns:
            str: Сформированные данные в формате JSON

        Raises:
            operation_exception: Если данные отсутствуют или не заполнены
        """
        super().create(storage_key)

        # Извлечение исходных данных
        items = self.data.get(storage_key)
        if items is None:
            raise operation_exception("Невозможно сформировать данные. Данные не заполнены!")

        if len(items) == 0:
            raise operation_exception("Невозможно сформировать данные. Нет данных!")

        # Сериализация данных
        factory = convert_factory()
        data = factory.serialize(items)

        # Формирование JSON-строки
        result = json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False)
        return result

    def mimetype(self) -> str:
        """
        Получить MIME-тип результата

        Returns:
            str: MIME-тип JSON-ответа
        """
        return "application/json; charset=utf-8"
