from _csv import register_dialect
from abc import abstractmethod
from csv import unix_dialect, DictReader, DictWriter

from phone_number_preparers import PhoneNumberForRingerDog
from transformers_mixins import CSVFileTransformerWithReusableFieldsMixin, CSVFileTransformerWithPhonesMixin


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


class LeadConvToRingerDogCSVFileTransformer(
    CSVFileTransformerWithReusableFieldsMixin,
    CSVFileTransformerWithPhonesMixin,
    BASECSVFileTransformer
):
    def __init__(self, src_file_path, dst_dir_path, reusable_field_names_tuple=(), *args, **kwargs):
        super(LeadConvToRingerDogCSVFileTransformer, self).__init__(
            src_file_path=src_file_path,
            dst_dir_path=dst_dir_path,
            reusable_field_names_tuple=reusable_field_names_tuple,
            phone_number_class=PhoneNumberForRingerDog,
            *args, **kwargs
        )

    def _prepare_data_in_list_of_dict(self):
        """Подготавливает данные из лид конвертера для звонопса"""
        prepared_csv_file_list_of_dict = []
        for cur_dict in self._csv_file_list_of_dict:
            res_phone = self.prepare_phone_number_string(src_phone_str=cur_dict.get('phone'))
            if len(res_phone) > 0:
                new_dict = {}

                self.append_reusable_fields_to_new_dict(cur_dict=cur_dict, new_dict=new_dict)
                new_dict['phone'] = res_phone

                prepared_csv_file_list_of_dict.append(new_dict)
            self._csv_file_list_of_dict = prepared_csv_file_list_of_dict
