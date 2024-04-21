from Src.Logics.Services.service import service
from Src.exceptions import exception_proxy, operation_exception
from Src.reference import reference
from Src.Logics.Services.storage_observer import storage_observer
from Src.Models.event_type import event_type
from Src.Logics.Services.post_processing_service import post_processing_service
from Src.Models.event_type import event_type

#
# Сервис для выполнения CRUD операций
#
class reference_service(service):

    def __init__(self, data: list) -> None:
        super().__init__(data)
        storage_observer.observers.append(self)
        post_processing_service.observers.append(self)

    def add(self, item: reference) -> bool:
        """
            Добавить новый элемент
        """
        exception_proxy.validate(item, reference)
        found = list(filter(lambda x: x.id == item.id , self.data))     
        if len(found) > 0:
            return False
        
        self.data.append(item)
        return True
    
    def delete(self, item:reference) -> bool:
        """
            Удалить элемент
        """
        exception_proxy.validate(item, reference)
        found = list(filter(lambda x: x.id == item.id , self.data))     
        if len(found) == 0:
            return False
        
        # вызвать событие
        
        self.data.remove(found[0])
        storage_observer.raise_event(event_type.nomenclature_deleted())
        return True

    def change(self, item:reference) -> bool:
        """
            Изменить элемент
        """
        exception_proxy.validate(item, reference)
        found = list(filter(lambda x: x.id == item.id , self.data))     
        if len(found) == 0:
            return False
        
        self.delete(found[0])
        self.add(item)
        return True
    
    def get(self) -> list:
        """
            Вернуть список 
        """
        return self.data
    
    def get_item(self, id: str) -> reference:
        """
            Вернуть элемент
        """
        exception_proxy.validate(id, str)
        found = list(filter(lambda x: x.id == id , self.data))     
        if len(found) == 0:
            raise operation_exception(f"Не найден элемент с кодом {id}!")
        
        return found
    

    def handle_event( self, event_type: str ):
        """ Обработать события"""

        super().handle_event(event_type)

