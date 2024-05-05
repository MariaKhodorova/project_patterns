from Src.Models.event_type import event_type
from Src.exceptions import exception_proxy

#
# Наблюдатель для складских операций
#
class storage_observer:
    _observers = []


    def raise_event(handle_event: str, reference = None):
        """ Сформировать события """

        exception_proxy.validate( handle_event, str )
        for object in storage_observer._observers:
            
            if object is not None:
                object.handle_event(handle_event)


