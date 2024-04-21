from Src.reference import reference


""" Типы событий """

class event_type(reference):



    @staticmethod
    def changed_block_period() -> str:

        """ Событие изменения даты блокировки """
        return "changed_block_period"