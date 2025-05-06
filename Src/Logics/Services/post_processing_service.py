from Src.Logics.Services.service import service
from Src.Logics.Services.storage_observer import storage_observer
from Src.Storage.storage import storage
from Src.Logics.Services.storage_observer import event_type
from Src.Models.nomenclature_model import nomenclature_model

#
# Сервис постобработки данных рецептов
# Обрабатывает события, связанные с удалением номенклатуры
#
class post_processing_service(service):

    def __init__(self, data: list, nomenclature) -> None:
        """
        Инициализация сервиса постобработки

        Args:
            data (list): Список объектов рецептов
            nomenclature: Объект номенклатуры, связанный с постобработкой
        """
        super().__init__(data)
        self.nomenclature = nomenclature
        # storage_observer.observers.append(self)

    def handle_event(self, handle_type: str):
        """
        Обработка событий от наблюдателя

        Args:
            handle_type (str): Тип события
        """
        if handle_type == event_type.nomenclature_deleted():
            self.nomenclature_deleted()

    def nomenclature_deleted(self, nomenclature: nomenclature_model):
        """
        Обработка удаления номенклатуры: удаляет строку из рецепта, если она ссылается на номенклатуру

        Args:
            nomenclature (nomenclature_model): Удаляемая номенклатура
        """
        for recipe in self.data:
            if self.nomenclature.name in recipe._rows:
                del recipe._rows[self.nomenclature.name]
                recipe.__calc_brutto()
