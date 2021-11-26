from abc import abstractmethod
from csv import unix_dialect, register_dialect
from csv import DictReader, DictWriter
from os import getcwd, listdir
from os.path import abspath


class BASECSVFileExtractor:
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

    def __init__(self, src_file_path, dst_dir_path):
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


def get_paths_of_files_in_source_folder() -> tuple:
    """Возвращает перечень csv в src директории"""
    source_dir_path = abspath(getcwd() + '/source_csv_files')
    files_in_src_dir = filter(lambda f: f.endswith('csv'), listdir(source_dir_path))
    return tuple(f'{source_dir_path}/{cur_file}' for cur_file in files_in_src_dir)


if __name__ == '__main__':
    try:
        dst_dir_path = abspath(getcwd() + '/result_csv_files')
        for cur_file_path in get_paths_of_files_in_source_folder():
            BASECSVFileExtractor(src_file_path=cur_file_path, dst_dir_path=dst_dir_path).extract_data_to_result_file()
    except Exception as e:
        print(f'Ошибка выполнения обработки конвертации: {e}')
