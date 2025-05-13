import unittest
from Src.Logics.start_factory import start_factory
from Src.settings_manager import settings_manager
from Src.Storage.storage import storage
from Src.Logics.report_factory import report_factory

class FactoryTest(unittest.TestCase):

    def test_check_method_storage_keys(self):
        """Проверить метод storage_keys в хранилище."""
        # Подготовка
        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()

        # Действие
        result = start.storage.storage_keys(start.storage)

        # Проверки
        self.assertIsNotNone(result, "Метод storage_keys вернул None!")
        self.assertGreater(len(result), 0, "Метод storage_keys вернул пустой список!")

    def test_check_report_factory_create(self):
        """Проверка работы фабрики для построения отчетности."""
        # Подготовка
        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()
        factory = report_factory()
        key = storage.unit_key()

        # Действие
        report = factory.create(manager.settings.report_mode, start.storage.data)

        # Проверки
        self.assertIsNotNone(report, "Фабрика отчетности не создала отчет!")
        self.assertIsNotNone(report.create(key), "Отчет не был создан для ключа!")

    def test_check_create_receipts(self):
        """Проверка создания начальных рецептов."""
        # Подготовка
        items = start_factory.create_receipts()

        # Проверки
        self.assertGreater(len(items), 0, "Рецепты не были созданы!")

    def test_check_create_nomenclatures(self):
        """Проверка создания начальной номенклатуры."""
        # Подготовка
        items = start_factory.create_nomenclatures()

        # Проверки
        self.assertGreater(len(items), 0, "Номенклатура не была создана!")

    def test_check_create_units(self):
        """Проверка создания списка единиц измерения."""
        # Подготовка
        items = start_factory.create_units()

        # Проверки
        self.assertGreater(len(items), 0, "Единицы измерения не были созданы!")

    def test_check_create_groups(self):
        """Проверка создания списка групп."""
        # Подготовка
        items = start_factory.create_groups()

        # Проверки
        self.assertGreater(len(items), 0, "Группы не были созданы!")

    def test_check_factory_create(self):
        """Проверка работы метода create класса start_factory."""
        # Подготовка
        manager = settings_manager()
        factory = start_factory(manager.settings)

        # Действие
        factory.create()

        # Проверки
        self.assertIsNotNone(factory.storage, "Хранилище не было создано!")
        self.assertIn(storage.nomenclature_key(), factory.storage.data, "Ключ номенклатуры не найден в данных!")
        self.assertIn(storage.receipt_key(), factory.storage.data, "Ключ рецепта не найден в данных!")
        self.assertIn(storage.group_key(), factory.storage.data, "Ключ группы не найден в данных!")
        self.assertIn(storage.unit_key(), factory.storage.data, "Ключ единиц измерения не найден в данных!")
        self.assertIn(storage.storage_transaction_key(), factory.storage.data, "Ключ транзакций не найден в данных!")
