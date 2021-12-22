from _csv import register_dialect
from csv import unix_dialect, DictReader


class CSVFileReaderMixin:
    """Миксин для чтения csv файлов"""
    _dialect = None
    _filename = None
    _src_file_path = None
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

    def _read_csv_in_list_of_dict(self):
        """Читает данные csv в _csv_file_list_of_dict"""
        with open(self._src_file_path, 'r') as read_obj:
            dict_reader = DictReader(read_obj, dialect=self._dialect)
            self._csv_file_list_of_dict = list(dict_reader)

    def __init__(self, src_file_path, *args, **kwargs):
        self._init_dialect()
        self.set_file_path(src_file_path=src_file_path)
        self._read_csv_in_list_of_dict()
        super(CSVFileReaderMixin, self).__init__(*args, **kwargs)

