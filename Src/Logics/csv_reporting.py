from Src.Logics.reporting import reporting
from Src.exceptions import operation_exception

#
# Класс — реализация построения отчетных данных в формате CSV
#
class csv_reporting(reporting):

    def create(self, storage_key: str):
        """
        Сформировать CSV-отчет по ключу хранилища

        Args:
            storage_key (str): Ключ доступа к данным из хранилища

        Returns:
            str: Сформированные данные в формате CSV

        Raises:
            operation_exception: Если данные отсутствуют или не заполнены
        """
        super().create(storage_key)
        result = ""
        delimetr = ";"

        # Извлечение данных по ключу
        items = self.data.get(storage_key)
        if items is None:
            raise operation_exception("Невозможно сформировать данные. Данные не заполнены!")

        if len(items) == 0:
            raise operation_exception("Невозможно сформировать данные. Нет данных!")

        # Формирование заголовка CSV
        header = delimetr.join(self.fields)
        result += f"{header}\n"

        # Формирование строк данных
        for item in items:
            row = ""
            for field in self.fields:
                attribute = getattr(item.__class__, field)
                if isinstance(attribute, property):
                    value = getattr(item, field)
                    # Пропуск списков, словарей и None
                    if isinstance(value, (list, dict)) or value is None:
                        value = ""
                    row += f"{value}{delimetr}"
            result += f"{row[:-1]}\n"  # Удаляем последний разделитель

        # Возврат результата
        return result
