import uuid
import unittest
from datetime import datetime

from Src.Logics.Services.storage_service import storage_service
from Src.Logics.Services.reference_service import reference_service
from Src.Logics.Services.post_processing_service import post_processing_service
from Src.Logics.Services.storage_observer import storage_observer

from Src.Logics.start_factory import start_factory
from Src.Logics.convert_factory import convert_factory

from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.event_type import event_type

from Src.settings_manager import settings_manager
from Src.Storage.storage import storage
from Src.exceptions import operation_exception


class ServiceTest(unittest.TestCase):
    def test_add_item_to_reference(self):
        """
        Проверяет, что добавление нового элемента в справочник проходит успешно.
        """
        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()

        key = storage.nomenclature_key()
        data = start.storage.data[key]
        converter = convert_factory()

        # Убедимся, что набор данных не пуст
        self.assertGreater(len(data), 0, "Некорректно сформирован набор данных!")

        # Сериализация элемента и создание модели
        serialized = converter.serialize(data[0])
        item = nomenclature_model().load(serialized)
        item.id = uuid.uuid4()  # Генерация нового уникального ID для элемента

        service = reference_service(data)
        start_len = len(data)

        # Добавляем элемент в справочник и проверяем результат
        result = service.add(item)

        # Проверяем, что элемент добавлен в справочник
        self.assertTrue(result)
        self.assertEqual(len(data), start_len + 1)

    def test_change_item_in_reference(self):
        """
        Проверяет, что изменение элемента справочника происходит корректно.
        """
        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()

        key = storage.nomenclature_key()
        data = start.storage.data[key]
        converter = convert_factory()

        # Убедимся, что набор данных не пуст
        self.assertGreater(len(data), 0, "Некорректно сформирован набор данных!")

        # Сериализация элемента и создание модели
        serialized = converter.serialize(data[0])
        item = nomenclature_model().load(serialized)
        item.name = "test"  # Изменяем имя элемента

        service = reference_service(data)
        start_len = len(data)

        # Применяем изменение и проверяем результат
        result = service.change(item)

        # Проверяем, что элемент был изменен
        self.assertTrue(result)
        self.assertEqual(len(data), start_len)

    def test_create_turns(self):
        """
        Проверяет создание временных интервалов (turns) в хранилище данных.
        """
        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()

        key = storage.storage_transaction_key()
        data = start.storage.data[key]

        service = storage_service(data)
        start_date = datetime(2024, 1, 1)
        stop_date = datetime(2024, 1, 10)

        # Создаем временные интервалы и проверяем результат
        result = service.create_turns(start_date, stop_date)

        self.assertGreater(len(result), 0)

    def test_create_turns_by_nomenclature(self):
        """
        Проверяет создание временных интервалов для определенной номенклатуры.
        """
        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()

        key = storage.storage_transaction_key()
        data = start.storage.data[key]

        self.assertGreater(len(data), 0, "Набор данных пуст!")

        service = storage_service(data)
        nomenclature = data[0].nomenclature

        # Создаем временные интервалы для номенклатуры и проверяем результат
        result = service.create_turns_by_nomenclature(
            datetime(2024, 1, 1), datetime(2024, 1, 30), nomenclature
        )

        self.assertEqual(len(result), 1)

    def test_create_turns_only_nomenclature(self):
        """
        Проверяет создание временных интервалов только для номенклатуры.
        """
        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()

        key = storage.storage_transaction_key()
        data = start.storage.data[key]

        self.assertGreater(len(data), 0, "Набор данных пуст!")

        service = storage_service(data)
        result = service.create_turns_only_nomenclature(data[0].nomenclature)

        # Проверяем, что были созданы временные интервалы
        self.assertGreater(len(result), 0)

    def test_create_turns_by_receipt(self):
        """
        Проверяет создание временных интервалов по данным рецептов.
        """
        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()

        transactions_key = storage.storage_transaction_key()
        transactions_data = start.storage.data[transactions_key]

        receipts_key = storage.receipt_key()
        receipts_data = start.storage.data[receipts_key]

        self.assertGreater(len(transactions_data), 0, "Набор данных пуст!")
        self.assertGreater(len(receipts_data), 0, "Набор данных пуст!")

        service = storage_service(transactions_data)
        result = service.create_turns_by_receipt(receipts_data[0])

        # Проверяем, что были созданы временные интервалы
        self.assertGreater(len(result), 0)

    def test_build_debits_by_receipt_should_fail(self):
        """
        Проверяет, что при неверном рецепте возникает исключение при построении дебетов.
        """
        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()

        transactions = start.storage.data[storage.storage_transaction_key()]
        receipts = start.storage.data[storage.receipt_key()]

        self.assertGreater(len(transactions), 0)
        self.assertGreater(len(receipts), 1)

        service = storage_service(transactions)

        # Проверяем, что при ошибке в рецепте возникает исключение
        with self.assertRaises(operation_exception):
            service.build_debits_by_receipt(receipts[1])

    def test_build_debits_by_receipt_should_pass(self):
        """
        Проверяет, что при корректном рецепте дебеты строятся правильно.
        """
        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()

        transactions = start.storage.data[storage.storage_transaction_key()]
        receipts = start.storage.data[storage.receipt_key()]

        self.assertGreater(len(transactions), 0)
        self.assertGreater(len(receipts), 0)

        service = storage_service(transactions)
        start_len = len(transactions)

        # Строим дебеты и проверяем, что количество транзакций увеличилось
        service.build_debits_by_receipt(receipts[0])
        stop_len = len(start.storage.data[storage.storage_transaction_key()])

        self.assertGreater(stop_len, start_len)

    def test_observer_blocked_period_event(self):
        """
        Проверяет, что событие изменения заблокированного периода корректно вызывается.
        """
        try:
            storage_observer.raise_event(event_type.changed_block_period())
        except Exception as e:
            self.fail(f"Observer вызвал исключение: {e}")

    def test_observer_nomenclature_deleted_event(self):
        """
        Проверяет, что событие удаления номенклатуры корректно вызывается.
        """
        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()

        nomenclature = nomenclature_model()
        service = reference_service(nomenclature)

        try:
            # Вызываем событие удаления номенклатуры
            storage_observer.raise_event(event_type.nomenclature_deleted())
            service.delete(nomenclature)
        except Exception as e:
            self.fail(f"Ошибка при удалении номенклатуры: {e}")

        # Проверяем, что номенклатура не была удалена (не зануляется объект)
        self.assertIsNotNone(nomenclature)
