from Src.errors import error_proxy
from Src.Storage.storage import storage
from Src.Logics.Services.storage_observer import storage_observer
from Src.Logics.Services.service import service
from Src.Models.event_type import event_type
from Src.Logics.convert_factory import reference_convertor
import json

class logging(service):
    __storage = None
    __log = None
    __save_path = './logs.txt'
    __save_path_json = './logs.json'

    def __init__(self):
        self.__storage = storage()
        storage_observer.observers.append(self)

    def handle_event(self, event: str):
        event = event.split(' ')
        if event[0] == event_type.make_log_key():
            self._create_log(event[1], event[2], event[3])
            self._save_log()

    def _create_log(self, log_type: str, text: str, source: str):
        self.__log = error_proxy(text, source)
        self.__log.log_type = log_type
        print(list(self.__storage.data.keys()))
        self.__storage.data[storage.logs_key()].append(self.__log)

    def _save_log(self):
        ref = reference_convertor(error_proxy)
        ref = ref.convert(self.__log)
        get = None
        to_write = json.dumps(ref, ensure_ascii=False)

        with open(self.__save_path, 'a') as saved:
            if saved.tell() != 0:
                saved.write('\n')
            saved.write(to_write)

        with open(self.__save_path_json, 'a') as saved_json:
            if saved_json.tell() != 0:
                saved_json.write('\n')
            get = json.load(saved_json)
            get['logs'].append(to_write)
            saved_json.seek(0)
            json.dump(get, saved_json)


