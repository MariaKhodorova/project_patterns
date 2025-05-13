from Src.reference import reference


""" Типы событий """

class event_type(reference):


    @staticmethod
    def changed_block_period() -> str:

        """
            Событие изменения даты блокировки
        """
        return "changed_block_period"
    
    @staticmethod
    def nomenclature_deleted() -> str:
        """
            Событие удаления номенклатуры из рецептов
        """
        return "nomenclature_deleted"