from abc import abstractmethod


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

    def __init__(self, src_full_name: str):
        self.set_src_full_name(src_full_name=src_full_name)
        self._init_without_extra_spaces_full_name()

    @abstractmethod
    def prepare_separate_parts_of_fullname(self):
        """Абстрактный метод для подготовки отдельных частей имени в наследниках"""
        pass

    @property
    def first_name(self):
        """Возвращает имя, приготовленное на базе полного имени"""
        return self._first_name

    @property
    def middle_name(self):
        """Возвращает отчество, приготовленное на базе полного имени"""
        return self._first_name

    @property
    def last_name(self):
        """Возвращает имя, приготовленное на базе полного имени"""
        return self._first_name
