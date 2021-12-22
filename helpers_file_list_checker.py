from abc import abstractmethod

from helpers_singleton import SingletonMeta
from helpers_mixins import CSVFileReaderMixin


class ListChecker(metaclass=SingletonMeta):
    """Класс для проверки вхождения значений в список"""
    _list_for_check = []

    @abstractmethod
    def _init_list(self, *args, **kwargs):
        """Абстракный метод для инициализации списков в наследниках"""

    def __init__(self, *args, **kwargs):
        self._init_list(*args, **kwargs)

    def check_value(self, value):
        """Проверяет вхождение значения в список"""
        return True if value in self._list_for_check else False


class StrListChecker(ListChecker):
    @abstractmethod
    def _init_list(self, *args, **kwargs):
        """Абстракный метод для инициализации списков в наследниках"""

    def check_value(self, value):
        """Проверяет вхождение значения в список"""
        return True if str(value).lower().strip() in self._list_for_check else False


class ListCheckerFromCSVNamesFile(CSVFileReaderMixin, StrListChecker):
    def _init_list(self, *args, **kwargs):
        """Инициализирует список из выбранной колонки csv файла"""
        column_name = kwargs.get('column_name')
        column_name = column_name if column_name else 'Name'

        for cur_line in self._csv_file_list_of_dict:
            cur_name = cur_line.get(column_name)
            if cur_name:
                self._list_for_check.append(str(cur_name).lower().strip())
