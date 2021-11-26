from abc import abstractmethod
from csv import unix_dialect, register_dialect
from csv import DictReader, DictWriter
from os import getcwd, listdir
from os.path import abspath


class BasePhoneNumber:
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

    @property
    @abstractmethod
    def prepared_phone_number(self):
        """Абстрактный метод для подготовки телефонного номера в наследниках"""
        return self._phone_number


class PhoneNumber(BasePhoneNumber):
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

    @property
    def prepared_phone_number(self):
        """Метод подготавливает и возвращает удобный телефонный номер"""
        self._remove_left_symbols_from_phone_str()
        self._replace_eight_to_seven_for_11_digit()
        self._append_seven_for_10_digit()
        self._append_plus_at_start_with_seven()
        return self._phone_number


class BASECSVFileTransformer:
    """Класс, управляющий преобразованием csv файлов"""

    _dialect = None
    _filename = None
    _src_file_path = None
    _dst_dir_path = None
    _csv_file_list_of_dict = None

    def _init_dialect(self):
        class DefaultDialect(unix_dialect):
            """Describe the usual properties of Unix-generated CSV files."""
            delimiter = ';'

        register_dialect("default", DefaultDialect)
        self._dialect = 'default'

    def set_file_path(self, src_file_path):
        """Сеттер пути исходного файла и наименования файла"""
        self._src_file_path = src_file_path
        self._filename = src_file_path.rsplit('/', 1)[-1]

    def set_dst_dir_path(self, dst_dir_path):
        """Сеттер пути результирующей директории"""
        self._dst_dir_path = dst_dir_path

    def __init__(self, src_file_path, dst_dir_path, *args, **kwargs):
        self._init_dialect()
        self.set_file_path(src_file_path=src_file_path)
        self.set_dst_dir_path(dst_dir_path=dst_dir_path)

    def _read_csv_in_list_of_dict(self):
        """Читает данные csv в _csv_file_list_of_dict"""
        with open(self._src_file_path, 'r') as read_obj:
            dict_reader = DictReader(read_obj, dialect=self._dialect)
            self._csv_file_list_of_dict = list(dict_reader)

    @abstractmethod
    def _prepare_data_in_list_of_dict(self):
        """Метод для подготовки данных"""
        pass

    def _save_csv_from_updated_list_of_dict(self):
        """Пишет обработанные данные в результирующую директорию"""
        result_csv_file = f'{self._dst_dir_path}/{self._filename}'
        with open(result_csv_file, 'w') as write_obj:
            dict_writer = DictWriter(write_obj, dialect=self._dialect, fieldnames=self._csv_file_list_of_dict[0].keys())
            dict_writer.writeheader()
            dict_writer.writerows(self._csv_file_list_of_dict)

    def extract_data_to_result_file(self):
        """Готовит результирующий файл"""
        self._read_csv_in_list_of_dict()
        self._prepare_data_in_list_of_dict()
        self._save_csv_from_updated_list_of_dict()


class LeadConvToRingerDogCSVFileTransformer(BASECSVFileTransformer):
    _reusable_field_names_list = []

    def set_reusable_field_names_list(self, reusable_field_names_list):
        """Метод для установки переносимых полей из исходного csv в результирующий"""
        self._reusable_field_names_list = reusable_field_names_list

    def __init__(self, src_file_path, dst_dir_path, reusable_field_names_list=[], *args, **kwargs):
        super(LeadConvToRingerDogCSVFileTransformer, self).__init__(src_file_path, dst_dir_path, *args, **kwargs)
        self.set_reusable_field_names_list(reusable_field_names_list=reusable_field_names_list)

    def _prepare_phone_number_string(self, src_phone_str):
        """Готовит телефон для звонопса"""
        return PhoneNumber(src_phone_number=src_phone_str).prepared_phone_number

    def _append_reusable_fields_to_new_dict(self, cur_dict, new_dict):
        """Переносит переиспользуемые поля из исходного csv в результирующий"""
        for cur_field_name in self._reusable_field_names_list:
            new_dict[cur_field_name] = cur_dict.get(cur_field_name)

    def _prepare_data_in_list_of_dict(self):
        """Метод для подготовки данных из лид конвертера для звонопса"""
        prepared_csv_file_list_of_dict = []
        for cur_dict in self._csv_file_list_of_dict:
            new_dict = {}

            self._append_reusable_fields_to_new_dict(cur_dict=cur_dict, new_dict=new_dict)
            new_dict['phone'] = self._prepare_phone_number_string(cur_dict.get('phone'))

            prepared_csv_file_list_of_dict.append(new_dict)
            self._csv_file_list_of_dict = prepared_csv_file_list_of_dict


def get_paths_of_files_in_source_folder() -> tuple:
    """Возвращает перечень csv в src директории"""
    source_dir_path = abspath(getcwd() + '/source_csv_files')
    files_in_src_dir = filter(lambda f: f.endswith('csv'), listdir(source_dir_path))
    return tuple(f'{source_dir_path}/{cur_file}' for cur_file in files_in_src_dir)


if __name__ == '__main__':
    try:
        dst_dir_path = abspath(getcwd() + '/result_csv_files')
        NeededTransformer = LeadConvToRingerDogCSVFileTransformer

        for cur_file_path in get_paths_of_files_in_source_folder():
            NeededTransformer(
                src_file_path=cur_file_path,
                dst_dir_path=dst_dir_path,
                reusable_field_names_list=[
                    'first_name', 'last_name', 'channel_name',
                    'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'
                ],
            ).extract_data_to_result_file()

    except Exception as e:
        print(f'Ошибка выполнения обработки конвертации: {e}')
