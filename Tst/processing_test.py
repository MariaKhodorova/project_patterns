import unittest
from Src.Logics.start_factory import start_factory
from Src.settings_manager import settings_manager
from Src.Logics.process_factory import process_factory
from Src.Storage.storage import storage
from Src.Logics.Processings.processing import processing
from Src.Models.storage_row_turn_model import storage_row_turn_model
from Src.exceptions import operation_exception
from Src.Models.storage_model import storage_model
from Src.Models.unit_model import unit_model

class ProcessingTest(unittest.TestCase):

    def test_check_process_factory(self):
        """Проверить работу фабрики процессов и запуск расчета складских оборотов."""
        # Подготовка
        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()
        factory = process_factory()

        # Действие
        result = factory.create(process_factory.turn_key())

        # Проверка
        self.assertIsNotNone(result, "Фабрика процессов не создала процесс!")

    def test_check_process_turns(self):
        """Проверить работу процесса расчета оборотов."""
        # Подготовка
        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()
        factory = process_factory()
        key = storage.storage_transaction_key()
        transactions = start.storage.data[key]
        processing = factory.create(process_factory.turn_key())

        # Действие
        result = processing().process(transactions)

        # Проверка
        self.assertIsNotNone(result, "Результат расчета оборотов пуст!")
        self.assertGreater(len(result), 0, "Обороты не были рассчитаны!")
        
        # Проверка конкретного оборота
        turn = next((x for x in result if x.nomenclature.name == "Сыр Пармезан"), None)
        self.assertIsNotNone(turn, "Не найден оборот для номенклатуры 'Сыр Пармезан'")
        self.assertEqual(turn.value, 0.5, "Значение оборота для 'Сыр Пармезан' некорректно!")

    def test_check_aggregate_turns(self):
        """Проверить работу агрегирования оборотов."""
        # Подготовка
        default_storage = storage_model.create_default()
        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()
        nomenclatures = start.storage.data[storage.nomenclature_key()]
        self.assertGreater(len(nomenclatures), 0, "Список номенклатуры пуст!")

        # Создаем тестовый оборот и добавляем его в хранилище
        turn = storage_row_turn_model()
        turn.nomenclature = nomenclatures[0]
        turn.storage = default_storage
        turn.unit = unit_model.create_killogram()
        turn.value = 1

        start.storage.data[storage.blocked_turns_key()] = [turn]

        # Получаем процессы агрегации и расчета оборотов
        factory = process_factory()
        aggregate_processing = factory.create(process_factory.aggregate_key())
        turn_processing = factory.create(process_factory.turn_key())
        calculated_turns = turn_processing().process(start.storage.data[storage.storage_transaction_key()])
        calculated_len = len(calculated_turns)

        # Действие
        result = aggregate_processing().process(calculated_turns)

        # Проверки
        self.assertIsNotNone(result, "Результат агрегации оборотов пуст!")
        self.assertEqual(len(result), calculated_len + 1, "Количество агрегированных оборотов некорректно!")



