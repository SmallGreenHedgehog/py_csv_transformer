from abc import abstractmethod
from os import getcwd
from os.path import abspath

from helpers_file_list_checker import ListCheckerFromCSVNamesFile


class FullName:
    """Класс для подготовки (разбиения на имя/фамилию) полных имен"""

    _src_full_name = ''
    _without_extra_spaces_full_name = ''

    _first_name = ''
    _middle_name = ''
    _last_name = ''

    def set_src_full_name(self, src_full_name):
        """Устанавливает свойство строки полного имени"""
        self._src_full_name = src_full_name

    def _init_without_extra_spaces_full_name(self):
        """Инициализация свойства пролного имени без табуляций и лишних пробелов

        Заменяет табуляции на пробелы,
        удаляет лишние пробелы

        """
        self._without_extra_spaces_full_name = ' '.join(self._src_full_name.replace('\t', ' ').split())

    @abstractmethod
    def prepare_separate_parts_of_fullname(self):
        """Абстрактный метод для подготовки отдельных частей имени в наследниках"""
        pass

    def __init__(self, src_full_name: str, *args, **kwargs):
        self.set_src_full_name(src_full_name=src_full_name)
        self._init_without_extra_spaces_full_name()
        self.prepare_separate_parts_of_fullname()

    @property
    def first_name(self):
        """Возвращает имя, приготовленное на базе полного имени"""
        return self._first_name

    @property
    def middle_name(self):
        """Возвращает отчество, приготовленное на базе полного имени"""
        return self._middle_name

    @property
    def last_name(self):
        """Возвращает имя, приготовленное на базе полного имени"""
        return self._last_name


class FullNameFromDavidPlatform(FullName):
    _nature_names_list_checker = None

    def _init_nature_names_list_checker(self):
        nature_names_file_path = abspath(getcwd() + '/csv_dict_helpers/nature_names.csv')
        self._nature_names_list_checker = ListCheckerFromCSVNamesFile(
            src_file_path=nature_names_file_path,
            column_name='Name',
        )

    def __init__(self, *args, **kwargs):
        self._init_nature_names_list_checker()
        super(FullNameFromDavidPlatform, self).__init__(*args, **kwargs)

    def _check_first_name(self, first_name):
        """Проверяет имя по справочнику"""
        return self._nature_names_list_checker.check_value(first_name)

    def _prepare_first_name(self):
        """Готовит свойство имени"""
        self._first_name = self._without_extra_spaces_full_name

        full_name_words_list = self._without_extra_spaces_full_name.split()
        for cur_word in full_name_words_list:
            if self._check_first_name(cur_word):
                self._first_name = cur_word
                break

    def _prepare_last_name(self):
        """Готовит свойство фамилии

        Присваивает свойству _last_name
        оставшуюся часть полного имени,
        после удаления _first_name

        """
        self._last_name = self._without_extra_spaces_full_name.replace(self._first_name, '').strip()

    def prepare_separate_parts_of_fullname(self):
        """Готовит отдельные поля имени и фамилии"""
        self._prepare_first_name()
        self._prepare_last_name()
