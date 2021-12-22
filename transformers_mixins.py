from preparers_for_full_names import FullName
from preparers_for_phone_number import PhoneNumber


class CSVFileTransformerWithReusableFieldsMixin:
    """Миксин для подготовки csv с переносимыми полями"""
    _reusable_field_names_tuple = ()

    def set_reusable_field_names_tuple(self, reusable_field_names_tuple):
        """Сеттер списка переносимых полей из исходного csv в результирующий"""
        self._reusable_field_names_tuple = reusable_field_names_tuple

    def append_reusable_fields_to_new_dict(self, cur_dict, new_dict):
        """Переносит переиспользуемые поля из исходного csv в результирующий"""
        for cur_field_name in self._reusable_field_names_tuple:
            new_dict[cur_field_name] = cur_dict.get(cur_field_name)

    def __init__(self, src_file_path, dst_dir_path, reusable_field_names_tuple=(), *args, **kwargs):
        self.set_reusable_field_names_tuple(reusable_field_names_tuple=reusable_field_names_tuple)
        super(CSVFileTransformerWithReusableFieldsMixin, self).__init__(
            src_file_path=src_file_path,
            dst_dir_path=dst_dir_path,
            *args, **kwargs
        )


class CSVFileTransformerWithPhonesMixin:
    """Миксин для подготовки CSV с телефонами"""
    _phone_number_class = None

    def set_phone_number_class(self, phone_number_class):
        """Сеттер класса для подготовки номера телефона"""
        self._phone_number_class = phone_number_class

    def prepared_phone_number_string(self, src_phone_str) -> str:
        """Возвращает приготовленную строку номера телефона, согласно установленного класса"""
        if not self._phone_number_class:
            raise AttributeError('Аттрибут "_phone_number_class" должен быть установлен методом set_phone_number_class')
        return self._phone_number_class(src_phone_number=src_phone_str).prepared_phone_number

    def __init__(self, src_file_path, dst_dir_path,
                 reusable_field_names_tuple=(),
                 phone_number_class=PhoneNumber,
                 *args, **kwargs
                 ):
        self.set_phone_number_class(phone_number_class=phone_number_class)
        super(CSVFileTransformerWithPhonesMixin, self).__init__(
            src_file_path=src_file_path,
            dst_dir_path=dst_dir_path,
            reusable_field_names_tuple=reusable_field_names_tuple,
            *args, **kwargs
        )


class CSVFileTransformerWithFullNames:
    """Миксин для подготовки CSV с разделением полных имен"""

    _full_names_class = None

    def set_full_names_class(self, full_names_class):
        """Сеттер класса для для разделения полных имен"""
        self._full_names_class = full_names_class

    def get_full_name_obj(self, src_full_name) -> FullName:
        """Возвращает приготовленную строку номера телефона, согласно установленного класса"""
        if not self._full_names_class:
            raise AttributeError('Аттрибут "_full_names_class" должен быть установлен методом set_full_names_class')
        return self._full_names_class(src_full_name=src_full_name)

    def __init__(self, src_file_path, dst_dir_path,
                 full_names_class=FullName,
                 *args, **kwargs
                 ):
        self.set_full_names_class(full_names_class=full_names_class)
        super(CSVFileTransformerWithFullNames, self).__init__(
            src_file_path=src_file_path,
            dst_dir_path=dst_dir_path,
            *args, **kwargs
        )
