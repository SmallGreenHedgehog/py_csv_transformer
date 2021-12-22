from _csv import register_dialect, QUOTE_MINIMAL
from abc import abstractmethod
from csv import DictWriter, unix_dialect

from helpers_mixins import CSVFileReaderMixin
from preparers_for_full_names import FullNameFromDavidPlatform
from preparers_for_phone_number import PhoneNumberForRingerDog
from transformers_mixins import CSVFileTransformerWithReusableFieldsMixin, CSVFileTransformerWithPhonesMixin, \
    CSVFileTransformerWithFullNames


class BASEFileTransformer:
    _dst_dir_path = None

    def set_dst_dir_path(self, dst_dir_path):
        """Сеттер пути результирующей директории"""
        self._dst_dir_path = dst_dir_path

    def __init__(self, dst_dir_path, *args, **kwargs):
        self.set_dst_dir_path(dst_dir_path=dst_dir_path)

    @abstractmethod
    def _prepare_data_for_export(self):
        """Метод для подготовки данных"""
        pass

    @abstractmethod
    def _save_prepared_data_file(self):
        """Метод для сохранения подготовленных данных"""
        pass

    def extract_data_to_result_file(self):
        """Готовит результирующий файл"""
        self._prepare_data_for_export()
        self._save_prepared_data_file()


class BASECSVFileTransformer(CSVFileReaderMixin, BASEFileTransformer):
    """Класс, управляющий преобразованием csv файлов"""

    def __init__(self, src_file_path, *args, **kwargs):
        super(BASECSVFileTransformer, self).__init__(src_file_path=src_file_path, *args, **kwargs)

    @abstractmethod
    def _prepare_data_for_export(self):
        """Метод для подготовки данных"""
        pass

    def _save_prepared_data_file(self):
        """Пишет обработанные данные в результирующую директорию"""
        result_csv_file = f'{self._dst_dir_path}/{self._filename}'
        with open(result_csv_file, 'w') as write_obj:
            dict_writer = DictWriter(write_obj, dialect=self._dialect, fieldnames=self._csv_file_list_of_dict[0].keys())
            dict_writer.writeheader()
            dict_writer.writerows(self._csv_file_list_of_dict)


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

    def _prepare_data_for_export(self):
        """Подготавливает данные из лид конвертера для звонопса"""
        prepared_csv_file_list_of_dict = []
        for cur_dict in self._csv_file_list_of_dict:
            res_phone = self.prepared_phone_number_string(src_phone_str=cur_dict.get('phone'))
            if len(res_phone) > 0:
                new_dict = {}

                self.append_reusable_fields_to_new_dict(cur_dict=cur_dict, new_dict=new_dict)
                new_dict['phone'] = res_phone

                prepared_csv_file_list_of_dict.append(new_dict)
            self._csv_file_list_of_dict = prepared_csv_file_list_of_dict


class DavidPlatformToLeadConvSubscriptionTransformer(
    CSVFileTransformerWithReusableFieldsMixin,
    CSVFileTransformerWithFullNames,
    BASECSVFileTransformer
):
    def _init_dialect(self):
        class LeadConvSubscriptionsDialect(unix_dialect):
            """Describe the usual properties of Unix-generated CSV files."""
            delimiter = ','
            quoting = QUOTE_MINIMAL

        register_dialect("lead_conv_subscriptions", LeadConvSubscriptionsDialect)
        self._dialect = 'lead_conv_subscriptions'

    def __init__(
            self, src_file_path, dst_dir_path,
            reusable_field_names_tuple=(
                    'ident', 'type', 'id', 'channel_id', 'system_id',
                    'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term',
                    'created_at', 'updated_at'
            ),
            *args, **kwargs
    ):
        super(DavidPlatformToLeadConvSubscriptionTransformer, self).__init__(
            src_file_path=src_file_path,
            dst_dir_path=dst_dir_path,
            reusable_field_names_tuple=reusable_field_names_tuple,
            full_names_class=FullNameFromDavidPlatform,
            *args, **kwargs
        )

    def _prepare_data_for_export(self):
        """Подготавливает данные подписок из платформы Давида для лид конвертера"""
        prepared_csv_file_list_of_dict = []
        for cur_dict in self._csv_file_list_of_dict:
            new_dict = {}

            self.append_reusable_fields_to_new_dict(cur_dict=cur_dict, new_dict=new_dict)
            full_name_obj = self.get_full_name_obj(cur_dict.get('name'))
            new_dict['first_name'] = full_name_obj.first_name
            new_dict['last_name'] = full_name_obj.last_name

            prepared_csv_file_list_of_dict.append(new_dict)
        self._csv_file_list_of_dict = prepared_csv_file_list_of_dict
