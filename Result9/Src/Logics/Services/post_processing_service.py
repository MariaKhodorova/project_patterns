from Src.Logics.Services.service import service
from Src.Logics.Services.storage_observer import storage_observer
from Src.Storage.storage import storage
from Src.Logics.Services.storage_observer import event_type
from Src.Models.nomenclature_model import nomenclature_model


class post_processing_service(service):

    def __init__(self, data: list, nomenclature) -> None:

        super().__init__(data)

        self.nomenclature = nomenclature
        storage_observer.observers.append(self)


    def handle_event(self, handle_type: str):
        if handle_type == event_type.nomenclature_deleted():
            self.nomenclature_deleted()


    def nomenclature_deleted(self, nomenclature: nomenclature_model):
        for recipe in self.data:
            if self.nomenclature in recipe._rows:
                del recipe._rows[self.nomenclature]
                recipe.__calc_brutto()

