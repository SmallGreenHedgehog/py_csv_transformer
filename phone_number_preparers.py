from abc import abstractmethod


class PhoneNumber:
    """Базовый класс для различных подготовок телефонных номеров

    _phone_number - обрабатываемое свойство номера телефона,
    возвращается в переопределяемом свойстве-методе prepared_phone_number

    """
    _src_phone_number = ''
    _phone_number = ''

    def set_src_phone_number(self, src_phone_number):
        """Сеттер исходного номера"""
        self._src_phone_number = src_phone_number

    def __init__(self, src_phone_number):
        self.set_src_phone_number(src_phone_number=src_phone_number)
        self._phone_number = self._src_phone_number

    def _remove_left_symbols_from_phone_str(self):
        """Удаляет лишние символы из телефонного номер. Очистка"""
        self._phone_number = ''.join(s for s in self._phone_number if s in '0123456789')

    def _replace_eight_to_seven_for_11_digit(self):
        """Заменяем восьмерку на семерку в 11 значных номерах, нач. с 89. Выполнять после очистки"""
        if len(self._phone_number) == 11 and self._phone_number[0:2] == '89':
            self._phone_number = '7' + self._phone_number[1:]

    def _append_seven_for_10_digit(self):
        """Добавляет семерку для десятизначных номеров, начинающихся с девяки"""
        if len(self._phone_number) == 10 and self._phone_number[0] == '9':
            self._phone_number = '7' + self._phone_number

    def _append_plus_at_start_with_seven(self):
        """Добавляет + в начало номера для 11 значных номеров, нач. с 79. Выполнять после очистки"""
        if len(self._phone_number) == 11 and self._phone_number[0:2] == '79':
            self._phone_number = '+' + self._phone_number

    @abstractmethod
    def prepare_phone_number(self):
        """Абстрактный метод для подготовки телефонного номера в наследниках"""
        pass

    @property
    def prepared_phone_number(self):
        """Подготавливает и возвращает удобный телефонный номер"""
        self.prepare_phone_number()
        return self._phone_number


class PhoneNumberForRingerDog(PhoneNumber):
    def prepare_phone_number(self):
        """Подготавливает номер телефона для звонопса"""
        self._remove_left_symbols_from_phone_str()
        self._replace_eight_to_seven_for_11_digit()
        self._append_seven_for_10_digit()
        self._append_plus_at_start_with_seven()
